"""Generar las tarjetas de respuesta para validar el protocolo (tarea 3.4).

En el recorrido guiado (*Wizard of Oz*) el facilitador responde como lo
haría el chatbot. Las tarjetas se generan desde ``docs/protocolo.yaml`` y
``data/processed/tupa.json`` para que los textos y los montos coincidan con
la fuente única.

Uso: ``.venv/bin/python scripts/generate_validation_cards.py``
"""

import json
import sys
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

from ucsm_bot.knowledge_export import format_contact, format_pages  # noqa: E402

PROTOCOL_PATH = ROOT_DIR / "docs" / "protocolo.yaml"
TUPA_PATH = ROOT_DIR / "data" / "processed" / "tupa.json"
OUTPUT_PATH = ROOT_DIR / "docs" / "validacion_tarjetas.md"

# Fichas que aparecen en las tareas del recorrido.
TASK_CODES = ("SE1130737868", "PA1130732571", "PA1130731912")


def quote_block(text: str) -> str:
    """Formatear un texto como cita Markdown.

    :param text: texto del mensaje.
    :return: líneas con prefijo ``> ``.
    """
    return "\n".join(f"> {line}" if line else ">" for line in
                     text.strip().splitlines())


def render_card(entry: dict) -> str:
    """Formatear la ficha de trámite como la mostraría la Adaptive Card.

    :param entry: campos de la ficha del TUPA.
    :return: bloque Markdown de la tarjeta.
    """
    rows = [
        f"**{entry['name']}**",
        "",
        f"- Código: {entry['code']}",
        f"- Costo: {entry['fee_display']}",
        f"- Plazo de atención: {entry['term']}",
        f"- Dónde se presenta: {entry['submission_unit'] or '—'}",
        f"- Contacto: {format_contact(entry['contact']) or '—'}",
        f"- Fuente: TUPA UCSM, {format_pages(entry['pages'])}",
    ]
    return quote_block("\n".join(rows))


def main() -> None:
    """Escribir ``docs/validacion_tarjetas.md``."""
    protocol = yaml.safe_load(PROTOCOL_PATH.read_text(encoding="utf-8"))
    tupa = {e["code"]: e for e in json.loads(
        TUPA_PATH.read_text(encoding="utf-8"))}
    intents = {i["id"]: i for i in protocol["intenciones"]}
    menu = protocol["menu"]
    lines = [
        "# Tarjetas de respuesta para la validación del protocolo",
        "",
        "Generado por `scripts/generate_validation_cards.py` desde "
        "`docs/protocolo.yaml` y `data/processed/tupa.json`. No editar a "
        "mano: cambiar el YAML y volver a generar.",
        "",
        "El facilitador lee (o pega en el chat simulado) la tarjeta que "
        "corresponde a lo que escribe el participante. Si el participante "
        "escribe algo no previsto, elegir la intención más cercana y anotarlo "
        "como hallazgo.",
        "",
        "## Bienvenida (al iniciar)",
        "",
        quote_block(intents["saludo"]["mensaje"]),
        ">",
        quote_block(protocol["avisos"]["no_oficial"]),
        ">",
        quote_block(menu["pregunta"]),
        ">",
        quote_block("\n".join(f"[{o['etiqueta']}]" for o in menu["opciones"])),
        "",
    ]
    for intent_id in ("menu", "datos_personales", "fuera_de_alcance",
                      "sin_evidencia", "contenido_inapropiado"):
        intent = intents[intent_id]
        examples = ", ".join(f"\"{e}\"" for e in intent.get("ejemplos", []))
        lines += [f"## {intent_id}", ""]
        if examples:
            lines += [f"Se usa ante: {examples}.", ""]
        lines += [quote_block(intent["mensaje"]), ""]

    farewell = intents["despedida"]
    lines += [
        "## despedida",
        "",
        quote_block(farewell["mensaje"]),
        ">",
        quote_block(f"{farewell['encuesta']} "
                    f"[{'] ['.join(farewell['opciones_encuesta'])}]"),
        "",
        "## Respuestas para las tareas del recorrido",
        "",
        "### Tarea 1 – Desaprobar un curso tres veces (consulta normativa)",
        "",
        quote_block(
            "Si desapruebas la misma asignatura por tres (3) veces, eres "
            "separado temporalmente por un año de la Universidad. Al volver, "
            "solo puedes matricularte en esa asignatura; si la desapruebas "
            "por cuarta vez, procede el retiro definitivo de la Escuela "
            "Profesional.\n\n"
            "Fuentes: Reglamento de Estudiantes, Art. 83° (pág. 24)\n"
            "Orientación no oficial; el texto vinculante es el documento "
            "oficial."
        ),
        "",
        "### Tarea 2 – Constancia de estudios (consulta de trámite)",
        "",
        render_card(tupa[TASK_CODES[0]]),
        ">",
        quote_block(intents["consulta_tramite"]["mensaje_despues"]),
        "",
        "### Tarea 3 – Evaluación extemporánea (desambiguación)",
        "",
        "Primero la pregunta de aclaración:",
        "",
        quote_block(
            intents["desambiguacion_evaluacion_extemporanea"]["pregunta"]
        ),
        ">",
        quote_block(" ".join(
            f"[{o['etiqueta']}]" for o in
            intents["desambiguacion_evaluacion_extemporanea"]["opciones"]
        )),
        "",
        "Si elige Escuela Profesional:",
        "",
        render_card(tupa[TASK_CODES[1]]),
        "",
        "Si elige Escuela de Postgrado:",
        "",
        render_card(tupa[TASK_CODES[2]]),
        "",
        "### Tarea 4 – Pregunta fuera de alcance",
        "",
        "Usar la tarjeta `fuera_de_alcance` (o `sin_evidencia` si la "
        "pregunta es del dominio pero no está en los documentos).",
        "",
        "### Tarea 5 – Despedida",
        "",
        "Usar la tarjeta `despedida`.",
        "",
    ]
    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Tarjetas: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
