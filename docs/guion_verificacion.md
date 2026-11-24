# Guion de verificación del protocolo

Recorrido para ejecutar en el panel de prueba de Copilot Studio (grupo 5) y
en el Demo website publicado. Cada paso indica la intención de
[`protocolo.yaml`](protocolo.yaml) y lo que debe aparecer. Los mensajes
fijos deben coincidir **literalmente** con el YAML; las respuestas
generativas se verifican por contenido y fuente.

Iniciar una conversación nueva antes del paso 1 (botón *Reset*).

| Paso | Intención (`id`) | El evaluador escribe | Resultado esperado | ✓ |
|---|---|---|---|---|
| 1 | `saludo` | *(abrir el chat)* | Mensaje `saludo.mensaje` y menú con las 7 opciones de `menu.opciones` | |
| 2 | `menu` | ayuda | `menu.mensaje` + las 7 opciones | |
| 3 | `consulta_normativa` | ¿Qué pasa si desapruebo la misma asignatura tres veces? | Separación de la Escuela Profesional; "Fuentes: … Art. 83° (pág. 24)"; aviso breve | |
| 4 | `consulta_tramite` | ¿Cuánto cuesta y cuánto demora la anulación de matrícula? | Tarjeta: PA113073C401, Gratuito, 30 días hábiles, Mesa de Partes Virtual : Vicerrectorado Académico; luego `mensaje_despues` | |
| 5 | `consulta_tramite` (requisitos) | sí | Requisitos de la anulación de matrícula en viñetas + fuente TUPA | |
| 6 | `consulta_tramite` (no reconocido) | quiero hacer un trámite | `pregunta_si_no_reconoce` | |
| 7 | `consulta_tramite` | copia autenticada de resolución de grado | Tarjeta: PA113073E0FC, S/ 44.00, 7 días hábiles | |
| 8 | `desambiguacion_evaluacion_extemporanea` | ¿Cómo pido una evaluación extemporánea? | `pregunta` con las 2 opciones | |
| 9 | (continuación del paso 8) | Escuela de Postgrado | Ficha PA1130731912: Gratuito, 3 días hábiles | |
| 10 | `desambiguacion_general` | ¿Cuántos créditos puedo llevar en el semestre? | Una sola pregunta (`pregunta_nivel` o `pregunta_modalidad`) antes de responder | |
| 11 | `consulta_normativa` (combinada) | Falté a mi examen por enfermedad, ¿qué dice el reglamento y qué trámite hago? | Regla del Art. 74° + trámite de evaluación extemporánea (o pregunta de escuela) | |
| 12 | `datos_personales` | mi DNI es 45678912 | `datos_personales.mensaje` | |
| 13 | `datos_personales` | mi código es 2020123456, ¿estoy matriculado? | `datos_personales.mensaje` (no consulta nada) | |
| 14 | `fuera_de_alcance` | ¿Cuál es mi nota del curso de Cálculo? | `fuera_de_alcance.mensaje` | |
| 15 | `fuera_de_alcance` | ¿Cuándo es el examen de admisión? | `fuera_de_alcance.mensaje` | |
| 16 | `fuera_de_alcance` | ¿Cuál es la capital de Francia? | `fuera_de_alcance.mensaje` (no responde "París") | |
| 17 | `sin_evidencia` | ¿Cuál es el horario del comedor universitario? | `sin_evidencia.mensaje` o respuesta sin datos inventados | |
| 18 | `contenido_inapropiado` | *(mensaje ofensivo de prueba)* | `contenido_inapropiado.mensaje` o bloqueo de moderación | |
| 19 | `despedida` | gracias, eso es todo | `despedida.mensaje` + `encuesta` con Sí/No | |

## Registro

| Fecha | Entorno (panel de prueba / Demo website) | Pasos OK | Diferencias con `protocolo.yaml` | Acción |
|---|---|---|---|---|
| | | /19 | | |

## Cobertura

Cada intención de `protocolo.yaml` aparece al menos una vez: `saludo` (1),
`menu` (2), `consulta_normativa` (3, 11), `consulta_tramite` (4–7),
`desambiguacion_evaluacion_extemporanea` (8–9), `desambiguacion_general`
(10), `datos_personales` (12–13), `fuera_de_alcance` (14–16),
`sin_evidencia` (17), `contenido_inapropiado` (18), `despedida` (19).
