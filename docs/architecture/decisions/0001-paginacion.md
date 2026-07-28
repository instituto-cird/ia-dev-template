# ADR 0001 - Estrategia de Paginación

## Contexto

La funcionalidad de historial de transacciones puede crecer significativamente en cantidad de registros por comercio.

## Alternativas

### Alternativa 1: Offset Pagination

- Fácil implementación.
- Compatible con consultas simples.

### Alternativa 2: Cursor Pagination

- Mejor rendimiento para grandes volúmenes.
- Menor impacto en consultas extensas.

## Decisión propuesta

Utilizar Offset Pagination para la primera versión debido a su simplicidad de implementación y mantenimiento.

## Consecuencias positivas

- Desarrollo más rápido.
- Menor complejidad técnica.
- Fácil comprensión para el equipo.

## Consecuencias negativas

- Puede degradar rendimiento con grandes volúmenes.
- Posibles tiempos de respuesta mayores en consultas extensas.

## Evidencia pendiente

- Volumen esperado de transacciones por comercio.
- Necesidades reales de escalabilidad.

## Condición de revisión

La decisión deberá revisarse si se detectan problemas de rendimiento o crecimiento significativo de datos.