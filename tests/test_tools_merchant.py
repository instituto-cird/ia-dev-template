"""
tests/test_tools_merchant.py — Suite de tests para `agent/tools/merchant_lookup.py`.

Patrón a seguir para tools que consultan datos:
    - Test del happy path (id existente)
    - Test del not found (id válido pero inexistente)
    - Test del input inválido (formato incorrecto)
    - Test de seguridad (campos sensibles NO se exponen)
"""

import json

from agent.tools.merchant_lookup import lookup_merchant

# ─── Happy path ──────────────────────────────────────────────────────────────


def test_lookup_existing_merchant_returns_data() -> None:
    """Un comerciante que existe debe retornar su info como JSON string."""
    result = lookup_merchant("MCHT-00001")
    data = json.loads(result)
    assert data["merchant_id"] == "MCHT-00001"
    assert data["name"]  # tiene nombre


def test_lookup_returns_status_field() -> None:
    """El campo status debe estar en la respuesta."""
    result = lookup_merchant("MCHT-00001")
    data = json.loads(result)
    assert "status" in data
    assert data["status"] in ("active", "suspended")


def test_lookup_suspended_merchant() -> None:
    """Un comerciante suspendido (MCHT-00099) debe retornar status='suspended'."""
    result = lookup_merchant("MCHT-00099")
    data = json.loads(result)
    assert data["status"] == "suspended"


# ─── Casos borde ──────────────────────────────────────────────────────────────


def test_lookup_normalizes_lowercase_id() -> None:
    """El ID debe normalizarse a mayúsculas (mcht-00001 → MCHT-00001)."""
    result = lookup_merchant("mcht-00001")
    data = json.loads(result)
    assert data["merchant_id"] == "MCHT-00001"


def test_lookup_strips_whitespace() -> None:
    """Espacios en blanco no deben romper el lookup."""
    result = lookup_merchant("  MCHT-00001  ")
    data = json.loads(result)
    assert data["merchant_id"] == "MCHT-00001"


def test_lookup_not_found_returns_message() -> None:
    """Un ID válido pero inexistente debe retornar NOT_FOUND, no crashear."""
    result = lookup_merchant("MCHT-99999")
    assert result.startswith("NOT_FOUND")


def test_lookup_invalid_format_returns_error() -> None:
    """Un ID sin formato MCHT- debe retornar ERROR."""
    result = lookup_merchant("INVALIDO")
    assert result.startswith("ERROR")


def test_lookup_non_string_returns_error() -> None:
    """Si el agente pasa algo que no es string, no debe crashear."""
    result = lookup_merchant(12345)  # type: ignore[arg-type]
    assert result.startswith("ERROR")


# ─── Seguridad ────────────────────────────────────────────────────────────────


def test_lookup_does_not_expose_pci_compliant_field() -> None:
    """El campo pci_compliant NO debe exponerse al agente (info interna)."""
    result = lookup_merchant("MCHT-00001")
    data = json.loads(result)
    # No debe filtrar info de cumplimiento PCI (información interna)
    assert "pci_compliant" not in data


def test_lookup_does_not_expose_internal_volume() -> None:
    """El monthly_volume_usd NO debe exponerse (dato sensible del negocio)."""
    result = lookup_merchant("MCHT-00001")
    data = json.loads(result)
    assert "monthly_volume_usd" not in data
