# Formulario SUS en Microsoft Forms

Guía para crear el cuestionario que cada participante responde al terminar
las tareas. Los textos deben copiarse tal cual: `eval/forms_to_sus.py` ubica
cada ítem por su texto (constante `SUS_ITEMS` en
`src/ucsm_bot/evaluation.py`).

## Configuración

- **Título:** Asistente de normatividad UCSM: cuestionario de usabilidad
- **Descripción:**

  > Gracias por probar el asistente. Este cuestionario es anónimo: no
  > escribas tu nombre, DNI, código de estudiante ni correo. Las respuestas
  > se usan solo para evaluar el asistente en un trabajo de maestría de la
  > UCSM. Toma unos 3 minutos.

- **Configuración → Quién puede responder:** *Cualquiera puede responder*
  (los participantes no necesitan iniciar sesión).
- **No** activar *Registrar nombre* ni *Una respuesta por persona* (exigen
  iniciar sesión y guardan el nombre).
- **Mezclar preguntas:** desactivado (el SUS se aplica en el orden original).

## Preguntas

1. **Identificador del participante** · *Texto*, obligatoria.
   Subtítulo: "Escribe el código que te dio el facilitador (P1, P2…)."
2. **Perfil** · *Elección*, obligatoria: Estudiante de pregrado ·
   Estudiante de postgrado · Docente · Otro.
3. **Dispositivo que usaste** · *Elección*, obligatoria: Celular ·
   Computadora.
4. **Cuestionario SUS** · *Likert*, obligatoria.
   - Opciones, en este orden: Totalmente en desacuerdo · En desacuerdo ·
     Ni de acuerdo ni en desacuerdo · De acuerdo · Totalmente de acuerdo.
   - Instrucciones (subtítulo): "Marca qué tan de acuerdo estás con cada
     afirmación sobre el asistente que acabas de usar."
   - Afirmaciones, en este orden:
     1. Creo que me gustaría usar este asistente con frecuencia.
     2. El asistente me pareció innecesariamente complicado.
     3. El asistente me resultó fácil de usar.
     4. Creo que necesitaría ayuda de una persona con conocimientos técnicos para usar este asistente.
     5. Las funciones del asistente me parecieron bien integradas.
     6. El asistente se comportaba de forma poco coherente (por ejemplo, respondía de manera distinta a preguntas parecidas).
     7. Imagino que la mayoría de las personas aprendería a usar este asistente muy rápidamente.
     8. El asistente me resultó muy difícil de usar.
     9. Me sentí con mucha confianza al usar el asistente.
     10. Necesité aprender muchas cosas antes de poder usar el asistente.
   - Adaptación al español: los ítems 2, 3, 5, 6 y 8 se reformularon
     (2026-11-25) para evitar los calcos del inglés ("Pensé que…",
     "Encontré…") y para explicar "inconsistencia" en el ítem 6 con un
     ejemplo. Cada ítem conserva su sentido y su polaridad (impares
     positivos, pares negativos), así que el puntaje se calcula igual.
5. **¿Qué fue lo más útil del asistente?** · *Texto largo*, opcional.
6. **¿Qué mejorarías?** · *Texto largo*, opcional.

Antes de compartirlo, responderlo una vez con el identificador `PRUEBA`,
revisar la exportación (ver abajo) y borrar esa respuesta en *Respuestas →
Eliminar todas las respuestas*.

## Exportar y calcular

1. *Ver respuestas → Abrir resultados en Excel → ⌄ → Descargar una copia*
   descarga un `.xlsx` en `~/Downloads`. No guardarlo en el repositorio:
   incluye la hora de cada respuesta.
2. Convertir y calcular (acepta el `.xlsx` directamente, o un CSV guardado
   desde Excel):

   ```bash
   .venv/bin/python eval/forms_to_sus.py ~/Downloads/<exportación>.xlsx
   .venv/bin/python eval/compute_sus.py
   ```

   El primer comando escribe `eval/sus.csv`; el segundo muestra el SUS por
   participante, el promedio (meta ≥ 68) y, si existe `eval/tareas.csv`, el
   éxito y el tiempo por tarea.
3. Copiar los comentarios de las preguntas 5 y 6 a
   `eval/usabilidad.md`, sin datos que identifiquen a nadie.

**Verificado el 2026-11-25:** una respuesta `PRUEBA` con el patrón
5,1,4,2,3,3,4,2,5,1 se exportó y `forms_to_sus.py` + `compute_sus.py`
dieron SUS 80,0, el valor esperado. La exportación trae las columnas
*Email* = "anonymous" y *Name* vacía (no se registran datos personales);
cada ítem del SUS es una columna con el texto de la afirmación. La
respuesta de prueba se borró después. Se repitió con el mismo resultado tras
ajustar la redacción de los ítems 2, 3, 5, 6 y 8.
