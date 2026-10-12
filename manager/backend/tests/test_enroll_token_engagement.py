"""test_enroll_token_engagement.py — Fleet → Add agent: engagement-bound install tokens.

A token created for an engagement must (1) be single-use and short-lived,
(2) refuse engagements that can't take an agent, (3) on use, build the agent's
Site from the engagement's scope *at enrolment time*, assign the agent to the
engagement and burn the token, and (4) degrade to manual approval — never widen
scope — when the engagement changed in between.
"""
from __future__ import annotations

import asyncio
import base64
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from app.models.agent import Agent
from app.models.audit_log import AuditLog
from app.models.probe_enrollment import ProbeEnrollmentToken
from app.models.probe_site import ProbeSite
from app.routers import portal
from app.routers import probe_enrollment as pe
from app.schemas.auth import CurrentUser

NOW = datetime(2026, 10, 2, 10, 0, tzinfo=timezone.utc)


def _engagement(**overrides):
    base = dict(id=uuid.uuid4(), tenant_id=uuid.uuid4(), assigned_agent_id=None,
                scope_cidrs=["10.20.0.0/24"], excluded_cidrs=["10.20.0.1/32"])
    base.update(overrides)
    return SimpleNamespace(**base)


class _Result:
    def __init__(self, value):
        self._value = value

    def scalar_one_or_none(self):
        return self._value

    def scalar_one(self):
        return self._value

    def scalars(self):
        value = self._value
        return SimpleNamespace(all=lambda: list(value or []))


class FakeDB:
    """Returns queued results in order and records everything added; flush()
    gives new rows an id the way the database would."""

    def __init__(self, *results):
        self.results = list(results)
        self.added: list = []
        self.commits = 0

    async def commit(self):
        self.commits += 1

    async def execute(self, _query):
        if not self.results:
            raise AssertionError("unexpected query")
        return _Result(self.results.pop(0))

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        for obj in self.added:
            if not hasattr(obj, "__table__"):
                continue
            if getattr(obj, "id", None) is None:
                obj.id = uuid.uuid4()
            # integer server defaults the database would fill in (version, uses, ...)
            for column in obj.__table__.columns:
                default = getattr(column.server_default, "arg", None)
                if getattr(obj, column.key, None) is None and isinstance(default, str) and default.isdigit():
                    setattr(obj, column.key, int(default))

    def of(self, kind):
        return [obj for obj in self.added if isinstance(obj, kind)]


# ── schema + pure helpers ────────────────────────────────────────────────────

class TestTokenCreateSchema:
    def test_exactly_one_target(self):
        with pytest.raises(ValueError, match="exactly one"):
            pe.EnrollTokenCreate(name="x")
        with pytest.raises(ValueError, match="exactly one"):
            pe.EnrollTokenCreate(name="x", site_id=uuid.uuid4(), engagement_id=uuid.uuid4())
        assert pe.EnrollTokenCreate(name="x", engagement_id=uuid.uuid4()).site_id is None

    def test_engagement_token_installs_one_agent(self):
        with pytest.raises(ValueError, match="exactly one agent"):
            pe.EnrollTokenCreate(name="x", engagement_id=uuid.uuid4(), max_uses=3)

    def test_portal_body_cannot_choose_the_engagement(self):
        body = portal.PortalInstallTokenCreate(name="edge", engagement_id=str(uuid.uuid4()))
        assert not hasattr(body, "engagement_id")


class TestBlocker:
    def test_ready_engagement(self):
        assert pe.engagement_enrollment_blocker(_engagement()) is None

    def test_missing_assigned_or_unscoped(self):
        assert pe.engagement_enrollment_blocker(None) == "Engagement not found"
        assert "already has" in pe.engagement_enrollment_blocker(_engagement(assigned_agent_id=uuid.uuid4()))
        assert "scope" in pe.engagement_enrollment_blocker(_engagement(scope_cidrs=[]))


def test_engagement_site_takes_scope_from_engagement_and_caps_from_device():
    engagement = _engagement()
    row = SimpleNamespace(id=uuid.uuid4(), reported_capabilities=["discovery", "port_scan", "discovery"])
    site = pe.engagement_site(engagement, engagement.tenant_id, row)
    assert site.authorized_cidrs == ["10.20.0.0/24"]
    assert site.excluded_cidrs == ["10.20.0.1/32"]
    assert site.approved_capabilities == ["discovery", "port_scan"]
    assert site.name.startswith(f"engagement-{str(engagement.id)[:8]}-")


