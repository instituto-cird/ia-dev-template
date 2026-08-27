from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openai import OpenAI

from app.agent.loop import run_agent


CASES: list[dict[str, str]] = [
    {
        "id": "rango-90-dias",
        "question": "¿cuál es el rango máximo del historial?",
        "expected": "90 días",
    },
    {
        "id": "pan-solo-ultimos-4",
        "question": "¿puedo exponer el PAN completo?",
        "expected": "últimos 4",
    },
    {
        "id": "fuera-de-alcance",
        "question": "¿cuál es la capital de Francia?",
        "expected": "Sin coincidencias",
    },
]


def run_case(case: dict[str, str]) -> tuple[bool, str]:
    client = OpenAI(base_url="http://localhost:8001/v1", api_key="sk-mock")
    answer = run_agent(case["question"], client)
    ok = case["expected"].lower() in answer.lower()
    status = "✅" if ok else "❌"
    label = f"{status} {case['id']}"
    return ok, f"{label}: {answer}"


def main() -> int:
    passed = 0
    total = len(CASES)

    for case in CASES:
        ok, result = run_case(case)
        print(result)
        if ok:
            passed += 1

    print(f"Total: {passed}/{total} casos correctos")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
