"""Limpieza del texto Markdown de los documentos del corpus.

Cada documento se convierte en una lista de líneas con su página de origen,
sin índice, encabezados, pies de página, avisos repetidos ni tablas rotas.
"""

import re
from dataclasses import dataclass, field

# --- Reglamento de Estudiantes -------------------------------------------

REGULATION_STAMP = re.compile(r"^RESOLUCIÓN No\. 9814-CU-2026(\d{1,2})\s*$")
REGULATION_HEADER_LINES = {
    "Texto Único Ordenado del Reglamento de",
    "Estudiantes de la UCSM",
    "TUO-EST-001 / V03",
    "Abril - 2026",
}
FOOTER_PREFIXES = (
    "Este documento no puede ser alterado",
    "La información contenida en el presente documento",
    "representa una falta.",
    "Una vez impreso el presente documento",
)
PAGE_FOOTER = re.compile(r"^- \d+ de \d+ -$")
FOOTNOTE_START = re.compile(r"^(\d{1,2}) ([A-ZÁÉÍÓÚÑ].*)$")
REGULATION_BODY_START = "TÍTULO I"
ORPHAN_LIST_MARKER = re.compile(r"^([a-zñ]{1,2})\.$")
INLINE_LIST_MARKER = re.compile(r"^[a-zñ]{1,2}\.\s+\S")
LIST_BLOCK_END = re.compile(r"^(Art\. ?\d|TÍTULO |CAPÍTULO |SUB CAPÍTULO )")

# --- TUPA -----------------------------------------------------------------

TUPA_STAMP = "RESOLUCIÓN No. 9888-CU-2026"
TUPA_TABLE_STAMP = re.compile(
    r"^\|\s*RESOLUCIÓN No\. 9888-CU-2026\s*\|.*\|\s*(\d{1,3})\s*\|\s*$"
)
TUPA_HEADER_LINES = {
    TUPA_STAMP,
    "Texto Único de Procedimientos Administrativos",
    '"UNIVERSIDAD CATÓLICA DE SANTA MARÍA"',
}
TUPA_INLINE_STAMP = re.compile(r"^RESOLUCIÓN No\. 9888-CU-2026 (\d{1,3})$")
TUPA_PRINTED_PAGE = re.compile(r"^pág\. \d+$")
TUPA_BODY_START = "SECCIÓN N° 1: PROCEDIMIENTOS ADMINISTRATIVOS"
TABLE_SEPARATOR = re.compile(r"^\|[\s\-|:]+\|$")
SPACED_LETTERS = re.compile(r"\b((?:[a-záéíóúñ] ){3,}[a-záéíóúñ])\b")

# --- Común ----------------------------------------------------------------

PDF_ARTIFACT = re.compile(r"\(cid:\d+\)")
MULTIPLE_SPACES = re.compile(r"[ \t]{2,}")


@dataclass
class PageLine:
    """Línea de texto limpio con su página de origen y notas al pie."""

    page: int
    text: str
    notes: list[int] = field(default_factory=list)


@dataclass
class Footnote:
    """Nota al pie del documento original."""

    number: int
    text: str
    page: int


def normalize_spaces(text: str) -> str:
    """Normalizar espacios y quitar artefactos de extracción del PDF.

    :param text: línea original.
    :return: línea sin espacios repetidos ni marcas ``(cid:N)``.
    """
    text = PDF_ARTIFACT.sub(" ", text)
    return MULTIPLE_SPACES.sub(" ", text).strip()


def is_regulation_footer(line: str) -> bool:
    """Indicar si una línea pertenece al pie de página del Reglamento.

    :param line: línea normalizada.
    :return: ``True`` si es un aviso del SGI/SGC o la numeración de página.
    """
    return line.startswith(FOOTER_PREFIXES) or bool(PAGE_FOOTER.match(line))


def split_regulation_pages(raw_text: str) -> list[tuple[int, list[str]]]:
    """Dividir el Markdown del Reglamento en páginas según el sello.

    El sello ``RESOLUCIÓN No. 9814-CU-2026N`` trae pegado el número de
    página N y marca el inicio de cada página.

    :param raw_text: contenido del archivo Markdown.
    :return: lista de pares (página, líneas normalizadas).
    """
    pages: list[tuple[int, list[str]]] = [(1, [])]
    for raw_line in raw_text.splitlines():
        line = normalize_spaces(raw_line)
        stamp = REGULATION_STAMP.match(line)
        if stamp:
            pages.append((int(stamp.group(1)), []))
            continue
        pages[-1][1].append(line)
    return pages


