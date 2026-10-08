"""Two-step sign-in (TOTP): the algorithm, secrets, recovery codes, challenge
tokens, and the sign-in / enrolment handlers."""
from __future__ import annotations

import asyncio
import base64
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.auth import mfa as mfa_lib
from app.auth import router as auth_router
from app.auth import totp
from app.models.enums import UserRole
from app.schemas.auth import LoginResponse, MfaCodeRequest, MfaTokenRequest
from app.services import org_settings

RFC_SECRET = base64.b32encode(b"12345678901234567890").decode()


class FakeRedis:
    def __init__(self):
        self.data: dict[str, str] = {}

    async def get(self, key):
        return self.data.get(key)

    async def set(self, key, value, ex=None):
        self.data[key] = value

    async def incr(self, key):
        self.data[key] = str(int(self.data.get(key, "0")) + 1)
        return int(self.data[key])

    async def expire(self, key, seconds):
        return True

    async def delete(self, key):
        self.data.pop(key, None)

    async def ttl(self, key):
        return 60


# ── algorithm ────────────────────────────────────────────────────────────────

def test_totp_matches_rfc6238_vectors():
    # RFC 6238 Appendix B (SHA-1), last six digits of the eight-digit values.
    assert totp.totp(RFC_SECRET, now=59) == "287082"
    assert totp.totp(RFC_SECRET, now=1111111109) == "081804"
    assert totp.totp(RFC_SECRET, now=1234567890) == "005924"


def test_verify_allows_one_step_of_drift_and_refuses_reuse():
    now = 1_000_000_000
    code_now = totp.totp(RFC_SECRET, now=now)
    previous = totp.totp(RFC_SECRET, now=now - 30)
    step = totp.verify(RFC_SECRET, code_now, now=now)
    assert step == totp.current_step(now)
    assert totp.verify(RFC_SECRET, previous, now=now) == step - 1
    # The same code (same step) cannot be used twice.
    assert totp.verify(RFC_SECRET, code_now, now=now, last_step=step) is None
    # Two steps away is too far.
    assert totp.verify(RFC_SECRET, totp.totp(RFC_SECRET, now=now - 90), now=now) is None
    assert totp.verify(RFC_SECRET, "12345", now=now) is None
    # Spaces in what people type are fine.
    assert totp.verify(RFC_SECRET, f"{code_now[:3]} {code_now[3:]}", now=now) == step


def test_provisioning_uri_is_what_authenticator_apps_read():
    uri = totp.provisioning_uri("JBSWY3DPEHPK3PXP", "a@b.io")
    assert uri.startswith("otpauth://totp/Vedha:a@b.io?")
    assert "secret=JBSWY3DPEHPK3PXP" in uri and "issuer=Vedha" in uri and "digits=6" in uri and "period=30" in uri


def test_generated_secrets_are_160_bit_and_distinct():
    a, b = totp.generate_secret(), totp.generate_secret()
    assert a != b and len(a) == 32


# ── storage ──────────────────────────────────────────────────────────────────

def test_secret_is_encrypted_at_rest():
    token = mfa_lib.encrypt_secret("JBSWY3DPEHPK3PXP")
    assert "JBSWY3DPEHPK3PXP" not in token
    assert mfa_lib.decrypt_secret(token) == "JBSWY3DPEHPK3PXP"
    assert mfa_lib.decrypt_secret("not-a-token") is None
    assert mfa_lib.decrypt_secret(None) is None


def test_recovery_codes_are_hashed_and_single_use():
    codes, hashes = mfa_lib.new_recovery_codes()
    assert len(codes) == 10 and len(set(codes)) == 10
    assert all(len(c) == 11 and c[5] == "-" for c in codes)
    assert not any(c in "".join(hashes) for c in codes)
    remaining = mfa_lib.consume_recovery_code(hashes, codes[3].lower().replace("-", " "))
    assert remaining is not None and len(remaining) == 9
    assert mfa_lib.consume_recovery_code(remaining, codes[3]) is None
    assert mfa_lib.looks_like_recovery_code(codes[0])
    assert not mfa_lib.looks_like_recovery_code("123456")


# ── challenge tokens ─────────────────────────────────────────────────────────

def test_challenge_token_is_scoped_and_not_a_session():
    token, jti = mfa_lib.create_challenge("u1", "t1", mfa_lib.PURPOSE_VERIFY)
    claims = mfa_lib.decode_challenge(token)
    assert claims["sub"] == "u1" and claims["purpose"] == "verify" and claims["jti"] == jti
    # Not an access token: the auth middleware only accepts type == "access".
    assert claims["type"] != "access"
    assert mfa_lib.decode_challenge(token + "x") is None
    # An access token is not a challenge.
    from app.auth.jwt import create_access_token
    assert mfa_lib.decode_challenge(create_access_token("u1", "t1", "admin")) is None


