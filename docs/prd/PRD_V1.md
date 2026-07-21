# PRODUCT REQUIREMENT DOCUMENT (PRD) - HISTORIAL DE TRANSACCIONES DE LEGACYPAY

## 1. Visión y problema

### Hechos Aprobados
- LegacyPay opera como una pasarela de pagos B2B.
- Se requiere que un comercio autorizado pueda consultar sus transacciones realizadas en el sistema.

### Propuestas
- **Problema:** Actualmente, los comercios carecen de una herramienta estructurada y segura dentro de la plataforma para visualizar y conciliar su historial de cobros de manera autónoma, lo que incrementa el volumen de consultas de soporte y dificulta el control de su flujo financiero.
- **Visión:** Facilitar a los comercios autorizados una consulta rápida, paginada y segura de su historial de transacciones recientes (limitado a 90 días), garantizando que no se exponga información confidencial de las tarjetas de pago ni credenciales de autenticación.

---

## 2. Alcance incluido y fuera de alcance

### Hechos Aprobados
- **Incluido:**
  - Consulta de transacciones realizadas en los últimos 90 días.
  - Filtros mínimos de búsqueda obligatorios: fecha, estado y monto.
  - Paginación en la entrega de resultados de la consulta.
  - Protección de datos: Exclusión de datos completos de tarjeta y datos de autenticación en cualquier sección del historial.
  - Uso exclusivo de datos sintéticos.
- **Fuera de alcance:**
  - Exposición del número de tarjeta completo (PAN).
  - Exposición de datos de autenticación del usuario (PIN, CVV/CVC, contraseñas de un solo uso u otros factores).

### Propuestas
- **Incluido:**
  - Visualización del enmascaramiento parcial del número de tarjeta (ej. solo mostrar los últimos 4 dígitos) para facilitar la identificación de la transacción por parte del comercio sin comprometer la seguridad.
  - Visualización de datos básicos transaccionales como Identificador de la Transacción, Fecha/Hora del evento, Estado, y Monto.
- **Fuera de alcance:**
  - Consulta de transacciones que excedan los 90 días de antigüedad.
  - Exportación masiva de transacciones a formatos externos (CSV, PDF, Excel) en esta fase inicial.
  - Acciones de reembolso o reversión de transacciones desde la pantalla de consulta de historial.

---

## 3. Usuarios, entidades y reglas de negocio

### Hechos Aprobados
- **Usuarios:**
  - **Comercio Autorizado:** Usuario o sistema del comercio que cuenta con credenciales y permisos validados para consultar información financiera en LegacyPay.
- **Entidades:**
  - **Transacción:** Registro del procesamiento de un cobro o intento de cobro a través de la pasarela LegacyPay.
- **Reglas de Negocio:**
  - **Límite Temporal de Consulta:** El sistema solo permitirá buscar y retornar transacciones cuya fecha de registro esté comprendida dentro de los últimos 90 días corridos a partir de la fecha de la consulta.
  - **Privacidad Estricta de Datos:** Está prohibida la persistencia en caché de cliente, transmisión o despliegue en pantalla de los datos de tarjetas completos (PAN) o cualquier dato utilizado para autenticar la transacción.
  - **Paginación Obligatoria:** Toda consulta al historial debe retornar los resultados paginados para evitar la saturación de los canales y la base de datos.

### Propuestas
- **Aislamiento de Comercios (Multi-tenant):** Un comercio autorizado solo puede visualizar las transacciones asociadas a su propio identificador de comercio único. No puede acceder a datos de otros comercios.
- **Operación de Filtros:** Los filtros mínimos (fecha, estado y monto) pueden combinarse entre sí (relación lógica AND) para refinar la búsqueda.
- **Filtro de Fecha:** Se implementará como un rango de fechas con "Fecha Desde" y "Fecha Hasta".
- **Filtro de Monto:** Se implementará como un rango numérico que admita "Monto Mínimo" y "Monto Máximo".

---

## 4. Historias de usuario con criterios de aceptación

### Historia de Usuario 1: Consulta paginada del historial
**Como** Comercio Autorizado,  
**Quiero** visualizar mi historial de transacciones de manera paginada,  
**Para** poder revisar la lista de operaciones realizadas sin sobrecargar la interfaz ni los sistemas.

* **Criterios de Aceptación:**
  * **Dado** que soy un Comercio Autorizado autenticado en la plataforma,
  * **Cuando** solicito el historial de transacciones sin especificar filtros avanzados,
  * **Entonces** el sistema debe presentar las transacciones de los últimos 90 días ordenadas cronológicamente [PREGUNTA ABIERTA: Orden por defecto (ascendente o descendente)].
  * **Y** el resultado debe estar fraccionado en páginas de un tamaño controlado [PREGUNTA ABIERTA: Tamaño de página por defecto y máximo].
  * **Y** la interfaz o la respuesta técnica debe proveer los metadatos de paginación (ej. número de página actual, total de páginas, o indicador de si hay una página siguiente disponible).

