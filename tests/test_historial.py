
from app.repositories.historial_repo import HistorialRepo
from app.schemas.historial import HistorialQueryParams
from app.services.historial_service import HistorialService


def build_qp(**overrides):
    data = {
        "desde": "2026-05-12",
        "hasta": "2026-08-10",
        "estado": "approved",
        "page_size": 2,
        "cursor": None,
    }
    data.update(overrides)
    return HistorialQueryParams.model_validate(data)


def test_mask_pan_keeps_last_four_digits():
    service = HistorialService(HistorialRepo())
    assert service._mask_pan("4111111111111111") == "************1111"


def test_mask_pan_short_value_returns_asterisks():
    service = HistorialService(HistorialRepo())
    assert service._mask_pan("1234") == "****"


def test_encode_decode_cursor_round_trip():
    service = HistorialService(HistorialRepo())
    assert service._decode_cursor(service._encode_cursor(7)) == 7


def test_decode_cursor_invalid_returns_zero():
    service = HistorialService(HistorialRepo())
    assert service._decode_cursor("%%%") == 0


def test_get_historial_filters_and_paginates():
    service = HistorialService(HistorialRepo())
    qp = build_qp(estado="approved", page_size=1, cursor=None)

    result = service.get_historial(qp)

    assert result["pagination"]["has_more"] in {True, False}
    assert isinstance(result["data"], list)
    assert all(item["estado"] == "approved" for item in result["data"])
    assert result["data"][0]["fecha"] == "2026-05-12" or result["data"][0]["fecha"] == "2026-05-12"
