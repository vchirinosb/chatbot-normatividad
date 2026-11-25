# Analítica de Copilot Studio (tarea 7.5)

**Agente:** Normatividad Estudiantil UCSM (entorno de prueba).
**Fuente:** Copilot Studio → *Monitor* (resumen y *Conversation outcomes*)
y *Monitor → Sessions → Download Sessions* (CSV con una fila por sesión).
**Consultado:** 2026-11-25. **Rango:** últimos 30 días (2026-10-27 al
2026-11-25); todas las sesiones registradas caen entre el 2026-11-24 a las
20:12 y el 2026-11-25 a las 16:10 (hora de Perú, UTC−5). Las rondas 1 y 2
del banco no aparecen en la analítica.

El CSV no se guarda en el repositorio: incluye las transcripciones
completas y los identificadores de sesión. Las cifras de abajo se
calcularon sobre él.

## Resumen del periodo

| Métrica | Valor |
|---|---|
| Sesiones de conversación | 187 |
| Canal | Direct Line: 187 (incluye el *Demo website*) |
| Engagement (sesiones con al menos un mensaje del usuario) | 90 % (168) |
| Resultado: Resolved | 138 (82,1 % de las sesiones con engagement) |
| Resultado: Abandoned | 30 (17,9 %) |
| Resultado: Escalated | 0 |
| Sin engagement (solo la bienvenida) | 19 |
| Resolución confirmada por el usuario / implícita | 0 / 138 (100 % implícita) |
| CSAT | Sin datos: ninguna sesión tiene calificación |
| Sentimiento y reacciones (👍/👎) | Sin datos ("Not enough data") |
| Temas (*topics*) | Ninguno: el agente responde con IA generativa y Copilot Studio solo clasifica temas en el modo clásico |
| Preguntas generadas, calidad y uso de conocimiento | 0 (Copilot Studio exige ≥ 10 respuestas por día para medir la calidad y no lo reportó) |
| Copilot credits | 0 (entorno de prueba) |
| Duración media / mensajes por sesión | 00:27 / 4,4 |

"Abandoned" no significa una falla: Copilot Studio marca así las sesiones
que terminan sin una respuesta de conocimiento. En el banco, las 15
preguntas fuera de alcance quedaron como *Abandoned* porque el agente las
rechazó, que era lo esperado.

## Sesiones por fase

| Fase | Fecha y hora (UTC−5) | Sesiones | Resolved | Abandoned | Sin engagement | Turnos medios |
|---|---|---|---|---|---|---|
| Ronda 3 del banco y reintentos (`run_bank.py`) | 2026-11-24, 20:12–21:49 | 151 | 124 | 27 | 0 | 4,3 |
| Verificación de las 5 tareas de usabilidad | 2026-11-24, 22:17–22:19 | 5 | 3 | 2 | 0 | 4,2 |
| Prueba de usabilidad (9 participantes) | 2026-11-25, 06:56–16:10 | 31 | 11 | 1 | 19 | 10,1 |
| **Total** | | **187** | **138** | **30** | **19** | |

Las fases se separaron por la hora de inicio; el banco se reconoce además
porque su primer mensaje coincide con `eval/questions.yaml`.

## Temas más consultados

Como no hay *topics*, los temas se tomaron del primer mensaje de cada
sesión.

**Banco (151 sesiones):**

| Categoría | Sesiones | Resolved | Abandoned |
|---|---|---|---|
| Reglamento | 54 | 54 | 0 |
| TUPA | 39 | 39 | 0 |
| Reintentos y variantes de redacción | 25 | 22 | 3 |
| Fuera de alcance | 15 | 0 | 15 |
| Sin respuesta en los documentos | 12 | 3 | 9 |
| Combinada (Reglamento + TUPA) | 6 | 6 | 0 |

**Prueba de usabilidad (12 sesiones con engagement):** 7 sesiones
contienen las 5 tareas en una misma conversación (9 a 19 turnos); las
otras 5 son sesiones cortas de 4 a 6 turnos con una sola pregunta (T1, un
saludo o T5: "vendes Bembos?", rechazada). El primer mensaje es la tarea
T1 en 10 de las 12. En las 7 sesiones completas:

- T2: en 4 de 7 el agente mostró la ficha *Copia autenticada del Acta de
  Grados Académicos y Títulos Profesionales* (S/ 55.00, 5 días hábiles) en
  lugar de *Copia autenticada de Resolución que aprueba el Grado Académico
  o Título Profesional* (S/ 44.00, 7 días hábiles). Las 4 veces el
  participante escribió "copia autenticada de mi título" sin la palabra
  "resolución"; las 3 veces que la escribió, el agente acertó.
- T3: el código PA1130732571 aparece solo en 3 de 7.
- T4: el Art. 28° aparece en las 7.

Las 19 sesiones sin engagement son aperturas del link (o recargas) en las
que no se escribió nada; por eso hay más sesiones que participantes.

## Conclusiones

- El agente atendió 187 sesiones sin escalamientos ni errores de sistema;
  el 82 % de las sesiones con engagement terminó resuelta, y casi todas
  las *Abandoned* son rechazos correctos fuera de alcance.
- Copilot Studio no entrega CSAT, sentimiento, temas ni calidad de
  respuestas para este agente: no se activó la encuesta de satisfacción,
  el agente es generativo (sin *topics*) y el volumen diario no alcanza el
  mínimo para medir la calidad. Esas dimensiones se cubren con la rúbrica
  (tarea 7.3) y el SUS (tarea 7.4).
- La analítica confirma el principal error de la prueba de usabilidad:
  la ambigüedad entre las fichas de copia autenticada (ver
  `eval/usabilidad.md`).
