# Glosario

Términos usados en esta wiki y en el repositorio, en orden alfabético.

| Término | Definición |
|---|---|
| **Adaptive Card** | Tarjeta con formato fijo que Copilot Studio muestra en el chat. El agente la usa para presentar la ficha de un trámite: denominación, código, costo, plazo, dónde se presenta, contacto y páginas del TUPA. Ver [Agente en Copilot Studio](Agente-en-Copilot-Studio). |
| **Agente** | El chatbot construido en Copilot Studio, llamado *Normatividad Estudiantil UCSM*. |
| **Alucinación** | Respuesta que inventa un artículo, código, monto, requisito u oficina, o que cita una fuente que no contiene lo afirmado. Es la peor calificación de la rúbrica; la meta es 0. |
| **Analítica** | Estadísticas de uso que registra Copilot Studio (*Monitor*): sesiones, resultados, CSAT y temas. Ver [Evaluación](Evaluacion). |
| **Banco de preguntas** | Las 44 preguntas de referencia de `eval/questions.yaml`, con su respuesta esperada, que se usan para medir el agente. |
| **Build** | El comando `python -m ucsm_bot.build`, que genera el corpus procesado, los documentos de conocimiento y los Topics. Es determinista: dos ejecuciones producen archivos idénticos. |
| **Calificación (TUPA)** | Tipo de evaluación que la UCSM aplica a un procedimiento, por ejemplo *Evaluación previa*. Es un campo de cada ficha. |
| **Código de procedimiento** | Identificador de una ficha del TUPA, por ejemplo `PA113073C401` (procedimiento) o `SE11307302CD` (servicio). El agente lo cita como fuente. |
| **Conocimiento (*Knowledge*)** | Documentos que Copilot Studio usa para las respuestas generativas. En este agente son `reglamento_estudiantes.docx` y `tupa_fichas.docx`. |
| **Consulta combinada** | Pregunta que necesita los dos documentos: la regla del Reglamento y el trámite del TUPA. |
| **Control de cambios** | Cuadro final del Reglamento con el historial de modificaciones por versión. Se indexa como unidad propia. |
| **Copilot Studio** | Plataforma *low-code* de Microsoft para crear agentes conversacionales con Topics, respuestas generativas y publicación en canales. |
| **Corpus** | Conjunto cerrado de documentos que el agente puede usar: el Reglamento de Estudiantes y el TUPA. Ver [Corpus](Corpus). |
| **CSAT** | *Customer Satisfaction*: calificación de satisfacción que el usuario puede dar al final de la conversación. |
| **Demo website** | Canal de Copilot Studio que publica el agente en una página web con un link. En este proyecto funciona sin iniciar sesión. |
| **Desambiguación** | Pregunta de aclaración que hace el agente cuando la respuesta depende del nivel, la modalidad o de cuál trámite se trata. Ver [Protocolo conversacional](Protocolo-conversacional). |
| **Direct Line** | Canal de Microsoft para conversar con el agente desde un programa. `eval/run_bank.py` lo usa con un token anónimo para ejecutar el banco de preguntas. |
| **Entidad** | Lista de valores que Copilot Studio reconoce en el mensaje del usuario. El agente usa las predefinidas de texto y de sí/no; el trámite se reconoce con la búsqueda en la tabla Power Fx. |
| **Entorno** | Espacio de Power Platform donde vive el agente. Este agente está en un entorno de prueba, que vence. |
| **Ficha** | Bloque del TUPA que describe un procedimiento o servicio con campos fijos: requisitos, costo, plazo, unidades, contacto y recursos. Hay 63. |
| **Fragmento (*chunk*)** | Trozo de texto en que se divide una unidad para la búsqueda. El build genera 186 del Reglamento y 120 del TUPA (`chunks.jsonl`). |
| **Fuera de alcance** | Consulta que no trata sobre el Reglamento ni el TUPA, como notas personales o admisión. El agente la rechaza y deriva al sitio de normatividad. |
| **Ingesta** | Proceso de leer, limpiar y segmentar los documentos fuente. Su resultado se resume en `data/processed/ingest_report.md`. |
| **Instrucciones** | Texto que define cómo responde el agente en las respuestas generativas: fuentes, formato, aclaraciones y privacidad. Está en `copilot/instructions.md`. |
| **Iteración** | Ronda de ajuste de instrucciones y Topics con un subconjunto de 15 preguntas, antes de ejecutar el banco completo. |
| **Latencia p50 / p90** | Tiempo de respuesta que no superan el 50 % y el 90 % de las preguntas. La meta de p90 es menos de 10 s. |
| **Literal** | Inciso de un artículo identificado con una letra (`a.`, `b.`, `c.`). Las instrucciones piden incluirlos todos. |
| **Low-code** | Desarrollo con herramientas visuales y configuración, con poco código. |
| **Orquestación generativa** | Modo de Copilot Studio en que el modelo decide, según la descripción de cada Topic, si activa un Topic o genera una respuesta con el conocimiento. |
| **Power Fx** | Lenguaje de fórmulas de Power Platform. `tabla_tupa.powerfx` contiene los datos de las 63 fichas que usa la Adaptive Card. |
| **Protocolo conversacional** | Reglas y mensajes fijos de la conversación: bienvenida, menú, aclaraciones, avisos y despedida. Su fuente única es `docs/protocolo.yaml`. |
| **RAG** | *Retrieval-Augmented Generation*: generar la respuesta a partir de fragmentos recuperados de documentos propios. Es lo que hacen las respuestas generativas del agente. |
| **Rechazo correcto** | Proporción de preguntas fuera de alcance o sin respuesta en el corpus que el agente rechaza o deriva, sin inventar. |
| **Reglamento de Estudiantes** | Texto Único Ordenado del Reglamento de Estudiantes de la UCSM (TUO-EST-001, Res. N° 9814-CU-2026), con 159 artículos. |
| **Respuesta generativa** | Respuesta que redacta el modelo de Copilot Studio a partir del conocimiento cargado, con cita de la fuente. |
| **Ronda** | Ejecución completa del banco de 44 preguntas. Hubo cuatro; la cuarta es la medición final. |
| **Rúbrica** | Criterios de `eval/rubrica.md` para calificar cada respuesta como correcta, parcial, incorrecta o alucinada. |
| **Sin evidencia** | Pregunta del dominio cuya respuesta no está en el corpus. El agente responde "No encontré…" y deriva. |
| **Solución** | Paquete exportable de Power Platform con el agente, sus Topics y su conocimiento. Se guarda en `copilot/solution/` como solución no administrada (editable al importarla). |
| **SUS** | *System Usability Scale*: cuestionario estándar de 10 ítems que da un puntaje de usabilidad de 0 a 100. La meta habitual es 68. |
| **Tenant (inquilino)** | Organización de Microsoft 365 a la que pertenecen las cuentas y los entornos. Sus identificadores no se guardan en el repositorio. |
| **Topic** | Diálogo de Copilot Studio con pasos definidos (mensajes, preguntas, condiciones y tarjetas). Los de este agente se generan en `copilot/topics/`. |
| **TUO** | Texto Único Ordenado: versión de una norma que integra todas sus modificaciones en un solo texto. |
| **TUPA** | Texto Único de Procedimientos Administrativos de la UCSM (Res. N° 9888-CU-2026): 48 procedimientos y 15 servicios con su costo, plazo y requisitos. |
| **Unidad** | Elemento normativo completo antes de fragmentar: un artículo del Reglamento o una ficha del TUPA (`units.jsonl`). |
