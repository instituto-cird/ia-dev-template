# Diagrama de Secuencia — Consulta de Historial de Transacciones

## 1. Propósito y Alcance

Este documento describe la interacción dinámica y el flujo de mensajes entre los componentes del sistema para resolver la historia de usuario **HU-01 (Consulta Paginada de Historial de Transacciones con Filtros)**.

El diagrama representa la validación de seguridad (autenticación B2B), la validación de parámetros de filtro (rango de 90 días, fechas, montos), la consulta paginada en la base de datos, la respuesta exitosa (200 OK) y los flujos alternativos de error (401 Unauthorized y 400 Bad Request).

---

## 2. Diagrama de Secuencia (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor Comercio as Comercio Autorizado
    participant API as API Gateway / Router
    participant Auth as Servicio de Autorización
    participant Service as Servicio de Historial (UseCase)
    participant DB as Repositorio / Base de Datos

    %% Flujo 1: Petición Inicial
    Comercio->>API: GET /api/v1/transacciones/historial (filtros, paginación, Token B2B)
    
    %% Flujo 2: Autenticación y Autorización
    API->>Auth: Validar Token y Permisos(token, id_comercio)
    alt Token Inválido o No Autorizado
        Auth-->>API: 401 Unauthorized (Token expirado o inválido)
        API-->>Comercio: HTTP 401 Unauthorized { error: "Acceso no autorizado" }
    else Token Válido
        Auth-->>API: 200 OK (Comercio autenticado)
        
        %% Flujo 3: Validación de Filtros
        API->>Service: consultarHistorial(id_comercio, filtros_fecha, estado, monto, page, page_size)
        
        alt Rango de Fechas Excede 90 Días o Filtro Inválido
            Service-->>API: ErrorValidacion ("Rango de fechas superior a 90 días")
            API-->>Comercio: HTTP 400 Bad Request { error: "El rango máximo de consulta es 90 días" }
        else Filtros Válidos
            
            %% Flujo 4: Consulta Paginada a BD
            Service->>DB: executeQuery(id_comercio, fecha_desde, fecha_hasta, estado, monto, limit, offset)
            DB-->>Service: List<TransaccionData> (Datos sintéticos + masked_pan) + Count Total
            
            %% Flujo 5: Respuesta Exitosa
            Service-->>API: HistorialPaginatedResponse (items, total_pages, current_page)
            API-->>Comercio: HTTP 200 OK { data: [...], pagination: { ... } }
        end
    end
```

---

## 3. Justificación de Participantes y Flujos

1. **Comercio Autorizado (Actor):** Usuario B2B autenticado que inicia la solicitud de consulta con parámetros de filtro y token.
2. **API Gateway / Router:** Punto de entrada que enruta la solicitud y retorna las respuestas HTTP estandarizadas.
3. **Servicio de Autorización:** Componente encargado de verificar la validez del token B2B y asegurar el aislamiento entre comercios.
4. **Servicio de Historial (Caso de Uso):** Aplica la lógica de negocio, valida que el rango de fechas no supere los 90 días naturales y gestiona el cálculo de paginación (`limit` / `offset`).
5. **Repositorio / BD:** Almacena y recupera los datos de las transacciones (sin exponer PAN ni CVV).

---

## 4. Auditoría y Coherencia

- **Seguridad primero:** Se garantiza que la autorización de la petición ocurre de forma síncrona **antes** de invocar cualquier consulta a la base de datos.
- **Flujos Alternativos:** Se incluyen dos caminos de excepción claros (HTTP 401 por falla de token y HTTP 400 por violar la regla de 90 días o filtros inválidos).
- **Consistencia:** Los atributos devueltos en la respuesta coinciden estrictamente con la entidad `TRANSACCION` definida en `erd.md` y `PRD.md`.
