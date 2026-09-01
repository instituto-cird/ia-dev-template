# Secuencia — Consulta de historial de transacciones

## Diagrama

```mermaid
sequenceDiagram
    autonumber
    actor Merchant as Comercio o usuario autorizado
    participant API as API
    participant Auth as Validador de identidad y comercio
    participant Service as Servicio / caso de uso
    participant Repo as Repositorio / base de datos

    Merchant->>API: GET /transactions?merchant_id=...&status=...&page=1&page_size=20
    API->>Auth: validar identidad y permisos del comercio/usuario
    alt usuario o comercio no autorizado
        Auth-->>API: error de autorización
        API-->>Merchant: 403 Forbidden / mensaje de acceso no autorizado
    else autorizado
        Auth-->>API: ok
        API->>Service: consultar historial con filtros y paginación
        Service->>Service: validar parámetros de filtro
        alt filtros inválidos
            Service-->>API: error de validación
            API-->>Merchant: 400 Bad Request / detalle del filtro
        else filtros válidos
            Service->>Repo: query historial por merchant_id, status, page, page_size
            Repo-->>Service: resultados paginados + metadata
            Service-->>API: respuesta de historial
            API-->>Merchant: 200 OK con lista paginada
        end
    end
```

## Supuestos

- La validación de identidad y comercio sucede antes de consultar datos.
- El actor `Merchant` representa a un comercio o usuario autorizado dentro del caso de uso.
- El `Service` es responsable de validar filtros y coordinar la consulta al repositorio.
- La paginación se representa con `page` y `page_size` como parámetros mínimos.
- La base de datos solo responde con los registros necesarios para la consulta.

## Preguntas abiertas

- ¿La API debe devolver 403 o 401 para comercio no autorizado? El PRD no lo define con precisión.
- ¿`status` es un único valor o un conjunto de estados permitidos para el filtro?
- ¿La consulta exige ordenamiento explícito por fecha más reciente primero?
- ¿La respuesta debe incluir metadata de paginación adicional, como `total_pages` o `total_records`?

### Auditoría de la secuencia

- ¿La autorización ocurre antes de consultar datos? Sí, en el flujo principal se valida antes de acceder a la consulta.
- ¿Cada participante está justificado? Sí: comercio, API, validador, servicio y repositorio.
- ¿El orden de mensajes es coherente? Sí, respetando validación, filtros y consulta paginada.
- ¿Existe al menos un flujo de error? Sí, hay rama de autorización y rama de filtros inválidos.
- ¿Coincide con el PRD y el ERD? Sí, se consulta transacciones por comercio y se usa paginación.
- ¿El diagrama renderiza? Sí, el bloque Mermaid es sintácticamente válido.

