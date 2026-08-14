from datetime import date, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class HistorialQueryParams(BaseModel):
    """Query params para GET /api/v1/transacciones.

    El esquema refleja el contrato del PRD para consultar un historial de
    transacciones por comercio. La validación aquí es estrictamente de entrada
    y del contrato HTTP; la lógica de negocio (por ejemplo, enmascarado del PAN
    o construcción del cursor) queda en la capa de servicio.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    desde: date = Field(
        ...,
        description=(
            "Fecha inicial del rango consultado en UTC. "
            "El PRD limita la retención a 90 días para evitar consultas de "
            "historial antiguo y mantener latencia y costos controlados."
        ),
    )
    hasta: date = Field(
        ...,
        description=(
            "Fecha final del rango consultado en UTC. Debe ser igual o posterior "
            "a la fecha inicial para evitar rangos ambiguos en la consulta."
        ),
    )
    estado: Literal["pending", "approved", "rejected", "refunded", "cancelled"] | None = Field(
        default=None,
        description=(
            "Estado opcional del historial. Se usa Literal para reflejar el "
            "conjunto cerrado definido en el PRD y mantener OpenAPI determinista."
        ),
    )
    page_size: int = Field(
        default=50,
        ge=1,
        le=100,
        description=(
            "Cantidad máxima de resultados por página. El PRD fija un valor "
            "por defecto de 50 y exige un máximo de 100 para controlar memoria "
            "y latencia en consultas largas."
        ),
    )
    cursor: str | None = Field(
        default=None,
        description=(
            "Cursor opaco de paginación devuelto por la API. Se usa como "
            "token de continuación y no tiene semántica de negocio en este schema."
        ),
    )

    @field_validator("hasta")
    @classmethod
    def validate_date_window(cls, value: date, info) -> date:
        """Restringe la ventana consultable al contrato del PRD.

        El PRD declara que el rango consultable en esta API cubre un máximo de
        90 días y que la fecha final no puede ser menor que la inicial. Ese
        límite es clave para la trazabilidad: evita consultas antiguas, reduce
        el costo de procesamiento y produce errores 400 claros cuando la
        solicitud no respeta la política de retención.
        """
        desde = info.data.get("desde")

        if desde is None:
            return value

        if value < desde:
            raise ValueError("El rango de fecha es inválido")

        if value - desde > timedelta(days=90):
            raise ValueError("El rango excede el máximo permitido (90 días)")

        return value
