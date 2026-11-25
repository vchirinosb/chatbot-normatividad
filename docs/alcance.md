# Alcance del chatbot

## Propósito

Asistente conversacional que orienta a los estudiantes de la Universidad
Católica de Santa María (UCSM) sobre **qué dice la norma** (Reglamento de
Estudiantes) y **cómo, cuánto, cuándo y dónde se tramita** (TUPA), citando
siempre el artículo o el código de procedimiento.

## Corpus (cerrado)

| Documento | Resolución | Páginas | Unidades |
|---|---|---|---|
| Texto Único Ordenado del Reglamento de Estudiantes (TUO-EST-001, V03) | Res. N° 9814-CU-2026 (abril 2026) | 40 | 159 artículos, disposiciones finales y transitorias, control de cambios |
| Texto Único de Procedimientos Administrativos (TUPA) | Res. N° 9888-CU-2026 (junio 2026) | 102 | 63 fichas: 48 procedimientos y 15 servicios |

Solo estos dos documentos de `data/raw/` forman la base de conocimiento.
El resto de documentos de https://ucsm.edu.pe/normatividad/ queda fuera.

## Usuarios objetivo

- **Principales:** estudiantes de pregrado de la UCSM (presencial,
  semipresencial y a distancia).
- **Secundarios:** estudiantes de postgrado (para los trámites de la Escuela
  de Postgrado del TUPA), ingresantes y padres de familia.
- **No objetivo:** docentes y personal administrativo (sus reglamentos no
  están en el corpus).

## Temas cubiertos

1. Matrícula, tipos de matrícula, ampliación de créditos y convalidaciones.
2. Evaluación, aprobación de asignaturas, evaluaciones extemporáneas y
   desaprobación reiterada.
3. Deberes, derechos, faltas y sanciones de los estudiantes.
4. Becas, bienestar universitario y servicios.
5. Grados, títulos, certificados y constancias.
6. Modalidades semipresencial y a distancia.
7. Trámites del TUPA: requisitos, costo, plazo de atención, unidad donde se
   presenta, unidad que aprueba, contacto y recursos.

## Fuera de alcance

1. Datos personales del estudiante: notas, pagos, deudas, estado de
   matrícula, horario (requieren sistemas institucionales con
   autenticación).
2. Admisión y proceso de ingreso (otro reglamento).
3. Reglamentos de docentes, de investigación, de grados por facultad, el
   Estatuto y otros documentos de la página de normatividad.
4. Calendario académico y fechas específicas del semestre en curso.
5. Realizar trámites, pagos o reservas en nombre del estudiante.
6. Asesoría legal o interpretación vinculante de la norma.
7. Preguntas de cultura general o ajenas a la UCSM.

Las consultas fuera de alcance se responden con el mensaje de derivación de
`docs/protocolo.yaml` y el enlace https://ucsm.edu.pe/normatividad/.

## Limitaciones

- **No oficial:** el asistente orienta; el texto vinculante es el del
  documento oficial.
- **Vigencia:** el corpus corresponde a las versiones de 2026; si la UCSM
  modifica los documentos, hay que regenerar el paquete
  (`python -m ucsm_bot.build`) y volver a cargarlo.
- **Calidad del texto fuente:** el Markdown convertido trae listas con los
  literales separados del texto; se reparan automáticamente 66 de 68 listas
  (ver `data/processed/ingest_report.md`). Una ficha del TUPA (Duplicado de
  Carné de Representante Estudiantil) no indica la unidad donde se presenta.
- **Plataforma (Copilot Studio):**
  - el conocimiento se carga como `.docx`; la cita apunta al documento y al
    fragmento, y el encabezado de cada artículo o ficha indica la página;
  - las respuestas generativas pueden variar entre ejecuciones; los montos
    y plazos se muestran desde una tabla fija (Adaptive Card) para que sean
    exactos;
  - la publicación sin autenticación depende de la política del inquilino y
    del tipo de licencia de la cuenta usada; una prueba puede vencer, por lo
    que se respalda con capturas y exportación de la solución;
  - con pago por uso, cada respuesta generativa consume créditos.
- **Idioma:** solo español.
