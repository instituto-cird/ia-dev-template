from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints


class TransactionCreateRequest(BaseModel):
    """Schema de entrada para crear una transacción según el PRD.

    Este modelo solo valida el contrato de entrada. La lógica de negocio
    sigue en la capa de servicio y no debe mezclarse con estas reglas.
    """

    comercio_id: Annotated[
        str,
        StringConstraints(
            min_length=1,
            pattern=r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Identificador del comercio afiliado. Se exige un UUID canónico "
                "para asegurar que la transacción siempre se asocia a un comercio "
                "válido y determinista."
            )
        ),
    ]

    amount_cents: Annotated[
        int,
        Field(
            gt=0,
            description=(
                "Monto de la transacción en centavos. Se exige que sea mayor a cero "
                "porque un monto nulo o negativo no representa una transacción válida."
            ),
        ),
    ]

    created_at: Annotated[
        str,
        StringConstraints(
            pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Fecha de creación de la transacción en formato ISO 8601 UTC. "
                "Se restringe a este formato para mantener un contrato determinista "
                "y evitar ambigüedades de zona horaria."
            )
        ),
    ]

    status: Annotated[
        str,
        StringConstraints(
            pattern=r"^(pending|approved|rejected|refunded|cancelled)$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Estado de la operación. Se limita a los valores del PRD para "
                "garantizar consistencia del dominio y evitar estados inválidos."
            )
        ),
    ]

    authorization_code: Annotated[
        str,
        StringConstraints(
            min_length=1,
            max_length=32,
            pattern=r"^[A-Za-z0-9\-]+$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Código de autorización. Se restringe a caracteres alfanuméricos "
                "y guiones para mantener un formato estable y determinista."
            )
        ),
    ]

    pan_last4: Annotated[
        str,
        StringConstraints(
            min_length=4,
            max_length=4,
            pattern=r"^\d{4}$",
            strip_whitespace=True,
        ),
        Field(
            description=(
                "Últimos 4 dígitos del PAN. Se exige exactamente 4 dígitos para "
                "cumplir la política de exposición mínima y evitar revelar datos sensibles."
            )
        ),
    ]
