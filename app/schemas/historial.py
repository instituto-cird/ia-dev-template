"""Query schema for the merchant transaction-history endpoint."""

from datetime import date, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

TransactionStatusFilter = Literal["pending", "approved", "rejected", "refunded", "cancelled"]


class HistorialQueryParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    desde: date | None = Field(default=None, description="Fecha inicial inclusiva")
    hasta: date | None = Field(default=None, description="Fecha final inclusiva")
    estado: TransactionStatusFilter | None = Field(default=None, description="Estado de la transacción")
    page_size: int = Field(default=50, ge=1, le=200, description="Cantidad de resultados por página")
    cursor: str | None = Field(default=None, min_length=1, description="Cursor opaco de paginación")

    @model_validator(mode="after")
    def validate_date_range(self) -> "HistorialQueryParams":
        if self.desde and self.hasta and self.desde > self.hasta:
            raise ValueError("El rango de fecha es inválido")
        lower_bound = date.today() - timedelta(days=90)
        if (self.desde and self.desde < lower_bound) or (self.hasta and self.hasta < lower_bound):
            raise ValueError("El rango excede el máximo permitido (90 días)")
        if (self.desde and self.desde > date.today()) or (self.hasta and self.hasta > date.today()):
            raise ValueError("El rango de fecha no puede incluir fechas futuras")
        return self
