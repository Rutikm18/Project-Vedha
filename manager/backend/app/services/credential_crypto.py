"""
credential_crypto.py — symmetric, at-rest encryption for operator-recoverable
secrets (currently: customer-portal temp passwords).

Passwords used for AUTH are one-way bcrypt hashes (see customer_access). Separately,
so an operator can re-reveal a customer's login later, the plaintext is stored
ENCRYPTED here with Fernet (AES-128-CBC + HMAC-SHA256), keyed by a value derived
from the manager's `jwt_secret` via HKDF-SHA256. A database leak alone therefore
does not expose portal passwords — the attacker also needs the manager secret.

Trade-off (accepted by the product owner): storing a recoverable credential is
weaker than hash-only. Rotating `jwt_secret` invalidates stored ciphertexts;
`decrypt_credential` returns None in that case and the operator re-issues via Reset.
"""
from __future__ import annotations

import base64

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from app.config import get_settings

_INFO = b"vedha:portal-credential:v1"


def _fernet() -> Fernet:
    secret = (get_settings().jwt_secret or "").encode()
    if not secret:
        raise RuntimeError("jwt_secret is not configured — cannot encrypt credentials")
    key_bytes = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=_INFO).derive(secret)
    return Fernet(base64.urlsafe_b64encode(key_bytes))


def encrypt_credential(plaintext: str) -> str:
    """Encrypt a plaintext secret to a storable token string."""
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt_credential(token: str | None) -> str | None:
    """Decrypt a stored token; None if absent or undecryptable (e.g. written before
    the key existed, or after a secret rotation) — never raises on bad input."""
    if not token:
        return None
    try:
        return _fernet().decrypt(token.encode()).decode()
    except (InvalidToken, ValueError):
        return None
