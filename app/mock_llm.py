"""
app/mock_llm.py — Servidor Mock que simula la API de OpenAI Chat Completions.

OBJETIVO
    Permitir que TODOS los Labs (0-4) corran sin necesidad de una API Key real.
    Compatible con `client = OpenAI(base_url="http://localhost:8001/v1", ...)` del SDK oficial.

ENDPOINTS
    POST /v1/chat/completions   — endpoint principal (idéntico al de OpenAI)

MODOS DE RESPUESTA
    1. Modo "agente ReAct": cuando detecta en el system prompt los términos
       'thought', 'action', 'action_input', responde con JSON estructurado
       que el agente del Módulo 4 puede parsear. Ejecuta una herramienta
       basándose en heurísticas simples sobre el último mensaje del usuario.
    2. Modo "conversacional": para Labs 0-3 y experimentación. Devuelve
       texto natural según palabras clave ('plan', 'test', 'refactor').

PARÁMETROS ACEPTADOS
    Acepta `tools`, `tool_choice`, `response_format`, `temperature`, etc.
    Los recibe sin error (Pydantic los valida como opcionales) y los ignora
    o los usa según el modo. No falla con 422 si el cliente envía campos extra.

CÓMO LEVANTARLO
    uv run --frozen uvicorn app.mock_llm:mock_app --port 8001

REFERENCIA
    OpenAI Chat Completions API:
    https://platform.openai.com/docs/api-reference/chat/create
"""

from __future__ import annotations

import json
import re
import time
import uuid
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

mock_app = FastAPI(
    title="Mock OpenAI Service",
    description="Simula OpenAI Chat Completions para los Labs del diplomado IA.",
    version="0.2.0",
)


# ─── Esquemas (compatibles con OpenAI) ───────────────────────────────────────


class Message(BaseModel):
    role: str
    content: str | None = None
    # Opcionales que aparecen en respuestas de tool_use (los aceptamos para no romper)
    name: str | None = None
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None


class ChatCompletionRequest(BaseModel):
    """
    Modelo permisivo: acepta cualquier campo opcional de la API real de OpenAI
    sin fallar (`tools`, `tool_choice`, `response_format`, etc.).
    """

    model: str
    messages: list[Message]
    temperature: float | None = 0.7
    max_tokens: int | None = None
    tools: list[dict[str, Any]] | None = None
    tool_choice: Any | None = None
    response_format: dict[str, Any] | None = None
    stream: bool | None = False
    # Cualquier otro campo desconocido se acepta sin error
    model_config = {"extra": "allow"}


class _Choice(BaseModel):
    index: int
    message: dict[str, Any]
    finish_reason: str


class _Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[_Choice]
    usage: _Usage


# ─── Lógica de decisión: ¿es una llamada de agente? ───────────────────────────


_AGENT_MARKERS = ("thought", "action", "action_input", "react")


def _is_agent_call(messages: list[Message]) -> bool:
    """
    Detecta si la llamada viene del motor ReAct del Módulo 4.

    Heurística: si el system prompt menciona 'thought', 'action' o 'action_input',
    asumimos que el cliente espera respuesta JSON estructurada.
    """
    for msg in messages:
        if msg.role == "system" and msg.content:
            content_lower = msg.content.lower()
            if all(marker in content_lower for marker in ("thought", "action")):
                return True
            if any(marker in content_lower for marker in _AGENT_MARKERS):
                return True
    return False


def _is_prd_agent_call(messages: list[Message]) -> bool:
    """Detecta el contrato del agente RAG del historial de transacciones."""
    return any(
        msg.role == "system"
        and msg.content
        and "buscar_regla_prd" in msg.content
        for msg in messages
    )


# ─── Modo Agente: JSON ReAct ──────────────────────────────────────────────────


def _decide_tool(user_msg: str) -> tuple[str, dict[str, Any], str]:
    """
    Decide qué herramienta usar basándose en el texto del usuario.

    Returns: (action, action_input, thought)
    """
    msg = user_msg.lower()

    # Heurística 1: cálculos matemáticos → calculator
    # Detecta números con operadores (+, -, *, /, x, ^) o palabras 'calcula', 'cuanto'
    has_math_expression = bool(re.search(r"\d\s*[\+\-\*\/x\^]\s*\d", msg)) or bool(
        re.search(r"\d+\s*(por|mas|menos|entre|veces)\s*\d+", msg)
    )
    has_math_keyword = any(w in msg for w in ("calcula", "cuanto", "cuánto", "resultado", "suma", "multiplica"))

    if has_math_expression or has_math_keyword:
        # Intenta extraer la expresión
        match = re.search(r"[\d\s\+\-\*\/x\^\.\(\)]+", user_msg)
        expression = match.group(0).strip() if match else "1+1"
        expression = expression.replace("x", "*")
        return (
            "calculate",
            {"expression": expression},
            "El usuario me pide un calculo matematico. Voy a usar la herramienta calculate.",
        )

    # Heurística 2: lookup de comerciantes → merchant_lookup
    merchant_match = re.search(r"(MCHT[-_]?\d{3,5})", user_msg, re.IGNORECASE)
    if merchant_match or "merchant" in msg or "comerciante" in msg or "comercio" in msg:
        merchant_id = merchant_match.group(1).upper() if merchant_match else "MCHT-00001"
        if "-" not in merchant_id and len(merchant_id) > 4:
            merchant_id = f"MCHT-{merchant_id[4:]}"
        return (
            "lookup_merchant",
            {"merchant_id": merchant_id},
            f"El usuario consulta sobre el comerciante {merchant_id}. Voy a buscarlo.",
        )

    # Heurística 3: terminar (saludos, agradecimientos, mensajes simples)
    if any(w in msg for w in ("gracias", "thanks", "listo", "ok", "fin")):
        return (
            "FINISH",
            {"answer": "Tarea completada."},
            "El usuario indica que esta satisfecho. Termino el ciclo.",
        )

    # Default: terminar con un mensaje genérico
    return (
        "FINISH",
        {"answer": (
            "No puedo identificar una herramienta adecuada para esta consulta. "
            "Por favor reformula tu pregunta indicando un calculo, un merchant_id, "
            "o usa el LLM real (MOCK_MODE=false)."
        )},
        "No tengo una herramienta clara para esta consulta. Termino el ciclo.",
    )


