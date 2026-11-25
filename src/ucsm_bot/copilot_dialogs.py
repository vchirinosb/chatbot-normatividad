"""Generación del YAML de los Topics a partir de ``docs/protocolo.yaml``.

Cada archivo se pega en el editor de código del Topic correspondiente en
Copilot Studio (Topic → More → Open code editor). Así los mensajes fijos del
agente son copia literal del protocolo.
"""

import re
from pathlib import Path

import yaml

from ucsm_bot.copilot_topics import (
    build_card_fields,
    build_powerfx_table,
    quote_powerfx,
)

# Palabras ya normalizadas (minúsculas, sin tildes): se comparan con el
# texto del usuario después de normalize_formula.
IGNORED_WORDS = ", ".join(
    f'"{word}"' for word in (
        "tramite", "tramites", "quiero", "cuanto", "cuesta", "costo",
        "demora", "plazo", "hacer", "pedir", "solicitar",
    )
)
# Reemplazos para comparar sin tildes ni guiones; "rr" -> "r" iguala
# "prerrequisitos" con "Pre-requisitos" del TUPA.
NORMALIZATION = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),
                 ("ü", "u"), ("-", ""), ("rr", "r"))
# Caracteres de cada palabra que se buscan en el nombre (raíz aproximada:
# "adeudo" coincide con "adeudar" y "convalidar" con "Convalidación").
STEM_LENGTH = 5
# Dos fichas empatan si coinciden en las mismas palabras (por raíz y
# completas) y el nombre de una no supera en más de este factor al de la
# mejor; entonces se pregunta cuál, hasta MAX_OPTIONS opciones.
SIMILAR_NAME_RATIO = 1.5
MAX_OPTIONS = 4
GRADUATE_KEYWORD = "Postgrado"
CARD_PLACEHOLDER = re.compile(r"\{(\w+)\}")
CARD_SCHEMA = "http://adaptivecards.io/schemas/adaptive-card.json"


def find_intent(protocol: dict, intent_id: str) -> dict:
    """Buscar una intención del protocolo por su identificador.

    :param protocol: contenido de ``protocolo.yaml``.
    :param intent_id: identificador de la intención.
    :return: intención encontrada.
    :raises KeyError: si la intención no existe.
    """
    for intent in protocol["intenciones"]:
        if intent["id"] == intent_id:
            return intent
    raise KeyError(f"Intención no encontrada en el protocolo: {intent_id}")


def build_message(action_id: str, text: str,
                  quick_replies: list[str] | None = None) -> dict:
    """Construir un nodo *SendActivity*.

    :param action_id: identificador único del nodo dentro del Topic.
    :param text: texto del mensaje.
    :param quick_replies: textos de los botones de respuesta rápida.
    :return: nodo serializable a YAML.
    """
    activity: dict = {"text": [text]}
    if quick_replies:
        activity["quickReplies"] = [
            {"kind": "MessageBack", "text": reply} for reply in quick_replies
        ]
    return {"kind": "SendActivity", "id": action_id, "activity": activity}


def build_menu_message(protocol: dict, action_id: str, text: str) -> dict:
    """Construir el mensaje del menú de temas con *quick replies*.

    :param protocol: contenido de ``protocolo.yaml``.
    :param action_id: identificador único del nodo.
    :param text: texto que acompaña a los botones.
    :return: nodo *SendActivity*.
    """
    options = [option["etiqueta"] for option in protocol["menu"]["opciones"]]
    return build_message(action_id, text, options)


def build_custom_topic(description: str, intent_name: str,
                       actions: list[dict]) -> dict:
    """Construir un Topic propio que elige la orquestación generativa.

    El Topic termina con *CancelAllDialogs* para que el orquestador no
    agregue una respuesta generativa después del mensaje fijo. Las frases
    de ejemplo del protocolo no se cargan como frases de activación: con
    orquestación generativa el Topic se elige por su descripción, y el
    editor las marcaba como duplicadas.

    :param description: descripción que usa la orquestación generativa.
    :param intent_name: nombre del Topic para el modelo.
    :param actions: nodos del Topic.
    :return: diálogo serializable a YAML.
    """
    return {
        "kind": "AdaptiveDialog",
        "modelDisplayName": intent_name,
        "modelDescription": description,
        "beginDialog": {
            "kind": "OnRecognizedIntent",
            "id": "main",
            "intent": {},
            "actions": actions + [
                {"kind": "CancelAllDialogs", "id": "cancelAllDialogs_fin"},
            ],
        },
    }


