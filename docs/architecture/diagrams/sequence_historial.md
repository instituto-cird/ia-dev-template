# Diagrama de Secuencia - Historial de Transacciones

```mermaid
sequenceDiagram
    autonumber
    actor Comercio as Comercio / Usuario Autorizado
    participant API as API Gateway / Controlador
    participant Auth as Validador de Autorización
    participant UC as Caso de Uso / Servicio (Historial)
    participant Repo as Repositorio de Transacciones

    Comercio->>API: GET /transactions?fecha_inicio=...&fecha_fin=...&estado=...&monto=...&page=1&limit=20
    activate API

    API->>Auth: Validar Identidad y Permisos (Token/Api-Key)
    activate Auth
    alt Token Inválido o Comercio No Autorizado
        Auth-->>API: Error de Autorización (401/403)
        API-->>Comercio: 401 Unauthorized / 403 Forbidden
    else Autorización Exitosa
        Auth-->>API: Comercio Autorizado (id_comercio)
        deactivate Auth

        API->>UC: Ejecutar Consulta (id_comercio, filtros, paginacion)
        activate UC

        UC->>UC: Validar límites de filtros (Ej: Rango <= 90 días, montos válidos)
        alt Filtros Inválidos (Rango > 90 días o monto negativo)
            UC-->>API: Excepción de Validación de Filtros
            API-->>Comercio: 400 Bad Request (Rango excede 90 días o filtros inválidos)
        else Filtros Válidos
            UC->>Repo: Buscar Transacciones Paginadas (id_comercio, filtros, offset, limit)
            activate Repo
            Repo-->>UC: Lista de Transacciones + Total Registros
            deactivate Repo

            UC->>UC: Formatear Datos (Enmascarar datos sensibles si aplica)
            UC-->>API: Lista de Transacciones + Metadata de Paginación
            deactivate UC
            API-->>Comercio: 200 OK (Transacciones Paginadas)
        end
    end
    deactivate API
```

## Flujos Representados

1. **Validación de Identidad y Comercio:** 
   - El componente `Validador de Autorización` verifica la firma/token del `Comercio`.
   - **Flujo alternativo de error:** Si el token no es válido o el comercio está inactivo/no autorizado, se retorna un error `401 Unauthorized` o `403 Forbidden` (Pasos 3-4).
2. **Validación de Filtros:**
   - El `Caso de Uso / Servicio` valida las reglas del negocio, principalmente que el rango de fechas consultado no sea mayor a 90 días.
   - **Flujo alternativo de error:** Si los filtros no cumplen las reglas de negocio (ej. consultar rango mayor a 90 días), se retorna un error `400 Bad Request` (Pasos 8-9).
3. **Consulta Paginada:**
   - El `Caso de Uso / Servicio` consulta al `Repositorio de Transacciones` pasándole los filtros limpios junto con los parámetros de paginación (`offset`, `limit`).
4. **Respuesta Correcta:**
   - Si todo es correcto, se formatea la respuesta (enmascarando información según sea necesario) y se devuelve una respuesta `200 OK` con la lista de transacciones y metadatos de paginación (Pasos 11-14).
