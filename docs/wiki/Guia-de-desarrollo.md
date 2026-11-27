# Guía de desarrollo

## Requisitos

- Python 3.13.
- Para regenerar el diagrama del protocolo: Node.js (`npx`).
- Para cargar el agente: una cuenta con acceso a Copilot Studio que permita
  publicar sin autenticación.

## Instalación

```bash
python3.13 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Dependencias: `python-docx`, `pyyaml` y `pytest`.

## Generar los artefactos

```bash
PYTHONPATH=src .venv/bin/python -m ucsm_bot.build
```

El comando es determinista y genera:

- `data/processed/`: texto limpio, `units.jsonl`, `chunks.jsonl`,
  `tupa.json` e `ingest_report.md`;
- `copilot/knowledge/`: los documentos de conocimiento;
- `copilot/topics/`: el YAML de los Topics, la entidad y la tabla Power Fx.

## Pruebas

```bash
.venv/bin/python -m pytest
```

Las pruebas cubren la limpieza, la segmentación, los campos del TUPA, los
artefactos generados y la evaluación.

## Otros comandos

| Comando | Qué hace |
|---|---|
| `.venv/bin/python eval/check_questions.py` | Verifica el banco de preguntas y que montos y plazos coincidan con el TUPA |
| `.venv/bin/python eval/run_bank.py` | Ejecuta el banco en el agente publicado (requiere la variable `UCSM_BOT_TOKEN_URL`) |
| `.venv/bin/python eval/to_results.py` | Combina transcripciones y calificación en `eval/results.csv` |
| `.venv/bin/python eval/compute_metrics.py` | Calcula las métricas y escribe `eval/reporte.md` |
| `.venv/bin/python eval/forms_to_sus.py <exportación.xlsx>` | Convierte la exportación de Microsoft Forms en `eval/sus.csv` |
| `.venv/bin/python eval/compute_sus.py` | Calcula el SUS y el éxito por tarea |
| `.venv/bin/python scripts/generate_copilot_topics.py` | Regenera solo la entidad y la tabla Power Fx |

## Actualizar el agente

1. Si cambian los documentos de la UCSM, reemplazar `data/raw/` y ejecutar
   el build y las pruebas.
2. En Copilot Studio, reemplazar los archivos de *Knowledge* y esperar a
   que queden en *Ready* antes de publicar.
3. Si cambian los Topics, pegar el YAML de `copilot/topics/` en el editor
   de código de cada Topic.
4. Si cambian las instrucciones, pegar el bloque de
   `copilot/instructions.md` en *Overview → Instructions*.
5. Publicar, ejecutar el banco y exportar la solución con una versión
   nueva en `copilot/solution/`.

## Estructura del repositorio

```
copilot/   instrucciones, conocimiento, Topics y solución exportada
data/      documentos fuente, inventario y corpus procesado
docs/      alcance, análisis del corpus, protocolo, guion de verificación,
           bitácora, figuras y esta wiki (docs/wiki/)
eval/      banco de preguntas, ejecución, métricas, rúbrica y usabilidad
scripts/   generación de Topics y publicación de la wiki
src/       paquete ucsm_bot
tests/     pruebas
```

## Publicar esta wiki

Las páginas están en `docs/wiki/` y las imágenes salen de `docs/figuras/`.
Con la wiki activada en GitHub y una primera página creada desde la web:

```bash
scripts/publish_wiki.sh --no-push
```

revisa el commit en la carpeta de la wiki, y sin `--no-push` lo publica.
