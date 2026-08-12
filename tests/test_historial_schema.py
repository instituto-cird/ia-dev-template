from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.historial import HistorialQueryParams


def test_history_query_defaults() -> None:
    query = HistorialQueryParams()

    assert query.page_size == 50
    assert query.desde is query.hasta is query.estado is query.cursor is None


@pytest.mark.parametrize(
    "params",
    [
        {"page_size": 0},
        {"page_size": 201},
        {"estado": "unknown"},
        {"cursor": ""},
        {"desde": "2026-08-02", "hasta": "2026-08-01"},
        {"desde": date.today() - timedelta(days=91)},
        {"hasta": date.today() + timedelta(days=1)},
    ],
)
def test_history_query_rejects_invalid_params(params: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        HistorialQueryParams(**params)
