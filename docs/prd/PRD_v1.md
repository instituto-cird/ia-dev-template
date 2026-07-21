# PRD — Historial de Transacciones (LegacyPay)

---

## HECHOS APROBADOS
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Filtros mínimos requeridos: fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- Usar únicamente datos sintéticos para ejemplos y pruebas.

---

## 1. Visión y problema
Visión: Permitir a comercios autorizados consultar y revisar de forma segura las transacciones procesadas por LegacyPay en los últimos 90 días, facilitando investigación y conciliación sin exponer datos sensibles.

Problema: Actualmente los comercios necesitan una interfaz/endpoint confiable para revisar transacciones recientes que cumpla con requisitos mínimos de filtrado y privacidad, y que soporte volúmenes paginados sin revelar información de pago sensible.

---

## 2. Alcance

Incluido
- Endpoint(s) o interfaz para listar transacciones de los últimos 90 días.
- Soporte de filtros: rango de fecha, estado de transacción y rango/valor de monto.
- Paginación de resultados.
- Visualización de datos no sensibles de la transacción para cada resultado.
- Uso de datos sintéticos en ejemplos, documentación y pruebas.

Fuera de alcance
- Exposición de datos completos de tarjeta (PAN completo), códigos de autenticación o credenciales.
- Procesamiento de reembolsos, cancelaciones o acciones sobre transacciones (solo lectura).
- Retención fuera del periodo de 90 días (no se define almacenamiento histórico adicional).
- Extracción/export masivo fuera de la paginación básica (PREGUNTA ABIERTA: export requerido? ver sección de preguntas).

---

## 3. Usuarios, entidades y reglas de negocio

Usuarios (roles)
- Comercio autorizado: usuario que consulta su propio historial de transacciones.
- Operador interno / Soporte (si aplica): PREGUNTA ABIERTA — ¿tendrá acceso distinto?

Entidades (separar hechos de propuestas)
- Hechos: existe el concepto de "transacción" y "comercio autorizado".
- Propuesta (sugerida, no implementada sin aprobación): representación de una transacción en la vista/listado incluirá únicamente campos no sensibles (metadatos identificadores y atributos no sensibles).  
  PREGUNTA ABIERTA: confirmar campos exactos permitidos en la representación.

Reglas de negocio (aprobadas)
- Solo se pueden consultar transacciones hasta 90 días hacia atrás.
- Las consultas deben soportar filtrado por fecha, estado y monto.
- Los resultados deben entregarse paginados.
- No se deben exponer datos completos de tarjeta ni datos de autenticación.

Reglas de negocio (propuestas / aclaraciones)
- El acceso estará limitado al comercio propietario de las transacciones (autorización por credenciales/rol). PREGUNTA ABIERTA: mecanismo exacto de autorización.
- Si un filtro no se provee, se aplica la consulta en el rango de 90 días por defecto. PREGUNTA ABIERTA: confirmar comportamiento por defecto.

---

## 4. Historias de usuario con criterios de aceptación

Historia 1 — Listado básico
- Como comercio autorizado
- Quiero obtener una lista paginada de mis transacciones de los últimos 90 días
- Para revisar actividad reciente sin exponer datos sensibles

Criterios de aceptación:
- Dado un comercio autenticado, cuando solicita el listado sin filtros, entonces recibe transacciones hasta 90 días atrás, paginadas.
- Los resultados no contienen PAN completo ni datos de autenticación.
- La respuesta contiene metadatos de paginación (p.ej. cursor o offset, total desconocido según decisión). PREGUNTA ABIERTA: forma de paginación preferida (cursor vs offset).

Historia 2 — Filtrado por fecha
- Como comercio autorizado
- Quiero filtrar por un rango de fecha dentro de los últimos 90 días
- Para ver transacciones en un periodo específico

Criterios de aceptación:
- Dado un rango de fecha válido dentro de 90 días, la respuesta incluye solo transacciones cuyo `timestamp` cae en ese rango.
- Si el rango solicitado excede 90 días hacia atrás, la consulta se restringe al máximo permitido y se devuelve un aviso o error (comportamiento a definir). PREGUNTA ABIERTA: ¿devolver error o truncar automáticamente?

Historia 3 — Filtrado por estado
- Como comercio autorizado
- Quiero filtrar por estado de transacción (p.ej. aprobado, rechazado)
- Para identificar transacciones con un mismo resultado

Criterios de aceptación:
- El sistema acepta uno o más estados como filtro y retorna solo transacciones que coincidan.
- PREGUNTA ABIERTA: lista de estados permitidos y sus codificaciones/labels.

