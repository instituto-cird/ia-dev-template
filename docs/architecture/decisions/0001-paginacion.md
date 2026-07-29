Te dejo un borrador listo para copiar en el archivo de ADR:

````md
# ADR 0001 - Estrategia de paginación del endpoint de historial de transacciones de LegacyPay

## Contexto

El endpoint de historial de transacciones puede crecer significativamente según el volumen de operaciones por comercio. La consulta debe ser paginada para facilitar la navegación y evitar respuestas excesivamente grandes. Además, el endpoint debe ser auditable, por lo que la paginación debe soportar un orden determinista de los resultados y permitir revisar páginas de forma consistente. No se establecen benchmarks ni SLA en este ADR; la decisión debe basarse en la simplicidad inicial y en la evidencia que se obtenga en operación.

## Alternativas

### Alternativa 1: Paginación por offset
- Implementación simple y de bajo riesgo.
- Fácil de entender y mantener.
- Compatible con consultas directas y con un orden estable.
- Menor costo de cambio inicial.

### Alternativa 2: Paginación por cursor
- Mejor comportamiento en conjuntos de datos grandes.
- Menor impacto en lecturas extensas y mejor escalabilidad.
- Requiere más diseño y mayor esfuerzo de implementación.
- Implica un costo de cambio mayor para la primera versión.

## Decisión propuesta

Para la primera versión del endpoint de historial de transacciones, utilizar paginación por offset con un criterio de orden estable (por ejemplo, fecha y/o identificador de transacción) que permita auditar y recorrer resultados de manera predecible. La decisión prioriza la simplicidad de implementación y el bajo costo de cambio sobre la optimización para volúmenes muy altos de datos.

## Consecuencias positivas

- Desarrollo más rápido y menor complejidad técnica.
- Menor riesgo de introducir cambios amplios en el primer lanzamiento.
- Experiencia de usuario sencilla para navegar por resultados paginados.
- Facilita la trazabilidad y la revisión de páginas en escenarios auditables.

## Consecuencias negativas

- Puede degradar el rendimiento a medida que crezca el volumen de transacciones por comercio.
- El uso de offset puede volverse menos eficiente en consultas largas o con muchas páginas.
- Puede requerirse una revisión posterior si se observa un impacto relevante sobre la respuesta del servicio.

## Evidencia pendiente

- Volumen esperado de transacciones por comercio.
- Frecuencia real de uso del historial y tamaño promedio de las páginas consultadas.
- Impacto en tiempos de respuesta y estabilidad del endpoint en operación.
- Necesidad de soporte para navegación profunda o páginas altas.

## Condición de revisión

Esta decisión deberá revisarse si se detecta un impacto significativo de rendimiento, una creciente complejidad operativa o evidencia de que la paginación por offset ya no resulta suficiente para los requisitos del servicio.
````