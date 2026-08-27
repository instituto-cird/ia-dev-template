"""Herramientas de recuperación lexical sobre el PRD."""

from __future__ import annotations

from pathlib import Path

# Resolver desde este archivo permite ejecutar el agente desde cualquier directorio.
PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"

# Este formato es el contrato que Chat Completions necesita para conocer la tool.
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": "Busca un termino en el PRD y devuelve evidencia con contexto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Termino lexical a buscar en el PRD.",
                    }
                },
                "required": ["termino"],
            },
        },
    }
]


def buscar_regla_prd(termino: str) -> str:
    """Busca hasta tres coincidencias, cada una con tres lineas de contexto."""
    if not PRD_PATH.exists():
        return f"PRD inexistente: no se encontro el archivo {PRD_PATH}."

    lines = PRD_PATH.read_text(encoding="utf-8").splitlines()
    normalized_term = termino.strip().casefold()
    if not normalized_term:
        return "Sin coincidencias: el termino de busqueda esta vacio."

    # Se limita la recuperación a tres líneas coincidentes para mantener la evidencia manejable.
    matching_indexes = [
        index
        for index, line in enumerate(lines)
        if normalized_term in line.casefold()
    ][:3]
    if not matching_indexes:
        return f"Sin coincidencias para el termino: {termino}."

    hits: list[str] = []
    # El rango se recorta en los extremos para evitar índices fuera del documento.
    for hit_number, index in enumerate(matching_indexes, start=1):
        start = max(0, index - 3)
        end = min(len(lines), index + 4)
        context = "\n".join(
            f"{line_number}: {lines[line_number - 1]}"
            for line_number in range(start + 1, end + 1)
        )
        hits.append(f"Coincidencia {hit_number} (linea {index + 1}):\n{context}")

    return "\n\n".join(hits)
