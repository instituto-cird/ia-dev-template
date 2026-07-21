# Historial de Transacciones de LegacyPay - PRD (Borrador)

## 1. Visión y problema

### Visión
Ofrecer a comercios autorizados una vista paginada y filtrable del historial de transacciones de LegacyPay de los últimos 90 días, que permita consultar resultados relevantes sin exponer datos sensibles.

### Problema
Los comercios necesitan revisar transacciones recientes para conciliación, seguimiento de pagos y soporte, pero el sistema actual no provee un historial accesible con filtros básicos y protección de datos sensibles.

---

## 2. Alcance incluido y fuera de alcance

### Alcance incluido
- Historial de transacciones de los últimos 90 días.
- Filtros mínimos: fecha, estado y monto.
- Paginación de resultados.
- Exclusión de datos completos de tarjeta.
- Exclusión de datos de autenticación.
- Uso de datos sintéticos para el caso de diseño.

### Alcance fuera de alcance
- Consultas de transacciones fuera del periodo de 90 días.
- Exportación masiva de historial.
- Acceso a detalles completos de tarjeta o autenticación.
- Cambios en la política de retención histórica.
- Funcionalidades de disputa o reembolsos desde este historial.

### Hechos proporcionados
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Filtros mínimos: fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- Usar únicamente datos sintéticos del caso.

### Propuestas
- Presentar resultados paginados con resumen de transacción.
- Incluir un listado de estados de transacción visibles para filtrado.
- Incluir rangos de monto como opciones de filtrado.
- Diseñar interfaces de consulta sin campos sensibles.

---

## 3. Usuarios, entidades y reglas de negocio

### Usuarios
- Comercio autorizado de LegacyPay.

### Entidades
- Transacción
- Comercio autorizado

### Reglas de negocio
- La consulta solo puede retornar transacciones de hasta 90 días atrás.
- Solo comercios autorizados pueden acceder al historial.
- El historial debe ser paginado.
- Los filtros mínimos disponibles son fecha, estado y monto.
- La respuesta no debe incluir datos completos de tarjeta ni datos de autenticación.
- Los datos mostrados en el caso pueden ser sintéticos.

### Datos no definidos / PREGUNTA ABIERTA
- PREGUNTA ABIERTA: ¿Cuál es el esquema exacto de los estados de transacción admitidos?
- PREGUNTA ABIERTA: ¿Cuál es el tamaño de página por defecto y los límites máximos de paginación?
- PREGUNTA ABIERTA: ¿Qué campos específicos de transacción deben mostrarse en el historial?
- PREGUNTA ABIERTA: ¿Se permite filtrar por rangos de monto, montos exactos, o ambos?
- PREGUNTA ABIERTA: ¿Cuáles son los criterios de autorización precisa para el comercio (tokens, roles, scopes)?

---

## 4. Historias de usuario con criterios de aceptación

### Historia 1
Como comercio autorizado, quiero consultar mi historial de transacciones de los últimos 90 días para revisar pagos recientes.

Criterios de aceptación:
- Puedo ver transacciones cuya fecha de creación está dentro de los últimos 90 días.
- El sistema no devuelve transacciones anteriores a 90 días.
- El listado muestra solo campos permitidos y no incluye datos completos de tarjeta ni datos de autenticación.

### Historia 2
Como comercio autorizado, quiero filtrar el historial por fecha, estado y monto para encontrar transacciones específicas.

Criterios de aceptación:
- Puedo aplicar al menos filtros de fecha, estado y monto.
- El resultado refleja correctamente los filtros aplicados.
- El historial sigue siendo paginado después de aplicar filtros.

### Historia 3
Como comercio autorizado, quiero navegar por el historial usando paginación para revisar muchas transacciones sin cargar todo de una vez.

Criterios de aceptación:
- La consulta devuelve un conjunto limitado de transacciones por página.
- Puedo solicitar la siguiente página de resultados.
- La paginación funciona junto con los filtros aplicados.

---

## 5. Restricciones no funcionales

- No exponer datos completos de tarjeta.
- No exponer datos de autenticación.
- Usar datos sintéticos para el caso de diseño y documentación.
- El sistema debe cumplir con el requerimiento de 90 días de retención visible.
- La consulta debe ser paginada.
- La solución debe ser compatible con el flujo B2B de LegacyPay.

### PREGUNTA ABIERTA
- PREGUNTA ABIERTA: ¿Hay requisitos de rendimiento específicos para la respuesta de consultas?
- PREGUNTA ABIERTA: ¿Existen requisitos de seguridad adicionales más allá de ocultar tarjeta y auth?

---

## 6. Preguntas abiertas

- ¿Cuál es el esquema exacto de los estados de transacción admitidos?
- ¿Cuál es el tamaño de página por defecto y los límites máximos de paginación?
- ¿Qué campos específicos de transacción deben mostrarse en el historial?
- ¿Se permite filtrar por montos exactos, rangos de monto, o ambos?
- ¿Cuál es el mecanismo de autorización de comercio autorizado (tokens, roles, scopes)?
- ¿Existen requisitos de rendimiento, disponibilidad o seguridad específicos para esta funcionalidad?
