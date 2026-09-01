"""Repositorio fake in-memory para el historial de transacciones."""

from __future__ import annotations

from datetime import date


class HistorialRepository:
    """Repositorio de prueba con 5 transacciones fijas y deterministas."""

    def __init__(self) -> None:
        self._transactions = [
            {
                "id": "txn-001",
                "comercio_id": "comercio-001",
                "monto": 1500,
                "estado": "approved",
                "fecha": date(2026, 8, 1),
                "pan_last4": "4242",
                "codigo_autorizacion": "ABC123",
            },
            {
                "id": "txn-002",
                "comercio_id": "comercio-001",
                "monto": 2500,
                "estado": "pending",
                "fecha": date(2026, 8, 5),
                "pan_last4": "1111",
                "codigo_autorizacion": "XYZ789",
            },
            {
                "id": "txn-003",
                "comercio_id": "comercio-001",
                "monto": 4500,
                "estado": "rejected",
                "fecha": date(2026, 8, 10),
                "pan_last4": "9876",
                "codigo_autorizacion": "QWE456",
            },
            {
                "id": "txn-004",
                "comercio_id": "comercio-001",
                "monto": 5500,
                "estado": "approved",
                "fecha": date(2026, 8, 13),
                "pan_last4": "0000",
                "codigo_autorizacion": "LMN654",
            },
            {
                "id": "txn-005",
                "comercio_id": "comercio-001",
                "monto": 6700,
                "estado": "cancelled",
                "fecha": date(2026, 8, 14),
                "pan_last4": "5555",
                "codigo_autorizacion": "RTY321",
            },
        ]

    def list_transactions(self) -> list[dict]:
        return [item.copy() for item in self._transactions]
