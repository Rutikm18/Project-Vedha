from __future__ import annotations

import base64
import hashlib
import json

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from agent.device_identity import (
    decode_key,
    encode_key,
    generate_signing_identity,
    sign_b64,
    signing_public_from_private,
    verify_site_policy,
)


def test_device_identity_round_trip_and_signature_proof() -> None:
    private, public = generate_signing_identity()
    message = "vedha-enrollment:request:challenge"
    signature = base64.b64decode(sign_b64(private, message), validate=True)

    assert len(private) == 32
    assert signing_public_from_private(private) == public
    assert decode_key(encode_key(private)) == private
    Ed25519PublicKey.from_public_bytes(public).verify(signature, message.encode())

    with pytest.raises(InvalidSignature):
        Ed25519PublicKey.from_public_bytes(public).verify(signature, b"tampered")


@pytest.mark.parametrize("invalid", ["not-base64", encode_key(b"short")])
def test_device_identity_rejects_invalid_private_key_encoding(invalid: str) -> None:
    with pytest.raises(ValueError):
        decode_key(invalid)


def test_site_policy_signature_and_tofu_pin_are_enforced() -> None:
    private, public = generate_signing_identity()
    policy = {
        "site_id": "site-1",
        "version": 4,
        "authorized_cidrs": ["10.0.0.0/24"],
        "excluded_cidrs": ["10.0.0.128/25"],
    }
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":"))
    policy["sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    signed_payload = json.dumps(policy, sort_keys=True, separators=(",", ":"))
    policy["signing_public_key"] = encode_key(public)
    policy["signing_key_id"] = hashlib.sha256(public).hexdigest()[:16]
    policy["signature"] = sign_b64(private, signed_payload)

    assert verify_site_policy(policy) == encode_key(public)
    assert verify_site_policy(policy, encode_key(public)) == encode_key(public)

    tampered = {**policy, "authorized_cidrs": ["0.0.0.0/0"]}
    with pytest.raises(ValueError, match="checksum"):
        verify_site_policy(tampered, encode_key(public))
    with pytest.raises(ValueError, match="signing key changed"):
        verify_site_policy(policy, encode_key(b"z" * 32))
