from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from app.repositories.historial_repo import HistorialRepository
from app.schemas.models import (
    TransactionHistoryRequest,
    TransactionHistoryResponse,
)
from app.services.historial_service import HistorialService

router = APIRouter(prefix="/api/v1", tags=["historial"])


def get_historial_service() -> HistorialService:
    return HistorialService(HistorialRepository())


@router.get("/transacciones", response_model=TransactionHistoryResponse)
def get_transacciones(
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
    status: str | None = Query(default=None),
    amount: Decimal | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1),
    service: HistorialService = Depends(get_historial_service),
) -> TransactionHistoryResponse:

    request = TransactionHistoryRequest(
        date_from=date_from,
        date_to=date_to,
        status=status,
        amount=amount,
        page=page,
        page_size=page_size,
    )

    return service.list_transactions(request)
