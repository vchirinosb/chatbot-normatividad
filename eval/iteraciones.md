# Iteraciones de ajuste del agente (tarea 6.2)

Registro de las rondas de ajuste ("entrenamiento") del agente *Normatividad
Estudiantil UCSM* en Copilot Studio con el subconjunto de 15 preguntas del
banco (`subset: true` en `questions.yaml`): REG-01, 02, 03, 05, 10, 17;
TUPA-01, 02, 04, 07, 11; COMB-01, 02; OUT-01, 03.

## Método

- Cada iteración se ejecuta en una sesión nueva del panel *Test your agent*
  (página recargada), con las 15 preguntas en el mismo orden y una pregunta
  por turno.
- Las respuestas se copian del panel y se guardan en
  `eval/iteraciones/itN.csv` con el formato de `results_template.csv`.
- Cada artículo, código, monto y plazo citado se contrasta con
  `data/processed/units.jsonl` y `data/processed/tupa.json`. La calificación
  sigue `rubrica.md`: ante la duda se elige el valor más bajo.
- Las métricas se calculan con `ucsm_bot.evaluation.compute_metrics`,
  restringido a las 15 preguntas. `reporte.md` queda reservado para la
  evaluación completa (tarea 7.2).
- La latencia no se midió en estas rondas (columna vacía). Se mide en la
  evaluación completa.

## Resumen

| Métrica | It. 1 | It. 2 | It. 3 |
|---|---|---|---|
| Correcta | 14 | 13 | 14 |
| Parcial | 1 | 0 | 1 |
| Incorrecta | 0 | 2 | 0 |
| Alucinada | 0 | 0 | 0 |
| Correcta + parcial | 100 % | 86,7 % | 100 % |
| Fuente esperada citada | 13/13 | 11/13 | 13/13 |
| Monto exacto | 7/7 | 5/7 | 6/7 |
| Plazo exacto | 7/7 | 5/7 | 6/7 |
| Rechazo fuera de alcance | 2/2 | 2/2 | 2/2 |

En las tres rondas no hubo respuestas alucinadas: ninguna inventó artículos,
códigos ni montos. Los artículos que se citaron además de los esperados
(32°, 72°, 84°, 86°, 135°) se verificaron en el corpus.

## Iteración 1 (2026-11-24): línea base

**Configuración:** instrucciones de la tarea 5.1, Topics de la tarea 5.2 y
búsqueda de trámites que acepta cualquier coincidencia (`Hits > 0`).

**Resultados:** 14 correctas y 1 parcial (`it1.csv`).

- REG-02 fue **parcial**: da la nota 12 en teoría y práctica, la nota 11
  para los planes anteriores a 2016 y la nota de modificación, pero omite el
  literal a del Art. 82° (asistencia al 100 % de la actividad práctica).
- Formato: las listas salían con viñetas y no numeradas, y REG-10 superó las
  150 palabras.
- Las cinco preguntas de TUPA mostraron la Adaptive Card con montos y plazos
  exactos. Las combinadas respondieron primero el Reglamento y luego el TUPA.

**Ajuste:** se añadieron dos reglas a la sección *Formato* de las
instrucciones (`copilot/instructions.md`):

1. presentar requisitos, condiciones, casos o pasos como lista numerada
   (1., 2., 3.), no con viñetas;
2. si el artículo enumera condiciones o literales, incluirlos todos, aunque
   sea en pocas palabras.

## Iteración 2 (2026-11-24): instrucciones ajustadas

**Resultados:** 13 correctas y 2 incorrectas (`it2.csv`).

- REG-02 pasó a **correcta**: ahora incluye la asistencia al 100 %.
- REG-01, REG-05 y REG-10 añadieron información pertinente y verificada
  (Art. 84°, Art. 86° y el límite de créditos del Art. 57°).
- **Regresiones de enrutamiento.** Las instrucciones no las causaron: la
  orquestación generativa eligió otro camino para las mismas preguntas.
  - COMB-01 → Topic *Evaluación extemporánea*: preguntó la escuela aunque el
    usuario dijo "pregrado" y no dio la regla del Art. 74°.
  - COMB-02 → Topic *Consulta de trámite*: la búsqueda por palabras devolvió
    *Cambio del Jurado Dictaminador del Proyecto de Tesis – Postgrado*
    (PA1130732A3B, Gratuito) porque coincidió con una sola palabra
    ("cambio").
- TUPA-07 se respondió con conocimiento generativo y no con la tarjeta, con
  los mismos montos y plazo. Se calificó correcta.

**Ajustes:**

1. Se añadió una exclusión a la descripción de los Topics *Consulta de
   trámite* y *Evaluación extemporánea*: no usarlos cuando la pregunta
   también pide qué dice el Reglamento o si algo está permitido. Esas
   consultas combinadas se responden con los documentos de conocimiento.
2. Se cambió el umbral de la búsqueda de trámites de `Hits > 0` a
   `Hits * 2 > CountRows(palabras)`: debe coincidir más de la mitad de las
   palabras significativas. El código exacto sigue valiendo 100.

Ambos cambios están en `src/ucsm_bot/copilot_dialogs.py` y en los YAML
regenerados de `copilot/topics/`.

## Iteración 3 (2026-11-24): descripciones y umbral ajustados

**Resultados:** 14 correctas y 1 parcial (`it3.csv`).

- COMB-01 volvió a **correcta**: Art. 74° (5 días hábiles, certificado
  visado, reprogramación dentro de 15 días hábiles) y luego PA1130732571.
- COMB-02 quedó **parcial**: cita bien el Art. 40° (rectificación de
  matrícula), pero dice que no encontró el monto en el TUPA. La recuperación
  no relaciona "cambio de sección" con *Rectificación de Matrícula*
  (PA113073BF13, S/ 13.00). No inventa el monto y deriva a la Escuela.
- Las cinco tarjetas de TUPA siguen apareciendo con el umbral nuevo.
- Las respuestas usan listas numeradas (10 listas `ol` en el panel).

## Observaciones y pendientes

- **No determinismo.** La misma pregunta puede ir al Topic o a la respuesta
  generativa según la ronda (TUPA-07, COMB-01, COMB-02). Por eso la
  evaluación completa (tarea 7) se hace sobre el agente publicado y una sola
  ronda se toma como medición. Las rondas de este registro no se promedian.
- **COMB-02** es una limitación conocida de la recuperación sobre
  `tupa_fichas.docx`: la ficha no contiene "sección". Se deja así para no
  añadir al documento de conocimiento texto que no está en el TUPA. Se
  vigila en la evaluación completa.
- No se cambiaron los documentos de conocimiento. El nivel de moderación no
  se puede ajustar: Copilot Studio indica que la moderación de contenido no
  está disponible para el idioma principal del agente (español) y no muestra
  selector de nivel. El valor `contentModeration: "Low"` de la solución
  exportada (tarea 6.4) no se aplica, y el nivel "Alta" previsto en D5 no es
  alcanzable. Las tres rondas se hicieron, por tanto, sin moderación
  configurable; el resultado de 0 alucinadas proviene de las instrucciones,
  de *Allow ungrounded responses* desactivado y de la búsqueda web
  desactivada (D5 actualizado).
