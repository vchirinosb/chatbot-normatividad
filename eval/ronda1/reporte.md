# Reporte de evaluación

Generado por `eval/compute_metrics.py` a partir de `eval/results.csv`.

## Métricas

| Métrica | Resultado | Meta |
|---|---|---|
| Acierto de fuente | 31/35 (88,6 %) | — |
| Exactitud de montos | 14/17 (82,4 %) | 100 % |
| Exactitud de plazos | 15/17 (88,2 %) | 100 % |
| Rechazo correcto (fuera de alcance y sin respuesta) | 9/9 (100,0 %) | — |
| Latencia p50 | 8,2 s | — |
| Latencia p90 | 10,2 s | < 10 s ✗ |

## Rúbrica

| Calificación | Preguntas |
|---|---|
| correcta | 38 |
| parcial | 1 |
| incorrecta | 4 |
| alucinada | 1 |

Correctas o parciales: 88,6 % (meta ≥ 80 %); alucinadas: 1 (meta 0). **No cumple la meta.**

## Detalle por pregunta

| Id | Categoría | Fuente | Monto | Plazo | Rechazo | Latencia | Rúbrica |
|---|---|---|---|---|---|---|---|
| REG-01 | reglamento | ✓ | — | — | — | 9,8 s | correcta |
| REG-02 | reglamento | ✓ | — | — | — | 8,3 s | parcial |
| REG-03 | reglamento | ✓ | — | — | — | 6,9 s | correcta |
| REG-04 | reglamento | ✓ | — | — | — | 6,6 s | correcta |
| REG-05 | reglamento | ✓ | — | — | — | 7,8 s | correcta |
| REG-06 | reglamento | ✓ | — | — | — | 8,8 s | correcta |
| REG-07 | reglamento | ✓ | — | — | — | 6,6 s | correcta |
| REG-08 | reglamento | ✓ | — | — | — | 9,1 s | correcta |
| REG-09 | reglamento | ✓ | — | — | — | 8,2 s | correcta |
| REG-10 | reglamento | ✓ | — | — | — | 9,8 s | correcta |
| REG-11 | reglamento | ✓ | — | — | — | 8,2 s | correcta |
| REG-12 | reglamento | ✓ | — | — | — | 8,2 s | correcta |
| REG-13 | reglamento | ✓ | — | — | — | 8,2 s | correcta |
| REG-14 | reglamento | ✗ | — | — | — | 12,8 s | incorrecta |
| REG-15 | reglamento | ✓ | — | — | — | 7,2 s | correcta |
| REG-16 | reglamento | ✓ | — | — | — | 8,8 s | correcta |
| REG-17 | reglamento | ✓ | — | — | — | 8,0 s | alucinada |
| REG-18 | reglamento | ✓ | — | — | — | 6,4 s | correcta |
| TUPA-01 | tupa | ✓ | ✓ | ✓ | — | 3,8 s | correcta |
| TUPA-02 | tupa | ✓ | ✓ | ✓ | — | 3,4 s | correcta |
| TUPA-03 | tupa | ✓ | ✓ | ✓ | — | 3,1 s | correcta |
| TUPA-04 | tupa | ✓ | ✓ | ✓ | — | 2,6 s | correcta |
| TUPA-05 | tupa | ✓ | ✓ | ✓ | — | 3,4 s | correcta |
| TUPA-06 | tupa | ✗ | ✗ | ✓ | — | 2,1 s | incorrecta |
| TUPA-07 | tupa | ✓ | ✓ | ✓ | — | 2,8 s | correcta |
| TUPA-08 | tupa | ✓ | ✓ | ✓ | — | 2,7 s | correcta |
| TUPA-09 | tupa | ✗ | ✗ | ✗ | — | 2,8 s | incorrecta |
| TUPA-10 | tupa | ✓ | ✓ | ✓ | — | 2,9 s | correcta |
| TUPA-11 | tupa | ✓ | ✓ | ✓ | — | 2,6 s | correcta |
| TUPA-12 | tupa | ✗ | ✗ | ✗ | — | 3,0 s | incorrecta |
| TUPA-13 | tupa | ✓ | ✓ | ✓ | — | 2,7 s | correcta |
| COMB-01 | combinada | ✓ | ✓ | ✓ | — | 13,2 s | correcta |
| COMB-02 | combinada | ✓ | ✓ | ✓ | — | 9,3 s | correcta |
| COMB-03 | combinada | ✓ | ✓ | ✓ | — | 9,1 s | correcta |
| COMB-04 | combinada | ✓ | ✓ | ✓ | — | 9,8 s | correcta |
| OUT-01 | fuera_alcance | — | — | — | ✓ | 8,5 s | correcta |
| OUT-02 | fuera_alcance | — | — | — | ✓ | 9,0 s | correcta |
| OUT-03 | fuera_alcance | — | — | — | ✓ | 8,3 s | correcta |
| OUT-04 | fuera_alcance | — | — | — | ✓ | 9,5 s | correcta |
| OUT-05 | fuera_alcance | — | — | — | ✓ | 8,4 s | correcta |
| NOANS-01 | sin_respuesta | — | — | — | ✓ | 14,2 s | correcta |
| NOANS-02 | sin_respuesta | — | — | — | ✓ | 9,0 s | correcta |
| NOANS-03 | sin_respuesta | — | — | — | ✓ | 10,3 s | correcta |
| NOANS-04 | sin_respuesta | — | — | — | ✓ | 24,7 s | correcta |
