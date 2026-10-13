"""
totp.py — time-based one-time passwords (RFC 6238 over RFC 4226 HOTP).

Six digits, 30-second steps, HMAC-SHA1: the parameters every authenticator app
(Google Authenticator, Microsoft Authenticator, 1Password, Authy, …) uses by
default. Implemented here rather than pulled in as a dependency because it is
twenty lines of standard-library code and is easy to test against the RFC
vectors.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import struct
import time
from urllib.parse import quote, urlencode

DIGITS = 6
PERIOD = 30
# Accept the previous and next step too, so a phone clock a little off still works.
DRIFT_STEPS = 1


def generate_secret() -> str:
    """A new 160-bit shared secret, base32 without padding (what apps expect)."""
    return base64.b32encode(secrets.token_bytes(20)).decode().rstrip("=")


def _key(secret: str) -> bytes:
    cleaned = secret.replace(" ", "").upper()
    return base64.b32decode(cleaned + "=" * (-len(cleaned) % 8))


def hotp(secret: str, counter: int, digits: int = DIGITS) -> str:
    digest = hmac.new(_key(secret), struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)


def current_step(now: float | None = None) -> int:
    return int((time.time() if now is None else now) // PERIOD)


def totp(secret: str, now: float | None = None) -> str:
    return hotp(secret, current_step(now))


def verify(secret: str, code: str, *, now: float | None = None, last_step: int | None = None) -> int | None:
    """The matched time step, or None.

    A step at or before `last_step` (the last one accepted for this user) is
    refused, so a code seen over someone's shoulder cannot be used twice.
    """
    candidate = "".join(ch for ch in str(code) if ch.isdigit())
    if len(candidate) != DIGITS:
        return None
    step = current_step(now)
    matched: int | None = None
    for offset in range(-DRIFT_STEPS, DRIFT_STEPS + 1):
        s = step + offset
        # Compare every candidate (no early exit) so timing does not reveal which matched.
        if hmac.compare_digest(hotp(secret, s), candidate) and matched is None:
            matched = s
    if matched is None or (last_step is not None and matched <= last_step):
        return None
    return matched


def provisioning_uri(secret: str, account: str, issuer: str = "Vedha") -> str:
    """The otpauth:// URI an authenticator app reads from a QR code."""
    label = quote(f"{issuer}:{account}", safe="@:")
    query = urlencode({"secret": secret, "issuer": issuer, "algorithm": "SHA1", "digits": DIGITS, "period": PERIOD})
    return f"otpauth://totp/{label}?{query}"
