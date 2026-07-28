# PRODUCT REQUIREMENT DOCUMENT (PRD) - HISTORIAL DE TRANSACCIONES DE LEGACYPAY

## 1. Visión y problema

### Hechos proporcionados

- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- La consulta debe permitir filtros por fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- Se deben utilizar únicamente datos sintéticos del caso.

**Fuente:**
- Pedido de negocio proporcionado.

### Propuestas

- Crear una funcionalidad de consulta del historial de transacciones para comercios autorizados.

---

## 2. Alcance incluido y fuera de alcance

### Incluido

- Consulta de transacciones de los últimos 90 días.
- Filtros por fecha, estado y monto.
- Resultados paginados.
- Uso de datos sintéticos.

### Fuera de alcance

- Exposición de datos completos de tarjeta.
- Exposición de datos de autenticación.

---

## 3. Usuarios y reglas de negocio

### Hechos proporcionados

**Usuario:**
- Comercio autorizado.

**Reglas de negocio:**
- La consulta está limitada a los últimos 90 días.
- Deben existir filtros por fecha, estado y monto.
- Los resultados deben ser paginados.
- No deben exponerse datos completos de tarjeta ni datos de autenticación.

---

## 4. Historias de usuario con criterios de aceptación

### Historia 1: Consulta del historial

**Como** comercio autorizado,  
**quiero** consultar el historial de transacciones,  
**para** acceder a las operaciones disponibles.

**Criterios de aceptación:**

- Permite consultar transacciones dentro de los últimos 90 días.
- Los resultados se entregan mediante paginación.

---

### Historia 2: Filtros de consulta

**Como** comercio autorizado,  
**quiero** aplicar filtros de búsqueda,  
**para** localizar transacciones.

**Criterios de aceptación:**

- Permite filtrar por fecha, estado y monto.
- Mantiene la paginación de resultados.

---

### Historia 3: Protección de datos

**Como** comercio autorizado,  
**quiero** consultar información sin datos restringidos,  
**para** evitar exposición de información sensible.

**Criterios de aceptación:**

- No muestra datos completos de tarjeta.
- No muestra datos de autenticación.

---

## 5. Restricciones no funcionales

### Hechos proporcionados

- No exponer datos completos de tarjeta.
- No exponer datos de autenticación.
- Limitar la consulta a los últimos 90 días.
- Utilizar paginación.
- Utilizar datos sintéticos.

---

## 6. Preguntas abiertas

1. ¿Cuál es el problema de negocio específico que origina esta necesidad?

2. ¿Qué información debe mostrarse por cada transacción?

3. ¿Qué valores tendrá el filtro de estado?

4. ¿Cómo funcionarán los filtros de fecha y monto?

5. ¿Cuál será la estructura y tamaño de paginación?

6. ¿Existe algún requisito adicional para la primera versión?