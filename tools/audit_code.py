#!/usr/bin/env python3
"""
tools/audit_code.py — Auditor de AI Smells para Lab 1.

USO
    uv run --frozen python tools/audit_code.py
    uv run --frozen python tools/audit_code.py --path agent/ --strict

QUÉ HACE
    Escanea los archivos .py del proyecto buscando los AI Smells documentados
    en `docs/AI_CODE_SMELLS.md`. Imprime un reporte con severidad y sugiere
    el comando del harness que detecta cada smell (ruff/mypy/bandit).

REGLA DEL LAB 1
    Este script DEBE retornar `exit code 0` para que el Lab 1 se considere
    aprobado. Si encuentra smells críticos, sale con código != 0 y el CI
    bloquea el merge.

DETECCIÓN
    Los chequeos son intencionalmente simples (regex sobre archivos planos)
    para que el estudiante pueda leerlos y entender qué se está auditando.
    En producción usaríamos `ast.parse` + `bandit` + reglas semánticas.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ─── Configuración ────────────────────────────────────────────────────────────

# Carpetas a auditar por defecto (relativas a la raíz del repo).
DEFAULT_PATHS = ["app", "agent", "frontend"]

# Carpetas a ignorar siempre.
IGNORE_DIRS = {".venv", "__pycache__", ".git", ".pytest_cache", ".ruff_cache",
               ".mypy_cache", "node_modules", "build", "dist"}


# ─── Reglas de detección ──────────────────────────────────────────────────────


class Smell:
    """Una regla de detección de un AI Smell."""

    def __init__(
        self,
        name: str,
        severity: str,
        pattern: str,
        description: str,
        fix_hint: str,
        flags: int = re.IGNORECASE,
    ) -> None:
        self.name = name
        self.severity = severity  # "high" | "medium" | "low"
        self.pattern = re.compile(pattern, flags)
        self.description = description
        self.fix_hint = fix_hint


SMELLS: list[Smell] = [
    Smell(
        name="HARDCODED_API_KEY",
        severity="high",
        pattern=r"""(?:api[_-]?key|secret|token)\s*=\s*['"](sk-|ghp_|gho_|github_pat_|xox[a-z]-)[A-Za-z0-9_-]{8,}['"]""",
        description="API key, secret o token hardcodeado en el código fuente.",
        fix_hint="Reemplazar por `os.getenv('OPENAI_API_KEY')` y cargar desde `.env`.",
    ),
    Smell(
        name="HARDCODED_PASSWORD",
        severity="high",
        pattern=r"""(?:password|passwd|pwd)\s*=\s*['"][A-Za-z0-9!@#$%^&*_-]{4,}['"]""",
        description="Password en texto plano dentro del código.",
        fix_hint="Mover a `.env` y leer con `os.getenv()`.",
    ),
    Smell(
        name="DANGEROUS_EVAL",
        severity="high",
        pattern=r"\beval\s*\(",
        description="Uso de eval() — ejecución arbitraria de código del usuario.",
        fix_hint="Usar `ast.literal_eval()` para datos, o un parser dedicado (ver `agent/tools/calculator.py`).",
    ),
    Smell(
        name="DANGEROUS_EXEC",
        severity="high",
        pattern=r"\bexec\s*\(",
        description="Uso de exec() — ejecución arbitraria de código.",
        fix_hint="Casi nunca es necesario. Reescribir la lógica sin exec.",
    ),
    Smell(
        name="SHELL_INJECTION_RISK",
        severity="high",
        pattern=r"subprocess\.(run|call|Popen)\([^)]*shell\s*=\s*True",
        description="subprocess con shell=True — riesgo de command injection.",
        fix_hint="Pasar argumentos como lista, sin shell=True.",
    ),
    Smell(
        name="EXCEPT_PASS",
        severity="medium",
        pattern=r"except\s+(?:Exception\s*)?:\s*\n\s*pass\b",
        description="`except: pass` o `except Exception: pass` — silencia errores reales.",
        fix_hint="Capturar excepciones específicas y al menos logguearlas.",
        flags=re.MULTILINE,
    ),
    Smell(
        name="BARE_EXCEPT",
        severity="medium",
        pattern=r"except\s*:\s*\n",
        description="Bare `except:` — captura todo, incluso KeyboardInterrupt y SystemExit.",
        fix_hint="Especificar la excepción: `except ValueError:` o al menos `except Exception:`.",
        flags=re.MULTILINE,
    ),
    Smell(
        name="GHOST_IMPORT",
        severity="medium",
        pattern=r"^\s*(?:from|import)\s+(fastapi_(?:magic|awesome|super)_[a-z_]+|anthropic_(?:streaming|magic)_[a-z_]+|openai_(?:agent|magic)_[a-z_]+)",
        description="Import que parece inventado por una IA (Ghost Dependency).",
        fix_hint="Verificar el paquete en PyPI antes de aceptar el import.",
        flags=re.MULTILINE,
    ),
    Smell(
        name="LOGGING_PII",
        severity="medium",
        pattern=r"(?:logger|logging|print)\s*\([^)]*(?:password|api_key|secret|token|cvv|pan)\b",
        description="Logging de datos sensibles (PII / PCI).",
        fix_hint="Nunca logguear objetos completos que contengan secretos.",
    ),
    Smell(
        name="ALLOW_ORIGINS_WILDCARD_WITH_CREDS",
        severity="medium",
        pattern=r'allow_origins\s*=\s*\[\s*["\']\*["\']\s*\]',
        description='allow_origins=["*"] — violación del spec CORS si allow_credentials=True.',
        fix_hint="Listar orígenes explícitamente.",
    ),
]


