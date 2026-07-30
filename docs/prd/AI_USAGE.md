
# AI_USAGE — Lab 2

## Entrada 1 — PRD_v1 (borrador generado)

**Fecha:** 2026-07-30

**Objetivo:** Generar un primer PRD para el historial de transacciones.

**Herramienta y modelo:** GitHub Copilot Chat, revisión manual por auditor humano.

**Contexto proporcionado:** Requisitos del caso: pasarela B2B, comercio autorizado, consultas de hasta 90 días, filtros mínimos (fecha, estado, monto), paginación, prohibición de exponer datos completos de tarjeta ni datos de autenticación; usar solo datos sintéticos.

**Salida obtenida:** `PRD.md` — versión auditada que marca claramente: HECHOS APROBADOS, PROPUESTA IA, DECISIONES APROBADAS y PREGUNTAS ABIERTAS; añade historia de control de acceso y explicita datos sensibles prohibidos.

**Problema detectado:** El borrador incluía supuestos no aprobados y preguntas abiertas suficientes para decidir detalles de implementación.

**Cambio realizado por mí:**
- Moví elementos no aprobados fuera del alcance o los marqué como PREGUNTA ABIERTA.
- Añadí `Historia 5` para control de acceso (evitar que un comercio vea transacciones de otro).
- Explicitqué los datos sensibles prohibidos: PAN completo, CVV, credenciales de autenticación.
- Guardé la versión final como `docs/prd/PRD.md`.

**Criterio o evidencia utilizada:** Texto de `PRD_v1.md` y las restricciones iniciales provistas por el caso (no inventar campos, privacidad, 90 días, filtros mínimos).

**Pregunta todavía abierta:**
- PREGUNTA ABIERTA: ¿Qué estados de transacción deben estar disponibles como opciones de filtro?
- PREGUNTA ABIERTA: ¿Cómo se define el tamaño de página y la navegación de paginación?
- PREGUNTA ABIERTA: ¿Qué campos mínimos exactos debe mostrar cada transacción en la interfaz?

## Entrada 2 — Secuencia auditada

**Fecha:** 2026-07-30

**Objetivo:** Documentar y auditar el diagrama de secuencia para la consulta de historial de transacciones.

**Herramienta y modelo:** GitHub Copilot Chat, revisión manual por auditor humano.

**Contexto proporcionado:** Primera historia de usuario de `PRD.md`, filtros mínimos y paginación; diseño lógico del ERD con `MERCHANT` y `TRANSACTION`.

**Salida obtenida:** `docs/architecture/diagrams/sequence_historial.md` con diagrama Mermaid de secuencia, auditoría, supuestos y preguntas abiertas.

**Problema detectado:** Faltaba una entrada en AI_USAGE para la corrección de la secuencia.

**Cambio realizado por mí:**
- Añadí una nueva entrada en `AI_USAGE.md` para documentar la corrección de la secuencia.
- Confirmé que la autorización precede a la consulta de datos.
- Aseguré que el flujo alternativo de error y los participantes mínimos estuvieran presentes.

**Criterio o evidencia utilizada:** `PRD.md` historia 1 con criterios de aceptación, el ERD y las reglas de auditoría de la secuencia.

**Pregunta todavía abierta:**
- PREGUNTA ABIERTA: ¿El token/credenciales llegan en el mismo request que los filtros o hay un flujo de sesión separado?

## Entrada 3 — ADR de paginación

**Fecha:** 2026-07-30

**Objetivo:** Generar un borrador de ADR para decidir la estrategia de paginación del endpoint de historial de transacciones.

**Herramienta y modelo:** GitHub Copilot Chat, revisión manual por auditor humano.

**Contexto proporcionado:** La consulta puede crecer mucho por comercio, el endpoint debe ser auditable, la consulta debe ser paginada, sin benchmarks ni SLA no aprobados.

**Salida obtenida:** `docs/architecture/decisions/0001-paginacion.md` con Contexto, Alternativas, Decisión propuesta, Consecuencias positivas y negativas, Evidencia pendiente y Condición de revisión.

**Problema detectado:** Ninguna alternativa debe ser redundante; el ADR necesita consecuencias honestas y evidencia faltante clara.

**Cambio realizado por mí:**
- Definí tres alternativas distintas: offset, cursor/seek y híbrida.
- Propuse la alternativa B (cursor/seek) como la estrategia preferida.
- Añadí consecuencias negativas honestas y evidencia pendiente.
- Incluí una condición de revisión concreta.

**Criterio o evidencia utilizada:** Requisitos del prompt del ADR y los criterios de rendimiento, implementación, experiencia de usuario, costo de cambio y evidencia pendiente.

**Pregunta todavía abierta:**
- PREGUNTA ABIERTA: ¿Qué requisitos de auditoría exactos deben guiar la trazabilidad del cursor?

## Entrada 4 — Sugerencia aceptada/modificada

**Fecha:** 2026-07-30

**Sugerencia:** Usar paginación basada en cursor/seek en lugar de offset tradicional.

**Resultado:** Aceptada con modificación.

**Por qué:** Cursor/seek ofrece mejor rendimiento bajo crecimiento de datos y orden consistente, lo que se alinea con el criterio de auditoría y con la necesidad de consultas grandes por comercio.

**Modificación:** Se mantiene pendiente la evidencia de datos reales y la decisión final sobre orden adicional; la sugerencia se documentó como preferida pero no definitiva.

**Consecuencia:** La implementación inicial puede priorizar cursor/seek, pero se revisará con métricas de latencia y requisitos de auditoría reales.
