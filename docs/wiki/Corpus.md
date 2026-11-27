# Corpus

Los dos documentos están en `data/raw/` en PDF (fuente oficial) y en
Markdown (conversión previa). Ambos PDF tienen capa de texto, así que no
hace falta OCR.

| Documento | Páginas | Caracteres (MD) | Unidad normativa |
|---|---|---|---|
| TUO del Reglamento de Estudiantes (Res. 9814-CU-2026) | 40 | ~158 k | 159 artículos (`Art. N°`) |
| TUPA (Res. 9888-CU-2026) | 102 | ~184 k | 63 fichas: 48 procedimientos y 15 servicios |

## Reglamento de Estudiantes

- 21 títulos con capítulos, disposiciones finales y transitorias, y un
  cuadro de control de cambios.
- **Limpieza:**
  - se excluye el índice (unas 200 líneas);
  - se quitan el encabezado y el pie repetidos en cada página;
  - se repara el número de página pegado al de la resolución
    (`9814-CU-20264` es la página 4);
  - se descartan falsos encabezados de artículo dentro de literales y del
    control de cambios;
  - se vuelven a unir los literales (`a.`, `b.`…) separados de su texto.
- **Segmentación:** por artículo, con la ruta Título > Capítulo. El control
  de cambios es una unidad propia; 24 artículos tienen notas de
  modificación.

## TUPA

- Secciones: procedimientos administrativos, servicios prestados en
  exclusividad, formularios y sedes de atención.
- Cada ficha tiene campos fijos: denominación y código, descripción,
  requisitos, monto, modalidad de pago, plazo, calificación, sedes, unidad
  donde se presenta, unidad que aprueba, contacto, recursos y base legal.
- **Limpieza:** se reparan las tablas Markdown rotas de base legal y
  recursos, y se reconstruye la página desde las marcas `pág. N`.
- **Campos estructurados** (`data/processed/tupa.json`): permiten mostrar
  la tarjeta del trámite y validar montos y plazos. Los montos van de
  S/ 0.00 a S/ 825.00 y los plazos están en días hábiles.

## Resultado de la ingesta

| Elemento | Encontrado | Esperado |
|---|---|---|
| Artículos del Reglamento | 159 | 159 |
| Fichas del TUPA | 63 | 63 |
| Procedimientos / servicios | 48 / 15 | 48 / 15 |
| Códigos TUPA únicos | 63 | 63 |

| Documento | Unidades | Fragmentos | Tamaño medio (caracteres) |
|---|---|---|---|
| Reglamento | 162 | 186 | 610 |
| TUPA | 65 | 120 | 1085 |

El detalle está en `data/processed/ingest_report.md`, que genera el build.

## Cruce entre documentos

Varios temas aparecen en ambos documentos: convalidación, anulación de
matrícula, traslados, exámenes de suficiencia, grados, becas y
certificados. Para esas consultas el agente da primero la regla del
Reglamento y luego el trámite del TUPA.
