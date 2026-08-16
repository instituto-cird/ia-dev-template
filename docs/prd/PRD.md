# PRD · Historial de Transacciones · LegacyPay

> **Escenario A del Lab 2** · Cohorte 2026-I · **versión de referencia canónica**
>
> **Autor:** Instituto CIRD *(ejemplo pedagógico)*
> **Fecha:** ago-2026
> **Estado:** aprobado · sirve como input del Lab 3
> **Uso:** referencia para estudiantes que quieran ver una versión canónica · NO reemplaza el trabajo propio del cohorte.

---

## 1. Visión

LegacyPay necesita exponer a los comercios afiliados una vista consultable de las transacciones que procesaron en los últimos 90 días, para que puedan auditar sus movimientos, conciliar contra su sistema contable, y detectar rápidamente inconsistencias sin abrir tickets al soporte.

## 2. Alcance

### IN (dentro del alcance)

- Consulta paginada del historial de transacciones de un comercio
- Filtros por rango de fecha, estado y rango de monto
- Autenticación por token JWT del comercio *(el comercio solo ve SUS transacciones)*
- Respuesta en formato JSON con paginación por cursor
- Endpoint documentado con OpenAPI

### OUT (fuera del alcance)

- Exportación a CSV o Excel *(planificado para v2)*
- Consulta de transacciones anteriores a 90 días *(archivadas · endpoint separado)*
- Modificación o anulación de transacciones *(fuera de este endpoint · va en el módulo de reembolsos)*
- Reportes contables agregados *(Escenario C · fuera de este PRD)*
- Notificaciones push o webhooks sobre transacciones *(módulo aparte)*

## 3. Entidades y Reglas

### Entidades del dominio

- **COMERCIO** · empresa afiliada a LegacyPay que procesa pagos. Identificado por `comercio_id` (UUID). Autenticado con JWT que contiene su ID.
- **TRANSACCION** · movimiento de pago procesado por un comercio. Cada transacción pertenece a UN comercio y tiene UN estado. Atributos clave: monto, fecha, últimos 4 dígitos del PAN, estado, código de autorización.
- **ESTADO** · valor enumerado del ciclo de vida de una transacción. Valores válidos: `pending` · `approved` · `rejected` · `refunded` · `cancelled`. NO es una tabla independiente · es un campo tipado en TRANSACCION.

### Reglas del negocio

- Un comercio **solo puede consultar sus propias transacciones** *(la autorización se verifica contra el JWT · no se acepta `comercio_id` como parámetro público)*
- El rango consultable es de **máximo 90 días hacia atrás desde hoy** *(fechas anteriores devuelven 400 con mensaje explícito)*
- Las transacciones se ordenan por defecto por `created_at DESC` *(las más recientes primero)*
- El monto se maneja siempre en **centavos** (integer) para evitar errores de punto flotante · la respuesta lo devuelve en formato decimal
- Solo se exponen los **últimos 4 dígitos del PAN** (nunca el PAN completo · política PCI-DSS)

## 4. Historias INVEST

### Historia 1 · Consultar transacciones recientes

**Como** comercio afiliado a LegacyPay
**Quiero** obtener las transacciones de mi comercio de los últimos días
**Para** revisar rápidamente el estado de mis pagos sin esperar reportes

**Criterio de aceptación testable:**

- `GET /api/v1/transacciones` con JWT válido responde `200 OK`
- La respuesta es un JSON con array `data` (transacciones) + `pagination` (cursor next/prev + total estimado)
- El `p95 latency` del endpoint es **< 500ms** medido en runtime con 100 req/s
- Las transacciones devueltas pertenecen exclusivamente al comercio identificado por el JWT

### Historia 2 · Filtrar por rango de fecha y estado

**Como** comercio afiliado
**Quiero** filtrar mis transacciones por rango de fechas y por estado
**Para** conciliar contra mi sistema contable en cierres mensuales

**Criterio de aceptación testable:**

- `GET /api/v1/transacciones?desde=2026-07-01&hasta=2026-07-31&estado=approved` responde 200 con solo las transacciones del rango solicitado y estado aprobado
- Si `desde` > `hasta` · responde 400 con mensaje `"El rango de fecha es inválido"`
- Si el rango excede 90 días desde hoy · responde 400 con `"El rango excede el máximo permitido (90 días)"`

### Historia 3 · Paginar resultados largos

**Como** comercio afiliado con alto volumen (5000+ transacciones/mes)
**Quiero** navegar los resultados en páginas de tamaño fijo
**Para** procesar el historial sin timeout ni consumo excesivo de memoria

**Criterio de aceptación testable:**

- `GET /api/v1/transacciones?page_size=50` devuelve máximo 50 elementos
- La respuesta incluye `pagination.next_cursor` cuando hay más resultados · `null` cuando es la última página
- `GET /api/v1/transacciones?page_size=50&cursor={next_cursor}` devuelve la siguiente página · sin repetir elementos
- `page_size` máximo permitido: 200 · valor por defecto: 50 · valores mayores devuelven 400

## 5. Restricciones no funcionales

- **Latencia:** `p95 < 500ms` medido con carga de 100 req/s en horario pico
- **Disponibilidad:** 99.5% mensual *(SLA con comercios)*
- **Retención:** consulta limitada a los últimos 90 días · más antiguo requiere endpoint de archivo separado
- **Autenticación:** JWT firmado con la clave privada de LegacyPay · TTL 1h · refresh disponible en `/auth/refresh`
- **Autorización:** cada comercio solo accede a sus datos · verificado contra el `sub` del JWT
- **Cumplimiento:** solo se exponen los últimos 4 dígitos del PAN · nunca el número completo *(PCI-DSS)*
- **Concurrencia:** el endpoint es de solo lectura · sin locks · escala horizontalmente
- **Cache:** el resultado de un query puede cachearse por 30 segundos con clave `(comercio_id + filtros + cursor)`

## 6. Open Questions

1. **¿Cómo manejamos comercios con múltiples usuarios?** Si un comercio tiene varios usuarios administrando la cuenta, ¿todos pueden consultar todas las transacciones o hay roles con permisos diferenciados? *(pendiente definir con producto · asumimos "todos los usuarios del comercio ven todas las transacciones" en v1)*
2. **¿Qué zona horaria usamos para los filtros de fecha?** Los comercios están en múltiples zonas horarias · ¿se envía el filtro en UTC o en la zona horaria del comercio? *(propuesta: UTC en el endpoint · el frontend hace la conversión · confirmar con producto)*
3. **¿Cómo notificamos cambios en el modelo?** Cuando agreguemos campos nuevos a la respuesta *(ej: nombre del titular)*, ¿cómo comunicamos el cambio a los comercios que consumen la API? *(pendiente definir política de versionado · propuesta: header `X-API-Version` + deprecation warnings)*
4. **¿Necesitamos búsqueda por texto libre en algún campo?** Algunos comercios podrían querer buscar por referencia externa · descripción del cliente · etc. *(fuera de v1 · evaluar en v2 según demanda)*

---

*PRD · Escenario A · Historial de Transacciones · LegacyPay · Cohorte 2026-I · versión de referencia canónica · Instituto CIRD.*
