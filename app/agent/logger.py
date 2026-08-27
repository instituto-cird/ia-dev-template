"""Registro compacto de ejecuciones del agente."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# El log queda en la raíz del proyecto, fuera del paquete de código.
LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "agent_run.jsonl"


def log_step(step: int, tool: str, args: dict[str, Any], result: str) -> None:
    """Agrega un paso ejecutado al log JSONL del agente."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Se guarda solo un resumen del resultado para evitar logs excesivamente grandes.
    entry = {
        "ts": datetime.now(UTC).isoformat(),
        "step": step,
        "tool": tool,
        "args": args,
        "result_summary": str(result)[:200],
    }
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
