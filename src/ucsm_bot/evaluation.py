"""Evaluación del agente: banco de preguntas, métricas y SUS.

- ``check_bank``: verifica los mínimos por categoría del banco y que los
  montos y plazos esperados coincidan con ``tupa.json``.
- ``compute_metrics``: calcula acierto de fuente, exactitud de montos y
  plazos, rechazo correcto, rúbrica y latencias desde ``results.csv``.
- ``compute_sus``: calcula el puntaje SUS por participante y el promedio.
"""

import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

import yaml

from ucsm_bot.corpus import PROCESSED_DIR, ROOT_DIR

EVAL_DIR = ROOT_DIR / "eval"
QUESTIONS_PATH = EVAL_DIR / "questions.yaml"
TUPA_JSON_PATH = PROCESSED_DIR / "tupa.json"
UNITS_PATH = PROCESSED_DIR / "units.jsonl"

MINIMUMS = {
    "total": 40,
    "reglamento": 15,
    "reglamento_titulos": 8,
    "tupa": 12,
    "combinada": 4,
    "fuera_alcance": 5,
    "sin_respuesta": 4,
}
REFUSAL_CATEGORIES = {"fuera_alcance", "sin_respuesta"}
RUBRIC_LEVELS = ("correcta", "parcial", "incorrecta", "alucinada")
RUBRIC_TARGET = 0.80
LATENCY_TARGET_P90 = 10.0
SUS_TARGET = 68.0
REFUSAL_MARKERS = (
    "fuera de mi alcance", "no encontré", "no encontre",
    "ucsm.edu.pe/normatividad", "solo respondo",
)
ARTICLE_CITATION = re.compile(r"Art(?:ículo|iculo|\.)?\s*(\d{1,3})\s*°?",
                              re.IGNORECASE)
CODE_CITATION = re.compile(r"\b(?:PA|PE|SE)[0-9A-F]{8,10}\b")
AMOUNT = re.compile(r"S/\s?([\d,]+\.\d{2})")
TERM_NUMBER = re.compile(r"(\d+)\s+d[ií]as?\s+h[áa]bil", re.IGNORECASE)


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict]:
    """Cargar las preguntas del banco.

    :param path: ruta de ``questions.yaml``.
    :return: lista de preguntas.
    """
    return yaml.safe_load(path.read_text(encoding="utf-8"))["questions"]


def load_tupa(path: Path = TUPA_JSON_PATH) -> dict[str, dict]:
    """Cargar las fichas del TUPA indexadas por código.

    :param path: ruta de ``tupa.json``.
    :return: fichas por código.
    """
    entries = json.loads(path.read_text(encoding="utf-8"))
    return {entry["code"]: entry for entry in entries}


def load_article_titles(path: Path = UNITS_PATH) -> dict[int, str]:
    """Obtener el TÍTULO del Reglamento al que pertenece cada artículo.

    :param path: ruta de ``units.jsonl``.
    :return: título (primer nivel de la ruta) por número de artículo.
    """
    titles = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            unit = json.loads(line)
            if unit["kind"] == "articulo":
                titles[unit["article"]] = unit["heading_path"][0]
    return titles


def check_bank(
    questions: list[dict], tupa: dict[str, dict], titles: dict[int, str]
) -> list[str]:
    """Verificar el banco: mínimos, ids únicos y datos esperados del TUPA.

    :param questions: preguntas del banco.
    :param tupa: fichas del TUPA por código.
    :param titles: título del Reglamento por artículo.
    :return: lista de errores (vacía si el banco es válido).
    """
    errors = []
    ids = [q["id"] for q in questions]
    duplicated = sorted({i for i in ids if ids.count(i) > 1})
    if duplicated:
        errors.append(f"Ids duplicados: {', '.join(duplicated)}")
    counts = Counter(q["category"] for q in questions)
    counts["total"] = len(questions)
    covered = {
        titles[source["article"]]
        for q in questions if q["category"] == "reglamento"
        for source in q["sources"] if "article" in source
    }
    counts["reglamento_titulos"] = len(covered)
    for key, minimum in MINIMUMS.items():
        if counts[key] < minimum:
            errors.append(f"{key}: {counts[key]} < {minimum}")
    for question in questions:
        for source in question["sources"]:
            if "article" in source and source["article"] not in titles:
                errors.append(f"{question['id']}: artículo inexistente "
                              f"{source['article']}")
            if "code" in source and source["code"] not in tupa:
                errors.append(f"{question['id']}: código inexistente "
                              f"{source['code']}")
        if question["category"] in {"tupa", "combinada"}:
            codes = [s["code"] for s in question["sources"] if "code" in s]
            if not codes:
                errors.append(f"{question['id']}: falta el código TUPA")
                continue
            entry = tupa.get(codes[0], {})
            for field, key in (("expected_fee", "fee_display"),
                               ("expected_term", "term")):
                if question.get(field) != entry.get(key):
                    errors.append(
                        f"{question['id']}: {field} "
                        f"'{question.get(field)}' ≠ '{entry.get(key)}'"
                    )
    return errors