def build_conversation_start(protocol: dict) -> dict:
    """Construir el Topic de sistema *Conversation Start*.

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo con bienvenida y menú de temas.
    """
    greeting = find_intent(protocol, "saludo")
    return {
        "kind": "AdaptiveDialog",
        "beginDialog": {
            "kind": "OnConversationStart",
            "id": "main",
            "actions": [
                build_message("sendMessage_saludo", greeting["mensaje"]),
                build_menu_message(protocol, "sendMessage_menu",
                                   protocol["menu"]["pregunta"]),
            ],
        },
    }


def build_fallback(protocol: dict) -> dict:
    """Construir el Topic de sistema *Fallback* (fuera de alcance).

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo que responde con el mensaje de fuera de alcance.
    """
    out_of_scope = find_intent(protocol, "fuera_de_alcance")
    return {
        "kind": "AdaptiveDialog",
        "beginDialog": {
            "kind": "OnUnknownIntent",
            "id": "main",
            "actions": [
                build_message("sendMessage_fuera_de_alcance",
                              out_of_scope["mensaje"]),
            ],
        },
    }


def build_end_of_conversation(protocol: dict) -> dict:
    """Construir el Topic de sistema *End of Conversation*.

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo con despedida, encuesta Sí/No y CSAT si fue útil.
    """
    farewell = find_intent(protocol, "despedida")
    return {
        "kind": "AdaptiveDialog",
        "startBehavior": "CancelOtherTopics",
        "beginDialog": {
            "kind": "OnSystemRedirect",
            "id": "main",
            "actions": [
                build_message("sendMessage_despedida", farewell["mensaje"]),
                {
                    "kind": "Question",
                    "id": "question_encuesta",
                    "conversationOutcome": "ResolvedImplied",
                    "alwaysPrompt": True,
                    "variable": "init:Topic.SurveyResponse",
                    "prompt": farewell["encuesta"],
                    "entity": "BooleanPrebuiltEntity",
                },
                {
                    "kind": "ConditionGroup",
                    "id": "condition_encuesta",
                    "conditions": [
                        {
                            "id": "condition_encuesta_si",
                            "condition": "=Topic.SurveyResponse = true",
                            "actions": [
                                {
                                    "kind": "CSATQuestion",
                                    "id": "csat_encuesta",
                                    "conversationOutcome":
                                        "ResolvedConfirmed",
                                },
                            ],
                        },
                    ],
                },
                {"kind": "EndConversation", "id": "endConversation_fin"},
            ],
        },
    }


def build_closing_topic(protocol: dict) -> dict:
    """Construir el Topic propio *Cierre de la conversación*.

    El Topic del sistema *Agradecimiento* respondía "De nada." a "gracias,
    eso es todo" y la despedida con encuesta no se mostraba. Este Topic se
    elige por su descripción y repite las acciones de *End of
    Conversation* (despedida, encuesta Sí/No y CSAT).

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo con despedida y encuesta.
    """
    end = build_end_of_conversation(protocol)
    return build_custom_topic(
        "Se activa cuando el usuario se despide o indica que terminó su "
        "consulta, por ejemplo \"gracias, eso es todo\", \"adiós\", \"chau\" "
        "o \"ya no tengo más preguntas\". Muestra la despedida y la encuesta "
        "de satisfacción.",
        "Cierre de la conversación",
        end["beginDialog"]["actions"],
    )


def build_menu_topic(protocol: dict) -> dict:
    """Construir el Topic propio *Menú de temas*.

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo que muestra el menú de temas.
    """
    menu = find_intent(protocol, "menu")
    return build_custom_topic(
        "Muestra el menú de temas cuando el usuario pide ayuda, pregunta qué "
        "puede hacer el asistente o pide ver los temas disponibles. No lo "
        "uses cuando el usuario dice que quiere hacer o consultar un trámite: "
        "para eso está Consulta de trámite.",
        "Menú de temas",
        [build_menu_message(protocol, "sendMessage_menu", menu["mensaje"])],
    )


