# AI_USAGE — Lab 2

## Entrada 1 — PRD

**Fecha:** 2026-07-28
**Objetivo:** Auditar y consolidar el PRD para el historial de transacciones.
**Herramienta y modelo:** Gemini 3.5 Flash (via Antigravity IDE)
**Contexto proporcionado:** Documentación inicial de requerimientos de negocio y checklist de auditoría del PRD.
**Salida obtenida:** Un borrador de PRD con un alcance sobredimensionado que incluía propuestas no confirmadas (ej: aislamiento multi-tenant y filtros de montos mínimos/máximos en la misma consulta).
**Problema detectado:** La IA sugirió una serie de criterios de aceptación complejos y de infraestructura de seguridad que no formaban parte del alcance aprobado de LegacyPay para esta fase.
**Cambio realizado por mí:** Simplifiqué el PRD_V1.md eliminando las asunciones de multi-tenancy e infraestructura externa, y reescribí las historias de usuario para que se enfoquen estrictamente en: consulta de transacciones de los últimos 90 días, filtros de fecha, estado y monto, paginación, y enmascaramiento de datos sensibles.
**Criterio o evidencia utilizada:** Criterios de auditoría del PRD del material del Módulo 2 y restricciones explícitas del negocio.
**Pregunta todavía abierta:** ¿Cuál es el tamaño máximo de página permitido por la API para evitar abusos de consumo?

## Entrada 2 — ERD

**Fecha:** 2026-07-28
**Objetivo:** Crear y auditar el ERD lógico simplificado para el historial de transacciones.
**Herramienta y modelo:** Gemini 3.5 Flash (via Antigravity IDE)
**Contexto proporcionado:** Documento PRD_V1.md auditado e instrucciones de restricciones del ERD (evitar PAN/CVV, incluir campos necesarios para filtros).
**Salida obtenida:** Un diagrama ERD mínimo con entidades `Comercio` y `Transaccion`, pero mezclando datos de pago en la transacción y sin contemplar auditoría.
**Problema detectado:** El diseño propuesto por la IA no estructuraba adecuadamente la protección de datos (almacenando datos de tarjeta directamente en la transacción) y no tenía un mecanismo claro de auditoría. Además, el archivo original carecía de las secciones obligatorias de Propósito, Supuestos y Preguntas abiertas.
**Cambio realizado por mí:** Creé tablas separadas para `DATOS_PAGO_ENMASCARADO` y `AUDITORIA_CONSULTA` para segregar datos sensibles y registrar auditorías de acceso. Añadí las secciones obligatorias del documento (`Propósito y alcance`, `Supuestos`, y `Preguntas abiertas`) en `erd.md`.
**Criterio o evidencia utilizada:** Restricciones de no exposición de PAN/CVV en el PRD y checklist de auditoría del ERD.
**Pregunta todavía abierta:** ¿Es necesario persistir los filtros aplicados en cada registro de auditoría o basta con un hash de los parámetros para optimizar espacio?

## Entrada 3 — Diagrama de Secuencia

**Fecha:** 2026-07-28
**Objetivo:** Crear y auditar el diagrama de secuencia para la consulta del historial de transacciones.
**Herramienta y modelo:** Gemini 3.5 Flash (via Antigravity IDE)
**Contexto proporcionado:** Historias de usuario y criterios de aceptación definidos en `PRD_V1.md`.
**Salida obtenida:** Un diagrama de secuencia básico que conectaba directamente el API Gateway con el repositorio de datos sin capas intermedias ni validaciones de negocio.
**Problema detectado:** El flujo original de la IA omitía la validación de autorización explícita antes de consultar los datos y no representaba de forma secuencial la validación de los filtros (por ejemplo, el límite estricto de 90 días) como flujo de error `400 Bad Request`.
**Cambio realizado por mí:** Introduje los componentes `Validador de Autorización` y `Caso de Uso / Servicio (Historial)` para desacoplar las responsabilidades. Representé explícitamente el flujo alternativo de token inválido (401/403) al inicio del diagrama y la validación del filtro de 90 días retornando una excepción controlada (400 Bad Request) antes de la consulta al repositorio.
**Criterio o evidencia utilizada:** Reglas de negocio del PRD (autorización previa y límites de filtros) y checklist de auditoría de secuencia.
**Pregunta todavía abierta:** ¿Cómo debe propagarse el error de la base de datos hacia el cliente si el repositorio falla por tiempo de espera (timeout)?
