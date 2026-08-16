"""
test_remediation_routes.py — Section 5: operator remediation endpoints + wiring.

Verifies the router is mounted on the app and that the two handlers behave:
  * GET  serves the cached plan on hit, the KB recipe on miss (never empty)
  * POST caches per (finding, os); AI when available, KB fallback otherwise;
    publish flips reviewed; cross-tenant access is 404.

Handlers are called directly with a mocked async db (repo convention).
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import remediation
from app.schemas.auth import CurrentUser


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _finding(title="SSLv3 supported (POODLE)"):
    return SimpleNamespace(id=uuid.uuid4(), engagement_id=uuid.uuid4(), title=title,
                           description="", remediation="", cve_ids=[])


def _db_scalar(*vals):
    db = MagicMock()
    results = []
    for v in vals:
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=v)
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    return db


class _FakeDB:
    """execute() pops queued scalar results; add/flush/refresh are recorded."""
    def __init__(self, scalars):
        self._scalars = list(scalars)
        self.added: list = []
        self.flushed = 0

    async def execute(self, *a, **k):
        r = MagicMock()
        val = self._scalars.pop(0) if self._scalars else None
        r.scalar_one_or_none = MagicMock(return_value=val)
        return r

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        self.flushed += 1

    async def refresh(self, obj):
        # A real flush populates the server_default; emulate it so _serialize works.
        if getattr(obj, "generated_at", None) is None:
            obj.generated_at = datetime.now(timezone.utc)


class _GenUnavailable:
    def __init__(self, db, **kw):
        self.available = False


class _GenAI:
    def __init__(self, db, **kw):
        self.available = True

    async def generate_remediation_plan(self, finding, os):
        return {"category": "ai", "os": os, "source": "ai", "model": "claude-test",
                "summary": "Patch and harden.", "effort": "low", "remediation_risk": "low",
                "steps": [{"step": 1, "title": "Patch", "description": "",
                           "commands_for_os": ["sudo apt-get upgrade"], "verification": "",
                           "risk": "low"}],
                "verification": [], "long_term_recommendations": [],
                "compensating_controls": ""}


# ── wiring ───────────────────────────────────────────────────────────────────────

def test_remediation_router_is_mounted():
    from app.main import app
    paths = {getattr(r, "path", None) for r in app.routes}
    assert "/findings/{finding_id}/remediation" in paths
    assert "/findings/{finding_id}/remediation/generate" in paths


# ── GET ──────────────────────────────────────────────────────────────────────────

class TestGetRemediation:
    def test_kb_on_cache_miss(self):
        db = _db_scalar(_finding(), None)          # finding, then no cached row
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert res["source"] == "deterministic_kb"
        assert res["cached"] is False
        assert res["reviewed"] is False
        assert res["plan"]["steps"]

    def test_cached_ai_on_hit(self):
        row = SimpleNamespace(reviewed=True, source="ai", model="claude-x",
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _db_scalar(_finding(), row)
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert res["source"] == "ai"
        assert res["cached"] is True
        assert res["reviewed"] is True
        assert res["model"] == "claude-x"

    def test_cross_tenant_is_404(self):
        db = _db_scalar(None)                       # tenant-scoped finding query misses
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert e.value.status_code == 404


# ── POST /generate ─────────────────────────────────────────────────────────────────

class TestGenerateRemediation:
    def test_ai_unavailable_falls_back_to_kb_and_publish_sets_reviewed(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenUnavailable)
        db = _FakeDB([_finding(), None])           # finding, then upsert cache miss
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=True, publish=True))
        assert res["source"] == "deterministic_kb"
        assert res["reviewed"] is True
        assert db.added and db.added[0].reviewed is True
        assert db.added[0].source == "deterministic_kb"

    def test_ai_available_caches_ai_plan(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenAI)
        db = _FakeDB([_finding(), None])
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=True, publish=False))
        assert res["source"] == "ai"
        assert res["model"] == "claude-test"
        assert res["reviewed"] is False
        assert db.added[0].source == "ai"

    def test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenUnavailable)
        row = SimpleNamespace(reviewed=False, source="ai", model="claude-x",
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_finding(), row])            # finding, cache hit
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=False, publish=True))
        assert res["source"] == "ai"
        assert row.reviewed is True                 # publish flipped it
        assert db.flushed >= 1
        assert not db.added                         # cached hit — nothing new inserted

    def test_cross_tenant_is_404(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenUnavailable)
        db = _FakeDB([None])
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.generate_remediation(
                uuid.uuid4(), db, _operator(), os="linux"))
        assert e.value.status_code == 404
