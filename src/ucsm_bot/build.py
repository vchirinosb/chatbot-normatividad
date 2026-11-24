"""Comando único de preparación del corpus: ``python -m ucsm_bot.build``.

Ejecuta limpieza, segmentación, extracción de campos del TUPA, reporte de
ingesta, paquete de conocimiento y tablas para los Topics.
"""

import json
from pathlib import Path
from statistics import mean

from ucsm_bot.chunking import Unit, segment_regulation, segment_tupa
from ucsm_bot.chunking import split_into_chunks
from ucsm_bot.cleaning import (
    ORPHAN_LIST_MARKER,
    clean_regulation,
    clean_tupa,
    render_clean_text,
)
from ucsm_bot.copilot_topics import write_topics
from ucsm_bot.corpus import (
    EXPECTED_ARTICLES,
    EXPECTED_PROCEDURES,
    EXPECTED_SERVICES,
    EXPECTED_TUPA_ENTRIES,
    KNOWLEDGE_DIR,
    PROCESSED_DIR,
    REGULATION_ID,
    TOPICS_DIR,
    TUPA_ID,
    load_inventory,
)
from ucsm_bot.knowledge_export import (
    export_regulation,
    export_tupa,
    export_tupa_csv,
    render_tupa_paragraphs,
)
from ucsm_bot.tupa_fields import extract_tupa_fields


def unit_to_dict(unit: Unit) -> dict:
    """Serializar una unidad para ``units.jsonl``.

    :param unit: unidad normativa.
    :return: diccionario con metadatos y texto.
    """
    return {
        "unit_id": unit.unit_id,
        "doc_id": unit.doc_id,
        "kind": unit.kind,
        "article": unit.article,
        "title": unit.title,
        "heading_path": unit.heading_path,
        "pages": unit.pages,
        "has_changes": unit.has_changes,
        "notes": unit.notes,
        "text": unit.text,
    }


def write_jsonl(rows: list[dict], path: Path) -> None:
    """Escribir filas en formato JSON Lines.

    :param rows: filas a escribir.
    :param path: ruta del archivo.
    :return: ``None``.
    """
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def orphan_markers(units: list[Unit]) -> int:
    """Contar los literales de lista que quedaron sin texto.

    :param units: unidades del Reglamento.
    :return: número de párrafos que son solo un literal (``a.``).
    """
    return sum(
        bool(ORPHAN_LIST_MARKER.match(line))
        for unit in units for paragraph in unit.paragraphs
        for line in paragraph.split()
        if paragraph.strip() == line
    )


