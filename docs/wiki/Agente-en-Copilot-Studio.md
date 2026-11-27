# Agente en Copilot Studio

El agente *Normatividad Estudiantil UCSM* es un agente estándar (basado en
Topics) en español, con orquestación generativa.

## Configuración

| Opción | Valor |
|---|---|
| Idioma | Español |
| Orquestación generativa | Activada |
| Use general knowledge | Desactivado |
| Búsqueda web | Desactivada |
| Allow ungrounded responses | Desactivado |
| Conocimiento | `reglamento_estudiantes.docx` y `tupa_fichas.docx` |
| Moderación de contenido | No configurable para agentes en español |
| Autenticación | *No authentication* |
| Canal | *Demo website* |

Las instrucciones están en `copilot/instructions.md`, listas para pegar en
*Overview → Instructions*. Piden responder solo con los documentos de
conocimiento, citar el artículo o el código con su página, copiar montos y
plazos tal como están en la ficha, hacer una sola pregunta de aclaración y
no pedir datos personales.

## Conocimiento

`python -m ucsm_bot.build` genera los archivos de `copilot/knowledge/`:

- `reglamento_estudiantes.docx`: un encabezado por artículo con su página;
  cada párrafo empieza con el número de artículo.
- `tupa_fichas.docx`: una sección por ficha con su código y sus campos.
- `tupa_fichas.csv`: los campos de las 63 fichas en una tabla.

## Topics

Los Topics se generan en `copilot/topics/` y se pegan en *Topic → Open code
editor*:

| Archivo | Topic |
|---|---|
| `sistema_inicio_conversacion.yaml` | Bienvenida con aviso y menú |
| `menu_temas.yaml` | Menú de temas |
| `consulta_tramite.yaml` | Consulta de trámite con Adaptive Card y desambiguación de fichas |
| `evaluacion_extemporanea.yaml` | Pregunta la escuela y muestra la ficha |
| `datos_personales.yaml` | Advertencia de privacidad |
| `cierre_conversacion.yaml` | Despedida y encuesta |
| `sistema_alternativa.yaml` | Mensaje cuando no se reconoce la consulta |
| `sistema_fin_conversacion.yaml` | Fin de la conversación con la encuesta de satisfacción |
| `entity_procedimientos.yaml`, `tabla_tupa.powerfx` | Entidad de procedimientos y tabla del TUPA que usa la tarjeta |

![Lienzo del Topic de trámite](images/agente_lienzo_topic_tramite.jpg)

La búsqueda de *Consulta de trámite* compara la consulta con la
denominación de cada ficha sin tildes ni guiones y por los primeros cinco
caracteres de cada palabra. Desempata por palabras completas y por la
denominación más corta; si aún empatan fichas parecidas, pregunta cuál.

![Tarjeta de un trámite del TUPA](images/agente_tarjeta_tupa.jpg)

## Publicación

- El agente se publicó en un entorno de prueba de Copilot Studio con
  *No authentication*, porque el entorno predeterminado no tenía capacidad
  de mensajes para los canales publicados.
- El link del *Demo website* abre el chat sin iniciar sesión, también en
  celular. El link no se guarda en el repositorio porque contiene
  identificadores del inquilino.

![Agente en un celular](images/agente_demo_movil.jpg)

![Pregunta fuera de alcance](images/agente_fuera_alcance.jpg)

## Versiones

La solución no administrada se exporta en `copilot/solution/`. La versión
vigente es la **1.0.0.4**:

| Versión | Cambio principal |
|---|---|
| 1.0.0.1 | Primera publicación |
| 1.0.0.2 | Búsqueda de trámites sin tildes y por raíz de palabra |
| 1.0.0.3 | Cada párrafo del Reglamento empieza con su artículo |
| 1.0.0.4 | Desambiguación de fichas con nombre parecido |

Para restaurar el agente en otro entorno, importar el `.zip` desde
*Solutions → Import* y publicar.
