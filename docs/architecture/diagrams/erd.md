# ERD — Historial de Transacciones

## Propósito y alcance

Representar las entidades mínimas necesarias para consultar el historial de transacciones.

## Diagrama

```mermaid
erDiagram

    MERCHANT ||--o{ TRANSACTION : owns

    MERCHANT {
        string merchant_id
        string merchant_name
    }

    TRANSACTION {
        string transaction_id
        date transaction_date
        decimal amount
        string status
        string currency
    }
```

## Supuestos

- Cada transacción pertenece a un comercio.
- Solo se representan los datos necesarios para consulta.
- No se almacenan datos sensibles.

## Preguntas abiertas

- ¿Qué estados válidos deben mostrarse en el historial?

- ¿Qué filtros deben soportarse: fecha, comercio, estado, moneda o combinación de ellos?

- ¿El historial debe incluir solo transacciones finalizadas o también aquellas en proceso o rechazadas?