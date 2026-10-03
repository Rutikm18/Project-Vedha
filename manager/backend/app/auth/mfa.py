"""
mfa.py — the pieces of two-step sign-in that are not HTTP: secret storage,
recovery codes, and the short-lived challenge token that links the password
step to the code step.

* The TOTP secret is encrypted at rest with Fernet under a key derived from the
  manager secret (HKDF, MFA-specific context), so a database copy alone cannot
  generate codes.
* Recovery codes are shown once and stored only as keyed hashes (HMAC-SHA256);
  each one works a single time.
* After a correct password, the client gets a challenge token, not a session. It
  lasts five minutes, allows five code attempts, and is spent on success.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from app.config import get_settings

CHALLENGE_MINUTES = 5
CHALLENGE_MAX_ATTEMPTS = 5
PENDING_SECRET_SECONDS = 10 * 60
RECOVERY_CODE_COUNT = 10
_RECOVERY_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # no 0/O, 1/I/L

PURPOSE_VERIFY = "verify"   # user has MFA: prove a code to finish signing in
PURPOSE_ENROLL = "enroll"   # policy requires MFA and the user has none yet


def _derived(info: bytes) -> bytes:
    secret = (get_settings().jwt_secret or "").encode()
    if not secret:
        raise RuntimeError("jwt_secret is not configured")
    return HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=info).derive(secret)


def _fernet() -> Fernet:
    return Fernet(base64.urlsafe_b64encode(_derived(b"vedha:mfa-secret:v1")))


def encrypt_secret(secret: str) -> str:
    return _fernet().encrypt(secret.encode()).decode()


def decrypt_secret(token: str | None) -> str | None:
    if not token:
        return None
    try:
        return _fernet().decrypt(token.encode()).decode()
    except (InvalidToken, ValueError):
        return None


# ── recovery codes ───────────────────────────────────────────────────────────

def _normalise_recovery(code: str) -> str:
    return "".join(ch for ch in code.upper() if ch.isalnum())


def hash_recovery_code(code: str) -> str:
    return hmac.new(_derived(b"vedha:mfa-recovery:v1"), _normalise_recovery(code).encode(), hashlib.sha256).hexdigest()


def new_recovery_codes(count: int = RECOVERY_CODE_COUNT) -> tuple[list[str], list[str]]:
    """(codes to show once, hashes to store). Codes look like 7KQ4M-X9PRT."""
    codes = []
    for _ in range(count):
        raw = "".join(secrets.choice(_RECOVERY_ALPHABET) for _ in range(10))
        codes.append(f"{raw[:5]}-{raw[5:]}")
    return codes, [hash_recovery_code(c) for c in codes]


def looks_like_recovery_code(code: str) -> bool:
    return len(_normalise_recovery(code)) == 10 and not code.strip().isdigit()


def consume_recovery_code(stored: list[str], code: str) -> list[str] | None:
    """The remaining hashes if `code` matched one (which is removed), else None."""
    candidate = hash_recovery_code(code)
    match = next((h for h in stored if hmac.compare_digest(h, candidate)), None)
    if match is None:
        return None
    return [h for h in stored if h != match]


# ── challenge token ──────────────────────────────────────────────────────────

_CHALLENGE_TYPE = "mfa_challenge"


def create_challenge(user_id: str, tenant_id: str, purpose: str) -> tuple[str, str]:
    """(token, jti). Not an access token: it opens only the MFA endpoints."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "type": _CHALLENGE_TYPE,
        "purpose": purpose,
        "aud": "vedha-mfa",
        "iat": now,
        "exp": now + timedelta(minutes=CHALLENGE_MINUTES),
        "jti": jti,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm), jti


def decode_challenge(token: str) -> dict | None:
    """The claims of a valid, unexpired challenge token, else None."""
    settings = get_settings()
    try:
        claims = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm], audience="vedha-mfa")
    except jwt.InvalidTokenError:
        return None
    if claims.get("type") != _CHALLENGE_TYPE or claims.get("purpose") not in (PURPOSE_VERIFY, PURPOSE_ENROLL):
        return None
    return claims


def _attempts_key(jti: str) -> str:
    return f"mfa:attempts:{jti}"


def _spent_key(jti: str) -> str:
    return f"mfa:spent:{jti}"


async def challenge_usable(redis, jti: str) -> bool:
    if await redis.get(_spent_key(jti)):
        return False
    attempts = await redis.get(_attempts_key(jti))
    return attempts is None or int(attempts) < CHALLENGE_MAX_ATTEMPTS


async def record_challenge_failure(redis, jti: str) -> None:
    key = _attempts_key(jti)
    if await redis.incr(key) == 1:
        await redis.expire(key, CHALLENGE_MINUTES * 60)


async def spend_challenge(redis, jti: str) -> None:
    await redis.set(_spent_key(jti), "1", ex=CHALLENGE_MINUTES * 60)


def pending_secret_key(user_id: str) -> str:
    return f"mfa:pending:{user_id}"
