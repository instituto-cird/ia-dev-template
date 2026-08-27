"""
evals/eval_agent.py — Evaluaciones del agente RAG con Mock LLM.

Ejecuta 3 casos de prueba contra el agente usando un cliente OpenAI
que apunta al Mock LLM HTTP (http://localhost:8001/v1).

REQUISITO: El Mock LLM debe estar corriendo:
    uv run --frozen uvicorn app.mock_llm:mock_app --port 8001

EJECUCIÓN:
    uv run python -m evals.eval_agent
"""

from __future__ import annotations

from openai import OpenAI

from app.agent.loop import run_agent


# Configurar cliente OpenAI apuntando al Mock LLM
_llm_client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="sk-mock-key-eval",  # Clave simulada para el mock
)


# Definir los casos de prueba
_EVAL_CASES = [
    {
        "id": "rango-90-dias",
        "pregunta": "¿cuál es el rango máximo del historial?",
        "expected_text": "90 días",
    },
    {
        "id": "pan-solo-ultimos-4",
        "pregunta": "¿puedo exponer el PAN completo?",
        "expected_text": "últimos 4",
    },
    {
        "id": "fuera-de-alcance",
        "pregunta": "¿cuál es la capital de Francia?",
        "expected_text": "Sin coincidencias",
    },
]


def run_eval() -> None:
    """Ejecuta todos los casos de evaluación e imprime resultados."""
    print("\n" + "=" * 60)
    print("📋 Evaluación del Agente RAG - Mock LLM")
    print("=" * 60 + "\n")

    results = []

    for case in _EVAL_CASES:
        case_id = case["id"]
        pregunta = case["pregunta"]
        expected_text = case["expected_text"]

        print(f"Ejecutando: {case_id}")
        print(f"  Pregunta: {pregunta}")

        try:
            # Ejecutar el agente
            respuesta = run_agent(pregunta, _llm_client)

            # Verificar si la respuesta contiene el texto esperado
            passed = expected_text.lower() in respuesta.lower()

            results.append((case_id, passed))

            if passed:
                print(f"  ✅ PASÓ - Respuesta contiene: '{expected_text}'")
            else:
                print(f"  ❌ FALLÓ - Respuesta NO contiene: '{expected_text}'")
                print(f"     Respuesta obtenida: {respuesta[:100]}...")

        except Exception as error:
            print(f"  ❌ ERROR - {type(error).__name__}: {error}")
            results.append((case_id, False))

        print()

    # Resumen final
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    print("=" * 60)
    print(f"📊 Resumen: {passed_count}/{total_count} casos pasaron")
    print("=" * 60)

    if passed_count == total_count:
        print("✅ ¡Todas las pruebas pasaron!")
    else:
        print(f"❌ {total_count - passed_count} prueba(s) fallaron:")
        for case_id, passed in results:
            if not passed:
                print(f"   - {case_id}")

    print()


if __name__ == "__main__":
    run_eval()