def build_personal_data_topic(protocol: dict) -> dict:
    """Construir el Topic propio *Datos personales*.

    :param protocol: contenido de ``protocolo.yaml``.
    :return: diálogo que advierte sin procesar el dato.
    """
    personal = find_intent(protocol, "datos_personales")
    return build_custom_topic(
        "Se activa cuando el usuario escribe datos personales como su DNI "
        "(8 dígitos), su código de estudiante (10 dígitos), sus notas o una "
        "contraseña. Advierte que no es necesario compartirlos y no los "
        "procesa.",
        "Datos personales",
        [build_message("sendMessage_datos_personales", personal["mensaje"])],
    )


def format_procedure_answer(entry: dict) -> str:
    """Redactar la respuesta fija de un procedimiento del TUPA.

    :param entry: campos de la ficha.
    :return: texto con denominación, código, costo, plazo, dónde y fuente.
    """
    fields = build_card_fields(entry)
    return (
        f"{fields['Name']} (código {fields['Code']}).\n\n"
        f"- Costo: {fields['Fee']}\n"
        f"- Plazo de atención: {fields['Term']}\n"
        f"- Dónde se presenta: {fields['Office']}\n"
        f"- Contacto: {fields['Contact']}\n\n"
        f"Fuente: TUPA UCSM, págs. {fields['Pages']}"
    )


def build_late_exam_topic(protocol: dict, entries: list[dict]) -> dict:
    """Construir el Topic propio *Evaluación extemporánea*.

    :param protocol: contenido de ``protocolo.yaml``.
    :param entries: campos de las fichas del TUPA.
    :return: diálogo con pregunta de opción múltiple y una respuesta por
        escuela generada desde ``tupa.json``; si el texto contiene
        "Postgrado" se muestra el trámite de postgrado, si no el de pregrado.
    """
    intent = find_intent(protocol, "desambiguacion_evaluacion_extemporanea")
    by_code = {entry["code"]: entry for entry in entries}
    options = intent["opciones"]
    graduate = next(o for o in options if GRADUATE_KEYWORD in o["etiqueta"])
    undergraduate = next(o for o in options if o is not graduate)

    def answer(option: dict) -> dict:
        code = option["codigo_tupa"]
        return build_message(f"sendMessage_{code}",
                             format_procedure_answer(by_code[code]))

    condition_group = {
        "kind": "ConditionGroup",
        "id": "condition_escuela",
        "conditions": [
            {
                "id": "condition_postgrado",
                "condition": f'="{GRADUATE_KEYWORD}" in Topic.Escuela',
                "actions": [answer(graduate)],
            },
        ],
        "elseActions": [answer(undergraduate)],
    }
    question = {
        "kind": "Question",
        "id": "question_escuela",
        "alwaysPrompt": True,
        "variable": "init:Topic.Escuela",
        "prompt": {
            "text": [intent["pregunta"]],
            "quickReplies": [
                {"kind": "MessageBack", "text": option["etiqueta"]}
                for option in options
            ],
        },
        "entity": "StringPrebuiltEntity",
    }
    return build_custom_topic(
        "Responde cómo solicitar una evaluación extemporánea (examen "
        "rezagado por enfermedad u otro motivo). Pregunta si es para una "
        "Escuela Profesional (pregrado) o para la Escuela de Postgrado y "
        "muestra el trámite del TUPA correspondiente. No lo uses si el "
        "usuario también pregunta qué dice el Reglamento, esa consulta "
        "combinada se responde con los documentos de conocimiento.",
        "Evaluación extemporánea",
        [question, condition_group],
    )


def quote_literal(text: str) -> str:
    """Escapar un texto como literal Power Fx sin alterar sus espacios.

    :param text: texto original.
    :return: literal entre comillas dobles con comillas duplicadas.
    """
    return '"' + text.replace('"', '""') + '"'


def build_powerfx_template(template: str, record: str) -> str:
    """Convertir una plantilla del protocolo en una expresión Power Fx.

    :param template: texto con campos entre llaves, p. ej. ``págs. {Pages}``.
    :param record: variable que contiene los campos, p. ej. ``Topic.Ficha``.
    :return: concatenación Power Fx, p. ej. ``"págs. " & Topic.Ficha.Pages``.
    """
    parts = []
    position = 0
    for match in CARD_PLACEHOLDER.finditer(template):
        if match.start() > position:
            parts.append(quote_literal(template[position:match.start()]))
        parts.append(f"{record}.{match.group(1)}")
        position = match.end()
    if position < len(template):
        parts.append(quote_literal(template[position:]))
    return " & ".join(parts)


