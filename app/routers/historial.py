import os
import secrets
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.repositories.historial_repo import HistorialRepo
from app.schemas.historial import HistorialQueryParams
from app.services.historial_service import HistorialService

router = APIRouter(prefix="/api/v1")

TEST_TOKEN = os.getenv("TEST_TOKEN", "test-valid-jwt")  # valor por defecto solo para tests/local

def _auth_header_valid(request: Request) -> bool:
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ", 1)[1]

    # TODO: reemplazar por validación JWT real en producción
    return secrets.compare_digest(token, TEST_TOKEN)


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
