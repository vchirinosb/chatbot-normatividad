# Tarjetas de respuesta para la validación del protocolo

Generado por `scripts/generate_validation_cards.py` desde `docs/protocolo.yaml` y `data/processed/tupa.json`. No editar a mano: cambiar el YAML y volver a generar.

El facilitador lee (o pega en el chat simulado) la tarjeta que corresponde a lo que escribe el participante. Si el participante escribe algo no previsto, elegir la intención más cercana y anotarlo como hallazgo.

## Bienvenida (al iniciar)

> ¡Hola! Soy el asistente de normatividad estudiantil de la UCSM. Puedo explicarte el Reglamento de Estudiantes y los trámites del TUPA (requisitos, costos y plazos). No consulto notas, pagos ni datos personales.
>
> Soy un asistente académico de orientación. No reemplazo a las instancias oficiales de la UCSM; el texto vinculante es el del documento oficial.
>
> ¿Sobre qué tema quieres consultar?
>
> [Matrícula y convalidaciones]
> [Evaluación y notas]
> [Deberes, derechos y sanciones]
> [Becas y bienestar]
> [Grados, títulos y certificados]
> [Modalidades semipresencial y a distancia]
> [Trámites (requisitos, costos y plazos)]

## menu

Se usa ante: "ayuda", "¿qué puedes hacer?", "menú", "temas".

> Estos son los temas que puedo ayudarte a consultar:

## datos_personales

Se usa ante: "mi DNI es 45678912", "mi código es 2020123456".

> Por tu seguridad, no compartas datos personales como tu DNI, código de estudiante, notas o contraseñas. No los necesito para responder: puedo orientarte con la normativa general. ¿Cuál es tu consulta?

## fuera_de_alcance

Se usa ante: "¿Cuál es mi nota del curso?", "¿Cuándo es el examen de admisión?", "¿Qué dice el reglamento de docentes?".

> Esa consulta está fuera de mi alcance: solo respondo sobre el Reglamento de Estudiantes y el TUPA de la UCSM. Para otros temas, revisa https://ucsm.edu.pe/normatividad/ o comunícate con la oficina correspondiente.

## sin_evidencia

> No encontré esa información en el Reglamento de Estudiantes ni en el TUPA. Te sugiero consultar con tu Escuela Profesional o con Secretaría General, o revisar https://ucsm.edu.pe/normatividad/.

## contenido_inapropiado

> Prefiero mantener una conversación respetuosa. Si tienes una consulta sobre el Reglamento de Estudiantes o los trámites del TUPA, con gusto te ayudo.

## despedida

> ¡Gracias por consultar! Si tienes otra duda sobre el Reglamento o los trámites, vuelve cuando quieras.
>
> ¿Te fue útil esta conversación? [Sí] [No]

## Respuestas para las tareas del recorrido

### Tarea 1 – Desaprobar un curso tres veces (consulta normativa)

> Si desapruebas la misma asignatura por tres (3) veces, eres separado temporalmente por un año de la Universidad. Al volver, solo puedes matricularte en esa asignatura; si la desapruebas por cuarta vez, procede el retiro definitivo de la Escuela Profesional.
>
> Fuentes: Reglamento de Estudiantes, Art. 83° (pág. 24)
> Orientación no oficial; el texto vinculante es el documento oficial.

### Tarea 2 – Constancia de estudios (consulta de trámite)

> **CONSTANCIAS**
>
> - Código: SE1130737868
> - Costo: Constancia de Estudios - Matrícula actual, Egreso, Bachiller, Título, Orden de Mérito, Promedio Ponderado, Escala de Calificación, Reconocimiento Legal de la Universidad, Ranking, Equivalencia de Promedio Ponderado, Constancia especial de estudios no regulares, Actas de Grados y Títulos, Constancia Beca PRONABEC y otras: S/ 44.00; Plan de Estudios con carga horaria: S/ 71.50; Internado Rotatorio: S/ 71.50; Constancia de Ingreso, de Escuela de Postgrado, de oficina de Admisión o de Escuelas Profesionales, Conducta, constancia de Modalidad de Titulación: S/ 44.00
> - Plazo de atención: 7 días hábiles
> - Dónde se presenta: Portal web Trámites en Línea : Dirección de Registro y Archivo Académico
> - Contacto: Teléfono 054-382038, anexo 1451, correo constancias.draa@ucsm.edu.pe
> - Fuente: TUPA UCSM, pág. 88
>
> ¿Quieres que te detalle los requisitos de este trámite?

### Tarea 3 – Evaluación extemporánea (desambiguación)

Primero la pregunta de aclaración:

> El TUPA tiene un trámite distinto según tu escuela. ¿Para cuál es la evaluación extemporánea?
>
> [Escuela Profesional (pregrado)] [Escuela de Postgrado]

Si elige Escuela Profesional:

> **Autorización para rendir evaluaciones extemporáneas por motivo de enfermedad u otros dentro de los cinco (05) días siguientes a la omisión - Escuelas Profesionales**
>
> - Código: PA1130732571
> - Costo: Gratuito
> - Plazo de atención: 5 días hábiles
> - Dónde se presenta: Mesa de Partes Virtual : Escuelas Profesionales
> - Contacto: Teléfono 054-382038, anexo 6000, 6001 ó 6002
> - Fuente: TUPA UCSM, pág. 46

Si elige Escuela de Postgrado:

> **Autorización para rendir evaluaciones extemporáneas por motivo de enfermedad u otros dentro de los cinco (05) días siguientes a la fecha del examen - Escuela de Postgrado**
>
> - Código: PA1130731912
> - Costo: Gratuito
> - Plazo de atención: 3 días hábiles
> - Dónde se presenta: Mesa de Partes Virtual : Escuela de Postgrado
> - Contacto: Teléfono 054-382038, anexo 1181, 1167, correo caepg@ucsm.edu.pe
> - Fuente: TUPA UCSM, pág. 60

### Tarea 4 – Pregunta fuera de alcance

Usar la tarjeta `fuera_de_alcance` (o `sin_evidencia` si la pregunta es del dominio pero no está en los documentos).

### Tarea 5 – Despedida

Usar la tarjeta `despedida`.
