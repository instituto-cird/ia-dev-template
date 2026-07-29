# AI_USAGE.md — Laboratorio 2

## Registro de decisiones asistidas por IA

### Entrada 001 - PRD

| Campo | Detalle |
|-------|---------|
| **Fecha** | 2026-07-21 |
| **Objetivo** | Crear un PRD  |
| **Herramienta y modelo** | Visual Studio Code con Copilot |
| **Contexto proporcionado** | Al final de la tabla |
| **Salida obtenida** | Se creo un documento en PRD_v1.md |
| **Problema detectado** | Ningun problema detectado que amerite una correccion en el prompt |
| **Cambio realizado por mí** | Ninguna |
| **Criterio o evidencia utilizada** | Genero solo 2 entidades, podria ser poca |
| **Pregunta todavía abierta** | 
- ¿Cuál es el conjunto exacto de valores permitidos para el estado de la transacción?
- ¿Qué campos adicionales deben mostrarse en la vista de resumen del historial?
- ¿Se debe filtrar por montos exactos, rangos de montos, o ambos?
- ¿Cuál es el tamaño de página por defecto y el máximo permitido? |
---
>PROMPT UTILIZADO

OBJETIVO
Preparar un primer borrador de PRD para el historial de transacciones de LegacyPay.

HECHOS APROBADOS
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Filtros mínimos: fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- Usar únicamente datos sintéticos del caso.

TAREA
Generá un PRD con estas secciones:
1. Visión y problema.
2. Alcance incluido y fuera de alcance.
3. Usuarios, entidades y reglas de negocio.
4. Historias de usuario con criterios de aceptación.
5. Restricciones no funcionales.
6. Preguntas abiertas.

RESTRICCIONES
- No inventes campos, SLA, volúmenes, reglas regulatorias ni políticas internas.
- Marcá como PREGUNTA ABIERTA todo dato no definido.
- Separá hechos proporcionados de propuestas.
- No conviertas automáticamente cada sustantivo en una entidad.
- No propongas cambios de arquitectura o dependencias sin justificarlos.

FORMATO
Markdown, sin explicaciones externas al documento.

---

### Entrada 002 - ERD

| Campo | Detalle |
|-------|---------|
| **Fecha** | 2026-07-28 |
| **Objetivo** | Crear un ERD  |
| **Herramienta y modelo** | Visual Studio Code con Copilot |
| **Contexto proporcionado** | Al final de la tabla |
| **Salida obtenida** | Se creo un documento en erd.md en docs/architecture/diagrams |
| **Problema detectado** | Ningun problema detectado que amerite una correccion en el prompt |
| **Cambio realizado por mí** | Ninguna |
| **Criterio o evidencia utilizada** | atributo merchant_id no coincide con la Entidad  |
| **Pregunta todavía abierta** | 
- ¿Cuál es el esquema exacto de los estados de transacción admitidos?
- ¿Cuál es el tamaño de página por defecto y los límites máximos de paginación?
- ¿Qué campos específicos de transacción deben mostrarse en el historial?
- ¿Se permite filtrar por montos exactos, rangos de monto, o ambos?
- ¿Cuál es el mecanismo de autorización de comercio autorizado (tokens, roles, scopes)?
- ¿Existen requisitos de rendimiento, disponibilidad o seguridad específicos para esta funcionalidad? |
---
>PROMPT UTILIZADO

Basado en el archivo PRD.md, generá un ERD lógico simplificado en Mermaid para la funcionalidad de historial de transacciones.

RESTRICCIONES
- No conviertas cada sustantivo en una tabla.
- No agregues campos, tablas ni relaciones no confirmadas sin marcarlas como propuesta.
- Incluí solo datos necesarios para filtros y visualización.
- No incluyas PAN completo, CVV ni datos de autenticación sensibles.
- No asumas que el ERD implementa por sí solo reglas de autorización, privacidad o concurrencia.

FORMATO
1. Bloque Mermaid.
2. Lista breve de supuestos.
3. Preguntas abiertas.
---