def build_card_formula(card: dict, record: str) -> str:
    """Construir la Adaptive Card de un trámite como fórmula Power Fx.

    :param card: definición ``tarjeta`` del protocolo.
    :param record: variable con la fila de la tabla del TUPA.
    :return: fórmula ``={...}`` para un adjunto *AdaptiveCardTemplate*.
    """
    facts = ",\n".join(
        f"      {{title: {quote_powerfx(field['etiqueta'])}, "
        f"value: {build_powerfx_template(field['valor'], record)}}}"
        for field in card["campos"]
    )
    title = build_powerfx_template(card["titulo"], record)
    return (
        "={\n"
        '  type: "AdaptiveCard",\n'
        f"  '$schema': \"{CARD_SCHEMA}\",\n"
        '  version: "1.5",\n'
        "  body: [\n"
        f"    {{type: \"TextBlock\", text: {title}, weight: \"Bolder\", "
        'size: "Medium", wrap: true},\n'
        '    {type: "FactSet", facts: [\n'
        f"{facts}\n"
        "    ]}\n"
        "  ]\n"
        "}"
    )


def normalize_formula(expression: str) -> str:
    """Envolver una expresión Power Fx para normalizar el texto.

    :param expression: expresión de texto Power Fx.
    :return: expresión en minúsculas, sin tildes ni guiones y con "rr"
        reducido a "r".
    """
    formula = f"Lower({expression})"
    for old, new in NORMALIZATION:
        formula = f'Substitute({formula}, "{old}", "{new}")'
    return formula


