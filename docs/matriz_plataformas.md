# Matriz de selección de plataforma

Condiciones de licencia consultadas el 24 de noviembre de 2026. Los puntajes
se recalculan con:

```bash
.venv/bin/python scripts/compute_platform_matrix.py
```

Las tablas de abajo son la salida de ese script (escala 1–5; puntaje
ponderado = Σ peso × puntaje / 100).

## Condiciones de licencia verificadas

| Plataforma | Capa gratuita / prueba | Pago | Implicancia para el proyecto |
|---|---|---|---|
| Microsoft Copilot Studio | Prueba de 30 días (no permite publicar en canales) o licencia del inquilino | Pago por uso: US$ 0,01 por *Copilot Credit* (respuesta clásica = 1 crédito, generativa = 2); requiere suscripción de Azure y cuenta de trabajo o estudiante. Paquete: US$ 200/mes por 25 000 créditos | Con licencia institucional el costo es 0. Con una cuenta nueva de pago por uso, el gasto estimado para el desarrollo y la evaluación es de US$ 20–50 |
| Botpress Cloud | Plan Free US$ 0 con 100 conversaciones/mes, sin excedentes (las del emulador también cuentan) | Plus: US$ 150/mes con facturación anual | Alcanza para el desarrollo, pero se queda corto para la evaluación (≥ 40 preguntas + 5 usuarios + iteraciones) |
| Dialogflow CX (Conversational Agents) | Crédito de prueba de US$ 600 (flows) y US$ 1 000 (funciones generativas), válido 1 año; requiere proyecto GCP con facturación | US$ 0,007 por solicitud de chat (flows), US$ 0,012 (playbooks) | Gratuito en la práctica, pero exige tarjeta y configurar GCP |
| RAG propio (Python + Ollama) | Gratuito (modelos locales) | — | Sin costo, pero no es low-code y el link público es temporal (túnel) |

Fuentes: páginas oficiales de precios de Microsoft Copilot Studio, Botpress
y Google Cloud Conversational Agents; detalle de la búsqueda en
`docs/bitacora.md`.

## Matriz ponderada y análisis de sensibilidad

### A. Low-code (elegido)

| Criterio (peso) | Dialogflow CX | Copilot Studio | Botpress Cloud | RAG Python + Ollama |
|---|---|---|---|---|
| Costo para el autor (25 %) | 2 | 3 | 4 | 5 |
| RAG gestionado sobre documentos con citas (20 %) | 4 | 4 | 3 | 5 |
| Desarrollo low-code y protocolo visual (20 %) | 4 | 5 | 4 | 1 |
| Publicación web pública (15 %) | 3 | 3 | 4 | 3 |
| Calidad en español (10 %) | 4 | 4 | 4 | 4 |
| Analítica y evaluación integradas (10 %) | 4 | 5 | 3 | 2 |
| **Puntaje ponderado** | 3,35 | **3,90** | 3,70 | 3,50 |

### B. Costo y control

| Criterio (peso) | Dialogflow CX | Copilot Studio | Botpress Cloud | RAG Python + Ollama |
|---|---|---|---|---|
| Costo para el autor (30 %) | 2 | 3 | 4 | 5 |
| RAG gestionado sobre documentos con citas (20 %) | 4 | 4 | 3 | 5 |
| Desarrollo low-code y protocolo visual (5 %) | 4 | 5 | 4 | 1 |
| Publicación web pública (15 %) | 3 | 3 | 4 | 3 |
| Calidad en español (10 %) | 4 | 4 | 4 | 4 |
| Analítica y evaluación integradas (5 %) | 4 | 5 | 3 | 2 |
| Control y reproducibilidad (15 %) | 2 | 2 | 2 | 5 |
| **Puntaje ponderado** | 2,95 | 3,35 | 3,45 | **4,25** |

### C. Igual que A, Copilot Studio con pago por uso (costo = 2)

| Criterio (peso) | Dialogflow CX | Copilot Studio | Botpress Cloud | RAG Python + Ollama |
|---|---|---|---|---|
| Costo para el autor (25 %) | 2 | 2 | 4 | 5 |
| RAG gestionado sobre documentos con citas (20 %) | 4 | 4 | 3 | 5 |
| Desarrollo low-code y protocolo visual (20 %) | 4 | 5 | 4 | 1 |
| Publicación web pública (15 %) | 3 | 3 | 4 | 3 |
| Calidad en español (10 %) | 4 | 4 | 4 | 4 |
| Analítica y evaluación integradas (10 %) | 4 | 5 | 3 | 2 |
| **Puntaje ponderado** | 3,35 | 3,65 | **3,70** | 3,50 |

## Interpretación

- **Escenario A (criterio del autor):** se prioriza el desarrollo low-code y
  las capacidades integradas porque la actividad pide construir el chatbot
  en una plataforma de desarrollo de chatbots. Copilot Studio gana
  (3,90) por el lienzo de Topics, las Adaptive Cards, la analítica con
  encuesta de satisfacción y el conocimiento sobre documentos con citas.
- **Escenario B (costo y control):** si pesan más el costo y la
  reproducibilidad, gana el RAG propio con Ollama (4,25) y Copilot Studio
  queda tercero (3,35). Nota: design.md (D1) indicaba 2,50 para Copilot en
  este escenario; con los puntajes de la tabla el valor recalculado es 3,35.
- **Escenario C (cuenta nueva con pago por uso):** si la cuenta de Copilot
  Studio no tiene licencia y se paga por uso, su puntaje de costo baja a 2
  y Botpress Cloud pasa adelante por 0,05 (3,70 frente a 3,65). La
  diferencia es menor que la incertidumbre de los puntajes, por lo que la
  elección depende del tipo de cuenta: con licencia o prueba que permita
  publicar se mantiene Copilot Studio; sin ella, Botpress es una
  alternativa equivalente.
- **Fuera de la tabla:** la API de OpenAI (sin capa gratuita y sin
  interfaz low-code) y Rasa (sin RAG nativo ni hosting gratuito).

## Decisión

Se mantiene **Microsoft Copilot Studio** con la cuenta alternativa del autor,
condicionada a la verificación de la tarea 1.1 (crear un agente y publicar
en *Demo website* sin autenticación). El tipo de licencia y su vencimiento
se registran en `docs/bitacora.md`, y el paper presenta los tres
escenarios.
