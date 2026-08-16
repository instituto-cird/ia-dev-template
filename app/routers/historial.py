"""Router HTTP del historial de transacciones."""

from fastapi import APIRouter, HTTPException, Query

from app.schemas.transaction_create import HistorialQuery
from app.services.historial_service import HistorialService

router = APIRouter()
service = HistorialService()


@router.get("/api/v1/transacciones", tags=["Historial"], status_code=200)
def get_historial(
    query: HistorialQuery = Query(default_factory=HistorialQuery),
) -> dict:
    """Consulta el historial de transacciones del comercio autenticado."""
    try:
        return service.get_historial(
            desde=query.desde,
            hasta=query.hasta,
            estado=query.estado,
            monto_min=query.monto_min,
            monto_max=query.monto_max,
            page_size=query.page_size,
            cursor=query.cursor,
        )
    except ValueError as exc:
        message = str(exc)
        if message == "El rango de fecha es inválido":
            raise HTTPException(status_code=422, detail=message) from exc
        if message == "El rango excede el máximo permitido (90 días)":
            raise HTTPException(status_code=400, detail=message) from exc
        if message == "Cursor inválido":
            raise HTTPException(status_code=400, detail=message) from exc
        raise HTTPException(status_code=400, detail=message) from exc
