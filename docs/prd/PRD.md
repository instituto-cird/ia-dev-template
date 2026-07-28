# Documento de Requisitos del Producto (PRD) — Historial de Transacciones (Auditado)

## 1. Visión y Problema

### Visión
Proporcionar a los comercios afiliados a la pasarela B2B **LegacyPay** un endpoint y una interfaz segura, auditable y eficiente para la consulta de su historial de transacciones.

### Problema
Los comercios requieren visualizar y filtrar las operaciones procesadas en su cuenta durante los últimos 90 días para actividades de conciliación y soporte, garantizando la privacidad de los datos sensibles y el cumplimiento de normas de auditoría.

---

## 2. Alcance Incluido y Fuera de Alcance

### Alcance Incluido [HECHO APROBADO]
- **Consulta de historial de 90 días:** Acceso exclusivamente a transacciones procesadas en los últimos 90 días naturales.
- **Filtros obligatorios:**
  - Rango de fechas (desde / hasta).
  - Estado de la transacción (ej. Aprobada, Rechazada, Pendiente).
  - Rango de monto (mínimo / máximo).
- **Paginación obligatoria:** Los resultados retornados por la API deben ser paginados de forma transparente.
- **Auditoría:** Registro de accesos y consultas efectuadas al endpoint.
- **Protección de Datos:** Mascaramiento riguroso de PAN (solo últimos 4 dígitos) y exclusión total de CVV o datos de autenticación.
- **Uso de Datos Sintéticos:** El entorno de demostración y pruebas utilizará únicamente datos sintéticos.

### Fuera de Alcance [DECISIÓN APROBADA]
- Exportación masiva a archivos externos (CSV, Excel, PDF) — *Descartado del alcance v1*.
- Notificaciones push o webhooks en tiempo real sobre transacciones.
- Consultas de transacciones con antigüedad mayor a 90 días.
- Procesamiento de reembolsos o reversiones desde la vista de historial.

---

## 3. Usuarios, Entidades y Reglas de Negocio

### Usuarios [HECHO / PREGUNTA ABIERTA]
- **Comercio Autorizado:** Entidad comercial autenticada en la plataforma LegacyPay.
- *[PREGUNTA ABIERTA 01]*: El caso no especifica la jerarquía interna de usuarios del comercio (ej. Rol Administrador vs Rol Contador). Para la v1 se asume un rol único de "Comercio Autorizado".

### Entidades de Dominio Validadas [DECISIÓN APROBADA]
- **Comercio:** `id_comercio`, `nombre_comercio`, `estado`.
- **Transacción:** `id_transaccion`, `id_comercio`, `fecha_hora`, `monto`, `moneda`, `estado_transaccion`, `masked_pan` (últimos 4 dígitos), `marca_tarjeta`.

> [!NOTE]
> **Auditoría de Entidades:** Se descarta la entidad "Filtro" propuesta por la IA en la v1, ya que corresponde a parámetros de consulta HTTP y no a una entidad persistente de base de datos.

### Reglas de Negocio Validadas
- **RN-01 (Límite Temporal 90 días):** La API rechazará o limitará automáticamente cualquier consulta cuyo rango de fechas supere los 90 días de antigüedad respecto a la fecha actual.
- **RN-02 (Privacidad de Tarjeta PCI):** Queda prohibida la exposición del PAN completo (Número de Tarjeta) y datos de autenticación (CVV/PIN). Solo se retornará el atributo `masked_pan` (ej. `**** **** **** 1234`).
- **RN-03 (Paginación Obligatoria):** Toda respuesta de lista de transacciones debe incluir parámetros de paginación (`page`, `page_size`, `total_records`, `total_pages`).
- **RN-04 (Aislamiento por Comercio):** Un comercio autorizado solo puede consultar transacciones asociadas a su propio `id_comercio`.

---

## 4. Historias de Usuario con Criterios de Aceptación

### HU-01: Consulta Paginada de Historial de Transacciones con Filtros
**Como** comercio autorizado  
**Quiero** consultar la lista de mis transacciones procesadas en los últimos 90 días aplicando filtros por fecha, estado y monto  
**Para** realizar la conciliación financiera de mi negocio de forma segura.

#### Criterios de Aceptación:
- **CA-01.1 (Filtro por Rango de Fechas):** Dado un comercio autenticado, cuando envía una solicitud de consulta indicando una fecha de inicio y fecha de fin válidas (dentro de los últimos 90 días), el sistema retorna las transacciones comprendidas en ese intervalo.
- **CA-01.2 (Filtro por Estado):** Dado un comercio autenticado, cuando filtra por estado (ej. "APROBADA"), el sistema retorna exclusivamente las transacciones cuyo `estado_transaccion` coincida con el valor solicitado.
- **CA-01.3 (Filtro por Monto):** Dado un comercio autenticado, cuando especifica un monto mínimo y/o monto máximo, el sistema retorna solo las transacciones cuyos montos se encuentren en dicho rango.
- **CA-01.4 (Paginación de Resultados):** La respuesta HTTP 200 OK retorna la lista de transacciones correspondientes a la página solicitada junto con los metadatos de paginación.
- **CA-01.5 (Seguridad y Privacidad):** Los objetos de transacción devueltos contienen únicamente el número de tarjeta enmascarado (`masked_pan`) y no contienen datos de autenticación ni CVV.

---

## 5. Restricciones No Funcionales
- **Seguridad:** Autenticación y autorización previa mediante token B2B antes de procesar cualquier consulta.
- **Auditoría:** Registro (logging) auditable de todas las peticiones de consulta realizadas por los comercios.
- **Cumplimiento PCI:** Cumplimiento con las normas de no almacenamiento ni exposición de datos sensibles de tarjetas.

---

## 6. Preguntas Abiertas

- **[PREGUNTA ABIERTA 01]:** ¿Existen roles diferenciados dentro del comercio (ej. Operador vs Administrador) con permisos de lectura restringidos?
- **[PREGUNTA ABIERTA 02]:** ¿Cuál es el límite máximo de registros por página (`page_size`) permitido en el endpoint para evitar degradación de rendimiento?
- **[PREGUNTA ABIERTA 03]:** ¿Cuál es el comportamiento por defecto si el comercio realiza una consulta sin especificar ningún filtro de fecha (¿se asumen los últimos 30 días o los 90 días completos?)?
