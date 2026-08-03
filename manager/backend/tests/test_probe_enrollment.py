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


# ── Pre-authorized, Site-bound enrollment tokens ────────────────────────────

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.routers.probe_enrollment import (
    ENROLL_TOKEN_PREFIX,
    EnrollmentCreate,
    EnrollTokenCreate,
    _secret_hash,
    enroll_token_is_usable,
    generate_enroll_token,
)


def _token(**overrides):
    now = datetime.now(timezone.utc)
    base = dict(revoked_at=None, expires_at=now + timedelta(minutes=30), uses=0, max_uses=1)
    base.update(overrides)
    return SimpleNamespace(**base)


def test_generate_enroll_token_is_prefixed_hashed_and_shown_once() -> None:
    raw, token_hash, prefix = generate_enroll_token()

    assert raw.startswith(ENROLL_TOKEN_PREFIX)
    assert token_hash == _secret_hash(raw)          # only the hash is stored
    assert prefix == raw[:12] and raw != token_hash  # prefix is display-only
    # distinct each call
    assert generate_enroll_token()[0] != raw


def test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses() -> None:
    now = datetime.now(timezone.utc)
    assert enroll_token_is_usable(_token(), now) is True
    assert enroll_token_is_usable(None, now) is False
    assert enroll_token_is_usable(_token(revoked_at=now), now) is False
    assert enroll_token_is_usable(_token(expires_at=now - timedelta(seconds=1)), now) is False
    assert enroll_token_is_usable(_token(uses=1, max_uses=1), now) is False
    # a multi-use token remains usable until exhausted
    assert enroll_token_is_usable(_token(uses=1, max_uses=3), now) is True


def test_enroll_token_create_defaults_and_bounds() -> None:
    import uuid

    body = EnrollTokenCreate(name="dmz-probe", site_id=uuid.uuid4())
    assert body.max_uses == 1 and body.expires_in_minutes == 60  # single-use, short TTL

    with pytest.raises(ValueError):
        EnrollTokenCreate(name="x", site_id=uuid.uuid4(), expires_in_minutes=5000)  # > 24h
    with pytest.raises(ValueError):
        EnrollTokenCreate(name="x", site_id=uuid.uuid4(), max_uses=0)


def test_enrollment_create_accepts_optional_enroll_token() -> None:
    valid_key = base64.b64encode(b"x" * 32).decode()
    fields = dict(
        signing_public_key=valid_key,
        encryption_public_key=valid_key,
        nonce="a" * 16,
        platform="linux",
        architecture="x86_64",
        agent_version="1.0",
        installer_version="1.0",
        build_digest="d" * 8,
    )
    assert EnrollmentCreate(**fields).enroll_token is None          # manual path unchanged
    assert EnrollmentCreate(**fields, enroll_token="vet_abc123xy").enroll_token == "vet_abc123xy"