def test_challenge_allows_five_attempts_and_is_spent_once():
    async def run():
        redis = FakeRedis()
        assert await mfa_lib.challenge_usable(redis, "j1")
        for _ in range(mfa_lib.CHALLENGE_MAX_ATTEMPTS):
            await mfa_lib.record_challenge_failure(redis, "j1")
        assert not await mfa_lib.challenge_usable(redis, "j1")
        await mfa_lib.spend_challenge(redis, "j2")
        assert not await mfa_lib.challenge_usable(redis, "j2")
    asyncio.run(run())


def test_policy_requires_mfa_per_audience():
    policy = org_settings.AuthPolicy(mfa_required_for_operators=True)
    assert org_settings.mfa_required(policy, role="manager")
    assert org_settings.mfa_required(policy, role="admin")
    assert not org_settings.mfa_required(policy, role="client")
    assert org_settings.mfa_required(org_settings.AuthPolicy(mfa_required_for_customers=True), role="client")


# ── handlers ─────────────────────────────────────────────────────────────────

def _user(**kw):
    secret = kw.pop("secret", RFC_SECRET)
    return SimpleNamespace(
        id=uuid.uuid4(), tenant_id=uuid.uuid4(), email="ops@vedha.io", role=UserRole.manager,
        is_active=True, password_expires_at=None, hashed_password="x",
        mfa_enabled=True, mfa_secret_enc=mfa_lib.encrypt_secret(secret), mfa_last_step=None,
        mfa_recovery_hashes=[], mfa_enabled_at=None, client_engagement_id=None, **kw,
    )


def _db_for(user):
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    tenant = MagicMock()
    tenant.scalar_one_or_none.return_value = SimpleNamespace(is_active=True)
    db.execute = AsyncMock(side_effect=[result, tenant])
    db.add = MagicMock()
    return db


@pytest.fixture
def wired(monkeypatch):
    monkeypatch.setattr(org_settings, "get_section", AsyncMock(return_value=org_settings.AuthPolicy()))
    issued = []

    async def fake_issue(user, redis, bound):
        issued.append(user.id)
        return LoginResponse(access_token="access", refresh_token="refresh")

    monkeypatch.setattr(auth_router, "_issue_session", fake_issue)
    request = SimpleNamespace(headers={}, client=SimpleNamespace(host="203.0.113.5"))
    monkeypatch.setattr(auth_router, "client_ip", lambda _r: "203.0.113.5")
    return SimpleNamespace(issued=issued, request=request)


def test_correct_code_finishes_sign_in_once(wired):
    user = _user()
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)
    redis = FakeRedis()
    code = totp.totp(RFC_SECRET)

    out = asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code=code), wired.request, _db_for(user), redis))
    assert out.access_token == "access" and wired.issued == [user.id]
    assert user.mfa_last_step == totp.current_step()

    # The challenge is spent: replaying it fails even with a fresh code.
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code=code), wired.request, _db_for(user), redis))
    assert caught.value.status_code == 401


def test_wrong_code_is_counted_and_never_issues_a_session(wired):
    user = _user()
    token, jti = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)
    redis = FakeRedis()
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code="000000"), wired.request, _db_for(user), redis))
    assert caught.value.status_code == 401 and caught.value.detail == "Invalid or expired code"
    assert wired.issued == []
    assert redis.data[f"mfa:attempts:{jti}"] == "1"


def test_recovery_code_signs_in_and_is_used_up(wired):
    codes, hashes = mfa_lib.new_recovery_codes()
    user = _user()
    user.mfa_recovery_hashes = hashes
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)
    out = asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code=codes[0]), wired.request, _db_for(user), FakeRedis()))
    assert out.access_token == "access"
    assert len(user.mfa_recovery_hashes) == 9


def test_enrolment_challenge_cannot_be_used_to_verify(wired):
    user = _user()
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_ENROLL)
    with pytest.raises(HTTPException):
        asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code=totp.totp(RFC_SECRET)), wired.request, _db_for(user), FakeRedis()))
    assert wired.issued == []


