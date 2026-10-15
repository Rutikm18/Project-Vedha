"""Finding-selection scope for the canonical report: the ``finding_ids`` filter
on the loader, its parsing and forwarding in the route, and the AI generate
request field."""

from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers.report_document import _parse_finding_ids, get_report_document
from app.services.report_document import load_report_document

from tests.test_report_document import NOW, _asset, _engagement, _finding


# ── _parse_finding_ids ──────────────────────────────────────────────────────────

def test_parse_finding_ids_reads_a_comma_separated_subset():
    a, b = uuid.uuid4(), uuid.uuid4()
    assert _parse_finding_ids(f"{a},{b}") == {a, b}


def test_parse_finding_ids_tolerates_blanks_and_whitespace():
    a = uuid.uuid4()
    assert _parse_finding_ids(f" {a} , , ") == {a}


def test_parse_finding_ids_falls_back_to_whole_engagement():
    # Absent, empty, or all-invalid falls back to the whole engagement rather
    # than silently emptying the report.
    assert _parse_finding_ids(None) is None
    assert _parse_finding_ids("") is None
    assert _parse_finding_ids("not-a-uuid,also-bad") is None


def test_parse_finding_ids_drops_invalid_tokens_but_keeps_valid_ones():
    good = uuid.uuid4()
    assert _parse_finding_ids(f"{good},not-a-uuid") == {good}


# ── route forwards the parsed scope ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_route_forwards_parsed_finding_ids_to_the_loader(monkeypatch):
    from app.routers import report_document as report_router

    document = object()
    loader = AsyncMock(return_value=document)
    monkeypatch.setattr(report_router, "load_report_document", loader)
    user = SimpleNamespace(tenant_id=uuid.uuid4())
    engagement_id = uuid.uuid4()
    a, b = uuid.uuid4(), uuid.uuid4()

    result = await get_report_document(engagement_id, MagicMock(), user, finding_ids=f"{a},{b}")

    assert result is document
    assert loader.await_args.kwargs["finding_ids"] == {a, b}


@pytest.mark.asyncio
async def test_route_passes_none_scope_when_no_selection(monkeypatch):
    from app.routers import report_document as report_router

    loader = AsyncMock(return_value=object())
    monkeypatch.setattr(report_router, "load_report_document", loader)
    user = SimpleNamespace(tenant_id=uuid.uuid4())

    await get_report_document(uuid.uuid4(), MagicMock(), user)

    assert loader.await_args.kwargs["finding_ids"] is None


# ── loader scopes and recomputes for the subset ─────────────────────────────────

def _result(*, scalar=None, rows=None, scalar_rows=None):
    value = MagicMock()
    value.scalar_one_or_none.return_value = scalar
    value.all.return_value = rows or []
    value.scalars.return_value.all.return_value = scalar_rows or []
    return value


@pytest.mark.asyncio
async def test_loader_scopes_findings_to_the_selection_and_recomputes_summary():
    tenant_id = uuid.uuid4()
    engagement = _engagement(tenant_id=tenant_id)
    asset = _asset(engagement.id)
    # Two findings; no runs/assignees so the loader's related-row queries stay minimal.
    keep = _finding(
        engagement.id, asset.id, uuid.uuid4(),
        detection_run_id=None, initial_detection_run_id=None, resolution_run_id=None,
        assigned_to=None,
    )
    drop = _finding(
        engagement.id, asset.id, uuid.uuid4(),
        detection_run_id=None, initial_detection_run_id=None, resolution_run_id=None,
        assigned_to=None,
    )

    db = MagicMock()
    db.get_bind.return_value = SimpleNamespace(dialect=SimpleNamespace(name="test"))
    db.execute = AsyncMock(
        side_effect=[
            _result(scalar=engagement),             # engagement
            _result(rows=[(keep, asset), (drop, asset)]),  # findings (both loaded)
            _result(scalar_rows=[asset.tags]),      # asset tags
            _result(scalar_rows=[]),                # finding events
            _result(scalar_rows=[]),                # remediation plans
            _result(scalar=None),                   # SLA policy → default windows
            _result(scalar=None),                   # latest completed run (coverage sheet)
        ]
    )

    document = await load_report_document(
        db,
        tenant_id=tenant_id,
        engagement_id=engagement.id,
        generated_at=NOW,
        finding_ids={keep.id},
    )

    assert document is not None
    assert document.summary.total_findings == 1
    assert [f.id for f in document.findings] == [keep.id]


@pytest.mark.asyncio
async def test_loader_with_no_scope_keeps_every_finding():
    tenant_id = uuid.uuid4()
    engagement = _engagement(tenant_id=tenant_id)
    asset = _asset(engagement.id)
    f1 = _finding(engagement.id, asset.id, uuid.uuid4(),
                  detection_run_id=None, initial_detection_run_id=None,
                  resolution_run_id=None, assigned_to=None)
    f2 = _finding(engagement.id, asset.id, uuid.uuid4(),
                  detection_run_id=None, initial_detection_run_id=None,
                  resolution_run_id=None, assigned_to=None)

    db = MagicMock()
    db.get_bind.return_value = SimpleNamespace(dialect=SimpleNamespace(name="test"))
    db.execute = AsyncMock(
        side_effect=[
            _result(scalar=engagement),
            _result(rows=[(f1, asset), (f2, asset)]),
            _result(scalar_rows=[asset.tags]),
            _result(scalar_rows=[]),
            _result(scalar_rows=[]),
            _result(scalar=None),
            _result(scalar=None),
        ]
    )

    document = await load_report_document(
        db, tenant_id=tenant_id, engagement_id=engagement.id, generated_at=NOW,
    )

    assert document is not None
    assert document.summary.total_findings == 2


# ── AI generate accepts the selection ───────────────────────────────────────────

def test_ai_generate_request_accepts_selected_finding_ids():
    from app.routers.ai_report import GenerateRequest

    a, b = uuid.uuid4(), uuid.uuid4()
    req = GenerateRequest(selected_finding_ids=[a, b])
    assert req.model_dump()["selected_finding_ids"] == [a, b]
    # Omitted ⇒ None ⇒ the generator writes up all findings (prior behaviour).
    assert GenerateRequest().selected_finding_ids is None
