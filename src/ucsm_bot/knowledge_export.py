"""Exportación del corpus a documentos de conocimiento para Copilot Studio.

Genera un ``.docx`` por documento, con un encabezado de nivel 2 por artículo
o ficha que incluye su número o código y página, más la URL oficial, y la
tabla de fichas del TUPA en CSV. Los ``.docx`` se escriben de forma
determinista (fechas fijas en metadatos y en el ZIP).
"""

import csv
import io
import zipfile
from datetime import datetime
from pathlib import Path

from docx import Document as DocxDocument

from ucsm_bot.chunking import Unit
from ucsm_bot.corpus import Document

FIXED_DATETIME = datetime(2026, 1, 1)
ZIP_DATE_TIME = (2026, 1, 1, 0, 0, 0)
TUPA_CSV_COLUMNS = (
    "code", "name", "kind", "section", "pages", "fee_display", "term",
    "qualification", "submission_unit", "approval_unit", "phone",
    "extension", "email", "requirements", "payment_methods", "source_url",
)
TUPA_FIELD_LABELS = (
    ("description", "Descripción"),
    ("requirements", "Requisitos"),
    ("notes", "Notas"),
    ("forms", "Formularios"),
    ("fee_display", "Pago por derecho de tramitación"),
    ("payment_methods", "Modalidad de pago"),
    ("term", "Plazo de atención"),
    ("qualification", "Calificación"),
    ("submission_unit", "Unidad donde se presenta"),
    ("approval_unit", "Unidad que aprueba"),
    ("offices", "Sedes y horarios de atención"),
    ("contact", "Consultas"),
    ("appeals", "Instancias de resolución de recursos"),
    ("legal_basis", "Base legal"),
)


def format_pages(pages: list[int]) -> str:
    """Formatear las páginas de una unidad.

    :param pages: páginas ordenadas.
    :return: ``pág. 8`` o ``págs. 8–9``.
    """
    if not pages:
        return ""
    if len(pages) == 1:
        return f"pág. {pages[0]}"
    return f"págs. {pages[0]}–{pages[-1]}"


def format_contact(contact: dict[str, str]) -> str:
    """Formatear teléfono, anexo y correo de contacto.

    :param contact: diccionario con ``phone``, ``extension`` y ``email``.
    :return: texto de contacto o cadena vacía.
    """
    parts = []
    if contact.get("phone"):
        parts.append(f"Teléfono {contact['phone']}")
    if contact.get("extension"):
        parts.append(f"anexo {contact['extension']}")
    if contact.get("email"):
        parts.append(f"correo {contact['email']}")
    return ", ".join(parts)


def render_tupa_paragraphs(entry: dict) -> list[str]:
    """Convertir los campos de una ficha en párrafos ``Campo: valor``.

    :param entry: campos extraídos de la ficha.
    :return: párrafos con los campos que tienen contenido.
    """
    paragraphs = []
    for key, label in TUPA_FIELD_LABELS:
        value = entry.get(key)
        if key == "contact":
            value = format_contact(value or {})
        if isinstance(value, list):
            value = " ".join(value)
        if value:
            paragraphs.append(f"{label}: {value}")
    return paragraphs


def article_heading(unit: Unit) -> str:
    """Construir el encabezado de un artículo del Reglamento.

    :param unit: unidad de tipo ``articulo``.
    :return: texto como ``Art. 57° – Título · pág. 18``.
    """
    title = f" – {unit.title}" if unit.title else ""
    return f"Art. {unit.article}°{title} · {format_pages(unit.pages)}"


def tupa_heading(entry: dict) -> str:
    """Construir el encabezado de una ficha del TUPA.

    :param entry: campos de la ficha.
    :return: texto como ``Denominación (Código) · pág. 8``.
    """
    return f"{entry['name']} ({entry['code']}) · {format_pages(entry['pages'])}"


def save_deterministic(docx: DocxDocument, path: Path, title: str) -> None:
    """Guardar un ``.docx`` con metadatos y fechas del ZIP fijos.

    :param docx: documento de python-docx.
    :param path: ruta de salida.
    :param title: título para las propiedades del documento.
    :return: ``None``.
    """
    properties = docx.core_properties
    properties.title = title
    properties.author = "chatbot-normatividad-ucsm"
    properties.last_modified_by = "chatbot-normatividad-ucsm"
    properties.created = FIXED_DATETIME
    properties.modified = FIXED_DATETIME
    properties.revision = 1
    buffer = io.BytesIO()
    docx.save(buffer)
    buffer.seek(0)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(buffer) as source, zipfile.ZipFile(
        path, "w", zipfile.ZIP_DEFLATED
    ) as target:
        for name in sorted(source.namelist()):
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            target.writestr(info, source.read(name))


