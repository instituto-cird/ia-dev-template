# Proyecto Final · [Tu Nombre]
Agente RAG que responde preguntas sobre el PRD "Historial de Transacciones LegacyPay". Basado en el patrón ReAct con retriever lexical sobre `docs/prd/PRD.md`.

## Cómo probarlo en 5 minutos

1. Clonar y sincronizar:
```bash
git clone <url-de-tu-fork>
cd ia-dev-template
git checkout proyecto-final
uv sync --extra llm
```

2.	Levantar el mock LLM (terminal aparte):
```bash
uv run --frozen uvicorn app.mock_llm:mock_app --port 8001
```

3.	Correr el agente:
```bash
uv run --frozen python -c "
from openai import OpenAI
from app.agent.loop import run_agent
client = OpenAI(base_url='http://localhost:8001/v1', api_key='mock')
print(run_agent('¿cuál es el rango máximo del historial?', client))"
```

4.	Correr el eval set:
```bash
uv run --frozen python evals/eval_agent.py
```
