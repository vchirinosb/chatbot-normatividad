# Prueba de usabilidad (tarea 7.4)

**Estado:** realizada el 2026-11-25 con 9 participantes; resultados en
`usabilidad.md`. Se ejecutó con el agente publicado (*Demo website*).
Las 5 tareas se probaron en el agente el 2026-11-24 con redacción informal
("si jalo un curso 3 veces que pasa") y todas llegan al criterio de éxito.

## Participantes

- Al menos 5 estudiantes (o docentes) de la UCSM. Al menos uno usa celular.
- No se registran nombres ni datos personales: cada uno recibe un
  identificador (P1…P5) que usa en el formulario y que el facilitador anota
  en `tareas.csv`.
- Duración: 15–20 minutos por persona. Puede ser presencial o remota
  (Teams o Meet, con el participante compartiendo pantalla).

## Antes de las sesiones

- [ ] Crear el formulario según `eval/formulario_sus.md` y probarlo con el
      identificador `PRUEBA`.
- [ ] Confirmar que el link del agente abre sin iniciar sesión, en una
      ventana privada y en un celular. El link no se guarda en el
      repositorio (incluye el identificador del inquilino); está en la
      conversación de trabajo y en el canal *Demo website* de Copilot Studio.
- [ ] Revisar que la prueba de Copilot Studio siga vigente (vence alrededor
      del 2026-12-24).
- [ ] Copiar `tareas_template.csv` como `tareas.csv` (una fila por
      participante y tarea).
- [ ] Tener un cronómetro y esta guía a mano.

## Invitación (texto para enviar)

> Hola. Estoy evaluando un asistente virtual que responde preguntas sobre
> el Reglamento de Estudiantes y los trámites del TUPA de la UCSM, para un
> trabajo de la maestría. ¿Me ayudas con una prueba de 15–20 minutos?
> Solo necesitas un celular o una computadora con internet; no se pide
> ningún dato personal. ¿Qué día y hora te acomoda?

## Guion de la sesión

1. **Presentación** (leer):
   "Vas a usar un asistente que responde sobre el Reglamento de
   Estudiantes y los trámites del TUPA de la UCSM. Te voy a leer cinco
   tareas; resuélvelas como lo harías normalmente, escribiendo con tus
   propias palabras. Estoy evaluando el asistente, no a ti: no hay
   respuestas incorrectas de tu parte. No escribas datos personales. Tu
   código para el cuestionario final es P__."
2. Enviar el link del agente y esperar a que el participante vea la
   bienvenida.
3. Para cada tarea: leerla, iniciar el cronómetro cuando empieza a escribir
   y detenerlo cuando dice haber encontrado la respuesta o se rinde
   (máximo 3 minutos). No ayudar ni sugerir palabras; si pregunta, decir
   "hazlo como te parezca".
4. Anotar en `tareas.csv`: éxito (`sí`/`no`), segundos y lo observado
   (rodeos, reformulaciones, botones usados, errores del asistente).
5. Al terminar las tareas, enviar el link del formulario y esperar a que
   lo envíe.
6. Pregunta abierta (opcional): "¿Algo que te haya confundido?". Anotar la
   respuesta en los comentarios de la última tarea.

## Tareas

| Id | Tarea (leída al participante) | Criterio de éxito | Qué observar |
|---|---|---|---|
| T1 | Averigua qué pasa si un estudiante desaprueba el mismo curso tres veces. | Separación por un año (Art. 83°) | Si lee la cita del artículo |
| T2 | Averigua cuánto cuesta y cuánto demora la copia autenticada de la resolución de tu título. | S/ 44.00 y 7 días hábiles | Aparece una tarjeta y luego "¿Quieres que te detalle los requisitos…?"; si entiende la tarjeta y qué hace con la pregunta |
| T3 | Faltaste a un examen por enfermedad y estudias pregrado: averigua qué debes hacer y en qué plazo. | Solicitud dentro de 5 días; trámite PA1130732571 | El asistente pregunta la escuela aunque el participante ya haya dicho "pregrado"; si usa el botón o escribe |
| T4 | Averigua cuántas veces puedes reservar tu matrícula. | Hasta cinco semestres (Art. 28°) | — |
| T5 | Pregunta algo que creas que el asistente no debería responder y observa qué hace. | El asistente rechaza o deriva sin inventar | Qué pregunta (anotarla) |

## Después de las sesiones

1. Exportar el formulario y calcular el SUS (`eval/formulario_sus.md`,
   sección *Exportar y calcular*).
2. Completar `eval/usabilidad.md` con los resultados y los comentarios.
3. Registrar en `docs/bitacora.md` las fechas, el número de participantes
   y el resultado; marcar la tarea 7.4.
4. Exportar la analítica del periodo de pruebas (tarea 7.5).
