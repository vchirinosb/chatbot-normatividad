"""Verificar los mínimos del banco de preguntas.

Uso: ``.venv/bin/python eval/check_questions.py``
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import (  # noqa: E402
    MINIMUMS,
    bank_summary,
    check_bank,
    load_article_titles,
    load_questions,
    load_tupa,
)


def main() -> int:
    """Imprimir los conteos y los errores del banco."""
    questions = load_questions()
    titles = load_article_titles()
    summary = bank_summary(questions, titles)
    for key, minimum in MINIMUMS.items():
        print(f"{key}: {summary.get(key, 0)} (mínimo {minimum})")
    print(f"subconjunto de iteración: {summary['subset']}")
    errors = check_bank(questions, load_tupa(), titles)
    for error in errors:
        print(f"ERROR {error}")
    print("Banco válido" if not errors else "Banco inválido")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
