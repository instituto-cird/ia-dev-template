"""
agent/core.py — Núcleo del Agente ReAct.

"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from agent.tools.calculator import calculate
from agent.tools.merchant_lookup import lookup_merchant

logger = logging.getLogger(__name__)

MAX_STEPS = 10

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

ACTIONS_REQUIRING_APPROVAL: set[str] = {
    "delete_record",
    "send_alert",
    "charge_customer",
    "override_threshold",
}

TOOL_REGISTRY: dict[str, Any] = {
    "calculate": calculate,
    "lookup_merchant": lookup_merchant,
}


class AgentStep:
    """Representa un paso del ciclo ReAct."""

    def __init__(self, step: int, thought: str, action: str,
                 action_input: dict[str, Any], observation: str) -> None:
        self.step = step
        self.thought = thought
        self.action = action
        self.action_input = action_input
        self.observation = observation

    def to_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "thought": self.thought,
            "action": self.action,
            "action_input": self.action_input,
            "observation": self.observation,
        }


class AgentResult:
    """Resultado final de una ejecución del agente."""

    def __init__(self, goal: str, answer: str, steps: list[AgentStep],
                 approved: bool = True) -> None:
        self.goal = goal
        self.answer = answer
        self.steps = steps
        self.approved = approved

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "answer": self.answer,
            "steps": [s.to_dict() for s in self.steps],
            "approved": self.approved,
            "total_steps": len(self.steps),
        }


def _parse_llm_response(raw: str) -> tuple[str, str, dict[str, Any]]:
    """Parsea la respuesta del LLM en formato ReAct."""
    try:
        parsed = json.loads(raw)
        thought = parsed.get("thought", "")
        action = parsed.get("action", "")
        action_input = parsed.get("action_input", {})
        if not action:
            raise ValueError("El campo 'action' esta vacio")
        return thought, action, action_input
    except json.JSONDecodeError as e:
        raise ValueError(
            f"El LLM no respondio con JSON valido: {e}\nRespuesta raw: {raw[:200]}"
        ) from e


def _execute_tool(action: str, action_input: dict[str, Any]) -> str:
    """Ejecuta la herramienta registrada bajo `action`."""
    if action not in TOOL_REGISTRY:
        available = ", ".join(TOOL_REGISTRY.keys())
        return f"ERROR: herramienta '{action}' no encontrada. Disponibles: {available}"

    tool_fn = TOOL_REGISTRY[action]
    try:
        result = tool_fn(**action_input)
        return str(result)
    except TypeError as e:
        return f"ERROR: argumentos incorrectos para '{action}': {e}"
    except Exception as e:  # noqa: BLE001
        logger.exception("Error inesperado en herramienta '%s'", action)
        return f"ERROR: {e}"


def run_agent(goal: str, llm_client: Any) -> AgentResult:
    """Ejecuta el ciclo ReAct para alcanzar `goal`."""
    steps: list[AgentStep] = []
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "Eres un agente que resuelve problemas usando herramientas. "
                "Responde SIEMPRE con JSON valido con las claves: thought, action, action_input. "
                f"Herramientas disponibles: {list(TOOL_REGISTRY.keys())}. "
                "Cuando tengas la respuesta final, usa action='FINISH' y pon la respuesta "
                "en action_input={'answer': '...'}."
            ),
        },
        {"role": "user", "content": goal},
    ]

    for step_num in range(1, MAX_STEPS + 1):
        response = llm_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
        )
        raw = response.choices[0].message.content

        try:
            thought, action, action_input = _parse_llm_response(raw)
        except ValueError as e:
            logger.warning("Error parseando respuesta del LLM: %s", e)
            break

        if action in ACTIONS_REQUIRING_APPROVAL:
            return AgentResult(
                goal=goal,
                answer=(
                    f"La accion '{action}' requiere aprobacion de un operador humano "
                    "antes de ejecutarse."
                ),
                steps=steps,
                approved=False,
            )

        if action == "FINISH":
            answer = action_input.get("answer", "El agente termino sin respuesta explicita.")
            steps.append(AgentStep(step_num, thought, action, action_input, answer))
            return AgentResult(goal=goal, answer=answer, steps=steps)

        observation = _execute_tool(action, action_input)
        step = AgentStep(step_num, thought, action, action_input, observation)
        steps.append(step)

        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"Observacion: {observation}"})

    return AgentResult(
        goal=goal,
        answer="El agente alcanzo el limite de pasos sin completar el objetivo.",
        steps=steps,
    )
