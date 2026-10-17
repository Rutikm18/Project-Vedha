"""At-rest protection for SIEM/EDR connection secrets.

DetectionConfig.siem_config / edr_config are JSONB blobs holding the platform API
token. Integrations already encrypt theirs (credential_crypto); these were stored in
plaintext, so a database read or backup exposed every tenant's SIEM/EDR credential.

Secret-bearing keys are Fernet-encrypted with a prefix on write and decrypted just
before an engine is built. Rows written before this change hold plaintext; they keep
working (no prefix = used as is) and are encrypted the next time the config is saved.
"""
from __future__ import annotations

from typing import Any

from app.services.credential_crypto import decrypt_credential, encrypt_credential

SECRET_KEYS = frozenset({"token", "api_key", "apikey", "password", "secret", "client_secret"})
_PREFIX = "enc:v1:"


def protect(config: dict[str, Any] | None) -> dict[str, Any] | None:
    """Copy of config with secret values encrypted (idempotent)."""
    if config is None:
        return None
    out: dict[str, Any] = {}
    for key, value in config.items():
        if key.lower() in SECRET_KEYS and isinstance(value, str) and value and not value.startswith(_PREFIX):
            out[key] = _PREFIX + encrypt_credential(value)
        else:
            out[key] = value
    return out


def reveal(config: dict[str, Any] | None) -> dict[str, Any]:
    """Copy of config with secrets decrypted, for building a query engine only.

    A value that no longer decrypts (JWT_SECRET rotated) becomes "" so the platform
    rejects the call, rather than sending ciphertext as a credential."""
    out: dict[str, Any] = {}
    for key, value in (config or {}).items():
        if isinstance(value, str) and value.startswith(_PREFIX):
            out[key] = decrypt_credential(value[len(_PREFIX):]) or ""
        else:
            out[key] = value
    return out
