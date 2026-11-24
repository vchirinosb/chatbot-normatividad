"""Extracción de campos estructurados de las fichas del TUPA."""

import re

from ucsm_bot.chunking import Unit, join_lines

FIELD_LABELS: list[tuple[str, re.Pattern]] = [
    ("name", re.compile(r"^Denominación del (Procedimiento Administrativo"
                        r"|Servicio)$")),
    ("code", re.compile(r"^Código:\s*(\S+)\s*$")),
    ("description", re.compile(r"^Descripción del (procedimiento|Servicio)$")),
    ("requirements", re.compile(r"^Requisitos$")),
    ("notes", re.compile(r"^Notas:$")),
    ("forms", re.compile(r"^Formularios$")),
    ("channels", re.compile(r"^Canales de atención$")),
    ("payment", re.compile(r"^Pago por derecho de tramitación")),
    ("term", re.compile(r"^Plazo( de atención.*)?$")),
    ("offices", re.compile(r"^Sedes y horarios de atención$")),
    ("submission_unit", re.compile(r"^Unidad de organización donde se "
                                   r"presenta")),
    ("approval_unit", re.compile(r"^Unidad de organización responsable de "
                                 r"aprobar")),
    ("appeals", re.compile(r"^Instancias de resolución de recursos$")),
    ("legal_basis", re.compile(r"^Base legal$")),
]
REQUIRED_FIELDS = (
    "code", "name", "requirements", "fees", "term", "submission_unit",
    "approval_unit",
)
LEGAL_BASIS_NOISE = {
    "Fecha", "Publicación", "Artículo Denominación Tipo Número",
}
FEE = re.compile(r"Monto - S/ ?([\d,]+\.\d{2})")
FREE_OF_CHARGE = re.compile(r"^Gratuito\b", re.IGNORECASE)
NUMBERED_ITEM = re.compile(r"^\d+\.-")
TERM = re.compile(
    r"^(\d+\s+d[ií]as?\s+(?:h[áa]biles|calendario)|Inmediat[oa])\s*(.*)$",
    re.IGNORECASE,
)
RIGHT_COLUMN_FRAGMENTS = re.compile(
    r"Agencia Bancaria:.*$|Otras opciones|Modalidad de pagos?"
    r"|(?:del |de la )?[Ss]istema ERP\.?|Plataforma del"
    r"|a través de la plataforma"
)
PHONE = re.compile(r"Tel[ée]fono:?\s*([\d][\d\s-]{5,}\d)")
EXTENSION = re.compile(r"Anexos?:?\s*([\d][\d ,yó]*\d)")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def split_blocks(lines: list[str]) -> dict[str, list[str]]:
    """Repartir las líneas de una ficha entre sus etiquetas.

    :param lines: líneas limpias de la ficha.
    :return: líneas de contenido por campo (sin la línea de la etiqueta,
        salvo el código, que va en la misma línea).
    """
    blocks: dict[str, list[str]] = {}
    current = None
    for line in lines:
        for key, pattern in FIELD_LABELS:
            match = pattern.match(line)
            if match:
                current = key
                blocks.setdefault(key, [])
                if key == "code":
                    blocks[key].append(match.group(1))
                break
        else:
            if current:
                blocks[current].append(line)
    return blocks


def join_numbered_items(lines: list[str]) -> list[str]:
    """Unir las líneas de una lista numerada (``1.- …``) en ítems.

    :param lines: líneas del bloque.
    :return: ítems de la lista; si no hay numeración, un único ítem.
    """
    items: list[list[str]] = []
    for line in lines:
        if NUMBERED_ITEM.match(line) or not items:
            items.append([line])
        else:
            items[-1].append(line)
    return [join_lines(item) for item in items if item]


def clean_fee_concept(lines: list[str]) -> str:
    """Reconstruir el concepto de un monto sin el texto de la otra columna.

    :param lines: líneas entre el monto anterior y el actual.
    :return: concepto del monto.
    """
    parts = [RIGHT_COLUMN_FRAGMENTS.sub(" ", line) for line in lines]
    concept = " ".join(" ".join(parts).split())
    return concept.strip(" ,.;")


def extract_fees(lines: list[str]) -> list[dict]:
    """Extraer los montos del bloque de pago y su concepto.

    El concepto de cada monto son las líneas que lo preceden desde el monto
    anterior, sin los fragmentos de la columna "Modalidad de pagos".

    :param lines: líneas del bloque "Pago por derecho de tramitación".
    :return: lista de montos con ``concept`` (vacío si es único) y
        ``amount`` (``S/ 44.00`` o ``Gratuito``).
    """
    fees: list[dict] = []
    pending: list[str] = []
    for line in lines:
        fee = FEE.search(line)
        if fee or FREE_OF_CHARGE.match(line):
            amount = f"S/ {fee.group(1)}" if fee else "Gratuito"
            fees.append(
                {"concept": clean_fee_concept(pending), "amount": amount}
            )
            pending = []
        else:
            pending.append(line)
    if len(fees) == 1:
        fees[0]["concept"] = ""
    return fees


