"""The audit trail: what an entry carries, how request context reaches it, which events
write one, and that entries written on a failing path survive."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app import audit_context
from app.audit_middleware import AuditContextMiddleware
from app.auth import mfa as mfa_lib
from app.auth import rbac
from app.auth import router as auth_router
from app.auth.exceptions import PasswordMismatchError, UserNotFoundError
from app.models.enums import UserRole
from app.schemas.auth import LoginRequest, LoginResponse, MfaCodeRequest
from app.services import audit, org_settings


@pytest.fixture(autouse=True)
def _clean_context():
    audit_context.clear()
    yield
    audit_context.clear()


# ── the entry ────────────────────────────────────────────────────────────────

def test_an_entry_takes_request_context_when_the_caller_does_not_pass_it():
    tenant = uuid.uuid4()
    audit_context.bind(ip="203.0.113.9", user_agent="curl/8", request_id="req-1",
                       tenant_id=str(tenant), actor_type="user")
    e = audit.build_entry(actor_id="u1", action="finding.updated")
    assert (e.ip_address, e.user_agent, e.request_id, e.tenant_id, e.actor_type) == (
        "203.0.113.9", "curl/8", "req-1", tenant, "user")
    assert e.outcome == "success" and e.timestamp.tzinfo is not None


def test_explicit_values_beat_the_context():
    audit_context.bind(ip="203.0.113.9", tenant_id=str(uuid.uuid4()))
    other = uuid.uuid4()
    e = audit.build_entry(actor_id="u1", action="x", ip="198.51.100.1", tenant_id=other,
                          actor_type="client", outcome="denied")
    assert (e.ip_address, e.tenant_id, e.actor_type, e.outcome) == ("198.51.100.1", other, "client", "denied")


def test_an_unknown_outcome_is_refused_and_long_text_is_clipped():
    with pytest.raises(ValueError):
        audit.build_entry(actor_id="u", action="x", outcome="maybe")
    e = audit.build_entry(actor_id="u", action="x", user_agent="a" * 900, actor_label="b" * 900)
    assert len(e.user_agent) == 255 and len(e.actor_label) == 255


def test_record_audit_joins_the_callers_transaction():
    db = MagicMock()
    audit.record_audit(db, actor_id="u", action="x", detail={"k": 1}, changes={"f": {"before": 1, "after": 2}})
    (row,) = [c.args[0] for c in db.add.call_args_list]
    assert row.detail == {"k": 1} and row.changes == {"f": {"before": 1, "after": 2}}


def test_an_independent_write_survives_a_failing_request_and_never_raises(audit_sink, monkeypatch):
    asyncio.run(audit.record_audit_independent(actor_id="u", action="auth.login.failure", outcome="failure"))
    assert [e.action for e in audit_sink] == ["auth.login.failure"]

    async def boom(_entry):
        raise RuntimeError("db down")

    monkeypatch.setattr(audit, "_commit_entry", boom)
    asyncio.run(audit.record_audit_independent(actor_id="u", action="x"))   # must not raise


# ── request context ──────────────────────────────────────────────────────────

def _app():
    app = FastAPI()
    app.add_middleware(AuditContextMiddleware)

    @app.get("/ctx")
    async def ctx():
        return audit_context.current()

    return app


def test_the_middleware_binds_source_agent_and_a_request_id():
    out = TestClient(_app()).get("/ctx", headers={"user-agent": "probe/1", "x-request-id": "abc-123"}).json()
    assert out["user_agent"] == "probe/1" and out["request_id"] == "abc-123"
    assert out["method"] == "GET" and out["path"] == "/ctx" and out["ip"]


def test_a_hostile_request_id_is_replaced_not_stored():
    out = TestClient(_app()).get("/ctx", headers={"x-request-id": "bad id;\t<script>"}).json()
    assert uuid.UUID(out["request_id"])


# ── sign-in events ───────────────────────────────────────────────────────────

def test_a_failed_sign_in_is_recorded_with_its_reason_and_the_generic_401_is_unchanged(audit_sink, monkeypatch):
    user = SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), client_engagement_id=None,
                           email="ops@vedha.io", role=UserRole.manager)

    async def fail(*_a, **_k):
        raise auth_router._tag_user(PasswordMismatchError("no"), user)

    monkeypatch.setattr(auth_router, "_authenticate", fail)
    monkeypatch.setattr(auth_router, "check_login_failures", AsyncMock())
    monkeypatch.setattr(auth_router, "record_login_failure", AsyncMock())
    request = SimpleNamespace(headers={}, client=SimpleNamespace(host="203.0.113.5"))
    monkeypatch.setattr(auth_router, "client_ip", lambda _r: "203.0.113.5")

    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.login(LoginRequest(email="ops@vedha.io", password="pw"), request, AsyncMock(), MagicMock()))
    assert caught.value.status_code == 401 and caught.value.detail == auth_router._GENERIC_401
    (entry,) = audit_sink
    assert (entry.action, entry.outcome, entry.actor_id, entry.tenant_id, entry.actor_label) == (
        "auth.login.failure", "failure", str(user.id), user.tenant_id, "ops@vedha.io")
    assert entry.detail == {"reason": "password_mismatch"}


def test_an_unknown_account_is_recorded_as_anonymous_with_the_email_tried(audit_sink, monkeypatch):
    async def fail(*_a, **_k):
        raise UserNotFoundError("none")

    monkeypatch.setattr(auth_router, "_authenticate", fail)
    monkeypatch.setattr(auth_router, "check_login_failures", AsyncMock())
    monkeypatch.setattr(auth_router, "record_login_failure", AsyncMock())
    monkeypatch.setattr(auth_router, "client_ip", lambda _r: "203.0.113.5")
    with pytest.raises(HTTPException):
        asyncio.run(auth_router.login(LoginRequest(email="ghost@x.io", password="pw"),
                                      SimpleNamespace(headers={}, client=None), AsyncMock(), MagicMock()))
    (entry,) = audit_sink
    assert (entry.actor_id, entry.actor_type, entry.actor_label, entry.tenant_id) == (
        "anonymous", "anonymous", "ghost@x.io", None)
    assert entry.detail == {"reason": "user_not_found"}


def test_a_locked_account_is_recorded_as_denied(audit_sink, monkeypatch):
    def too_many(*_a, **_k):
        raise HTTPException(429, "slow down")

    monkeypatch.setattr(auth_router, "check_login_failures", AsyncMock(side_effect=too_many))
    monkeypatch.setattr(auth_router, "client_ip", lambda _r: "203.0.113.5")
    with pytest.raises(HTTPException) as caught:
        asyncio.run(auth_router.login(LoginRequest(email="ops@vedha.io", password="pw"),
                                      SimpleNamespace(headers={}, client=None), AsyncMock(), MagicMock()))
    assert caught.value.status_code == 429
    assert [(e.action, e.outcome) for e in audit_sink] == [("auth.login.locked", "denied")]


def test_a_wrong_second_step_code_is_recorded(audit_sink, monkeypatch):
    user = SimpleNamespace(
        id=uuid.uuid4(), tenant_id=uuid.uuid4(), email="ops@vedha.io", role=UserRole.manager,
        is_active=True, password_expires_at=None, hashed_password="x", mfa_enabled=True,
        mfa_secret_enc=mfa_lib.encrypt_secret("GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"), mfa_last_step=None,
        mfa_recovery_hashes=[], mfa_enabled_at=None, client_engagement_id=None)
    monkeypatch.setattr(org_settings, "get_section", AsyncMock(return_value=org_settings.AuthPolicy()))
    monkeypatch.setattr(auth_router, "client_ip", lambda _r: "203.0.113.5")
    db = AsyncMock()
    found, tenant = MagicMock(), MagicMock()
    found.scalar_one_or_none.return_value = user
    tenant.scalar_one_or_none.return_value = SimpleNamespace(is_active=True)
    db.execute = AsyncMock(side_effect=[found, tenant])
    token, _ = mfa_lib.create_challenge(str(user.id), str(user.tenant_id), mfa_lib.PURPOSE_VERIFY)

    class Redis:
        def __init__(self): self.d = {}
        async def get(self, k): return self.d.get(k)
        async def set(self, k, v, ex=None): self.d[k] = v
        async def incr(self, k): self.d[k] = str(int(self.d.get(k, "0")) + 1); return int(self.d[k])
        async def expire(self, k, s): return True
        async def delete(self, k): self.d.pop(k, None)
        async def ttl(self, k): return 60

    with pytest.raises(HTTPException):
        asyncio.run(auth_router.mfa_verify(MfaCodeRequest(mfa_token=token, code="000000"),
                                           SimpleNamespace(headers={}, client=None), db, Redis()))
    assert [(e.action, e.outcome, e.actor_id) for e in audit_sink] == [
        ("auth.mfa.challenge_failed", "failure", str(user.id))]


def test_a_successful_sign_in_is_recorded_with_the_method(audit_sink):
    user = SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), email="ops@vedha.io",
                           role=UserRole.manager, client_engagement_id=None)
    asyncio.run(auth_router._audit_sign_in_success(user, method="password"))
    (entry,) = audit_sink
    assert (entry.action, entry.outcome, entry.actor_type, entry.detail) == (
        "auth.login.success", "success", "user", {"method": "password", "role": "manager"})


def test_a_client_sign_in_is_typed_as_a_client(audit_sink):
    user = SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), email="ciso@c.io",
                           role=UserRole.client, client_engagement_id=uuid.uuid4())
    asyncio.run(auth_router._audit_sign_in_success(user, method="password"))
    assert audit_sink[0].actor_type == "client"


# ── access control ───────────────────────────────────────────────────────────

def test_a_refused_role_is_recorded_before_the_403(audit_sink):
    audit_context.bind(method="DELETE", path="/users/7")
    check = rbac.require_role(["admin"]).dependency
    user = SimpleNamespace(role="analyst", user_id=uuid.uuid4(), tenant_id=uuid.uuid4())
    with pytest.raises(HTTPException) as caught:
        asyncio.run(check(user))
    assert caught.value.status_code == 403
    (entry,) = audit_sink
    assert (entry.action, entry.outcome, entry.actor_id) == ("access.denied", "denied", str(user.user_id))
    assert entry.detail == {"method": "DELETE", "path": "/users/7", "role": "analyst", "required_roles": ["admin"]}


def test_a_permitted_role_writes_nothing(audit_sink):
    check = rbac.require_role(["admin"]).dependency
    user = SimpleNamespace(role="admin", user_id=uuid.uuid4(), tenant_id=uuid.uuid4())
    assert asyncio.run(check(user)) is user
    assert audit_sink == []


# ── retention rules (no database) ────────────────────────────────────────────

def test_retention_is_held_between_the_legal_floor_and_a_ceiling():
    from app.services.audit_integrity import (
        DEFAULT_RETENTION_DAYS, MAX_RETENTION_DAYS, MIN_RETENTION_DAYS, clamp_retention_days)
    assert clamp_retention_days(None) == DEFAULT_RETENTION_DAYS == 365
    assert clamp_retention_days(7) == MIN_RETENTION_DAYS == 180
    assert clamp_retention_days(99999) == MAX_RETENTION_DAYS
    assert clamp_retention_days(730) == 730


def test_the_audit_policy_refuses_a_period_under_the_floor():
    with pytest.raises(Exception):
        org_settings.AuditPolicy(retention_days=30)
    assert org_settings.AuditPolicy().retention_days == 365


def test_every_catalogued_action_has_a_category_and_a_label():
    from app.services import audit_catalog as c
    for code, info in c.CATALOG.items():
        assert info.category in c.CATEGORIES and info.label, code
    assert c.describe("org_settings.auth.updated").label == "Organisation auth policy changed"
    unknown = c.describe("brand.new_thing")
    assert unknown.category == "other" and unknown.label and not unknown.customer_visible
