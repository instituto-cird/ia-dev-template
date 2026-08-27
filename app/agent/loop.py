from __future__ import annotations

import json
import os
from typing import Any

from app.agent.logger import log_step
from app.agent.tools import TOOLS_SCHEMA, buscar_regla_prd

# baranda 1: cantidad limite de pasos del agente
MAX_STEPS = 5
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# baranda 2: prompt del sistema para el agente, se delimita que solo responda sobre el PRD 
# y que no ejecute acciones destructivas ni invente resultados. 
SYSTEM_PROMPT = (
    "Sos un agente RAG para el Historial de Transacciones de LegacyPay. "
    "Solo respondés sobre el PRD; si te preguntan otra cosa decís "
    "'fuera de alcance'. NO ejecutás acciones destructivas. "
    "NO inventás resultados. "
    "En cada turno respondé únicamente JSON válido con las claves "
    "'thought', 'action' y 'action_input'. "
    "'action' debe ser 'buscar_regla_prd' o 'final'. "
    "Para buscar, action_input es {'termino': '...'}. "
    "Para finalizar, action_input es {'respuesta': '...'}. "
    "Usá la evidencia de las observaciones para responder."
)

_TOOL_REGISTRY = {"buscar_regla_prd": buscar_regla_prd}


def _parse_decision(raw: str) -> tuple[str, dict[str, Any]]:
    try:
        decision = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("El LLM no devolvió JSON válido.") from error

    action = decision.get("action")
    action_input = decision.get("action_input")
    if action not in {"buscar_regla_prd", "final"}:
        raise ValueError("La decisión contiene una acción no permitida.")
    if not isinstance(action_input, dict):
        raise ValueError("'action_input' debe ser un objeto JSON.")
    return action, action_input


def _call_llm(llm_client: Any, messages: list[dict[str, str]], model: str) -> str:
    response = llm_client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS_SCHEMA,
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("El LLM devolvió una respuesta vacía.")
    return content


def run_agent(question: str, llm_client: Any, model: str = DEFAULT_MODEL) -> str:
    """Ejecuta el loop ReAct y devuelve la respuesta final del agente."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, MAX_STEPS + 1):
        try:
            raw_decision = _call_llm(llm_client, messages, model)
            action, action_input = _parse_decision(raw_decision)
        except (ValueError, KeyError) as error:
            return f"Error del agente: {error}"

        if action == "final":
            respuesta = action_input.get("respuesta")
            if not isinstance(respuesta, str):
                return "Error del agente: la respuesta final no es un texto válido."
            return respuesta

        termino = action_input.get("termino")
        if not isinstance(termino, str):
            observation = "ERROR: 'termino' debe ser un texto."
        else:
            try:
                observation = _TOOL_REGISTRY[action](termino=termino)
            except Exception as error:  # noqa: BLE001
                observation = f"ERROR al ejecutar {action}: {error}"

        log_step(step, action, action_input, observation)
        messages.append(
            {
                "role": "user",
                "content": f"Observation: {observation}",
            }
        )

    return f"Error del agente: se alcanzó el límite de {MAX_STEPS} pasos sin respuesta final."
