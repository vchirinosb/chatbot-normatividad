"""Calcular las métricas del agente y escribir eval/reporte.md.

Uso: ``.venv/bin/python eval/compute_metrics.py [results.csv]``
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import (  # noqa: E402
    EVAL_DIR,
    compute_metrics,
    load_questions,
    read_csv,
    render_report,
)


def main() -> None:
    """Leer los resultados, calcular métricas y escribir el reporte."""
    results = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        EVAL_DIR / "results.csv"
    )
    metrics = compute_metrics(load_questions(), read_csv(results))
    report = EVAL_DIR / "reporte.md"
    report.write_text(render_report(metrics), encoding="utf-8")
    print(f"Reporte: {report}")


if __name__ == "__main__":
    main()
