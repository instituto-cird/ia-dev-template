# Nivelación: Python Esencial para el Diplomado

> **¿Para quién?** Si llevas menos de 1 año usando Python, o si nunca has usado
> type hints, Pydantic o pytest. Tiempo estimado: 2-3 horas.
>
> Esto NO es un tutorial de Python. Es la lista mínima de conceptos que aparecen
> en el código del diplomado desde el Día 1.

---

## 1. Type hints (anotaciones de tipo)

El código del diplomado usa type hints en todos los parámetros y retornos.
mypy las valida. Si no las usas, el CI falla.

```python
# Sin type hints (no usar en este diplomado)
def sumar(a, b):
    return a + b

# Con type hints (estándar del curso)
def sumar(a: int, b: int) -> int:
    return a + b

# Tipos comunes que verás:
from typing import Any

x: str = "hola"
y: int = 42
z: float = 3.14
lista: list[str] = ["a", "b"]
diccionario: dict[str, Any] = {"key": "value"}
opcional: str | None = None          # Python 3.10+: equivale a Optional[str]
```

**Regla del diplomado:** Toda función en `app/` y `agent/` debe tener type hints.
Si mypy reporta un error de tipo, es un bug potencial.

---

## 2. Pydantic v2 — Modelos de datos con validación

Pydantic es la columna vertebral del diplomado. FastAPI la usa internamente.
La versión 2 tiene sintaxis diferente a la v1 — no mezcles ejemplos.

```python
from pydantic import BaseModel, Field, field_validator

# Modelo básico
class Merchant(BaseModel):
    merchant_id: str
    name: str
    daily_limit_usd: float
    status: str = "active"  # valor por defecto

# Con validaciones
class Transaction(BaseModel):
    merchant_id: str = Field(pattern=r"^MCHT-\d{5}$")  # regex
    amount_usd: float = Field(gt=0, le=100_000)         # mayor que 0, hasta 100k
    currency: str = "USD"

    @field_validator("currency")
    @classmethod
    def must_be_uppercase(cls, v: str) -> str:
        if v != v.upper():
            raise ValueError(f"Moneda debe ser mayusculas, recibio: {v}")
        return v

# Uso
t = Transaction(merchant_id="MCHT-00001", amount_usd=150.0)
print(t.model_dump())  # v2: model_dump() en lugar de dict()

# Validación que falla → lanza ValidationError
from pydantic import ValidationError
try:
    bad = Transaction(merchant_id="INVALIDO", amount_usd=-5)
except ValidationError as e:
    print(e.errors())
```

**Por qué importa:** Cuando FastAPI recibe un POST con JSON inválido, Pydantic
lo rechaza automáticamente con un 422 Unprocessable Entity antes de que tu
código lo procese. Esto elimina una clase entera de bugs de validación.

---

## 3. async/await — Funciones asíncronas

FastAPI es asíncrono. Necesitas entender la diferencia entre funciones sync y async.

```python
import asyncio
import httpx  # cliente HTTP async

# Función síncrona (bloquea el hilo mientras espera)
def get_data_sync(url: str) -> str:
    import requests
    return requests.get(url).text  # Bloqueante

# Función asíncrona (libera el hilo mientras espera I/O)
async def get_data_async(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text  # No bloquea

# En FastAPI, usa async def para I/O (DB, APIs externas)
# y def para cálculos puros (sin I/O)
from fastapi import FastAPI
app = FastAPI()

@app.get("/data")
async def endpoint_con_io() -> dict[str, str]:
    # Aquí harías: await db.fetch(...) o await http_client.get(...)
    return {"data": "ok"}

@app.get("/compute")
def endpoint_sin_io() -> dict[str, int]:
    resultado = sum(range(1_000_000))  # CPU puro, sin I/O
    return {"resultado": resultado}
```

**Regla práctica para el diplomado:**
- Endpoints que llaman al LLM o a una DB → `async def`
- Funciones de cálculo puro (como `calculate()` en `agent/tools/`) → `def`

---

## 4. pytest — Tests que el CI ejecuta

El CI corre `pytest` en cada push. Un test que falla = CI rojo = PR bloqueado.

```python
# tests/test_mi_modulo.py

import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Test básico
def test_endpoint_retorna_200() -> None:
    r = client.get("/health")
    assert r.status_code == 200

# Test con dato parametrizado
@pytest.mark.parametrize("merchant_id,esperado", [
    ("MCHT-00001", True),
    ("INVALIDO",   False),
    ("",           False),
])
def test_merchant_id_valido(merchant_id: str, esperado: bool) -> None:
    import re
    patron = re.compile(r"^MCHT-\d{5}$")
    assert bool(patron.match(merchant_id)) == esperado

# Test que espera una excepción
def test_pydantic_rechaza_monto_negativo() -> None:
    from pydantic import ValidationError
    from app.main import HealthResponse
    with pytest.raises(ValidationError):
        HealthResponse(status="", version="0.1.0", module="Test")

# Test async (requiere pytest-asyncio)
import pytest_asyncio

@pytest.mark.asyncio
async def test_algo_async() -> None:
    import asyncio
    await asyncio.sleep(0)  # placeholder
    assert True
```

**Cómo correr tests localmente:**
```bash
uv run pytest -q                           # Todos los tests
uv run pytest tests/test_sanity.py -v     # Un archivo específico
uv run pytest -k "test_health" -v         # Tests que contengan "test_health"
uv run pytest --cov=app --cov-report=term-missing  # Con cobertura
```

---

## 5. Manejo de errores — Lo que NO debes hacer

```python
# MAL — captura todo y lo ignora (AI Code Smell #1)
try:
    resultado = llm_client.call()
except:
    pass  # nunca hagas esto

# MAL — captura Exception sin loggear
try:
    resultado = llm_client.call()
except Exception:
    return None  # el error desaparece

# BIEN — captura específica con logging
import logging
logger = logging.getLogger(__name__)

try:
    resultado = llm_client.call()
except httpx.TimeoutException:
    logger.warning("LLM timeout — usando fallback")
    return {"error": "timeout", "fallback": True}
except httpx.HTTPStatusError as e:
    logger.error("LLM HTTP error: %s", e.response.status_code)
    raise  # re-lanza para que FastAPI devuelva 500
```

---

## Recursos para profundizar

- [Real Python — Type Hints](https://realpython.com/python-type-checking/)
- [Pydantic v2 docs](https://docs.pydantic.dev/latest/)
- [pytest docs](https://docs.pytest.org/en/stable/)
- [FastAPI — tutorial oficial](https://fastapi.tiangolo.com/tutorial/)
