# Reporte de ingesta

Generado por `python -m ucsm_bot.build`.

## Cobertura

| Elemento | Encontrado | Esperado | Estado |
|---|---|---|---|
| Artículos del Reglamento | 159/159 | 159 | OK |
| Fichas del TUPA | 63/63 | 63 | OK |
| Procedimientos | 48 | 48 | OK |
| Servicios | 15 | 15 | OK |
| Códigos TUPA únicos | 63 | 63 | OK |

## Fragmentos

| Documento | Unidades | Fragmentos | Tamaño medio (caracteres) |
|---|---|---|---|
| reglamento-estudiantes | 162 | 186 | 610 |
| tupa | 65 | 120 | 1085 |

## Control de cambios

Se detectaron 43 notas al pie de modificación; 24 artículos tienen `has_changes`: 9, 21, 29, 31, 34, 42, 51, 54, 56, 57, 58, 59, 72, 75, 79, 80, 82, 84, 97, 98, 102, 109, 124, 127.

El cuerpo del TUO ya consolida las modificaciones; el cuadro "Control de cambios" es el historial por versión (con numeración anterior y actual mezcladas) y se indexa como unidad propia `reg-control`. Por eso `has_changes` se toma de las notas al pie, que usan la numeración vigente.

## Listas del Reglamento

En el Markdown, varias listas traen los literales (`a.`, `b.`…) separados de su texto; la limpieza los vuelve a unir cuando el número de ítems coincide con el de literales. Literales que quedaron sueltos (sin reparar): 5.

## Campos TUPA faltantes

- Duplicado de Carné de Representante Estudiantil (SE1130730F26, pág. 97): submission_unit. Revisado contra el PDF: el bloque está vacío en el documento original.
