"""Business rules for merchant transaction history."""

import base64
import binascii
import json
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.repositories.historial_repo import HistorialRepository, TransactionRecord
from app.schemas.historial import HistorialQueryParams


class HistorialError(ValueError):
    """Controlled error that the HTTP adapter translates into a 400 response."""


class HistorialService:
    def __init__(self, repository: HistorialRepository | None = None) -> None:
        self._repository = repository or HistorialRepository()

    def listar(self, merchant_id: str, query: HistorialQueryParams) -> dict[str, object]:
        self._validate_business_rules(query)
        records = self._filter(self._repository.list_for_merchant(merchant_id), query)
        records.sort(key=lambda item: (item.created_at, item.id), reverse=True)
        total_estimated = len(records)
        page = self._page(records, query.cursor, query.page_size)

        return {
            "data": [self._serialize(record) for record in page],
            "pagination": {
                "next_cursor": self._next_cursor(records, page),
                "prev_cursor": self._prev_cursor(records, page),
                "total_estimated": total_estimated,
            },
        }

    def list_transactions(self, merchant_id: str, query: HistorialQueryParams) -> dict[str, object]:
        """English alias for adapters that use the endpoint terminology."""
        return self.listar(merchant_id, query)

    @staticmethod
    def _validate_business_rules(query: HistorialQueryParams) -> None:
        today = date.today()
        oldest_allowed = today - timedelta(days=90)
        if (
            (query.desde is not None and query.desde < oldest_allowed)
            or (query.hasta is not None and query.hasta < oldest_allowed)
        ):
            raise HistorialError("El rango excede el máximo permitido (90 días)")

    @staticmethod
    def _filter(records: list[TransactionRecord], query: HistorialQueryParams) -> list[TransactionRecord]:
        return [
            item
            for item in records
            if (query.desde is None or item.created_at.date() >= query.desde)
            and (query.hasta is None or item.created_at.date() <= query.hasta)
            and (query.estado is None or item.status == query.estado)
        ]

    def _page(self, records: list[TransactionRecord], cursor: str | None, page_size: int) -> list[TransactionRecord]:
        if cursor is None:
            return records[:page_size]

        created_at, transaction_id, direction = self._decode_cursor(cursor)
        key = (created_at, transaction_id)
        if direction == "next":
            return [item for item in records if (item.created_at, item.id) < key][:page_size]
        return [item for item in records if (item.created_at, item.id) > key][-page_size:]

    def _next_cursor(self, records: list[TransactionRecord], page: list[TransactionRecord]) -> str | None:
        if not page:
            return None
        last = page[-1]
        return self._encode_cursor(last, "next") if any((item.created_at, item.id) < (last.created_at, last.id) for item in records) else None

    def _prev_cursor(self, records: list[TransactionRecord], page: list[TransactionRecord]) -> str | None:
        if not page:
            return None
        first = page[0]
        return self._encode_cursor(first, "prev") if any((item.created_at, item.id) > (first.created_at, first.id) for item in records) else None

    @staticmethod
    def _serialize(record: TransactionRecord) -> dict[str, object]:
        return {
            "id": record.id,
            "amount": float(Decimal(record.amount_cents) / 100),
            "currency": record.currency,
            "created_at": record.created_at,
            "pan_last4": record.pan[-4:],
            "status": record.status,
            "authorization_code": record.authorization_code,
        }

    @staticmethod
    def _encode_cursor(record: TransactionRecord, direction: str) -> str:
        value = json.dumps([record.created_at.isoformat(), record.id, direction], separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(value).rstrip(b"=").decode()

    @staticmethod
    def _decode_cursor(cursor: str) -> tuple[datetime, str, str]:
        try:
            decoded = base64.urlsafe_b64decode(cursor + "=" * (-len(cursor) % 4))
            raw_created_at, transaction_id, direction = json.loads(decoded)
            created_at = datetime.fromisoformat(raw_created_at)
            if created_at.tzinfo is None or not isinstance(transaction_id, str) or direction not in {"next", "prev"}:
                raise ValueError
            return created_at, transaction_id, direction
        except (ValueError, TypeError, UnicodeDecodeError, binascii.Error, json.JSONDecodeError):
            raise HistorialError("Cursor inválido") from None
