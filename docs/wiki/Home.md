# Chatbot de normatividad estudiantil UCSM

Asistente conversacional que orienta a los estudiantes de la Universidad
Católica de Santa María (UCSM) sobre dos documentos oficiales:

- el **Texto Único Ordenado del Reglamento de Estudiantes** (Res. N°
  9814-CU-2026): qué dice la norma;
- el **Texto Único de Procedimientos Administrativos (TUPA)** (Res. N°
  9888-CU-2026): cómo, cuánto, cuándo y dónde se tramita.

El agente está construido en **Microsoft Copilot Studio** y publicado en el
canal *Demo website*, sin inicio de sesión. Cada respuesta cita el artículo
del Reglamento o el código del procedimiento del TUPA.

> **Aviso:** es un asistente de orientación, no un canal oficial de la
> UCSM. El texto vinculante es el de los documentos publicados en
> https://ucsm.edu.pe/normatividad/.

![Bienvenida del agente](images/agente_bienvenida.png)

## Resultados principales

| Indicador | Resultado | Meta |
|---|---|---|
| Banco de 44 preguntas (ronda final) | 44 correctas, 0 alucinadas | ≥ 80 % correctas o parciales, 0 alucinadas |
| Exactitud de montos y plazos del TUPA | 17/17 y 17/17 | 100 % |
| Rechazo de preguntas fuera de alcance o sin respuesta | 9/9 | — |
| Latencia p90 | 12,3 s | < 10 s (no cumple) |
| SUS (9 participantes) | 85,8 | ≥ 68 |

## Páginas

| Página | Contenido |
|---|---|
| [Alcance y limitaciones](Alcance-y-limitaciones) | Usuarios, temas cubiertos, temas fuera de alcance y limitaciones |
| [Arquitectura](Arquitectura) | Cómo se combinan el corpus procesado y Copilot Studio |
| [Corpus](Corpus) | Documentos fuente, limpieza, segmentación y campos del TUPA |
| [Protocolo conversacional](Protocolo-conversacional) | Intenciones, flujo, desambiguación y formato de respuesta |
| [Agente en Copilot Studio](Agente-en-Copilot-Studio) | Instrucciones, conocimiento, Topics, publicación y versiones |
| [Evaluación](Evaluacion) | Banco de preguntas, métricas, rondas, usabilidad y analítica |
| [Glosario](Glosario) | Términos de Copilot Studio, del corpus y de la evaluación |
