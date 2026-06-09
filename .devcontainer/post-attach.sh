#!/usr/bin/env bash
# .devcontainer/post-attach.sh
# Se ejecuta cada vez que VS Code se conecta al container (no solo en creación).
# Mantenelo corto: lo lento va en post-create.sh.
set -euo pipefail

# Asegurar que el venv de uv está activado en la terminal.
if [ -f .venv/bin/activate ]; then
  echo "✓ Diplomado IA listo. Entorno virtual disponible en .venv/"
  echo "  Comandos frecuentes:"
  echo "    uv sync                            (sincronizar dependencias)"
  echo "    uv run --frozen pytest                      (correr tests)"
  echo "    uv run --frozen uvicorn app.main:app --reload  (levantar backend)"
fi
