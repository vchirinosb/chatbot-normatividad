"""Pruebas de la extracción de campos de las fichas del TUPA."""

from ucsm_bot.corpus import EXPECTED_TUPA_ENTRIES
from ucsm_bot.tupa_fields import extract_fees


def find(entries, text):
    return next(e for e in entries if text.lower() in e["name"].lower())


def test_63_entries_with_unique_codes(tupa_entries):
    codes = [entry["code"] for entry in tupa_entries]
    assert len(codes) == EXPECTED_TUPA_ENTRIES
    assert len(set(codes)) == EXPECTED_TUPA_ENTRIES
    assert all(codes)


def test_authenticated_copy_of_degree_resolution(tupa_entries):
    entry = find(entries=tupa_entries, text="Copia autenticada de Resolución")
    assert entry["fee_display"] == "S/ 44.00"
    assert entry["term"] == "7 días hábiles"
    assert entry["contact"]["email"] == "osecgen@ucsm.edu.pe"


def test_enrollment_cancellation_is_free(tupa_entries):
    entry = find(tupa_entries, "Anulación de Matrícula")
    assert entry["fee_display"] == "Gratuito"
    assert entry["term"] == "30 días hábiles"


def test_multiple_fees_keep_their_concepts(tupa_entries):
    entry = find(tupa_entries, "Grado Académico de Maestro o Doctor")
    assert entry["fee_display"] == "Maestro: S/ 2970.00; Doctor: S/ 4433.00"
    thesis = find(tupa_entries, "Aprobación del Proyecto de Tesis - Postgrado")
    assert thesis["fee_display"] == "Maestría: Gratuito; Doctorado: Gratuito"


def test_only_known_entry_has_missing_fields(tupa_entries):
    missing = {e["name"]: e["missing_fields"] for e in tupa_entries
               if e["missing_fields"]}
    assert missing == {
        "Duplicado de Carné de Representante Estudiantil": ["submission_unit"]
    }


def test_extract_fees_strips_right_column():
    lines = [
        "Maestro",
        "Monto - S/ 2970.00 Otras opciones",
        "Agencia Bancaria: BCP",
        "Doctor del sistema ERP",
        "Monto - S/ 4433.00",
    ]
    assert extract_fees(lines) == [
        {"concept": "Maestro", "amount": "S/ 2970.00"},
        {"concept": "Doctor", "amount": "S/ 4433.00"},
    ]
