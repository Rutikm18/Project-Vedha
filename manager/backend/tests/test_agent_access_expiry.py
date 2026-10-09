"""Agent access expiry, set from Fleet and enforced only by the manager.

Past access_expires_at the manager refuses the agent's heartbeats, job polls and
token refreshes, but still accepts an in-flight scan's result/chunk uploads so a
job running at the moment of expiry isn't lost. Enforcement lives in one helper
(app.agent_access) used by the auth middleware and the refresh endpoint.
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app import agent_access
from app.routers import agents as agents_router
from app.routers import probe_enrollment as pe
from app.schemas.auth import CurrentUser

# Fixed instant for the pure is_expired(x, now) checks only. The routes read the
# real clock, so anything sent through a route is built from _now() instead:
# NOW + 7 days stopped being in the future on 2026-10-09 and broke the suite.
NOW = datetime(2026, 10, 2, 12, 0, tzinfo=timezone.utc)


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── the pure helper ──────────────────────────────────────────────────────────

class TestIsExpired:
    def test_none_never_expires(self):
        assert agent_access.is_expired(None, NOW) is False

    def test_future_is_live_past_is_expired(self):
        assert agent_access.is_expired(NOW + timedelta(hours=1), NOW) is False
        assert agent_access.is_expired(NOW - timedelta(seconds=1), NOW) is True

    def test_exact_instant_counts_as_expired(self):
        assert agent_access.is_expired(NOW, NOW) is True

    def test_naive_datetime_is_treated_as_utc(self):
        naive = NOW.replace(tzinfo=None) - timedelta(minutes=1)
        assert agent_access.is_expired(naive, NOW) is True


class TestResultUploadStaysOpen:
    @pytest.mark.parametrize("path,allowed", [
        ("/agents/abc/jobs/def/result", True),
        ("/agents/abc/jobs/def/chunks", True),
        ("/agents/abc/jobs", False),            # new work — blocked when expired
        ("/agents/heartbeat", False),
        ("/engagements/e/scope", False),
    ])
    def test_only_in_flight_uploads_survive_expiry(self, path, allowed):
        assert agent_access.path_allows_after_expiry(path) is allowed


# ── enforcement at the refresh endpoint ──────────────────────────────────────

def _credential(agent_id, now):
    return SimpleNamespace(
        agent_id=agent_id, generation=3, revoked_at=None,
        expires_at=now + timedelta(days=30),
        refresh_secret_hash=pe._secret_hash("refresh-secret-value-long-enough-xxxx"),
        signing_public_key="pk", last_nonce=None, last_used_at=None,
    )


def _refresh_db(credential, agent):
    db = MagicMock()
    results = [credential, agent]
    async def execute(_q):
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=results.pop(0))
        return r
    db.execute = AsyncMock(side_effect=execute)
    return db


def _refresh_body(agent_id):
    return SimpleNamespace(
        agent_id=agent_id, generation=3,
        refresh_secret="refresh-secret-value-long-enough-xxxx",
        nonce="n" * 16, signature="s" * 48,
    )


def test_refresh_is_refused_for_an_expired_agent(monkeypatch):
    agent_id = uuid.uuid4()
    agent = SimpleNamespace(id=agent_id, tenant_id=uuid.uuid4(), lifecycle_status="active",
                            credential_generation=3, access_expires_at=datetime(2020, 1, 1, tzinfo=timezone.utc))
    monkeypatch.setattr(pe, "_verify_signature", lambda *a, **k: None)
    redis = MagicMock(); redis.incr = AsyncMock(return_value=1); redis.expire = AsyncMock()
    redis.set = AsyncMock(return_value=True)
    request = MagicMock()
    request.client.host = "10.0.0.9"; request.headers = {}
    with pytest.raises(HTTPException) as exc:
        asyncio.run(pe.refresh_device_token(
            _refresh_body(agent_id), request, _refresh_db(_credential(agent_id, _now()), agent), redis,
        ))
    assert exc.value.status_code == 403 and "expired" in exc.value.detail.lower()


# ── Fleet set/extend endpoint ────────────────────────────────────────────────

def _operator():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _agent_db(agent):
    db = MagicMock()
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=agent)
    db.execute = AsyncMock(return_value=r)
    db.add = MagicMock()
    db.flush = AsyncMock()
    return db


def test_operator_sets_and_clears_expiry():
    user = _operator()
    agent = SimpleNamespace(id=uuid.uuid4(), tenant_id=user.tenant_id, access_expires_at=None)
    db = _agent_db(agent)
    when = _now() + timedelta(days=7)
    out = asyncio.run(agents_router.set_agent_access_expiry(
        agent.id, agents_router.AgentExpiryUpdate(access_expires_at=when), db, user))
    assert agent.access_expires_at == when
    assert out["access_expired"] is False
    # clearing
    out = asyncio.run(agents_router.set_agent_access_expiry(
        agent.id, agents_router.AgentExpiryUpdate(access_expires_at=None), db, user))
    assert agent.access_expires_at is None and out["access_expires_at"] is None


def test_setting_a_past_date_expires_immediately():
    user = _operator()
    agent = SimpleNamespace(id=uuid.uuid4(), tenant_id=user.tenant_id, access_expires_at=None)
    out = asyncio.run(agents_router.set_agent_access_expiry(
        agent.id, agents_router.AgentExpiryUpdate(access_expires_at=datetime(2020, 1, 1, tzinfo=timezone.utc)),
        _agent_db(agent), user))
    assert out["access_expired"] is True


def test_unknown_agent_is_404():
    user = _operator()
    with pytest.raises(HTTPException) as exc:
        asyncio.run(agents_router.set_agent_access_expiry(
            uuid.uuid4(), agents_router.AgentExpiryUpdate(access_expires_at=None), _agent_db(None), user))
    assert exc.value.status_code == 404


# ── install-command lifetimes (T16) ──────────────────────────────────────────

class TestLifetimes:
    def test_engagement_token_accepts_only_the_three_presets(self):
        eng = uuid.uuid4()
        for minutes in (60, 1440, 10080):
            assert pe.EnrollTokenCreate(name="x", engagement_id=eng, expires_in_minutes=minutes)
        for bad in (30, 120, 4320):
            with pytest.raises(ValueError, match="one of"):
                pe.EnrollTokenCreate(name="x", engagement_id=eng, expires_in_minutes=bad)

    def test_site_token_still_capped_at_24h(self):
        site = uuid.uuid4()
        assert pe.EnrollTokenCreate(name="x", site_id=site, expires_in_minutes=120)
        with pytest.raises(ValueError, match="at most 1440"):
            pe.EnrollTokenCreate(name="x", site_id=site, expires_in_minutes=10080)

    def test_portal_body_validates_lifetime(self):
        from app.routers.portal import PortalInstallTokenCreate
        assert PortalInstallTokenCreate(lifetime_minutes=10080).lifetime_minutes == 10080
        assert PortalInstallTokenCreate().lifetime_minutes == 1440   # default 24 h
        with pytest.raises(ValueError, match="one of"):
            PortalInstallTokenCreate(lifetime_minutes=99)
