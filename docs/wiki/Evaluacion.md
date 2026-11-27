# Evaluación

## Banco de preguntas

`eval/questions.yaml` tiene 44 preguntas con su respuesta esperada:

| Categoría | Preguntas |
|---|---|
| Reglamento | 18 |
| TUPA | 13 |
| Combinadas | 4 |
| Fuera de alcance | 5 |
| Sin respuesta en el corpus | 4 |

**Método:**
- `eval/run_bank.py` envía cada pregunta en una conversación nueva por
  Direct Line con un token anónimo, igual que un visitante del *Demo
  website* sin sesión, y guarda `transcripts.jsonl`.
- La calificación manual (`calificacion.json`) sigue `eval/rubrica.md`:
  correcta, parcial, incorrecta o alucinada. Cada artículo, código, monto y
  plazo citado se contrasta con el corpus procesado.
- `eval/to_results.py` combina ambos en `results.csv`, y
  `eval/compute_metrics.py` escribe `eval/reporte.md`.

## Resultados por ronda

| Métrica | Ronda 1 | Ronda 2 | Ronda 3 | Ronda 4 | Meta |
|---|---|---|---|---|---|
| Correctas o parciales | 88,6 % | 97,7 % | 97,7 % | **100 %** | ≥ 80 % |
| Respuestas alucinadas | 1 | 1 | 0 | **0** | 0 |
| Acierto de fuente | 88,6 % | 100 % | 97,1 % | **100 %** | — |
| Exactitud de montos | 82,4 % | 100 % | 100 % | **100 %** | 100 % |
| Exactitud de plazos | 88,2 % | 100 % | 100 % | **100 %** | 100 % |
| Rechazo correcto | 9/9 | 9/9 | 9/9 | **9/9** | — |
| Latencia p90 | 10,2 s | 11,2 s | 10,8 s | **12,3 s** | < 10 s |

En la ronda 4 las 44 preguntas son correctas en todas las categorías. La
única meta que no se cumple es la latencia: las respuestas generativas
tardan entre 6 y 16 s y dependen de la plataforma.

## Mejoras entre rondas

1. **Ronda 1 → 2:** tres trámites del TUPA salían mal por la búsqueda por
   palabras. La búsqueda pasó a comparar sin tildes ni guiones y por los
   primeros cinco caracteres de cada palabra.
2. **Ronda 2 → 3:** una respuesta atribuía un dato al artículo vecino
   (REG-17). La causa era el corte en fragmentos; ahora cada párrafo del
   Reglamento empieza con su artículo.
3. **Ronda 3 → 4:** en la prueba de usabilidad el agente elegía una ficha
   equivocada cuando dos tenían nombres parecidos. Ahora desempata por
   palabras completas y, si siguen empatadas, pregunta cuál.

Antes del banco completo hubo tres iteraciones de ajuste de instrucciones
y Topics con un subconjunto de 15 preguntas; están registradas en
`docs/bitacora.md`.

## Prueba de usabilidad

- **Participantes:** 9 (7 personal administrativo de la UCSM y 2
  estudiantes de pregrado), 4 en celular y 5 en computadora, en el agente
  publicado sin iniciar sesión.
- **Tareas y guion:** `eval/tareas_usabilidad.md`. Cuestionario SUS en
  Microsoft Forms (`eval/formulario_sus.md`), convertido con
  `eval/forms_to_sus.py` y calculado con `eval/compute_sus.py`.

**SUS promedio: 85,8** (mediana 85,0; mínimo 80,0; máximo 95,0; meta ≥ 68).

| Tarea | Éxito |
|---|---|
| T1. Desaprobar un curso tres veces | 9/9 |
| T2. Costo y plazo de la copia autenticada de la resolución del título | 4/9 |
| T3. Examen perdido por enfermedad (pregrado) | 5/9 |
| T4. Reserva de matrícula | 9/9 |
| T5. Pregunta fuera de alcance | 9/9 |

El error de T2 (ficha equivocada) se corrigió después de la prueba con la
desambiguación de fichas; en T3, cuatro participantes no recibieron el
código del trámite, aunque sí el plazo correcto. El detalle está en
`eval/usabilidad.md`.

## Analítica de Copilot Studio

En el periodo de pruebas hubo 187 sesiones por Direct Line: 138
resueltas, 30 abandonadas (sobre todo rechazos fuera de alcance, que era
lo esperado), 0 escaladas y 19 sin interacción. Copilot Studio no reportó
CSAT, temas ni calidad de respuestas por el bajo volumen; esas dimensiones
se cubren con la rúbrica y el SUS. El detalle está en `eval/analitica.md`.

## Pendiente

- Revisión de al menos 10 respuestas del banco por una segunda persona.