def bank_summary(
    questions: list[dict], titles: dict[int, str]
) -> dict[str, int]:
    """Contar preguntas por categoría y títulos cubiertos.

    :param questions: preguntas del banco.
    :param titles: título del Reglamento por artículo.
    :return: conteos por categoría, total, títulos y subconjunto.
    """
    summary = dict(Counter(q["category"] for q in questions))
    summary["total"] = len(questions)
    summary["reglamento_titulos"] = len({
        titles[s["article"]] for q in questions
        if q["category"] == "reglamento" for s in q["sources"]
        if "article" in s
    })
    summary["subset"] = sum(bool(q.get("subset")) for q in questions)
    return summary


def percentile(values: list[float], fraction: float) -> float:
    """Calcular un percentil con interpolación lineal.

    :param values: valores numéricos.
    :param fraction: percentil entre 0 y 1.
    :return: percentil, o ``nan`` si no hay valores.
    """
    if not values:
        return math.nan
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def cited_sources(text: str) -> set[str]:
    """Extraer artículos y códigos citados en una respuesta.

    :param text: respuesta y fuentes citadas.
    :return: conjunto como ``{"art:83", "code:PA113073C401"}``.
    """
    sources = {f"art:{int(n)}" for n in ARTICLE_CITATION.findall(text)}
    sources |= {f"code:{code}" for code in CODE_CITATION.findall(text)}
    return sources


def expected_sources(question: dict) -> set[str]:
    """Convertir las fuentes esperadas al formato de ``cited_sources``.

    :param question: pregunta del banco.
    :return: conjunto de fuentes esperadas.
    """
    return {
        f"art:{s['article']}" if "article" in s else f"code:{s['code']}"
        for s in question["sources"]
    }


def amounts_match(expected_fee: str, text: str) -> bool:
    """Indicar si todos los montos esperados aparecen en el texto.

    :param expected_fee: monto esperado (``S/ 44.00`` o ``Gratuito``).
    :param text: respuesta y contenido de la tarjeta.
    :return: ``True`` si coinciden.
    """
    expected = AMOUNT.findall(expected_fee)
    if not expected:
        return "gratuit" in text.lower()
    found = set(AMOUNT.findall(text))
    return all(amount in found for amount in expected)


def term_matches(expected_term: str, text: str) -> bool:
    """Indicar si el plazo esperado aparece en el texto.

    :param expected_term: plazo esperado (``7 días hábiles``).
    :param text: respuesta y contenido de la tarjeta.
    :return: ``True`` si el número de días coincide.
    """
    expected = TERM_NUMBER.findall(expected_term)
    return bool(expected) and expected[0] in TERM_NUMBER.findall(text)


def is_refusal(row: dict) -> bool:
    """Indicar si la respuesta es un rechazo o derivación.

    La columna ``refused`` (sí/no), si se llenó, prevalece sobre la
    detección automática por frases del protocolo.

    :param row: fila de ``results.csv``.
    :return: ``True`` si el agente rechazó o derivó.
    """
    manual = row.get("refused", "").strip().lower()
    if manual in {"si", "sí", "yes", "1"}:
        return True
    if manual in {"no", "0"}:
        return False
    answer = row.get("answer", "").lower()
    return any(marker in answer for marker in REFUSAL_MARKERS)


def ratio(hits: int, total: int) -> float:
    """Calcular una proporción segura.

    :param hits: aciertos.
    :param total: casos.
    :return: proporción o ``nan`` si no hay casos.
    """
    return hits / total if total else math.nan


