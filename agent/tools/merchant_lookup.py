"""
agent/tools/merchant_lookup.py — Herramienta de consulta de comerciantes LegacyPay.

Carga los datos desde data/merchants_sample.json.
En produccion, esto conectaria a la base de datos real de LegacyPay.

Patron demostrado:
    - Separacion entre la interfaz de la herramienta (lo que el agente llama)
      y la fuente de datos (JSON, DB, API externa).
    - Validacion de entrada con tipo explicito.
    - Manejo de "not found" sin lanzar excepciones — el agente debe decidir
      que hacer con un resultado vacio, no crashear.
"""

import json
from pathlib import Path
from typing import Any

_DATA_FILE = Path(__file__).parent.parent.parent / "data" / "merchants_sample.json"
_CACHE: dict[str, Any] | None = None


def _load_merchants() -> dict[str, Any]:
    """Carga y cachea los datos de comerciantes desde disco."""
    global _CACHE  # noqa: PLW0603
    if _CACHE is None:
        if not _DATA_FILE.exists():
            _CACHE = {}
            return _CACHE
        with _DATA_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
        # Indexa por merchant_id para O(1) lookup
        _CACHE = {m["merchant_id"]: m for m in data.get("merchants", [])}
    return _CACHE


def lookup_merchant(merchant_id: str) -> str:
    """
    Busca un comerciante por su ID y retorna sus datos relevantes.

    Args:
        merchant_id: ID del comerciante en formato MCHT-NNNNN.
                     Ejemplos: "MCHT-00001", "MCHT-00042"

    Returns:
        JSON string con los datos del comerciante, o mensaje de error si no existe.

    Uso desde el agente:
        action: "lookup_merchant"
        action_input: {"merchant_id": "MCHT-00003"}
    """
    if not isinstance(merchant_id, str):
        return f"ERROR: 'merchant_id' debe ser string, recibio {type(merchant_id).__name__}"

    merchant_id = merchant_id.strip().upper()
    if not merchant_id.startswith("MCHT-"):
        return f"ERROR: formato invalido '{merchant_id}'. Use MCHT-NNNNN"

    merchants = _load_merchants()

    if not merchants:
        return "ERROR: base de datos de comerciantes no disponible (data/merchants_sample.json)"

    merchant = merchants.get(merchant_id)
    if merchant is None:
        return f"NOT_FOUND: comerciante '{merchant_id}' no existe en el sistema"

    # Retorna solo los campos relevantes para el agente (no datos sensibles)
    safe_fields = {
        "merchant_id": merchant.get("merchant_id"),
        "name": merchant.get("name"),
        "category": merchant.get("category"),
        "status": merchant.get("status"),
        "daily_limit_usd": merchant.get("daily_limit_usd"),
        "risk_level": merchant.get("risk_level"),
    }
    return json.dumps(safe_fields, ensure_ascii=False)
