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


# NUEVO:
# Antes había un único test que enviaba estado inválido + page_size inválido
# y aceptaba que cualquiera de los dos produjera el error.
# Ahora se prueba específicamente el campo estado.
def test_get_transactions_returns_422_for_invalid_estado() -> None:
    # Arrange
    query = {
        "estado": "estado_invalido",
        "page_size": 50,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=query)

    # Assert
    assert response.status_code == 422
    detail = response.json()["detail"]

    # NUEVO/MODIFICADO:
    # Se valida exactamente que el error corresponda a "estado".
    assert any(
        item.get("loc") == ["query", "estado"]
        for item in detail
    )


# NUEVO:
# Se separa page_size en su propio test para comprobar
# específicamente la regla del máximo permitido de 200.
def test_get_transactions_returns_422_for_invalid_page_size() -> None:
    # Arrange
    query = {
        "estado": "approved",
        "page_size": 201,
    }

    # Act
    response = client.get("/api/v1/transacciones", params=query)

    # Assert
    assert response.status_code == 422
    detail = response.json()["detail"]

    # NUEVO:
    # Se valida que el error corresponda exactamente a page_size.
    assert any(
        item.get("loc") == ["query", "page_size"]
        for item in detail
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
    # MODIFICADO:
    # Antes aceptaba encontrar "hasta" O "desde".
    # Ahora comprobamos exactamente que la validación esté asociada a "hasta".
    assert any(
        item.get("loc") == ["query", "hasta"]
        for item in detail
    )

def test_get_transactions_rejects_range_over_90_days() -> None:
    query = {
        "desde": "2026-04-01",
        "hasta": "2026-08-15",
        "page_size": 50,
    }

    response = client.get("/api/v1/transacciones", params=query)

    assert response.status_code == 400
    assert response.json()["detail"] == "El rango excede el máximo permitido (90 días)"


def test_get_transactions_masks_pan() -> None:
    response = client.get(
        "/api/v1/transacciones",
        params={"page_size": 50},
    )

    assert response.status_code == 200

    for item in response.json()["data"]:
        if "pan_last4" in item:
            assert item["pan_last4"].startswith("****")
            assert len(item["pan_last4"]) == 8
