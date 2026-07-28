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

---

## Entrada 3 · 21-jul-2026 · Diagrama de Secuencia

**Objetivo:** Generar el diagrama de secuencia Mermaid para la consulta paginada de historial de transacciones basada en `PRD.md` (HU-01).

**Herramienta y modelo:** GitHub Copilot / LLM Assistant.

**Contexto proporcionado:** 
- Prompt 3 con lista explícita de participantes (Comercio, API, Auth, Service, DB), exigencia de flujo feliz, consulta paginada y al menos un flujo alternativo de error.

**Salida obtenida:** 
- Diagrama Mermaid inicial propuesto en `sequence_historial.md` con flujo síncrono lineal sin validación explícita de seguridad previa.

**Problema detectado:** 
1. **Omisión de componente de seguridad:** La IA conectó la API directamente con el servicio de base de datos sin consultar al componente de `Autorización`.
2. **Falta de flujos de excepción:** El modelo únicamente graficó el camino feliz (200 OK), ignorando la validación del límite de 90 días.

**Cambio realizado por mí:** 
1. Reordené el diagrama para incluir el `Servicio de Autorización` como paso obligatorio antes de consultar el servicio de dominio.
2. Agregué los bloques alternativos (`alt / else`) para capturar las respuestas de error HTTP 401 (token inválido) y HTTP 400 (exceso del rango de 90 días).
3. Aseguré que los nombres de los atributos retornados coincidan con el modelo `erd.md`.

**Evidencia o criterio utilizado:** 
- Principio de Arquitectura Segura (Security by Design) y la regla RN-01 definida en `PRD.md`.

**Pregunta todavía abierta:** 
- ¿Cuál es la estrategia de manejo de timeouts cuando la base de datos tarda en responder consultas con filtros amplios?

---

## Entrada 4 · 21-jul-2026 · Registro de Decisión de Arquitectura (ADR)

**Objetivo:** Elaborar el borrador del ADR 0001 para seleccionar la estrategia de paginación del historial de transacciones en LegacyPay.

**Herramienta y modelo:** GitHub Copilot / LLM Assistant.

**Contexto proporcionado:** 
- Prompt 4 con la restricción explícita de no inventar SLAs ni benchmarks no aprobados y evaluar alternativas bajo criterios de rendimiento, facilidad de implementación, UX y costo de cambio.

**Salida obtenida:** 
- Borrador inicial en `0001-paginacion.md` recomendando Keyset Pagination e inventando un SLA de respuesta menor a 50 ms y benchmarks no realizados.

**Problema detectado:** 
1. **Alucinación de métricas:** La IA inventó métricas de rendimiento y SLAs que no fueron aprobados ni probados en el proyecto.
2. **Subestimación de fricción B2B:** El modelo priorizó la teoría de rendimiento sobre la usabilidad e integración práctica para los comercios en la v1.

**Cambio realizado por mí:** 
1. Eliminé todos los benchmarks e inventos de SLA.
2. Cambié la decisión propuesta a **Paginación Basada en Offset** acotada a `page_size = 100` por facilidad de integración B2B y acotamiento a 90 días.
3. Explicité las consecuencias negativas honestas (posible degradación en páginas muy profundas) y añadí la sección de "Evidencia Pendiente" (pruebas de carga) y las condiciones de revisión.

**Evidencia o criterio utilizado:** 
- Estándares del formato ADR profesional y la restricción explícita del prompt de no asumir SLAs sin evidencia previa.

**Pregunta todavía abierta:** 
- ¿Qué porcentaje de consultas efectivas de los comercios llegan a requerir una paginación superior a la página 50?



