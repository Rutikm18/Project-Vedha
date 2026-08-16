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


def _scalar_result(val):
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=val)
    return r


def _one_result(row):
    """A result whose .one() yields the RETURNING row (upsert path)."""
    r = MagicMock()
    r.one = MagicMock(return_value=row)
    return r


def _returning_row(reviewed, model=None):
    return SimpleNamespace(reviewed=reviewed, model=model,
                           generated_at=datetime.now(timezone.utc))


class _FakeDB:
    """execute() returns the next queued result object; flush is counted."""
    def __init__(self, results):
        self._results = list(results)
        self.executed = 0
        self.flushed = 0

    async def execute(self, *a, **k):
        self.executed += 1
        return self._results.pop(0) if self._results else _scalar_result(None)

    async def flush(self):
        self.flushed += 1


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
        # finding lookup, then the atomic upsert RETURNING row (reviewed=True).
        db = _FakeDB([_scalar_result(_finding()), _one_result(_returning_row(True))])
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=True, publish=True))
        assert res["source"] == "deterministic_kb"
        assert res["reviewed"] is True
        assert db.executed == 2                     # tenant finding + single upsert

    def test_ai_available_caches_ai_plan(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenAI)
        db = _FakeDB([_scalar_result(_finding()),
                      _one_result(_returning_row(False, model="claude-test"))])
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=True, publish=False))
        assert res["source"] == "ai"
        assert res["model"] == "claude-test"
        assert res["reviewed"] is False

    def test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenUnavailable)
        row = SimpleNamespace(reviewed=False, source="ai", model="claude-x",
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(row)])  # finding, cache hit
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=False, publish=True))
        assert res["source"] == "ai"
        assert row.reviewed is True                 # publish flipped it
        assert db.flushed >= 1
        assert db.executed == 2                     # no third query — early return

    def test_cross_tenant_is_404(self, monkeypatch):
        monkeypatch.setattr(remediation, "LLMReportGenerator", _GenUnavailable)
        db = _FakeDB([_scalar_result(None)])
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.generate_remediation(
                uuid.uuid4(), db, _operator(), os="linux"))
        assert e.value.status_code == 404


class TestUpsertStatement:
    """Verify the ON CONFLICT logic at the SQL level (no DB needed)."""

    def _sql(self, publish):
        from sqlalchemy.dialects.postgresql import dialect
        stmt = remediation._build_upsert_stmt(
            tenant_id=uuid.uuid4(), engagement_id=uuid.uuid4(), finding_id=uuid.uuid4(),
            os="linux", plan={"source": "ai", "model": "x", "steps": []}, publish=publish)
        return str(stmt.compile(dialect=dialect())).lower()

    def test_targets_the_unique_constraint(self):
        assert "on conflict on constraint uq_remediation_finding_os" in self._sql(True)

    def test_regeneration_resets_review_gate_not_inherits_prior_approval(self):
        # New content must RE-PASS review: `reviewed` = the caller's publish intent
        # (excluded), and must NOT OR-in the stale prior value — otherwise a
        # force-regenerate of an approved plan would leak unreviewed AI content.
        sql = self._sql(False)
        set_clause = sql.split("returning")[0]
        assert "reviewed = excluded.reviewed" in set_clause
        assert "remediation_plans.reviewed" not in set_clause   # no OR with prior value

    def test_refreshes_generated_at_on_conflict(self):
        assert "generated_at = now()" in self._sql(True)
