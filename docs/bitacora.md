# Bitácora del proyecto

## Verificación de acceso a Copilot Studio (tarea 1.1)

| Campo | Valor |
|---|---|
| Fecha | 2026-11-24 |
| URL | https://copilotstudio.microsoft.com |
| Cuenta | Cuenta institucional UCSM (Entra ID) |
| Inicio de sesión | Correcto |
| Entorno | "Universidad Católica de Santa María (default)" |
| Versión de la plataforma | `release/2026.11.12.2` (nueva experiencia de Copilot Studio) |
| Indicador en la página de inicio | "Uses Copilot Credits" |
| Creación de agente | **Fallida**: al guardar el agente vacío "Prueba acceso UCSM" la plataforma mostró *"You don't have permission to create agents. Ask your admin to grant you the right role, then try again."* con el detalle *"User license not found"* |
| Tipo de acceso | Ninguno: la cuenta no tiene licencia de Copilot Studio ni rol de creador en el entorno predeterminado |
| Vencimiento | No aplica |
| "No authentication" / *Demo website* | No verificable: no se pudo crear ni guardar el agente |
| Opciones vistas en el menú de cuenta | Novedades, Solutions, experiencia clásica, Power Platform Admin Center, Learn, detalles de sesión. No aparece una opción de prueba gratuita |

**Resultado:** acceso **bloqueado**. Según la tarea 1.1 y el requisito
"Verificación de acceso a la plataforma" de `copilot-studio-agent`, se
detienen los grupos 5 y 6 hasta que el autor decida cómo continuar.

**Alternativas identificadas:**
1. Solicitar a la Dirección de Informática de la UCSM una licencia de Copilot
   Studio, o el rol de creador en un entorno, y el permiso de publicar sin
   autenticación.
2. Intentar la prueba gratuita de Copilot Studio con la cuenta UCSM. El
   inquilino puede bloquear el registro de autoservicio y requiere aceptar
   términos.
3. Usar un inquilino propio de prueba o desarrollador de Microsoft 365, con
   una cuenta nueva creada por el autor.
4. Cambiar de plataforma: Botpress (3,70 en la matriz) o RAG propio con Ollama
   (3,50).

### Segundo intento con otra cuenta (2026-11-24)

| Campo | Valor |
|---|---|
| Fecha | 2026-11-24 |
| Cuenta | Segunda cuenta del inquilino `ucsm.edu.pe` (no la de estudiante); se agregó como cuenta adicional sin cerrar la sesión anterior |
| Entorno | "Universidad Católica de Santa María (default)", el mismo del primer intento |
| Diferencia visible | La cuenta muestra la sección "Apps (Preview)", ausente en la cuenta sin licencia |
| Creación de agente | **Correcta**: el agente vacío "Prueba acceso" se guardó ("Your agent has been saved") |
| "No authentication" | **Disponible**, tras quitar la herramienta *Work IQ*, que viene activada por defecto y exige autenticación de Microsoft ("No authentication unavailable: Microsoft authentication is required for Work IQ") |
| Canal *Demo website* | Aparece en *Channels* al seleccionar "No authentication" |
| Publicación | No realizada en esta verificación (se hará en la tarea 6.3) |
| Tipo de acceso y vencimiento | No visibles en la interfaz (el menú de cuenta no muestra la licencia); consultar al titular de la cuenta o en el Power Platform Admin Center |

**Resultado:** acceso **verificado**. Se pueden iniciar los grupos 5 y 6.

