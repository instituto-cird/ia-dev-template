# Product Requirements Document (PRD): Historial de Transacciones de LegacyPay

## 1. Visión y problema
**Visión:** Proveer a los comercios autorizados que operan en la pasarela B2B LegacyPay una herramienta de consulta para acceder al historial de sus operaciones recientes.
**Problema:** Los comercios necesitan visibilidad de sus transacciones para conciliación y seguimiento, requiriendo un mecanismo que permita consultar, filtrar y navegar los datos sin comprometer información sensible.

## 2. Alcance incluido y fuera de alcance
**Incluido (Hechos aprobados):**
* Consulta del historial de transacciones limitada a los últimos 90 días.
* Acceso exclusivo para comercios autorizados.
* Capacidad de filtrado mínimo por: fecha, estado y monto.
* Paginación de los resultados de la consulta.
* Enmascaramiento y exclusión de datos completos de tarjeta y datos de autenticación.

**Fuera de alcance:**
* Consulta de transacciones con una antigüedad superior a 90 días.
* Exposición de datos de autenticación o información completa de la tarjeta de pago.
* *PREGUNTA ABIERTA: ¿Se contempla la exportación de resultados (ej. CSV, PDF)?*

## 3. Usuarios, entidades y reglas de negocio

**Usuarios:**
* **Comercio Autorizado:** Cliente B2B de LegacyPay con permisos para consultar su propia actividad transaccional.

**Entidades:**
* **Transacción:** Representación de un cobro o movimiento en la pasarela.

**Reglas de Negocio:**
* **Hecho:** El horizonte de consulta de transacciones está estrictamente limitado a los últimos 90 días.
* **Hecho:** Un comercio únicamente tiene permitido consultar la información de las transacciones asociadas a su cuenta.
* **Hecho:** Los datos completos de la tarjeta y los datos de autenticación no deben exponerse bajo ninguna circunstancia.
* *PREGUNTA ABIERTA: ¿Cuáles son los estados válidos de una transacción en el sistema (ej. Aprobada, Rechazada, Anulada)?*
* *PREGUNTA ABIERTA: ¿Cómo se aplican los filtros (ej. rangos de fechas, coincidencia exacta para monto)?*

## 4. Historias de usuario con criterios de aceptación

**HU 1: Consulta paginada del historial de transacciones**
Como **comercio autorizado**,
Quiero **consultar mi historial de transacciones de los últimos 90 días de forma paginada**,
Para **revisar mis operaciones recientes sin sobrecargar la interfaz o el sistema**.

*Criterios de Aceptación:*
* El sistema debe retornar un listado de transacciones pertenecientes exclusivamente al comercio solicitante.
* El sistema debe rechazar u omitir peticiones de transacciones anteriores a 90 días.
* La respuesta del sistema no debe contener datos completos de tarjeta ni credenciales de autenticación.
* La respuesta debe estar dividida en páginas.
* *PREGUNTA ABIERTA: ¿Cuáles son los parámetros de paginación por defecto (ej. tamaño de página, método de offset vs cursor)?*

**HU 2: Filtrado básico del historial**
Como **comercio autorizado**,
Quiero **filtrar mis transacciones por fecha, estado y monto**,
Para **encontrar registros específicos de manera eficiente**.

*Criterios de Aceptación:*
* El sistema debe permitir aplicar uno o múltiples filtros concurrentes: fecha, estado, monto.
* El sistema debe retornar únicamente los registros que cumplan con todos los criterios de filtrado provistos.

## 5. Restricciones no funcionales
* **Seguridad de la información (Hecho):** Protección de datos sensibles garantizando la no exposición de numeración de tarjetas completa y elementos de autenticación.
* **Aislamiento de datos (Hecho):** Los resultados deben filtrarse a nivel de sistema para garantizar que un usuario solo acceda a su información.
* *PREGUNTA ABIERTA: ¿Existen Acuerdos de Nivel de Servicio (SLA) definidos para el tiempo de respuesta de esta consulta?*
* *PREGUNTA ABIERTA: ¿Cuál es el volumen esperado de consultas concurrentes o el rendimiento (throughput) requerido?*
* *PREGUNTA ABIERTA: ¿Existen políticas de retención y purga de logs u otras normativas (ej. PCI-DSS) adicionales que afecten cómo se consultan los datos?*

## 6. Preguntas abiertas
* ¿Qué atributos adicionales a la Fecha, Estado y Monto componen la entidad de Transacción para ser mostrados al comercio de manera segura?
* ¿Cuál es el mecanismo mediante el cual se identifica que el comercio está autorizado para realizar la consulta en la solicitud?
* ¿Se espera que los filtros de fecha y monto soporten rangos (ej. "desde/hasta") o valores exactos?
* ¿Cómo deben representarse los datos parciales de la tarjeta si se requiere mostrarlos (ej. enmascaramiento mostrando los últimos 4 dígitos)?
