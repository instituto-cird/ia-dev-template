# Entity Relationship Diagram

```mermaid
erDiagram

    CUSTOMER {
        int customer_id PK
        string name
        string email
    }

    TRANSACTION {
        int transaction_id PK
        float amount
        string status
        int customer_id FK
    }

    SUPPORT_REQUEST {
        int request_id PK
        string description
        string ai_response
        int transaction_id FK
    }

    CUSTOMER ||--o{ TRANSACTION : owns
    TRANSACTION ||--o{ SUPPORT_REQUEST : generates