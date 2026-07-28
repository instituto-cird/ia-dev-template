# ERD — Historial de Transacciones

## Propósito y alcance

El propósito de este modelo de datos lógico es soportar la consulta del historial de transacciones para comercios autorizados dentro de la ventana de los últimos 90 días, incluyendo filtros por fecha, estado y monto, garantizando la protección de datos sensibles mediante el enmascaramiento de información y la auditoría de accesos.

## Diagrama

```mermaid
erDiagram
    COMERCIO ||--o{ TRANSACCION : "posee / gestiona"
    TRANSACCION ||--|| DATOS_PAGO_ENMASCARADO : "contiene"
    COMERCIO ||--o{ AUDITORIA_CONSULTA : "ejecuta"

    COMERCIO {
        string id_comercio PK
        string razon_social
        string ruc_identificacion
        string estado_comercio "ACTIVO | INACTIVO"
        datetime fecha_registro
    }

    TRANSACCION {
        string id_transaccion PK
        string id_comercio FK
        decimal monto "Soporta filtro por monto"
        string moneda "Ej: USD, PYG, EUR"
        string estado "APROBADA | RECHAZADA | PENDIENTE | REVERTIDA"
        datetime fecha_transaccion "Soporta filtro <= 90 dias"
        string referencia_orden
        string codigo_autorizacion
    }

    DATOS_PAGO_ENMASCARADO {
        string id_datos_pago PK
        string id_transaccion FK
        string tipo_metodo "TARJETA_CREDITO | TARJETA_DEBITO"
        string marca_tarjeta "VISA | MASTERCARD | AMEX"
        string ultimos_cuatro_digitos "Ej: 1234 (Sin exponer PAN)"
        string titular_enmascarado "Ej: J*** D**"
    }

    AUDITORIA_CONSULTA {
        string id_log_consulta PK
        string id_comercio FK
        datetime fecha_consulta
        string filtro_estado
        datetime filtro_fecha_inicio
        datetime filtro_fecha_fin
        decimal filtro_monto_min
        decimal filtro_monto_max
        int numero_pagina
        int registros_por_pagina
    }
```

## Supuestos

1. Cada comercio posee un identificador único `id_comercio` y un estado operacional.
2. Los datos de pago confidenciales (como el PAN completo o CVV) nunca se almacenan en este modelo; en su lugar, se asocian a un registro enmascarado `DATOS_PAGO_ENMASCARADO` para la visualización segura del comercio.
3. Se registran auditorías de consulta (`AUDITORIA_CONSULTA`) para cumplir con los requisitos de trazabilidad y seguridad operativa en cada solicitud.

## Preguntas abiertas

1. ¿Se requiere indexar el campo `referencia_orden` para búsquedas directas en el historial?
2. ¿Qué longitud exacta deben tener las descripciones de los estados de transacción?