Historia 4 — Filtrado por monto
- Como comercio autorizado
- Quiero filtrar por rango de monto
- Para localizar transacciones dentro de valores monetarios específicos

Criterios de aceptación:
- Se aceptan filtros de mínimo y/o máximo monto y la respuesta respeta los límites.
- PREGUNTA ABIERTA: moneda(s) soportadas y reglas de conversión/moneda por transacción.

Historia 5 — Visualizar detalle limitado de transacción
- Como comercio autorizado
- Quiero ver el detalle de una transacción individual sin datos sensibles
- Para investigar una transacción específica

Criterios de aceptación:
- Al solicitar detalle, se muestran solo campos no sensibles y/o datos enmascarados.
- No se incluyen PAN completo, códigos de autenticación ni credenciales.
- Si se considera mostrar fragmentos enmascarados (ej. último 4), esto debe aprobarse explícitamente. PREGUNTA ABIERTA: ¿se permite mostrar `last4` enmascarado?

Historia 6 — Uso de datos sintéticos para pruebas
- Como equipo de desarrollo/QA
- Quiero ejemplos y datasets sintéticos
- Para validar y demostrar funcionalidad sin usar datos reales

Criterios de aceptación:
- Toda documentación de ejemplo y los tests usan datos sintéticos.
- No se incluyen datos reales en repositorios, demos o pruebas públicas.

---

## 5. Restricciones no funcionales
- Seguridad y privacidad: la implementación no debe exponer datos completos de tarjeta ni credenciales; el acceso debe estar autorizado y registrado.
- Data privacy por diseño: minimizar campos retornados y preferir enmascaramiento cuando sea necesario.
- Paginación obligatoria en todas las respuestas de listado.
- Disponibilidad y rendimiento: el servicio debe ser razonablemente responsivo para consultas interactivas; no se definen SLAs numéricos en este documento. PREGUNTA ABIERTA: requisitos de latencia y disponibilidad.
- Observabilidad: registrar accesos y consultas para auditoría y soporte. PREGUNTA ABIERTA: nivel y retención de logs.
- Pruebas: cubrir filtros, paginación y masking con datos sintéticos.
- Internacionalización/fechas: las fechas deben tener especificación clara (timezone/format). PREGUNTA ABIERTA: formato de fecha y zona horaria por defecto.
- Cumplimiento: no se definen requerimientos regulatorios adicionales aquí. PREGUNTA ABIERTA: ¿revisar requisitos regulatorios aplicables?

---

## 6. Preguntas abiertas (PREGUNTA ABIERTA)
- ¿Cuál es la lista formal de campos permitidos en la representación de una transacción para la API/ UI? (confirmar campos no sensibles)
- ¿Se permite mostrar el `last4` del PAN enmascarado? (sí/no)
- ¿Qué forma de paginación se prefiere: offset/limit o cursor-based?
- ¿Cuál es el tamaño de página por defecto y el tamaño máximo permitido?
- ¿Comportamiento al solicitar un rango de fechas que excede 90 días: truncar o retornar error?
- ¿Cuáles son los estados de transacción canónicos (vocabulario/labels y códigos)?
- ¿Qué monedas deben ser soportadas y cómo se indica la moneda por transacción?
- ¿Qué mecanismo exacto de autorización/autenticación usan los comercios para acceder a este endpoint?
- ¿Se requiere capacidad de export (CSV/JSON) o solo vistas paginadas? 
- ¿Necesitamos auditoría/retención específica de logs (niveles, duración)?
- ¿Requerimientos de latencia y disponibilidad (SLA) para consultas interactivas?
- ¿Soporte para ordenamiento por columnas (p.ej. fecha desc/asc) es necesario?
- ¿Existirá un rol de operador interno con acceso distinto al de comercios? Si sí, especificar permisos.
- ¿Formato y zona horaria estándar para las fechas mostradas en la UI/API?

---

## Separación: hechos proporcionados vs propuestas resumidas
- Hechos proporcionados: listados en la sección "HECHOS APROBADOS".
- Propuestas y supuestos: cualquier detalle operativo, campos de salida, comportamiento por defecto y decisiones tecnológicas listadas en secciones de "Propuesta" o marcadas como PREGUNTA ABIERTA deben validarse antes de implementar.

--- 

Notas finales: Todas las muestras de datos y ejemplos en documentación y pruebas se realizarán con datos sintéticos conforme al hecho aprobado.