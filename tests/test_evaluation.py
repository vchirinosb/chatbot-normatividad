"""Pruebas del banco de preguntas, las métricas y el SUS."""

import math

import pytest

from ucsm_bot.evaluation import (
    amounts_match,
    bank_summary,
    check_bank,
    cited_sources,
    compute_metrics,
    compute_sus,
    convert_forms_export,
    load_article_titles,
    load_questions,
    load_tupa,
    percentile,
    render_report,
    SUS_ITEMS,
    sus_score,
    term_matches,
)
from ucsm_bot.evaluation import TUPA_JSON_PATH

pytestmark = pytest.mark.skipif(
    not TUPA_JSON_PATH.exists(), reason="Ejecutar antes python -m ucsm_bot.build"
)


@pytest.fixture(scope="module")
def questions():
    return load_questions()


def test_bank_meets_minimums_and_matches_tupa(questions):
    titles = load_article_titles()
    assert check_bank(questions, load_tupa(), titles) == []
    summary = bank_summary(questions, titles)
    assert summary["total"] >= 40
    assert 13 <= summary["subset"] <= 17


def test_check_bank_detects_wrong_fee(questions):
    broken = [dict(q) for q in questions]
    broken[18] = {**broken[18], "expected_fee": "S/ 1.00"}
    errors = check_bank(broken, load_tupa(), load_article_titles())
    assert any("expected_fee" in error for error in errors)


def test_cited_sources():
    text = "Fuentes: Reglamento, Art. 83° (pág. 24); TUPA PA113073C401"
    assert cited_sources(text) == {"art:83", "code:PA113073C401"}


def test_cited_sources_with_article_lists():
    text = ("Fuentes: Reglamento, artículos 136° y 137° (pág. 33); "
            "Arts. 96° (pág. 26) y 97° (pág. 27); Arts. 47° y 48°.")
    assert cited_sources(text) == {"art:47", "art:48", "art:96", "art:97",
                                   "art:136", "art:137"}


def test_amount_and_term_matching():
    assert amounts_match("S/ 44.00", "Cuesta S/ 44.00 y demora")
    assert not amounts_match("S/ 44.00", "Cuesta S/ 40.00")
    assert amounts_match("Maestro: S/ 2970.00; Doctor: S/ 4433.00",
                         "S/ 2970.00 para maestro y S/4433.00 para doctor")
    assert amounts_match("Gratuito", "El trámite es gratuito")
    assert term_matches("7 días hábiles", "en 7 dias habiles")
    assert term_matches("1 día hábil", "en 1 día hábil")
    assert not term_matches("7 días hábiles", "en 5 días hábiles")


def test_percentile():
    assert percentile([1, 2, 3, 4], 0.5) == 2.5
    assert percentile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.9) == pytest.approx(9.1)
    assert math.isnan(percentile([], 0.5))


def perfect_row(question):
    """Construir una respuesta ideal para una pregunta del banco."""
    if question["category"] in {"fuera_alcance", "sin_respuesta"}:
        answer = "Esa consulta está fuera de mi alcance."
    else:
        answer = "Respuesta. " + question.get("expected_fee", "") + " " + (
            question.get("expected_term", "")
        )
    cited = "; ".join(
        f"Art. {s['article']}°" if "article" in s else s["code"]
        for s in question["sources"]
    )
    return {"id": question["id"], "answer": answer, "sources_cited": cited,
            "card_text": "", "latency_s": "4.0", "rubric": "correcta"}


def test_metrics_with_perfect_results(questions):
    metrics = compute_metrics(questions, [perfect_row(q) for q in questions])
    for key in ("source_accuracy", "fee_accuracy", "term_accuracy",
                "refusal_accuracy"):
        hits, total, share = metrics[key]
        assert total > 0 and share == 1.0, key
    assert metrics["latency_p90"] == 4.0
    assert metrics["rubric_good_rate"] == 1.0
    report = render_report(metrics)
    assert "Cumple la meta" in report
    assert report.count("| REG-") == sum(
        q["category"] == "reglamento" for q in questions
    )


def test_metrics_detect_errors(questions):
    rows = [perfect_row(q) for q in questions]
    tupa_row = next(r for r in rows if r["id"] == "TUPA-01")
    tupa_row["answer"] = "Cuesta S/ 40.00 y demora 5 días hábiles"
    out_row = next(r for r in rows if r["id"] == "OUT-03")
    out_row["answer"] = "La capital de Francia es París."
    metrics = compute_metrics(questions, rows)
    detail = {d["id"]: d for d in metrics["detail"]}
    assert detail["TUPA-01"]["fee_ok"] is False
    assert detail["TUPA-01"]["term_ok"] is False
    assert detail["OUT-03"]["refusal_ok"] is False


def test_metrics_require_one_row_per_question(questions):
    rows = [perfect_row(q) for q in questions][:-1]
    with pytest.raises(ValueError):
        compute_metrics(questions, rows)


def test_sus_score_and_summary():
    assert sus_score([5, 1] * 5) == 100.0
    assert sus_score([1, 5] * 5) == 0.0
    assert sus_score([3] * 10) == 50.0
    with pytest.raises(ValueError):
        sus_score([3] * 9)
    sus_rows = [
        {"participant": "P1", **{f"q{i}": "5" if i % 2 else "1"
                                 for i in range(1, 11)}},
        {"participant": "P2", **{f"q{i}": "3" for i in range(1, 11)}},
    ]
    task_rows = [
        {"participant": "P1", "task": "T1", "success": "sí", "seconds": "60"},
        {"participant": "P2", "task": "T1", "success": "no", "seconds": "120"},
    ]
    result = compute_sus(sus_rows, task_rows)
    assert result["mean"] == 75.0
    assert result["tasks"]["T1"] == {"success_rate": 0.5,
                                     "mean_seconds": 90.0}


def test_convert_forms_export_maps_labels_and_numbers():
    row = {"Id": "1", "Identificador del participante": " p1 "}
    labels = ["Totalmente de acuerdo", "Totalmente en desacuerdo"] * 5
    for item, label in zip(SUS_ITEMS, labels):
        row[f"Cuestionario SUS.{item}"] = label
    other = dict(row, **{"Identificador del participante": "P2"})
    for item in SUS_ITEMS:
        other[f"Cuestionario SUS.{item}"] = "Ni de acuerdo ni en desacuerdo"
    converted = convert_forms_export([row, other])
    assert converted[0]["participant"] == "P1"
    assert compute_sus(converted, [])["scores"] == {"P1": 100.0, "P2": 50.0}
    numbered = {"Identificador": "P3",
                **{f"{i}. {item}": "4" for i, item in
                   enumerate(SUS_ITEMS, start=1)}}
    assert convert_forms_export([numbered])[0]["q10"] == "4"
    with pytest.raises(ValueError):
        convert_forms_export([{"Identificador": "P4"}])
