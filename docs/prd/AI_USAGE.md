
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
