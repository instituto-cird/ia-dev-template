from __future__ import annotations

from pathlib import Path


PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": "Busca lexicalmente un término en el PRD de Historial de Transacciones.",
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
    """Devuelve hasta tres coincidencias del término con contexto cercano."""
    if not PRD_PATH.exists():
        return f"ERROR: no se encontró el PRD en {PRD_PATH}."

    lines = PRD_PATH.read_text(encoding="utf-8").splitlines()
    normalized_term = termino.strip().casefold()
    if not normalized_term:
        return "Sin coincidencias: el término de búsqueda está vacío."

    hit_indexes = [
        index
        for index, line in enumerate(lines)
        if normalized_term in line.casefold()
    ][:3]
    if not hit_indexes:
        return f"Sin coincidencias para el término: {termino!r}."

    hits: list[str] = []
    for hit_index in hit_indexes:
        start = max(0, hit_index - 3)
        end = min(len(lines), hit_index + 4)
        context = "\n".join(
            f"{line_number}: {lines[line_number - 1]}"
            for line_number in range(start + 1, end + 1)
        )
        hits.append(f"Hit en línea {hit_index + 1}:\n{context}")

    return "\n\n".join(hits)
