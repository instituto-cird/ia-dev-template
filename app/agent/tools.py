"""Herramientas de recuperación para el agente del PRD."""

from __future__ import annotations

from pathlib import Path

_PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": "Busca lexicalmente un término en las reglas del PRD.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Término o frase a buscar en el PRD.",
                    }
                },
                "required": ["termino"],
            },
        },
    }
]


def buscar_regla_prd(termino: str) -> str:
    """Devuelve hasta tres coincidencias con tres líneas de contexto."""
    if not _PRD_PATH.exists():
        return "ERROR: no se encontró el PRD en docs/prd/PRD.md."

    normalized_term = termino.strip().casefold()
    if not normalized_term:
        return "Sin coincidencias: el término de búsqueda está vacío."

    lines = _PRD_PATH.read_text(encoding="utf-8").splitlines()
    hit_indexes = [
        index
        for index, line in enumerate(lines)
        if normalized_term in line.casefold()
    ][:3]
    if not hit_indexes:
        return f"Sin coincidencias para '{termino}'."

    hits: list[str] = []
    for hit_number, index in enumerate(hit_indexes, start=1):
        start = max(0, index - 3)
        end = min(len(lines), index + 4)
        context = "\n".join(
            f"{line_number}: {lines[line_number - 1]}"
            for line_number in range(start + 1, end + 1)
        )
        hits.append(f"Hit {hit_number} (línea {index + 1}):\n{context}")
    return "\n\n".join(hits)