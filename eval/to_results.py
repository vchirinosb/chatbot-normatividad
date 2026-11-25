"""Convertir las transcripciones del banco en ``results.csv`` (tareas 7.1 y 7.3).

Uso::

    .venv/bin/python eval/to_results.py [transcripts.jsonl] [calificacion.json] [results.csv]

``calificacion.json`` contiene, por id de pregunta, la calificación manual
según ``rubrica.md``: ``rubric``, ``notes`` y, opcionalmente, ``refused``.
Si no existe, las columnas de la rúbrica quedan vacías.
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import EVAL_DIR, cited_sources, load_questions  # noqa: E402

FIELDS = ["id", "question", "answer", "sources_cited", "card_shown",
          "card_text", "latency_s", "refused", "rubric", "notes"]


def format_sources(text: str) -> str:
    """Listar las fuentes citadas en el formato de ``results_template.csv``."""
    sources = cited_sources(text)
    articles = sorted(int(s.split(":")[1]) for s in sources
                      if s.startswith("art:"))
    codes = sorted(s.split(":")[1] for s in sources if s.startswith("code:"))
    return "; ".join([f"Art. {n}°" for n in articles] + codes)


def build_rows(transcripts: list[dict], grades: dict) -> list[dict]:
    """Armar una fila por pregunta del banco, en el orden del banco."""
    by_id = {record["id"]: record for record in transcripts}
    rows = []
    for question in load_questions():
        record = by_id.get(question["id"], {})
        answer = " ".join(" ".join(record.get("texts", [])).split())
        card = " | ".join(record.get("cards", []))
        grade = grades.get(question["id"], {})
        latency = record.get("latency_s")
        rows.append({
            "id": question["id"],
            "question": question["question"],
            "answer": answer,
            "sources_cited": format_sources(card + " " + answer),
            "card_shown": "sí" if card else "no",
            "card_text": card,
            "latency_s": "" if latency is None else f"{latency:.2f}",
            "refused": grade.get("refused", ""),
            "rubric": grade.get("rubric", ""),
            "notes": grade.get("notes", ""),
        })
    return rows


def main() -> None:
    """Leer transcripciones y calificaciones y escribir el CSV."""
    args = sys.argv[1:]
    transcripts_path = Path(args[0]) if args else EVAL_DIR / "transcripts.jsonl"
    grades_path = Path(args[1]) if len(args) > 1 else EVAL_DIR / "calificacion.json"
    out_path = Path(args[2]) if len(args) > 2 else EVAL_DIR / "results.csv"
    transcripts = [json.loads(line) for line in
                   transcripts_path.read_text(encoding="utf-8").splitlines()
                   if line.strip()]
    grades = (json.loads(grades_path.read_text(encoding="utf-8"))
              if grades_path.exists() else {})
    rows = build_rows(transcripts, grades)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} filas -> {out_path}")


if __name__ == "__main__":
    main()
