"""HTTP API for LegacyPay's merchant transaction history."""

import base64
import binascii
import hashlib
import hmac
import json
import os
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from enum import StrEnum
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_serializer

from app.routers.historial import router as historial_router

load_dotenv()

app = FastAPI(
    title="LegacyPay Transaction History API",
    description="Consulta segura del historial reciente de transacciones por comercio.",
    version="0.2.0",
)

_default_origins = [
    "http://localhost:8501",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:8501",
    "http://127.0.0.1:3000",
]
_env_origins = os.getenv("CORS_ORIGINS", "")
_origins = [origin.strip() for origin in _env_origins.split(",") if origin.strip()] or _default_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^\d+\.\d+\.\d+$")
    module: str = Field(min_length=1)


class TransactionStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class Transaction(BaseModel):
    """Internal representation. Amounts are stored exclusively as cents."""

    id: str
    merchant_id: str
    amount_cents: int = Field(ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    created_at: datetime
    pan_last4: str = Field(pattern=r"^\d{4}$")
    status: TransactionStatus
    authorization_code: str | None = None


class TransactionResponse(BaseModel):
    id: str
    amount: Decimal
    currency: str
    created_at: datetime
    pan_last4: str
    status: TransactionStatus
    authorization_code: str | None

    @field_serializer("amount")
    def serialize_amount(self, amount: Decimal) -> float:
        """Expose a JSON decimal number while persisting the value as integer cents."""
        return float(amount)


class Pagination(BaseModel):
    next_cursor: str | None
    prev_cursor: str | None
    total_estimated: int = Field(ge=0)


class TransactionListResponse(BaseModel):
    data: list[TransactionResponse]
    pagination: Pagination


def _utc_now() -> datetime:
    return datetime.now(UTC)


# In-memory sample repository for the lab. A production implementation would inject a
# database repository with an index on (merchant_id, created_at DESC, id DESC).
TRANSACTIONS: list[Transaction] = [
    Transaction(id="txn-1003", merchant_id="MCHT-00001", amount_cents=12850, created_at=_utc_now() - timedelta(hours=2), pan_last4="4242", status=TransactionStatus.APPROVED, authorization_code="AP1003"),
    Transaction(id="txn-1002", merchant_id="MCHT-00001", amount_cents=4999, created_at=_utc_now() - timedelta(days=2), pan_last4="1234", status=TransactionStatus.PENDING, authorization_code="AP1002"),
    Transaction(id="txn-1001", merchant_id="MCHT-00001", amount_cents=2500, created_at=_utc_now() - timedelta(days=10), pan_last4="9876", status=TransactionStatus.REJECTED),
    Transaction(id="txn-2001", merchant_id="MCHT-00002", amount_cents=7500, created_at=_utc_now() - timedelta(days=1), pan_last4="1111", status=TransactionStatus.APPROVED, authorization_code="AP2001"),
]

_bearer = HTTPBearer(auto_error=False)
_jwt_secret = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production").encode()


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(merchant_id: str, expires_in: timedelta = timedelta(hours=1)) -> str:
    """Create a HS256 token for local development and automated tests."""
    header = _b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    payload = _b64encode(json.dumps({"sub": merchant_id, "exp": int((_utc_now() + expires_in).timestamp())}, separators=(",", ":")).encode())
    signature = _b64encode(hmac.new(_jwt_secret, f"{header}.{payload}".encode(), hashlib.sha256).digest())
    return f"{header}.{payload}.{signature}"


def current_merchant(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)]) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT requerido")
    try:
        header, payload, signature = credentials.credentials.split(".")
        expected = _b64encode(hmac.new(_jwt_secret, f"{header}.{payload}".encode(), hashlib.sha256).digest())
        claims = json.loads(_b64decode(payload))
        expires_at = claims.get("exp")
        if (
            not hmac.compare_digest(signature, expected)
            or not isinstance(expires_at, (int, float))
            or expires_at < _utc_now().timestamp()
        ):
            raise ValueError("invalid token")
        merchant_id = claims["sub"]
        if not isinstance(merchant_id, str) or not merchant_id:
            raise ValueError("missing subject")
    except (KeyError, ValueError, UnicodeDecodeError, binascii.Error, json.JSONDecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT inválido") from None
    return merchant_id


def _encode_cursor(transaction: Transaction, direction: str) -> str:
    payload = json.dumps(
        [transaction.created_at.isoformat(), transaction.id, direction], separators=(",", ":")
    ).encode()
    return _b64encode(payload)


def _decode_cursor(cursor: str) -> tuple[datetime, str, str]:
    try:
        raw_created_at, transaction_id, direction = json.loads(_b64decode(cursor))
        created_at = datetime.fromisoformat(raw_created_at)
        if (
            created_at.tzinfo is None
            or not isinstance(transaction_id, str)
            or direction not in {"next", "prev"}
        ):
            raise ValueError("invalid cursor")
        return created_at, transaction_id, direction
    except (ValueError, TypeError, UnicodeDecodeError, binascii.Error, json.JSONDecodeError):
        raise HTTPException(status_code=400, detail="Cursor inválido") from None


@app.get("/", tags=["General"])
async def root() -> dict[str, str]:
    return {"message": "Bienvenido a la API de LegacyPay"}


@app.get("/health", response_model=HealthResponse, tags=["Ops"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version="0.2.0", module="System")


@app.get(
    "/api/v1/_legacy/transacciones",
    response_model=TransactionListResponse,
    tags=["Transacciones"],
    summary="Consulta el historial reciente del comercio autenticado",
)
async def list_transactions(
    merchant_id: Annotated[str, Depends(current_merchant)],
    desde: date | None = None,
    hasta: date | None = None,
    estado: TransactionStatus | None = None,
    monto_min: int | None = Query(default=None, ge=0, description="Monto mínimo en centavos"),
    monto_max: int | None = Query(default=None, ge=0, description="Monto máximo en centavos"),
    page_size: int = Query(default=50, ge=1),
    cursor: str | None = None,
) -> TransactionListResponse:
    today = _utc_now().date()
    oldest_allowed = today - timedelta(days=90)
    if page_size > 200:
        raise HTTPException(status_code=400, detail="page_size máximo permitido: 200")
    if desde and hasta and desde > hasta:
        raise HTTPException(status_code=400, detail="El rango de fecha es inválido")
    if monto_min is not None and monto_max is not None and monto_min > monto_max:
        raise HTTPException(status_code=400, detail="El rango de monto es inválido")
    if (desde and desde < oldest_allowed) or (hasta and hasta < oldest_allowed):
        raise HTTPException(status_code=400, detail="El rango excede el máximo permitido (90 días)")

    records = [item for item in TRANSACTIONS if item.merchant_id == merchant_id and item.created_at.date() >= oldest_allowed]
    if desde:
        records = [item for item in records if item.created_at.date() >= desde]
    if hasta:
        records = [item for item in records if item.created_at.date() <= hasta]
    if estado:
        records = [item for item in records if item.status == estado]
    if monto_min is not None:
        records = [item for item in records if item.amount_cents >= monto_min]
    if monto_max is not None:
        records = [item for item in records if item.amount_cents <= monto_max]
    records.sort(key=lambda item: (item.created_at, item.id), reverse=True)
    matching_records = records
    total_estimated = len(matching_records)
    if cursor:
        cursor_created_at, cursor_id, direction = _decode_cursor(cursor)
        cursor_key = (cursor_created_at, cursor_id)
        if direction == "next":
            records = [item for item in records if (item.created_at, item.id) < cursor_key]
            page = records[:page_size]
        else:
            records = [item for item in records if (item.created_at, item.id) > cursor_key]
            page = records[-page_size:]
    else:
        page = records[:page_size]

    response_data = [TransactionResponse(id=item.id, amount=Decimal(item.amount_cents) / 100, currency=item.currency, created_at=item.created_at, pan_last4=item.pan_last4, status=item.status, authorization_code=item.authorization_code) for item in page]
    if not page:
        return TransactionListResponse(data=[], pagination=Pagination(next_cursor=None, prev_cursor=None, total_estimated=total_estimated))
    first_key = (page[0].created_at, page[0].id)
    last_key = (page[-1].created_at, page[-1].id)
    next_cursor = _encode_cursor(page[-1], "next") if any((item.created_at, item.id) < last_key for item in matching_records) else None
    prev_cursor = _encode_cursor(page[0], "prev") if any((item.created_at, item.id) > first_key for item in matching_records) else None
    return TransactionListResponse(data=response_data, pagination=Pagination(next_cursor=next_cursor, prev_cursor=prev_cursor, total_estimated=total_estimated))


app.include_router(historial_router)
