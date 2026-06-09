"""
tests/mocks/mock_llm.py — Cliente LLM simulado in-process para tests deterministas.

USO
    Para tests del agente Track B y del Golden Set del Lab 4. A diferencia del
    Mock HTTP en `app/mock_llm.py`, este cliente es in-process (no requiere
    levantar un servidor) y permite controlar exactamente qué respuestas
    devuelve el "LLM" en cada llamada.

EJEMPLO
    >>> from tests.mocks.mock_llm import MockLLMClient, mock_chat_response
    >>> client = MockLLMClient(responses=[
    ...     mock_chat_response(thought="Voy a calcular.", action="calculate",
    ...                        action_input={"expression": "42 * 7"}),
    ...     mock_chat_response(thought="Listo.", action="FINISH",
    ...                        action_input={"answer": "294"}),
    ... ])
    >>> from agent.core import run_agent
    >>> result = run_agent("Cuanto es 42 * 7?", client)
    >>> result.answer
    '294'

API COMPATIBLE
    El cliente expone `.chat.completions.create(...)` igual que el SDK de
    `openai`, por lo que cualquier código que reciba un `OpenAI()` real
    funciona también con este mock.
"""

from __future__ import annotations

import json
from typing import Any

# ─── Tipos que simulan los del SDK de openai ──────────────────────────────────


class _MockChoice:
    """Replica la forma de `response.choices[0]`."""

    def __init__(self, message_content: str) -> None:
        self.index = 0
        self.message = _MockMessageBody(content=message_content)
        self.finish_reason = "stop"


class _MockMessageBody:
    """Replica `response.choices[0].message`."""

    def __init__(self, content: str) -> None:
        self.role = "assistant"
        self.content = content
        self.tool_calls: list[Any] | None = None


class _MockUsage:
    """Replica `response.usage`."""

    def __init__(self, prompt: int, completion: int) -> None:
        self.prompt_tokens = prompt
        self.completion_tokens = completion
        self.total_tokens = prompt + completion


class MockMessage:
    """
    Una respuesta predefinida del Mock LLM.

    Atributos:
        choices: lista con UN _MockChoice (formato OpenAI)
        usage: estadísticas de tokens (estimadas)
        model: nombre del modelo simulado
        id: identificador único de la respuesta
    """

    def __init__(self, content: str, *, model: str = "mock-llm-v2") -> None:
        self.id = f"chatcmpl-mock-{id(self) % 1_000_000:06d}"
        self.object = "chat.completion"
        self.model = model
        self.choices = [_MockChoice(message_content=content)]
        self.usage = _MockUsage(prompt=len(content) // 4, completion=len(content) // 4)


def mock_chat_response(
    *,
    thought: str = "",
    action: str = "FINISH",
    action_input: dict[str, Any] | None = None,
    text: str | None = None,
) -> MockMessage:
    """
    Construye una `MockMessage` con el formato JSON ReAct esperado por `agent.core`.

    Usá `text=...` si querés devolver texto plano (modo conversacional, no agente).
    Si pasás `text`, los demás kwargs se ignoran.

    Args:
        thought:      Razonamiento simulado del modelo (campo `thought` del JSON).
        action:       Herramienta a invocar, o "FINISH" para terminar.
        action_input: Argumentos de la herramienta (o `{"answer": "..."}` si FINISH).
        text:         Texto plano para modo no-agente (sobrescribe los demás).

    Returns:
        `MockMessage` lista para ser retornada por el `MockLLMClient`.
    """
    if text is not None:
        return MockMessage(content=text)

    payload = {
        "thought": thought,
        "action": action,
        "action_input": action_input or {},
    }
    return MockMessage(content=json.dumps(payload, ensure_ascii=False))


# ─── Cliente Mock que reemplaza a `openai.OpenAI()` en tests ─────────────────


class _MockChatNamespace:
    """Implementa `client.chat.completions`."""

    def __init__(self, parent: MockLLMClient) -> None:
        self.completions = _MockCompletionsNamespace(parent)


class _MockCompletionsNamespace:
    """Implementa `client.chat.completions.create()`."""

    def __init__(self, parent: MockLLMClient) -> None:
        self._parent = parent

    def create(self, **kwargs: Any) -> MockMessage:
        return self._parent._next_response()


class MockLLMClient:
    """
    Cliente LLM simulado in-process, compatible con la API del SDK de OpenAI.

    Reemplaza a `from openai import OpenAI; client = OpenAI(...)`.
    No hace llamadas de red — devuelve respuestas predefinidas en orden.

    Cuando se agotan las respuestas predefinidas, devuelve un FINISH genérico
    para evitar loops infinitos en los tests.

    Args:
        responses: lista de `MockMessage` predefinidas (orden FIFO).
                   Si está vacío, usa `_DEFAULT_RESPONSES` con un escenario
                   simple de "calcula y termina".
    """

    # Respuestas por defecto para un escenario mínimo de prueba
    _DEFAULT_RESPONSES: list[MockMessage] = [
        mock_chat_response(
            thought="El usuario me hizo una consulta. Voy a usar la calculadora.",
            action="calculate",
            action_input={"expression": "1 + 1"},
        ),
        mock_chat_response(
            thought="Ya tengo el resultado. Termino el ciclo.",
            action="FINISH",
            action_input={"answer": "2"},
        ),
    ]

    def __init__(self, responses: list[MockMessage] | None = None) -> None:
        self._responses: list[MockMessage] = list(responses) if responses else list(self._DEFAULT_RESPONSES)
        self._call_count = 0
        # Interfaz tipo OpenAI: client.chat.completions.create(...)
        self.chat = _MockChatNamespace(self)

    def _next_response(self) -> MockMessage:
        """Devuelve la siguiente respuesta predefinida (o FINISH genérico si se agotaron)."""
        if self._call_count < len(self._responses):
            response = self._responses[self._call_count]
        else:
            response = mock_chat_response(
                thought="Se agotaron las respuestas predefinidas del mock.",
                action="FINISH",
                action_input={"answer": "El mock se quedo sin respuestas."},
            )
        self._call_count += 1
        return response

    def reset(self) -> None:
        """Reinicia el contador para reutilizar el mismo cliente en múltiples tests."""
        self._call_count = 0

    @property
    def call_count(self) -> int:
        """Cuántas veces se llamó a `.chat.completions.create()`."""
        return self._call_count
