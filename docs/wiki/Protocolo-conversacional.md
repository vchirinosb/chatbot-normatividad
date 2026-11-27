# Protocolo conversacional

Los textos fijos (bienvenida, menú, avisos, preguntas de aclaración,
despedida) están en `docs/protocolo.yaml`, que es la fuente única. Los
Topics de Copilot Studio se generan a partir de ese archivo.

## Principios

- **Claro y breve:** hasta ~150 palabras, en español formal y sencillo, con
  pasos numerados cuando hay requisitos o condiciones.
- **Siempre con fuente:** cada respuesta normativa termina con "Fuentes:" y
  el artículo o el código del procedimiento, con su página.
- **Una sola pregunta de aclaración:** si la respuesta depende del nivel, la
  modalidad o el trámite, se pregunta una vez con opciones concretas.
- **Sin datos personales:** el asistente no pide ni procesa DNI, código,
  notas ni contraseñas.
- **No oficial:** el aviso aparece en la bienvenida, en la descripción del
  agente y al final de las respuestas normativas.

## Flujo

![Diagrama de flujo del protocolo](images/protocolo_flujo.png)

## Intenciones

| Intención | Cómo se atiende | Ejemplo | Respuesta |
|---|---|---|---|
| Saludo | Topic de inicio (sistema) | "hola" | Bienvenida, aviso de alcance y menú |
| Ayuda / menú | *Menú de temas* | "¿qué puedes hacer?" | Menú de 7 temas con respuestas rápidas |
| Consulta normativa | Respuesta generativa sobre el Reglamento | "¿Qué pasa si desapruebo un curso tres veces?" | Respuesta breve con cita (Art. 83°, pág. 24) |
| Consulta de trámite | *Consulta de trámite* | "¿Cuánto cuesta la anulación de matrícula?" | Adaptive Card con costo, plazo, dónde y contacto, y oferta de requisitos |
| Consulta combinada | Respuesta generativa (ambos documentos) | "Falté a un examen por enfermedad, ¿qué hago?" | Regla del Reglamento y trámite del TUPA |
| Trámite con variantes | *Evaluación extemporánea* | "¿Cómo pido una evaluación extemporánea?" | Pregunta Escuela Profesional o Escuela de Postgrado |
| Nivel o modalidad | Instrucciones del agente | "¿Cuántos créditos puedo llevar?" | Pregunta pregrado/postgrado o modalidad |
| Datos personales | *Datos personales* | "mi DNI es …" | Advierte que no hace falta y retoma la consulta |
| Fuera de alcance | Topic alternativo (sistema) e instrucciones | "¿Cuál es mi nota?" | Explica el alcance y deriva al sitio de normatividad |
| Sin evidencia | Respuesta generativa sin resultados | Pregunta del dominio sin respuesta en el corpus | "No encontré…" y derivación |
| Despedida | *Cierre de la conversación* | "gracias, eso es todo" | Despedida y encuesta "¿Te fue útil?" |

## Desambiguación

1. **Trámite con variantes:** el TUPA tiene trámites casi iguales por
   escuela; el Topic pregunta la escuela y muestra la ficha que
   corresponde.
2. **Nivel y modalidad:** las instrucciones piden una sola pregunta de
   aclaración cuando la regla cambia según el nivel o la modalidad.
3. **Trámite no reconocido:** el Topic pide el nombre del trámite con un
   ejemplo.
4. **Varias fichas igual de probables:** si la búsqueda empata entre fichas
   de nombre parecido (por ejemplo "copia autenticada de mi título"), el
   agente lista hasta cuatro con código, costo y plazo, y pregunta cuál. El
   usuario responde con el número, el código o el nombre.

![Desambiguación de fichas](images/agente_desambiguacion.jpg)

## Formato de respuesta

```
<respuesta directa en 1–2 frases>

1. <paso o requisito>
2. <paso o requisito>

Fuentes: Reglamento de Estudiantes, Art. 83° (pág. 24)
Orientación no oficial; el texto vinculante es el documento oficial.
```

![Respuesta con cita](images/agente_respuesta_cita.jpg)

## Verificación

`docs/guion_verificacion.md` recorre todas las intenciones en 19 pasos con
el texto literal esperado. En el panel de prueba de Copilot Studio el
resultado final fue 18/19: queda una diferencia menor (el agente da la
regla general antes de preguntar el nivel).
