"""Ejecutar el banco de preguntas en el agente publicado (tarea 7.1).

Cada pregunta se envía en una conversación nueva de Direct Line con un token
anónimo, igual que un visitante del Demo website sin sesión de Microsoft.
La latencia es la diferencia entre la marca de tiempo del servidor del
mensaje del usuario y la del último mensaje del agente.

Uso::

    UCSM_BOT_TOKEN_URL='https://<entorno>.environment.api.powerplatform.com/powervirtualagents/botsbyschema/<esquema>/directline/token?api-version=2022-03-01-preview' \\
    .venv/bin/python eval/run_bank.py [eval/transcripts.jsonl]

La URL del token no se guarda en el repositorio porque identifica el
entorno. Las respuestas en bruto se escriben en JSON Lines; ``to_results``
las convierte en ``results.csv``.
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import EVAL_DIR, load_questions  # noqa: E402

DIRECT_LINE = "https://directline.botframework.com/v3/directline"
USER = {"id": "evaluacion-anonima", "name": "evaluacion"}
POLL_SECONDS = 2.0
QUIET_SECONDS = 8.0
MAX_WAIT_SECONDS = 90.0


def call_json(url: str, token: str | None = None, body: dict | None = None) -> dict:
    """Llamar a un endpoint JSON con GET, o con POST si hay cuerpo o token."""
    data = None if body is None else json.dumps(body).encode()
    method = "POST" if body is not None else "GET"
    request = urllib.request.Request(url, data=data, method=method)
    if token:
        request.add_header("Authorization", "Bearer " + token)
    if body is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read() or b"{}")


def parse_timestamp(value: str) -> float:
    """Convertir la marca de tiempo ISO de Direct Line a segundos."""
    value = value.rstrip("Z")
    if "." in value:
        head, frac = value.split(".")
        value = f"{head}.{frac[:6]}"
    return datetime.fromisoformat(value).timestamp()


def extract_card_text(node) -> list[str]:
    """Extraer el texto visible de una Adaptive Card (TextBlock y FactSet)."""
    lines: list[str] = []
    if isinstance(node, dict):
        if node.get("type") == "TextBlock" and node.get("text"):
            lines.append(str(node["text"]))
        for fact in node.get("facts", []) or []:
            lines.append(f"{fact.get('title', '')}: {fact.get('value', '')}")
        for key, value in node.items():
            if key != "facts" and isinstance(value, (dict, list)):
                lines.extend(extract_card_text(value))
    elif isinstance(node, list):
        for item in node:
            lines.extend(extract_card_text(item))
    return lines


def ask_question(token_url: str, question: str) -> dict:
    """Abrir una conversación, enviar la pregunta y recoger las respuestas."""
    token = call_json(token_url)["token"]
    conversation = call_json(f"{DIRECT_LINE}/conversations", token, {})
    conversation_id = conversation["conversationId"]
    token = conversation.get("token", token)
    base = f"{DIRECT_LINE}/conversations/{conversation_id}/activities"
    call_json(base, token, {"type": "event", "name": "startConversation",
                            "from": USER, "locale": "es-PE"})
    time.sleep(3)
    sent = call_json(base, token, {"type": "message", "from": USER,
                                   "locale": "es-PE", "text": question})
    started = time.monotonic()
    last_change = started
    replies: dict[str, dict] = {}
    user_timestamp = None
    while time.monotonic() - started < MAX_WAIT_SECONDS:
        time.sleep(POLL_SECONDS)
        request = urllib.request.Request(base)
        request.add_header("Authorization", "Bearer " + token)
        with urllib.request.urlopen(request, timeout=60) as response:
            activities = json.loads(response.read())["activities"]
        for activity in activities:
            if activity.get("id") == sent.get("id"):
                user_timestamp = activity.get("timestamp")
                continue
            if (activity.get("type") != "message"
                    or activity.get("from", {}).get("id") == USER["id"]
                    or activity.get("replyToId") != sent.get("id")
                    or activity["id"] in replies):
                continue
            replies[activity["id"]] = activity
            last_change = time.monotonic()
        if replies and time.monotonic() - last_change >= QUIET_SECONDS:
            break
    ordered = sorted(replies.values(), key=lambda a: a.get("timestamp", ""))
    latency = None
    if ordered and user_timestamp:
        latency = round(parse_timestamp(ordered[-1]["timestamp"])
                        - parse_timestamp(user_timestamp), 2)
    return {
        "texts": [a.get("text", "") for a in ordered if a.get("text")],
        "cards": [line for a in ordered for att in a.get("attachments", [])
                  for line in extract_card_text(att.get("content"))],
        "latency_s": latency,
    }


def main() -> None:
    """Ejecutar todas las preguntas del banco y guardar las transcripciones."""
    token_url = os.environ.get("UCSM_BOT_TOKEN_URL")
    if not token_url:
        sys.exit("Falta la variable UCSM_BOT_TOKEN_URL.")
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        EVAL_DIR / "transcripts.jsonl"
    )
    done = set()
    if out_path.exists():
        done = {json.loads(line)["id"] for line in out_path.open(encoding="utf-8")}
    with out_path.open("a", encoding="utf-8") as out:
        for question in load_questions():
            if question["id"] in done:
                continue
            result = ask_question(token_url, question["question"])
            record = {"id": question["id"], "question": question["question"],
                      **result}
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            print(question["id"], result["latency_s"], flush=True)


if __name__ == "__main__":
    main()
