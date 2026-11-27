# Evaluación

| Archivo | Uso |
|---|---|
| `questions.yaml` | Banco de 44 preguntas. Verificar con `.venv/bin/python eval/check_questions.py` |
| `results.csv` | Una fila por pregunta del banco ejecutado en el agente publicado (columnas abajo) |
| `run_bank.py` | Ejecuta el banco en el agente publicado por Direct Line (token anónimo, una conversación por pregunta) → `transcripts.jsonl`. Requiere la variable `UCSM_BOT_TOKEN_URL` |
| `to_results.py` | Combina `transcripts.jsonl` y la calificación manual `calificacion.json` → `results.csv` |
| `evaluacion_completa.md` | Método, resultados de las cuatro rondas, brechas y revisión pendiente; los archivos de `eval/` son la ronda 4 |
| `compute_metrics.py` | `.venv/bin/python eval/compute_metrics.py` → `reporte.md` |
| `rubrica.md` | Criterios para la columna `rubric` |
| `tareas_usabilidad.md` | Preparación, invitación, guion de la sesión y tareas |
| `formulario_sus.md` | Cómo crear el cuestionario SUS en Microsoft Forms y exportarlo |
| `forms_to_sus.py` | Exportación de Forms (`.xlsx` o CSV) → `sus.csv` |
| `sus.csv`, `tareas.csv` | Datos de la prueba (9 participantes): respuestas SUS anónimas (salen de `forms_to_sus.py`) y éxito por tarea según las notas del facilitador; calcular con `eval/compute_sus.py` |
| `usabilidad.md` | Resultados de la prueba: SUS 85,8, éxito por tarea, comentarios y cambios derivados |
| `analitica.md` | Analítica de Copilot Studio (187 sesiones, resultados, temas por fase); el CSV de sesiones no se guarda (incluye transcripciones) |

Columnas de `results.csv`: `answer` (texto de la respuesta),
`sources_cited` (citas mostradas, p. ej. "Art. 83°; PA113073C401"),
`card_shown` (sí/no), `card_text` (contenido de la Adaptive Card),
`latency_s` (segundos desde el envío hasta la respuesta completa),
`refused` (opcional, sí/no; si se deja vacío se detecta por frases del
protocolo), `rubric` (ver `rubrica.md`) y `notes`.
