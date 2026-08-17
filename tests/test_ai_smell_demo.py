from decimal import Decimal

from app.schemas.models import SupportRequest
from app.services.support_service import SupportService


def test_ai_generated_false_confidence_corrected() -> None:
    service = SupportService()

    request = SupportRequest(
        transaction_id="TX-1001",
        claimed_amount=Decimal("150.00"),
        reason="Monto cobrado incorrectamente",
    )

    result = service.create_request(request)

    assert result.transaction_id == "TX-1001"
    assert result.claimed_amount == Decimal("150.00")
    assert result.status == "pending_review"