def format_fees(fees: list[dict]) -> str:
    """Formatear los montos para mostrarlos en una línea.

    :param fees: montos extraídos.
    :return: texto como ``S/ 44.00`` o ``Copia simple: S/ 0.10; …``.
    """
    return "; ".join(
        f"{fee['concept']}: {fee['amount']}" if fee["concept"]
        else fee["amount"]
        for fee in fees
    )


def extract_payment_methods(lines: list[str]) -> str:
    """Extraer la modalidad de pago (agencia bancaria, plataforma, etc.).

    :param lines: líneas del bloque de pago.
    :return: descripción de la modalidad de pago o cadena vacía.
    """
    text = join_lines(lines)
    match = re.search(r"Agencia Bancaria:.*?(?=Monto -|$)", text)
    if not match:
        return ""
    method = match.group(0).strip()
    if "Sistema ERP" in text and "ERP" not in method:
        method = f"{method} Sistema ERP"
    return method


def extract_contact(lines: list[str]) -> dict[str, str]:
    """Extraer teléfono, anexo y correo de un bloque de texto.

    :param lines: líneas del bloque.
    :return: diccionario con ``phone``, ``extension`` y ``email``.
    """
    text = " ".join(lines)
    phone = PHONE.search(text)
    extension = EXTENSION.search(text)
    email = EMAIL.search(text)
    return {
        "phone": phone.group(1).strip() if phone else "",
        "extension": extension.group(1).strip() if extension else "",
        "email": email.group(0) if email else "",
    }


def normalize_term(term: str) -> str:
    """Escribir el plazo con tildes (``2 dias habiles`` → ``2 días hábiles``).

    :param term: plazo extraído.
    :return: plazo normalizado.
    """
    term = re.sub(r"\bd[ií]as\b", "días", term, flags=re.IGNORECASE)
    term = re.sub(r"\bh[áa]biles\b", "hábiles", term, flags=re.IGNORECASE)
    return re.sub(r"^1 días hábiles", "1 día hábil", term)


def collapse_repeated_unit(text: str) -> str:
    """Simplificar ``Canal : Unidad`` cuando canal y unidad coinciden.

    :param text: texto del campo "Unidad de organización donde se presenta".
    :return: ``Unidad`` si ambos lados son iguales; si no, el texto original.
    """
    channel, separator, office = text.partition(" : ")
    if separator and channel.strip() == office.strip():
        return office.strip()
    return text


def extract_tupa_fields(unit: Unit) -> dict:
    """Extraer los campos estructurados de una ficha del TUPA.

    :param unit: unidad de tipo ``procedimiento`` o ``servicio``.
    :return: campos de la ficha, con la lista ``missing_fields`` de los
        campos obligatorios que no pudieron extraerse.
    """
    blocks = split_blocks(unit.lines)
    term_text = join_lines(blocks.get("term", []))
    term_match = TERM.match(term_text)
    approval_lines = blocks.get("approval_unit", [])
    contact = extract_contact(approval_lines)
    channel_contact = extract_contact(blocks.get("channels", []))
    for key, value in channel_contact.items():
        contact[key] = contact[key] or value
    fees = extract_fees(blocks.get("payment", []))
    legal_basis = [
        line for line in blocks.get("legal_basis", [])
        if line not in LEGAL_BASIS_NOISE
    ]
    approval_unit = ""
    if approval_lines:
        approval_unit = re.split(r"\s+Tel[ée]fono", approval_lines[0])[0]

    fields = {
        "unit_id": unit.unit_id,
        "code": (blocks.get("code") or [""])[0],
        "name": join_lines(blocks.get("name", [])).strip('" ').strip(),
        "kind": unit.kind,
        "section": unit.heading_path[0] if unit.heading_path else "",
        "pages": unit.pages,
        "description": join_lines(blocks.get("description", [])),
        "requirements": join_numbered_items(blocks.get("requirements", [])),
        "notes": join_numbered_items(blocks.get("notes", [])),
        "forms": join_lines(blocks.get("forms", [])),
        "channels": blocks.get("channels", []),
        "fees": fees,
        "fee_display": format_fees(fees),
        "payment_methods": extract_payment_methods(blocks.get("payment", [])),
        "term": normalize_term(
            term_match.group(1) if term_match else term_text
        ),
        "qualification": term_match.group(2) if term_match else "",
        "offices": join_lines(blocks.get("offices", [])),
        "submission_unit": collapse_repeated_unit(
            join_lines(blocks.get("submission_unit", []))
        ),
        "approval_unit": approval_unit.strip(),
        "contact": contact,
        "appeals": join_lines(blocks.get("appeals", [])),
        "legal_basis": join_lines(legal_basis),
    }
    fields["missing_fields"] = [
        key for key in REQUIRED_FIELDS if not fields[key]
    ]
    return fields