def compute_metrics(questions: list[dict], rows: list[dict]) -> dict:
    """Calcular las métricas automáticas y la rúbrica.

    :param questions: preguntas del banco.
    :param rows: filas de ``results.csv`` (``id``, ``answer``,
        ``sources_cited``, ``card_shown``, ``card_text``, ``latency_s``,
        ``rubric``, ``refused`` opcional).
    :return: métricas globales y detalle por pregunta.
    :raises ValueError: si faltan o sobran preguntas en los resultados.
    """
    by_id = {row["id"]: row for row in rows}
    missing = [q["id"] for q in questions if q["id"] not in by_id]
    unknown = sorted(set(by_id) - {q["id"] for q in questions})
    if missing or unknown:
        raise ValueError(f"Faltan: {missing}; desconocidas: {unknown}")

    detail = []
    for question in questions:
        row = by_id[question["id"]]
        text = " ".join(
            row.get(key, "") for key in ("answer", "sources_cited",
                                         "card_text")
        )
        expected = expected_sources(question)
        cited = cited_sources(text)
        item = {
            "id": question["id"],
            "category": question["category"],
            "source_hit": bool(expected & cited) if expected else None,
            "fee_ok": (amounts_match(question["expected_fee"], text)
                       if question.get("expected_fee") else None),
            "term_ok": (term_matches(question["expected_term"], text)
                        if question.get("expected_term") else None),
            "refused": is_refusal(row),
            "latency_s": float(row["latency_s"]) if row.get("latency_s")
            else None,
            "rubric": row.get("rubric", "").strip().lower(),
        }
        if question["category"] in REFUSAL_CATEGORIES:
            item["refusal_ok"] = item["refused"]
        else:
            item["refusal_ok"] = None
        detail.append(item)

    def rate(key: str) -> tuple[int, int, float]:
        values = [d[key] for d in detail if d[key] is not None]
        hits = sum(values)
        return hits, len(values), ratio(hits, len(values))

    latencies = [d["latency_s"] for d in detail if d["latency_s"] is not None]
    rubric = Counter(d["rubric"] for d in detail if d["rubric"])
    graded = sum(rubric[level] for level in RUBRIC_LEVELS)
    good = rubric["correcta"] + rubric["parcial"]
    return {
        "source_accuracy": rate("source_hit"),
        "fee_accuracy": rate("fee_ok"),
        "term_accuracy": rate("term_ok"),
        "refusal_accuracy": rate("refusal_ok"),
        "latency_p50": percentile(latencies, 0.5),
        "latency_p90": percentile(latencies, 0.9),
        "rubric": {level: rubric[level] for level in RUBRIC_LEVELS},
        "rubric_graded": graded,
        "rubric_good_rate": ratio(good, graded),
        "hallucinated": rubric["alucinada"],
        "detail": detail,
    }


def format_rate(value: tuple[int, int, float]) -> str:
    """Formatear aciertos/casos y porcentaje.

    :param value: tupla (aciertos, casos, proporción).
    :return: texto como ``12/14 (85,7 %)``.
    """
    hits, total, share = value
    if not total:
        return "sin casos"
    return f"{hits}/{total} ({share * 100:.1f} %)".replace(".", ",")


def format_seconds(value: float) -> str:
    """Formatear segundos con coma decimal.

    :param value: segundos.
    :return: texto como ``4,2 s`` o ``—``.
    """
    return "—" if math.isnan(value) else f"{value:.1f} s".replace(".", ",")


