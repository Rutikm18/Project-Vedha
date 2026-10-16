"""GET /findings/ids — the filtered id set that scopes a findings export.

Null means "no finding-level filter active", so the caller exports the whole
engagement instead of sending a long id list. The agent filter is threaded
through even though FindingFilters does not carry it.
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import findings as findings_router
from app.routers.findings import FindingFilters, filtered_finding_ids, list_finding_ids
from app.schemas.auth import CurrentUser

_TENANT = uuid.uuid4()


def _user():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=_TENANT, role="manager")


# ── the endpoint shape ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_endpoint_returns_null_when_no_filter(monkeypatch):
    monkeypatch.setattr(findings_router, "filtered_finding_ids", AsyncMock(return_value=None))
    out = await list_finding_ids(
        db=MagicMock(), current_user=_user(), engagement_id=uuid.uuid4(),
        agent_id=None, filters=FindingFilters())
    assert out == {"finding_ids": None}


@pytest.mark.asyncio
async def test_endpoint_returns_sorted_string_ids(monkeypatch):
    a, b, c = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    monkeypatch.setattr(findings_router, "filtered_finding_ids", AsyncMock(return_value={a, b, c}))
    out = await list_finding_ids(
        db=MagicMock(), current_user=_user(), engagement_id=uuid.uuid4(),
        agent_id=None, filters=FindingFilters(severity=None))
    assert out["finding_ids"] == sorted([str(a), str(b), str(c)])
    # stable ordering so the export's query param is deterministic
    assert out["finding_ids"] == sorted(out["finding_ids"])


@pytest.mark.asyncio
async def test_endpoint_passes_agent_to_the_resolver(monkeypatch):
    agent = uuid.uuid4()
    spy = AsyncMock(return_value=set())
    monkeypatch.setattr(findings_router, "filtered_finding_ids", spy)
    await list_finding_ids(
        db=MagicMock(), current_user=_user(), engagement_id=uuid.uuid4(),
        agent_id=agent, filters=FindingFilters())
    assert spy.await_args.kwargs["agent_id"] == agent


# ── filtered_finding_ids: the None rule + agent threading ───────────────────────

@pytest.mark.asyncio
async def test_resolver_none_when_truly_unfiltered():
    out = await filtered_finding_ids(
        MagicMock(), _user(), uuid.uuid4(), FindingFilters(), agent_id=None)
    assert out is None


@pytest.mark.asyncio
async def test_resolver_queries_when_only_agent_is_set(monkeypatch):
    rid = uuid.uuid4()
    seen: dict = {}

    async def fake_filtered(stmt, db, user, **kw):
        seen.update(kw)
        return "QUERY", None

    monkeypatch.setattr(findings_router, "_filtered_findings", fake_filtered)
    db = MagicMock()

    async def fake_execute(q):
        assert q == "QUERY"
        r = MagicMock()
        r.scalars.return_value.all.return_value = [rid]
        return r

    db.execute = fake_execute
    out = await filtered_finding_ids(
        db, _user(), uuid.uuid4(), FindingFilters(), agent_id=uuid.uuid4())
    assert out == {rid}
    assert seen.get("agent_id") is not None  # threaded through to _filtered_findings