def test_token_out_states_and_no_secret():
    row = SimpleNamespace(
        id=uuid.uuid4(), name="edge", token_prefix="vet_abcdefgh", site_id=None,
        engagement_id=uuid.uuid4(), max_uses=1, uses=0, created_at=NOW, last_used_at=None,
        expires_at=NOW + timedelta(hours=1), revoked_at=None, token_hash="h" * 64,
    )
    out = pe.token_out(row, NOW)
    assert out["state"] == "active" and out["usable"] is True
    assert "token_hash" not in out and "token" not in out
    assert pe.token_out(SimpleNamespace(**{**vars(row), "uses": 1}), NOW)["state"] == "used"
    assert pe.token_out(SimpleNamespace(**{**vars(row), "revoked_at": NOW}), NOW)["state"] == "revoked"
    assert pe.token_out(SimpleNamespace(**{**vars(row), "expires_at": NOW}), NOW)["state"] == "expired"


# ── issuing ──────────────────────────────────────────────────────────────────

class TestIssue:
    def test_issues_a_single_use_24h_engagement_token(self):
        engagement = _engagement()
        db = FakeDB([])  # no live tokens yet
        token, raw = asyncio.run(pe.issue_engagement_token(
            db, tenant_id=engagement.tenant_id, engagement=engagement,
            name=" Edge ", created_by="user-1", now=NOW,
        ))
        assert raw.startswith("vet_") and token.token_hash == pe._secret_hash(raw)
        assert token.engagement_id == engagement.id and token.site_id is None
        assert token.max_uses == 1 and token.name == "Edge"
        assert token.expires_at == NOW + timedelta(hours=24)
        audit = db.of(AuditLog)
        assert audit and audit[0].action == "probe.enrollment_token.created"
        assert audit[0].engagement_id == engagement.id
        assert raw not in str(audit[0].detail)

    @pytest.mark.parametrize("engagement,code", [
        (None, 404),
        (_engagement(assigned_agent_id=uuid.uuid4()), 409),
        (_engagement(scope_cidrs=[]), 409),
    ])
    def test_refuses_engagements_that_cannot_take_an_agent(self, engagement, code):
        with pytest.raises(HTTPException) as exc:
            asyncio.run(pe.issue_engagement_token(
                FakeDB(), tenant_id=uuid.uuid4(), engagement=engagement,
                name="x", created_by="u", now=NOW,
            ))
        assert exc.value.status_code == code

    def test_caps_live_unused_tokens(self):
        live = [uuid.uuid4() for _ in range(pe.MAX_LIVE_ENGAGEMENT_TOKENS)]
        with pytest.raises(HTTPException) as exc:
            asyncio.run(pe.issue_engagement_token(
                FakeDB(live), tenant_id=uuid.uuid4(), engagement=_engagement(),
                name="x", created_by="u", now=NOW,
            ))
        assert exc.value.status_code == 409 and "revoke" in exc.value.detail


# ── consumption (POST /probe-enrollment/requests with the token) ─────────────

def _enroll_body(token: str):
    key = base64.b64encode(b"k" * 32).decode()
    return pe.EnrollmentCreate(
        signing_public_key=key, encryption_public_key=key, nonce="n" * 16,
        hostname_hint="branch-vm", platform="linux", architecture="x86_64",
        agent_version="1.0.335", installer_version="1.0.335", build_digest="d" * 16,
        capabilities=["discovery", "port_scan"], enroll_token=token,
    )


def _request():
    return Request({"type": "http", "method": "POST", "path": "/probe-enrollment/requests",
                    "headers": [], "client": ("198.51.100.7", 4000), "query_string": b""})


def _redis():
    redis = MagicMock()
    redis.incr = AsyncMock(return_value=1)
    redis.expire = AsyncMock()
    return redis


def _live_token(engagement):
    return ProbeEnrollmentToken(
        id=uuid.uuid4(), tenant_id=engagement.tenant_id, engagement_id=engagement.id,
        site_id=None, name="edge", token_hash="h", token_prefix="vet_x", max_uses=1, uses=0,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1), revoked_at=None,
    )


