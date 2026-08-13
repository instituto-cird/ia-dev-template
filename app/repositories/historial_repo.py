from __future__ import annotations

from datetime import date
from typing import Iterable, List


class HistorialRepo:
    """Repositorio en memoria con transacciones fijas y determinísticas.

    Cada transacción es un dict sencillo con campos mínimos que usa el
    servicio: `id`, `fecha` (date), `pan`, `monto`, `estado`.
    """

    def __init__(self) -> None:
        # Fixed sample data (5 transactions)
        self._data = [
            {
                "id": "tx1",
                "fecha": date(2026, 5, 12),
                "pan": "4111111111111111",
                "monto": 1000,
                "estado": "approved",
            },
            {
                "id": "tx2",
                "fecha": date(2026, 5, 20),
                "pan": "4242424242424242",
                "monto": 2500,
                "estado": "pending",
            },
            {
                "id": "tx3",
                "fecha": date(2026, 6, 15),
                "pan": "4000056655665556",
                "monto": 500,
                "estado": "rejected",
            },
            {
                "id": "tx4",
                "fecha": date(2026, 7, 10),
                "pan": "5555555555554444",
                "monto": 750,
                "estado": "refunded",
            },
            {
                "id": "tx5",
                "fecha": date(2026, 8, 1),
                "pan": "5105105105105100",
                "monto": 1200,
                "estado": "cancelled",
            },
        ]

    def list_all(self) -> List[dict]:
        return list(self._data)

    def query_by_date_range(self, desde: date, hasta: date) -> List[dict]:
        return [t for t in self._data if desde <= t["fecha"] <= hasta]

    def filter(self, desde: date, hasta: date, estado: str | None = None) -> List[dict]:
        items = self.query_by_date_range(desde, hasta)
        if estado:
            items = [t for t in items if t.get("estado") == estado]
        # Sort by fecha ascending to make pagination deterministic
        items.sort(key=lambda t: t["fecha"])
        return items
