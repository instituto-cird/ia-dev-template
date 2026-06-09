#!/usr/bin/env bash
# scripts/verify_setup.sh
# Verifica que el entorno del estudiante está correctamente configurado.
# Pensado para correrse antes de la Clase 1 y al inicio de cada módulo nuevo.
#
# USO
#   bash scripts/verify_setup.sh
#
# SALIDA
#   Exit code 0 si TODO está bien.
#   Exit code 1 con un reporte claro si algo falla.

set -u

# Colores (si la terminal los soporta)
if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; RED=$'\033[0;31m'; YELLOW=$'\033[1;33m'
  BLUE=$'\033[0;34m'; RESET=$'\033[0m'
else
  GREEN=""; RED=""; YELLOW=""; BLUE=""; RESET=""
fi

PASSED=0
FAILED=0
WARNINGS=0
FAILED_CHECKS=()

check() {
  local name="$1"
  local cmd="$2"
  local hint="$3"

  printf "  %-50s " "$name"
  if eval "$cmd" >/dev/null 2>&1; then
    printf "${GREEN}✓ OK${RESET}\n"
    PASSED=$((PASSED + 1))
  else
    printf "${RED}✗ FAIL${RESET}\n"
    FAILED=$((FAILED + 1))
    FAILED_CHECKS+=("$name | hint: $hint")
  fi
}

warn() {
  local name="$1"
  local cmd="$2"
  local hint="$3"

  printf "  %-50s " "$name"
  if eval "$cmd" >/dev/null 2>&1; then
    printf "${GREEN}✓ OK${RESET}\n"
    PASSED=$((PASSED + 1))
  else
    printf "${YELLOW}⚠ NO${RESET}  ${hint}\n"
    WARNINGS=$((WARNINGS + 1))
  fi
}

echo ""
echo "${BLUE}══════════════════════════════════════════════════════════════════${RESET}"
echo "${BLUE}  Diplomado IA — Verificación de entorno${RESET}"
echo "${BLUE}══════════════════════════════════════════════════════════════════${RESET}"
echo ""

# ─── 1. Herramientas del sistema ─────────────────────────────────────────────
echo "${BLUE}1. Herramientas del sistema${RESET}"
check "Python 3.12 instalado"                                                "python3 --version | grep -qE '3\.(1[2-9]|[2-9][0-9])'"        "Instalar Python 3.12+ (ver docs/nivelacion/00_python_essentials.md)"
check "Git instalado"                                                        "git --version"                                                  "brew install git / apt install git"
check "uv instalado"                                                         "uv --version"                                                   "curl -LsSf https://astral.sh/uv/install.sh | sh"
warn "Docker instalado (opcional para M0-M4)"                                "docker --version"                                               "Docker no es obligatorio. Recomendado para M5"

# ─── 2. Estructura del proyecto ──────────────────────────────────────────────
echo ""
echo "${BLUE}2. Estructura del proyecto${RESET}"
check "Archivo pyproject.toml presente"                                      "test -f pyproject.toml"                                         "Estás en la carpeta raíz del template?"
check "Archivo .python-version presente"                                     "test -f .python-version"                                        "git pull del template"
check ".env existe (copiá .env.example a .env)"                              "test -f .env"                                                   "cp .env.example .env"
check "Carpetas app/, agent/, tests/ presentes"                              "test -d app && test -d agent && test -d tests"                  "Repositorio incompleto — clonalo de nuevo"

# ─── 3. Dependencias instaladas ──────────────────────────────────────────────
echo ""
echo "${BLUE}3. Dependencias del proyecto${RESET}"
check "uv.lock presente"                                                     "test -f uv.lock"                                                "uv lock"
check ".venv creado (uv sync corrió al menos una vez)"                       "test -d .venv"                                                  "uv sync --all-groups"
check "FastAPI importable"                                                   "uv run python -c 'import fastapi'"                              "uv sync --all-groups"
check "Pydantic v2 importable"                                               "uv run python -c 'import pydantic; assert pydantic.VERSION.startswith(\"2.\")'" "uv sync --all-groups"
check "pytest importable"                                                    "uv run python -c 'import pytest'"                               "uv sync --all-groups"

