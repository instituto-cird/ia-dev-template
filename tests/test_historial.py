import datetime as dt
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_transacciones_happy_path_returns_paginated_history() -> None:
    # Arrange
    today = dt.date.today()
    params = {
        "date_from": (today - dt.timedelta(days=30)).isoformat(),
        "date_to": today.isoformat(),
        "status": "approved",
        "amount": "150.00",
        "page": 1,
        "page_size": 10,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=params)

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 1
    assert payload["page_size"] == 10
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) >= 1

    first_item = payload["items"][0]

    assert first_item["status"] == "approved"
    assert Decimal(str(first_item["amount"])) <= Decimal("150.00")
    assert "date" in first_item
    assert "amount" in first_item


def test_get_transacciones_returns_empty_list_when_range_exceeds_ninety_days() -> None:
    # Arrange
    today = dt.date.today()

    params = {
        "date_from": (today - dt.timedelta(days=120)).isoformat(),
        "date_to": (today - dt.timedelta(days=95)).isoformat(),
        "status": "approved",
        "amount": "500.00",
        "page": 1,
        "page_size": 10,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=params)

    # Assert
    assert response.status_code == 200

    payload = response.json()

    assert payload["items"] == []
    assert payload["page"] == 1
    assert payload["page_size"] == 10


def test_get_transacciones_does_not_expose_sensitive_fields() -> None:
    # Arrange
    today = dt.date.today()

    params = {
        "date_from": (today - dt.timedelta(days=7)).isoformat(),
        "date_to": today.isoformat(),
        "status": "approved",
        "amount": "1000.00",
        "page": 1,
        "page_size": 10,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=params)

    # Assert
    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload["items"], list)

    if payload["items"]:
        first_item = payload["items"][0]

        assert "date" in first_item
        assert "status" in first_item
        assert "amount" in first_item

        for sensitive_field in (
            "card_number",
            "pan",
            "card_pan",
            "cvv",
            "auth_code",
            "authentication_data",
            "token",
            "full_track",
        ):
            assert sensitive_field not in first_item