def _agent_response(user_msg: str) -> str:
    """Construye la respuesta JSON ReAct que el agente puede parsear."""
    action, action_input, thought = _decide_tool(user_msg)
    payload = {
        "thought": thought,
        "action": action,
        "action_input": action_input,
    }
    return json.dumps(payload, ensure_ascii=False)


def _prd_agent_response(last_msg: str) -> str:
    """Devuelve una decisión reproducible para el agente RAG local."""
    if last_msg.startswith("Observation:"):
        return json.dumps(
            {
                "thought": "Ya tengo evidencia recuperada del PRD.",
                "action": "final",
                "action_input": {"respuesta": last_msg.removeprefix("Observation: ").strip()},
            },
            ensure_ascii=False,
        )
    return json.dumps(
        {
            "thought": "Necesito evidencia del PRD para responder.",
            "action": "buscar_regla_prd",
            "action_input": {"termino": last_msg},
        },
        ensure_ascii=False,
    )


# ─── Modo Conversacional: texto natural ──────────────────────────────────────


def _conversational_response(user_msg: str) -> str:
    """Respuesta en texto plano para Labs 0-3 y experimentación general."""
    msg_lower = user_msg.lower()

    if "plan" in msg_lower:
        return (
            "Entendido. Aqui esta el plan de ejecucion (Simulado por Mock LLM):\n"
            "1. Analizar requisitos.\n"
            "2. Crear archivo de pruebas.\n"
            "3. Implementar codigo.\n"
            "Procedo?"
        )
    if "test" in msg_lower or "prueba" in msg_lower:
        return (
            "Generando tests con pytest... (Simulacion: Se han creado 3 tests unitarios "
            "cubriendo edge cases. Recuerda que esto es el Mock LLM)."
        )
    if "refactor" in msg_lower:
        return (
            "He detectado complejidad ciclomatica alta. Dividiendo la funcion en tres "
            "componentes mas pequenos... (Simulacion del Mock LLM)."
        )

    return (
        f"Simulacion Mock LLM: recibi tu input '{user_msg[:40]}...'. "
        "Para respuestas mas inteligentes configura un LLM real con MOCK_MODE=false."
    )


# ─── Endpoint principal ───────────────────────────────────────────────────────


@mock_app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest) -> ChatCompletionResponse:
    """Endpoint compatible con OpenAI Chat Completions."""
    if not request.messages:
        last_msg = ""
    else:
        last_msg = request.messages[-1].content or ""

    # Decide el modo de respuesta
    if _is_prd_agent_call(request.messages):
        content = _prd_agent_response(last_msg)
    elif _is_agent_call(request.messages):
        content = _agent_response(last_msg)
    else:
        content = _conversational_response(last_msg)

    response_id = f"chatcmpl-mock-{uuid.uuid4().hex[:12]}"

    return ChatCompletionResponse(
        id=response_id,
        created=int(time.time()),
        model=request.model,
        choices=[
            _Choice(
                index=0,
                message={"role": "assistant", "content": content},
                finish_reason="stop",
            )
        ],
        usage=_Usage(
            prompt_tokens=len(last_msg),
            completion_tokens=len(content),
            total_tokens=len(last_msg) + len(content),
        ),
    )


@mock_app.get("/health")
async def health() -> dict[str, str]:
    """Health check del Mock LLM (útil para verificar que está corriendo)."""
    return {"status": "ok", "service": "mock-llm", "version": "0.2.0"}


@mock_app.get("/")
async def root() -> dict[str, Any]:
    """Info básica del Mock LLM."""
    return {
        "service": "Mock OpenAI Service",
        "version": "0.2.0",
        "endpoints": {
            "/v1/chat/completions": "POST — compatible con OpenAI",
            "/health": "GET — health check",
        },
        "modes": {
            "agent": "Detecta system prompt ReAct y responde JSON con thought/action/action_input",
            "conversational": "Modo texto plano para experimentación general",
        },
        "docs": "Ver app/mock_llm.py o docs/MOCK_LLM_GUIDE.md",
    }


# Permite ejecutar como módulo: `uv run --frozen python -m app.mock_llm`
if __name__ == "__main__":
    import uvicorn
    # Mock LLM debe escuchar todas las interfaces para Docker Compose
    uvicorn.run(mock_app, host="0.0.0.0", port=8001)  # noqa: S104  # nosec B104
