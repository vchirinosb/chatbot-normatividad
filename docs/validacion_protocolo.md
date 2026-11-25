# Validación del protocolo con usuarios

**Estado: descartada (2026-11-24, decisión del autor).** La tarea 3.4 se
quitó del plan: el agente ya estaba construido, y el protocolo se validó
sobre él con el guion de verificación, las iteraciones de instrucciones
(`eval/iteraciones.md`) y tres rondas del banco de preguntas
(`eval/evaluacion_completa.md`). La opinión de usuarios se recoge en la
prueba de usabilidad (tarea 7.4). Se conserva el método como referencia.

## Método

- **Tipo:** recorrido guiado (*Wizard of Oz*): el evaluador lee el
  protocolo (`protocolo.yaml` y el diagrama) y responde como lo haría el
  chatbot; el participante consulta con sus propias palabras.
- **Duración:** 15–20 minutos por participante.
- **Tareas:**
  1. Averiguar qué pasa si desaprueba un curso tres veces.
  2. Averiguar cuánto cuesta y cuánto demora una constancia de estudios.
  3. Pedir una evaluación extemporánea (debe aparecer la pregunta de
     escuela).
  4. Hacer una pregunta que el chatbot no debería responder.
  5. Despedirse.
- **Preguntas al final** (escala 1–5 y comentario):
  - ¿La bienvenida deja claro qué puede y qué no puede hacer el chatbot?
  - ¿Las opciones del menú corresponden a lo que consultarías?
  - ¿La pregunta de aclaración fue útil o molesta?
  - ¿El formato de respuesta (breve, con fuente) es fácil de leer?
- **Consentimiento:** no se registran nombres ni datos personales; solo
  carrera y semestre.

## Materiales

- [`validacion_tarjetas.md`](validacion_tarjetas.md): respuestas que el
  facilitador da como chatbot, generadas desde `protocolo.yaml` y
  `tupa.json` (`.venv/bin/python scripts/generate_validation_cards.py`).
- [`figuras/protocolo_flujo.png`](figuras/protocolo_flujo.png): diagrama
  del flujo, para que el facilitador ubique cada intención.
- Una hoja de observación por participante (sección siguiente).

## Guion de la sesión

1. **Preparación (antes de la sesión):** abrir un chat simulado donde el
   facilitador pueda escribir como "Asistente" (por ejemplo un documento
   compartido, un chat de Teams entre dos cuentas o papel), con las
   tarjetas a la mano. Cronómetro listo.
2. **Introducción (1 min), leer en voz alta:** "Vas a probar el diseño de un
   asistente que responde sobre el Reglamento de Estudiantes y los trámites
   del TUPA. Yo haré de asistente siguiendo un guion. Evaluamos el diseño,
   no a ti. Piensa en voz alta: di lo que esperas y lo que te confunde. No
   compartas datos personales."
3. **Bienvenida:** mostrar la tarjeta de bienvenida y preguntar: "¿Qué crees
   que puede hacer este asistente y qué no?".
4. **Tareas 1–5:** leer cada tarea sin sugerir palabras. Responder solo con
   la tarjeta que corresponde. Anotar las palabras exactas del
   participante, dudas, y si llegó a la información.
5. **Preguntas finales:** las cuatro preguntas de escala 1–5 y un
   comentario libre: "¿Qué cambiarías?".
6. **Cierre:** agradecer; completar la hoja de observación de inmediato.

## Puntos a observar (riesgos ya identificados)

- **Costo con varios conceptos:** la tarjeta de "CONSTANCIAS" muestra un
  costo muy largo en un solo campo. Observar si el participante encuentra
  su monto; si no, proponer una tarjeta con un concepto por línea.
- **Menú de 7 temas:** ver si el participante lo usa o escribe directamente.
- **Pregunta de aclaración (tarea 3):** ver si entiende la diferencia entre
  Escuela Profesional y Escuela de Postgrado.
- **Fuera de alcance (tarea 4):** ver si el mensaje de derivación le parece
  útil o un callejón sin salida.

## Hoja de observación (copiar una por participante)

| Campo | Registro |
|---|---|
| ID / carrera / semestre | |
| Fecha / duración | |
| Expectativa tras la bienvenida | |

| Tarea | Lo que escribió | Tarjeta usada | ¿Llegó a la información? (sí/no/parcial) | Tiempo | Dudas o comentarios |
|---|---|---|---|---|---|
| T1 | | | | | |
| T2 | | | | | |
| T3 | | | | | |
| T4 | | | | | |
| T5 | | | | | |

| Pregunta final | 1–5 | Comentario |
|---|---|---|
| La bienvenida deja claro el alcance | | |
| Las opciones del menú son las que consultaría | | |
| La pregunta de aclaración fue útil | | |
| El formato de respuesta es fácil de leer | | |
| ¿Qué cambiarías? | — | |

## Participantes

| ID | Carrera | Semestre | Fecha | Duración |
|---|---|---|---|---|
| P1 | | | | |
| P2 | | | | |
| P3 | | | | |

## Hallazgos

| ID | Tarea | Hallazgo | Severidad (alta/media/baja) |
|---|---|---|---|
| | | | |

## Ajustes aplicados al protocolo

| Hallazgo | Cambio en `protocolo.yaml` / diagrama | Versión |
|---|---|---|
| | | |
