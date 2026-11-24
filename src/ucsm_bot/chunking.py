"""Segmentación del corpus en unidades normativas (artículos y fichas)."""

import re
from dataclasses import dataclass, field

from ucsm_bot.cleaning import Footnote, PageLine

MAX_CHUNK_CHARS = 1500
CHUNK_OVERLAP_CHARS = 150

ARTICLE_START = re.compile(r"^Art\. ?(\d{1,3})°\s*(.*)$")
TITLE_HEADING = re.compile(r"^TÍTULO ([IVXLC]+)$")
CHAPTER_HEADING = re.compile(r"^CAPÍTULO ([IVXLC]+)$")
SUBCHAPTER_HEADING = re.compile(r"^SUB CAPÍTULO ([IVXLC]+)\.?$")
PROVISIONS_HEADING = re.compile(r"^DISPOSICIONES (FINALES|TRANSITORIAS)$")
CHANGE_CONTROL_HEADING = "CONTROL DE CAMBIOS"
ARTICLE_TITLE_MAX_CHARS = 60

TUPA_SECTION = re.compile(r"^SECCIÓN N° (\d): (.+)$")
TUPA_ENTRY_START = {
    "Denominación del Procedimiento Administrativo": "procedimiento",
    "Denominación del Servicio": "servicio",
}


@dataclass
class Paragraph:
    """Párrafo reconstruido a partir de líneas consecutivas."""

    text: str
    pages: list[int]
    notes: list[int]


@dataclass
class Unit:
    """Unidad normativa: artículo, disposición, control de cambios o ficha."""

    unit_id: str
    doc_id: str
    kind: str
    title: str
    heading_path: list[str]
    pages: list[int]
    paragraphs: list[str] = field(default_factory=list)
    article: int | None = None
    notes: list[dict] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        """Devolver el texto completo de la unidad."""
        return "\n\n".join(self.paragraphs)

    @property
    def has_changes(self) -> bool:
        """Indicar si la unidad tiene notas de modificación."""
        return bool(self.notes)


def join_lines(lines: list[str]) -> str:
    """Unir líneas cortadas de un párrafo, reparando guiones de corte.

    :param lines: líneas del párrafo.
    :return: texto del párrafo en una sola línea.
    """
    text = ""
    for line in lines:
        if text.endswith("-") and line[:1].islower():
            text = text[:-1] + line
        else:
            text = f"{text} {line}" if text else line
    return text


def build_paragraphs(lines: list[PageLine]) -> list[Paragraph]:
    """Agrupar líneas no vacías consecutivas en párrafos.

    :param lines: líneas limpias con página y notas.
    :return: párrafos con sus páginas y notas al pie.
    """
    paragraphs: list[Paragraph] = []
    buffer: list[PageLine] = []

    def flush() -> None:
        if buffer:
            paragraphs.append(
                Paragraph(
                    text=join_lines([line.text for line in buffer]),
                    pages=sorted({line.page for line in buffer}),
                    notes=[n for line in buffer for n in line.notes],
                )
            )
            buffer.clear()

    for line in lines:
        if line.text:
            buffer.append(line)
        else:
            if line.notes and buffer:
                buffer[-1].notes.extend(line.notes)
            flush()
    flush()
    return paragraphs


def is_uppercase_text(text: str) -> bool:
    """Indicar si un texto está mayoritariamente en mayúsculas.

    :param text: texto a evaluar.
    :return: ``True`` si al menos el 80 % de sus letras son mayúsculas.
    """
    letters = [char for char in text if char.isalpha()]
    if not letters:
        return False
    return sum(char.isupper() for char in letters) / len(letters) >= 0.8


def split_article_heading(rest: str) -> tuple[str, str]:
    """Separar el título del artículo del inicio de su texto.

    :param rest: texto que sigue a ``Art. N°`` en el párrafo.
    :return: título (puede ser vacío) y texto restante.
    """
    head, colon, tail = rest.partition(":")
    if colon and len(head) <= ARTICLE_TITLE_MAX_CHARS:
        return head.strip(), tail.strip()
    if len(rest) <= ARTICLE_TITLE_MAX_CHARS:
        return rest.strip(), ""
    return "", rest.strip()


