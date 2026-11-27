# Evaluación completa del agente

Ejecución del banco de 44 preguntas (`questions.yaml`) sobre el agente
publicado *Normatividad Estudiantil UCSM*, el 2026-11-24, en el entorno de
prueba de Copilot Studio (ver `docs/bitacora.md`). Se hicieron
tres rondas: la ronda 1 detectó brechas en la búsqueda de trámites, que se
corrigieron en el Topic *Consulta de trámite* (ronda 2); la ronda 2 dejó una
respuesta alucinada (REG-17), que se corrigió en el documento de
conocimiento del Reglamento. La ronda 3 fue la medición final
prevista. El 2026-11-25, después de la prueba de usabilidad, se
corrigió la elección de fichas del TUPA cuando varias empatan y se repitió
el banco completo (ronda 4) para comprobar que el cambio no afectara otras
respuestas.

## Método

- **Canal:** Direct Line con token anónimo, igual que un visitante del Demo
  website sin sesión de Microsoft (`eval/run_bank.py`). La URL del token no
  se guarda en el repositorio porque identifica el entorno.
- **Una conversación nueva por pregunta**, para que ninguna respuesta
  dependa de la anterior. En las iteraciones de ajuste las 15
  preguntas se hicieron en una misma sesión.
- **Latencia:** diferencia entre la marca de tiempo del servidor del
  mensaje del usuario y la del último mensaje del agente. Incluye la
  pregunta de seguimiento de las tarjetas ("¿Quieres que te detalle los
  requisitos…?").
- **Registro:** respuestas en bruto en `transcripts.jsonl`; calificación
  manual en `calificacion.json`; ambas se combinan en `results.csv` con
  `to_results.py`, y `compute_metrics.py` genera `reporte.md`. Solo se
  conservan los archivos de la ronda 4, en `eval/`; las rondas 1–3 se
  resumen en este documento.
- **Calificación:** según `rubrica.md`. Cada artículo, código, monto y plazo
  citado se contrastó con `data/processed/units.jsonl` y `tupa.json`. Ante
  la duda se eligió el valor más bajo.
- **Moderación:** no configurable para español.

## Resultados

| Métrica | Ronda 1 | Ronda 2 | Ronda 3 | Ronda 4 | Meta | ¿Cumple (ronda 4)? |
|---|---|---|---|---|---|---|
| Correctas o parciales | 39/44 (88,6 %) | 43/44 (97,7 %) | 43/44 (97,7 %) | 44/44 (100 %) | ≥ 80 % | Sí |
| Correctas | — | — | 42/44 | 44/44 | — | — |
| Respuestas alucinadas | 1 | 1 (REG-17) | 0 | 0 | 0 | Sí |
| Acierto de fuente | 31/35 (88,6 %) | 35/35 (100 %) | 34/35 (97,1 %) | 35/35 (100 %) | — | — |
| Exactitud de montos | 14/17 (82,4 %) | 17/17 (100 %) | 17/17 (100 %) | 17/17 (100 %) | 100 % | Sí |
| Exactitud de plazos | 15/17 (88,2 %) | 17/17 (100 %) | 17/17 (100 %) | 17/17 (100 %) | 100 % | Sí |
| Rechazo correcto | 9/9 (100 %) | 9/9 (100 %) | 9/9 (100 %) | 9/9 (100 %)¹ | — | — |
| Latencia p50 | 8,2 s | 7,9 s | 7,3 s | 8,2 s | — | — |
| Latencia p90 | 10,2 s | 11,2 s | 10,8 s | 12,3 s | < 10 s | **No** |

¹ NOANS-02 se marcó a mano como rechazo en `calificacion.json`: dice que
la fecha no está en el Reglamento y deriva, pero con una frase que
`compute_metrics.py` no detecta (sin la marca, 8/9).

Rúbrica de la ronda 4 por categoría (en la ronda 3, Reglamento: 16
correctas, 1 parcial y 1 incorrecta):

| Categoría | Preguntas | Correctas | Parcial | Incorrectas | Alucinadas |
|---|---|---|---|---|---|
| Reglamento | 18 | 18 | 0 | 0 | 0 |
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

**Entre la ronda 3 y la 4** se corrigió el error principal de la prueba de
usabilidad (`usabilidad.md`, T2): ante "copia autenticada de mi título" el
agente mostraba la ficha del acta de grados (S/ 55.00, 5 días) en vez de la
de la resolución del título (S/ 44.00, 7 días). Las dos fichas coincidían
en las mismas tres palabras y el empate se resolvía por la denominación más
corta. Cambios en `src/ucsm_bot/copilot_dialogs.py`:

1. Segundo criterio de desempate: palabras completas contenidas en la
   denominación ("titulo" está en "títulos" pero no en "Titular"; antes,
   por raíz, empataba con *Copia autenticada de Resolución expedida por la
   Universidad (…Titular…)*).
2. Si aun así empatan fichas con denominaciones de largo parecido (hasta
   1,5 veces la mejor), el agente las lista (hasta cuatro) con código,
   costo y plazo y pregunta cuál; el usuario responde con el número, el
   código o el nombre.

Se simuló en Python con las 13 preguntas de TUPA y otras consultas: todas
las del banco conservan su ficha y solo preguntan las ambiguas ("copia
autenticada de mi título", "duplicado de carné", "evaluación
extemporánea"). Después de publicar se verificó por Direct Line: "copia
autenticada de mi título" lista las dos fichas y "1", "la de la
resolución" o el código llevan a la tarjeta correcta; con "resolución" en
la pregunta muestra directamente PA113073E0FC. En la ronda 4 las 13
tarjetas del TUPA son idénticas a las de la ronda 3 y ninguna pregunta del
banco activó la desambiguación. REG-14 y REG-17 pasaron a correctas sin
cambios en el Reglamento (variación de la recuperación).

## Brechas (ronda 4)

| Id | Rúbrica | Causa | Mejora propuesta |
|---|---|---|---|
| Latencia | p90 12,3 s | Las respuestas generativas tardan 7–16 s (COMB-04: 15,6 s; NOANS-01: 15,2 s); las tarjetas del TUPA, 2–3 s. | Depende de la plataforma (p90 entre 10,2 s y 12,3 s en las cuatro rondas). |

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
| REG-02 | parcial | En las dos rondas omite el literal a del Art. 82° (asistencia al 100 %), que sí incluía en las iteraciones 2 y 3 de ajuste. | Vigilar; la instrucción de incluir todos los literales ya existe. |
| Latencia | p90 11,2 s | Las respuestas generativas tardan 6–16 s (NOANS-01: 15,7 s; NOANS-04: 14,3 s); las tarjetas del TUPA tardan 2–3 s. | Depende de la plataforma y varía entre rondas (p90 10,2 s en la ronda 1). |

**Limitación conocida, fuera del banco:** "constancia de estudios" muestra
la *Constancia Especial Programa Especial de Estudios para Guías Oficiales
de Turismo*, porque la ficha general (*CONSTANCIAS*, SE1130737868) lista
los conceptos en el costo y no en la denominación. Incluir el costo en la
comparación causó regresiones en la simulación, por lo que no se aplicó.

## Pendiente

- **Revisión por una segunda persona** (`rubrica.md`, paso 3): revisar al
  menos 10 respuestas al azar de `results.csv` (ronda 4) y registrar aquí el
  acuerdo o la calificación acordada.

| Id | Calificación original | Calificación del revisor | Acordada |
|---|---|---|---|
| | | | |
