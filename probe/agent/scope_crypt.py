"""
scope_crypt.py — asymmetric scope encryption via X25519 + HKDF + AES-256-GCM.

The manager encrypts scope payloads to a specific probe's X25519 public key.
Only that probe (holding the corresponding private key) can decrypt. This
provides end-to-end confidentiality even if the TLS transport is compromised
(e.g. corporate MITM proxy).

Encrypted blob wire format (all-in-one, no side-channel):
  base64(ephemeral_pk_32 || nonce_12 || ciphertext || tag_16)

Where:
  ephemeral_pk  — the sender's one-time X25519 public key (32 bytes)
  nonce         — random AES-GCM nonce (12 bytes)
  ciphertext    — AES-256-GCM encrypted payload (variable)
  tag           — AES-GCM authentication tag (16 bytes)

The shared secret is derived via X25519 DH + HKDF-SHA256.
"""
from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

# Wire format constants
_EPHEMERAL_PK_LEN = 32
_NONCE_LEN = 12
_TAG_LEN = 16
_HEADER_LEN = _EPHEMERAL_PK_LEN + _NONCE_LEN

# HKDF info string — context-binds the derived key to this application
_HKDF_INFO = b"vedha-probe:scope-crypt:v1"


def generate_identity() -> tuple[bytes, bytes]:
    """Generate a fresh X25519 keypair.

    Returns (private_key_bytes, public_key_bytes) — store private_key_bytes
    in a secure location (encrypted STATE_FILE on the probe). Public key is
    sent to the manager at registration time.
    """
    sk = X25519PrivateKey.generate()
    pk = sk.public_key()
    return sk.private_bytes_raw(), pk.public_bytes_raw()


def encrypt_scope(scope_json: bytes, recipient_pk_bytes: bytes) -> bytes:
    """Encrypt scope JSON to a specific probe's public key.

    Args:
        scope_json: UTF-8 encoded JSON payload (scope_cidrs, excluded_cidrs).
        recipient_pk_bytes: Recipient's X25519 public key (32 raw bytes).

    Returns:
        Wire-formatted blob bytes (ready to base64 encode for transport).
    """
    # Generate ephemeral sender keypair (one-time per message)
    ephemeral_sk = X25519PrivateKey.generate()
    ephemeral_pk = ephemeral_sk.public_key()
    ephemeral_pk_raw = ephemeral_pk.public_bytes_raw()

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

    # AAD is the HKDF info string — same on both encrypt and decrypt
    aad = _HKDF_INFO
    ciphertext = aesgcm.encrypt(nonce, scope_json, associated_data=aad)

    # Pack: ephemeral_pk || nonce || ciphertext (which includes the 16-byte tag)
    return ephemeral_pk_raw + nonce + ciphertext


def decrypt_scope(blob: bytes, private_key_bytes: bytes) -> bytes:
    """Decrypt a scope blob using the probe's private key.

    Args:
        blob: Wire-format blob returned by encrypt_scope().
        private_key_bytes: Probe's X25519 private key (32 raw bytes).

    Returns:
        Decrypted scope JSON bytes.

    Raises:
        ValueError: Blob is malformed or authentication failed (tampered data).
    """
    if len(blob) < _HEADER_LEN + _TAG_LEN:
        raise ValueError(
            f"Encrypted scope blob too short ({len(blob)} bytes); "
            f"expected at least {_HEADER_LEN + _TAG_LEN} bytes"
        )

    ephemeral_pk_raw = blob[:_EPHEMERAL_PK_LEN]
    nonce = blob[_EPHEMERAL_PK_LEN:_HEADER_LEN]
    ciphertext = blob[_HEADER_LEN:]

    # Load keys
    ephemeral_pk = X25519PublicKey.from_public_bytes(ephemeral_pk_raw)
    probe_sk = X25519PrivateKey.from_private_bytes(private_key_bytes)

    # Derive shared secret via X25519 DH
    shared_secret = probe_sk.exchange(ephemeral_pk)

    # Derive AES-256-GCM key via HKDF-SHA256 (same params as encrypt)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=_HKDF_INFO,
    )
    key = hkdf.derive(shared_secret)

    # Decrypt (AESGCM verifies the auth tag internally).
    # AAD must be identical to what was used in encrypt_scope.
    aad = _HKDF_INFO
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=aad)
    except Exception as exc:
        raise ValueError(f"Scope decryption failed — data may be tampered: {exc}") from exc

    return plaintext


# ── Convenience helpers for base64 wire transport ─────────────────────────────

def encrypt_scope_b64(scope_json: bytes, recipient_pk_bytes: bytes) -> str:
    """encrypt_scope() returning a base64 string suitable for JSON transport."""
    return base64.b64encode(encrypt_scope(scope_json, recipient_pk_bytes)).decode()


def decrypt_scope_b64(blob_b64: str, private_key_bytes: bytes) -> bytes:
    """decrypt_scope() accepting a base64 string from JSON transport."""
    return decrypt_scope(base64.b64decode(blob_b64), private_key_bytes)


def pubkey_to_bytes(pubkey_b64: str) -> bytes:
    """Decode a base64-encoded X25519 public key to raw bytes."""
    return base64.b64decode(pubkey_b64)


def bytes_to_pubkey_b64(pubkey_bytes: bytes) -> str:
    """Encode raw X25519 public key bytes to a base64 string."""
    return base64.b64encode(pubkey_bytes).decode()
