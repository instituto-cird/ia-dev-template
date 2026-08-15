from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationInfo


class HistorialQuery(BaseModel):
    """Query params de GET /api/v1/transacciones."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    desde: date | None = Field(
        default=None,
        description="Fecha inicial del rango consultado.",
    )

    hasta: date | None = Field(
        default=None,
        description="Fecha final del rango consultado.",
    )

    estado: Literal[
        "pending",
        "approved",
        "rejected",
        "refunded",
        "cancelled"
    ] | None = None

    monto_min: int | None = Field(default=None, ge=0)
    monto_max: int | None = Field(default=None, ge=0)

    page_size: int = Field(
        default=50,
        ge=1,
        le=200,
    )

    cursor: str | None = None

    @field_validator("hasta")
    @classmethod
    def validate_date_range(
        cls,
        hasta: date | None,
        info: ValidationInfo,
    ) -> date | None:
        desde = info.data.get("desde")

        if desde and hasta and desde > hasta:
            raise ValueError("El rango de fecha es inválido")

        return hasta


TransactionCreateRequest = HistorialQuery

__all__ = ["HistorialQuery", "TransactionCreateRequest"]