from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LOG_PATH = Path(__file__).resolve().parents[2] / "logs" / "agent_run.jsonl"


def log_step(step: int, tool: str, args: dict[str, Any], result: str) -> None:
    """Agrega un paso de herramienta al log JSONL del agente."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "step": step,
        "tool": tool,
        "args": args,
        "result_summary": str(result)[:200],
    }
    with LOG_PATH.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
