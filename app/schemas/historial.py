"""Query schema for the merchant transaction-history endpoint."""

from datetime import date, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TransactionStatusFilter = Literal[
    "pending",
    "approved",
    "rejected",
    "refunded",
    "cancelled",
]


class HistorialQueryParams(BaseModel):
    """Validated filters and cursor pagination options for transaction history.

    The history is intentionally limited to the last 90 calendar days, including
    today.  ``cursor`` stays opaque because it is issued and decoded by the
    pagination layer.
    """

    model_config = ConfigDict(extra="forbid")

    desde: date | None = Field(default=None, description="Fecha inicial inclusiva")
    hasta: date | None = Field(default=None, description="Fecha final inclusiva")
    estado: TransactionStatusFilter | None = Field(
        default=None,
        description="Estado de la transacción",
    )
    page_size: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Cantidad de resultados por página",
    )
    cursor: str | None = Field(
        default=None,
        min_length=1,
        description="Cursor opaco de paginación",
    )

    @model_validator(mode="after")
    def validate_date_range(self) -> "HistorialQueryParams":
        """Enforce the allowed date window and chronological order."""
        if self.desde is not None and self.hasta is not None and self.desde > self.hasta:
            raise ValueError("El rango de fecha es inválido")

        today = date.today()
        oldest_allowed = today - timedelta(days=90)
        if (
            (self.desde is not None and self.desde < oldest_allowed)
            or (self.hasta is not None and self.hasta < oldest_allowed)
        ):
            raise ValueError("El rango excede el máximo permitido (90 días)")

        if (
            (self.desde is not None and self.desde > today)
            or (self.hasta is not None and self.hasta > today)
        ):
            raise ValueError("El rango de fecha no puede incluir fechas futuras")

        return self
