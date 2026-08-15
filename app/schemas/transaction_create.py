"""Schema de validación del request del endpoint de historial de transacciones.

Este modelo refleja el contrato del PRD: el comercio se identifica por el JWT,
no por un parámetro público, y los filtros forman parte del dominio de consulta.
No incluye lógica de negocio ni validaciones de servicio; esa capa debe quedar
fuera del schema.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class TransactionCreateRequest(BaseModel):
    """Request del endpoint de consulta del historial de transacciones.

    Importante: el PRD establece que el comercio no se recibe por parámetro público,
    sino que se resuelve desde el JWT. Por eso el request no incluye `comercio_id`.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    # `date` obliga a un valor de fecha ISO 8601. Esto alinea el contrato con el
    # PRD y evita cadenas libres o formatos inconsistentes en los filtros.
    desde: date | None = Field(
        default=None,
        description="Fecha inicial del rango consultado, en UTC según el PRD.",
    )

    # `date` sigue el mismo criterio para el extremo superior del rango. La validación
    # la resuelve luego el servicio, pero el schema asegura el tipo correcto.
    hasta: date | None = Field(
        default=None,
        description="Fecha final del rango consultado, en UTC según el PRD.",
    )

    # `Literal` restringe los valores a los estados del dominio definidos por el PRD.
    # Esto evita estados no soportados y mantiene la API determinista.
    estado: Literal["pending", "approved", "rejected", "refunded", "cancelled"] | None = Field(
        default=None,
        description="Estado de la transacción por el cual filtrar.",
    )

    # `ge=0` garantiza que un monto mínimo no sea negativo. El PRD define que los montos
    # se manejan en centavos y que el negocio no usa valores negativos en filtros.
    monto_min: int | None = Field(
        default=None,
        ge=0,
        description="Monto mínimo en centavos para filtrar el historial.",
    )

    # `gt=0` evita que el máximo sea cero; si el cliente quiere excluir 0, no es un rango
    # válido para un historial de pagos. Esto mantiene el filtro coherente con el dominio.
    monto_max: int | None = Field(
        default=None,
        gt=0,
        description="Monto máximo en centavos para filtrar el historial.",
    )

    # `ge=1` y `le=200` reflejan exactamente la restricción del PRD: page_size mínimo 1,
    # máximo 200, con valor por defecto 50. Esto evita abuso de memoria y errores del cliente.
    page_size: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Cantidad máxima de resultados por página; el PRD fija 50 por defecto y 200 como límite.",
    )

    # `cursor` es un token de paginación; se usa para avanzar entre páginas sin repetir
    # elementos, tal como lo define la historia 3 del PRD.
    cursor: str | None = Field(
        default=None,
        description="Token de paginación para iterar páginas de resultados.",
    )


__all__ = ["TransactionCreateRequest"]
