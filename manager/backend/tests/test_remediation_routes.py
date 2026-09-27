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
from app.schemas.remediation import RemediationPlanOut


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _finding(title="SSLv3 supported (POODLE)"):
    from app.models.enums import FindingSeverity, FindingStatus
    now = datetime.now(timezone.utc)
    return SimpleNamespace(id=uuid.uuid4(), engagement_id=uuid.uuid4(), title=title,
                           description="", remediation="", cve_ids=[],
                           severity=FindingSeverity.high, status=FindingStatus.open,
                           first_seen=now, created_at=now, due_at=None)


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


# ── wiring ───────────────────────────────────────────────────────────────────────

def test_remediation_router_is_mounted():
    # Via the app's OpenAPI schema: FastAPI >=0.13x keeps included routers as
    # wrappers in app.routes, so a flat path scan no longer sees nested routes.
    from app.main import app
    paths = set(app.openapi()["paths"])
    assert "/findings/{finding_id}/remediation" in paths
    assert "/findings/{finding_id}/remediation/generate" in paths


# ── GET ──────────────────────────────────────────────────────────────────────────

class TestGetRemediation:
    def test_kb_on_cache_miss(self):
        db = _db_scalar(_finding(), None, None, None)   # finding, no cache, no engagement/tenant SLA
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert res["source"] == "deterministic_kb"
        assert res["cached"] is False
        assert res["reviewed"] is False
        assert res["plan"]["steps"]
        validated = RemediationPlanOut.model_validate(res)
        assert validated.plan.steps[0].title

    def test_cached_ai_on_hit(self):
        row = SimpleNamespace(reviewed=True, source="ai", model="claude-x",
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _db_scalar(_finding(), row, None, None)
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert res["source"] == "ai"
        assert res["plan"]["due"]["source"] == "default"
        assert res["cached"] is True
        assert res["reviewed"] is True
        assert res["model"] == "claude-x"
        # Older cached rows are normalized by the response contract rather than
        # failing the entire detail view on a newly-added presentation field.
        validated = RemediationPlanOut.model_validate(res)
        assert validated.plan.steps[0].title == "Remediation step"

    def test_cross_tenant_is_404(self):
        db = _db_scalar(None)                       # tenant-scoped finding query misses
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert e.value.status_code == 404


# ── POST /refine (and the /generate alias) ─────────────────────────────────────────

def _ai_plan(kb_plan):
    return {**kb_plan, "source": "ai", "model": "claude-test", "summary": "Refined."}


class TestRefineRemediation:
    def _patch(self, monkeypatch, *, fail=False):
        calls = {}

        async def fake_refine(db, *, engagement, kb_plan, contexts, findings, actor_id, svc=None):
            calls["kb"] = kb_plan
            calls["contexts"] = contexts
            if fail:
                from app.services.llm import AiRuntimeError
                raise AiRuntimeError("no AI provider is configured", 503)
            return _ai_plan(kb_plan)

        monkeypatch.setattr(remediation.ai_refine, "refine", fake_refine)
        return calls

    def test_refine_overlays_kb_and_caches_unreviewed(self, monkeypatch):
        calls = self._patch(monkeypatch)
        # finding, cache miss, engagement(SLA) , tenant SLA, engagement(refine), upsert
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(None), _scalar_result(None),
                      _scalar_result(None), _scalar_result(None),
                      _one_result(_returning_row(False, model="claude-test"))])
        res = asyncio.run(remediation.refine_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=False, publish=False))
        assert res["source"] == "ai" and res["reviewed"] is False
        assert calls["kb"]["source"] == "deterministic_kb"      # started from the KB floor

    def test_unavailable_is_503_and_nothing_cached(self, monkeypatch):
        self._patch(monkeypatch, fail=True)
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(None)])
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.refine_remediation(
                uuid.uuid4(), db, _operator(), os="linux", force=False, publish=False))
        assert e.value.status_code == 503
        assert db.executed == 5                                  # no upsert ran

    def test_cached_fresh_ai_returned_and_publish_flips(self, monkeypatch):
        self._patch(monkeypatch)
        row = SimpleNamespace(reviewed=False, source="ai", model="claude-x", facts_fingerprint=None,
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(row)])
        res = asyncio.run(remediation.refine_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=False, publish=True))
        assert res["source"] == "ai" and row.reviewed is True
        assert db.executed == 2

    def test_generate_is_an_alias(self, monkeypatch):
        self._patch(monkeypatch)
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(None), _scalar_result(None),
                      _scalar_result(None), _scalar_result(None),
                      _one_result(_returning_row(True, model="claude-test"))])
        res = asyncio.run(remediation.generate_remediation(
            uuid.uuid4(), db, _operator(), os="linux", force=False, publish=True))
        assert res["source"] == "ai" and res["reviewed"] is True

    def test_cross_tenant_is_404(self, monkeypatch):
        self._patch(monkeypatch)
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.refine_remediation(
                uuid.uuid4(), _FakeDB([_scalar_result(None)]), _operator(), os="linux"))
        assert e.value.status_code == 404


