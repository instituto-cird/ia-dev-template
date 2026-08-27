"""Loop ReAct para responder consultas sobre el PRD."""

from __future__ import annotations

import json
import os
from typing import Any

from app.agent.logger import log_step
from app.agent.tools import TOOLS_SCHEMA, buscar_regla_prd


# Baranda de presupuesto: impide loops infinitos si el 
MAX_STEPS = 5
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# El prompt fija alcance, seguridad y el JSON que el loop puede interpretar.
# Baranda #1 · SCOPE · en el SYSTEM_PROMPT 
SYSTEM_PROMPT = (
    "Sos un agente RAG sobre el PRD de Historial de Transacciones LegacyPay. "
    "Solo respondés sobre el PRD; si te preguntan otra cosa decís 'fuera de alcance'. "
    "NO ejecutás acciones destructivas. NO inventás resultados. "
    "Decidí en cada iteración si necesitás buscar evidencia o si ya podés responder. "
    "Respondé siempre JSON válido con las claves thought, action y action_input. "
    "action debe ser 'buscar_regla_prd' o 'final'. "
    "Para buscar_regla_prd, action_input debe ser {'termino': '...'}. "
    "Para final, action_input debe ser {'respuesta': '...'}."
)

_TOOL_REGISTRY = {"buscar_regla_prd": buscar_regla_prd}


def _parse_decision(content: str) -> tuple[str, dict[str, Any]]:
    """Valida y devuelve la acción y sus argumentos."""
    try:
        decision = json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError("El LLM no devolvio JSON valido.") from error

    action = decision.get("action")
    action_input = decision.get("action_input")
    if action not in {"buscar_regla_prd", "final"}:
        raise ValueError("La accion del LLM no es valida.")
    if not isinstance(action_input, dict):
        raise ValueError("action_input debe ser un objeto JSON.")
    return action, action_input


def run_agent(consulta: str, llm_client: Any) -> str:
    """Ejecuta el loop ReAct y devuelve la respuesta final o un error."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": consulta},
    ]

    # Cada vuelta representa Reason -> Act -> Observe; el LLM conserva la decisión.
    for step in range(1, MAX_STEPS + 1):
        response = llm_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            temperature=0,
        )
        content = response.choices[0].message.content or ""
        try:
            action, action_input = _parse_decision(content)
        except ValueError as error:
            return f"Error del agente: {error}"

        # Una respuesta final no ejecuta tools ni genera una observación adicional.
        if action == "final":
            return str(action_input.get("respuesta", ""))

        termino = action_input.get("termino")
        if not isinstance(termino, str):
            observation = "Error: 'termino' debe ser un string."
        else:
            observation = _TOOL_REGISTRY[action](termino)
        # La observación vuelve al historial para que el LLM decida el siguiente paso.
        log_step(step, action, action_input, observation)
        messages.append({"role": "assistant", "content": content})
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "Error: se alcanzo MAX_STEPS sin una respuesta final."