# PRD preliminar - Historial de transacciones de LegacyPay

## 1. Visión y problema

### Hechos aprobados
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Los filtros mínimos de la consulta son fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- El caso debe usar únicamente datos sintéticos.

### Propuesta
- Definir un flujo de consulta del historial de transacciones que permita a un comercio autorizado revisar su historial de forma segura, filtrable y paginada, sin exponer datos sensibles y usando datos sintéticos.

## 2. Alcance incluido y fuera de alcance

### Alcance incluido
- Consulta de transacciones para un comercio autorizado.
- Filtros por fecha, estado y monto.
- Paginación de resultados.
- Exclusión de datos completos de tarjeta y datos de autenticación.
- Uso de datos sintéticos para el caso.

### Fuera de alcance
- Otros filtros distintos a fecha, estado y monto.
- Exposición de datos completos de tarjeta o de autenticación.
- Definición de reglas regulatorias, políticas internas o acuerdos de operación no especificados en los hechos aprobados.
- Cambios de arquitectura o dependencias que no estén justificados por el alcance del producto.

## 3. Usuarios, entidades y reglas de negocio

### Hechos aprobados
- El actor principal es un comercio autorizado.
- El caso de uso central es la consulta de transacciones.

### Propuesta
- Usuarios:
  - Comercio autorizado: realiza la consulta del historial de transacciones.
  - PREGUNTA ABIERTA: ¿debe existir un usuario o rol adicional para administrar o supervisar la consulta?

- Entidades relevantes:
  - Transacción: registro de negocio que se desea consultar.
  - Comercio autorizado: entidad que realiza la consulta.
  - Consulta: operación de búsqueda sobre transacciones.
  - PREGUNTA ABIERTA: ¿se requiere modelar una entidad adicional para representar el resultado paginado?

- Reglas de negocio:
  - La consulta solo aplica a transacciones dentro de los últimos 90 días.
  - La consulta admite filtros por fecha, estado y monto.
  - La consulta debe devolver resultados paginados.
  - No se deben exponer datos completos de tarjeta ni datos de autenticación.
  - El caso debe trabajar con datos sintéticos.
  - PREGUNTA ABIERTA: ¿qué valores exactos de estado y qué formato de fecha y monto deben aceptarse?

## 4. Historias de usuario con criterios de aceptación

### Historia 1
Como comercio autorizado, quiero consultar transacciones dentro de los últimos 90 días, para revisar el historial relevante.

Criterios de aceptación:
- La consulta devuelve únicamente transacciones dentro del rango de los últimos 90 días.
- La consulta puede ejecutarse para un comercio autorizado.
- PREGUNTA ABIERTA: ¿el rango de 90 días debe aplicarse por defecto en todos los casos?

### Historia 2
Como comercio autorizado, quiero filtrar transacciones por fecha, estado y monto, para encontrar registros específicos.

Criterios de aceptación:
- La consulta permite filtrar por fecha.
- La consulta permite filtrar por estado.
- La consulta permite filtrar por monto.
- PREGUNTA ABIERTA: ¿qué combinaciones de filtros son válidas?

### Historia 3
Como comercio autorizado, quiero recibir los resultados de forma paginada, para manejar información de forma ordenada.

Criterios de aceptación:
- Los resultados se entregan en páginas.
- La paginación forma parte del comportamiento de la consulta.
- PREGUNTA ABIERTA: ¿cuál es el tamaño de página por defecto y si se requiere navegación explícita?

### Historia 4
Como comercio autorizado, quiero que la consulta no exponga datos sensibles, para operar de forma segura.

Criterios de aceptación:
- No se exponen datos completos de tarjeta.
- No se exponen datos de autenticación.
- Los datos utilizados en el caso son sintéticos.
- PREGUNTA ABIERTA: ¿qué nivel de obfuscación o truncado se requiere para los campos que sí puedan exponerse?

## 5. Restricciones no funcionales

### Hechos aprobados
- Debe proteger datos sensibles.
- Debe usar datos sintéticos.
- Debe soportar paginación.
- Debe permitir filtros mínimos.

### Propuesta
- Confidencialidad:
  - La solución debe evitar exponer datos completos de tarjeta y datos de autenticación.
- Integridad del caso:
  - El escenario debe basarse en datos sintéticos.
- Usabilidad de consulta:
  - La consulta debe ser navegable mediante paginación.
- PREGUNTA ABIERTA:
  - No se han definido requisitos de rendimiento, disponibilidad, concurrencia, auditoría ni observabilidad.

## 6. Preguntas abiertas

- PREGUNTA ABIERTA: ¿qué formato exacto deben usar los filtros de fecha, estado y monto?
- PREGUNTA ABIERTA: ¿qué valores de estado son válidos para la consulta?
- PREGUNTA ABIERTA: ¿cuál es el tamaño de página por defecto para la paginación?
- PREGUNTA ABIERTA: ¿se requiere ordenar los resultados dentro de cada página?
- PREGUNTA ABIERTA: ¿qué nivel de autenticación o autorización debe aplicarse al acceso a la consulta?
- PREGUNTA ABIERTA: ¿se requiere un contrato de respuesta específico para los resultados de la consulta?
- PREGUNTA ABIERTA: ¿debe la consulta estar disponible para un único comercio autorizado o para múltiples comercios autorizados?
