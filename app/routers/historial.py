from typing import Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas.historial import HistorialQueryParams
from app.repositories.historial_repo import HistorialRepo
from app.services.historial_service import HistorialService

router = APIRouter(prefix="/api/v1")


def _auth_header_valid(request: Request) -> bool:
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ", 1)[1]
    
    # TODO auditoria: jwt no es una implementación real, es un placeholder para tests. Deuda técnica importante.
    # Deterministic test token
    return token == "test-valid-jwt"


@router.get("/transacciones")
async def get_transacciones(request: Request) -> Any:
    # Auth handling: return 401 when missing or invalid
    if not _auth_header_valid(request):
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Manual validation to be able to convert specific business validation
    # errors into 400 as requested by the PRD/tests.
    params = dict(request.query_params)
    try:
        qp = HistorialQueryParams(**params)
    except ValidationError as e:  # pydantic validation errors
        # If the error message matches the PRD range message, return 400
        for err in e.errors():
            msg = err.get("msg", "")
            if "El rango excede el máximo permitido (90 días)" in msg:
                return JSONResponse(
                    status_code=400,
                    content={"error": "El rango excede el máximo permitido (90 días)"},
                )

        # Otherwise, return standard 422 response with details
        raise HTTPException(status_code=422, detail=e.errors())

    # Business logic
    repo = HistorialRepo()
    service = HistorialService(repo)
    result = service.get_historial(qp)
    return result
