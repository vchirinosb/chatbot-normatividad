# Alcance y limitaciones

## Corpus

| Documento | Resolución | Páginas | Unidades |
|---|---|---|---|
| Texto Único Ordenado del Reglamento de Estudiantes (TUO-EST-001, V03) | Res. N° 9814-CU-2026 (abril 2026) | 40 | 159 artículos, disposiciones finales y transitorias, control de cambios |
| Texto Único de Procedimientos Administrativos (TUPA) | Res. N° 9888-CU-2026 (junio 2026) | 102 | 63 fichas: 48 procedimientos y 15 servicios |

El corpus es cerrado: el resto de documentos de
https://ucsm.edu.pe/normatividad/ queda fuera.

## Usuarios

- **Principales:** estudiantes de pregrado (presencial, semipresencial y a
  distancia).
- **Secundarios:** estudiantes de postgrado (trámites de la Escuela de
  Postgrado), ingresantes y padres de familia.
- **No objetivo:** docentes y personal administrativo, cuyos reglamentos no
  están en el corpus.

## Temas cubiertos

1. Matrícula, tipos de matrícula, ampliación de créditos y convalidaciones.
2. Evaluación, aprobación de asignaturas, evaluaciones extemporáneas y
   desaprobación reiterada.
3. Deberes, derechos, faltas y sanciones.
4. Becas, bienestar universitario y servicios.
5. Grados, títulos, certificados y constancias.
6. Modalidades semipresencial y a distancia.
7. Trámites del TUPA: requisitos, costo, plazo, unidad donde se presenta,
   unidad que aprueba, contacto y recursos.

## Fuera de alcance

1. Datos personales: notas, pagos, deudas, estado de matrícula u horario.
2. Admisión y proceso de ingreso.
3. Reglamentos de docentes, de investigación, de grados por facultad, el
   Estatuto y otros documentos.
4. Calendario académico y fechas del semestre en curso.
5. Hacer trámites, pagos o reservas en nombre del estudiante.
6. Asesoría legal o interpretación vinculante de la norma.
7. Cultura general o temas ajenos a la UCSM.

Estas consultas se responden con un mensaje de derivación a
https://ucsm.edu.pe/normatividad/.

## Limitaciones

- **No oficial:** el asistente orienta; manda el documento oficial.
- **Vigencia:** el corpus corresponde a las versiones de 2026. Si la UCSM
  cambia los documentos, hay que regenerar el conocimiento y volver a
  cargarlo en Copilot Studio.
- **Texto fuente:** la limpieza repara automáticamente la mayoría de las
  listas del Reglamento; quedan 5 literales sueltos. Una ficha del TUPA
  (Duplicado de Carné de Representante Estudiantil) no indica la unidad
  donde se presenta, también en el PDF original.
- **Respuestas generativas:** pueden variar entre ejecuciones. Los montos y
  plazos de trámites no dependen de ellas: salen de una tabla fija.
- **Latencia:** las respuestas generativas tardan entre 6 y 16 s; las
  tarjetas del TUPA, 2–3 s.
- **Moderación:** Copilot Studio no permite configurar el nivel de
  moderación para agentes en español; la sustituyen las instrucciones y la
  restricción al conocimiento cargado.
- **Disponibilidad:** el agente está en un entorno de prueba de Copilot
  Studio, que vence. La solución exportada en `copilot/solution/` permite
  importarlo en otro entorno.
- **Idioma:** solo español.
