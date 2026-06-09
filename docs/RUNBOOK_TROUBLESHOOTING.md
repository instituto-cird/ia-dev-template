# 🛟 Runbook · Troubleshooting de los Labs

> **Cuándo usar este documento**: leelo cuando tu setup falla, antes de publicar tu pregunta en el canal de soporte. La mayoría de los errores del Lab 0 y el Lab 4 están acá con su fix exacto.

> **Comando mágico**: si no sabés por dónde empezar, corré primero `bash scripts/verify_setup.sh` y pegá la salida en tu pregunta de soporte.

---

## Índice

1. [Setup inicial (Lab 0)](#1-setup-inicial-lab-0)
2. [Backend FastAPI no arranca](#2-backend-fastapi-no-arranca)
3. [Mock LLM y conexión con el agente](#3-mock-llm-y-conexión-con-el-agente)
4. [Tests fallando (Lab 1-4)](#4-tests-fallando-lab-1-4)
5. [Docker y docker-compose](#5-docker-y-docker-compose)
6. [GitHub Classroom y CI](#6-github-classroom-y-ci)
7. [Cuando todo lo demás falla](#7-cuando-todo-lo-demás-falla)

---

## 1. Setup inicial (Lab 0)

### `command not found: uv`

`uv` no está en tu PATH.

```bash
# Mac/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Después: cerrá y reabrí la terminal.

# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verificá:
uv --version
```

### `uv sync` falla con "Python 3.12 not found"

```bash
# Opción 1: que uv descargue Python por vos (recomendado)
uv python install 3.12

# Opción 2: instalá Python 3.12 directamente
# Mac:      brew install python@3.12
# Ubuntu:   sudo apt install python3.12 python3.12-venv
# Windows:  https://www.python.org/downloads/  (marcá "Add to PATH")

# Después:
uv sync --all-groups
```

### `Python version conflict` o `requires-python`

El template requiere Python 3.12. Si tenés Python 3.11 instalado, `uv sync` descargará 3.12 automáticamente. Si querés forzar:

```bash
uv python pin 3.12
uv sync --all-groups
```

### `pip install` o `python -m venv` no funciona como en tutoriales

El template usa `uv`, no `pip`+`venv`. Los comandos equivalentes:

| Si en un tutorial decía... | En el template usá... |
|----------------------------|----------------------|
| `python -m venv .venv` | (no hace falta — uv lo crea solo) |
| `source .venv/bin/activate` | (opcional — `uv run` lo activa por vos) |
| `pip install -r requirements.txt` | `uv sync` |
| `pip install paquete` | `uv add paquete` |
| `python script.py` | `uv run python script.py` |
| `pytest` | `uv run pytest` |

### `.env` no se carga / variables no leídas

```bash
# 1. Verificá que .env existe en la raíz del repo (no en una subcarpeta)
ls -la .env

# 2. Si no existe, copialo del template:
cp .env.example .env

# 3. Verificá que el backend lo lee:
uv run python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('MOCK_MODE'))"
# Debe imprimir: true
```

---

## 2. Backend FastAPI no arranca

### `Address already in use` / `Port 8000 is busy`

Algo está ocupando el puerto.

```bash
# Mac/Linux: buscá qué proceso lo usa
lsof -i :8000
# Después: kill -9 <PID>

# O usá otro puerto:
uv run uvicorn app.main:app --reload --port 8002

# Windows:
netstat -ano | findstr :8000
taskkill /F /PID <PID>
```

### `ModuleNotFoundError: No module named 'fastapi'`

`uv sync` no corrió o se corrió en otro directorio.

```bash
# Asegurate de estar en la raíz del repo (donde está pyproject.toml)
pwd  # debe terminar en /ia-dev-template
uv sync --all-groups
```

### `ImportError: cannot import name 'X' from 'app.main'`

Versión vieja del template. Hacé `git pull` para traer la versión actualizada de `app/main.py`.

### El backend arranca pero `localhost:8000` no responde

```bash
# Verificá con curl directo:
curl http://localhost:8000/health
# Esperado: {"status":"ok","version":"0.1.0","module":"System"}

# Si curl no funciona, el backend no arrancó realmente. Revisá la salida de uvicorn.
```

### CORS error desde el frontend Streamlit

Si ves "blocked by CORS policy" en la consola, agregá tu origen a `app/main.py`:

```python
_default_origins = [
    "http://localhost:8501",  # Streamlit
    "http://tu-origen-personalizado:PUERTO",  # agregá acá
]
```

O configurá `CORS_ORIGINS` en tu `.env`:

```bash
CORS_ORIGINS=http://localhost:8501,http://localhost:3000
```

---

## 3. Mock LLM y conexión con el agente

### `Connection refused` cuando el agente llama al Mock LLM

El Mock LLM no está corriendo. Tenés que levantarlo en una **segunda terminal**:

```bash
# Terminal 1: backend
uv run uvicorn app.main:app --reload

# Terminal 2 (nueva): Mock LLM
uv run uvicorn app.mock_llm:mock_app --port 8001

# Verificá:
curl http://localhost:8001/health
# Esperado: {"status":"ok","service":"mock-llm","version":"0.2.0"}
```

### `JSONDecodeError` cuando el agente parsea la respuesta del LLM

Esto pasaba en el Mock LLM viejo. **Asegurate de tener la versión actualizada de `app/mock_llm.py`**: hacé `git pull` y verificá que la versión es 0.2.0:

```bash
grep 'version="0.2.0"' app/mock_llm.py
```

Si no aparece, traé la versión nueva del template oficial.

### `pydantic ValidationError` cuando paso `tools=...` al cliente

Versión vieja del Mock. Actualizá `app/mock_llm.py` (versión 0.2.0+ acepta `tools` sin error).

### El agente loopea para siempre / nunca termina

Verificá que tu prompt incluye instrucciones claras de cuándo terminar. El system prompt del agente dice:

> "Cuando tengas la respuesta final, usa action='FINISH' y pon la respuesta en action_input={'answer': '...'}."

Si el Mock LLM no devuelve `FINISH`, el agente corre hasta `MAX_STEPS=10` y termina con "alcanzó el límite de pasos". Para forzar FINISH en tus tests, usá `mock_chat_response(action="FINISH", action_input={"answer": "..."})`.

### Quiero usar mi propia API key real en vez del Mock

```bash
# 1. Edita .env:
MOCK_MODE=false
OPENAI_API_KEY=sk-tu-key-real
OPENAI_BASE_URL=https://api.openai.com/v1   # para OpenAI
# O para Anthropic via compatible:
# OPENAI_BASE_URL=https://api.anthropic.com/v1
# O para Ollama local:
# OPENAI_BASE_URL=http://localhost:11434/v1

# 2. Reiniciá el backend
```

---

## 4. Tests fallando (Lab 1-4)

### `pytest: command not found`

```bash
# Tenés que correrlo via uv:
uv run pytest

# No: pytest (esto busca en el sistema, no en el venv del proyecto)
```

### `ModuleNotFoundError: No module named 'app'` en los tests

Estás corriendo pytest desde una subcarpeta. Volvé a la raíz:

```bash
cd /ruta/a/ia-dev-template
uv run pytest
```

### Coverage < 60% en CI

El umbral del template es 60% (configurado en `pyproject.toml`). Si tu PR rompe el threshold:

```bash
# Mirá qué líneas no están cubiertas:
uv run pytest --cov=app --cov-report=term-missing

# Agregá tests específicos para las líneas no cubiertas.
```

### El test del Mock LLM hace `pytest.skip`

Es esperado si el Mock LLM no está corriendo. Para correrlo de verdad:

```bash
# Terminal 1:
uv run uvicorn app.mock_llm:mock_app --port 8001

# Terminal 2:
uv run pytest tests/test_sanity.py::test_mock_llm_response_structure -v
```

### `tests/test_agent.py` falla con `ImportError: tests.mocks`

```bash
# 1. Verificá que existe el archivo:
ls tests/mocks/mock_llm.py

# 2. Si no existe, hacé git pull. Si sigue sin estar, copialo del template oficial.
```

### ruff falla en CI pero no localmente

Tu ruff local es viejo. Sincronizá:

```bash
uv sync --all-groups
uv run ruff check .
```

---

## 5. Docker y docker-compose

### `Cannot connect to the Docker daemon`

Docker Desktop / Podman no está corriendo.

- **Mac/Windows**: abrir Docker Desktop y esperar a que esté "Running"
- **Linux**: `sudo systemctl start docker`

### `docker compose up` falla con "version is obsolete"

Versión vieja del template. Actualizá `docker-compose.yml` (versión nueva no tiene línea `version:`).

### `port is already allocated` en Docker

Algo en tu máquina ya usa los puertos 8000/8001/8501. Cerrá los procesos locales (ver §2) o editá los puertos en `docker-compose.yml`.

### El Mock LLM en Docker no arranca

El servicio `mock-llm` instala fastapi/uvicorn en runtime con `pip install`. Si no hay internet o el pip falla, no arranca. Verificá la salida de `docker compose logs mock-llm`.

### Docker no es bloqueante

Si Docker te da problemas y estás antes de M5, **podés ignorarlo**. Los Labs 0-4 corren sin Docker (usá `uv run` directo).

---

## 6. GitHub Classroom y CI

### "I don't have access to the repository"

Aceptá el assignment de GitHub Classroom desde el link que el instructor compartió. Se crea automáticamente un repo privado para vos.

### El CI falla y no entiendo el error

```bash
# Corré el mismo pipeline que el CI, localmente:
uv run ruff check .
uv run mypy app/ --ignore-missing-imports
uv run bandit -r app/ -ll -q
uv run pytest -q --cov=app --cov-fail-under=60
```

Cualquier comando que falle es el que está rompiendo el CI.

### Hice `git push` pero no veo cambios en el CI

```bash
# Verificá que pusheaste a la rama correcta:
git branch  # tu rama actual
git status  # cambios pendientes
git log --oneline -3  # tus últimos commits

# Verificá el remote:
git remote -v
```

### "Branch protection rules" bloquean mi push a main

Es esperado. Trabajá en una rama de feature y abrí PR:

```bash
git checkout -b feat/mi-cambio
# ... hacé tus cambios ...
git add .
git commit -m "feat: descripción del cambio"
git push origin feat/mi-cambio
# Después abrí PR desde GitHub
```

---

## 7. Cuando todo lo demás falla

### Reset total del entorno local

```bash
# 1. Borrá el venv y caches
rm -rf .venv .pytest_cache .ruff_cache .mypy_cache

# 2. Re-clonalo desde GitHub
cd ..
mv ia-dev-template ia-dev-template-broken
git clone <URL de tu fork> ia-dev-template
cd ia-dev-template

# 3. Setup desde cero
cp .env.example .env
uv sync --all-groups
bash scripts/verify_setup.sh
```

### Tu máquina simplemente no aguanta

Pasate a **GitHub Codespaces** (60 horas/mes gratuitas):

1. En tu repo de GitHub: `Code → Codespaces → Create codespace on main`
2. Esperá 1-2 minutos. El `.devcontainer/` automatiza todo el setup.
3. Trabajás desde el navegador o desde VS Code conectado al Codespace.

Ver `.devcontainer/README.md` del template.

### Mensaje de soporte: qué incluir

Cuando publiques en el canal de soporte, incluí:

```
Sistema operativo: [macOS 14 / Ubuntu 22 / Windows 11 + WSL2]
Python: <salida de `python3 --version`>
uv:    <salida de `uv --version`>
Comando que falló: <copialo exacto>
Salida completa del error: <copialo exacto, sin recortar>
Lo que probaste antes de preguntar: <breve>
```

Y al final pegá:

```
Salida de bash scripts/verify_setup.sh:
<copialo exacto>
```

---

*Última actualización: junio 2026 — Cohorte 2026-II.*
*Si encontrás un error nuevo no documentado acá, abrí un Issue en el repo del handbook para que se incorpore.*
