#!/usr/bin/env bash
# .devcontainer/post-create.sh
# Se ejecuta UNA VEZ después de que el container se crea por primera vez.
# Idempotente: corre seguro si por alguna razón se vuelve a ejecutar.
set -euo pipefail

echo "════════════════════════════════════════════════════════════════════"
echo "  Diplomado IA · post-create.sh"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# 1. Sincronizar dependencias del proyecto con uv.
echo "▸ Sincronizando dependencias con uv..."
uv sync --all-extras

# 2. Asegurar que existe un .env de trabajo a partir de .env.example.
if [ ! -f .env ]; then
  echo "▸ Creando .env a partir de .env.example..."
  cp .env.example .env
  echo "  ✓ .env creado. MOCK_MODE=true por defecto, no requiere API keys."
else
  echo "▸ .env ya existe — no se sobrescribe."
fi

# 3. Hooks de pre-commit si el proyecto los define (no rompe si no hay).
if [ -f .pre-commit-config.yaml ]; then
  echo "▸ Instalando hooks de pre-commit..."
  uv run pre-commit install || true
fi

# 4. Smoke test rápido: verificar que el stack carga.
echo ""
echo "▸ Smoke test del entorno..."
uv run python -c "
import sys
print(f'  Python: {sys.version.split()[0]}')
import fastapi, pydantic, pytest
print(f'  FastAPI: {fastapi.__version__}')
print(f'  Pydantic: {pydantic.VERSION}')
print(f'  pytest: {pytest.__version__}')
"

# 5. Verificar que pytest corre (smoke test del repo).
echo ""
echo "▸ Corriendo pytest (smoke test del repo)..."
if uv run pytest -q --tb=no 2>&1 | tail -5; then
  echo "  ✓ Tests del template pasan."
else
  echo "  ⚠ Algún test falló o no hay tests todavía. Revisar después del Lab 0."
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  ✓ Entorno listo."
echo ""
echo "  Próximos pasos sugeridos:"
echo "    1. Levantar el Mock LLM:   uv run python -m app.mock_llm"
echo "       (en otra terminal:)"
echo "    2. Levantar el backend:    uv run uvicorn app.main:app --reload"
echo "    3. Probar la API:          http://localhost:8000/docs"
echo ""
echo "  Documentación: README.md del repositorio."
echo "════════════════════════════════════════════════════════════════════"
