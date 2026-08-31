## Diagrama de secuencia: consulta de historial de transacciones

Basado en la Historia 1 y los criterios de aceptación del PRD, este flujo cubre autenticación/autorización, validación de filtros, consulta paginada y manejo de errores sin inventar servicios externos.

```mermaid
sequenceDiagram
    actor Comercio as Comercio o usuario autorizado
    participant API as API LegacyPay
    participant Auth as Validador de identidad y comercio
    participant UC as Caso de uso: Consultar historial
    participant Repo as Repositorio / Base de datos

    Comercio->>API: GET /transactions?fechaDesde=...&fechaHasta=...&estado=...&monto=...&page=1
    API->>Auth: Validar identidad y permisos del comercio
    Auth-->>API: Autorizado / No autorizado

    alt Comercio no autorizado
        API-->>Comercio: 403 Forbidden
    else Comercio autorizado
        API->>UC: Consultar historial(merchantId, filtros, page, pageSize)
        UC->>UC: Validar filtros (fecha <= 90 días, estado, monto, page)
        
        alt Filtros inválidos
            UC-->>API: Error de validación de filtros
            API-->>Comercio: 400 Bad Request con detalle del filtro inválido
        else Filtros válidos
            UC->>Repo: Buscar transacciones del comercio en rango permitido\ncon filtros aplicados\n(offset, limit)
            Repo-->>UC: Transacciones paginadas + total de resultados

            UC->>UC: Excluir campos sensibles (tarjeta completa, autenticación)\nMantener solo campos permitidos

            UC-->>API: Resultado paginado + metadata de página
            API-->>Comercio: 200 OK con historial de transacciones\n(page=1, items, totalPages, etc.)

            Comercio->>API: GET /transactions?...&page=2
            API->>Auth: Validar identidad y permisos del comercio
            Auth-->>API: Autorizado

            API->>UC: Consultar historial(merchantId, filtros, page=2)
            UC->>Repo: Buscar siguiente página con mismo filtro
            Repo-->>UC: Siguiente lote de transacciones
            UC-->>API: Resultado paginado de la página 2
            API-->>Comercio: 200 OK con siguiente página
        end
    end
```

### Observaciones
- La validación de identidad y comercio se realiza en el componente de autorización/validación.
- Los filtros se validan antes de consultar el repositorio, con la restricción de 90 días.
- La consulta es paginada y conserva la misma lógica en páginas subsiguientes.
- La respuesta correcta entrega solo campos permitidos, sin tarjeta completa ni datos de autenticación.
- El flujo alternativo cubre error por comercio no autorizado y error por filtros inválidos.