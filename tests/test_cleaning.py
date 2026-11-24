"""Pruebas de la limpieza del Reglamento y del TUPA."""

import re

from ucsm_bot.cleaning import (
    FOOTER_PREFIXES,
    PageLine,
    flatten_table_row,
    join_spaced_letters,
    remove_footnote_marker,
    Footnote,
)


def test_regulation_has_no_footers_or_headers(regulation_clean):
    lines, _ = regulation_clean
    for line in lines:
        assert not line.text.startswith(FOOTER_PREFIXES)
        assert not re.match(r"^- \d+ de \d+ -$", line.text)
        assert "9814-CU-2026" not in line.text
        assert line.text != "TUO-EST-001 / V03"


def test_regulation_starts_after_index(regulation_clean):
    lines, _ = regulation_clean
    assert lines[0].text == "TÍTULO I"
    assert not any("...." in line.text for line in lines)


def test_every_line_has_a_valid_page(regulation_clean, tupa_clean):
    lines, _ = regulation_clean
    assert all(1 <= line.page <= 40 for line in lines)
    assert all(1 <= line.page <= 102 for line in tupa_clean)


def test_regulation_footnotes_are_detected_and_linked(regulation_clean):
    lines, footnotes = regulation_clean
    numbers = [note.number for note in footnotes]
    assert numbers == list(range(1, len(numbers) + 1))
    linked = {n for line in lines for n in line.notes}
    assert linked == set(numbers)


def test_tupa_has_no_tables_stamps_or_printed_pages(tupa_clean):
    for line in tupa_clean:
        assert "|" not in line.text
        assert "9888-CU-2026" not in line.text
        assert not re.match(r"^pág\. \d+$", line.text)
    assert tupa_clean[0].text.startswith("SECCIÓN N° 1")


def test_flatten_table_row():
    assert flatten_table_row("|---|---|") == ""
    assert flatten_table_row("| a | | b |") == "a b"
    assert flatten_table_row("texto") is None


def test_join_spaced_letters():
    assert join_spaced_letters("la d i s p o s i c i ó n") == "la disposición"


def test_remove_glued_and_trailing_markers():
    lines = [PageLine(1, "texto seleccionada9."), PageLine(1, "fin de línea 10")]
    remove_footnote_marker(lines, Footnote(9, "nota", 1))
    remove_footnote_marker(lines, Footnote(10, "nota", 1))
    assert lines[0].text == "texto seleccionada."
    assert lines[1].text == "fin de línea"
    assert lines[0].notes == [9] and lines[1].notes == [10]


def test_orphan_list_markers_are_restored(regulation_units):
    art_23 = next(u for u in regulation_units if u.article == 23)
    assert "a. Recibir formación académica" in art_23.text
    assert "b. Participar responsablemente" in art_23.text
    orphans = sum(
        paragraph.strip() in {"a.", "b.", "c.", "d."}
        for unit in regulation_units for paragraph in unit.paragraphs
    )
    assert orphans <= 5
