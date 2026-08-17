from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SupportRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(min_length=1)
    claimed_amount: Decimal = Field(gt=0)
    reason: str = Field(min_length=1)


class SupportResponse(BaseModel):
    transaction_id: str
    claimed_amount: Decimal
    reason: str
    status: str
