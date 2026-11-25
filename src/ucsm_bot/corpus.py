"""Inventario del corpus y rutas del proyecto."""

import csv
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT_DIR / "data" / "inventory.csv"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
KNOWLEDGE_DIR = ROOT_DIR / "copilot" / "knowledge"
TOPICS_DIR = ROOT_DIR / "copilot" / "topics"
PROTOCOL_PATH = ROOT_DIR / "docs" / "protocolo.yaml"

REGULATION_ID = "reglamento-estudiantes"
TUPA_ID = "tupa"

EXPECTED_ARTICLES = 159
EXPECTED_TUPA_ENTRIES = 63
EXPECTED_PROCEDURES = 48
EXPECTED_SERVICES = 15


@dataclass(frozen=True)
class Document:
    """Documento del corpus con sus metadatos de inventario."""

    doc_id: str
    title: str
    doc_type: str
    resolution: str
    version: str
    date: str
    source_url: str
    pages: int
    pdf_path: Path
    md_path: Path


def load_inventory(
    inventory_path: Path = INVENTORY_PATH, root_dir: Path = ROOT_DIR
) -> dict[str, Document]:
    """Cargar el inventario y verificar que existan los archivos.

    :param inventory_path: ruta del CSV de inventario.
    :param root_dir: carpeta base para resolver las rutas relativas.
    :return: documentos indexados por ``doc_id``.
    :raises FileNotFoundError: si falta el PDF o el Markdown de un documento.
    """
    documents: dict[str, Document] = {}
    with inventory_path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            document = Document(
                doc_id=row["doc_id"],
                title=row["title"],
                doc_type=row["doc_type"],
                resolution=row["resolution"],
                version=row["version"],
                date=row["date"],
                source_url=row["source_url"],
                pages=int(row["pages"]),
                pdf_path=root_dir / row["pdf_path"],
                md_path=root_dir / row["md_path"],
            )
            for path in (document.pdf_path, document.md_path):
                if not path.exists():
                    raise FileNotFoundError(
                        f"Falta el archivo del documento "
                        f"'{document.doc_id}': {path}"
                    )
            documents[document.doc_id] = document
    return documents
