"""Fixtures compartidas: el corpus se limpia y segmenta una sola vez."""

import pytest

from ucsm_bot.chunking import segment_regulation, segment_tupa
from ucsm_bot.cleaning import clean_regulation, clean_tupa
from ucsm_bot.corpus import REGULATION_ID, TUPA_ID, load_inventory
from ucsm_bot.tupa_fields import extract_tupa_fields


@pytest.fixture(scope="session")
def documents():
    """Cargar el inventario del corpus."""
    return load_inventory()


@pytest.fixture(scope="session")
def regulation_raw(documents):
    """Leer el Markdown original del Reglamento."""
    return documents[REGULATION_ID].md_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def tupa_raw(documents):
    """Leer el Markdown original del TUPA."""
    return documents[TUPA_ID].md_path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def regulation_clean(regulation_raw):
    """Limpiar el Reglamento: líneas del cuerpo y notas al pie."""
    return clean_regulation(regulation_raw)


@pytest.fixture(scope="session")
def tupa_clean(tupa_raw):
    """Limpiar el TUPA."""
    return clean_tupa(tupa_raw)


@pytest.fixture(scope="session")
def regulation_units(regulation_clean):
    """Segmentar el Reglamento en unidades."""
    lines, footnotes = regulation_clean
    return segment_regulation(lines, footnotes, REGULATION_ID)


@pytest.fixture(scope="session")
def tupa_units(tupa_clean):
    """Segmentar el TUPA en unidades."""
    return segment_tupa(tupa_clean, TUPA_ID)


@pytest.fixture(scope="session")
def tupa_entries(tupa_units):
    """Extraer los campos de las fichas del TUPA."""
    return [
        extract_tupa_fields(unit)
        for unit in tupa_units
        if unit.kind in {"procedimiento", "servicio"}
    ]