class TestStaleAndPublish:
    def test_stale_when_fingerprint_differs(self):
        row = SimpleNamespace(reviewed=True, source="ai", model="m", facts_fingerprint="old",
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(row)])
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert res["stale"] is True

    def test_publish_stale_is_409(self):
        row = SimpleNamespace(reviewed=False, source="ai", model="m", facts_fingerprint="old",
                              plan={"source": "ai"}, generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(row)])
        with pytest.raises(HTTPException) as e:
            asyncio.run(remediation.publish_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert e.value.status_code == 409

    def test_publish_fresh(self):
        row = SimpleNamespace(reviewed=False, source="ai", model="m", facts_fingerprint=None,
                              plan={"source": "ai", "steps": [{"step": 1}]},
                              generated_at=datetime.now(timezone.utc))
        db = _FakeDB([_scalar_result(_finding()), _scalar_result(row)])
        db.add = lambda obj: None
        res = asyncio.run(remediation.publish_remediation(uuid.uuid4(), db, _operator(), os="linux"))
        assert row.reviewed is True and res["reviewed"] is True


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

    def test_bundle_upsert_targets_partial_index(self):
        from sqlalchemy.dialects.postgresql import dialect
        stmt = remediation._build_bundle_upsert_stmt(
            tenant_id=uuid.uuid4(), engagement_id=uuid.uuid4(), fix_key="abcdef123456", os="linux",
            plan={"source": "ai"}, publish=False, facts_fingerprint="f")
        sql = str(stmt.compile(dialect=dialect())).lower()
        assert "on conflict (engagement_id, fix_key, os) where subject_type = 'bundle'" in sql
        assert "reviewed = excluded.reviewed" in sql


# ── v2 contextual plans ──────────────────────────────────────────────────────────

def _scalars_result(vals):
    r = MagicMock()
    r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=list(vals))))
    return r


