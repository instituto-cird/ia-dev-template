"""Tools del agente RAG para consultar las reglas del PRD."""

import re
from pathlib import Path

PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"


def buscar_regla_prd(termino: str) -> dict:
    """Busca información relevante del PRD mediante coincidencia lexical."""
    if not termino or not termino.strip():
        return {
            "found": False,
            "term": termino,
            "matches": [],
            "message": "Debe proporcionar un término de búsqueda.",
        }

    contenido = PRD_PATH.read_text(encoding="utf-8")
    patron = re.compile(re.escape(termino.strip()), re.IGNORECASE)

    matches = []

    for numero, linea in enumerate(contenido.splitlines(), start=1):
        if patron.search(linea):
            matches.append(
                {
                    "line": numero,
                    "text": linea.strip(),
                }
            )

    return {
        "found": bool(matches),
        "term": termino.strip(),
        "matches": matches[:10],
    }


TOOL_SCHEMA = {
    "name": "buscar_regla_prd",
    "description": "Busca información relevante en el PRD de LegacyPay.",
    "input_schema": {
        "type": "object",
        "properties": {
            "termino": {
                "type": "string",
                "description": "Término o concepto a buscar en el PRD.",
            }
        },
        "required": ["termino"],
        "additionalProperties": False,
    },
}
