from __future__ import annotations

import base64
import uuid

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from app.auth.jwt import create_device_access_token, decode_token
from app.routers.probe_enrollment import (
    SitePolicyInput,
    _decode_public_key,
    _derive_refresh_secret,
    _verify_signature,
)


def test_device_access_token_has_dedicated_audience_and_generation() -> None:
    token = create_device_access_token(str(uuid.uuid4()), str(uuid.uuid4()), 3)
    claims = decode_token(token)

    assert claims["role"] == "agent"
    assert claims["type"] == "access"
    assert claims["typ"] == "device_access"
    assert claims["aud"] == "vedha-probe-api"
    assert claims["credential_generation"] == 3


def test_public_key_must_be_canonical_base64_of_32_bytes() -> None:
    valid = base64.b64encode(b"x" * 32).decode()
    assert _decode_public_key(valid, "key") == b"x" * 32

    with pytest.raises(ValueError, match="exactly 32 bytes"):
        _decode_public_key(base64.b64encode(b"short").decode(), "key")
    with pytest.raises(ValueError, match="canonical base64"):
        _decode_public_key("not-base64", "key")


def test_ed25519_proof_of_possession_rejects_tampering() -> None:
    private = Ed25519PrivateKey.generate()
    public_b64 = base64.b64encode(private.public_key().public_bytes_raw()).decode()
    message = "vedha-enrollment:request:challenge"
    signature = base64.b64encode(private.sign(message.encode())).decode()

    _verify_signature(public_b64, message, signature)
    with pytest.raises(Exception, match="Invalid device proof"):
        _verify_signature(public_b64, message + "-tampered", signature)


def test_refresh_secret_is_stable_per_request_and_device_secret() -> None:
    request_id = uuid.uuid4()
    first = _derive_refresh_secret(request_id, "device-secret-value")

    assert first == _derive_refresh_secret(request_id, "device-secret-value")
    assert first != _derive_refresh_secret(request_id, "other-device-secret")


def test_site_policy_rejects_exclusion_outside_authorized_scope() -> None:
    with pytest.raises(ValueError, match="not inside authorized_cidrs"):
        SitePolicyInput(
            user_code="ABCD-EFGH",
            probe_name="probe-1",
            site_name="site-1",
            authorized_cidrs=["10.0.0.0/24"],
            excluded_cidrs=["10.1.0.0/24"],
            approved_capabilities=["discovery"],
        )
