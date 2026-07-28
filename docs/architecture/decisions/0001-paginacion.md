# ADR 001: Estrategia de Paginación para el Historial de Transacciones de LegacyPay

## Contexto

LegacyPay es una pasarela B2B que procesa un volumen creciente de operaciones financieras para diversos comercios autorizados. La funcionalidad de consulta del historial de transacciones permite a los comercios filtrar sus operaciones de los últimos 90 días por fecha, estado y monto.

Dado el crecimiento continuo del volumen de datos por comercio y la necesidad de mantener el endpoint auditable y seguro (sin exponer datos sensibles de tarjetas ni credenciales), es indispensable definir una estrategia de paginación eficiente que garantice respuestas consistentes sin degradar el rendimiento de la base de datos ni la experiencia de integración de los clientes.

---

## Alternativas

### 1. Paginación basada en Offset y Límite (Offset-based Pagination)
Consiste en utilizar cláusulas SQL `LIMIT` y `OFFSET` (o `page` y `limit`) para desplazarse por el conjunto de resultados.
- **Ventajas:** Trivial de implementar en cualquier ORM o motor relacional; permite navegación bidireccional libre y acceso directo a páginas específicas (ej. ir directamente a la página 5).
- **Desventajas:** Problemas de rendimiento a medida que crece el `OFFSET` (la base de datos debe escanear y descartar filas previas); inconsistencia de datos (filas duplicadas u omitidas si se insertan nuevas transacciones mientras el usuario navega).

### 2. Paginación por Cursores / Keyset Pagination (Cursor-based Pagination)
Consiste en utilizar un puntero opaco (generalmente compuesto por un timestamp e identificador único) que indica la última posición obtenida. Las siguientes consultas solicitan registros posteriores a dicho cursor.
- **Ventajas:** Rendimiento constante O(1) independiente del volumen de datos (aprovecha índices B-Tree); consistente ante inserciones en tiempo real sin saltos ni duplicados de información.
- **Desventajas:** Ligeramente mayor complejidad en la API; no permite salto directo a páginas aleatorias (solo navegación secuencial hacia adelante/atrás).

---

## Decisión propuesta

Se propone adoptar **Paginación basada en Offset (con límites de tamaño de página estrictos) para la V1**, con un plan claro de migración a **Paginación por Cursores para versiones subsecuentes** si el volumen de datos por comercio lo demanda.

Para mitigar el impacto de rendimiento en la V1:
- Se establece un tamaño de página por defecto de 20 registros y un máximo permitido de 100 registros por petición.
- La restricción de negocio que limita la consulta a los últimos 90 días acota naturalmente el universo de datos a escanear por la base de datos.

### Evaluación según Criterios

| Criterio | Evaluación de la Decisión |
| :--- | :--- |
| **Rendimiento bajo crecimiento de datos** | Aceptable en el corto plazo debido al límite rígido de 90 días de historial. Para grandes volúmenes, la curva de latencia puede degradarse en páginas elevadas (*high-offset query penalty*). |
| **Facilidad de implementación** | Alta. Integración directa en controladores, servicios y capas de repositorio relacionales existentes, reduciendo el tiempo de desarrollo. |
| **Experiencia de usuario** | Excelente para integración B2B estándar: permite construir componentes de UI con numeración de páginas explícita (1, 2, 3...) y conocer el total acumulado de registros. |
| **Costo de cambio** | Bajo/Moderado. Abstraer la respuesta HTTP con un objeto de metadatos genérico permitirá migrar internamente a un esquema basado en cursores sin romper el contrato del cliente. |

---

## Consecuencias positivas

- **Aceleración del Time-to-Market:** Permite cumplir rápidamente con los criterios de aceptación de las Historias de Usuario sin introducir complejidad de cursores en la V1.
- **Facilidad de Auditoría e Integración:** Facilita a los comercios automatizar la descarga serializada y verificable de su historial mediante páginas contiguas.
- **Simplicidad de Contrato:** Entrada de parámetros comprensibles (`page`, `limit`) e integración simple con filtros por fecha, estado y monto.

---

## Consecuencias negativas

- **Degradación potencial de latencia:** Si un comercio registra un volumen excepcionalmente alto de transacciones en los 90 días y consulta las últimas páginas (offset alto), la base de datos procesará la consulta con mayor consumo de I/O.
- **Riesgo de anomalías en lecturas concurrentes:** Si ocurren nuevas transacciones durante la paginación activa de un comercio, algunos registros pueden desplazarse de página.

---

## Evidencia pendiente

- Realizar pruebas de carga con datos sintéticos que simulen la densidad máxima proyectada de transacciones en un rango de 90 días por comercio.
- Monitorear y medir el plan de ejecución de las consultas SQL utilizando índices compuestos sobre `(id_comercio, fecha_transaccion)`.
- Evaluar los patrones reales de consumo de los comercios (si consultan principalmente las primeras páginas o ejecutan exportaciones masivas).

---

## Condición de revisión

Este ADR deberá revisarse si se presenta cualquiera de las siguientes situaciones:
1. El tiempo de respuesta de las consultas con `OFFSET` elevado supera los umbrales operativos aceptables durante las pruebas con datos sintéticos.
2. Se extiende el requerimiento de negocio para consultar historiales con antigüedad mayor a 90 días.
3. Se identifica que más del 80% de los clientes B2B consumen el endpoint mediante procesos automáticos batch que se beneficiarían del uso de cursores.
