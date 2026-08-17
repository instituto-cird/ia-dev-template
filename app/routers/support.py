from fastapi import APIRouter

from app.schemas.models import SupportRequest, SupportResponse
from app.services.support_service import SupportService

router = APIRouter(prefix="/support", tags=["Support"])

service = SupportService()


@router.post("/requests", response_model=SupportResponse)
async def create_support_request(request: SupportRequest) -> SupportResponse:
    return service.create_request(request)