# ─── Motor de auditoría ───────────────────────────────────────────────────────


def _iter_python_files(roots: list[Path]) -> list[Path]:
    """Recorre las carpetas de entrada y devuelve los .py encontrados."""
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if root.is_file() and root.suffix == ".py":
            files.append(root)
            continue
        for path in root.rglob("*.py"):
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            files.append(path)
    return sorted(files)


def audit_file(path: Path) -> list[dict[str, object]]:
    """Audita un archivo y devuelve los smells encontrados."""
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [{
            "file": str(path),
            "line": 0,
            "smell": "UNREADABLE_FILE",
            "severity": "low",
            "message": f"No se pudo leer el archivo: {e}",
            "fix_hint": "Verificar codificación o permisos.",
        }]

    findings: list[dict[str, object]] = []
    for smell in SMELLS:
        for match in smell.pattern.finditer(content):
            line_num = content[: match.start()].count("\n") + 1
            findings.append({
                "file": str(path),
                "line": line_num,
                "smell": smell.name,
                "severity": smell.severity,
                "message": smell.description,
                "fix_hint": smell.fix_hint,
            })
    return findings


# ─── Reporte ──────────────────────────────────────────────────────────────────


_SEV_ICON = {"high": "🔴", "medium": "🟡", "low": "🔵"}


def print_report(findings: list[dict[str, object]], strict: bool = False) -> int:
    """Imprime el reporte y devuelve el exit code."""
    if not findings:
        print("✅ Auditoría completada — 0 AI Smells detectados.")
        print()
        print("Recordá correr el harness completo antes del PR:")
        print("  uv run --frozen ruff check .")
        print("  uv run --frozen mypy app/ --ignore-missing-imports")
        print("  uv run --frozen bandit -r app/ -ll -q")
        print("  uv run --frozen pytest -q --cov=app --cov-fail-under=60")
        return 0

    # Agrupa por archivo
    by_file: dict[str, list[dict[str, object]]] = {}
    for f in findings:
        by_file.setdefault(str(f["file"]), []).append(f)

    print(f"🚨 Auditoría completada — {len(findings)} AI Smells detectados:")
    print("=" * 70)

    for filename, file_findings in sorted(by_file.items()):
        print(f"\n📄 {filename}")
        for f in file_findings:
            icon = _SEV_ICON.get(str(f["severity"]), "⚪")
            print(f"  {icon} Línea {f['line']:>4} · {f['smell']}")
            print(f"     {f['message']}")
            print(f"     💡 {f['fix_hint']}")

    print()
    print("=" * 70)

    high_count = sum(1 for f in findings if f["severity"] == "high")
    medium_count = sum(1 for f in findings if f["severity"] == "medium")
    low_count = sum(1 for f in findings if f["severity"] == "low")

    print(f"Resumen: 🔴 {high_count} altos · 🟡 {medium_count} medios · 🔵 {low_count} bajos")

    # Exit code:
    #   - high severity siempre falla
    #   - medium severity falla solo en modo --strict
    if high_count > 0:
        print()
        print("❌ Falla la auditoría: hay smells de severidad ALTA. Corregilos antes de mergear.")
        return 1
    if strict and medium_count > 0:
        print()
        print("❌ Falla la auditoría en modo --strict: hay smells de severidad MEDIA.")
        return 1
    return 0


# ─── CLI ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auditor de AI Smells para el Lab 1 del Diplomado IA.",
    )
    parser.add_argument(
        "--path",
        nargs="*",
        default=DEFAULT_PATHS,
        help=f"Carpetas a auditar (default: {' '.join(DEFAULT_PATHS)})",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Falla también con smells de severidad media (no solo altos).",
    )
    args = parser.parse_args()

    roots = [Path(p) for p in args.path]
    files = _iter_python_files(roots)

    if not files:
        print(f"⚠️  No se encontraron archivos .py en: {', '.join(args.path)}")
        return 0

    print(f"Auditando {len(files)} archivo(s)...")
    print()

    all_findings: list[dict[str, object]] = []
    for f in files:
        all_findings.extend(audit_file(f))

    return print_report(all_findings, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