# ─── 4. Backend arranca ──────────────────────────────────────────────────────
echo ""
echo "${BLUE}4. Backend (FastAPI)${RESET}"
check "app.main importa sin errores"                                         "uv run python -c 'from app.main import app'"                    "Revisar app/main.py"
check "Health endpoint funciona (in-process)"                                "uv run python -c 'from fastapi.testclient import TestClient; from app.main import app; r = TestClient(app).get(\"/health\"); assert r.status_code == 200'" "Revisar app/main.py"

# ─── 5. Mock LLM ──────────────────────────────────────────────────────────────
echo ""
echo "${BLUE}5. Mock LLM${RESET}"
check "app.mock_llm importa sin errores"                                     "uv run python -c 'from app.mock_llm import mock_app'"           "Revisar app/mock_llm.py"
check "Mock LLM responde (in-process)"                                       "uv run python -c 'from fastapi.testclient import TestClient; from app.mock_llm import mock_app; r = TestClient(mock_app).post(\"/v1/chat/completions\", json={\"model\":\"x\",\"messages\":[{\"role\":\"user\",\"content\":\"hola\"}]}); assert r.status_code == 200'" "Ver docs/MOCK_LLM_GUIDE.md"

# ─── 6. Agente con MockLLMClient ─────────────────────────────────────────────
echo ""
echo "${BLUE}6. Agente (Track B)${RESET}"
check "agent.core importa sin errores"                                       "uv run python -c 'from agent.core import run_agent'"            "Revisar agent/core.py"
check "MockLLMClient importable"                                             "uv run python -c 'from tests.mocks.mock_llm import MockLLMClient'" "Falta tests/mocks/mock_llm.py — git pull"
check "Calculator tool funciona"                                             "uv run python -c 'from agent.tools.calculator import calculate; assert calculate(\"2+2\") == \"4\"'" "Revisar agent/tools/calculator.py"
check "Merchant lookup tool funciona"                                        "uv run python -c 'from agent.tools.merchant_lookup import lookup_merchant; r = lookup_merchant(\"MCHT-00001\"); assert \"MCHT-00001\" in r'" "Revisar data/merchants_sample.json"

# ─── 7. Harness de calidad ───────────────────────────────────────────────────
echo ""
echo "${BLUE}7. Harness (ruff + mypy + bandit + pytest)${RESET}"
check "ruff disponible"                                                      "uv run ruff --version"                                          "uv sync --all-groups"
check "mypy disponible"                                                      "uv run mypy --version"                                          "uv sync --all-groups"
check "bandit disponible"                                                    "uv run bandit --version"                                        "uv sync --all-groups"
check "pytest pasa todos los tests"                                          "uv run pytest -q --tb=no"                                       "Mirá la salida real con: uv run pytest -v"

# ─── 8. Git ───────────────────────────────────────────────────────────────────
echo ""
echo "${BLUE}8. Git${RESET}"
check "git status funciona"                                                  "git status"                                                     "Estás en un repo git? (git init si es nuevo)"
warn "Hay un remote configurado (GitHub)"                                    "git remote -v | grep -q ."                                     "git remote add origin <URL del classroom>"

# ─── Reporte final ────────────────────────────────────────────────────────────
TOTAL=$((PASSED + FAILED))

echo ""
echo "${BLUE}══════════════════════════════════════════════════════════════════${RESET}"
echo "  ${GREEN}PASSED: ${PASSED}/${TOTAL}${RESET}   ${RED}FAILED: ${FAILED}${RESET}   ${YELLOW}WARNINGS: ${WARNINGS}${RESET}"
echo "${BLUE}══════════════════════════════════════════════════════════════════${RESET}"

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "${GREEN}✅ Entorno listo para los Labs. Podés arrancar.${RESET}"
  echo ""
  echo "Próximo paso sugerido: Lab 0 (Onboarding) — ver el handbook"
  exit 0
else
  echo ""
  echo "${RED}❌ Hay checks fallando:${RESET}"
  echo ""
  for c in "${FAILED_CHECKS[@]}"; do
    echo "  • $c"
  done
  echo ""
  echo "Si no podés resolver alguno, mirá ${YELLOW}docs/RUNBOOK_TROUBLESHOOTING.md${RESET}"
  echo "o publicá tu pregunta en el canal de soporte con la salida completa."
  exit 1
fi