def build_procedure_topic(protocol: dict, entries: list[dict]) -> dict:
    """Construir el Topic propio *Consulta de trámite*.

    El procedimiento llega como entrada de texto del Topic (la orquestación
    la extrae del mensaje o la pregunta). Se elige, en la tabla Power Fx
    generada desde ``tupa.json``, la ficha cuyo código coincide o cuyo
    nombre contiene más palabras del texto; se ignoran las palabras cortas y
    genéricas. Texto y nombre se comparan normalizados (sin tildes ni
    guiones) y cada palabra se busca por sus primeros ``STEM_LENGTH``
    caracteres. Debe coincidir más de la mitad de las palabras; a igual
    número de coincidencias gana la que tiene más palabras completas en el
    nombre ("titulo" está en "títulos" pero no en "Titular") y luego el
    nombre más corto (el más específico). Si aun así varias fichas empatan
    con nombres de largo parecido (por ejemplo "copia autenticada de mi
    título": acta de grados o resolución del título), se listan con su costo
    y plazo y se pregunta cuál, en lugar de elegir una. Una entidad de lista
    cerrada embebida no sirve: Copilot Studio le asigna un tipo de conjunto
    de opciones que la entrada de texto no acepta.

    :param protocol: contenido de ``protocolo.yaml``.
    :param entries: campos de las fichas del TUPA.
    :return: diálogo con entrada, búsqueda, desambiguación, Adaptive Card y
        pregunta de seguimiento.
    """
    intent = find_intent(protocol, "consulta_tramite")
    no_evidence = find_intent(protocol, "sin_evidencia")
    table = build_powerfx_table(entries).strip()
    user_text = normalize_formula("Trim(Topic.Tramite)")
    candidates = (
        f"=With({{palabras: Filter(Split({user_text}, \" \"), "
        f"Len(Value) > 3 && !(Value in [{IGNORED_WORDS}]))}}, "
        "Sort(Filter(AddColumns(AddColumns(AddColumns(AddColumns("
        f"{table}, Key, {normalize_formula('Name')}), Hits, "
        "If(Code = Upper(Trim(Topic.Tramite)), 100, "
        f"CountIf(palabras, Left(Value, {STEM_LENGTH}) in Key))), "
        "Exact, CountIf(palabras, Value in Key)), "
        "Score, Hits * 100000 + Exact * 1000 - Len(Name)), "
        "Hits * 2 > CountRows(palabras)), Score, SortOrder.Descending))"
    )
    similar = (
        "=With({mejor: First(Topic.Candidatas)}, FirstN(Filter("
        "Topic.Candidatas, Hits = mejor.Hits && Exact = mejor.Exact && "
        f"Len(Name) <= Len(mejor.Name) * {SIMILAR_NAME_RATIO}), "
        f"{MAX_OPTIONS}))"
    )
    option = "Index(Topic.Parecidas, Value)"
    options_text = (
        "=Concat(Sequence(CountRows(Topic.Parecidas)), Value & \". \" & "
        f"{option}.Name & \" (\" & {option}.Code & \"): \" & "
        f"{option}.Fee & \", \" & {option}.Term, Char(10))"
    )
    choice_text = normalize_formula("Trim(Topic.Eleccion)")
    chosen = (
        "=With({e: Trim(Topic.Eleccion), "
        "n: IfError(Value(Trim(Topic.Eleccion)), 0)}, Coalesce("
        "LookUp(Topic.Parecidas, Code = Upper(e)), "
        "If(n >= 1 && n <= CountRows(Topic.Parecidas), "
        "Index(Topic.Parecidas, n)), "
        "First(DropColumns(Sort(AddColumns(Topic.Parecidas, Elegida, "
        f"CountIf(Split({choice_text}, \" \"), Len(Value) > 3 && "
        f"Left(Value, {STEM_LENGTH}) in Key)), Elegida, "
        "SortOrder.Descending), Elegida))))"
    )
    input_description = (
        "Nombre del procedimiento o servicio del TUPA que el usuario quiere "
        "consultar, sin palabras de la pregunta (por ejemplo \"anulación de "
        "matrícula\", \"carné universitario\" o el código PA113073C401). "
        "Déjalo vacío si el usuario no nombra un trámite concreto."
    )
    return {
        "kind": "AdaptiveDialog",
        "inputs": [
            {
                "kind": "AutomaticTaskInput",
                "propertyName": "Tramite",
                "description": input_description,
                "entity": "StringPrebuiltEntity",
                "shouldPromptUser": False,
            },
        ],
        "modelDisplayName": "Consulta de trámite",
        "modelDescription": (
            "Muestra el costo, el plazo de atención, dónde se presenta y el "
            "contacto de un procedimiento o servicio del TUPA de la UCSM "
            "(por ejemplo anulación de matrícula, constancia de estudios o "
            "duplicado de carné). Úsalo cuando el usuario pregunte cuánto "
            "cuesta, cuánto demora o dónde se tramita algo, y también cuando "
            "diga que quiere hacer un trámite sin nombrarlo (por ejemplo "
            "\"quiero hacer un trámite\"): en ese caso deja la entrada vacía "
            "para preguntar cuál. No lo uses si la pregunta también pide qué "
            "dice el Reglamento o si algo está permitido (por ejemplo "
            "\"¿puedo cambiarme de sección y cuánto cuesta?\"): esas "
            "consultas combinadas se responden con los documentos de "
            "conocimiento."
        ),
        "beginDialog": {
            "kind": "OnRecognizedIntent",
            "id": "main",
            "intent": {},
            "actions": [
                # La orquestación redacta su propia pregunta si la entrada
                # se pide sola; así se usa el texto literal del protocolo.
                {
                    "kind": "ConditionGroup",
                    "id": "condition_tramite_vacio",
                    "conditions": [
                        {
                            "id": "condition_tramite_vacio_si",
                            "condition": "=IsBlank(Topic.Tramite)",
                            "actions": [
                                {
                                    "kind": "Question",
                                    "id": "question_tramite",
                                    "alwaysPrompt": True,
                                    "variable": "Topic.Tramite",
                                    "prompt": " ".join(
                                        intent["pregunta_si_no_reconoce"]
                                        .split()),
                                    "entity": "StringPrebuiltEntity",
                                },
                            ],
                        },
                    ],
                },
                {
                    "kind": "SetVariable",
                    "id": "setVariable_candidatas",
                    "variable": "init:Topic.Candidatas",
                    "value": candidates,
                },
                {
                    "kind": "SetVariable",
                    "id": "setVariable_parecidas",
                    "variable": "init:Topic.Parecidas",
                    "value": similar,
                },
                {
                    "kind": "SetVariable",
                    "id": "setVariable_ficha",
                    "variable": "init:Topic.Ficha",
                    "value": "=First(Topic.Candidatas)",
                },
                # Varias fichas igual de probables: listarlas y preguntar.
                {
                    "kind": "ConditionGroup",
                    "id": "condition_varias",
                    "conditions": [
                        {
                            "id": "condition_varias_si",
                            "condition": "=CountRows(Topic.Parecidas) > 1",
                            "actions": [
                                {
                                    "kind": "SetVariable",
                                    "id": "setVariable_opciones",
                                    "variable": "init:Topic.Opciones",
                                    "value": options_text,
                                },
                                build_message(
                                    "sendMessage_varias",
                                    f"{intent['varias_fichas']}\n\n"
                                    "{Topic.Opciones}"),
                                {
                                    "kind": "Question",
                                    "id": "question_ficha",
                                    "alwaysPrompt": True,
                                    "variable": "init:Topic.Eleccion",
                                    "prompt": intent["pregunta_cual"],
                                    "entity": "StringPrebuiltEntity",
                                },
                                {
                                    "kind": "SetVariable",
                                    "id": "setVariable_eleccion",
                                    "variable": "Topic.Ficha",
                                    "value": chosen,
                                },
                            ],
                        },
                    ],
                },
                {
                    "kind": "ConditionGroup",
                    "id": "condition_ficha",
                    "conditions": [
                        {
                            "id": "condition_sin_ficha",
                            "condition": "=IsBlank(Topic.Ficha)",
                            "actions": [
                                build_message("sendMessage_sin_ficha",
                                              no_evidence["mensaje"]),
                            ],
                        },
                    ],
                    "elseActions": [
                        {
                            "kind": "SendActivity",
                            "id": "sendMessage_tarjeta",
                            "activity": {
                                "attachments": [
                                    {
                                        "kind": "AdaptiveCardTemplate",
                                        "cardContent": build_card_formula(
                                            intent["tarjeta"], "Topic.Ficha"
                                        ),
                                    },
                                ],
                            },
                        },
                        build_message("sendMessage_requisitos",
                                      intent["mensaje_despues"]),
                    ],
                },
                {"kind": "CancelAllDialogs", "id": "cancelAllDialogs_fin"},
            ],
        },
        "inputType": {
            "properties": {
                "Tramite": {
                    "displayName": "Tramite",
                    "description": input_description,
                    "type": "String",
                },
            },
        },
    }


