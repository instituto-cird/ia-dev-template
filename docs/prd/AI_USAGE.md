# AI_USAGE — Lab 2

## Entrada 1 — PRD

**Fecha:** 2026-09-01

**Objetivo:** Registrar la experiencia de generación y auditoría del Product Requirements Document (PRD) para Lab 2.

**Herramienta y modelo:** Copilot en el entorno de desarrollo; modelo AI asistente interno para generación y revisión de requisitos.

**Contexto proporcionado:** Documento de PRD en desarrollo dentro del repositorio `ia-dev-template`; alcance centrado en la funcionalidad de historial de transacciones y el diseño de arquitectura asociado.

**Salida obtenida:** Se generó una propuesta inicial del PRD con alcance, historias de usuario, criterios de aceptación y restricciones. La IA sugirió varias descripciones de negocio y algunos elementos de solución que requerían revisión.

**Problema detectado:** La IA propuso funcionalidades fuera del alcance aprobado y definiciones demasiado rígidas sobre datos, roles y responsabilidades. También se arriesgó a convertir atributos simples en entidades nuevas sin evidencia en el PRD.

**Cambio realizado por mí:** Eliminé sugerencias no aprobadas, mantuve el alcance centrado en historial de transacciones y dejé abiertas las decisiones que aún no estaban definidas por el negocio.

**Criterio o evidencia utilizada:** Comparé la propuesta con el alcance del Lab 2, la documentación del repositorio y la regla de no inventar campos, reglas regulatorias o políticas internas sin confirmar.

**Pregunta todavía abierta:** ¿Qué roles específicos están autorizados para consultar y filtrar el historial de transacciones, y cómo deben documentarse esos permisos?

### Ejemplo de entrada útil
Copilot añadió exportación a CSV y otros elementos no aprobados. Eliminé esa funcionalidad y dejé una pregunta abierta sobre los roles autorizados porque el caso no definía con precisión la regla de negocio.

## Entrada 2 — ERD

**Fecha:** 2026-09-01

**Objetivo:** Validar y ajustar el ERD lógico para el historial de transacciones sin introducir entidades o campos no confirmados.

**Herramienta y modelo:** Copilot + revisión manual del diagrama Mermaid y del PRD.

**Contexto proporcionado:** Se solicitó un ERD simplificado para la funcionalidad de historial de transacciones con restricciones claras: no inventar tablas, no incluir datos sensibles, solo campos útiles para filtros y visualización.

**Salida obtenida:** Un primer ERD con `TRANSACTION` y `MERCHANT`, con relaciones básicas y supuestos explícitos.

**Problema detectado:** La IA había intentado incluir campos o atributos de metadata no confirmados, como `created_at` y nombres de comerciante, sin indicar claramente que eran propuestas.

**Cambio realizado por mí:** Reforcé la formulación del diagrama para dejar `created_at` como propuesta y reducir la entidad `MERCHANT` a una referencia mínima. También añadí una auditoría explícita para documentar qué elementos eran confirmados y cuáles pendientes.

**Criterio o evidencia utilizada:** Validación del alcance del PRD, la regla de evitar entidades no justificadas y la prueba de que el diagrama Mermaid renderiza con sintaxis correcta.

**Pregunta todavía abierta:** ¿El PRD confirma el uso de `merchant_id` como referencia única o requiere una entidad de comerciante con más atributos para la consulta?

## Entrada 3 — Secuencia

**Fecha:** 2026-09-01

**Objetivo:** Generar y auditar un diagrama de secuencia para la consulta de historial de transacciones y ajustar el flujo con validación y manejo de error.

**Herramienta y modelo:** Copilot para generar Mermaid; auditoría manual del orden de mensajes y participantes.

**Contexto proporcionado:** Debía basarse en la primera historia de usuario y sus criterios de aceptación del PRD, con participantes mínimos: comercio/usuario autorizado, API, validador, servicio y repositorio/base de datos.

**Salida obtenida:** Un diagrama de secuencia con validación de identidad, validación de filtros, consulta paginada, respuesta correcta y flujo de error alternativo.

**Problema detectado:** La IA inicial no dejaba claro el orden de autorización antes de consultar ni la diferenciación entre validación de filtros y error de negocio.

**Cambio realizado por mí:** Ajusté la secuencia para que la autorización ocurra antes de la consulta, agregué validación de filtros y dejé un bloque `alt` explícito para errores de validación y de autorización. También mantuve la estructura sin servicios externos inventados.

**Criterio o evidencia utilizada:** Revisión del flujo de la historia de usuario, consistencia entre actores y comparación con el ERD para asegurar que los datos consultados correspondan a la entidad `TRANSACTION`.

**Pregunta todavía abierta:** ¿Debe el endpoint devolver un error de negocio específico para comercio no autorizado o basta con una respuesta 403/400 con mensaje claro?

## Entrada 4 — ADR

**Fecha:** 2026-09-01

**Objetivo:** Redactar un ADR provisional para decidir la estrategia de paginación del historial de transacciones.

**Herramienta y modelo:** Copilot + revisión de criterios del caso de uso y de la arquitectura esperada.

**Contexto proporcionado:** El endpoint puede crecer mucho por comercio, requiere trazabilidad, y la consulta debe ser paginada sin inventar benchmarks ni SLAs no aprobados.

**Salida obtenida:** Un borrador con contexto, alternativas, decisión propuesta, consecuencias y evidencia pendiente.

**Problema detectado:** La IA sugería alternativas sin distinguir claramente trade-offs y sin dejar evidencia pendiente ni condición de revisión concreta.

**Cambio realizado por mí:** Estructuré el ADR con tres alternativas reales y un criterio claro: usar paginación por página/tamaño con orden estable, dejando la condición de revisión explícita si aparecen requisitos de volumen o auditoría más estrictos.

**Criterio o evidencia utilizada:** Comparación de necesidades reales del caso — crecimiento de datos, trazabilidad y experiencia de usuario — y rechazo de supuestos no confirmados.

**Pregunta todavía abierta:** ¿Se debe seguir con paginación por offset o exigir cursor-based pagination si el número de registros crece de forma más agresiva?

