"""Deterministic in-memory repository used by the transaction-history service."""

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class TransactionRecord:
    id: str
    merchant_id: str
    amount_cents: int
    currency: str
    created_at: datetime
    pan: str
    status: str
    authorization_code: str | None = None


class HistorialRepository:
    """Fake repository; replace this boundary with a database adapter later."""

    def __init__(self) -> None:
        self._transactions = (
            TransactionRecord("txn-1003", "MCHT-00001", 12850, "USD", datetime(2026, 8, 10, 14, 0, tzinfo=UTC), "4111111111114242", "approved", "AP1003"),
            TransactionRecord("txn-1002", "MCHT-00001", 4999, "USD", datetime(2026, 8, 8, 10, 30, tzinfo=UTC), "5555555555551234", "pending", "AP1002"),
            TransactionRecord("txn-1001", "MCHT-00001", 2500, "USD", datetime(2026, 8, 1, 9, 0, tzinfo=UTC), "4000000000009876", "rejected"),
            TransactionRecord("txn-2002", "MCHT-00002", 12500, "USD", datetime(2026, 8, 9, 11, 0, tzinfo=UTC), "378282246310005", "refunded", "AP2002"),
            TransactionRecord("txn-2001", "MCHT-00002", 7500, "USD", datetime(2026, 8, 7, 16, 0, tzinfo=UTC), "6011111111111117", "cancelled"),
        )

    def list_for_merchant(self, merchant_id: str) -> list[TransactionRecord]:
        return [item for item in self._transactions if item.merchant_id == merchant_id]
