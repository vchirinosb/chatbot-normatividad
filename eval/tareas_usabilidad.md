# Prueba de usabilidad (tarea 7.4)

**Estado:** preparada; se ejecuta con el agente publicado (*Demo website*).

## Participantes

Al menos 5 estudiantes (o docentes) de la UCSM que no hayan participado en
la validación del protocolo. No se registran nombres ni datos personales:
solo un identificador (P1…P5), carrera y semestre.

## Procedimiento

1. Leer al participante: "Vas a usar un asistente que responde sobre el
   Reglamento de Estudiantes y los trámites del TUPA. Realiza cada tarea
   como lo harías normalmente; no hay respuestas incorrectas de tu parte."
2. Abrir el link del agente en el dispositivo del participante (al menos
   uno en celular).
3. Leer cada tarea, medir el tiempo desde que empieza a escribir hasta que
   dice haber encontrado la respuesta (máximo 3 minutos por tarea).
4. Marcar éxito si la información obtenida coincide con el criterio.
5. Al final, aplicar el cuestionario SUS en Microsoft Forms (10 ítems,
   escala 1–5) y pedir comentarios abiertos.

## Tareas

| Id | Tarea (leída al participante) | Criterio de éxito |
|---|---|---|
| T1 | Averigua qué pasa si un estudiante desaprueba el mismo curso tres veces. | Separación por un año (Art. 83°) |
| T2 | Averigua cuánto cuesta y cuánto demora la copia autenticada de la resolución de tu título. | S/ 44.00 y 7 días hábiles |
| T3 | Faltaste a un examen por enfermedad y estudias pregrado: averigua qué debes hacer y en qué plazo. | Solicitud dentro de 5 días hábiles; trámite PA1130732571 |
| T4 | Averigua cuántas veces puedes reservar tu matrícula. | Hasta cinco semestres (Art. 28°) |
| T5 | Pregunta algo que creas que el asistente no debería responder y observa qué hace. | El asistente rechaza o deriva sin inventar |

## Cuestionario SUS (Microsoft Forms)

Escala: 1 = Totalmente en desacuerdo … 5 = Totalmente de acuerdo.

1. Creo que me gustaría usar este asistente con frecuencia.
2. Encontré el asistente innecesariamente complejo.
3. Pensé que el asistente era fácil de usar.
4. Creo que necesitaría ayuda de una persona con conocimientos técnicos
   para usar este asistente.
5. Encontré que las funciones del asistente estaban bien integradas.
6. Pensé que había demasiada inconsistencia en el asistente.
7. Imagino que la mayoría de las personas aprendería a usar este asistente
   muy rápidamente.
8. Encontré el asistente muy difícil de usar.
9. Me sentí muy confiado al usar el asistente.
10. Necesité aprender muchas cosas antes de poder usar el asistente.

## Registro y cálculo

- Copiar `sus_template.csv` como `sus.csv` y `tareas_template.csv` como
  `tareas.csv`; llenar con las respuestas (éxito: `sí`/`no`; tiempo en
  segundos).
- Ejecutar `.venv/bin/python eval/compute_sus.py`: muestra el SUS por
  participante, el promedio (meta ≥ 68), la tasa de éxito y el tiempo medio
  por tarea.
- Registrar los comentarios cualitativos y los resultados en el paper.
