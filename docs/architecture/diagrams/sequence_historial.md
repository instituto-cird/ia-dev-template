# Diagrama de Secuencia · GET /api/v1/transacciones · LegacyPay

> **Escenario A del Lab 2** · versión de referencia canónica.
>
> **Aplicado a la Historia INVEST #1 del PRD:** consultar transacciones recientes.
>
> **Contrato observable:** este diagrama define el flujo que los tests de aceptación deben verificar.

---

## Flujo principal · Happy Path + validaciones + paginación

```mermaid
sequenceDiagram
    autonumber
    participant C as Comercio
    participant A as API (FastAPI)
    participant S as Service
    participant R as Repository
    participant DB as Postgres

    C->>A: GET /api/v1/transacciones?desde=...&hasta=...&estado=approved&page_size=50<br/>Header: Authorization: Bearer {JWT}

    Note over A: Bloque de validación
    A->>A: Verifica firma JWT · extrae comercio_id
    A->>A: Valida query params (Pydantic)
    A->>A: Verifica rango <= 90 días

    alt Rango > 90 días
        A-->>C: 400 Bad Request<br/>{"error": "El rango excede el máximo permitido (90 días)"}
    end

    alt JWT inválido o expirado
        A-->>C: 401 Unauthorized<br/>{"error": "Token inválido"}
    end

    Note over A,DB: Bloque de consulta
    A->>S: obtener_historial(comercio_id, filtros, cursor, page_size)
    S->>R: buscar_por_comercio(comercio_id, filtros, cursor, limit=page_size+1)
    R->>DB: SELECT * FROM transaccion<br/>WHERE comercio_id=? AND created_at BETWEEN ? AND ?<br/>ORDER BY created_at DESC, id DESC<br/>LIMIT 51

    DB-->>R: rows (hasta 51 · el +1 es para saber si hay más páginas)
    R-->>S: rows (deserializadas a Transaccion)
    S->>S: Construir next_cursor si len(rows) > page_size
    S->>S: Enmascarar PAN (dejar solo last4)
    S-->>A: {data: rows[:50], pagination: {next_cursor, has_more}}

    Note over A,C: Respuesta
    A-->>C: 200 OK<br/>{data: [...], pagination: {next_cursor, has_more}}
```

---

## Notas del diagrama

### Trazabilidad con el PRD

| Paso del diagrama | Requisito del PRD |
|-------------------|-------------------|
| Verifica firma JWT · extrae comercio_id | §5 Autenticación + §3 Regla "solo consultar sus propias transacciones" |
| Verifica rango <= 90 días | §5 Retención + §3 Regla "máximo 90 días hacia atrás" |
| Ordena por `created_at DESC · id DESC` | §3 Regla "las más recientes primero" |
| Enmascarar PAN (solo last4) | §5 Cumplimiento PCI-DSS |
| LIMIT 51 (page_size+1) | ADR-0003 · técnica de paginación cursor |
| Respuesta con pagination.next_cursor | §4 Historia 3 + ADR-0003 |

### Auditoría del diagrama con 2 preguntas rápidas

1. **¿Cada mensaje representa una interacción real?** ✅ Los pasos 1-11 son llamadas efectivas (HTTP · función · SQL) · no hay pasos decorativos ni interacciones que la implementación no vaya a ejecutar.
2. **¿Los flujos alternativos (rango > 90 días · JWT inválido) están?** ✅ Los 2 casos negativos están explícitos con las respuestas HTTP esperadas · sirven como base para los tests de casos borde.

### Base para los tests de aceptación

Con este diagrama, los tests unitarios e integración pueden derivarse directamente:

**Tests unitarios (Service · con mocks del Repository):**
- `test_obtener_historial_devuelve_hasta_page_size_elementos`
- `test_obtener_historial_construye_next_cursor_si_hay_mas`
- `test_obtener_historial_enmascara_pan_last4`

**Tests unitarios (validación en API):**
- `test_rango_mayor_a_90_dias_devuelve_400`
- `test_jwt_invalido_devuelve_401`
- `test_desde_mayor_a_hasta_devuelve_400`

**Tests de integración (opcional · reto plus):**
- `test_endpoint_consulta_completa_end_to_end`
- `test_paginacion_no_repite_elementos_entre_paginas`

### Decisión sobre orden de las capas

El diagrama respeta Clean Architecture del PRD:
- **API (Router)** solo maneja HTTP · validaciones de contrato · códigos de respuesta
- **Service** contiene lógica de negocio (construir cursor · enmascarar PAN · aplicar reglas)
- **Repository** único que habla con Postgres

**Test de la separación:** si mañana cambiamos de FastAPI a Django · el Service y Repository no se tocan. ✅

---

*Diagrama de Secuencia · Escenario A · Historial de Transacciones · LegacyPay · Cohorte 2026-I · versión de referencia canónica.*
