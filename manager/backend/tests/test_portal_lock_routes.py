"""Portal plan locks at the route level: activation on every customer request,
the 403 gates for locked findings and locked features, and a coverage check that
fails when a portal route that needs a gate is added without one."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.auth import portal_scope
from app.routers import portal
from app.services import portal_locks


@pytest.fixture(autouse=True)
def _clean():
    portal_locks._LOCKED.set(None)
    portal_locks._FEATURES.set(None)
    yield
    portal_locks._LOCKED.set(None)
    portal_locks._FEATURES.set(None)


def _db(first_row):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: first_row))
    return db


def _client_user(engagement_id=None):
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="client",
                           engagement_id=engagement_id or uuid.uuid4())


# ── activation ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_customer_request_activates_its_plan_locks(monkeypatch):
    monkeypatch.setattr(portal_scope, "assert_client", lambda u: u.engagement_id)
    user = await portal_scope.require_client_with_locks(
        _client_user(), _db((["critical", "high"], ["reports"])))
    assert user.role == "client"
    assert portal_locks.current() == frozenset({"critical", "high"})
    assert portal_locks.feature_locked("reports") and not portal_locks.feature_locked("ai_assistant")


@pytest.mark.asyncio
async def test_customer_without_a_plan_has_nothing_locked(monkeypatch):
    monkeypatch.setattr(portal_scope, "assert_client", lambda u: u.engagement_id)
    await portal_scope.require_client_with_locks(_client_user(), _db(None))
    assert portal_locks.current() == frozenset()


def test_locks_set_in_a_dependency_are_visible_inside_the_route():
    app = FastAPI()

    async def dep() -> None:
        portal_locks.activate(["critical"], ["ai_assistant"])

    @app.get("/probe", dependencies=[Depends(dep)])
    async def probe():
        return {"locked": sorted(portal_locks.current()),
                "ai": portal_locks.feature_locked("ai_assistant")}

    assert TestClient(app).get("/probe").json() == {"locked": ["critical"], "ai": True}


# ── gates ─────────────────────────────────────────────────────────────────────

def _sev_db(severity):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: severity))
    return db


@pytest.mark.asyncio
async def test_locked_finding_is_403_with_the_plan_message():
    portal_locks.activate(["critical", "high"])
    with pytest.raises(HTTPException) as exc:
        await portal_locks.ensure_finding_unlocked(_sev_db("critical"), uuid.uuid4(), uuid.uuid4())
    assert exc.value.status_code == 403
    assert exc.value.detail == portal_locks.LOCKED_MESSAGE


@pytest.mark.asyncio
async def test_open_or_missing_finding_passes_the_gate():
    portal_locks.activate(["critical"])
    await portal_locks.ensure_finding_unlocked(_sev_db("medium"), uuid.uuid4(), uuid.uuid4())
    await portal_locks.ensure_finding_unlocked(_sev_db(None), uuid.uuid4(), uuid.uuid4())  # handler 404s


@pytest.mark.asyncio
async def test_no_locks_skips_the_lookup():
    db = _sev_db("critical")
    await portal_locks.ensure_finding_unlocked(db, uuid.uuid4(), uuid.uuid4())
    db.execute.assert_not_awaited()


@pytest.mark.parametrize("feature", ["ai_assistant", "reports", "remediation", "compliance"])
def test_locked_feature_is_403_with_its_message(feature):
    portal_locks.activate([], [feature])
    with pytest.raises(HTTPException) as exc:
        portal_locks.ensure_feature_unlocked(feature)
    assert exc.value.status_code == 403
    assert "licensed plan" in exc.value.detail
    portal_locks.activate([], [])
    portal_locks.ensure_feature_unlocked(feature)          # open again: no error


def test_written_reports_are_withheld_while_any_severity_is_locked():
    portal_locks.activate(["critical"], [])
    with pytest.raises(HTTPException) as exc:
        portal_locks.ensure_written_reports_available()
    assert exc.value.detail == portal_locks.WRITTEN_REPORTS_MESSAGE
    portal_locks.activate([], [])
    portal_locks.ensure_written_reports_available()


# ── teaser ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_teaser_counts_only_locked_severities_and_reads_without_the_guard():
    portal_locks.activate(["critical", "high"])
    seen_guard = []

    async def execute(_stmt):
        seen_guard.append(portal_locks.current())
        return MagicMock(all=lambda: [("critical", 2), ("high", 1)])

    db = MagicMock(execute=execute)
    out = await portal_locks.locked_teaser(db, uuid.uuid4())
    assert out == {"locked_severities": ["critical", "high"], "counts": {"critical": 2, "high": 1},
                   "total": 3, "message": "Available on a licensed plan."}
    assert seen_guard == [frozenset()]                   # counted with the guard lifted
    assert portal_locks.current() == frozenset({"critical", "high"})   # and restored


@pytest.mark.asyncio
async def test_teaser_is_empty_when_nothing_is_locked():
    db = MagicMock(execute=AsyncMock())
    out = await portal_locks.locked_teaser(db, uuid.uuid4())
    assert out["total"] == 0 and out["counts"] == {}
    db.execute.assert_not_awaited()


# ── coverage: every route that needs a gate has it ────────────────────────────

def _deps(route):
    names = set()
    stack = list(route.dependant.dependencies)
    while stack:
        d = stack.pop()
        names.add(getattr(d.call, "__name__", ""))
        stack.extend(d.dependencies)
    return names


def _portal_routes():
    return [r for r in portal.router.routes if hasattr(r, "dependant")]


def test_every_portal_route_with_a_finding_id_has_the_lock_gate():
    missing = [r.path for r in _portal_routes()
               if "{finding_id}" in r.path and "finding_lock_gate" not in _deps(r)]
    assert missing == []


@pytest.mark.parametrize("fragment,gate", [
    ("/assistant/", "ai_assistant_gate"),
    ("/remediation", "remediation_gate"),
    ("/obligations", "compliance_gate"),
    ("/compliance-brief", "compliance_gate"),
    ("/reports", "written_reports_gate"),
])
def test_feature_routes_have_their_gate(fragment, gate):
    routes = [r for r in _portal_routes() if fragment in r.path]
    assert routes, f"no portal route matches {fragment}"
    missing = [r.path for r in routes if gate not in _deps(r)]
    assert missing == []


def test_customer_ai_report_generation_sits_behind_the_reports_switch():
    from app.routers import engagement_report
    route = next(r for r in engagement_report.router.routes
                 if getattr(r, "path", "") == "/portal/ai-report/engagement")
    assert "reports_gate" in _deps(route)
