"""Generación de la tabla Power Fx para el Topic de trámites.

La tabla se incrusta en el Topic *Consulta de trámite* y también se escribe
suelta en ``copilot/topics/tabla_tupa.powerfx`` para revisarla.
"""

from pathlib import Path

from ucsm_bot.knowledge_export import format_contact


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


def write_tupa_table(entries: list[dict], topics_dir: Path) -> Path:
    """Escribir la tabla Power Fx del TUPA.

    :param entries: campos de las fichas.
    :param topics_dir: carpeta ``copilot/topics``.
    :return: ruta de ``tabla_tupa.powerfx``.
    """
    topics_dir.mkdir(parents=True, exist_ok=True)
    table_path = topics_dir / "tabla_tupa.powerfx"
    table_path.write_text(build_powerfx_table(entries), encoding="utf-8")
    return table_path
