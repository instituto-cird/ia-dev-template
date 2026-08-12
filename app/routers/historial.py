"""HTTP adapter for transaction-history queries."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError

from app.schemas.historial import HistorialQueryParams, TransactionStatusFilter
from app.security import current_merchant
from app.services.historial_service import HistorialError, HistorialService

router = APIRouter(tags=["Transacciones"])


def get_historial_service() -> HistorialService:
    return HistorialService()


@router.get("/api/v1/transacciones", summary="Consulta el historial reciente del comercio autenticado")
async def list_transactions(
    merchant_id: Annotated[str, Depends(current_merchant)],
    service: Annotated[HistorialService, Depends(get_historial_service)],
    desde: date | None = None,
    hasta: date | None = None,
    estado: TransactionStatusFilter | None = None,
    page_size: int = Query(default=50, ge=1),
    cursor: str | None = Query(default=None, min_length=1),
) -> dict[str, object]:
    """Translate query parameters and controlled business errors to HTTP."""
    try:
        query = HistorialQueryParams(desde=desde, hasta=hasta, estado=estado, page_size=page_size, cursor=cursor)
        return service.listar(merchant_id, query)
    except ValidationError as error:
        first_error = error.errors()[0]
        context = first_error.get("ctx", {})
        detail = str(context.get("error", first_error["msg"]))
        if first_error["loc"] == ("page_size",) and first_error["type"] == "less_than_equal":
            detail = "page_size máximo permitido: 200"
        raise HTTPException(status_code=400, detail=detail) from error
    except (HistorialError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
