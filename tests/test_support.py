from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.models import SupportRequest
from app.services.support_service import SupportService


def test_support_request_valid() -> None:
    request = SupportRequest(
        transaction_id="TX-1001",
        claimed_amount=Decimal("150.00"),
        reason="Monto cobrado incorrectamente",
    )

    assert request.transaction_id == "TX-1001"
    assert request.claimed_amount == Decimal("150.00")
    assert request.reason == "Monto cobrado incorrectamente"


def test_support_request_rejects_negative_amount() -> None:
    with pytest.raises(ValidationError):
        SupportRequest(
            transaction_id="TX-1001",
            claimed_amount=Decimal("-10.00"),
            reason="Monto incorrecto",
        )


def test_support_request_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        SupportRequest(
            transaction_id="TX-1001",
            claimed_amount=Decimal("100.00"),
            reason="Monto incorrecto",
            customer_card="4111111111111111",
        )


def test_support_request_rejects_empty_transaction_id() -> None:
    with pytest.raises(ValidationError):
        SupportRequest(
            transaction_id="",
            claimed_amount=Decimal("100.00"),
            reason="Monto incorrecto",
        )


def test_support_service_creates_pending_review() -> None:
    request = SupportRequest(
        transaction_id="TX-1001",
        claimed_amount=Decimal("150.00"),
        reason="Monto cobrado incorrectamente",
    )

    response = SupportService().create_request(request)

    assert response.transaction_id == "TX-1001"
    assert response.claimed_amount == Decimal("150.00")
    assert response.reason == "Monto cobrado incorrectamente"
    assert response.status == "pending_review"


def test_support_service_never_executes_financial_action() -> None:
    request = SupportRequest(
        transaction_id="TX-1002",
        claimed_amount=Decimal("500.00"),
        reason="Solicito reembolso",
    )

    response = SupportService().create_request(request)

    assert response.status == "pending_review"
    assert not hasattr(response, "refund_executed")