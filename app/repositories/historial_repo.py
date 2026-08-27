from __future__ import annotations

from datetime import date
from typing import TypedDict


class TransactionRow(TypedDict):
    id: str
    fecha: date
    pan: str
    monto: int
    estado: str


class HistorialRepo:
    def __init__(self) -> None:
        self._data: list[TransactionRow] = [
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

    def list_all(self) -> list[TransactionRow]:
        return list(self._data)

    def query_by_date_range(self, desde: date, hasta: date) -> list[TransactionRow]:
        return [t for t in self._data if desde <= t["fecha"] <= hasta]

    def filter(
        self,
        desde: date,
        hasta: date,
        estado: str | None = None,
    ) -> list[TransactionRow]:
        items = self.query_by_date_range(desde, hasta)
        if estado:
            items = [t for t in items if t["estado"] == estado]
        items.sort(key=lambda t: t["fecha"])
        return items