def extract_footnotes(
    lines: list[str], page: int, last_number: int
) -> tuple[list[str], list[Footnote]]:
    """Separar el bloque de notas al pie que precede al pie de página.

    :param lines: líneas de la página sin encabezados.
    :param page: número de página.
    :param last_number: número de la última nota encontrada en el documento.
    :return: líneas del cuerpo y notas al pie de la página.
    """
    footer_index = next(
        (i for i, line in enumerate(lines) if is_regulation_footer(line)),
        len(lines),
    )
    end = footer_index
    while end > 0 and not lines[end - 1]:
        end -= 1
    start = end
    while start > 0 and lines[start - 1]:
        start -= 1
    block_start = None
    for index in range(start, end):
        match = FOOTNOTE_START.match(lines[index])
        if match and int(match.group(1)) > last_number:
            block_start = index
            break
    if block_start is None:
        return lines[:footer_index], []

    footnotes: list[Footnote] = []
    for line in lines[block_start:footer_index]:
        match = FOOTNOTE_START.match(line)
        expected = footnotes[-1].number if footnotes else last_number
        if match and int(match.group(1)) > expected:
            footnotes.append(
                Footnote(int(match.group(1)), match.group(2), page)
            )
        elif footnotes and line:
            footnotes[-1].text = f"{footnotes[-1].text} {line}"
    return lines[:block_start], footnotes


def remove_footnote_marker(lines: list[PageLine], footnote: Footnote) -> None:
    """Quitar la llamada a una nota pegada al texto y registrarla en la línea.

    Las llamadas aparecen pegadas a la palabra anterior (``seleccionada9.``).
    Se busca la primera aparición en la misma página.

    :param lines: líneas de la página.
    :param footnote: nota al pie cuya llamada se busca.
    :return: ``None``; modifica las líneas en el lugar.
    """
    number = footnote.number
    glued = re.compile(rf"(?<=[A-Za-zÁÉÍÓÚáéíóúÑñ.,;:)”\"°]){number}(?!\d)")
    trailing = re.compile(
        rf"(?<![Nn]°)(?<!No\.)(?<!Nro\.)(?<!Art\.)(?<=[^\d\s]) {number}$"
    )
    for page_line in lines:
        if page_line.text == str(number):
            page_line.text = ""
            page_line.notes.append(number)
            return
        for marker in (glued, trailing):
            if marker.search(page_line.text):
                page_line.text = marker.sub("", page_line.text, count=1)
                page_line.notes.append(number)
                return


def find_regulation_body_start(lines: list[PageLine]) -> int:
    """Ubicar el inicio del cuerpo del Reglamento, después del índice.

    :param lines: líneas limpias del documento completo.
    :return: índice de la línea ``TÍTULO I`` del cuerpo.
    :raises ValueError: si no se encuentra el inicio del cuerpo.
    """
    for index, page_line in enumerate(lines):
        if page_line.text != REGULATION_BODY_START:
            continue
        following = next(
            (line.text for line in lines[index + 1:] if line.text), ""
        )
        if "...." not in following:
            return index
    raise ValueError("No se encontró el inicio del cuerpo del Reglamento")


def find_list_items(lines: list[PageLine], start: int, count: int) -> list[int]:
    """Ubicar el inicio de los ítems de una lista cuyos literales se separaron.

    Un ítem empieza en una línea con mayúscula inicial cuya línea anterior
    está vacía o termina en ``.``, ``;`` o ``:``. La búsqueda se detiene en
    otro literal, un artículo o un encabezado.

    :param lines: líneas limpias.
    :param start: índice de la primera línea después de los literales.
    :param count: número de literales que se deben asignar.
    :return: índices de inicio de ítem (como máximo ``count + 1``).
    """
    starts: list[int] = []
    previous = ""
    for index in range(start, len(lines)):
        text = lines[index].text
        if text and (
            ORPHAN_LIST_MARKER.match(text) or INLINE_LIST_MARKER.match(text)
            or LIST_BLOCK_END.match(text)
        ):
            break
        if text and text[0].isupper() and (
            not previous or previous.endswith((".", ";", ":"))
        ):
            starts.append(index)
            if len(starts) > count:
                break
        previous = text
    return starts


