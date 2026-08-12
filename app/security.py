"""Authentication dependency shared by HTTP routers."""

import base64
import binascii
import hashlib
import hmac
import json
import os
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=False)
_jwt_secret = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production").encode()


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _b64encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode()


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def current_merchant(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token JWT requerido")
    try:
        header, payload, signature = credentials.credentials.split(".")
        expected = _b64encode(
            hmac.new(_jwt_secret, f"{header}.{payload}".encode(), hashlib.sha256).digest()
        )
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
