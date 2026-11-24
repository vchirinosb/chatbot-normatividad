# Bitácora del proyecto

## Verificación de acceso a Copilot Studio (tarea 1.1)

| Campo | Valor |
|---|---|
| Fecha | 2026-11-24 |
| URL | https://copilotstudio.microsoft.com |
| Cuenta | Cuenta institucional UCSM (Entra ID) |
| Inicio de sesión | Correcto |
| Entorno | "Universidad Católica de Santa María (default)" |
| Versión de la plataforma | `release/2026.11.12.2` (nueva experiencia de Copilot Studio) |
| Indicador en la página de inicio | "Uses Copilot Credits" |
| Creación de agente | **Fallida**: al guardar el agente vacío "Prueba acceso UCSM" la plataforma mostró *"You don't have permission to create agents. Ask your admin to grant you the right role, then try again."* con el detalle *"User license not found"* |
| Tipo de acceso | Ninguno: la cuenta no tiene licencia de Copilot Studio ni rol de creador en el entorno predeterminado |
| Vencimiento | No aplica |
| "No authentication" / *Demo website* | No verificable: no se pudo crear ni guardar el agente |
| Opciones vistas en el menú de cuenta | Novedades, Solutions, experiencia clásica, Power Platform Admin Center, Learn, detalles de sesión. No aparece una opción de prueba gratuita |

**Resultado:** acceso **bloqueado**. Según la tarea 1.1 y el requisito
"Verificación de acceso a la plataforma" de `copilot-studio-agent`, se
detienen los grupos 5 y 6 hasta que el autor decida cómo continuar.

**Alternativas identificadas:**
1. Solicitar a la Dirección de Informática de la UCSM una licencia de Copilot
   Studio, o el rol de creador en un entorno, y el permiso de publicar sin
   autenticación.
2. Intentar la prueba gratuita de Copilot Studio con la cuenta UCSM. El
   inquilino puede bloquear el registro de autoservicio y requiere aceptar
   términos.
3. Usar un inquilino propio de prueba o desarrollador de Microsoft 365, con
   una cuenta nueva creada por el autor.
4. Cambiar de plataforma: Botpress (3,70 en la matriz) o RAG propio con Ollama
   (3,50).

### Segundo intento con otra cuenta (pendiente)

El autor decidió continuar con otra cuenta de Copilot Studio (alternativa
3). Al iniciar sesión con ella se registrará aquí: fecha, tipo de cuenta
(prueba, licencia o pago por uso), vencimiento, si se pudo crear el agente y
si el *Demo website* admite "No authentication". La prueba de 30 días no
permite publicar en canales; si la cuenta es de pago por uso, se estima un
gasto de US$ 20–50 para el desarrollo y la evaluación (ver
`docs/matriz_plataformas.md`, escenario C).

## Consulta de licencias (tarea 2.3), 2026-11-24

- Copilot Studio: prueba sin publicación; pago por uso a US$ 0,01 por
  *Copilot Credit* (clásica = 1, generativa = 2) con suscripción de Azure;
  paquete de US$ 200/mes por 25 000 créditos.
- Botpress Cloud: plan Free de US$ 0 con 100 conversaciones/mes sin
  excedentes (el emulador también consume); Plus de US$ 150/mes (anual).
- Dialogflow CX (Conversational Agents): créditos de prueba de US$ 600
  (flows) y US$ 1 000 (generativo) por 1 año; US$ 0,007 por solicitud de
  chat (flows) y US$ 0,012 (playbooks); requiere facturación en GCP.

## Horas por grupo de tareas

El autor completa la columna de horas al cerrar cada grupo.

| Grupo | Horas | Notas |
|---|---|---|
| 1. Configuración y verificación de acceso | | 1.2–1.4 cerradas el 2026-11-24; 1.1 pendiente con la nueva cuenta |
| 2. Alcance, revisión y matriz | | Cerrado el 2026-11-24 |
| 3. Protocolo conversacional | | 3.1–3.3 cerradas el 2026-11-24; falta la validación con usuarios (3.4) |
| 4. Preparación del corpus | | Cerrado el 2026-11-24 (28 pruebas OK, build determinista) |
| 5. Construcción del agente | | |
| 6. Entrenamiento, publicación y versionado | | |
| 7. Evaluación | | |
| 8. Paper | | |