def segment_regulation(
    lines: list[PageLine], footnotes: list[Footnote], doc_id: str
) -> list[Unit]:
    """Segmentar el Reglamento en artículos, disposiciones y control.

    Solo se acepta un nuevo artículo si su número es el siguiente al último
    encontrado; así se descartan referencias como ``Art. 83° b.`` dentro de
    otro artículo.

    :param lines: líneas limpias del cuerpo del Reglamento.
    :param footnotes: notas al pie del documento.
    :param doc_id: identificador del documento.
    :return: unidades en orden de aparición.
    """
    notes_by_number = {note.number: note for note in footnotes}
    units: list[Unit] = []
    headings: dict[str, str | None] = {
        "title": None, "chapter": None, "subchapter": None,
    }
    pending_heading: str | None = None
    current: Unit | None = None
    last_article = 0

    def heading_path() -> list[str]:
        keys = ("title", "chapter", "subchapter")
        return [headings[key] for key in keys if headings[key]]

    def add_notes(unit: Unit, numbers: list[int]) -> None:
        for number in numbers:
            note = notes_by_number[number]
            unit.notes.append({"number": number, "text": note.text})

    for paragraph in build_paragraphs(lines):
        text = paragraph.text
        if pending_heading:
            if is_uppercase_text(text):
                headings[pending_heading] += f" – {text}"
                pending_heading = None
                continue
            pending_heading = None

        for key, pattern, label in (
            ("title", TITLE_HEADING, "TÍTULO"),
            ("chapter", CHAPTER_HEADING, "CAPÍTULO"),
            ("subchapter", SUBCHAPTER_HEADING, "SUB CAPÍTULO"),
        ):
            match = pattern.match(text)
            if match:
                headings[key] = f"{label} {match.group(1)}"
                if key == "title":
                    headings["chapter"] = headings["subchapter"] = None
                elif key == "chapter":
                    headings["subchapter"] = None
                pending_heading = key
                break
        if match:
            continue

        provisions = PROVISIONS_HEADING.match(text)
        if provisions or text == CHANGE_CONTROL_HEADING:
            kind = "disposicion" if provisions else "control_cambios"
            slug = (
                provisions.group(1).lower() if provisions else "control"
            )
            current = Unit(
                unit_id=f"reg-{slug}",
                doc_id=doc_id,
                kind=kind,
                title=text.title() if provisions else "Control de cambios",
                heading_path=[],
                pages=list(paragraph.pages),
            )
            units.append(current)
            continue

        article = ARTICLE_START.match(text)
        if article and int(article.group(1)) == last_article + 1:
            last_article += 1
            title, body = split_article_heading(article.group(2))
            current = Unit(
                unit_id=f"reg-art-{last_article:03d}",
                doc_id=doc_id,
                kind="articulo",
                title=title,
                heading_path=heading_path(),
                pages=list(paragraph.pages),
                article=last_article,
            )
            if body:
                current.paragraphs.append(body)
            add_notes(current, paragraph.notes)
            units.append(current)
            continue

        if current is None:
            continue
        current.paragraphs.append(text)
        current.pages = sorted(set(current.pages) | set(paragraph.pages))
        add_notes(current, paragraph.notes)
    return units


def segment_tupa(lines: list[PageLine], doc_id: str) -> list[Unit]:
    """Segmentar el TUPA en fichas de procedimientos y servicios.

    Las secciones de formularios y sedes se conservan como unidades propias.

    :param lines: líneas limpias del cuerpo del TUPA.
    :param doc_id: identificador del documento.
    :return: unidades en orden de aparición.
    """
    units: list[Unit] = []
    section = ""
    current: Unit | None = None
    for page_line in lines:
        text = page_line.text
        section_match = TUPA_SECTION.match(text)
        if section_match:
            section = section_match.group(2).title()
            current = None
            if section_match.group(1) in {"3", "4"}:
                slug = "formularios" if section_match.group(1) == "3" else (
                    "sedes"
                )
                current = Unit(
                    unit_id=f"tupa-{slug}",
                    doc_id=doc_id,
                    kind=slug,
                    title=section,
                    heading_path=[f"SECCIÓN N° {section_match.group(1)}"],
                    pages=[page_line.page],
                )
                units.append(current)
            continue
        if text in TUPA_ENTRY_START:
            current = Unit(
                unit_id=f"tupa-{len(units) + 1:03d}",
                doc_id=doc_id,
                kind=TUPA_ENTRY_START[text],
                title="",
                heading_path=[section],
                pages=[page_line.page],
            )
            units.append(current)
        if current is None or not text:
            continue
        current.lines.append(text)
        if page_line.page not in current.pages:
            current.pages.append(page_line.page)
    for unit in units:
        if unit.kind in {"formularios", "sedes"}:
            unit.paragraphs = [join_lines(unit.lines)]
    return units


def split_into_chunks(unit: Unit, prefix: str = "") -> list[dict]:
    """Dividir una unidad en fragmentos de tamaño máximo con solapamiento.

    La unidad solo se divide si su texto supera ``MAX_CHUNK_CHARS``; cada
    fragmento conserva el identificador y el artículo de la unidad.

    :param unit: unidad normativa.
    :param prefix: texto que encabeza cada fragmento (p. ej. denominación y
        código de una ficha del TUPA).
    :return: fragmentos con ``chunk_id``, ``unit_id``, ``part`` y ``text``.
    """
    parts: list[str] = []
    current = ""
    for paragraph in unit.paragraphs or [unit.text]:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if current and len(candidate) > MAX_CHUNK_CHARS:
            parts.append(current)
            overlap = current[-CHUNK_OVERLAP_CHARS:]
            current = f"{overlap}\n\n{paragraph}"
        else:
            current = candidate
    if current:
        parts.append(current)
    return [
        {
            "chunk_id": f"{unit.unit_id}-p{index}",
            "unit_id": unit.unit_id,
            "doc_id": unit.doc_id,
            "article": unit.article,
            "part": index,
            "text": f"{prefix}\n\n{text}" if prefix else text,
        }
        for index, text in enumerate(parts, start=1)
    ]
