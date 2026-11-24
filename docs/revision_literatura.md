# Revisión de literatura

## 1. Tipos de chatbot

**Basados en reglas.** Desde ELIZA (Weizenbaum, 1966), los primeros
chatbots respondieron con patrones y plantillas. Son predecibles y baratos,
pero solo atienden lo previsto por el diseñador. AIML, usado en chatbots
universitarios de preguntas frecuentes (Ranoliya et al., 2017), es un
ejemplo de esta familia.

**Basados en recuperación.** Seleccionan la respuesta más parecida de una
base de preguntas y respuestas o de documentos mediante similitud léxica o
semántica (Adamopoulou & Moussiades, 2020). Garantizan que el texto
provenga de la fuente, pero no redactan respuestas nuevas.

**Generativos.** Los modelos de lenguaje grandes (LLM) redactan respuestas
fluidas a partir de su entrenamiento, pero pueden "alucinar", es decir,
producir contenido no sustentado en ninguna fuente (Ji et al., 2023). En un
dominio normativo, donde un monto o un plazo equivocado tiene
consecuencias, esto es un riesgo central.

**Generación aumentada por recuperación (RAG).** Combina ambos enfoques:
recupera fragmentos relevantes de una base documental y los entrega al
modelo como contexto para generar la respuesta (Lewis et al., 2020). Reduce
las alucinaciones, permite citar la fuente y actualizar el conocimiento sin
reentrenar el modelo (Gao et al., 2023). Es la arquitectura que usan las
funciones de "respuestas generativas sobre conocimiento" de las plataformas
comerciales actuales.

## 2. Plataformas de desarrollo

Las plataformas *low-code* permiten construir chatbots sin programar la
recuperación ni la interfaz:

- **Microsoft Copilot Studio:** agentes con orquestación generativa,
  conocimiento sobre archivos y sitios, Topics diseñados en un lienzo
  visual, Adaptive Cards, analítica y publicación en sitio web y Teams
  (Microsoft, 2026).
- **Google Dialogflow CX (Conversational Agents):** flujos y páginas como
  máquina de estados, *playbooks* generativos y *data stores* para RAG
  (Google Cloud, 2026).
- **Botpress:** editor visual de flujos, base de conocimiento con
  recuperación y capa gratuita limitada (Botpress, 2026).
- **Rasa:** marco de código abierto para chatbots basados en intenciones;
  requiere programación y alojamiento propio.

El diseño conversacional en estas plataformas sigue un mismo patrón:
intenciones (qué quiere el usuario), entidades (datos de la consulta),
gestión del diálogo (qué preguntar o responder) y respuestas, con
mecanismos de desambiguación y de *fallback* para lo no reconocido
(Adamopoulou & Moussiades, 2020; Kuhail et al., 2023).

## 3. Chatbots en educación

Las revisiones sistemáticas muestran que los chatbots educativos se usan
sobre todo para enseñanza, apoyo administrativo y orientación al
estudiante (Okonkwo & Ade-Ibijola, 2021; Wollny et al., 2021). Kuhail et
al. (2023) señalan que la mayoría usa interfaces web, diálogo guiado por el
chatbot y evaluación con cuestionarios de usabilidad, pero con muestras
pequeñas. Wollny et al. (2021) destacan la falta de evaluaciones
rigurosas y la necesidad de medir la exactitud además de la satisfacción.

## 4. Trabajos relacionados

| Trabajo | Dominio | Enfoque | Plataforma / técnica | Evaluación |
|---|---|---|---|---|
| Ranoliya et al. (2017) | Preguntas frecuentes de una universidad (India) | Reglas + recuperación | AIML y análisis semántico latente (LSA) | Ejemplos de conversación |
| Ho et al. (2018) | Elección de cursos electivos (Hong Kong) | Intenciones + base de cursos | IBM Watson Conversation, Telegram | Encuesta de facilidad de uso |
| Hien et al. (2018) | Apoyo administrativo y de aprendizaje (FIT-EBot, Vietnam) | Intenciones + base de conocimiento | Procesamiento de lenguaje natural propio | Pruebas con estudiantes |
| Clarizia et al. (2018) | Apoyo a estudiantes (Italia) | Recuperación con ontologías de dominio | PLN + ontologías | Campaña experimental con estudiantes |
| Neupane et al. (2024) | Recursos de Mississippi State University (BarkPlug v.2) | RAG sobre datos institucionales | LLM + recuperación | RAGAS (0,96) y SUS |

**Brechas que aborda este proyecto:**

1. Los trabajos basados en reglas o intenciones (2017–2018) cubren
   preguntas frecuentes, no el texto normativo completo; aquí se indexan los
   159 artículos y las 63 fichas del TUPA.
2. Pocos trabajos combinan la norma (qué dice) con el trámite (cómo, cuánto,
   cuándo); aquí ambas fuentes se integran y se citan.
3. Los montos y plazos son datos críticos: se muestran desde una tabla
   estructurada (exacta por construcción) y no solo desde la generación.
4. Se evalúa con exactitud de fuente y montos, rechazo fuera de alcance y
   SUS (Brooke, 1996; Bangor et al., 2008), siguiendo la recomendación de
   medir tanto exactitud como usabilidad.

## 5. Evaluación de usabilidad

