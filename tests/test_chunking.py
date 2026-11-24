"""Pruebas de la segmentación del Reglamento y del TUPA."""

from ucsm_bot.chunking import MAX_CHUNK_CHARS, join_lines, split_into_chunks
from ucsm_bot.corpus import (
    EXPECTED_ARTICLES,
    EXPECTED_PROCEDURES,
    EXPECTED_SERVICES,
)


def articles(units):
    return [unit for unit in units if unit.kind == "articulo"]


def test_regulation_has_all_articles_once(regulation_units):
    numbers = [unit.article for unit in articles(regulation_units)]
    assert numbers == list(range(1, EXPECTED_ARTICLES + 1))
    assert len({unit.unit_id for unit in regulation_units}) == len(
        regulation_units
    )


def test_article_reference_does_not_create_article(regulation_units):
    art_80 = next(u for u in regulation_units if u.article == 80)
    assert "Art. 83° b." in art_80.text
    assert sum(1 for u in regulation_units if u.article == 83) == 1


def test_article_57_has_changes(regulation_units):
    art_57 = next(u for u in regulation_units if u.article == 57)
    assert art_57.has_changes
    assert art_57.notes[0]["text"]


def test_articles_have_heading_path_and_pages(regulation_units):
    for unit in articles(regulation_units):
        assert unit.heading_path and unit.heading_path[0].startswith("TÍTULO")
        assert unit.pages
        assert unit.text


def test_regulation_special_units(regulation_units):
    ids = {unit.unit_id for unit in regulation_units}
    assert {"reg-finales", "reg-transitorias", "reg-control"} <= ids


def test_tupa_counts(tupa_units):
    kinds = [unit.kind for unit in tupa_units]
    assert kinds.count("procedimiento") == EXPECTED_PROCEDURES
    assert kinds.count("servicio") == EXPECTED_SERVICES


def test_join_lines_repairs_hyphenation():
    assert join_lines(["regla-", "mento de", "estudiantes"]) == (
        "reglamento de estudiantes"
    )


def test_chunks_respect_limit_and_keep_article(regulation_units):
    for unit in regulation_units:
        for chunk in split_into_chunks(unit):
            assert chunk["unit_id"] == unit.unit_id
            assert chunk["article"] == unit.article
            longest_paragraph = max(
                (len(p) for p in unit.paragraphs), default=0
            )
            assert len(chunk["text"]) <= max(
                MAX_CHUNK_CHARS, longest_paragraph + 200
            )
