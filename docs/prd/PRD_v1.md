# Documento de Requisitos del Producto (PRD) — Historial de Transacciones (v1 - Sin Auditar)

## 1. Visión y Problema
### Visión
Proporcionar a los comercios afiliados a la pasarela B2B LegacyPay una herramienta transparente, auditable y segura para consultar el historial de sus operaciones financieras récientes.

### Problema
Actualmente, los comercios carecen de una interfaz y un endpoint estandarizado para visualizar y filtrar sus transacciones de los últimos 90 días, lo que dificulta la conciliación contable y la atención a reclamos de sus clientes.

---

## 2. Alcance Incluido y Fuera de Alcance

### Alcance Incluido
- Consulta de transacciones realizadas en los últimos 90 días.
- Filtros de búsqueda mínimos por:
  - Rango de fechas (desde / hasta).
  - Estado de la transacción (ej. Aprobada, Rechazada, Pendiente).
  - Rango de monto (mínimo / máximo).
- Paginación de los resultados devueltos por la API para optimizar el rendimiento.
- Mascaramiento de datos sensibles: No se expone el número completo de tarjeta (PAN) ni credenciales de autenticación.

### Fuera de Alcance (Propuesta IA - Sin Validar)
- Exportación masiva de transacciones en formato CSV o PDF.
- Notificaciones push o webhooks en tiempo real sobre cambio de estados.
- Consultas de historial superiores a los 90 días.

---

## 3. Usuarios, Entidades y Reglas de Negocio

### Usuarios
- **Comercio Autorizado:** Usuario autenticado que representa a una entidad comercial registrada en LegacyPay.

### Entidades (Propuestas)
- **Comercio:** Identificador único del comercio, nombre social, estado.
- **Transacción:** ID de transacción, ID del comercio, fecha/hora, monto, moneda, estado, marca de tarjeta, últimos 4 dígitos del PAN (masked PAN).
- **Filtro:** (Propuesta de IA) Parámetros de búsqueda aplicados por el usuario.

### Reglas de Negocio
- **RN-01 (Límite temporal):** Solo se permite consultar transacciones cuyo registro no supere los 90 días de antigüedad desde la fecha actual.
- **RN-02 (Privacidad de Tarjeta):** Bajo ninguna circunstancia la API retornará el PAN completo ni el CVV/CVC de las tarjetas procesadas.
- **RN-03 (Datos Sintéticos):** Todos los datos de prueba y respuestas mock deben utilizar datos sintéticos del caso.
- **RN-04 (Paginación obligatoria):** Las respuestas de lista de transacciones deben estar paginadas con un tamaño de página por defecto.

---

## 4. Historias de Usuario con Criterios de Aceptación

### HU-01: Consulta de historial filtrado por fecha y estado
**Como** comercio autorizado  
**Quiero** consultar la lista de mis transacciones de los últimos 90 días aplicando filtros por fecha y estado  
**Para** realizar la conciliación diaria de mis cobros.

#### Criterios de Aceptación:
- **CA-01.1:** Dado un comercio autenticado, cuando solicita la lista de transacciones especificando un rango de fechas dentro de los últimos 90 días, el sistema retorna solo las transacciones correspondientes a dicho período.
- **CA-01.2:** Si el comercio aplica el filtro de estado "Aprobada", solo se muestran las transacciones con dicho estado.
- **CA-01.3:** La respuesta incluye la lista paginada y los metadatos de paginación (total de páginas, página actual, total de registros).
- **CA-01.4:** (Propuesta IA) El sistema permite exportar los resultados filtrados en un archivo CSV descargable.

---

## 5. Restricciones No Funcionales
- **Seguridad:** Autenticación obligatoria mediante token B2B para cada solicitud de consulta.
- **Auditoría:** Cada petición al endpoint de historial debe quedar registrada en los logs de auditoría del sistema.
- **Privacidad:** Mascaramiento riguroso de datos PCI-DSS (solo últimos 4 dígitos visible).

---

## 6. Preguntas Abiertas
- [PREGUNTA ABIERTA 01]: ¿Qué roles específicos dentro del comercio (ej. Administrador, Contabilidad, Operador) tienen permiso para consultar el historial?
- [PREGUNTA ABIERTA 02]: ¿Cuál es el tamaño máximo de página permitido en la paginación de la API?
- [PREGUNTA ABIERTA 03]: ¿Cuál es el comportamiento del sistema cuando una consulta no especifica filtros de fecha (se asume el rango completo de 90 días)?
