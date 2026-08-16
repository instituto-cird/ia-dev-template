from datetime import date, timedelta

from app.repositories.historial_repo import HistorialRepository
from app.schemas.models import (
    TransactionHistoryItem,
    TransactionHistoryRequest,
    TransactionHistoryResponse,
)


class HistorialService:
    def __init__(self, repository: HistorialRepository) -> None:
        self.repository = repository

    def list_transactions(
        self,
        request: TransactionHistoryRequest,
    ) -> TransactionHistoryResponse:

        page = request.page or 1
        page_size = request.page_size or 10

        today = date.today()
        min_allowed_date = today - timedelta(days=90)

        effective_from = request.date_from or min_allowed_date
        effective_to = request.date_to or today

        effective_from = max(effective_from, min_allowed_date)
        effective_to = min(effective_to, today)

        if effective_from > effective_to:
            return TransactionHistoryResponse(
                items=[],
                page=page,
                page_size=page_size,
            )

        filtered_items: list[TransactionHistoryItem] = []

        for item in self.repository.list_transactions():
            if item.date < effective_from or item.date > effective_to:
                continue

            if request.status is not None and item.status != request.status:
                continue

            if request.amount is not None and item.amount > request.amount:
                continue

            filtered_items.append(item)

        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        return TransactionHistoryResponse(
            items=filtered_items[start_index:end_index],
            page=page,
            page_size=page_size,
        )
