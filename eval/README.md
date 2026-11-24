# Evaluación

| Archivo | Tarea | Uso |
|---|---|---|
| `questions.yaml` | 6.1 | Banco de 44 preguntas. Verificar con `.venv/bin/python eval/check_questions.py` |
| `results_template.csv` | 7.1 | Copiar como `results.csv` y llenar una fila por pregunta al ejecutar el banco en el agente publicado |
| `compute_metrics.py` | 7.2 | `.venv/bin/python eval/compute_metrics.py` → `reporte.md` |
| `rubrica.md` | 7.3 | Criterios para la columna `rubric` |
| `tareas_usabilidad.md` | 7.4 | Tareas, guion y cuestionario SUS |
| `sus_template.csv`, `tareas_template.csv` | 7.4 | Copiar como `sus.csv` y `tareas.csv`; calcular con `eval/compute_sus.py` |

Columnas de `results.csv`: `answer` (texto de la respuesta),
`sources_cited` (citas mostradas, p. ej. "Art. 83°; PA113073C401"),
`card_shown` (sí/no), `card_text` (contenido de la Adaptive Card),
`latency_s` (segundos desde el envío hasta la respuesta completa),
`refused` (opcional, sí/no; si se deja vacío se detecta por frases del
protocolo), `rubric` (ver `rubrica.md`) y `notes`.
