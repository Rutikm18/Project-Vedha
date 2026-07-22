"""
scope_crypto.py — manager-side: encrypt scope payloads to a probe's X25519 public key.

Wire format (must match probe/agent/scope_crypt.py exactly):
    base64(ephemeral_pk_32 || nonce_12 || ciphertext_tagged)
where ciphertext_tagged = AES-256-GCM(ciphertext, tag_16).

The shared secret is derived via X25519 DH + HKDF-SHA256.
The AAD is the HKDF info string ("vedha-probe:scope-crypt:v1").
"""
from __future__ import annotations

import base64
import os
from typing import Any

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Must match probe/agent/scope_crypt.py
_HKDF_INFO = b"vedha-probe:scope-crypt:v1"
_EPHEMERAL_PK_LEN = 32
_NONCE_LEN = 12

import structlog
logger = structlog.get_logger()


def encrypt_scope(scope_json: bytes, recipient_pk_bytes: bytes) -> bytes:
    """Encrypt scope JSON to a specific probe's X25519 public key.

    Args:
        scope_json: UTF-8 JSON (e.g. {"scope_cidrs": [...], "excluded_cidrs": [...]}).
        recipient_pk_bytes: Probe's X25519 public key (32 raw bytes).

    Returns:
        Wire blob: ephemeral_pk || nonce || AES-GCM(ciphertext, tag).
    """
    if len(recipient_pk_bytes) != 32:
        raise ValueError(
            f"Invalid X25519 public key: expected 32 bytes, got {len(recipient_pk_bytes)}"
        )

    # Ephemeral sender keypair (one-time per message)
    ephemeral_sk = X25519PrivateKey.generate()
    ephemeral_pk_raw = ephemeral_sk.public_key().public_bytes_raw()

    # Load recipient's public key
    recipient_pk = X25519PublicKey.from_public_bytes(recipient_pk_bytes)

    # Derive shared secret via X25519 DH
    shared_secret = ephemeral_sk.exchange(recipient_pk)

    # Derive AES-256-GCM key via HKDF-SHA256
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=_HKDF_INFO,
    )
    key = hkdf.derive(shared_secret)

    # Encrypt with AES-256-GCM
    nonce = os.urandom(_NONCE_LEN)
    aesgcm = AESGCM(key)
    aad = _HKDF_INFO  # must match probe's decrypt
    ciphertext = aesgcm.encrypt(nonce, scope_json, associated_data=aad)

    return ephemeral_pk_raw + nonce + ciphertext


def encrypt_scope_b64(scope_dict: dict[str, Any], recipient_pk_bytes: bytes) -> str:
    """Convenience: dict → JSON → encrypt → base64 string."""
    import json
    scope_json = json.dumps(scope_dict, separators=(",", ":")).encode()
    blob = encrypt_scope(scope_json, recipient_pk_bytes)
    return base64.b64encode(blob).decode()


def public_key_from_b64(pubkey_b64: str) -> bytes:
    """Decode a base64-encoded X25519 public key to raw bytes.

    Returns empty bytes if the key is missing (so callers can gracefully skip
    encryption for agents that haven't registered a public key yet).
    """
    if not pubkey_b64:
        return b""
    try:
        raw = base64.b64decode(pubkey_b64)
        if len(raw) != 32:
            logger.warning("scope_crypto.invalid_key_len", length=len(raw))
            return b""
        return raw
    except Exception:
        logger.warning("scope_crypto.invalid_b64")
        return b""
