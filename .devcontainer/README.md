# `.devcontainer/` · Entorno reproducible para Codespaces y VS Code

Este directorio define el sandbox del programa, alineado con la guía
*Cápsula 05 · Sandboxes y modelos open source en el programa* del paquete
de materiales complementarios.

## Cuándo usar este sandbox

- Tu máquina no soporta el setup local (Python, uv, políticas corporativas).
- Querés el mismo entorno que tus compañeros para reproducir problemas.
- Estás trabajando desde una máquina prestada o un equipo con poco poder.

Si tu entorno local ya funciona, **podés seguir usándolo**. El sandbox no es
obligatorio en el programa — es alternativa.

## Cómo arrancarlo

### Opción A · GitHub Codespaces (recomendada)

1. Asegurate de tener aceptado el repositorio en GitHub Classroom.
2. En tu repositorio, hacé clic en `Code → Codespaces → Create codespace on main`.
3. Esperá 1–2 minutos a que el container construya por primera vez.
4. El `post-create.sh` corre automáticamente: instala dependencias, copia `.env`,
   ejecuta el smoke test y confirma que el entorno funciona.

### Opción B · VS Code local con la extensión Dev Containers

1. Instalá la extensión `ms-vscode-remote.remote-containers` en VS Code.
2. Asegurate de tener Docker corriendo (Docker Desktop, OrbStack, Podman).
3. Abrí la carpeta del repositorio en VS Code.
4. Cuando VS Code detecte el `.devcontainer/`, ofrecerá *Reopen in Container*.

## Qué viene preinstalado

- Python 3.12 fijo (alineado con `.python-version` del template).
- `uv` 0.5.x para gestión de dependencias y entornos.
- Stack del curso: FastAPI, Pydantic v2, pytest, ruff, mypy, bandit.
- Mock LLM listo para correr en el puerto 8001.
- Extensiones de VS Code preconfiguradas: Python, Ruff, Pylance, mypy,
  GitLens, GitHub Copilot, soporte Mermaid.
- Puertos forwardeados: 8000 (backend FastAPI), 8001 (Mock LLM),
  8501 (Streamlit opcional).

## Validación rápida después del primer arranque

```bash
uv run --frozen pytest                                 # los tests del template deben pasar
uv run --frozen python -m app.mock_llm &               # Mock LLM en background
uv run --frozen uvicorn app.main:app --reload          # backend en otra terminal
curl http://localhost:8000/                   # debe responder OK
```

## Capa opcional · modelos open source con Ollama

El sandbox base usa el Mock LLM. Si querés correr un modelo OS real
dentro del Codespaces, instalá Ollama y descargá un modelo chico:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull phi3:mini      # ~2.3 GB, corre en CPU
ollama serve &
```

Después actualizá `.env`:
```
MOCK_MODE=false
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
```

Esperá rendimiento de ~5–10 tok/s en CPU. Para los Labs alcanza; para
producción, usá API gratuita (Groq, OpenRouter) o tu propia GPU local.
Más detalle en la *Cápsula 05* del paquete de materiales complementarios.
