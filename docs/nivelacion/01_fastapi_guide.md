# Nivelación: FastAPI para el Diplomado

> **¿Para quién?** Si venís de Flask, Django, Express o nunca hiciste una API en Python.

---

## ¿Por qué FastAPI y no Flask?

| Característica | Flask | FastAPI |
|---|---|---|
| Validación de entrada | Manual (o WTForms) | Automática con Pydantic |
| Documentación OpenAPI | Plugin externo | Incluida y automática |
| Type hints | Opcionales | Integrados con el framework |
| Async nativo | No (con extensiones) | Sí |
| Performance | Bueno | Muy bueno (comparable a Node.js) |
| Curva de aprendizaje | Baja | Media |

Para el diplomado, la validación automática y la documentación interactiva son
decisivas — el instructor puede ver tu contrato de API en `/docs` sin leer el código.

---

## Anatomía de un endpoint FastAPI

```python
# app/main.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Mi API", version="1.0.0")

# ── Modelos (Contratos de datos) ───────────────────────────────────────────────

class TransactionRequest(BaseModel):
    merchant_id: str = Field(pattern=r"^MCHT-\d{5}$", examples=["MCHT-00001"])
    amount_usd: float = Field(gt=0, description="Monto en USD, mayor que cero")

class TransactionResponse(BaseModel):
    transaction_id: str
    status: str
    message: str

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post(
    "/transactions",
    response_model=TransactionResponse,  # FastAPI valida el output también
    status_code=201,
    tags=["Transactions"],
    summary="Procesa una transaccion",
)
async def create_transaction(body: TransactionRequest) -> TransactionResponse:
    """
    Procesa una transaccion de LegacyPay.

    - El `merchant_id` debe existir en el sistema.
    - El `amount_usd` debe ser positivo.
    - Retorna 422 automaticamente si el body no cumple el schema.
    """
    # FastAPI ya validó que body.merchant_id tiene formato MCHT-NNNNN
    # y que body.amount_usd > 0. No necesitas validar manualmente.

    if body.merchant_id == "MCHT-00099":  # comerciante suspendido en sample data
        raise HTTPException(status_code=403, detail="Comerciante suspendido")

    return TransactionResponse(
        transaction_id="TXN-2026-000001",
        status="approved",
        message=f"Transaccion de {body.amount_usd} USD aprobada",
    )

# ── Query parameters ───────────────────────────────────────────────────────────

@app.get("/merchants", tags=["Merchants"])
async def list_merchants(
    limit: int = Query(default=10, ge=1, le=100),
    status: str | None = Query(default=None, pattern="^(active|suspended)$"),
) -> dict[str, list[str]]:
    """Lista comerciantes. `limit` entre 1-100. `status` opcional."""
    # Implementación real consultaría la DB
    return {"merchants": ["MCHT-00001", "MCHT-00002"]}
```

---

## Documentación interactiva (gratis)

Cuando corres `uv run --frozen uvicorn app.main:app --reload`, FastAPI genera automáticamente:

- **Swagger UI**: `http://localhost:8000/docs` — probar endpoints desde el browser
- **ReDoc**: `http://localhost:8000/redoc` — documentación más limpia para clientes
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` — esquema de la API

Esto es lo que el instructor verifica en la evaluación de M2.

---

## Errores HTTP más comunes

```python
from fastapi import HTTPException

# 400 Bad Request — petición mal formada (que Pydantic no pudo detectar)
raise HTTPException(status_code=400, detail="Fecha fuera de rango")

# 401 Unauthorized — no autenticado
raise HTTPException(status_code=401, detail="Token requerido")

# 403 Forbidden — autenticado pero sin permisos
raise HTTPException(status_code=403, detail="Sin permisos para esta operacion")

# 404 Not Found — recurso no existe
raise HTTPException(status_code=404, detail=f"Comerciante {merchant_id} no encontrado")

# 422 Unprocessable Entity — FastAPI lo genera AUTOMÁTICAMENTE cuando Pydantic falla
# No necesitas lanzarlo manualmente.

# 500 Internal Server Error — FastAPI lo genera cuando hay una excepcion no capturada
# Nunca dejes que llegue a produccion. Usa try/except.
```

---

## TestClient — Tests sin levantar el servidor

```python
# tests/test_transactions.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_transaccion_valida() -> None:
    r = client.post("/transactions", json={
        "merchant_id": "MCHT-00001",
        "amount_usd": 150.0,
    })
    assert r.status_code == 201
    assert r.json()["status"] == "approved"

def test_merchant_invalido_retorna_422() -> None:
    r = client.post("/transactions", json={
        "merchant_id": "INVALIDO",  # No cumple el pattern MCHT-NNNNN
        "amount_usd": 150.0,
    })
    assert r.status_code == 422  # FastAPI lo rechaza automáticamente

def test_merchant_suspendido_retorna_403() -> None:
    r = client.post("/transactions", json={
        "merchant_id": "MCHT-00099",
        "amount_usd": 100.0,
    })
    assert r.status_code == 403
```

---

## Errores típicos en el diplomado (y cómo evitarlos)

**Error 1: Olvidar `response_model`**
```python
# Mal — FastAPI serializa lo que sea que retornes (puede exponer campos internos)
@app.get("/merchant/{id}")
async def get_merchant(id: str):
    return merchant_db[id]  # Puede incluir campos sensibles

# Bien — solo retorna los campos del modelo de respuesta
@app.get("/merchant/{id}", response_model=MerchantPublic)
async def get_merchant(id: str) -> MerchantPublic:
    data = merchant_db[id]
    return MerchantPublic(**data)  # Solo campos públicos
```

**Error 2: Validación manual redundante**
```python
# Mal — Pydantic ya valida esto
@app.post("/tx")
async def create_tx(body: TransactionRequest) -> ...:
    if not body.merchant_id.startswith("MCHT-"):  # Redundante
        raise HTTPException(400, "ID inválido")

# Bien — confía en el schema Pydantic
@app.post("/tx")
async def create_tx(body: TransactionRequest) -> ...:
    # body.merchant_id garantizadamente cumple pattern="^MCHT-\d{5}$"
    ...
```

---

## Recursos

- [FastAPI Tutorial oficial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic v2 — FastAPI integration](https://docs.pydantic.dev/latest/integrations/fastapi/)
