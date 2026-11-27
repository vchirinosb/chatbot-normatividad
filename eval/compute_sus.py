"""Calcular el SUS y las métricas de tareas de usabilidad.

Uso: ``.venv/bin/python eval/compute_sus.py`` (lee eval/sus.csv y
eval/tareas.csv).
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import (  # noqa: E402
    EVAL_DIR,
    SUS_TARGET,
    compute_sus,
    read_csv,
)


def main() -> None:
    """Imprimir el SUS por participante, el promedio y las tareas."""
    tasks_path = EVAL_DIR / "tareas.csv"
    result = compute_sus(
        read_csv(EVAL_DIR / "sus.csv"),
        read_csv(tasks_path) if tasks_path.exists() else [],
    )
    for participant, score in result["scores"].items():
        print(f"{participant}: {score:.1f}")
    mean = result["mean"]
    status = "cumple" if mean >= SUS_TARGET else "no cumple"
    print(f"SUS promedio: {mean:.1f} (meta ≥ {SUS_TARGET:.0f}, {status})")
    for name, task in result["tasks"].items():
        seconds = task["mean_seconds"]
        print(f"{name}: éxito {task['success_rate'] * 100:.0f} %, "
              f"tiempo medio "
              f"{'—' if math.isnan(seconds) else f'{seconds:.0f} s'}")


if __name__ == "__main__":
    main()
