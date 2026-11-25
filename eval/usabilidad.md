# Resultados de la prueba de usabilidad (tarea 7.4)

**Estado:** realizada el 2026-11-25 con 9 participantes (procedimiento en
`tareas_usabilidad.md`). Datos: `eval/sus.csv` (exportación del formulario
convertida con `forms_to_sus.py`) y `eval/tareas.csv` (notas del
facilitador). La exportación `.xlsx` no se guarda en el repositorio.

## Datos de la prueba

| Dato | Valor |
|---|---|
| Fecha | 2026-11-25 |
| Participantes | 9 (P01–P09) |
| Perfil | 7 personal administrativo de la UCSM (marcaron "Otro" en el formulario), 2 estudiantes de pregrado |
| Dispositivo | 4 celular, 5 computadora |
| Canal | Agente publicado (*Demo website*), sin iniciar sesión |
| Tiempo por tarea | No se cronometró: `seconds` queda vacío en `tareas.csv` |

## SUS

Salida de `.venv/bin/python eval/compute_sus.py`:

| Participante | SUS |
|---|---|
| P01 | 85,0 |
| P02 | 87,5 |
| P03 | 82,5 |
| P04 | 82,5 |
| P05 | 85,0 |
| P06 | 95,0 |
| P07 | 80,0 |
| P08 | 82,5 |
| P09 | 92,5 |
| **Promedio** | **85,8** (meta ≥ 68: cumple) |

Mediana 85,0; desviación estándar 5,0; mínimo 80,0; máximo 95,0. Todos
los participantes superan la meta.

Dos participantes respondieron de forma contradictoria a ítems de
polaridad opuesta: P03 marcó "Totalmente de acuerdo" en el ítem 3 (fácil
de usar) y en el 8 (muy difícil de usar); P07 hizo lo mismo y además
marcó "Totalmente de acuerdo" en el ítem 2 (innecesariamente complicado).
Es el error típico de leer los ítems negativos como positivos. Sin ellos,
el promedio es 87,1 (n = 7), así que la conclusión no cambia.

## Tareas

Criterios de éxito de `tareas_usabilidad.md`, aplicados de forma estricta:

| Tarea | Éxito | Tiempo medio | Observación |
|---|---|---|---|
| T1. Desaprobar un curso tres veces | 9/9 (100 %) | — | Separación por un año (Art. 83°) |
| T2. Costo y plazo de la copia autenticada de la resolución del título | 4/9 (44 %) | — | 5 recibieron S/ 55.00 y 5 días hábiles (ficha equivocada) |
| T3. Examen perdido por enfermedad (pregrado) | 5/9 (56 %) | — | Los 9 recibieron el plazo de 5 días; 4 no recibieron el código PA1130732571 (parcial) |
| T4. Reserva de matrícula | 9/9 (100 %) | — | Hasta cinco semestres (Art. 28°) |
| T5. Pregunta fuera de alcance | 9/9 (100 %) | — | El agente rechazó o derivó sin inventar |

Contando T3 como éxito cuando el plazo es correcto (sin el código), T3
sube a 9/9.

### Errores del agente

- **T2, ficha equivocada (5 de 9):** el agente respondió con *Copia
  autenticada del Acta de Grados Académicos y Títulos Profesionales*
  (PA113073BCE9: S/ 55.00, 5 días hábiles) en lugar de *Copia autenticada
  de Resolución que aprueba el Grado Académico o Título Profesional*
  (PA113073E0FC: S/ 44.00, 7 días hábiles). En las transcripciones de
  Copilot Studio (`eval/analitica.md`) pasó cada vez que el participante
  escribió "copia autenticada de mi título" sin la palabra "resolución";
  cuando la escribió, acertó. P08 detectó la confusión por su cuenta. No
  es una alucinación (los montos existen en el TUPA), pero la pregunta es
  ambigua y el agente eligió sin preguntar.
- **T3, sin código de trámite (4 de 9):** el agente explicó el plazo y el
  procedimiento, pero no mostró la ficha PA1130732571. Los que sí la
  recibieron eligieron "Escuela Profesional (pregrado)" cuando el agente
  preguntó la unidad, como se anticipó en la guía.

## Observaciones y comentarios

- **Lo más útil** (pregunta 5 del formulario): la rapidez y precisión de
  las respuestas, que sean breves ("sin llenarme de texto"), que indique
  los pasos del trámite, que cite la norma y su resolución, y que mantenga
  el hilo de la conversación.
- **Qué mejorarían** (pregunta 6):
  - que pregunte cuando un trámite es ambiguo o muestre trámites
    parecidos (P08, a raíz de T2);
  - que oriente cuando no puede responder;
  - más normativa en su base de conocimiento ("mayor alcance de datos");
  - más sugerencias que complementen la respuesta;
  - interfaz más llamativa;
  - fallas de la interfaz del *Demo website*: se "cuelga" al borrar todo
    el texto del campo de mensaje (P01) y a veces no deja ver lo escrito
    líneas arriba (P09);
  - un participante: "nada que mejorar por ahora".
- **Observado por el facilitador** (columna `comments` de `tareas.csv`):
  el agente pide la unidad en T3 aunque el participante ya dijo
  "pregrado"; los participantes eligen la opción sin dificultad.

## Cambios derivados

| Prioridad | Cambio |
|---|---|
| Alta | Desambiguar las fichas de copia autenticada (resolución del grado o título, acta de grados, otras resoluciones): cuando la consulta no dice cuál, preguntar o mostrar las opciones con su costo, en lugar de elegir una. **Aplicado el 2026-11-25** (versión 1.0.0.4): el agente lista las fichas empatadas y pregunta cuál; verificado por Direct Line y sin regresiones en la ronda 4 del banco (`evaluacion_completa.md`). No se repitió la prueba con participantes. |
| Media | En T3, mostrar siempre la ficha del trámite (código PA1130732571) después de explicar el plazo, también cuando el participante ya indicó "pregrado". |
| Media | Cuando la pregunta esté fuera de alcance o sin respuesta, indicar a qué oficina acudir (reforzarlo en las instrucciones del agente). |
| Baja | Las fallas de la interfaz son del *Demo website* de Copilot Studio y no se pueden corregir en el agente; documentarlas como limitación. |
