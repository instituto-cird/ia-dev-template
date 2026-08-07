from fastapi.testclient import TestClient

from app.main import app


def test_create_transaction_returns_201_for_valid_payload() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 1500,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "approved",
        "authorization_code": "AUTH-001",
        "pan_last4": "4242",
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 201


def test_create_transaction_returns_422_for_invalid_field() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 0,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "approved",
        "authorization_code": "AUTH-001",
        "pan_last4": "4242",
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 422
    assert any(error["loc"][-1] == "amount_cents" for error in response.json()["detail"])


def test_create_transaction_accepts_prd_boundary_values() -> None:
    # Arrange
    client = TestClient(app)
    payload = {
        "comercio_id": "123e4567-e89b-42d3-a456-426614174000",
        "amount_cents": 1,
        "created_at": "2026-08-06T12:00:00Z",
        "status": "cancelled",
        "authorization_code": "A" * 32,
        "pan_last4": "0000",
    }

    # Act
    response = client.post("/transactions", json=payload)

    # Assert
    assert response.status_code == 201