def restore_list_markers(lines: list[PageLine]) -> tuple[int, int]:
    """Volver a unir los literales (``a.``, ``b.``…) separados de su texto.

    En el Markdown algunas listas traen primero todos los literales y luego
    los textos. Si el número de ítems detectados coincide con el de
    literales (o lo supera en uno, con ítems separados por líneas en blanco,
    porque tras la lista sigue un párrafo del artículo), cada literal se
    antepone a su ítem y el ítem queda como párrafo propio; si no, se
    conservan las líneas sin cambios.

    :param lines: líneas limpias; se modifican en el lugar.
    :return: listas reparadas y listas sin reparar.
    """
    repaired = unresolved = 0
    index = 0
    while index < len(lines):
        if not ORPHAN_LIST_MARKER.match(lines[index].text):
            index += 1
            continue
        markers: list[int] = []
        cursor = index
        while cursor < len(lines) and (
            not lines[cursor].text
            or ORPHAN_LIST_MARKER.match(lines[cursor].text)
        ):
            if lines[cursor].text:
                markers.append(cursor)
            cursor += 1
        starts = find_list_items(lines, cursor, len(markers))
        separated = all(not lines[item - 1].text for item in starts[1:])
        if len(starts) == len(markers) + 1 and separated:
            starts = starts[:-1]
        if len(starts) == len(markers):
            for marker, item in reversed(list(zip(markers, starts))):
                lines[item].text = f"{lines[marker].text} {lines[item].text}"
                lines[marker].text = ""
                if lines[item - 1].text:
                    lines.insert(item, PageLine(lines[item].page, ""))
            repaired += 1
            cursor = starts[-1]
        else:
            unresolved += 1
        index = cursor
    return repaired, unresolved


def clean_regulation(raw_text: str) -> tuple[list[PageLine], list[Footnote]]:
    """Limpiar el Markdown del Reglamento de Estudiantes.

    :param raw_text: contenido del archivo Markdown.
    :return: líneas del cuerpo con su página y notas al pie del documento.
    """
    all_lines: list[PageLine] = []
    all_footnotes: list[Footnote] = []
    last_number = 0
    for page, page_lines in split_regulation_pages(raw_text):
        lines = [
            line for line in page_lines if line not in REGULATION_HEADER_LINES
        ]
        body, footnotes = extract_footnotes(lines, page, last_number)
        page_body = [
            PageLine(page, line)
            for line in body
            if not is_regulation_footer(line)
        ]
        for footnote in footnotes:
            remove_footnote_marker(page_body, footnote)
            last_number = footnote.number
        all_lines.extend(page_body)
        all_footnotes.extend(footnotes)
    body_start = find_regulation_body_start(all_lines)
    body = all_lines[body_start:]
    restore_list_markers(body)
    return body, all_footnotes


def flatten_table_row(line: str) -> str | None:
    """Convertir una fila de tabla Markdown rota en texto plano.

    :param line: línea que puede ser una fila de tabla.
    :return: texto de las celdas no vacías, cadena vacía para separadores
        o ``None`` si la línea no es una fila de tabla.
    """
    if not line.startswith("|"):
        return None
    if TABLE_SEPARATOR.match(line):
        return ""
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    return " ".join(cell for cell in cells if cell)


def join_spaced_letters(text: str) -> str:
    """Unir palabras partidas letra por letra (``d i s p o s i c i ó n``).

    :param text: línea de texto.
    :return: línea con las letras sueltas unidas.
    """
    return SPACED_LETTERS.sub(lambda m: m.group(1).replace(" ", ""), text)


def clean_tupa(raw_text: str) -> list[PageLine]:
    """Limpiar el Markdown del TUPA.

    La página se toma del número que acompaña a la cabecera
    ``RESOLUCIÓN No. 9888-CU-2026`` (línea previa, misma línea o última
    celda de tabla).

    :param raw_text: contenido del archivo Markdown.
    :return: líneas del cuerpo con su página.
    """
    raw_lines = [normalize_spaces(line) for line in raw_text.splitlines()]
    lines: list[PageLine] = []
    page = 1
    for index, line in enumerate(raw_lines):
        table_stamp = TUPA_TABLE_STAMP.match(line)
        if table_stamp:
            page = int(table_stamp.group(1))
            continue
        inline_stamp = TUPA_INLINE_STAMP.match(line)
        if inline_stamp:
            page = int(inline_stamp.group(1))
            continue
        if line.isdigit():
            following = next(
                (text for text in raw_lines[index + 1:] if text), ""
            )
            if following == TUPA_STAMP:
                page = int(line)
                continue
        if line in TUPA_HEADER_LINES or TUPA_PRINTED_PAGE.match(line):
            continue
        flattened = flatten_table_row(line)
        if flattened is not None:
            if not flattened:
                continue
            line = flattened
        lines.append(PageLine(page, join_spaced_letters(line)))

    body_start = next(
        i for i, line in enumerate(lines) if line.text == TUPA_BODY_START
    )
    return lines[body_start:]


def render_clean_text(lines: list[PageLine]) -> str:
    """Generar el texto limpio con marcadores de página.

    :param lines: líneas limpias.
    :return: texto con un comentario ``<!-- pág. N -->`` en cada cambio de
        página.
    """
    output: list[str] = []
    current_page = None
    for page_line in lines:
        if page_line.page != current_page:
            output.append(f"\n<!-- pág. {page_line.page} -->\n")
            current_page = page_line.page
        output.append(page_line.text)
    return "\n".join(output).strip() + "\n"