La *System Usability Scale* (SUS) es un cuestionario de 10 ítems con escala
de 5 puntos que produce un puntaje de 0 a 100 (Brooke, 1996). Bangor et al.
(2008) ubican el promedio alrededor de 68 y proponen interpretarlo con
adjetivos (por ejemplo, "bueno" por encima de ~71); por eso la meta del
proyecto es SUS ≥ 68.

## Referencias

Adamopoulou, E., & Moussiades, L. (2020). Chatbots: History, technology,
and applications. *Machine Learning with Applications, 2*, 100006.
https://doi.org/10.1016/j.mlwa.2020.100006

Bangor, A., Kortum, P. T., & Miller, J. T. (2008). An empirical evaluation
of the System Usability Scale. *International Journal of Human–Computer
Interaction, 24*(6), 574–594. https://doi.org/10.1080/10447310802205776

Botpress. (2026). *Botpress documentation*. https://botpress.com/docs

Brooke, J. (1996). SUS: A "quick and dirty" usability scale. En P. W.
Jordan, B. Thomas, B. A. Weerdmeester & I. L. McClelland (Eds.),
*Usability evaluation in industry* (pp. 189–194). Taylor & Francis.

Clarizia, F., Colace, F., Lombardi, M., Pascale, F., & Santaniello, D.
(2018). Chatbot: An education support system for student. En *Cyberspace
Safety and Security (CSS 2018)*, Lecture Notes in Computer Science (Vol.
11161, pp. 291–302). Springer.
https://doi.org/10.1007/978-3-030-01689-0_23

Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J.,
Wang, M., & Wang, H. (2023). *Retrieval-augmented generation for large
language models: A survey* (arXiv:2312.10997). arXiv.
https://doi.org/10.48550/arXiv.2312.10997

Google Cloud. (2026). *Conversational Agents (Dialogflow CX)
documentation*. https://cloud.google.com/dialogflow/cx/docs

Hien, H. T., Cuong, P.-N., Nam, L. N. H., Nhung, H. L. T. K., & Thang, L. D.
(2018). Intelligent assistants in higher-education environments: The
FIT-EBot, a chatbot for administrative and learning support. En
*Proceedings of the Ninth International Symposium on Information and
Communication Technology (SoICT 2018)* (pp. 69–76). ACM.
https://doi.org/10.1145/3287921.3287937

Ho, C. C., Lee, H. L., Lo, W. K., & Lui, K. F. A. (2018). Developing a
chatbot for college student programme advisement. En *2018 International
Symposium on Educational Technology (ISET)* (pp. 52–56). IEEE.

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., Ishii, E., Bang, Y.
J., Madotto, A., & Fung, P. (2023). Survey of hallucination in natural
language generation. *ACM Computing Surveys, 55*(12), 1–38.
https://doi.org/10.1145/3571730

Kuhail, M. A., Alturki, N., Alramlawi, S., & Alhejori, K. (2023).
Interacting with educational chatbots: A systematic review. *Education and
Information Technologies, 28*(1), 973–1018.
https://doi.org/10.1007/s10639-022-10747-1

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D.
(2020). Retrieval-augmented generation for knowledge-intensive NLP tasks.
*Advances in Neural Information Processing Systems, 33*, 9459–9474.

Microsoft. (2026). *Microsoft Copilot Studio documentation*.
https://learn.microsoft.com/microsoft-copilot-studio/

Neupane, S., Hossain, E., Keith, J., Tripathi, H., Ghiasi, F., Golilarz,
N. A., Amirlatifi, A., Mittal, S., & Rahimi, S. (2024). *From questions to
insightful answers: Building an informed chatbot for university resources*
(arXiv:2405.08120). arXiv. https://doi.org/10.48550/arXiv.2405.08120

Okonkwo, C. W., & Ade-Ibijola, A. (2021). Chatbots applications in
education: A systematic review. *Computers and Education: Artificial
Intelligence, 2*, 100033. https://doi.org/10.1016/j.caeai.2021.100033

Ranoliya, B. R., Raghuwanshi, N., & Singh, S. (2017). Chatbot for
university related FAQs. En *2017 International Conference on Advances in
Computing, Communications and Informatics (ICACCI)* (pp. 1525–1530). IEEE.
https://doi.org/10.1109/ICACCI.2017.8126057

Universidad Católica de Santa María. (2026a). *Texto Único Ordenado del
Reglamento de Estudiantes de la UCSM* (Resolución N° 9814-CU-2026).
https://www.ucsm.edu.pe/wp-content/uploads/documentos/reglamentos/RES_9814-CU-2026.pdf

Universidad Católica de Santa María. (2026b). *Texto Único de
Procedimientos Administrativos (TUPA)* (Resolución N° 9888-CU-2026).
https://www.ucsm.edu.pe/wp-content/uploads/documentos/reglamentos/RES_9888-CU-2026-TUPA.pdf

Weizenbaum, J. (1966). ELIZA—A computer program for the study of natural
language communication between man and machine. *Communications of the
ACM, 9*(1), 36–45. https://doi.org/10.1145/365153.365168

Wollny, S., Schneider, J., Di Mitri, D., Weidlich, J., Rittberger, M., &
Drachsler, H. (2021). Are we there yet? A systematic literature review on
chatbots in education. *Frontiers in Artificial Intelligence, 4*, 654924.
https://doi.org/10.3389/frai.2021.654924
