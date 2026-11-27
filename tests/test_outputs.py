"""Pruebas de los artefactos generados por ``python -m ucsm_bot.build``."""

import csv
import json
import re

import pytest
import yaml
from docx import Document as DocxDocument

from ucsm_bot.corpus import (
    EXPECTED_ARTICLES,
    EXPECTED_TUPA_ENTRIES,
    KNOWLEDGE_DIR,
    PROCESSED_DIR,
    TOPICS_DIR,
)

TUPA_JSON = PROCESSED_DIR / "tupa.json"
pytestmark = pytest.mark.skipif(
    not TUPA_JSON.exists(), reason="Ejecutar antes python -m ucsm_bot.build"
)


def heading_2_texts(path):
    return [p.text for p in DocxDocument(path).paragraphs
            if p.style.name == "Heading 2"]


@pytest.fixture(scope="module")
def tupa_json():
    return json.loads(TUPA_JSON.read_text(encoding="utf-8"))


def test_regulation_docx_has_one_heading_per_article():
    headings = heading_2_texts(KNOWLEDGE_DIR / "reglamento_estudiantes.docx")
    assert len(headings) == EXPECTED_ARTICLES
    assert all(re.match(r"^Art\. \d+°.* · págs?\. ", h) for h in headings)



def test_regulation_paragraphs_start_with_their_article():
    docx = DocxDocument(KNOWLEDGE_DIR / "reglamento_estudiantes.docx")
    article = None
    checked = 0
    for paragraph in docx.paragraphs:
        heading = re.match(r"^Art\. (\d+)°", paragraph.text)
        if paragraph.style.name == "Heading 2" and heading:
            article = heading.group(1)
        elif paragraph.style.name.startswith("Heading"):
            article = None
        elif article and not paragraph.text.startswith("Fuente:"):
            assert paragraph.text.startswith(f"Art. {article}°: "), paragraph.text
            checked += 1
    assert checked >= EXPECTED_ARTICLES

def test_tupa_docx_has_one_heading_per_entry():
    headings = heading_2_texts(KNOWLEDGE_DIR / "tupa_fichas.docx")
    assert len(headings) == EXPECTED_TUPA_ENTRIES


def test_tupa_csv_matches_json(tupa_json):
    with (KNOWLEDGE_DIR / "tupa_fichas.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["code"] for r in rows] == [e["code"] for e in tupa_json]
    assert [r["fee_display"] for r in rows] == [
        e["fee_display"] for e in tupa_json
    ]


def test_powerfx_table_fees_match_json(tupa_json):
    table = (TOPICS_DIR / "tabla_tupa.powerfx").read_text("utf-8")
    fees = re.findall(r'Fee: "((?:[^"]|"")*)"', table)
    assert len(fees) == EXPECTED_TUPA_ENTRIES
    assert [f.replace('""', '"') for f in fees] == [
        " ".join(e["fee_display"].split()) for e in tupa_json
    ]


def test_procedure_lookup_normalizes_text():
    from ucsm_bot.copilot_dialogs import STEM_LENGTH, normalize_formula

    assert normalize_formula("Name").startswith(
        'Substitute(Substitute(Substitute(Substitute(Substitute('
        'Substitute(Substitute(Substitute(Lower(Name), "á", "a")'
    )
    assert normalize_formula("Name").endswith('"-", ""), "rr", "r")')
    dialog = yaml.safe_load(
        (TOPICS_DIR / "consulta_tramite.yaml").read_text("utf-8"))
    lookup = next(
        action["value"] for action in dialog["beginDialog"]["actions"]
        if action.get("id") == "setVariable_candidatas"
    )
    assert f"Left(Value, {STEM_LENGTH}) in Key" in lookup
    assert "Exact, CountIf(palabras, Value in Key)" in lookup
    assert "Score, SortOrder.Descending" in lookup


def test_procedure_topic_asks_when_cards_tie():
    dialog = yaml.safe_load(
        (TOPICS_DIR / "consulta_tramite.yaml").read_text("utf-8"))
    actions = {action["id"]: action
               for action in dialog["beginDialog"]["actions"]}
    assert actions["setVariable_ficha"]["value"] == "=First(Topic.Candidatas)"
    branch = actions["condition_varias"]["conditions"][0]
    assert branch["condition"] == "=CountRows(Topic.Parecidas) > 1"
    steps = [step["id"] for step in branch["actions"]]
    assert steps == ["setVariable_opciones", "sendMessage_varias",
                     "question_ficha", "setVariable_eleccion"]
    # La ficha elegida reemplaza a la primera antes de mostrar la tarjeta.
    order = list(actions)
    assert order.index("condition_varias") < order.index("condition_ficha")
    assert branch["actions"][-1]["variable"] == "Topic.Ficha"