def test_required_enrolment_turns_mfa_on_and_signs_in(wired):
    user = _user()
    user.mfa_enabled = False
    user.mfa_secret_enc = None
    redis = FakeRedis()
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_ENROLL)

    setup = asyncio.run(auth_router.mfa_enroll_setup(MfaTokenRequest(mfa_token=token), wired.request, _db_for(user), redis))
    assert setup.otpauth_uri.startswith("otpauth://totp/")
    # The pending secret is stored encrypted, never in clear.
    assert setup.secret not in "".join(redis.data.values())

    out = asyncio.run(auth_router.mfa_enroll_enable(
        MfaCodeRequest(mfa_token=token, code=totp.totp(setup.secret)), wired.request, _db_for(user), redis))
    assert user.mfa_enabled is True and len(out.recovery_codes) == 10
    assert out.access_token == "access"
    assert mfa_lib.decrypt_secret(user.mfa_secret_enc) == setup.secret


def test_flag_without_a_secret_is_not_treated_as_enrolled(wired):
    # A row flagged on before secrets existed must not lock its owner out.
    user = _user()
    user.mfa_secret_enc = None
    assert auth_router._has_mfa(user) is False
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)
    with pytest.raises(HTTPException):
        asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code=totp.totp(RFC_SECRET)), wired.request, _db_for(user), FakeRedis()))


# ── signed-in management ─────────────────────────────────────────────────────

from app.schemas.auth import CurrentUser, MfaDisableRequest, MfaEnableRequest  # noqa: E402


def _single_db(user):
    db = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    db.execute = AsyncMock(return_value=result)
    db.add = MagicMock()
    return db


def _me(user, role="admin", **kw):
    return CurrentUser(user_id=kw.pop("user_id", user.id), tenant_id=kw.pop("tenant_id", user.tenant_id), role=role, **kw)


def test_admin_reset_clears_another_users_mfa_in_the_same_tenant(wired):
    target = _user()
    target.mfa_recovery_hashes = ["h"]
    admin = _me(target, user_id=uuid.uuid4())
    out = asyncio.run(auth_router.mfa_reset(target.id, wired.request, admin, _single_db(target)))
    assert out == {"user_id": str(target.id), "mfa_enabled": False}
    assert target.mfa_enabled is False and target.mfa_secret_enc is None and target.mfa_recovery_hashes == []


def test_admin_reset_hides_other_tenants_and_refuses_self(wired):
    target = _user()
    other_tenant_admin = _me(target, user_id=uuid.uuid4(), tenant_id=uuid.uuid4())
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_reset(target.id, wired.request, other_tenant_admin, _single_db(target)))
    assert caught.value.status_code == 404 and target.mfa_enabled is True
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_reset(target.id, wired.request, _me(target), _single_db(target)))
    assert caught.value.status_code == 409


def test_wrong_code_in_a_session_is_400_not_401(wired, monkeypatch):
    # A 401 would read to the browser as "signed out" and end the session.
    user = _user()
    monkeypatch.setattr(auth_router._pwd, "verify", lambda *_: True)
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_disable(MfaDisableRequest(password="pw", code="000000"), wired.request,
                                            _me(user, role="manager"), _single_db(user), FakeRedis()))
    assert caught.value.status_code == 400 and user.mfa_enabled is True
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_new_recovery_codes(MfaEnableRequest(code="000000"), wired.request,
                                                       _me(user, role="manager"), _single_db(user), FakeRedis()))
    assert caught.value.status_code == 400


def test_mfa_cannot_be_turned_off_when_the_organisation_requires_it(wired, monkeypatch):
    user = _user()
    monkeypatch.setattr(org_settings, "get_section", AsyncMock(return_value=org_settings.AuthPolicy(mfa_required_for_operators=True)))
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_disable(MfaDisableRequest(password="pw", code=totp.totp(RFC_SECRET)), wired.request,
                                            _me(user, role="manager"), _single_db(user), FakeRedis()))
    assert caught.value.status_code == 409 and user.mfa_enabled is True


def test_api_tokens_cannot_manage_mfa(wired):
    user = _user()
    pat = _me(user, role="manager", auth_type="pat")
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.mfa_status(pat, _single_db(user)))
    assert caught.value.status_code == 403


def test_required_setup_never_replaces_an_existing_authenticator(wired):
    user = _user()  # already enrolled
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_ENROLL)
    before = user.mfa_secret_enc
    for call in (
        lambda: auth_router.mfa_enroll_setup(MfaTokenRequest(mfa_token=token), wired.request, _db_for(user), FakeRedis()),
        lambda: auth_router.mfa_enroll_enable(MfaCodeRequest(mfa_token=token, code="123456"), wired.request, _db_for(user), FakeRedis()),
    ):
        with pytest.raises(HTTPException) as caught:
            asyncio.run(call())
        assert caught.value.status_code == 409
    assert user.mfa_secret_enc == before and wired.issued == []
