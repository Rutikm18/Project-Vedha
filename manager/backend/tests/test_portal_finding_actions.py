from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.audit_log import AuditLog
from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding_event import FindingEvent
from app.routers import findings as finding_routes
from app.routers.portal import (
    patch_portal_finding,
    portal_workspace_finding_summary,
    portal_workspace_findings,
)
from app.schemas.auth import CurrentUser
from app.schemas.finding import FindingPatch


def _client(engagement_id: uuid.UUID) -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="client",
        client_engagement_id=engagement_id,
    )


def _finding(engagement_id: uuid.UUID):
    now = datetime.now(timezone.utc)
    return SimpleNamespace(
        id=uuid.uuid4(),
        engagement_id=engagement_id,
        asset_id=None,
        status=FindingStatus.open,
        severity=FindingSeverity.high,
        cvss_score=None,
        risk_score=None,
        remediation=None,
        resolved_at=None,
        resolution_method=None,
        resolution_run_id=None,
        reopened_count=0,
        evidence={},
        updated_at=now,
    )


@pytest.mark.asyncio
async def test_customer_transition_mutates_shared_row_and_records_origin():
    engagement_id = uuid.uuid4()
    finding = _finding(engagement_id)
    user = _client(engagement_id)
    added = []
    result = MagicMock(scalar_one_or_none=lambda: finding)
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock(side_effect=added.append)

    updated = await patch_portal_finding(
        finding.id,
        FindingPatch(status=FindingStatus.accepted, action_reason="Approved exception"),
        user,
        db,
    )

    assert updated is finding
    assert finding.status == FindingStatus.accepted
    event = next(row for row in added if isinstance(row, FindingEvent))
    assert event.actor_type == "customer"
    assert event.detail == {"origin": "portal", "reason": "Approved exception"}
    audit = next(row for row in added if isinstance(row, AuditLog))
    assert audit.engagement_id == engagement_id
    assert audit.detail["origin"] == "portal"


@pytest.mark.asyncio
async def test_customer_cannot_mutate_a_finding_outside_bound_engagement():
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    result = MagicMock(scalar_one_or_none=lambda: None)
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)

    with pytest.raises(HTTPException) as exc:
        await patch_portal_finding(
            uuid.uuid4(),
            FindingPatch(status=FindingStatus.confirmed),
            user,
            db,
        )

    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_workspace_queries_pin_engagement_and_forward_agent_filter(monkeypatch):
    engagement_id = uuid.uuid4()
    agent_id = uuid.uuid4()
    user = _client(engagement_id)
    db = MagicMock()
    list_result = object()
    summary_result = object()
    list_findings = AsyncMock(return_value=list_result)
    finding_summary = AsyncMock(return_value=summary_result)
    monkeypatch.setattr(finding_routes, "list_findings", list_findings)
    monkeypatch.setattr(finding_routes, "finding_summary", finding_summary)

    listed = await portal_workspace_findings(
        user=user,
        db=db,
        agent_id=agent_id,
    )
    summarized = await portal_workspace_finding_summary(
        user=user,
        db=db,
        agent_id=agent_id,
    )

    assert listed is list_result
    assert summarized is summary_result
    assert list_findings.await_args.kwargs["engagement_id"] == engagement_id
    assert list_findings.await_args.kwargs["agent_id"] == agent_id
    assert finding_summary.await_args.kwargs == {
        "db": db,
        "current_user": user,
        "engagement_id": engagement_id,
        "agent_id": agent_id,
    }
