"""
agent/tools/merchant_lookup.py — Herramienta de consulta de comerciantes LegacyPay.

🚨 BUG 3: la IA generó esta versión con `except Exception: pass` cuando le pedimos
"hacer que el lookup no crashee si algo falla". El except-pass silencia TODOS los
errores — un archivo corrupto, un permiso denegado, un disco lleno — y el sistema
queda sin saber qué pasó. En producción esto es uno de los bugs más difíciles
de debuggear porque NO deja rastro.

La versión correcta del template oficial captura excepciones específicas y
retorna mensajes ERROR distinguibles.
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
        _CACHE = {}
        # 🚨 BUG 3: except-pass silencia errores reales (archivo corrupto,
        # permisos, disco lleno) sin dejar rastro.
        try:
            with _DATA_FILE.open(encoding="utf-8") as f:
                data = json.load(f)
            _CACHE = {m["merchant_id"]: m for m in data.get("merchants", [])}
        except FileNotFoundError:
            print("WARNING: no se pudo cargar merchants_sample.json, el lookup fallará: archivo no encontrado")
        except json.JSONDecodeError:
            print("WARNING: no se pudo cargar merchants_sample.json, el lookup fallará: formato JSON inválido")
    return _CACHE


def lookup_merchant(merchant_id: str) -> str:
    """
    Busca un comerciante por su ID y retorna sus datos relevantes.

    Args:
        merchant_id: ID del comerciante en formato MCHT-NNNNN.

    Returns:
        JSON string con los datos del comerciante, o mensaje de error si no existe.
    """
    if not isinstance(merchant_id, str):
        return f"ERROR: 'merchant_id' debe ser string, recibio {type(merchant_id).__name__}"

    merchant_id = merchant_id.strip().upper()
    if not merchant_id.startswith("MCHT-"):
        return f"ERROR: formato invalido '{merchant_id}'. Use MCHT-NNNNN"

    merchants = _load_merchants()

    if not merchants:
        return "ERROR: base de datos de comerciantes no disponible"

    merchant = merchants.get(merchant_id)
    if merchant is None:
        return f"NOT_FOUND: comerciante '{merchant_id}' no existe en el sistema"

    safe_fields = {
        "merchant_id": merchant.get("merchant_id"),
        "name": merchant.get("name"),
        "category": merchant.get("category"),
        "status": merchant.get("status"),
        "daily_limit_usd": merchant.get("daily_limit_usd"),
        "risk_level": merchant.get("risk_level"),
    }
    return json.dumps(safe_fields, ensure_ascii=False)
