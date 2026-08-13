from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import date
import base64


class HistorialService:
    def __init__(self, repo) -> None:
        self.repo = repo

    def _mask_pan(self, pan: str) -> str:
        # Simple deterministic mask: keep last 4, replace rest with asterisks
        if not pan or len(pan) <= 4:
            return "*" * len(pan)
        return "*" * (len(pan) - 4) + pan[-4:]

    def _encode_cursor(self, index: int) -> str:
        return base64.urlsafe_b64encode(str(index).encode()).decode()

    def _decode_cursor(self, cursor: Optional[str]) -> int:
        if not cursor:
            return 0
        try:
            raw = base64.urlsafe_b64decode(cursor.encode()).decode()
            return int(raw)
        
        # TODO auditoria: excepcion muy general, deberíamos capturar ValueError, binascii.Error, UnicodeDecodeError específicamente
        except Exception:
            return 0

    def get_historial(self, qp) -> Dict[str, Any]:
        """Return data and pagination following a simple cursor model.

        qp: HistorialQueryParams instance
        """
        desde: date = qp.desde
        hasta: date = qp.hasta
        page_size: int = qp.page_size
        estado = qp.estado
        cursor = qp.cursor

        items = self.repo.filter(desde, hasta, estado)

        start = self._decode_cursor(cursor)
        end = start + page_size
        page = items[start:end]

        # TODO auditoria: t es variable temporal, estas líneas no tienen efecto en el resultado final
        # Mask PANs
        # for t in page:
        #     if "pan" in t:
        #         t = t.copy()
        #         t["pan"] = self._mask_pan(t.get("pan", ""))

        # Build response data (return shallow copies)
        data: List[Dict[str, Any]] = [
            {
                "id": t["id"],
                "fecha": t["fecha"].isoformat(),
                "pan": self._mask_pan(t.get("pan", "")),
                "monto": t.get("monto"),
                "estado": t.get("estado"),
            }
            for t in page
        ]

        has_more = end < len(items)
        next_cursor = self._encode_cursor(end) if has_more else None

        return {
            "data": data,
            "pagination": {"next_cursor": next_cursor, "has_more": has_more},
        }