def render_report(metrics: dict) -> str:
    """Generar ``reporte.md`` con las métricas y el detalle.

    :param metrics: resultado de ``compute_metrics``.
    :return: texto Markdown.
    """
    def mark(value) -> str:
        return "—" if value is None else ("✓" if value else "✗")

    p90 = metrics["latency_p90"]
    good_rate = metrics["rubric_good_rate"]
    lines = [
        "# Reporte de evaluación",
        "",
        "Generado por `eval/compute_metrics.py` a partir de "
        "`eval/results.csv`.",
        "",
        "## Métricas",
        "",
        "| Métrica | Resultado | Meta |",
        "|---|---|---|",
        f"| Acierto de fuente | {format_rate(metrics['source_accuracy'])} | — |",
        f"| Exactitud de montos | {format_rate(metrics['fee_accuracy'])} "
        "| 100 % |",
        f"| Exactitud de plazos | {format_rate(metrics['term_accuracy'])} "
        "| 100 % |",
        f"| Rechazo correcto (fuera de alcance y sin respuesta) | "
        f"{format_rate(metrics['refusal_accuracy'])} | — |",
        f"| Latencia p50 | {format_seconds(metrics['latency_p50'])} | — |",
        f"| Latencia p90 | {format_seconds(p90)} | < 10 s "
        f"{'✓' if not math.isnan(p90) and p90 < LATENCY_TARGET_P90 else '✗'} |",
        "",
        "## Rúbrica",
        "",
        "| Calificación | Preguntas |",
        "|---|---|",
    ]
    for level, count in metrics["rubric"].items():
        lines.append(f"| {level} | {count} |")
    if metrics["rubric_graded"]:
        meets = (good_rate >= RUBRIC_TARGET
                 and metrics["hallucinated"] == 0)
        lines += [
            "",
            f"Correctas o parciales: {good_rate * 100:.1f} %".replace(
                ".", ",")
            + f" (meta ≥ 80 %); alucinadas: {metrics['hallucinated']} "
            f"(meta 0). **{'Cumple' if meets else 'No cumple'} la meta.**",
        ]
    lines += [
        "",
        "## Detalle por pregunta",
        "",
        "| Id | Categoría | Fuente | Monto | Plazo | Rechazo | Latencia | "
        "Rúbrica |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for item in metrics["detail"]:
        latency = ("—" if item["latency_s"] is None
                   else format_seconds(item["latency_s"]))
        lines.append(
            f"| {item['id']} | {item['category']} | "
            f"{mark(item['source_hit'])} | {mark(item['fee_ok'])} | "
            f"{mark(item['term_ok'])} | {mark(item['refusal_ok'])} | "
            f"{latency} | {item['rubric'] or '—'} |"
        )
    return "\n".join(lines) + "\n"


def sus_score(answers: list[int]) -> float:
    """Calcular el puntaje SUS de un participante.

    Ítems impares: respuesta − 1; pares: 5 − respuesta; suma × 2,5.

    :param answers: 10 respuestas en escala 1–5.
    :return: puntaje de 0 a 100.
    :raises ValueError: si no hay 10 respuestas entre 1 y 5.
    """
    if len(answers) != 10 or any(not 1 <= a <= 5 for a in answers):
        raise ValueError("SUS requiere 10 respuestas entre 1 y 5")
    total = sum(
        (a - 1) if index % 2 == 0 else (5 - a)
        for index, a in enumerate(answers)
    )
    return total * 2.5


def compute_sus(sus_rows: list[dict], task_rows: list[dict]) -> dict:
    """Calcular SUS por participante, promedio, éxito y tiempo por tarea.

    :param sus_rows: filas de ``sus.csv`` (``participant``, ``q1``…``q10``).
    :param task_rows: filas de ``tareas.csv`` (``participant``, ``task``,
        ``success`` sí/no, ``seconds``).
    :return: puntajes por participante, promedio y resumen por tarea.
    """
    scores = {
        row["participant"]: sus_score(
            [int(row[f"q{i}"]) for i in range(1, 11)]
        )
        for row in sus_rows
    }
    tasks: dict[str, dict] = {}
    for row in task_rows:
        task = tasks.setdefault(row["task"], {"done": 0, "total": 0,
                                              "seconds": []})
        task["total"] += 1
        task["done"] += row["success"].strip().lower() in {"si", "sí", "1",
                                                           "yes"}
        if row.get("seconds"):
            task["seconds"].append(float(row["seconds"]))
    return {
        "scores": scores,
        "mean": (sum(scores.values()) / len(scores)) if scores else math.nan,
        "tasks": {
            name: {
                "success_rate": ratio(t["done"], t["total"]),
                "mean_seconds": (sum(t["seconds"]) / len(t["seconds"])
                                 if t["seconds"] else math.nan),
            }
            for name, t in sorted(tasks.items())
        },
    }


def read_csv(path: Path) -> list[dict]:
    """Leer un CSV como lista de diccionarios.

    :param path: ruta del CSV.
    :return: filas.
    """
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
