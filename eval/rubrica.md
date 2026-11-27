# Rúbrica de calificación manual

Cada respuesta del banco se califica en la columna `rubric` de
`eval/results.csv` con uno de estos valores. Se compara con
`expected_answer`, `sources`, `expected_fee` y `expected_term` de
`eval/questions.yaml` y, ante la duda, con el PDF oficial.

| Valor | Criterio | Ejemplo |
|---|---|---|
| `correcta` | Contiene lo esencial de la respuesta esperada, sin errores, y cita la fuente correcta (artículo o código). En fuera de alcance / sin respuesta: rechaza o deriva sin inventar. | REG-01: separación por un año, retiro a la cuarta vez, cita Art. 83° |
| `parcial` | Es correcta pero incompleta (omite un requisito, una condición o la segunda fuente de una combinada) o cita el documento sin el artículo o código. | REG-01: menciona la separación pero no el retiro definitivo |
| `incorrecta` | Contradice el documento, da un monto o plazo equivocado, responde una pregunta fuera de alcance o no responde una que sí está en el corpus. | TUPA-01: "S/ 40.00" |
| `alucinada` | Inventa un artículo, código, monto, requisito u oficina que no existe en el corpus, o cita una fuente que no contiene lo afirmado. | Cita "Art. 210°" o un código TUPA inexistente |

**Metas:** ≥ 80 % de respuestas `correcta` o
`parcial` y 0 respuestas `alucinada`. `eval/compute_metrics.py` calcula los
porcentajes y los compara con la meta en `eval/reporte.md`.

**Procedimiento:**

1. Calificar sin mirar las métricas automáticas.
2. Si hay duda entre dos valores, elegir el más bajo y anotar el motivo en
   la columna `notes`.
3. Una segunda persona revisa al menos 10 respuestas al azar; si hay
   desacuerdo, se discute y se registra la calificación acordada.
