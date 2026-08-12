from datetime import timedelta

from fastapi.testclient import TestClient

from app.main import app, create_access_token

client = TestClient(app)


def auth(merchant_id: str = "MCHT-00001") -> dict[str, str]:
    return {"Authorization": f"Bearer {create_access_token(merchant_id)}"}


def test_history_requires_a_token() -> None:
    assert client.get("/api/v1/transacciones").status_code == 401


def test_history_is_scoped_to_jwt_merchant() -> None:
    response = client.get("/api/v1/transacciones", headers=auth())
    assert response.status_code == 200
    assert [item["id"] for item in response.json()["data"]] == ["txn-1003", "txn-1002", "txn-1001"]
    assert response.json()["data"][0]["amount"] == 128.5
    assert "pan" not in response.text.lower() or "pan_last4" in response.text


def test_history_filters_and_paginates_without_duplicates() -> None:
    first = client.get("/api/v1/transacciones?page_size=2", headers=auth())
    cursor = first.json()["pagination"]["next_cursor"]
    second = client.get(f"/api/v1/transacciones?page_size=2&cursor={cursor}", headers=auth())
    assert first.status_code == second.status_code == 200
    assert {item["id"] for item in first.json()["data"]}.isdisjoint({item["id"] for item in second.json()["data"]})
    previous = client.get(
        f"/api/v1/transacciones?page_size=2&cursor={second.json()['pagination']['prev_cursor']}",
        headers=auth(),
    )
    assert [item["id"] for item in previous.json()["data"]] == ["txn-1003", "txn-1002"]
    approved = client.get("/api/v1/transacciones?estado=approved", headers=auth())
    assert approved.json()["data"][0]["status"] == "approved"


def test_history_rejects_invalid_ranges() -> None:
    invalid_date = client.get("/api/v1/transacciones?desde=2026-08-02&hasta=2026-08-01", headers=auth())
    old_range = client.get("/api/v1/transacciones?desde=2000-01-01", headers=auth())
    page_size = client.get("/api/v1/transacciones?page_size=201", headers=auth())
    assert invalid_date.status_code == old_range.status_code == page_size.status_code == 400
    assert invalid_date.json()["detail"] == "El rango de fecha es inválido"
    assert old_range.json()["detail"] == "El rango excede el máximo permitido (90 días)"


def test_history_rejects_expired_token() -> None:
    expired = create_access_token("MCHT-00001", expires_in=timedelta(seconds=-1))
    assert client.get("/api/v1/transacciones", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_history_rejects_malformed_token() -> None:
    response = client.get("/api/v1/transacciones", headers={"Authorization": "Bearer invalid.token.value"})
    assert response.status_code == 401
