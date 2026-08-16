from datetime import date, timedelta
from decimal import Decimal

from app.schemas.models import TransactionHistoryItem


class HistorialRepository:
    def __init__(self) -> None:
        today = date.today()

        self._transactions: list[TransactionHistoryItem] = [
            TransactionHistoryItem(
                date=today - timedelta(days=5),
                status="approved",
                amount=Decimal("120.50"),
            ),
            TransactionHistoryItem(
                date=today - timedelta(days=20),
                status="pending",
                amount=Decimal("75.00"),
            ),
            TransactionHistoryItem(
                date=today - timedelta(days=45),
                status="approved",
                amount=Decimal("210.00"),
            ),
            TransactionHistoryItem(
                date=today - timedelta(days=95),
                status="declined",
                amount=Decimal("500.00"),
            ),
            TransactionHistoryItem(
                date=today - timedelta(days=120),
                status="approved",
                amount=Decimal("350.00"),
            ),
        ]

    def list_transactions(self) -> list[TransactionHistoryItem]:
        return [item.model_copy(deep=True) for item in self._transactions]
