"""
tests/test_sanity.py — Suite mínima de sanidad del template.

Estos tests deben pasar en verde SIEMPRE, en cualquier ambiente.
Son el "latido" del proyecto: si alguno falla, algo fundamental está roto.

Cobertura:
    - /health endpoint (status + version)
    - Esquema Pydantic de HealthResponse
    - Endpoint raiz /
    - Mock LLM: estructura de respuesta OpenAI-compatible
    - Validacion de entrada invalida (422 Unprocessable Entity)
"""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.main import HealthResponse, app

client = TestClient(app)


# ─── 1. Health endpoint ───────────────────────────────────────────────────────


def test_health_status_ok() -> None:
    """El health check debe retornar status='ok'."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_response_schema() -> None:
    """La respuesta de /health debe cumplir el esquema HealthResponse completo."""
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    # Valida que el JSON puede construir el modelo Pydantic sin errores
    parsed = HealthResponse(**body)
    assert parsed.status == "ok"
    assert isinstance(parsed.version, str) and len(parsed.version) > 0
    assert isinstance(parsed.module, str) and len(parsed.module) > 0


def test_health_version_format() -> None:
    """La version debe tener formato semver (X.Y.Z)."""
    r = client.get("/health")
    version = r.json()["version"]
    parts = version.split(".")
    assert len(parts) == 3, f"Version '{version}' no tiene formato X.Y.Z"
    assert all(p.isdigit() for p in parts), f"Version '{version}' contiene partes no numericas"


# ─── 2. Root endpoint ─────────────────────────────────────────────────────────


def test_root_returns_welcome_message() -> None:
    """El endpoint raiz debe retornar un mensaje de bienvenida."""
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert "message" in body
    assert len(body["message"]) > 0


# ─── 3. Esquema Pydantic ──────────────────────────────────────────────────────


def test_health_response_pydantic_invalid_status() -> None:
    """HealthResponse debe rechazar status vacio."""
    with pytest.raises(ValidationError):
        HealthResponse(status="", version="0.1.0", module="Test")


def test_health_response_pydantic_missing_field() -> None:
    """HealthResponse debe rechazar datos incompletos."""
    with pytest.raises(ValidationError):
        HealthResponse(status="ok")  # type: ignore[call-arg]


# ─── 4. Mock LLM ──────────────────────────────────────────────────────────────


def test_mock_llm_response_structure() -> None:
    """
    El Mock LLM debe retornar una respuesta compatible con la API de OpenAI.

    Usa TestClient (in-process, sin red) para no depender de levantar el servidor
    en otra terminal. Esto permite que el CI valide la respuesta del Mock LLM
    sin coordinar procesos paralelos.
    """
    from app.mock_llm import mock_app

    client = TestClient(mock_app)
    r = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-mock",
            "messages": [{"role": "user", "content": "hola"}],
        },
    )

    assert r.status_code == 200
    body = r.json()

    # Campos obligatorios de la API OpenAI
    assert "choices" in body, "Falta 'choices' en la respuesta del Mock LLM"
    assert len(body["choices"]) > 0
    choice = body["choices"][0]
    assert "message" in choice
    assert "content" in choice["message"]
    assert isinstance(choice["message"]["content"], str)

    # Campos de uso de tokens
    assert "usage" in body
    assert "total_tokens" in body["usage"]


def test_mock_llm_agent_mode_returns_json() -> None:
    """
    Cuando el Mock LLM detecta system prompt de agente (palabras 'thought' y 'action'),
    debe responder con JSON parseable que el motor ReAct pueda procesar.

    Esto es el contrato crítico para Lab 4 — sin esto, el agente falla con JSONDecodeError.
    """
    import json as _json

    from app.mock_llm import mock_app

    client = TestClient(mock_app)
    r = client.post(
        "/v1/chat/completions",
        json={
            "model": "gpt-mock",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Eres un agente. Responde con JSON: thought, action, action_input."
                    ),
                },
                {"role": "user", "content": "Calcula 42 * 7"},
            ],
        },
    )

    assert r.status_code == 200
    content = r.json()["choices"][0]["message"]["content"]
    parsed = _json.loads(content)  # debe ser JSON parseable
    assert "thought" in parsed
    assert "action" in parsed
    assert "action_input" in parsed
