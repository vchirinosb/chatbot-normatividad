# Evaluación completa del agente (tareas 7.1–7.3)

Ejecución del banco de 44 preguntas (`questions.yaml`) sobre el agente
publicado *Normatividad Estudiantil UCSM*, el 2026-11-24, en el entorno de
prueba de Copilot Studio (ver `docs/bitacora.md`, tarea 6.3). Se hicieron
tres rondas: la ronda 1 detectó brechas en la búsqueda de trámites, que se
corrigieron en el Topic *Consulta de trámite* (ronda 2); la ronda 2 dejó una
respuesta alucinada (REG-17), que se corrigió en el documento de
conocimiento del Reglamento. La ronda 3 es la medición final.

## Método

- **Canal:** Direct Line con token anónimo, igual que un visitante del Demo
  website sin sesión de Microsoft (`eval/run_bank.py`). La URL del token no
  se guarda en el repositorio porque identifica el entorno.
- **Una conversación nueva por pregunta**, para que ninguna respuesta
  dependa de la anterior. En las iteraciones de la tarea 6.2 las 15
  preguntas se hicieron en una misma sesión.
- **Latencia:** diferencia entre la marca de tiempo del servidor del
  mensaje del usuario y la del último mensaje del agente. Incluye la
  pregunta de seguimiento de las tarjetas ("¿Quieres que te detalle los
  requisitos…?").
- **Registro:** respuestas en bruto en `transcripts.jsonl`; calificación
  manual en `calificacion.json`; ambas se combinan en `results.csv` con
  `to_results.py`, y `compute_metrics.py` genera `reporte.md`. La ronda 1
  está en `eval/ronda1/`, la ronda 2 en `eval/ronda2/` y la ronda 3 en
  `eval/` (archivos por defecto).
- **Calificación:** según `rubrica.md`. Cada artículo, código, monto y plazo
  citado se contrastó con `data/processed/units.jsonl` y `tupa.json`. Ante
  la duda se eligió el valor más bajo.
- **Moderación:** no configurable para español (D5).

## Resultados

| Métrica | Ronda 1 | Ronda 2 | Ronda 3 | Meta | ¿Cumple (ronda 3)? |
|---|---|---|---|---|---|
| Correctas o parciales | 39/44 (88,6 %) | 43/44 (97,7 %) | 43/44 (97,7 %) | ≥ 80 % | Sí |
| Respuestas alucinadas | 1 | 1 (REG-17) | 0 | 0 | Sí |
| Acierto de fuente | 31/35 (88,6 %) | 35/35 (100 %) | 34/35 (97,1 %) | — | — |
| Exactitud de montos | 14/17 (82,4 %) | 17/17 (100 %) | 17/17 (100 %) | 100 % | Sí |
| Exactitud de plazos | 15/17 (88,2 %) | 17/17 (100 %) | 17/17 (100 %) | 100 % | Sí |
| Rechazo correcto | 9/9 (100 %) | 9/9 (100 %) | 9/9 (100 %) | — | — |
| Latencia p50 | 8,2 s | 7,9 s | 7,3 s | — | — |
| Latencia p90 | 10,2 s | 11,2 s | 10,8 s | < 10 s | **No** |

Rúbrica de la ronda 3 por categoría:

| Categoría | Preguntas | Correctas | Parcial | Incorrectas | Alucinadas |
|---|---|---|---|---|---|
| Reglamento | 18 | 16 | 1 | 1 | 0 |
| TUPA | 13 | 13 | 0 | 0 | 0 |
| Combinadas | 4 | 4 | 0 | 0 | 0 |
| Fuera de alcance | 5 | 5 | 0 | 0 | 0 |
| Sin respuesta | 4 | 4 | 0 | 0 | 0 |

## Cambios entre rondas

En la ronda 1, TUPA-06, TUPA-09 y TUPA-12 fueron incorrectas por la
búsqueda por palabras del Topic *Consulta de trámite*. Se cambió la búsqueda
en `src/ucsm_bot/copilot_dialogs.py`:

1. Consulta y denominación se comparan sin tildes ni guiones, con "rr"
   reducido a "r" ("prerrequisitos" ~ "Pre-requisitos").
2. Cada palabra se busca por sus primeros cinco caracteres ("adeudo" ~
   "adeudar", "convalidar" ~ "Convalidación").
3. A igual número de coincidencias gana la denominación más corta
   ("certificado de estudios" → *Certificado de Estudios (por semestre)* y
   no *Autenticación de Certificados de estudios…*).

Se simuló la búsqueda nueva en Python con las 13 preguntas de TUPA del
banco y otras consultas frecuentes antes de pegarla en Copilot Studio; no
cambió el resultado de ninguna que ya era correcta. En la ronda 2 las tres
pasaron a correctas. REG-14 también pasó a correcta (cita el Art. 108°),
aunque no se cambió nada en el Reglamento: es variación de la recuperación
entre rondas.

**Entre la ronda 2 y la 3** se corrigió REG-17. En las rondas 1 y 2 el
texto atribuía el 20 % al Art. 137° (tutoría). Primero se agregó a las
instrucciones la regla de citar el artículo del encabezado del fragmento
que contiene cada dato, sin efecto (3 de 3 intentos con el mismo error). La
causa era el corte en fragmentos: el Art. 136° es corto y queda junto al
encabezado del Art. 137°. Se cambió `src/ucsm_bot/knowledge_export.py` para
que cada párrafo del Reglamento empiece con su artículo ("Art. 136°: Se
podrá autorizar…") y se reemplazó el documento de conocimiento. REG-17 quedó
bien atribuida en los 3 intentos previos y en la ronda 3. REG-02 también
pasó a correcta (incluye el literal a del Art. 82°).

## Brechas (ronda 3)

| Id | Rúbrica | Causa | Mejora propuesta |
|---|---|---|---|
| REG-14 | incorrecta | Responde que no encontró un plazo de prescripción y cita la ficha del Bachiller; el Art. 108° dice que los estudios no prescriben. Repetida 3 veces después de la ronda, acertó las 3 (cita el Art. 108°). Falló también en la ronda 1 y acertó en la 2: variación de la recuperación. | Vigilar; si se repite, añadir sinónimos ("prescripción", "caducar", "vencer") al encabezado del Art. 108°. |
| REG-17 | parcial | Atribución correcta (Arts. 135° y 136°), pero omite que las asignaturas exoneradas deben ser del Área de Formación Profesional. | Vigilar; la instrucción de incluir todas las condiciones ya existe. |
| Latencia | p90 10,8 s | Las respuestas generativas tardan 6–16 s (REG-10: 15,6 s; COMB-01 y NOANS-01: 14,7 s); las tarjetas del TUPA tardan 2–3 s. | Depende de la plataforma (p90 10,2 s, 11,2 s y 10,8 s en las tres rondas). |

Brechas de la ronda 2, ya corregidas o cambiadas en la ronda 3:

| Id | Rúbrica | Causa | Mejora propuesta |
|---|---|---|---|
| REG-17 | alucinada | En las dos rondas el dato (20 %) es correcto, pero el texto lo atribuye al Art. 137° (tutoría), que no lo contiene; está en el Art. 136°, también citado en *Fuentes*, y las condiciones en el Art. 135°, no citado. El fragmento del documento de conocimiento está bien etiquetado, así que el error es del modelo al redactar. | Reforzar en las instrucciones que el número de artículo se copie del encabezado del fragmento que contiene cada dato, y no se infiera de fragmentos vecinos; volver a medir REG-17. |
| REG-02 | parcial | En las dos rondas omite el literal a del Art. 82° (asistencia al 100 %), que sí incluía en las iteraciones 2 y 3 de la tarea 6.2. | Vigilar; la instrucción de incluir todos los literales ya existe. |
| Latencia | p90 11,2 s | Las respuestas generativas tardan 6–16 s (NOANS-01: 15,7 s; NOANS-04: 14,3 s); las tarjetas del TUPA tardan 2–3 s. | Depende de la plataforma y varía entre rondas (p90 10,2 s en la ronda 1). |

**Limitación conocida, fuera del banco:** "constancia de estudios" muestra
la *Constancia Especial Programa Especial de Estudios para Guías Oficiales
de Turismo*, porque la ficha general (*CONSTANCIAS*, SE1130737868) lista
los conceptos en el costo y no en la denominación. Incluir el costo en la
comparación causó regresiones en la simulación, por lo que no se aplicó.

## Pendiente

- **Revisión por una segunda persona** (`rubrica.md`, paso 3): revisar al
  menos 10 respuestas al azar de `results.csv` (ronda 3) y registrar aquí el
  acuerdo o la calificación acordada.

| Id | Calificación original | Calificación del revisor | Acordada |
|---|---|---|---|
| | | | |