class TestConsume:
    def test_token_enrols_and_assigns_the_agent_to_the_engagement(self):
        engagement = _engagement()
        token = _live_token(engagement)
        # waiting-requests count; existing-agent lookup → none; token; engagement; duplicate-name check → none
        db = FakeDB(0, None, token, engagement, None)
        response = asyncio.run(pe.create_enrollment_request(_enroll_body("vet_live"), _request(), db, _redis()))

        assert response["state"] == "approved" and "user_code" not in response
        # committed before answering: the device polls immediately (race fix)
        assert db.commits == 1
        agent = db.of(Agent)[0]
        site = db.of(ProbeSite)[0]
        assert engagement.assigned_agent_id == agent.id
        assert agent.tenant_id == engagement.tenant_id
        assert site.authorized_cidrs == ["10.20.0.0/24"] and site.excluded_cidrs == ["10.20.0.1/32"]
        assert agent.approved_networks == ["10.20.0.0/24"]
        assert token.uses == 1 and token.last_used_at is not None
        actions = [row.action for row in db.of(AuditLog)]
        assert "probe.enrollment.approved" in actions and "portal.agent.assigned" in actions

    def test_engagement_that_gained_an_agent_degrades_to_manual_approval(self):
        engagement = _engagement(assigned_agent_id=uuid.uuid4())
        token = _live_token(engagement)
        db = FakeDB(0, None, token, engagement)
        response = asyncio.run(pe.create_enrollment_request(_enroll_body("vet_live"), _request(), db, _redis()))

        assert response["state"] == "awaiting_approval" and "user_code" in response
        assert not db.of(Agent) and not db.of(ProbeSite)
        assert token.uses == 0  # not burned — nothing was enrolled with it

    def test_used_token_never_auto_approves(self):
        engagement = _engagement()
        token = _live_token(engagement)
        token.uses = 1
        db = FakeDB(0, None, token)
        response = asyncio.run(pe.create_enrollment_request(_enroll_body("vet_live"), _request(), db, _redis()))
        assert response["state"] == "awaiting_approval"
        assert engagement.assigned_agent_id is None


# ── portal endpoints ─────────────────────────────────────────────────────────

def _client(engagement_id):
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client",
                       client_engagement_id=engagement_id)


def _http_request():
    return Request({"type": "http", "method": "POST", "path": "/portal/workspace/fleet/enroll-tokens",
                    "headers": [], "client": ("198.51.100.7", 4000), "query_string": b"",
                    "scheme": "https", "server": ("api.vedhasec.com", 443)})


class TestPortalEndpoints:
    def test_create_binds_to_the_session_engagement_and_returns_commands(self, monkeypatch):
        from app.config import Settings
        from app.routers import agent_distribution

        monkeypatch.setattr(agent_distribution, "get_settings",
                            lambda: Settings(manager_public_url="https://api.vedhasec.com"))
        engagement = _engagement()
        user = _client(engagement.id)
        db = FakeDB(engagement, [])
        out = asyncio.run(portal.portal_workspace_fleet_create_token(
            portal.PortalInstallTokenCreate(name="branch"), _http_request(), user, db,
        ))
        token = db.of(ProbeEnrollmentToken)[0]
        assert token.engagement_id == engagement.id
        assert token.tenant_id == user.tenant_id
        assert out["token"].startswith("vet_")
        assert out["commands"]["one_line"].endswith(f"--manager https://api.vedhasec.com --token {out['token']}")

    def test_revoke_of_another_engagements_token_is_404(self):
        user = _client(uuid.uuid4())
        with pytest.raises(HTTPException) as exc:
            asyncio.run(portal.portal_workspace_fleet_revoke_token(uuid.uuid4(), user, FakeDB(None)))
        assert exc.value.status_code == 404

    def test_revoke_marks_the_token_and_audits(self):
        engagement_id = uuid.uuid4()
        row = SimpleNamespace(id=uuid.uuid4(), revoked_at=None)
        db = FakeDB(row)
        asyncio.run(portal.portal_workspace_fleet_revoke_token(row.id, _client(engagement_id), db))
        assert row.revoked_at is not None
        assert db.of(AuditLog)[0].action == "probe.enrollment_token.revoked"
