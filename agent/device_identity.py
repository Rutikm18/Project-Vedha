from __future__ import annotations

import base64
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def generate_signing_identity() -> tuple[bytes, bytes]:
    private = Ed25519PrivateKey.generate()
    return private.private_bytes_raw(), private.public_key().public_bytes_raw()


def signing_public_from_private(private_key: bytes) -> bytes:
    return Ed25519PrivateKey.from_private_bytes(private_key).public_key().public_bytes_raw()


def sign_b64(private_key: bytes, message: str) -> str:
    signature = Ed25519PrivateKey.from_private_bytes(private_key).sign(message.encode("utf-8"))
    return base64.b64encode(signature).decode()


def encode_key(value: bytes) -> str:
    return base64.b64encode(value).decode()


def decode_key(value: str) -> bytes:
    decoded = base64.b64decode(value, validate=True)
    if len(decoded) != 32:
        raise ValueError("device signing key must be 32 bytes")
    return decoded


def verify_site_policy(policy: dict, pinned_public_key: str | None = None) -> str:
    """Verify a Manager-signed policy and return its public key for TOFU pinning."""
    if not isinstance(policy, dict):
        raise ValueError("Site policy must be an object")
    public_key_b64 = policy.get("signing_public_key")
    signature_b64 = policy.get("signature")
    if not isinstance(public_key_b64, str) or not isinstance(signature_b64, str):
        raise ValueError("Site policy is unsigned")
    if pinned_public_key and public_key_b64 != pinned_public_key:
        raise ValueError("Site policy signing key changed outside an approved rotation")

    signed = {
        key: value for key, value in policy.items()
        if key not in {"signing_public_key", "signing_key_id", "signature"}
    }
    policy_hash = signed.pop("sha256", None)
    canonical_policy = json.dumps(signed, sort_keys=True, separators=(",", ":"))
    if not isinstance(policy_hash, str) or not hashlib.sha256(
        canonical_policy.encode()
    ).hexdigest() == policy_hash:
        raise ValueError("Site policy checksum mismatch")
    signed["sha256"] = policy_hash
    signed_payload = json.dumps(signed, sort_keys=True, separators=(",", ":"))
    try:
        public_key = Ed25519PublicKey.from_public_bytes(decode_key(public_key_b64))
        signature = base64.b64decode(signature_b64, validate=True)
        public_key.verify(signature, signed_payload.encode())
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise ValueError("Site policy signature is invalid") from exc
    return public_key_b64
