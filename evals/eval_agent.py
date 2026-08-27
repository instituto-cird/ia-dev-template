from __future__ import annotations

import sys
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


CASES = [
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


def evaluate_case(case: dict[str, str]) -> bool:
    from app.agent.loop import run_agent
    client = OpenAI(
        base_url="http://localhost:8001/v1",
        api_key="sk-mock-key-123",
    )

    answer = run_agent(case["question"], client, model="gpt-4o-mini")
    ok = case["expected"].lower() in answer.lower()

    print(f"{case['id']}: {'✅' if ok else '❌'}")
    print(f"  pregunta: {case['question']}")
    print(f"  respuesta: {answer}")
    return ok


def main() -> None:
    passed = 0
    for case in CASES:
        if evaluate_case(case):
            passed += 1

    print(f"Total: {passed}/{len(CASES)}")


if __name__ == "__main__":
    main()
