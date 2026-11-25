"""Convertir la exportación de Microsoft Forms a ``eval/sus.csv`` (tarea 7.4).

Uso: ``.venv/bin/python eval/forms_to_sus.py <exportacion.xlsx>``

Acepta el ``.xlsx`` que descarga Forms (*Descargar una copia*) o un CSV
guardado desde Excel. Después ejecutar ``eval/compute_sus.py``.
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ucsm_bot.evaluation import (  # noqa: E402
    EVAL_DIR,
    convert_forms_export,
    read_table,
)


def main() -> None:
    """Escribir ``eval/sus.csv`` a partir de la exportación indicada."""
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rows = convert_forms_export(read_table(Path(sys.argv[1])))
    out_path = EVAL_DIR / "sus.csv"
    fields = ["participant", *[f"q{i}" for i in range(1, 11)]]
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} participantes -> {out_path}")


if __name__ == "__main__":
    main()
