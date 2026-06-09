# ia-dev-template

Template oficial del **Diplomado: IA Aplicada al Desarrollo de Software**.

Este repositorio es tu entorno de trabajo durante los 5 módulos del diplomado. NO creas repos nuevos por módulo — cada PR de evaluación agrega capas sobre este mismo repo. Al terminar el diplomado, el historial de commits ES tu portafolio profesional.

---

## Stack

| Componente | Tecnología | Para qué |
|---|---|---|
| API Backend | FastAPI + Pydantic v2 | Endpoints tipados, validación automática, OpenAPI docs |
| Frontend | Streamlit | Prototipado rápido de UI |
| Mock LLM | FastAPI (servidor local) | Simula OpenAI sin usar cuota ni API key real |
| Agente | ReAct pattern | Módulo 4 — Track B |
| Tests | pytest + pytest-asyncio | Suite incremental por módulo |
| Linting | ruff | Estilo + errores comunes |
| Tipos | mypy | Errores de tipo en tiempo de desarrollo |
| Seguridad | bandit | Vulnerabilidades conocidas |
| Dependencias | uv | Gestor moderno, lockfile determinista |
| CI | GitHub Actions | Harness automático en cada PR |
| Contenedores | Docker + docker-compose | Ambiente reproducible |

---

## Requisitos

- **Python 3.12** (usa exactamente esta versión — `.python-version` la fija para uv)
- **uv** — instalación: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git** (y cuenta en GitHub)
- **Docker** (para demo con docker-compose)

> Si eres nuevo en alguna de estas herramientas, lee primero:
> - [docs/nivelacion/00_python_essentials.md](docs/nivelacion/00_python_essentials.md) — Type hints, Pydantic v2, async, pytest
> - [docs/nivelacion/01_fastapi_guide.md](docs/nivelacion/01_fastapi_guide.md) — Endpoints, modelos, errores HTTP, TestClient
> - [docs/nivelacion/02_docker_guide.md](docs/nivelacion/02_docker_guide.md) — Dockerfile, docker-compose, variables de entorno
> - [docs/nivelacion/03_git_github_guide.md](docs/nivelacion/03_git_github_guide.md) — Ramas, commits convencionales, PRs, CI
>
> ¿No sabes cuál necesitas? Haz el Lab 0 y usa
> [docs/nivelacion/04_diagnostico_path.md](docs/nivelacion/04_diagnostico_path.md) como mapa.

---

## Setup rápido (obligatorio antes de Clase 01)

```bash
# 1. Clona tu repo (el link lo recibes del instructor via GitHub Classroom)
git clone https://github.com/ia-aplicada-al-desarrollo-de-software/[tu-repo-asignado].git
cd [tu-repo-asignado]

# 2. Copia el .env de ejemplo
cp .env.example .env

# 3. Instala dependencias (incluyendo dev tools)
uv sync --all-groups

# 4. Verifica que todo está listo (22 chequeos automáticos)
bash scripts/verify_setup.sh

# Si el script termina con "✅ Entorno listo": estás listo para Clase 1.
# Si falla algo: leé docs/RUNBOOK_TROUBLESHOOTING.md antes de pedir ayuda.
```

---

## Estructura del proyecto

```
ia-dev-template/
│
├── app/                    # Backend FastAPI (Track A — tu API vive aquí)
│   ├── __init__.py
│   ├── main.py             # FastAPI app, endpoints, modelos Pydantic
│   └── mock_llm.py         # Servidor local que simula la API de OpenAI
│
├── agent/                  # Agente ReAct (Track B — tu agente vive aquí)
│   ├── __init__.py
│   ├── core.py             # Motor del ciclo Reason → Act → Observe
│   └── tools/              # Una herramienta por archivo
│       ├── __init__.py
│       ├── calculator.py   # Ejemplo: evaluación aritmética segura
│       └── merchant_lookup.py  # Ejemplo: consulta de comerciantes LegacyPay
│
├── tests/                  # Suite de tests (se acumula por módulo)
│   ├── __init__.py
│   └── test_sanity.py      # Tests base — NUNCA deben fallar
│
├── frontend/               # UI Streamlit (opcional, M3+)
│   └── app.py
│
├── data/                   # Datos de muestra para ejercicios
│   └── merchants_sample.json  # Comerciantes LegacyPay (5 registros de ejemplo)
│
├── docs/
│   ├── AI_CODE_SMELLS.md   # Guía de auditoría — leer antes de cada PR
│   ├── templates/
│   │   ├── AI_USAGE.md     # PLANTILLA — copia a raíz del repo y completa
│   │   └── DEMO_PLAN.md    # PLANTILLA — copia a raíz del repo y completa
│   └── nivelacion/         # Guías de nivelación técnica
│
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline: ruff → mypy → bandit → pytest+coverage
│
├── .env.example            # Variables de entorno (copia a .env y personaliza)
├── .python-version         # Python 3.12 (uv lo lee automáticamente)
├── pyproject.toml          # Dependencias + configuración de herramientas
├── uv.lock                 # Lockfile determinista (commitear siempre)
├── docker-compose.yml      # Backend + Frontend + Mock LLM en contenedores
├── Dockerfile.backend      # Imagen del backend
└── Dockerfile.frontend     # Imagen del frontend
```