class TestContextualGet:
    def _grounded(self):
        f = SimpleNamespace(id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=uuid.uuid4(),
                            title="SMBv1 enabled (wormable, deprecated)", description="",
                            remediation="", cve_ids=[], severity=__import__("app.models.enums", fromlist=["x"]).FindingSeverity.critical,
                            evidence={"rule_id": "POSTURE-SMB-V1-ENABLED", "port": 445},
                            epss_score=None, exploit_validated=False,
                            status=__import__("app.models.enums", fromlist=["x"]).FindingStatus.open,
                            first_seen=datetime.now(timezone.utc), created_at=datetime.now(timezone.utc),
                            due_at=None)
        asset = SimpleNamespace(ip_address="10.0.0.5", hostname="FS01", fqdn=None, os="Windows",
                                os_version="Windows Server 2012 R2",
                                asset_type=SimpleNamespace(value="server"),
                                criticality=SimpleNamespace(value="high"), environment=None, tags=None)
        svc = SimpleNamespace(port=445, protocol="tcp", service_name="microsoft-ds", product="SMB",
                              version=None, cpe=None, banner=None, exposure="internal_only")
        return f, asset, svc

    def test_os_defaults_to_scanned_os_and_v2_fields_survive_schema(self):
        f, asset, svc = self._grounded()
        db = _FakeDB([_scalar_result(f), _scalar_result(asset), _scalars_result([svc]),
                      _scalar_result(None)])
        res = asyncio.run(remediation.get_remediation(f.id, db, _operator(), os=None))
        assert res["os"] == "windows"
        out = RemediationPlanOut.model_validate(res)
        assert out.plan.recipe_id == "POSTURE-SMB-V1-ENABLED"
        assert out.plan.context["host"]["value"] == "FS01"
        assert out.plan.verification_check["scanner"] == "smb_scan"
        assert out.plan.steps[0].tier == "containment"
        assert out.plan.exposure == "internal"
        assert out.plan.due["source"] == "default" and out.plan.due["at"]

    def test_explicit_os_is_respected(self):
        f, asset, svc = self._grounded()
        db = _FakeDB([_scalar_result(f), _scalar_result(asset), _scalars_result([svc]),
                      _scalar_result(None)])
        res = asyncio.run(remediation.get_remediation(f.id, db, _operator(), os="linux"))
        assert res["os"] == "linux"

# ── platform auto-detection (os=auto, the default) ────────────────────────────

def _asset_result(asset):
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=asset)
    return r


def _services_result(services):
    r = MagicMock()
    r.scalars.return_value.all.return_value = services
    return r


def _windows_asset():
    return SimpleNamespace(id=uuid.uuid4(), ip_address="10.0.0.9", hostname="dc01", fqdn=None,
                           os="Windows Server 2019", asset_type="server", device_role=None,
                           role_detail=None, role_confidence=None, tags=None)


class TestAutoPlatform:
    def test_get_auto_resolves_asset_os(self):
        f = _finding("SMB signing not required")
        f.asset_id = uuid.uuid4()
        db = _FakeDB([_scalar_result(f), _asset_result(_windows_asset()),
                      _services_result([]), _scalar_result(None)])
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="auto"))
        RemediationPlanOut.model_validate(res)
        assert res["os"] == "windows"
        assert res["platform"]["requested"] == "auto"
        assert res["platform"]["source"] == "asset_os"
        assert res["platform"]["family"] == "windows"
        # Windows commands are served, not the generic fallback.
        step_cmds = " ".join(c for s in res["plan"]["steps"] for c in s["commands_for_os"])
        assert "Set-SmbServerConfiguration -RequireSecuritySignature" in step_cmds

    def test_get_auto_without_asset_is_generic_not_detected(self):
        f = _finding()
        f.asset_id = None
        db = _FakeDB([_scalar_result(f), _scalar_result(None)])
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="auto"))
        assert res["os"] == "generic"
        assert res["platform"]["source"] == "no_asset"
        assert db.executed == 4          # finding, cache, engagement + tenant SLA (due date)

    def test_explicit_os_is_an_override(self):
        f = _finding()
        f.asset_id = uuid.uuid4()
        db = _FakeDB([_scalar_result(f), _scalar_result(None)])
        res = asyncio.run(remediation.get_remediation(uuid.uuid4(), db, _operator(), os="macos"))
        assert res["os"] == "macos"
        assert res["platform"] == {"requested": "macos", "os": "macos", "family": None,
                                   "source": "requested", "evidence": None, "confidence": None}
        mac = " ".join(c for s in res["plan"]["steps"] for c in s["commands_for_os"])
        assert "Set-ItemProperty" not in mac     # the override really selects other commands

    def test_default_query_value_is_auto(self):
        import inspect
        for fn in (remediation.get_remediation, remediation.generate_remediation,
                   remediation.refine_remediation, remediation.publish_remediation):
            assert inspect.signature(fn).parameters["os"].default.default == "auto"
