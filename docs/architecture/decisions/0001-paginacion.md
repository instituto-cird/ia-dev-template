# ADR 0001: Estrategia de paginación para el historial de transacciones

## Contexto

El servicio LegacyPay expone un endpoint para la consulta del historial de transacciones. Dadas las proyecciones de uso, se establecen las siguientes condiciones:
- La cantidad de transacciones puede crecer de manera significativa por comercio.
- El endpoint debe ser auditable, requiriendo trazabilidad de qué información exacta fue consultada y retornada en un momento dado.
- Es mandatorio que la consulta esté paginada para evitar sobrecargar tanto la base de datos como el servicio.
- Actualmente no contamos con benchmarks o Acuerdos de Nivel de Servicio (SLA) específicos de tiempos de respuesta aprobados, por lo que se deben priorizar patrones arquitectónicos que soporten un crecimiento sostenido de datos orgánicamente sin requerir hardware excesivo.

Los criterios principales para la evaluación son:
- Rendimiento bajo crecimiento de datos.
- Facilidad de implementación.
- Experiencia de usuario (navegación y consistencia).
- Costo de cambio (impacto al cambiar la estrategia en el futuro).
- Evidencia pendiente.

## Alternativas

### Opción 1: Paginación basada en Offset / Limit
Consiste en utilizar los parámetros `page` (o `offset`) y `size` (o `limit`).
- **Ventajas:** Facilidad de implementación alta; soportado nativamente por la mayoría de los frameworks y ORMs. Buena experiencia de usuario en casos donde se requiere saltar a una página específica (ej. página 15).
- **Desventajas:** El rendimiento bajo crecimiento de datos se degrada exponencialmente a medida que el `offset` se hace grande, ya que la base de datos escanea y descarta miles de registros previos. Adicionalmente, puede presentar registros duplicados u omitidos si hay inserciones mientras el usuario navega, afectando la auditabilidad. Costo de cambio futuro alto (requiere cambiar el contrato de la API y la UI).

### Opción 2: Paginación basada en Cursor (Keyset Pagination)
Consiste en utilizar un token opaco o apuntador (`cursor`) que referencia el último registro procesado, permitiendo a la base de datos buscar registros adyacentes a través de índices.
- **Ventajas:** Excelente rendimiento bajo crecimiento de datos (tiempo de consulta constante independientemente de cuán avanzada esté la página). Elimina anomalías en la vista ante inserciones concurrentes, fortaleciendo la trazabilidad y la auditabilidad.
- **Desventajas:** Facilidad de implementación moderada (requiere codificar/decodificar el cursor y manejar múltiples campos de ordenamiento con cuidado). La experiencia de usuario se restringe a navegación de "siguiente" o "anterior" o uso de scroll infinito (no permite saltar a una página N).

## Decisión propuesta

Se propone adoptar la **Paginación basada en Cursor (Keyset Pagination)**.

Dado que la cantidad de registros por comercio crecerá considerablemente y la auditabilidad demanda consistencia al consultar la información, los beneficios de rendimiento y consistencia superan las desventajas de no poder saltar a páginas arbitrarias. Es preferible asumir un leve sobrecosto de implementación ahora que enfrentar una refactorización (alto costo de cambio) cuando el servicio se degrade por volumen de datos.

## Consecuencias positivas

- **Rendimiento predecible y escalable:** Se garantiza una respuesta rápida sin importar la página en la que se encuentre el cliente.
- **Consistencia de datos (Auditabilidad):** Se mitiga el riesgo de saltar o duplicar transacciones al paginar, dado que el cursor apunta siempre a un registro estable en el índice.
- **Prevención de rediseño temprano:** Nos adelantamos a problemas clásicos de degradación, manteniendo bajo el costo técnico futuro.

## Consecuencias negativas

- **Mayor esfuerzo inicial:** Requerirá lógica adicional para serializar y deserializar el token del cursor, así como asegurar índices correctos en base de datos.
- **Restricción de experiencia de usuario UI:** El cliente o portal deberá ser diseñado con "scroll infinito" o botones "Siguiente / Anterior", sin paginador numérico explícito.
- **Complejidad al ordenar:** Si más adelante se requieren filtros y ordenamientos dinámicos muy complejos, el uso de cursores puede complicarse.

## Evidencia pendiente

- **Análisis del ORM/Framework:** Se requiere comprobar qué tan natural es la implementación del cursor en la pila tecnológica seleccionada (ej. si SQLAlchemy, Prisma, etc. cuentan con plugins robustos para esto).
- **Estructura del Cursor:** Acordar cómo se generará el token del cursor (ej. Base64 encodeado de un timestamp y el ID de la transacción `{"created_at": "...", "id": "..."}`) asegurando ofuscación si se considera necesario.

## Condición de revisión

Esta decisión debe ser reevaluada si:
- Se define la necesidad crítica de negocio de permitir "saltar a páginas" (page skipping) por encima del rendimiento.
- Se implementan herramientas de búsqueda indexada (tipo Elasticsearch o Algolia) u otras bases de datos analíticas que asuman el peso de la paginación de reportes masivos y cambien los requisitos de rendimiento en la base de datos transaccional principal.
