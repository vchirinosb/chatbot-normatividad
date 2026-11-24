# Análisis del corpus (`data/raw/`)

El corpus del chatbot se limita a los dos documentos de `data/raw/`. Cada
uno está disponible en PDF (fuente oficial) y en Markdown (conversión previa
del autor).

| Documento | Archivo | Páginas | Caracteres (MD) | Unidad normativa |
|---|---|---|---|---|
| TUO del Reglamento de Estudiantes de la UCSM (TUO-EST-001 V03, Res. 9814-CU-2026, abril 2026) | `Reglamento de estudiantes.pdf/.md` | 40 | ~158 k | 159 artículos (`Art. N°`) |
| Texto Único de Procedimientos Administrativos – TUPA (Res. 9888-CU-2026) | `RES_9888-CU-2026-TUPA.pdf/.md` | 102 | ~184 k | 63 fichas: 48 procedimientos + 15 servicios |

URLs oficiales:
- https://www.ucsm.edu.pe/wp-content/uploads/documentos/reglamentos/RES_9814-CU-2026.pdf
- https://www.ucsm.edu.pe/wp-content/uploads/documentos/reglamentos/RES_9888-CU-2026-TUPA.pdf

Ambos PDFs tienen capa de texto: **no se requiere OCR**.

## Reglamento de Estudiantes

- **Estructura:** 21 títulos con capítulos y subcapítulos, más
  disposiciones finales, disposiciones transitorias y un cuadro de control
  de cambios. Temas: disposiciones generales, organización académica,
  régimen de estudios, deberes, derechos y sanciones, participación
  estudiantil, matrícula, complementación, nivelación, traslados internos y
  convalidación, exámenes de suficiencia, evaluación del rendimiento
  (etapas, técnicas, calificación, aprobación, faltas y sanciones), ranking,
  premio a la excelencia, ayudantía de cátedra, certificados, grados y
  títulos, tutoría, bienestar, becas, atención a estudiantes con
  discapacidad, defensoría, egresados, prohibición de alcohol y tabaco, y
  las modalidades semipresencial y a distancia.
- **Artículos:** encabezado `Art. N°  Título:`, del Art. 1° al 159°.
- **Ruido de conversión:**
  - El índice ocupa las ~200 primeras líneas y debe excluirse.
  - El encabezado y el pie se repiten en cada página: código TUO-EST-001,
    aviso del SGI y `- N de 39 -`.
  - El número de página quedó pegado al de la resolución
    (`9814-CU-20264` significa página 4).
  - Hay falsos encabezados de artículo:
    - Un literal `Art. 83° b.24` que no es el inicio de un artículo.
    - Cuatro menciones `Art. 7°/33°/34°` dentro del control de cambios.
- **Vigencia:** el control de cambios final (versiones 02 y 03) incluye
  fe de erratas del tipo "dice / debe decir" (Arts. 57, 98, 102, 124 y 127)
  y adiciones (por ejemplo, el Art. 57 b sobre asignaturas íntegramente
  prácticas). Se indexa como sección propia y se cruza con los artículos
  afectados.

## TUPA

- **Estructura:** sección 1, procedimientos administrativos (48); sección
  2, servicios prestados en exclusividad (15); sección 3, formularios;
  sección 4, sedes de atención.
- **Ficha con campos fijos:** cada procedimiento o servicio trae:
  - Denominación y código (por ejemplo, `PA113073E0FC`).
  - Descripción, requisitos, notas, formularios y canales de atención.
  - Pago por derecho de tramitación (`Monto - S/ xx.xx`) y modalidad de
    pago.
  - Plazo de atención y calificación (evaluación previa o aprobación
    automática, con silencio positivo o negativo).
  - Sedes y horarios, unidad donde se presenta y unidad que aprueba.
  - Consulta (teléfono, anexo y correo).
  - Instancias de recurso (reconsideración y apelación, con autoridad y
    plazos).
  - Base legal.
- **Calidad del MD:** el texto de las fichas es correcto y conserva el
  orden de lectura. Las tablas de "Base legal" y "Recursos" quedaron como
  tablas Markdown rotas (398 líneas `|`, con columnas vacías y palabras
  partidas como `d i s p o s i c i ó n`). Hay que limpiarlas o tomarlas de
  `pdftotext -layout`, que las conserva mejor. Las páginas aparecen como
  `pág. N` y en la cabecera `RESOLUCIÓN No. 9888-CU-2026 | … | N`.
- **Datos críticos para el usuario:**
  - Montos en soles (de S/ 0.00 a S/ 825.00).
  - Plazos en días hábiles.
  - Requisitos numerados.
  - Correos y teléfonos de contacto.

Estos datos deben citarse literalmente y nunca parafrasearse con números
inventados.

## Implicancias para el diseño

1. **Ingesta:** usar el `.md` como fuente principal y el PDF solo para
   verificar páginas y tablas. Sin OCR.
2. **Segmentación:**
   - Reglamento: por artículo, con la ruta Título > Capítulo.
   - TUPA: un fragmento por ficha, más sub-fragmentos por campo cuando
     exceda el tamaño, siempre con el nombre del procedimiento y su código.
3. **Metadatos estructurados del TUPA** (monto, plazo, unidad, código):
   permiten mostrar fichas resumidas y validar las respuestas numéricas.
4. **Cruce entre documentos:** varios temas aparecen en ambos (convalidación,
   anulación de matrícula, traslados, exámenes de suficiencia, grados,
   becas, certificados). El chatbot
   debe combinar la regla del Reglamento con el trámite del TUPA.
5. **Fuera de alcance:** admisión, estatuto, docentes, reglamento interno de
   trabajo y otros reglamentos de la página de normatividad no están en el
   corpus. El chatbot debe derivarlos al sitio oficial.
