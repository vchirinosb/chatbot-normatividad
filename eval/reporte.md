# Reporte de evaluación

Generado por `eval/compute_metrics.py` a partir de `eval/results.csv`.

## Métricas

| Métrica | Resultado | Meta |
|---|---|---|
| Acierto de fuente | 34/35 (97,1 %) | — |
| Exactitud de montos | 17/17 (100,0 %) | 100 % |
| Exactitud de plazos | 17/17 (100,0 %) | 100 % |
| Rechazo correcto (fuera de alcance y sin respuesta) | 9/9 (100,0 %) | — |
| Latencia p50 | 7,3 s | — |
| Latencia p90 | 10,8 s | < 10 s ✗ |

## Rúbrica

| Calificación | Preguntas |
|---|---|
| correcta | 42 |
| parcial | 1 |
| incorrecta | 1 |
| alucinada | 0 |

Correctas o parciales: 97,7 % (meta ≥ 80 %); alucinadas: 0 (meta 0). **Cumple la meta.**

## Detalle por pregunta

| Id | Categoría | Fuente | Monto | Plazo | Rechazo | Latencia | Rúbrica |
|---|---|---|---|---|---|---|---|
| REG-01 | reglamento | ✓ | — | — | — | 7,0 s | correcta |
| REG-02 | reglamento | ✓ | — | — | — | 8,6 s | correcta |
| REG-03 | reglamento | ✓ | — | — | — | 7,9 s | correcta |
| REG-04 | reglamento | ✓ | — | — | — | 5,9 s | correcta |
| REG-05 | reglamento | ✓ | — | — | — | 8,7 s | correcta |
| REG-06 | reglamento | ✓ | — | — | — | 7,5 s | correcta |
| REG-07 | reglamento | ✓ | — | — | — | 6,6 s | correcta |
| REG-08 | reglamento | ✓ | — | — | — | 6,9 s | correcta |
| REG-09 | reglamento | ✓ | — | — | — | 8,0 s | correcta |
| REG-10 | reglamento | ✓ | — | — | — | 15,6 s | correcta |
| REG-11 | reglamento | ✓ | — | — | — | 7,7 s | correcta |
| REG-12 | reglamento | ✓ | — | — | — | 7,9 s | correcta |
| REG-13 | reglamento | ✓ | — | — | — | 6,6 s | correcta |
| REG-14 | reglamento | ✗ | — | — | — | 10,9 s | incorrecta |
| REG-15 | reglamento | ✓ | — | — | — | 7,1 s | correcta |
| REG-16 | reglamento | ✓ | — | — | — | 7,3 s | correcta |
| REG-17 | reglamento | ✓ | — | — | — | 7,3 s | parcial |
| REG-18 | reglamento | ✓ | — | — | — | 7,9 s | correcta |
| TUPA-01 | tupa | ✓ | ✓ | ✓ | — | 2,0 s | correcta |
| TUPA-02 | tupa | ✓ | ✓ | ✓ | — | 2,1 s | correcta |
| TUPA-03 | tupa | ✓ | ✓ | ✓ | — | 2,1 s | correcta |
| TUPA-04 | tupa | ✓ | ✓ | ✓ | — | 2,2 s | correcta |
| TUPA-05 | tupa | ✓ | ✓ | ✓ | — | 2,4 s | correcta |
| TUPA-06 | tupa | ✓ | ✓ | ✓ | — | 2,6 s | correcta |
| TUPA-07 | tupa | ✓ | ✓ | ✓ | — | 2,5 s | correcta |
| TUPA-08 | tupa | ✓ | ✓ | ✓ | — | 2,6 s | correcta |
| TUPA-09 | tupa | ✓ | ✓ | ✓ | — | 2,0 s | correcta |
| TUPA-10 | tupa | ✓ | ✓ | ✓ | — | 2,1 s | correcta |
| TUPA-11 | tupa | ✓ | ✓ | ✓ | — | 2,5 s | correcta |
| TUPA-12 | tupa | ✓ | ✓ | ✓ | — | 2,2 s | correcta |
| TUPA-13 | tupa | ✓ | ✓ | ✓ | — | 3,2 s | correcta |
| COMB-01 | combinada | ✓ | ✓ | ✓ | — | 14,7 s | correcta |
| COMB-02 | combinada | ✓ | ✓ | ✓ | — | 7,4 s | correcta |
| COMB-03 | combinada | ✓ | ✓ | ✓ | — | 8,5 s | correcta |
| COMB-04 | combinada | ✓ | ✓ | ✓ | — | 10,5 s | correcta |
| OUT-01 | fuera_alcance | — | — | — | ✓ | 8,6 s | correcta |
| OUT-02 | fuera_alcance | — | — | — | ✓ | 8,7 s | correcta |
| OUT-03 | fuera_alcance | — | — | — | ✓ | 8,4 s | correcta |
| OUT-04 | fuera_alcance | — | — | — | ✓ | 9,1 s | correcta |
| OUT-05 | fuera_alcance | — | — | — | ✓ | 8,0 s | correcta |
| NOANS-01 | sin_respuesta | — | — | — | ✓ | 14,7 s | correcta |
| NOANS-02 | sin_respuesta | — | — | — | ✓ | 5,7 s | correcta |
| NOANS-03 | sin_respuesta | — | — | — | ✓ | 8,0 s | correcta |
| NOANS-04 | sin_respuesta | — | — | — | ✓ | 13,8 s | correcta |
