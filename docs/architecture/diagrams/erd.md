# ERD — Historial de Transacciones

## Propósito y alcance

Representar de forma simplificada las entidades y relaciones necesarias para consultas y visualización del historial de transacciones. Incluye solo los datos de transacción y referencia a comerciante necesarios para filtros básicos y presentación; no modela datos sensibles ni reglas de autorización.

## Diagrama

```mermaid
erDiagram
    TRANSACTION {
        string transaction_id PK
        string merchant_id FK
        number amount_usd
        string status
        string created_at? "propuesta"
    }

    MERCHANT {
        string merchant_id PK
        string status?
    }

    MERCHANT ||--o{ TRANSACTION : "tiene"
```

## Supuestos

- `transaction_id` es la clave primaria única del historial de transacciones.
- `merchant_id` permite filtrar transacciones por comerciante.
- `amount_usd` y `status` son datos suficientes para la visualización básica del historial.
- `created_at` se incluye como propuesta porque es útil para ordenar y filtrar, pero no está confirmado en el PRD.
- La tabla `MERCHANT` se incluye solo como referencia mínima para evitar transformar un atributo en entidad innecesaria.
- No se incluyen PAN, CVV ni ningún dato de autenticación sensible.

## Preguntas abiertas

- ¿El PRD confirma una entidad `Merchant` o solo una referencia `merchant_id` dentro de `Transaction`?
- ¿Es `created_at` un campo requerido o solo un dato opcional de metadata de historial?
- ¿Qué estados de transacción deben incluirse en el ERD para la vista de historial? ¿`approved`, `declined`, `pending`, otros?
- ¿Se requiere enriquecer el historial con datos de comerciante (nombre, categoría) fuera del ERD?
- ¿Debe existir una entidad separada de auditoría de cambios o el historial de transacciones basta como registro?

### Auditoría del ERD

- ¿Cada entidad está justificada por el PRD? `TRANSACTION` sí, `MERCHANT` está propuesta como referencia mínima.
- ¿La IA convirtió un atributo o estado en tabla? No, se evitó convertir estados de transacción o atributos simples en nuevas entidades.
- ¿Las cardinalidades coinciden con las reglas conocidas? Sí: un comerciante puede tener muchas transacciones.
- ¿Se agregaron entidades o campos no confirmados? Solo `created_at` se marcó como propuesta y `MERCHANT.status` como opcional.
- ¿Aparecen datos sensibles innecesarios? No.
- ¿El diagrama renderiza correctamente? Sí, es un diagrama Mermaid `erDiagram` válido.
- ¿Los supuestos y preguntas abiertas están visibles? Sí.