---

## Cómo arrancar cada servicio

### Opción A — Local (recomendada para desarrollo)

```bash
# Terminal 1: Backend API
uv run uvicorn app.main:app --reload --port 8000
# → Documentación interactiva en http://localhost:8000/docs

# Terminal 2: Mock LLM (simula OpenAI)
uv run uvicorn app.mock_llm:mock_app --port 8001
# → Acepta requests en http://localhost:8001/v1/chat/completions

# Terminal 3: Frontend Streamlit (opcional)
uv run streamlit run frontend/app.py
# → UI en http://localhost:8501
```

### Opción B — Docker (para prueba de ambiente reproducible)

```bash
# Construye y levanta todo
docker compose up --build

# Servicios disponibles:
# Backend:    http://localhost:8000
# Frontend:   http://localhost:8501
# Mock LLM:   http://localhost:8001
```

---

## Variables de entorno

Copia `.env.example` a `.env` antes de correr el backend:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|---|---|---|
| `MOCK_MODE` | `true` | `true` = usa el Mock LLM local, no requiere API key |
| `OPENAI_BASE_URL` | `http://localhost:8001/v1` | URL del LLM (mock o real) |
| `OPENAI_API_KEY` | `sk-mock-key-123` | Solo necesaria si `MOCK_MODE=false` |
| `BACKEND_URL` | `http://localhost:8000` | URL que usa el frontend para conectarse |
| `SECRET_KEY` | `dev-secret-...` | Cambiar en producción |

> `.env` está en `.gitignore`. Nunca lo commitees. Nunca pongas API keys reales en el código.

---

## Comandos del Harness Engineering

Estos son los mismos comandos que corre el CI. Córrelos antes de cada PR:

```bash
# Estilo de código
uv run ruff check .

# Tipos estáticos
uv run mypy app/ --ignore-missing-imports

# Vulnerabilidades de seguridad
uv run bandit -r app/ -ll -q

# Tests + cobertura (debe ser >= 60%)
uv run pytest -q --cov=app --cov-report=term-missing

# Todo de una vez (equivalente al CI):
uv run ruff check . && uv run mypy app/ --ignore-missing-imports && uv run bandit -r app/ -ll -q && uv run pytest -q --cov=app --cov-fail-under=60
```

> Si algún comando falla, el CI fallará también. No abras un PR con CI rojo.

---

## 🤖 Política de uso de IA

Este diplomado fomenta el uso de herramientas avanzadas (Cursor, Claude Code, Copilot), pero bajo la política de **"Copiloto, no Piloto Automático"**.

**Modo Manual (M1 y M2):** Desactiva el "auto-apply" de Claude Code/Cursor. Lee cada línea que la IA sugiere antes de aceptarla.

**Mock Mode:** Por defecto, el repo usa un Mock LLM local. Si usas herramientas externas, asegúrate de que tus PRs pasen los tests del repo, no solo los tests que la IA escribe por ti.

**Vibe Coding:** Está prohibido entregar código que funciona "de casualidad". Si en la defensa se te pregunta "¿por qué usaste esta librería?" y la respuesta es "porque Claude lo puso", se considera fallo.

### Flujo de trabajo AI-Native (Estándar 2026)

1. **Ideación (Humano):** Defines el Qué y el Por qué en un Issue de GitHub.

2. **Scaffolding (Agente):** Usas `uv` + Cursor/Claude para generar la estructura base.

