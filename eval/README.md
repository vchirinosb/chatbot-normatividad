# Evaluación

| Archivo | Tarea | Uso |
|---|---|---|
| `questions.yaml` | 6.1 | Banco de 44 preguntas. Verificar con `.venv/bin/python eval/check_questions.py` |
| `results_template.csv` | 7.1 | Copiar como `results.csv` y llenar una fila por pregunta al ejecutar el banco en el agente publicado |
| `run_bank.py` | 7.1 | Ejecuta el banco en el agente publicado por Direct Line (token anónimo, una conversación por pregunta) → `transcripts.jsonl`. Requiere la variable `UCSM_BOT_TOKEN_URL` |
| `to_results.py` | 7.1, 7.3 | Combina `transcripts.jsonl` y la calificación manual `calificacion.json` → `results.csv` |
| `evaluacion_completa.md` | 7.1–7.3 | Método, resultados de las tres rondas, brechas y revisión pendiente |
| `ronda1/` | 7.1–7.3 | Transcripciones, calificación, resultados y reporte de la ronda 1 (antes de corregir la búsqueda de trámites) |
| `ronda2/` | 7.1–7.3 | Lo mismo para la ronda 2 (antes de anteponer el artículo a cada párrafo del Reglamento) |
| `compute_metrics.py` | 7.2 | `.venv/bin/python eval/compute_metrics.py` → `reporte.md` |
| `rubrica.md` | 7.3 | Criterios para la columna `rubric` |
| `tareas_usabilidad.md` | 7.4 | Preparación, invitación, guion de la sesión y tareas |
| `formulario_sus.md` | 7.4 | Cómo crear el cuestionario SUS en Microsoft Forms y exportarlo |
| `forms_to_sus.py` | 7.4 | Exportación de Forms (CSV) → `sus.csv` |
| `sus_template.csv`, `tareas_template.csv` | 7.4 | `tareas.csv` se llena en la sesión; `sus.csv` sale de `forms_to_sus.py` (o a mano); calcular con `eval/compute_sus.py` |
| `usabilidad.md` | 7.4 | Resultados de la prueba (por completar) |

Columnas de `results.csv`: `answer` (texto de la respuesta),
`sources_cited` (citas mostradas, p. ej. "Art. 83°; PA113073C401"),
`card_shown` (sí/no), `card_text` (contenido de la Adaptive Card),
`latency_s` (segundos desde el envío hasta la respuesta completa),
`refused` (opcional, sí/no; si se deja vacío se detecta por frases del
protocolo), `rubric` (ver `rubrica.md`) y `notes`.
