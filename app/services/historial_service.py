"""Lógica de negocio para consultar historial de transacciones."""

from __future__ import annotations

from datetime import date, timedelta

from app.repositories.historial_repo import HistorialRepository


class HistorialService:
    """Service con filtro, validación de rango y enmascarado de PAN."""

    def __init__(self, repository: HistorialRepository | None = None) -> None:
        self.repository = repository or HistorialRepository()

    def get_historial(
        self,
        *,
        desde: date | None = None,
        hasta: date | None = None,
        estado: str | None = None,
        monto_min: int | None = None,
        monto_max: int | None = None,
        page_size: int = 50,
        cursor: str | None = None,
    ) -> dict:
        """Devuelve un payload con data + pagination para el endpoint."""
        if desde and hasta and desde > hasta:
            raise ValueError("El rango de fecha es inválido")

        today = date.today()
        if desde and (today - desde).days > 90:
            raise ValueError("El rango excede el máximo permitido (90 días)")
        if hasta and (today - hasta).days > 90:
            raise ValueError("El rango excede el máximo permitido (90 días)")

        items = self.repository.list_transactions()
        filtered = []
        for item in items:
            if desde and item["fecha"] < desde:
                continue
            if hasta and item["fecha"] > hasta:
                continue
            if estado and item["estado"] != estado:
                continue
            if monto_min is not None and item["monto"] < monto_min:
                continue
            if monto_max is not None and item["monto"] > monto_max:
                continue

            masked = dict(item)
            masked["pan_last4"] = f"****{masked['pan_last4'][-4:]}"
            filtered.append(masked)

        filtered.sort(key=lambda item: item["fecha"], reverse=True)

        start = 0
        if cursor:
            try:
                start = int(cursor)
            except ValueError:
                raise ValueError("Cursor inválido")

        end = start + page_size
        page = filtered[start:end]
        next_cursor = str(end) if end < len(filtered) else None

        return {
            "data": page,
            "pagination": {
                "next_cursor": next_cursor,
                "prev_cursor": str(max(start - page_size, 0)) if start > 0 else None,
                "total": len(filtered),
            },
        }
