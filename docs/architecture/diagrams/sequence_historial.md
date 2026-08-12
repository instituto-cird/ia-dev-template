# Diagrama de Secuencia: Historial de Transacciones

Este diagrama representa el flujo de consulta del historial de transacciones basado en la **Historia de Usuario 1** del PRD: *Consulta paginada del historial de transacciones*. Cumple con las reglas de negocio de privacidad de datos, limitación de antigüedad y aislamiento por comercio.

```mermaid
sequenceDiagram
    autonumber
    actor C as Comercio / Usuario Autorizado
    participant API as API
    participant Auth as Autorización / Validación
    participant CU as Servicio (Caso de Uso)
    participant BD as Repositorio / Base de Datos

    C->>API: GET /transacciones?fecha_inicio={fecha}&page=1&size=20
    
    %% Validación de identidad y comercio
    API->>Auth: Validar credenciales y permisos
    alt No Autorizado
        Auth-->>API: Token inválido o comercio no habilitado
        API-->>C: 401 Unauthorized / 403 Forbidden
    else Autorizado
        Auth-->>API: Identidad válida (merchant_id)
        
        %% Validación de filtros
        API->>CU: obtener_historial_paginado(merchant_id, filtros, paginacion)
        CU->>CU: Validar reglas de negocio (ej. antigüedad <= 90 días)
        
        alt Filtros inválidos (> 90 días)
            CU-->>API: Error de validación (Límite de tiempo excedido)
            API-->>C: 400 Bad Request (Error de validación)
        else Filtros válidos
            %% Consulta paginada y filtrada por comercio (Aislamiento)
            CU->>BD: buscar_transacciones(merchant_id, filtros, limit, offset)
            BD-->>CU: Transacciones (datos crudos) + Total de registros
            
            %% Limpieza de datos
            CU->>CU: Enmascarar número de tarjeta y excluir credenciales
            
            %% Respuesta correcta
            CU-->>API: Resultados procesados y metadatos de paginación
            API-->>C: 200 OK (Lista segura de transacciones)
        end
    end
```
