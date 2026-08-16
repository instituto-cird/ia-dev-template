from __future__ import annotations

import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionHistoryRequest(BaseModel):
    """Request contract for the GET transaction history endpoint.

    This model intentionally mirrors only the filters and pagination explicitly
    described in the PRD: date range, status, amount, and page metadata. No
    additional business rules or undocumented fields are modeled here.
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
    )

    date_from: dt.date | None = Field(
        default=None,
        description="Lower bound for the transaction date filter in ISO format.",
    )
    date_to: dt.date | None = Field(
        default=None,
        description="Upper bound for the transaction date filter in ISO format.",
    )
    status: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Status filter as a non-empty value. The PRD defines the need to filter by status, but not the exact allowed values, so this stays intentionally generic.",
    )
    amount: Decimal | None = Field(
        default=None,
        ge=0,
        description="Monetary filter expressed as a Decimal to preserve exact values without float rounding.",
    )
    page: int | None = Field(
        default=None,
        ge=1,
        description="Pagination index. It must be a positive integer; zero or negatives are not meaningful for a page number.",
    )
    page_size: int | None = Field(
        default=None,
        ge=1,
        description="Number of items per page. A value of 0 or less would produce an invalid or ambiguous page size.",
    )


class TransactionHistoryItem(BaseModel):
    """Minimal transaction record returned by the history query.

    Only fields explicitly supported by the PRD and required to inspect the
    transaction without exposing sensitive payment data are included here.
    """

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    date: dt.date = Field(
        description="Transaction date in ISO format. Using date keeps the value deterministic and avoids ambiguous datetime parsing.",
    )
    status: str = Field(
        min_length=1,
        max_length=50,
        description="Transaction status as stored by the system. A non-empty status is required to avoid returning an invalid or blank state.",
    )
    amount: Decimal = Field(
        ge=0,
        description="Transaction amount stored as Decimal to avoid float precision issues in financial values.",
    )


class TransactionHistoryResponse(BaseModel):
    """Paginated response for the transaction history endpoint."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
    )

    items: list[TransactionHistoryItem] = Field(
        description="Collection of transactions matching the request. The list is intentionally minimal and excludes card or auth data, per the PRD.",
    )
    page: int = Field(
        ge=1,
        description="Current page index. Positive page numbers are required for deterministic pagination.",
    )
    page_size: int = Field(
        ge=1,
        description="Number of items in the current page. The size must be positive to keep the response unambiguous.",
    )
