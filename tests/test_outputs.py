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


def test_entity_has_63_items(tupa_json):
    entity = yaml.safe_load(
        (TOPICS_DIR / "entity_procedimientos.yaml").read_text("utf-8")
    )
    assert [item["id"] for item in entity["items"]] == [
        e["code"] for e in tupa_json
    ]


def test_powerfx_table_fees_match_json(tupa_json):
    table = (TOPICS_DIR / "tabla_tupa.powerfx").read_text("utf-8")
    fees = re.findall(r'Fee: "((?:[^"]|"")*)"', table)
    assert len(fees) == EXPECTED_TUPA_ENTRIES
    assert [f.replace('""', '"') for f in fees] == [
        " ".join(e["fee_display"].split()) for e in tupa_json
    ]
