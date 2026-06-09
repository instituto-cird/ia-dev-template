"""
tests/test_agent.py — Tests del motor ReAct con MockLLMClient.

Este archivo es el punto de partida para el Golden Set del Lab 4 (Track B).
Mostramos cómo testear el agente sin necesidad de una API Key real, usando
`tests/mocks/mock_llm.py`.

PATRÓN GOLDEN SET
    Cada test define una secuencia de respuestas predefinidas que simulan
    lo que un LLM real diría. El agente se ejecuta contra esas respuestas
    y verificamos:
        - ¿Llegó al FINISH?
        - ¿Usó la herramienta correcta?
        - ¿La respuesta final coincide con lo esperado?
"""

from __future__ import annotations

from agent.core import run_agent
from tests.mocks.mock_llm import MockLLMClient, mock_chat_response

# ─── Tests felices del bucle ReAct ───────────────────────────────────────────


def test_agent_calculate_and_finish() -> None:
    """El agente debe usar `calculate`, recibir el resultado, y terminar con FINISH."""
    client = MockLLMClient(responses=[
        mock_chat_response(
            thought="Necesito calcular 42 * 7.",
            action="calculate",
            action_input={"expression": "42 * 7"},
        ),
        mock_chat_response(
            thought="El resultado es 294. Termino.",
            action="FINISH",
            action_input={"answer": "294"},
        ),
    ])

    result = run_agent("Cuanto es 42 * 7?", client)

    assert result.answer == "294"
    assert result.approved is True
    assert len(result.steps) == 2
    # El paso 1 debe haber usado la herramienta calculate
    assert result.steps[0].action == "calculate"


def test_agent_lookup_merchant_flow() -> None:
    """El agente debe consultar un comerciante y reportar su status."""
    client = MockLLMClient(responses=[
        mock_chat_response(
            thought="El usuario pregunta por MCHT-00001.",
            action="lookup_merchant",
            action_input={"merchant_id": "MCHT-00001"},
        ),
        mock_chat_response(
            thought="El comerciante existe y esta activo.",
            action="FINISH",
            action_input={"answer": "El comerciante MCHT-00001 esta activo."},
        ),
    ])

    result = run_agent("Cual es el estado de MCHT-00001?", client)

    assert "activo" in result.answer.lower()
    assert result.steps[0].action == "lookup_merchant"
    # La observación del paso 1 debe contener datos del merchant
    assert "MCHT-00001" in result.steps[0].observation


# ─── Tests de guardrails / seguridad ─────────────────────────────────────────


def test_agent_blocks_action_requiring_approval() -> None:
    """
    Si el LLM elige una acción en `ACTIONS_REQUIRING_APPROVAL`, el agente
    debe detenerse y reportar approved=False.
    """
    client = MockLLMClient(responses=[
        mock_chat_response(
            thought="Voy a borrar este registro.",
            action="delete_record",  # ← acción que requiere aprobación
            action_input={"id": "TXN-001"},
        ),
    ])

    result = run_agent("Borra el registro TXN-001.", client)

    assert result.approved is False
    assert "aprobacion" in result.answer.lower() or "aprobación" in result.answer.lower()


def test_agent_handles_unknown_tool_gracefully() -> None:
    """Si el LLM inventa una herramienta, el agente registra ERROR y continúa."""
    client = MockLLMClient(responses=[
        mock_chat_response(
            thought="Voy a usar una herramienta que no existe.",
            action="fly_to_mars",
            action_input={},
        ),
        mock_chat_response(
            thought="La herramienta no existe. Termino.",
            action="FINISH",
            action_input={"answer": "No pude completar la tarea."},
        ),
    ])

    result = run_agent("Vuela a Marte.", client)

    assert result.approved is True  # No requiere aprobación, solo es desconocida
    # El paso 1 debe tener observación de tipo ERROR
    assert "ERROR" in result.steps[0].observation
    assert "fly_to_mars" in result.steps[0].observation


# ─── Tests de límites del agente ─────────────────────────────────────────────


def test_agent_max_steps_limit() -> None:
    """
    Si el agente nunca llega a FINISH, debe detenerse tras MAX_STEPS y reportarlo.
    Simulamos un loop que solo invoca calculate indefinidamente.
    """
    # Le damos 20 respuestas iguales — el agente solo procesará MAX_STEPS=10
    loop_response = mock_chat_response(
        thought="Sigo calculando.",
        action="calculate",
        action_input={"expression": "1 + 1"},
    )
    client = MockLLMClient(responses=[loop_response] * 20)

    result = run_agent("Calcula infinitamente.", client)

    assert "limite" in result.answer.lower() or "límite" in result.answer.lower()
    assert len(result.steps) == 10  # MAX_STEPS


def test_mock_client_reset() -> None:
    """`MockLLMClient.reset()` debe permitir reutilizar el mismo cliente."""
    client = MockLLMClient(responses=[
        mock_chat_response(action="FINISH", action_input={"answer": "ok"}),
    ])
    run_agent("test 1", client)
    assert client.call_count == 1

    client.reset()
    assert client.call_count == 0
    run_agent("test 2", client)
    assert client.call_count == 1
