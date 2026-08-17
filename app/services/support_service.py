from app.schemas.models import SupportRequest, SupportResponse


class SupportService:
    """Contiene la lógica de negocio de las solicitudes de soporte."""

    def create_request(self, request: SupportRequest) -> SupportResponse:
        return SupportResponse(
            transaction_id=request.transaction_id,
            claimed_amount=request.claimed_amount,
            reason=request.reason,
            status="pending_review",
        )