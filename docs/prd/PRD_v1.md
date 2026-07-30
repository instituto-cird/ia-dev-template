# PRD: Historial de transacciones de LegacyPay

## 1. Visión y problema

### Hechos aprobados
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Filtros mínimos: fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- Usar únicamente datos sintéticos del caso.

### Propuesta
LegacyPay debe ofrecer a los comercios autorizados una vista de historial de transacciones que les permita:
- localizar transacciones recientes de hasta 90 días,
- filtrar por fecha, estado y monto,
- navegar resultados paginados,
- mantener seguridad y privacidad evitando exposición de datos sensibles.

## 2. Alcance incluido y fuera de alcance

### Incluido
- Listado de transacciones de hasta 90 días para comercios autorizados.
- Filtros de búsqueda por:
  - rango de fecha
  - estado de transacción
  - monto
- Paginación de resultados.
- Visualización de datos básicos de transacción sin información sensible.
- Uso de datos sintéticos para pruebas y ejemplos.

### Fuera de alcance
- Consulta de transacciones anteriores a 90 días.
- Descarga o exportación masiva de historial.
- Modificación, reversión o anulación de transacciones.
- Exposición de datos completos de tarjeta.
- Exposición de datos de autenticación.
- Cálculo de métricas agregadas o reportes avanzados.
- Integración con sistemas externos no definidos.

## 3. Usuarios, entidades y reglas de negocio

### Usuarios
- Comercio autorizado: cliente B2B que accede al historial de sus propias transacciones.

### Entidades
- Transacción
  - Fecha
  - Estado
  - Monto
  - Identificador de transacción
  - Información comercial mínima necesaria para identificación

### Reglas de negocio
- Solo los comercios autorizados pueden consultar el historial.
- El historial debe limitarse a transacciones de los últimos 90 días.
- El listado debe soportar filtros por fecha, estado y monto.
- El listado debe ser paginado para evitar grandes volúmenes en una sola consulta.
- No se deben mostrar datos completos de tarjeta ni datos de autenticación en ninguna respuesta.
- La vista debe usar exclusivamente datos sintéticos cuando se trate de ejemplos o pruebas.

## 4. Historias de usuario con criterios de aceptación

### Historia 1
Como comercio autorizado,
quiero ver el historial de mis transacciones de hasta 90 días,
para revisar mi actividad reciente.

Criterios de aceptación:
- Se muestra un listado de transacciones.
- Todas las transacciones son de los últimos 90 días.
- No aparecen datos completos de tarjeta ni datos de autenticación.
- El listado está paginado.

### Historia 2
Como comercio autorizado,
quiero filtrar el historial por rango de fecha,
para encontrar transacciones dentro de un periodo específico.

Criterios de aceptación:
- Existe un filtro por fecha de inicio y fin.
- El resultado incluye solo transacciones dentro del rango seleccionado.
- La paginación sigue funcionando después de aplicar el filtro.

### Historia 3
Como comercio autorizado,
quiero filtrar el historial por estado de transacción,
para revisar solo transacciones aprobadas, fallidas u otro estado.

Criterios de aceptación:
- Existe un filtro de estado.
- Solo se muestran transacciones con el estado seleccionado.
- No se muestran datos sensibles.

### Historia 4
Como comercio autorizado,
quiero filtrar el historial por monto,
para encontrar transacciones dentro de un rango de valores.

Criterios de aceptación:
- Existe un filtro de monto mínimo y máximo.
- El resultado incluye solo transacciones dentro del rango seleccionado.
- No se muestran datos de tarjeta completos ni autenticación.

## 5. Restricciones no funcionales
- Las consultas deben ser paginadas para evitar respuestas excesivamente grandes.
- La interfaz debe garantizar que ningún dato sensible se exponga.
- Debe utilizarse datos sintéticos para casos de prueba o demostración.
- La implementación debe ser compatible con un entorno B2B de comercio autorizado.

## 6. Preguntas abiertas
- PREGUNTA ABIERTA: ¿Qué estados de transacción deben estar disponibles como opciones de filtro?
- PREGUNTA ABIERTA: ¿Cómo se define el tamaño de página y la navegación de paginación?
- PREGUNTA ABIERTA: ¿Qué campos mínimos exactos debe mostrar cada transacción en la interfaz?
- PREGUNTA ABIERTA: ¿Se requiere ordenamiento de resultados? Si es así, ¿por qué campos?
- PREGUNTA ABIERTA: ¿Existen requisitos de auditoría o registro de acceso para estas consultas?