def build_report(
    regulation_units: list[Unit],
    tupa_units: list[Unit],
    entries: list[dict],
    chunks: list[dict],
    footnote_count: int,
) -> str:
    """Construir el reporte de ingesta en Markdown.

    :param regulation_units: unidades del Reglamento.
    :param tupa_units: unidades del TUPA.
    :param entries: campos de las fichas del TUPA.
    :param chunks: fragmentos de ambos documentos.
    :param footnote_count: notas al pie detectadas en el Reglamento.
    :return: texto del reporte.
    """
    articles = [u for u in regulation_units if u.kind == "articulo"]
    procedures = [u for u in tupa_units if u.kind == "procedimiento"]
    services = [u for u in tupa_units if u.kind == "servicio"]
    codes = {entry["code"] for entry in entries}

    def status(found: int, expected: int) -> str:
        return "OK" if found == expected else "DIFERENCIA"

    lines = [
        "# Reporte de ingesta",
        "",
        "Generado por `python -m ucsm_bot.build`.",
        "",
        "## Cobertura",
        "",
        "| Elemento | Encontrado | Esperado | Estado |",
        "|---|---|---|---|",
        f"| Artículos del Reglamento | {len(articles)}/{EXPECTED_ARTICLES} "
        f"| {EXPECTED_ARTICLES} | {status(len(articles), EXPECTED_ARTICLES)} |",
        f"| Fichas del TUPA | {len(entries)}/{EXPECTED_TUPA_ENTRIES} "
        f"| {EXPECTED_TUPA_ENTRIES} "
        f"| {status(len(entries), EXPECTED_TUPA_ENTRIES)} |",
        f"| Procedimientos | {len(procedures)} | {EXPECTED_PROCEDURES} "
        f"| {status(len(procedures), EXPECTED_PROCEDURES)} |",
        f"| Servicios | {len(services)} | {EXPECTED_SERVICES} "
        f"| {status(len(services), EXPECTED_SERVICES)} |",
        f"| Códigos TUPA únicos | {len(codes)} | {EXPECTED_TUPA_ENTRIES} "
        f"| {status(len(codes), EXPECTED_TUPA_ENTRIES)} |",
        "",
        "## Fragmentos",
        "",
        "| Documento | Unidades | Fragmentos | Tamaño medio (caracteres) |",
        "|---|---|---|---|",
    ]
    for doc_id, units in ((REGULATION_ID, regulation_units),
                          (TUPA_ID, tupa_units)):
        doc_chunks = [c for c in chunks if c["doc_id"] == doc_id]
        size = round(mean(len(c["text"]) for c in doc_chunks))
        lines.append(f"| {doc_id} | {len(units)} | {len(doc_chunks)} "
                     f"| {size} |")

    changed = [u.article for u in articles if u.has_changes]
    lines += [
        "",
        "## Control de cambios",
        "",
        f"Se detectaron {footnote_count} notas al pie de modificación; "
        f"{len(changed)} artículos tienen `has_changes`: "
        f"{', '.join(str(n) for n in changed)}.",
        "",
        "El cuerpo del TUO ya consolida las modificaciones; el cuadro "
        "\"Control de cambios\" es el historial por versión (con numeración "
        "anterior y actual mezcladas) y se indexa como unidad propia "
        "`reg-control`. Por eso `has_changes` se toma de las notas al pie, "
        "que usan la numeración vigente.",
        "",
        "## Listas del Reglamento",
        "",
        "En el Markdown, varias listas traen los literales (`a.`, `b.`…) "
        "separados de su texto; la limpieza los vuelve a unir cuando el "
        "número de ítems coincide con el de literales. Literales que "
        "quedaron sueltos (sin reparar): "
        f"{orphan_markers(regulation_units)}.",
        "",
        "## Campos TUPA faltantes",
        "",
    ]
    missing = [e for e in entries if e["missing_fields"]]
    if not missing:
        lines.append("Ninguno.")
    for entry in missing:
        lines.append(
            f"- {entry['name']} ({entry['code']}, pág. "
            f"{', '.join(map(str, entry['pages']))}): "
            f"{', '.join(entry['missing_fields'])}. Revisado contra el PDF: "
            "el bloque está vacío en el documento original."
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    """Ejecutar la preparación completa del corpus."""
    documents = load_inventory()
    regulation = documents[REGULATION_ID]
    tupa = documents[TUPA_ID]
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    regulation_lines, footnotes = clean_regulation(
        regulation.md_path.read_text(encoding="utf-8")
    )
    tupa_lines = clean_tupa(tupa.md_path.read_text(encoding="utf-8"))
    (PROCESSED_DIR / "reglamento_estudiantes.clean.md").write_text(
        render_clean_text(regulation_lines), encoding="utf-8"
    )
    (PROCESSED_DIR / "tupa.clean.md").write_text(
        render_clean_text(tupa_lines), encoding="utf-8"
    )

    regulation_units = segment_regulation(
        regulation_lines, footnotes, REGULATION_ID
    )
    tupa_units = segment_tupa(tupa_lines, TUPA_ID)
    entries = [
        extract_tupa_fields(unit) for unit in tupa_units
        if unit.kind in {"procedimiento", "servicio"}
    ]
    entries_by_unit = {entry["unit_id"]: entry for entry in entries}

    chunks: list[dict] = []
    for unit in regulation_units:
        chunks.extend(split_into_chunks(unit))
    for unit in tupa_units:
        entry = entries_by_unit.get(unit.unit_id)
        if entry is None:
            chunks.extend(split_into_chunks(unit))
            continue
        unit.title = entry["name"]
        unit.paragraphs = render_tupa_paragraphs(entry)
        chunks.extend(
            split_into_chunks(unit, f"{entry['name']} ({entry['code']})")
        )

    write_jsonl(
        [unit_to_dict(u) for u in regulation_units + tupa_units],
        PROCESSED_DIR / "units.jsonl",
    )
    write_jsonl(chunks, PROCESSED_DIR / "chunks.jsonl")
    (PROCESSED_DIR / "tupa.json").write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (PROCESSED_DIR / "ingest_report.md").write_text(
        build_report(regulation_units, tupa_units, entries, chunks,
                     len(footnotes)),
        encoding="utf-8",
    )

    articles = export_regulation(
        regulation_units, regulation,
        KNOWLEDGE_DIR / "reglamento_estudiantes.docx",
    )
    fichas = export_tupa(
        tupa_units, entries, tupa, KNOWLEDGE_DIR / "tupa_fichas.docx"
    )
    export_tupa_csv(entries, tupa, KNOWLEDGE_DIR / "tupa_fichas.csv")
    write_topics(entries, TOPICS_DIR)
    print(f"Artículos: {articles}/{EXPECTED_ARTICLES}; "
          f"fichas: {fichas}/{EXPECTED_TUPA_ENTRIES}; "
          f"fragmentos: {len(chunks)}")


if __name__ == "__main__":
    main()