class DialogDumper(yaml.SafeDumper):
    """Serializador YAML con el formato del editor de Copilot Studio.

    Indenta las listas bajo su clave (el editor rechaza las listas sin
    sangría) y escribe los textos multilínea como bloque.
    """

    def increase_indent(self, flow: bool = False,
                        indentless: bool = False) -> None:
        """Indentar siempre las secuencias anidadas en un mapeo."""
        super().increase_indent(flow, False)


def represent_text(dumper: yaml.SafeDumper, text: str) -> yaml.ScalarNode:
    """Representar un texto con el estilo que acepta Copilot Studio.

    Los textos multilínea van en estilo literal (``|``); los que contienen
    una URL van entre comillas simples, porque el editor rechaza el ``:``
    de ``https:`` en un valor sin comillas.

    :param dumper: serializador YAML.
    :param text: texto a representar.
    :return: nodo escalar.
    """
    if "\n" in text:
        style = "|"
    elif "://" in text and not text.startswith("="):
        style = "'"
    else:
        style = None
    return dumper.represent_scalar("tag:yaml.org,2002:str", text, style=style)


DialogDumper.add_representer(str, represent_text)


def dump_dialog(dialog: dict) -> str:
    """Serializar un diálogo al YAML del editor de código.

    :param dialog: diálogo.
    :return: texto YAML con tildes y sin reordenar claves.
    """
    return yaml.dump(dialog, Dumper=DialogDumper, allow_unicode=True,
                     sort_keys=False, width=1000)


def write_dialogs(protocol: dict, entries: list[dict],
                  topics_dir: Path) -> dict[str, Path]:
    """Escribir el YAML de los Topics del sistema y propios.

    :param protocol: contenido de ``protocolo.yaml``.
    :param entries: campos de las fichas del TUPA.
    :param topics_dir: carpeta ``copilot/topics``.
    :return: rutas generadas por nombre de Topic.
    """
    dialogs = {
        "sistema_inicio_conversacion": build_conversation_start(protocol),
        "sistema_alternativa": build_fallback(protocol),
        "sistema_fin_conversacion": build_end_of_conversation(protocol),
        "menu_temas": build_menu_topic(protocol),
        "cierre_conversacion": build_closing_topic(protocol),
        "datos_personales": build_personal_data_topic(protocol),
        "evaluacion_extemporanea": build_late_exam_topic(protocol, entries),
        "consulta_tramite": build_procedure_topic(protocol, entries),
    }
    topics_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, dialog in dialogs.items():
        path = topics_dir / f"{name}.yaml"
        path.write_text(dump_dialog(dialog), encoding="utf-8")
        paths[name] = path
    return paths
