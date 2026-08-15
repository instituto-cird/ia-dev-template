from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_transactions_happy_path_returns_200() -> None:
    # Arrange
    query = {
        "desde": "2026-08-01",
        "hasta": "2026-08-15",
        "estado": "approved",
        "monto_min": 100,
        "monto_max": 5000,
        "page_size": 50,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=query)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "pagination" in body
    assert isinstance(body["data"], list)


def test_get_transactions_returns_422_for_invalid_field_value() -> None:
    # Arrange
    query = {
        "desde": "2026-08-15",
        "hasta": "2026-08-01",
        "estado": "estado_invalido",
        "page_size": 201,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=query)

    # Assert
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("estado" in str(item.get("loc", [])) for item in detail) or any(
        "page_size" in str(item.get("loc", [])) for item in detail
    )


def test_get_transactions_prd_boundary_case_rejects_invalid_range() -> None:
    # Arrange
    query = {
        "desde": "2026-08-15",
        "hasta": "2026-08-01",
        "page_size": 50,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=query)

    # Assert
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("hasta" in str(item.get("loc", [])) or "desde" in str(item.get("loc", [])) for item in detail)