### Historia de Usuario 2: Búsqueda con filtros mínimos
**Como** Comercio Autorizado,  
**Quiero** filtrar el historial de transacciones por fecha, estado y monto,  
**Para** localizar rápidamente cobros específicos y agilizar mis tareas de conciliación operativa.

* **Criterios de Aceptación:**
  * **Dado** que estoy visualizando el historial de transacciones,
  * **Cuando** aplico un filtro por rango de fechas (dentro del límite de 90 días), un filtro por estado específico o un rango de montos (o una combinación de ellos),
  * **Entonces** el sistema debe retornar únicamente las transacciones que coincidan con todos los filtros indicados.
  * **Y** el conjunto de resultados filtrados debe entregarse respetando la regla de paginación obligatoria.

### Historia de Usuario 3: Enmascaramiento y seguridad de datos sensibles
**Como** Comercio Autorizado,  
**Quiero** ver la información de mis cobros sin exponer datos completos de tarjeta de los clientes ni información de autenticación,  
**Para** asegurar el cumplimiento de las normativas de seguridad y proteger a los tarjetahabientes.

* **Criterios de Aceptación:**
  * **Dado** que se despliega la información de una transacción en el historial,
  * **Cuando** se visualiza el medio de pago (tarjeta) asociado,
  * **Entonces** el número de la tarjeta debe presentarse enmascarado [PREGUNTA ABIERTA: Formato de enmascaramiento exacto, ej. \*\*\*\* \*\*\*\* \*\*\*\* 1234 o 123456\*\*\*\*\*\*1234].
  * **Y** el sistema no debe almacenar temporalmente, transmitir en el cuerpo de la respuesta ni renderizar bajo ninguna condición el CVV/CVC, el PIN, ni ningún token de autenticación del pagador.

---

## 5. Restricciones no funcionales

### Hechos Aprobados
- **Seguridad:** Cero exposición de datos completos de tarjeta y datos de autenticación.
- **Período de Conservación/Consulta:** Restricción estricta de acceso a transacciones de los últimos 90 días.

### Propuestas
- **Protocolo de Comunicación:** Toda transferencia de información entre el cliente (comercio) y la pasarela debe realizarse sobre un canal seguro mediante HTTPS cifrado.
- **Autenticación de Peticiones:** Las consultas al historial deben estar respaldadas por tokens de sesión o API Keys válidas y vigentes asignadas al Comercio Autorizado.

---

## 6. Preguntas abiertas

Las siguientes definiciones e información no fueron provistas en el material original y deben ser aclaradas y aprobadas antes de proceder con el diseño técnico detallado o la construcción del software:

1. **Estados de la Transacción:** ¿Cuáles son los estados válidos en LegacyPay para el filtro por estado? (Ej. *Aprobada*, *Declinada*, *Pendiente*, *Reversada*, *Cancelada*).
2. **Dimensionamiento de la Paginación:** ¿Cuál será el límite de ítems por página configurado por defecto y el máximo permitido si el usuario solicita personalizar el tamaño de página?
3. **Formato exacto de enmascaramiento:** ¿Cuál es el estándar de enmascaramiento requerido para los números de tarjeta? (Ej. Mostrar BIN de 6 dígitos + 4 dígitos finales, o solo mostrar los últimos 4 dígitos).
4. **Campos adicionales en el modelo de datos sintéticos:** ¿Qué campos adicionales no confidenciales deben formar parte del registro transaccional sintético? (Ej. moneda, identificador de terminal, descripción de la compra, código de respuesta del procesador).
5. **Comportamiento ante solicitudes fuera de rango:** Si un comercio intenta forzar un filtro de fecha que inicia hace más de 90 días, ¿el sistema debe arrojar un error de validación explícito (ej. HTTP 400) o debe truncar el rango de búsqueda silenciosamente a los últimos 90 días?
6. **Manejo de zonas horarias:** ¿Las búsquedas por fecha se realizan bajo la zona horaria UTC del servidor o bajo la zona horaria configurada para el comercio?
7. **SLA de rendimiento:** ¿Cuál es el tiempo de respuesta máximo aceptable para la consulta paginada bajo condiciones normales de uso?
8. **Auditoría de accesos:** ¿Se requiere registrar en logs cada consulta al historial de transacciones indicando el usuario y los parámetros de búsqueda utilizados?
9. **Medios de pago soportados:** ¿El historial de transacciones debe contemplar únicamente pagos con tarjeta de crédito/débito o existen otros medios de pago sintéticos a incluir (ej. transferencias bancarias, billeteras digitales)?
