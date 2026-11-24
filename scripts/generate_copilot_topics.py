"""Generar la entidad y la tabla Power Fx a partir de data/processed/tupa.json.

Uso: ``python scripts/generate_copilot_topics.py`` (ejecutar antes
``python -m ucsm_bot.build`` para tener ``tupa.json`` actualizado).
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.copilot_topics import write_topics  # noqa: E402
from ucsm_bot.corpus import PROCESSED_DIR, TOPICS_DIR  # noqa: E402


def main() -> None:
    """Leer ``tupa.json`` y escribir los archivos de ``copilot/topics``."""
    entries = json.loads((PROCESSED_DIR / "tupa.json").read_text("utf-8"))
    for name, path in write_topics(entries, TOPICS_DIR).items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