3. **Refinamiento (Humano + Linter):** Corres `ruff` y ajustas la arquitectura. Aquí aplicas el filtro de [AI Code Smells](docs/AI_CODE_SMELLS.md).

4. **Tests (Híbrido):** Pides a la IA que genere casos borde ("Edge Cases"), tú validas que la lógica de negocio sea correcta.

5. **Review (Humano):** NADA entra a main sin que lo hayas leído y entendido. Regla: si no puedes explicarlo, no lo commitees.

6. **Prueba (Humano):** El CI debe estar verde. Si no, investigas tú, no la IA. El agente puede sugerir el fix, pero tú decides si tiene sentido.

---

## GitHub Classroom — Instrucciones para el estudiante

**Classroom del diplomado:** [ia-aplicada-al-desarrollo-de-software](https://classroom.github.com/classrooms/254552850-ia-aplicada-al-desarrollo-de-software)

1. El instructor te comparte el link de invitación al primer assignment (formato `classroom.github.com/a/[código]`).
2. Acepta la tarea — GitHub Classroom crea automáticamente tu repo privado a partir de este template.
3. Clona **tu repo** (no el template original):
   ```bash
   git clone https://github.com/ia-aplicada-al-desarrollo-de-software/[tu-repo-asignado].git
   ```
4. El CI corre automáticamente en cada push — verifica el estado en la pestaña **Actions** de tu repo.
5. Para cada entregable el instructor comparte un nuevo link de assignment — siempre apunta al mismo repo.

### Estrategia de ramas recomendada

```
main              ← Código estable. Solo se actualiza via PR con CI verde.
feature/m1-harness    ← Trabajo de M1. PR → main al entregar.
feature/m2-arquitectura
feature/m3-tdd
feature/m4-agent
release/candidate ← Congelación de features. Solo bugfixes. PR final = Demo Day.
```

### Entregables por módulo

| Módulo | PR desde | Criterio mínimo de CI |
|---|---|---|
| M0 Onboarding | cualquier rama | `pytest` pasa |
| M1 Harness | `feature/m1-harness` | `ruff + mypy + bandit + pytest` pasan |
| M2 Arquitectura | `feature/m2-arquitectura` | CI verde + `docs/ADR-001.md` existe |
| M3 TDD | `feature/m3-tdd` | CI verde + cobertura ≥ 60% |
| M4 Agente | `feature/m4-agent` | CI verde + Golden Set ≥ 80% (Track B) |
| M5 RC | `release/candidate` | CI verde + `DEMO_PLAN.md` + `AI_USAGE.md` |

---

## Track A vs Track B

**Track A — API End-to-End:** Construyes una API FastAPI real con Pydantic v2, tests y al menos una feature asistida por IA. El código principal vive en `app/`.

**Track B — Agente/Orquestación:** Implementas un agente ReAct con 3+ herramientas propias, Golden Set con ≥ 80% de casos deterministas pasando, y `ACTIONS_REQUIRING_APPROVAL` definido. El código principal vive en `agent/`.

Ambos tracks comparten los mismos requisitos de CI, `AI_USAGE.md`, `DEMO_PLAN.md` y defensa.

---

## Documentación complementaria

- [docs/VERIFY_SETUP.md](docs/VERIFY_SETUP.md) — cómo usar `scripts/verify_setup.sh`
- [docs/RUNBOOK_TROUBLESHOOTING.md](docs/RUNBOOK_TROUBLESHOOTING.md) — errores frecuentes y sus fixes
- [docs/MOCK_LLM_GUIDE.md](docs/MOCK_LLM_GUIDE.md) — cuándo usar Mock HTTP vs Mock In-Process
- [docs/AI_CODE_SMELLS.md](docs/AI_CODE_SMELLS.md) — los 6 AI Smells del curso + auditoría automática
- [tools/audit_code.py](tools/audit_code.py) — script de auditoría para el Lab 1

## Referencias externas

- [uv — gestor de dependencias](https://docs.astral.sh/uv/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [ruff — linter](https://docs.astral.sh/ruff/)
- [mypy — type checker](https://mypy.readthedocs.io/)
- [bandit — security linter](https://bandit.readthedocs.io/)
- [pytest](https://docs.pytest.org/)
- [ReAct pattern (paper)](https://arxiv.org/abs/2210.03629)
