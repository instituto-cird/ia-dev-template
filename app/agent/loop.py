"""Loop principal del agente RAG."""

import json
from datetime import UTC, datetime
from pathlib import Path

from app.agent.tools import buscar_regla_prd

MAX_STEPS = 5
LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "agent_run.jsonl"

BLOCKED_ACTIONS = (
    "ejecutá un reembolso",
    "ejecutar un reembolso",
    "ejecuta un reembolso",
    "hacer un reembolso",
    "procesar un reembolso",
)


def _log_step(step: int, tool: str, args: dict, result: dict) -> None:
    """Registra cada paso de la trayectoria del agente."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "step": step,
        "tool": tool,
        "args": args,
        "result_summary": {
            "found": result.get("found", False),
            "matches_count": len(result.get("matches", [])),
        },
        "ts": datetime.now(UTC).isoformat(),
    }

    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")


def run_agent(question: str) -> dict:
    """Ejecuta un ciclo controlado de consulta al PRD."""

    if not question or not question.strip():
        return {
            "answer": "Debe proporcionar una pregunta.",
            "steps": 0,
        }

    normalized_question = question.strip().lower()

    # Baranda human-in-the-loop:
    # las operaciones financieras no pueden ser ejecutadas por el agente.
    if any(action in normalized_question for action in BLOCKED_ACTIONS):
        return {
            "answer": (
                "Acción bloqueada: las operaciones financieras requieren "
                "autorización humana y no pueden ser ejecutadas por el agente."
            ),
            "steps": 0,
            "blocked": True,
            "requires_human_approval": True,
        }

    for step in range(1, MAX_STEPS + 1):
        args = {"termino": question.strip()}
        result = buscar_regla_prd(**args)

        _log_step(
            step=step,
            tool="buscar_regla_prd",
            args=args,
            result=result,
        )

        if result["found"]:
            return {
                "answer": "\n".join(match["text"] for match in result["matches"]),
                "steps": step,
                "source": "docs/prd/PRD.md",
            }

        return {
            "answer": "No encontré una regla relacionada en el PRD.",
            "steps": step,
            "source": "docs/prd/PRD.md",
        }

    return {
        "answer": "Se alcanzó el límite máximo de pasos.",
        "steps": MAX_STEPS,
    }