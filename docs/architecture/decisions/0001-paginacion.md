# ADR 0001 — Paginación del historial de transacciones

## Contexto

El endpoint de historial de transacciones de LegacyPay debe soportar consultas crecientes por comercio. La consulta debe ser paginada, auditable y consistente con el caso de uso de revisión del historial. No se han definido benchmarks ni SLA explícitos, por lo que la decisión debe priorizar claridad operativa y facilidad de implementación sobre supuestos de escala no confirmados.

El problema principal es equilibrar: 
- crecimiento potencial de registros por comercio;
- necesidad de auditar resultados y mantener trazabilidad;
- experiencia de usuario al navegar el historial;
- facilidad de implementación y costo de cambio del endpoint.

## Alternativas

### Alternativa 1 — Paginación por offset

- La API recibe `page` y `page_size`.
- El backend calcula el desplazamiento a partir del número de registros.
- Es simple de implementar y fácil de entender para clientes.

#### Ventajas
- Implementación directa y familiar.
- Permite navegar por páginas con criterio simple.
- Buena experiencia para casos pequeños y medianos.

#### Desventajas
- Puede degradar al moverse a páginas altas, porque el desplazamiento crece con el número total de registros.
- Es más frágil si hay cambios en el conjunto de resultados entre páginas.
- Requiere cuidado para mantener orden estable y evitar resultados inconsistente entre consultas.

### Alternativa 2 — Paginación por cursor

- La API recibe un token o cursor basado en un valor estable del orden de resultados.
- El backend retorna el siguiente cursor si hay más resultados.
- Es más robusta frente a cambios de conjunto durante la navegación.

#### Ventajas
- Mejor comportamiento bajo crecimiento de datos y consultas largas.
- Menos sensible a cambios del conjunto y a reordenamientos.
- Tiene mejor trazabilidad si se usa un criterio de orden determinista.

#### Desventajas
- Más compleja de implementar y documentar.
- Requiere definiciones más claras sobre el orden de resultados y la semántica del cursor.
- Puede ser más costosa de cambiar si la API ya está orientada a `page`/`size`.

### Alternativa 3 — Sin paginación, devolver un conjunto acotado por defecto

- La API devuelve un máximo fijo de registros por solicitud.
- Se intentaría limitar el número de resultados sin paginación explícita.

#### Ventajas
- Muy simple de desplegar.
- Reduce riesgo inmediato de respuestas enormes.

#### Desventajas
- No resuelve bien la navegación del historial.
- Dificulta la experiencia del usuario y la auditoría del conjunto completo.
- No permite volumen ni trazabilidad clara de la consulta.

## Decisión propuesta

Se propone usar paginación por offset con parámetros explícitos de `page` y `page_size`, siempre con un orden determinista por fecha y/o identificador de transacción. La decisión se basa en la necesidad de una solución simple, auditable y fácil de implementar dentro del alcance del caso de uso.

Se acepta como condición de revisión que si el volumen de transacciones o el crecimiento del comercio evidencia un problema real de rendimiento o consistencia, se reevalúa la estrategia y se considera migrar a cursor-based pagination.

## Consecuencias positivas

- Es una estrategia fácil de implementar y probar.
- La API queda clara para clientes y usuarios internos.
- Permite revisar el historial en fragmentos manejables.
- Es compatible con la necesidad de auditoría y con la trazabilidad básica del historial.

## Consecuencias negativas

- La paginación por offset puede volverse menos eficiente con archivos largos o páginas altas.
- El orden debe mantenerse estable para evitar resultados ambiguos entre consultas.
- En escenarios con cambios frecuentes en la base de datos, los resultados pueden verse afectados por una vista cambiante del conjunto.

## Evidencia pendiente

- Volumen real esperado de transacciones por comercio.
- Requisito operativo de orden de resultados para auditoría.
- Decisión sobre si un comercio necesita páginas muy avanzadas o un tratamiento distinto.
- Confirmación sobre el criterio de orden (fecha, id, status o combinación).

## Condición de revisión

Este ADR se revisará si la carga de registros o los requisitos de auditoría muestran que offset no es suficiente, o si se definen requerimientos explícitos de consistencia o rendimiento en producción.