def add_source_line(docx: DocxDocument, text: str) -> None:
    """Agregar una línea de fuente en cursiva.

    :param docx: documento de python-docx.
    :param text: texto de la fuente.
    :return: ``None``.
    """
    docx.add_paragraph().add_run(text).italic = True


def export_regulation(units: list[Unit], document: Document, path: Path) -> int:
    """Exportar el Reglamento a ``.docx`` con un encabezado por artículo.

    :param units: unidades del Reglamento.
    :param document: metadatos del documento.
    :param path: ruta del ``.docx``.
    :return: número de encabezados de artículo escritos.
    """
    docx = DocxDocument()
    docx.add_heading(document.title, level=0)
    add_source_line(
        docx, f"{document.resolution}, versión {document.version}. "
        f"Fuente oficial: {document.source_url}",
    )
    current_title = None
    count = 0
    for unit in units:
        if unit.kind != "articulo":
            docx.add_heading(f"{unit.title} · {format_pages(unit.pages)}", 1)
            current_title = None
            for paragraph in unit.paragraphs:
                docx.add_paragraph(paragraph)
            continue
        if unit.heading_path[0] != current_title:
            current_title = unit.heading_path[0]
            docx.add_heading(current_title, level=1)
        docx.add_heading(article_heading(unit), level=2)
        count += 1
        add_source_line(
            docx,
            f"Fuente: {document.title}, Art. {unit.article}°, "
            f"{format_pages(unit.pages)}. Ubicación: "
            f"{' > '.join(unit.heading_path)}. {document.source_url}",
        )
        # Cada párrafo empieza con su artículo: así ningún fragmento que
        # genere Copilot Studio separa un dato de su referencia.
        reference = f"Art. {unit.article}°"
        for paragraph in unit.paragraphs:
            docx.add_paragraph(f"{reference}: {paragraph}")
        for note in unit.notes:
            docx.add_paragraph(f"{reference}: Nota de modificación "
                               f"{note['number']}: {note['text']}")
    save_deterministic(docx, path, document.title)
    return count


def export_tupa(
    units: list[Unit], entries: list[dict], document: Document, path: Path
) -> int:
    """Exportar el TUPA a ``.docx`` con un encabezado por ficha.

    :param units: unidades del TUPA (fichas, formularios y sedes).
    :param entries: campos de las fichas, en el mismo orden que las fichas.
    :param document: metadatos del documento.
    :param path: ruta del ``.docx``.
    :return: número de encabezados de ficha escritos.
    """
    docx = DocxDocument()
    docx.add_heading(document.title, level=0)
    add_source_line(
        docx, f"{document.resolution}. Fuente oficial: {document.source_url}"
    )
    entries_by_unit = {entry["unit_id"]: entry for entry in entries}
    current_section = None
    count = 0
    for unit in units:
        entry = entries_by_unit.get(unit.unit_id)
        if entry is None:
            docx.add_heading(f"{unit.title} · {format_pages(unit.pages)}", 1)
            current_section = None
            for paragraph in unit.paragraphs:
                docx.add_paragraph(paragraph)
            continue
        if entry["section"] != current_section:
            current_section = entry["section"]
            docx.add_heading(current_section, level=1)
        docx.add_heading(tupa_heading(entry), level=2)
        count += 1
        add_source_line(
            docx,
            f"Fuente: TUPA UCSM, {entry['kind']} {entry['code']}, "
            f"{format_pages(entry['pages'])}. {document.source_url}",
        )
        for paragraph in render_tupa_paragraphs(entry):
            docx.add_paragraph(paragraph)
    save_deterministic(docx, path, document.title)
    return count


def export_tupa_csv(entries: list[dict], document: Document, path: Path) -> None:
    """Exportar los campos de las fichas del TUPA a CSV.

    :param entries: campos de las fichas.
    :param document: metadatos del TUPA (para la URL oficial).
    :param path: ruta del CSV.
    :return: ``None``.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TUPA_CSV_COLUMNS,
                                lineterminator="\n")
        writer.writeheader()
        for entry in entries:
            writer.writerow({
                **{key: entry.get(key, "") for key in TUPA_CSV_COLUMNS},
                "pages": " ".join(str(page) for page in entry["pages"]),
                "phone": entry["contact"]["phone"],
                "extension": entry["contact"]["extension"],
                "email": entry["contact"]["email"],
                "requirements": " | ".join(entry["requirements"]),
                "source_url": document.source_url,
            })
