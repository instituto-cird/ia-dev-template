"""
agent/core.py — Núcleo del Agente ReAct.

Este módulo implementa el ciclo Reason → Act → Observe (ReAct) del Módulo 4.

FLUJO:
    1. El agente recibe un objetivo (goal) del usuario.
    2. Razona (Reason): elige qué herramienta usar y con qué argumentos.
    3. Actúa   (Act):    ejecuta la herramienta seleccionada.
    4. Observa (Observe): recibe el resultado y decide si continúa o termina.
    5. Repite hasta alcanzar el objetivo o superar MAX_STEPS.

TRACK B — REQUISITOS MÍNIMOS:
    - Al menos 3 herramientas con lógica propia (ver agent/tools/).
    - Golden Set con >= 80% de casos deterministas pasando.
    - ACTIONS_REQUIRING_APPROVAL: lista de acciones que requieren confirmación humana.
    - AI_USAGE.md documentando cada decisión de diseño asistida por IA.

REFERENCIA: Pattern "ReAct" (Yao et al., 2022) — https://arxiv.org/abs/2210.03629
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

# Herramientas disponibles para el agente — importa las tuyas aquí
from agent.tools.calculator import calculate
from agent.tools.merchant_lookup import lookup_merchant

logger = logging.getLogger(__name__)

# ─── Configuración ────────────────────────────────────────────────────────────

MAX_STEPS = 10  # Límite de iteraciones para evitar loops infinitos

# Nombre del modelo a usar. El Mock LLM lo ignora. Para LLM real, configurar
# LLM_MODEL en .env (ej: "gpt-4o-mini", "claude-sonnet-4-6", "llama3.2:3b").
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Acciones que requieren confirmación explícita del operador humano
# antes de ejecutarse. Modifica esta lista según tu dominio.
ACTIONS_REQUIRING_APPROVAL: set[str] = {
    "delete_record",
    "send_alert",
    "charge_customer",
    "override_threshold",
}

# Registro de herramientas disponibles: nombre → función callable
TOOL_REGISTRY: dict[str, Any] = {
    "calculate": calculate,
    "lookup_merchant": lookup_merchant,
    # Agrega tus herramientas aquí:
    # "nombre_herramienta": mi_funcion,
}


# ─── Tipos de datos ───────────────────────────────────────────────────────────


class AgentStep:
    """Representa un paso del ciclo ReAct."""

    def __init__(
        self,
        step: int,
        thought: str,
        action: str,
        action_input: dict[str, Any],
        observation: str,
    ) -> None:
        self.step = step
        self.thought = thought          # Razonamiento del modelo
        self.action = action            # Herramienta elegida
        self.action_input = action_input  # Argumentos para la herramienta
        self.observation = observation  # Resultado de ejecutar la herramienta

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

    def __init__(
        self,
        goal: str,
        answer: str,
        steps: list[AgentStep],
        approved: bool = True,
    ) -> None:
        self.goal = goal
        self.answer = answer        # Respuesta final al usuario
        self.steps = steps          # Historial del ciclo ReAct
        self.approved = approved    # False si se detuvo por requerir aprobación humana

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal": self.goal,
            "answer": self.answer,
            "steps": [s.to_dict() for s in self.steps],
            "approved": self.approved,
            "total_steps": len(self.steps),
        }


# ─── Motor del agente ─────────────────────────────────────────────────────────


def _parse_llm_response(raw: str) -> tuple[str, str, dict[str, Any]]:
    """
    Parsea la respuesta del LLM en el formato ReAct esperado.

    El LLM debe responder con JSON con esta estructura:
        {
            "thought": "Razonamiento del modelo...",
            "action": "nombre_herramienta",       # o "FINISH" para terminar
            "action_input": { "arg1": "valor1" }
        }

    Returns:
        (thought, action, action_input)

    Raises:
        ValueError: si la respuesta no tiene el formato esperado.
    """
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
    """
    Ejecuta la herramienta registrada bajo `action`.

    Returns:
        Resultado de la herramienta como string (la observacion del agente).
    """
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
    """
    Ejecuta el ciclo ReAct para alcanzar `goal`.

    Args:
        goal:       Objetivo en lenguaje natural.
                    Ej: "Cual es el limite del comerciante MCHT-00042?"
        llm_client: Cliente LLM compatible con OpenAI (puede ser el Mock LLM local).
                    Debe tener: client.chat.completions.create(model, messages)

    Returns:
        AgentResult con el historial completo de pasos y la respuesta final.

    Ejemplo de uso:
        from openai import OpenAI
        client = OpenAI(base_url="http://localhost:8001/v1", api_key="sk-mock")
        result = run_agent("Cuanto es 42 * 7?", client)
        print(result.answer)
    """
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
        logger.debug("Paso %d — enviando al LLM", step_num)

        # ── Reason ───────────────────────────────────────────────────────────
        response = llm_client.chat.completions.create(
            model=DEFAULT_MODEL,  # configurable via LLM_MODEL en .env
            messages=messages,
        )
        raw = response.choices[0].message.content

        try:
            thought, action, action_input = _parse_llm_response(raw)
        except ValueError as e:
            logger.warning("Error parseando respuesta del LLM: %s", e)
            break

        # ── Verificacion de aprobacion humana ─────────────────────────────
        if action in ACTIONS_REQUIRING_APPROVAL:
            logger.warning(
                "Accion '%s' requiere aprobacion humana — deteniendo agente", action
            )
            return AgentResult(
                goal=goal,
                answer=(
                    f"La accion '{action}' requiere aprobacion de un operador humano "
                    "antes de ejecutarse."
                ),
                steps=steps,
                approved=False,
            )

        # ── Terminacion ───────────────────────────────────────────────────
        if action == "FINISH":
            answer = action_input.get("answer", "El agente termino sin respuesta explicita.")
            steps.append(AgentStep(step_num, thought, action, action_input, answer))
            return AgentResult(goal=goal, answer=answer, steps=steps)

        # ── Act ───────────────────────────────────────────────────────────
        observation = _execute_tool(action, action_input)
        logger.debug("Paso %d — observacion: %s", step_num, observation[:100])

        step = AgentStep(step_num, thought, action, action_input, observation)
        steps.append(step)

        # ── Observe: actualiza el historial para el siguiente paso ─────────
        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"Observacion: {observation}"})

    # Si llegamos aqui, se agotaron los pasos
    return AgentResult(
        goal=goal,
        answer="El agente alcanzo el limite de pasos sin completar el objetivo.",
        steps=steps,
    )
