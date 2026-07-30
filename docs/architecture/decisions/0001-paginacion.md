# ADR 0001: Estrategia de paginación para el endpoint de historial de transacciones de LegacyPay

## Contexto
- La consulta de historial de transacciones puede crecer mucho por comercio.
- El endpoint debe ser auditable.
- La consulta debe ser paginada.
- No se deben inventar benchmarks ni SLA no aprobados.

## Alternativas

### Alternativa A: Paginación basada en offset con límite de página fijo
Descripción: usar parámetros `page` y `page_size`, con un límite máximo estricto para `page_size` y validaciones en el API.

### Alternativa B: Paginación basada en cursor/seek (keyset pagination)
Descripción: usar un cursor opaco que almacene la última `transaction_date` y `transaction_id` vistos, manteniendo un orden estable y limitando la cantidad de filas por página.

### Alternativa C: Paginación híbrida con offset para primer acceso y cursor para siguientes páginas
Descripción: permitir `page` y `page_size` solo en accesos iniciales pequeños, y usar cursor cuando la consulta crezca o cuando el cliente solicite más páginas del mismo contexto.

## Decisión propuesta
Se propone adoptar la alternativa B: paginación basada en cursor/seek con orden estable por `transaction_date` y `transaction_id`.

## Consecuencias positivas
- Mejor rendimiento frente a grandes volúmenes de datos por comercio, ya que evita saltos de offset costosos.
- Orden consistente y menos riesgo de registros omitidos o duplicados cuando los datos cambian entre páginas.
- Facilita la auditoría si el cursor puede relacionarse con el último registro leído y la consulta aplicada.

## Consecuencias negativas
- Mayor complejidad de implementación que un esquema offset simple.
- La experiencia de "ir a la página N" no es directa; el cliente debe seguir el cursor.
- Puede requerir más coordinación entre API y servicio para generar y validar cursors opacos.

## Evidencia pendiente
- Necesidad de datos reales de crecimiento por comercio y volumen de consultas por página.
- Requisitos de auditoría concretos sobre trazabilidad de consultas paginadas.
- Decisión final sobre ordenamiento predeterminado y si se permite orden adicional por campos distintos a `transaction_date`.

## Condición de revisión
Revisar esta decisión después del primer trimestre de operación en producción o cuando la métrica de latencia de consulta paginada supere un umbral acordado durante la implementación inicial.
