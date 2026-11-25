"""Generación de la entidad y la tabla Power Fx para el Topic de trámites.

El formato exacto que acepta el editor de Copilot Studio se verifica al
construir el agente (grupo 5); aquí se genera texto listo para pegar.
"""

import unicodedata
from pathlib import Path

import yaml

from ucsm_bot.knowledge_export import format_contact

NAME_PREFIXES_TO_DROP = ("Duplicado de ", "Copia de ", "Constancia de ")


def strip_accents(text: str) -> str:
    """Quitar tildes y pasar a minúsculas.

    :param text: texto original.
    :return: texto sin tildes en minúsculas.
    """
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    ).lower()


def build_synonyms(entry: dict) -> list[str]:
    """Generar sinónimos simples para una denominación del TUPA.

    :param entry: campos de la ficha.
    :return: sinónimos únicos y ordenados (código, nombre sin tildes, nombre
        sin paréntesis).
    """
    name = entry["name"]
    synonyms = {entry["code"].lower(), strip_accents(name)}
    if "(" in name:
        synonyms.add(strip_accents(name.split("(")[0]).strip())
    if " - " in name:
        synonyms.add(strip_accents(name.split(" - ")[0]).strip())
    synonyms.discard(name)
    return sorted(synonym for synonym in synonyms if synonym)


def build_entity(entries: list[dict]) -> dict:
    """Construir la entidad de lista cerrada de procedimientos y servicios.

    :param entries: campos de las fichas.
    :return: estructura serializable a YAML.
    """
    return {
        "kind": "ClosedListEntity",
        "displayName": "Procedimiento TUPA",
        "items": [
            {
                "id": entry["code"],
                "displayName": entry["name"],
                "synonyms": build_synonyms(entry),
            }
            for entry in entries
        ],
    }


def quote_powerfx(text: str) -> str:
    """Escapar un texto como literal de cadena Power Fx.

    :param text: texto original.
    :return: literal entre comillas dobles con comillas duplicadas.
    """
    return '"' + " ".join(text.split()).replace('"', '""') + '"'


def build_card_fields(entry: dict) -> dict[str, str]:
    """Reunir los campos que muestra la tarjeta de un trámite.

    :param entry: campos de la ficha.
    :return: código, denominación, costo, plazo, oficina, contacto y páginas.
    """
    return {
        "Code": entry["code"],
        "Name": entry["name"],
        "Fee": entry["fee_display"],
        "Term": entry["term"],
        "Office": entry["submission_unit"] or entry["approval_unit"],
        "Contact": format_contact(entry["contact"]),
        "Pages": ", ".join(str(page) for page in entry["pages"]),
    }


def build_powerfx_table(entries: list[dict]) -> str:
    """Construir la tabla Power Fx con los campos de cada ficha.

    :param entries: campos de las fichas.
    :return: expresión ``Table({...}, ...)``.
    """
    rows = []
    for entry in entries:
        body = ", ".join(
            f"{key}: {quote_powerfx(value)}"
            for key, value in build_card_fields(entry).items()
        )
        rows.append(f"    {{{body}}}")
    return "Table(\n" + ",\n".join(rows) + "\n)\n"


def write_topics(entries: list[dict], topics_dir: Path) -> dict[str, Path]:
    """Escribir la entidad YAML y la tabla Power Fx.

    :param entries: campos de las fichas.
    :param topics_dir: carpeta ``copilot/topics``.
    :return: rutas generadas por nombre.
    """
    topics_dir.mkdir(parents=True, exist_ok=True)
    entity_path = topics_dir / "entity_procedimientos.yaml"
    table_path = topics_dir / "tabla_tupa.powerfx"
    entity_path.write_text(
        yaml.safe_dump(build_entity(entries), allow_unicode=True,
                       sort_keys=False, width=100),
        encoding="utf-8",
    )
    table_path.write_text(build_powerfx_table(entries), encoding="utf-8")
    return {"entity": entity_path, "table": table_path}