**Hallazgos para la construcción del agente (grupo 5):**
- El idioma principal se fija al guardar el agente por primera vez y no se
  puede cambiar después ("These values were set when the agent was first
  saved and can't be changed"). El agente de prueba quedó en inglés; el
  agente real debe crearse en **español** desde el inicio.
- Un agente nuevo trae activados *Work IQ* (herramienta) y *Search all
  websites* (conocimiento). Hay que quitar ambos: el primero impide "No
  authentication" y el segundo contradice el conocimiento restringido al
  corpus.
- La configuración de autenticación está en *Settings → Safety & access →
  Authentication*.

## Construcción del agente (grupo 5), 2026-11-24

- La experiencia nueva de Copilot Studio no muestra Topics (usa Skills,
  Tools y Knowledge). La opción "Open classic experience" abre una ventana
  emergente; la alternativa es **New agent → Agent (Standard)**, el agente
  basado en Topics.
- Se creó el agente Standard **"Normatividad Estudiantil UCSM"** en
  **Spanish (Mexico)** (el nombre admite pocos caracteres; "Asistente de
  Normatividad Estudiantil UCSM" excedía el máximo).
- **Bloqueo:** en el agente Standard, *Knowledge* y la IA generativa
  muestran "Upgrade your license to start using knowledge" / "Expand the
  capabilities … to include generative AI, agent flows, knowledge, tools …
  by upgrading your license" con el botón *Start a trial*. Sin licencia, el
  agente Standard solo admite Topics con reglas, lo que no permite responder
  sobre los 159 artículos del Reglamento (D5).
- En el entorno ya existía otro agente, "Asistente Normativo UCSM", que no
  es de este proyecto; no se modificó.

## Topics del agente (tareas 5.2–5.4), 2026-11-24

- **Método de carga:** `ucsm_bot.build` genera el YAML de cada Topic en
  `copilot/topics/` a partir de `docs/protocolo.yaml` y `tupa.json`; se pega
  en *Topic → More → Open code editor*. El editor de Copilot Studio exige
  las listas indentadas bajo su clave, rechaza un `:` sin comillas dentro de
  un texto (por ejemplo el `https:` de una URL) y rechaza sinónimos repetidos
  entre ítems de una lista cerrada (`SynonymsNotUnique`); el generador ya
  contempla los tres casos.
- Los Topics propios terminan con `CancelAllDialogs`: sin él, la
  orquestación generativa añadía una respuesta extra después del mensaje
  fijo y se perdían las respuestas rápidas del menú.
- Los Topics propios no tienen frases de activación: se activan por su
  descripción ("The agent chooses"). Las frases de ejemplo provocaban un
  error transitorio `DuplicateItem` en el editor.
- **Desviación (Datos personales):** el diseño preveía una entidad regex
  para DNI y código; se reemplazó por la descripción del Topic, que la
  orquestación reconoce. Verificado con los pasos 12 y 13 del guion.
- **Desviación (Consulta de trámite):** el diseño preveía una entidad de
  lista cerrada con los 63 procedimientos. Copilot Studio asigna a una
  entidad embebida un tipo de conjunto de opciones que la entrada del Topic
  (texto) no acepta ("EmbeddedOptionSetDataType … StringDataType"). La
  entrada `Tramite` es ahora texto y la ficha se elige en la tabla Power Fx
  por código o por la mayor cantidad de palabras de la consulta contenidas
  en la denominación (se ignoran palabras cortas y genéricas). Limitación:
  la comparación distingue tildes.
- Verificación 5.3 (panel de prueba): pasos 2, 8, 9, 12 y 13 del guion con
  los textos literales de `protocolo.yaml`.
- Verificación 5.4 (panel de prueba): paso 4 → tarjeta PA113073C401,
  Gratuito, 30 días hábiles, Mesa de Partes Virtual : Vicerrectorado
  Académico, pág. 32 (coincide con `tupa.json`); paso 7 → PA113073E0FC,
  S/ 44.00, 7 días hábiles.
- Verificación 5.5 (panel de prueba, sesión nueva, 19 pasos): 16/19 sin
  diferencias. Detalle en el registro de `docs/guion_verificacion.md`.
  - Paso 3: la respuesta cita el Art. 83° (pág. 24) y su contenido coincide
    con el texto del artículo (separación temporal de un año; retiro
    definitivo a la cuarta desaprobación). El "resultado esperado" del guion
    lo resume como "separación de la Escuela Profesional".
  - Paso 5: requisitos de la anulación con fuentes TUPA (PA113073C401,
    pág. 32) y Art. 41° (pág. 14), ambos coinciden con el corpus.
  - Diferencias: paso 6 (abre el Menú en vez de `pregunta_si_no_reconoce`),
    paso 10 (da la regla general antes de la pregunta de nivel) y paso 19
    ("gracias, eso es todo" activa el Topic del sistema *Agradecimiento*).
  - Paso 18: el mensaje ofensivo no recibe respuesta generativa y el agente responde
    `fuera_de_alcance`; no hay un mensaje propio de `contenido_inapropiado`.
  - El aviso "No information was found…" de los pasos 14–18 solo lo ve el
    creador en el panel de prueba ("Only visible to you").
- Correcciones posteriores a 5.5 (mismo día):
  - Paso 6: la descripción de *Menú de temas* excluye las solicitudes de
    trámite y la de *Consulta de trámite* las incluye. La entrada `Tramite`
    ya no se pide sola (la orquestación redactaba su propia pregunta); si
    llega vacía, un nodo Pregunta muestra `pregunta_si_no_reconoce` literal.
  - Paso 19: nuevo Topic propio *Cierre de la conversación* (descripción
    con "gracias, eso es todo", "adiós", "chau") con la despedida, la
    encuesta Sí/No y el CSAT; el Topic del sistema *Agradecimiento* ya no
    lo intercepta.
  - Repetidos los pasos 4, 6 y 19: correctos. Resultado del guion: 18/19
    (queda la diferencia menor del paso 10).

## Ajuste, publicación y versionado (tareas 6.2–6.5), 2026-11-24

- 6.2: tres rondas con las 15 preguntas del subconjunto. Están registradas
  en `eval/iteraciones.md`, con las respuestas en `eval/iteraciones/it1.csv`,
  `it2.csv` e `it3.csv`.
  - It. 1: 14 correctas y 1 parcial (REG-02 omitía la asistencia al 100 %).
    Ajuste: las instrucciones piden listas numeradas e incluir todos los
    literales del artículo.
  - It. 2: REG-02 pasa a correcta, pero COMB-01 y COMB-02 salen incorrectas
    porque la orquestación las envió a los Topics.
    Ajuste: las descripciones de *Consulta de trámite* y *Evaluación
    extemporánea* excluyen las consultas combinadas, y la búsqueda de
    trámites exige que coincida más de la mitad de las palabras.
  - It. 3: 14 correctas y 1 parcial (COMB-02 no encuentra el monto de la
    rectificación). Ninguna respuesta alucinada en las tres rondas.
  - Las instrucciones se pegaron en *Overview → Instructions* (3317
    caracteres, igual que el archivo). Los Topics se cambiaron en el editor
    de código y se verificaron en la solución exportada.
- 6.3: autenticación cambiada a *No authentication* y agente publicado (con
  aprobación del autor). La licencia solo ofrece los canales Microsoft
  365/Teams; el *Demo website* requiere la prueba de Copilot Studio. El autor
  aprobó iniciarla, pero el registro pide cargo, empresa y teléfono de
  trabajo, que debe completar el autor. **Pendiente:** el link del Demo
  website y la verificación en ventana privada y celular.
  - Después de que el autor completó el registro de la prueba, aparecieron
    el canal *Demo website* y su link. El link incluye el ID del tenant y no
    se guarda en el repositorio.
  - La página carga sin redirigir al inicio de sesión (HTTP 200) y se ve
    bien en tamaño de celular (375×812).
  - El chat responde "Este agente no está disponible en estos momentos. Ha
    alcanzado el límite de uso". Sigue igual después de esperar y de
    republicar.
  - Causa probable: el entorno *Default* del tenant no tiene capacidad de
    mensajes (*Copilot Credits*) para los canales publicados. La licencia de
    prueba del usuario no la añade. El panel de prueba sí funciona, porque no
    consume esa capacidad.
  - Solución (aprobada por el autor): se creó un entorno de prueba
    (*Trial*, 30 días, región Sudamérica, con Dataverse y sin grupo de
    seguridad) y se importó en él la solución de la tarea 6.4. El autor
    eligió el `.zip` en el diálogo de importación, porque el navegador del
    agente no puede adjuntar archivos locales.
  - Tras la importación, el agente quedó publicado y con las mismas
    instrucciones (3317 caracteres), los 9 Topics personalizados activos, los
    2 documentos de conocimiento en estado *Ready* y *No authentication*. El
    estado del agente muestra dos advertencias esperadas: acceso sin inicio
    de sesión y ninguna evaluación ejecutada.
  - El Demo website de este entorno sí responde. Con sesión: "¿Cuál es la
    nota mínima para aprobar una asignatura?" devuelve el Art. 82°
    (pág. 24). En tamaño de celular (375×812): "¿Cuánto cuesta la anulación
    de matrícula?" muestra la tarjeta de PA113073C401 (Gratuito, 30 días
    hábiles), que coincide con `tupa.json`.
  - Sin sesión de Microsoft: la página del link responde HTTP 200 sin
    cookies, y una conversación por Direct Line con token anónimo (sin
    credenciales) respondió la bienvenida y la pregunta sobre evaluación
    extemporánea en pregrado (PA1130732571, Gratuito, 5 días hábiles,
    verificado en `tupa.json`). No se abrió en un celular físico: la prueba
    móvil se hizo con la emulación del navegador.
  - El link nuevo también contiene el ID del tenant y no se guarda en el
    repositorio. El entorno de prueba vence a los 30 días (2026-12-24
    aprox.); para la evaluación completa y la defensa hay que tenerlo en
    cuenta.
- 6.4: se aceptó la bienvenida de Power Apps (Perú, sin ofertas) y se creó la
  solución no administrada *Normatividad Estudiantil UCSM*. Solo contiene
  este agente (1 agente y 21 componentes) y usa el publicador CDS Default
  Publisher. Se exportó como `copilot/solution/NormatividadEstudiantilUCSM_1_0_0_1.zip`
  (47 archivos: `bot.xml`, el Topic de cada diálogo y los 2 `.docx`).
  - No se usó *Publish all changes*, porque publicaría las personalizaciones
    de todo el entorno compartido.
  - Revisión del `.zip`: no contiene nombres ni IDs personales; los únicos
    correos son los de contacto del TUPA.
  - La configuración exportada muestra `contentModeration: "Low"`, distinto
    del valor "Alta" previsto en D5. Al intentar subirlo (con aprobación del
    autor), *Settings → Generative AI → Moderation* indica "Content
    moderation isn't supported for this agent's primary language" (español)
    y no ofrece selector de nivel; tampoco hay *Boosting conversations* en
    español. No se cambió nada ni se repitió la ronda. D5,
    `copilot/instructions.md` y `eval/iteraciones.md` se actualizaron: la
    moderación configurable no aplica y la sustituyen las instrucciones,
    *Allow ungrounded responses* desactivado y la búsqueda web desactivada.
- 6.5: seis capturas en `docs/figuras/agente_*`: lienzo del Topic de
  trámite, bienvenida, respuesta con cita y mapa de actividad, Adaptive
  Card, desambiguación y fuera de alcance.
  - Están recortadas para excluir la lista de Topics con el nombre del autor
    y el avatar.
  - Resolución de 763×513 px como máximo, limitada por el panel del
    navegador.
  - Captura móvil: `docs/figuras/agente_demo_movil.jpg` (Demo website del
    entorno de prueba a 375×812, tarjeta de Anulación de Matrícula).

## Evaluación (tareas 7.1–7.5), 2026-11-24

- 7.1: banco de 44 preguntas ejecutado sobre el agente publicado por Direct
  Line con token anónimo (`eval/run_bank.py`), una conversación por
  pregunta. Transcripciones en `eval/transcripts.jsonl`; `results.csv`
  tiene una fila por pregunta (44).
- 7.2: `compute_metrics.py` ya existía; se corrigió la extracción de citas
  para listas de artículos ("artículos 136° y 137°", "Arts. 85° y 86°"),
  con una prueba nueva (38 pruebas OK). `eval/reporte.md` generado.
- 7.3, ronda 1 (`eval/ronda1/`): 38 correctas, 1 parcial, 4 incorrectas y
  1 alucinada (88,6 %); montos 82,4 %, plazos 88,2 %, p90 10,2 s. Tres
  incorrectas (TUPA-06, 09 y 12) venían de la búsqueda por palabras del
  Topic *Consulta de trámite*.
- Corrección (aprobada por el autor): la búsqueda compara sin tildes ni
  guiones, por los primeros cinco caracteres de cada palabra, y desempata
  por la denominación más corta. Simulada en Python antes de aplicarla;
  YAML regenerado (39 pruebas OK), pegado en el editor de código solo con
  el cambio de la fórmula (la tabla se verificó idéntica) y agente
  republicado.
- 7.3, ronda 2 (medición final, `eval/`): 42 correctas, 1 parcial y 1
  alucinada (97,7 %); fuentes, montos y plazos al 100 %. No se cumplen
  0 alucinadas (REG-17 atribuye el 20 % al Art. 137° en vez del 136° en
  las dos rondas) ni p90 < 10 s (11,2 s). Detalle en
  `eval/evaluacion_completa.md`. **Pendiente:** revisión de al menos 10
  respuestas por una segunda persona.
- Versionado (aprobado por el autor): solución exportada desde el entorno
  de prueba como no administrada, versión 1.0.0.2, en
  `copilot/solution/NormatividadEstudiantilUCSM_1_0_0_2.zip` (47 archivos).
  Se conserva la 1.0.0.1 (agente de las iteraciones 6.2 y de la ronda 1).
  Diferencias con la 1.0.0.1: el Topic *Consulta de trámite* (búsqueda
  nueva), el número de versión y la versión de la plataforma; `bot.xml` ya
  no incluye la configuración de autenticación vacía. Sin nombres ni IDs
  personales; los correos son los de contacto del TUPA. El agente del
  entorno *Default* conserva la búsqueda anterior.
- Corrección de REG-17 (aprobada por el autor): la regla de instrucciones
  "cada artículo debe ser el del encabezado del fragmento" no bastó (3 de 3
  intentos seguían atribuyendo el 20 % al Art. 137°). Causa: el Art. 136°
  es corto y queda en el mismo fragmento que el encabezado del Art. 137°.
  Se cambió `src/ucsm_bot/knowledge_export.py` para que cada párrafo del
  Reglamento empiece con su artículo ("Art. 136°: Se podrá autorizar…"),
  con una prueba nueva (40 pruebas OK). El autor reemplazó
  `reglamento_estudiantes.docx` en *Knowledge*; se publicó cuando quedó en
  *Ready* (mientras estaba *In progress* el agente respondía "fuera de
  alcance" a preguntas del Reglamento). REG-17 quedó bien atribuida en 4 de
  4 intentos.
- Ronda 3 (banco completo, con el `.docx` nuevo): 42 correctas, 1 parcial
  (REG-17 omite el Área de Formación Profesional), 1 incorrecta (REG-14
  responde "no encontré"; al repetirla 3 veces acertó las 3) y **0
  alucinadas**: 97,7 % correctas o parciales. Montos y plazos 100 %; p90
  10,8 s (no cumple < 10 s). La ronda 2 quedó en `eval/ronda2/`.
- Versionado después de la ronda 3 (aprobado por el autor): solución
  exportada como no administrada, versión 1.0.0.3, en
  `copilot/solution/NormatividadEstudiantilUCSM_1_0_0_3.zip` (47 archivos).
  Diferencias con la 1.0.0.2: el `reglamento_estudiantes.docx` nuevo
  (idéntico byte a byte a `copilot/knowledge/reglamento_estudiantes.docx`),
  la regla de atribución de artículos en las instrucciones y el número de
  versión. Sin nombres ni IDs personales. Se conservan la 1.0.0.1 y la
  1.0.0.2.
- Alcance (decisión del autor, 2026-11-24): se quitaron las tareas 3.4
  (validación del protocolo con usuarios; el protocolo se validó sobre el
  agente) y 7.6 (video de demostración; el respaldo del link son las
  capturas, la solución exportada y las transcripciones). Se actualizaron
  propuesta, diseño, specs y tareas (`openspec validate` OK).
- 7.4 preparada: guion de sesión, invitación y lista previa en
  `eval/tareas_usabilidad.md`; formulario de Forms en
  `eval/formulario_sus.md`; conversión de la exportación con
  `eval/forms_to_sus.py` (prueba nueva; 41 pruebas OK; verificada con una
  exportación simulada); plantilla de resultados en `eval/usabilidad.md`.
  Las 5 tareas se probaron en el agente con redacción informal y llegan al
  criterio de éxito. **Pendiente:** crear el formulario y hacer la prueba
  con ≥ 5 participantes.
- 7.5: **pendiente.** La analítica del agente (*Monitor*) seguía en cero
  sesiones después del banco; Copilot Studio tarda en procesarlas, y el
  periodo de pruebas debe incluir la prueba de usabilidad.

## Consulta de licencias (tarea 2.3), 2026-11-24

- Copilot Studio: prueba sin publicación; pago por uso a US$ 0,01 por
  *Copilot Credit* (clásica = 1, generativa = 2) con suscripción de Azure;
  paquete de US$ 200/mes por 25 000 créditos.
- Botpress Cloud: plan Free de US$ 0 con 100 conversaciones/mes sin
  excedentes (el emulador también consume); Plus de US$ 150/mes (anual).
- Dialogflow CX (Conversational Agents): créditos de prueba de US$ 600
  (flows) y US$ 1 000 (generativo) por 1 año; US$ 0,007 por solicitud de
  chat (flows) y US$ 0,012 (playbooks); requiere facturación en GCP.

## Horas por grupo de tareas

El autor completa la columna de horas al cerrar cada grupo.

| Grupo | Horas | Notas |
|---|---|---|
| 1. Configuración y verificación de acceso | | Cerrado el 2026-11-24 (1.1 verificada con la segunda cuenta) |
| 2. Alcance, revisión y matriz | | Cerrado el 2026-11-24 |
| 3. Protocolo conversacional | | Cerrado el 2026-11-24 (3.4 descartada por el autor; validación sobre el agente) |
| 4. Preparación del corpus | | Cerrado el 2026-11-24 (28 pruebas OK, build determinista) |
| 5. Construcción del agente | | |
| 6. Entrenamiento, publicación y versionado | | |
| 7. Evaluación | | |
| 8. Paper | | |
