import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status

from app.config import get_settings

settings = get_settings()

_ALGORITHM = settings.jwt_algorithm
_SECRET = settings.jwt_secret

# Audience separation (defense in depth): operator-dashboard tokens vs customer-
# portal tokens. A portal token carries PORTAL_AUDIENCE so it can be rejected on
# operator APIs even if a role check is ever missed. Device tokens have their own
# audience (see create_device_access_token).
MANAGER_AUDIENCE = "vedha-manager"
PORTAL_AUDIENCE = "vedha-portal"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def create_access_token(subject: str, tenant_id: str, role: str,
                        expires_minutes: int | None = None,
                        extra_claims: dict[str, Any] | None = None) -> str:
    # Long-running clients (probes/agents) pass a large expires_minutes so their
    # token doesn't lapse every 15 minutes; interactive users use the default.
    minutes = settings.access_token_expire_minutes if expires_minutes is None else expires_minutes
    expire = _now() + timedelta(minutes=minutes)
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "role": role,
        "type": "access",
        "exp": expire,
        "iat": _now(),
        "jti": str(uuid.uuid4()),
    }
    payload.update(extra_claims or {})
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM)


def create_device_access_token(
    subject: str,
    tenant_id: str,
    credential_generation: int,
    *,
    expires_minutes: int = 10,
) -> str:
    return create_access_token(
        subject,
        tenant_id,
        "agent",
        expires_minutes=expires_minutes,
        extra_claims={
            "typ": "device_access",
            "aud": "vedha-probe-api",
            "credential_generation": credential_generation,
        },
    )


def create_refresh_token(subject: str, tenant_id: str) -> tuple[str, str]:
    """Returns (token, jti) — jti is stored in Redis for revocation."""
    jti = str(uuid.uuid4())
    expire = _now() + timedelta(days=settings.refresh_token_expire_days)
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "type": "refresh",
        "exp": expire,
        "iat": _now(),
        "jti": jti,
    }
    return jwt.encode(payload, _SECRET, algorithm=_ALGORITHM), jti


def decode_token(token: str) -> dict[str, Any]:
    try:
        # Audience is enforced by the caller for its credential class. Human
        # legacy tokens do not yet carry aud, while device tokens do.
        return jwt.decode(
            token,
            _SECRET,
            algorithms=[_ALGORITHM],
            options={"verify_aud": False},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}")
