import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="base_historial_params")
def fixture_base_historial_params() -> dict[str, str | int]:
    """Query params base para GET /api/v1/transacciones."""
    return {
        "desde": "2026-05-12",
        "hasta": "2026-08-10",
        "page_size": 50,
    }


@pytest.fixture(name="valid_jwt_header")
def fixture_valid_jwt_header() -> dict[str, str]:
    """Header de Authorization con un JWT de prueba determinista."""
    return {"Authorization": "Bearer test-valid-jwt"}


def _assert_historial_response_shape(body: dict) -> None:
    assert isinstance(body, dict)
    assert "data" in body and isinstance(body["data"], list)
    assert "pagination" in body and isinstance(body["pagination"], dict)
    assert "next_cursor" in body["pagination"]
    assert body["pagination"]["next_cursor"] is None or isinstance(
        body["pagination"]["next_cursor"], str
    )
    assert "has_more" in body["pagination"]
    assert isinstance(body["pagination"]["has_more"], bool)


def test_historial_desde_hasta_validos_con_jwt_retorna_200_shape_correcto(
    base_historial_params: dict[str, str | int], valid_jwt_header: dict[str, str]
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()
    headers = valid_jwt_header

    # Act
    response = client.get("/api/v1/transacciones", params=params, headers=headers)

    # Assert
    assert response.status_code == 200
    body = response.json()
    _assert_historial_response_shape(body)
    assert body["pagination"]["has_more"] in {True, False}


def test_historial_rango_mayor_a_90_dias_retorna_400_mensaje_prd(
    base_historial_params: dict[str, str | int], valid_jwt_header: dict[str, str]
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()
    params["desde"] = "2026-01-01"
    params["hasta"] = "2026-04-05"
    headers = valid_jwt_header

    # Act
    response = client.get("/api/v1/transacciones", params=params, headers=headers)

    # Assert
    assert response.status_code == 400
    body = response.json()
    assert isinstance(body, dict)
    assert body.get("error") == "El rango excede el máximo permitido (90 días)"


def test_historial_sin_authorization_retorna_401(
    base_historial_params: dict[str, str | int]
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()

    # Act
    response = client.get("/api/v1/transacciones", params=params)

    # Assert
    assert response.status_code == 401
    body = response.json()
    assert isinstance(body, dict)
    assert "detail" in body or "error" in body


def test_historial_jwt_malformado_o_expirado_retorna_401(
    base_historial_params: dict[str, str | int]
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()
    headers = {"Authorization": "Bearer invalid.jwt.token"}

    # Act
    response = client.get("/api/v1/transacciones", params=params, headers=headers)

    # Assert
    assert response.status_code == 401
    body = response.json()
    assert isinstance(body, dict)
    assert "detail" in body or "error" in body


@pytest.mark.parametrize("invalid_page_size", [0, 101])
def test_historial_page_size_fuera_de_rango_retorna_422_con_campo_page_size(
    invalid_page_size: int,
    base_historial_params: dict[str, str | int],
    valid_jwt_header: dict[str, str],
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()
    params["page_size"] = invalid_page_size
    headers = valid_jwt_header

    # Act
    response = client.get("/api/v1/transacciones", params=params, headers=headers)

    # Assert
    assert response.status_code == 422
    body = response.json()
    assert isinstance(body, dict)
    assert isinstance(body.get("detail"), list)
    assert any(
        error.get("loc", [])[-1] == "page_size" for error in body["detail"]
    )


def test_historial_rango_exacto_90_dias_retorna_200_frontera_valida(
    base_historial_params: dict[str, str | int], valid_jwt_header: dict[str, str]
) -> None:
    # Arrange
    client = TestClient(app)
    params = base_historial_params.copy()
    params["desde"] = "2026-05-12"
    params["hasta"] = "2026-08-10"
    headers = valid_jwt_header

    # Act
    response = client.get("/api/v1/transacciones", params=params, headers=headers)

    # Assert
    assert response.status_code == 200
    body = response.json()
    _assert_historial_response_shape(body)
    assert body["pagination"]["has_more"] in {True, False}
