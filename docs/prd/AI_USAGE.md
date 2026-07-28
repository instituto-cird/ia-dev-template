# AI Usage Log — Laboratorio 2 (LegacyPay)

Este documento registra la trazabilidad y la auditoría humana aplicada a cada artefacto de especificación y arquitectura generado con la asistencia de Inteligencia Artificial.

---

## Entrada 1 · 21-jul-2026 · Documento de Requisitos del Producto (PRD)

**Objetivo:** Generar un primer borrador de PRD para la funcionalidad de Historial de Transacciones de LegacyPay.

**Herramienta y modelo:** GitHub Copilot / LLM Assistant.

**Contexto proporcionado:** 
- Prompt 1 estructurado con hechos aprobados (LegacyPay como pasarela B2B, rango de 90 días, filtros por fecha, estado y monto, paginación obligatoria, prohibición de exponer PAN completo o CVV, datos sintéticos).

**Salida obtenida:** 
- Archivo `PRD_v1.md` estructurado con Visión, Alcance, Usuarios, Entidades, Historias de Usuario (HU-01) y Preguntas Abiertas.

**Problema detectado:** 
1. **Alucinación de alcance:** La IA incluyó la exportación de resultados a archivos CSV (CA-01.4 en v1) como un criterio de aceptación del alcance actual.
2. **Sobre-diseño de entidades:** La IA incluyó "Filtro" como una entidad del dominio en la sección de datos.

**Cambio realizado por mí:** 
1. Eliminé la exportación a CSV de las historias de usuario y la moví explícitamente a la sección "Fuera de Alcance" en `PRD.md`.
2. Eliminé "Filtro" de la lista de entidades de base de datos, aclarando que se trata de parámetros de consulta de la petición HTTP.
3. Formateé las preguntas abiertas y explicité los supuestos de negocio.

**Evidencia o criterio utilizado:** 
- El pedido de negocio de LegacyPay especifica únicamente la consulta paginada en pantalla con filtros mínimos. La exportación externa requiere infraestructura y decisiones no aprobadas en la v1.

**Pregunta todavía abierta:** 
- ¿Existen roles diferenciados dentro del comercio (ej. Operador vs Administrador) con permisos de lectura restringidos?

---

## Entrada 2 · 21-jul-2026 · Modelo Entidad-Relación (ERD)

**Objetivo:** Generar un modelo entidad-relación lógico simplificado en formato Mermaid a partir de `PRD.md`.

**Herramienta y modelo:** GitHub Copilot / LLM Assistant.

**Contexto proporcionado:** 
- Prompt 2 con restricciones de no convertir sustantivos simples en tablas, no incluir PAN completo ni CVV, e incluir supuestos explícitos.

**Salida obtenida:** 
- Diagrama Mermaid inicial propuesto en `erd.md` con entidades `COMERCIO`, `TRANSACCION`, `ESTADO_TRANSACCION` y `EXPORTACION`.

**Problema detectado:** 
1. **Entidad fuera de alcance:** La IA generó la tabla `EXPORTACION` derivándola de la alucinación previa del PRD_v1.
2. **Normalización excesiva:** La IA aisló el estado en la tabla `ESTADO_TRANSACCION`, agregando complejidad innecesaria para un atributo enumerable simple.

**Cambio realizado por mí:** 
1. Eliminé por completo la entidad `EXPORTACION`.
2. Convertí `estado_transaccion` en un atributo tipo cadena/enum dentro de la tabla `TRANSACCION`.
3. Verifiqué que solo se exponga `masked_pan` y redacté los supuestos de cardinalidad `1:N`.

**Evidencia o criterio utilizado:** 
- El principio de diseño ágil y las instrucciones del prompt prohíben sobre-diseños de base de datos para funcionalidades básicas de consulta filtrada.

**Pregunta todavía abierta:** 
- ¿Se requiere una entidad separada para el manejo de reembolsos/devoluciones o se tratarán como un estado de transacción en la v1?

