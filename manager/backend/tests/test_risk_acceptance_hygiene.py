"""M12 — a risk can only be accepted with an owner, a future expiry and a compensating control."""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.enums import FindingStatus
from app.schemas.finding import FindingPatch
from app.services import finding_workflow as wf

FUTURE = (datetime.now(timezone.utc) + timedelta(days=90)).isoformat()


def _finding(asset_id=None):
    return SimpleNamespace(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=asset_id, status=FindingStatus.open,
        resolved_at=None, resolution_method=None, resolution_run_id=None, reopened_count=0,
        cvss_score=None, risk_score=None, remediation=None, assigned_to=None, evidence={},
        title="Redis exposed", severity="critical")


def _db(asset=None):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: asset))
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.add = MagicMock()
    return db


async def _patch(finding, body, db=None):
    return await wf.patch_finding(db or _db(), finding, body, tenant_id=uuid.uuid4(),
                                  actor_id=uuid.uuid4(), actor_type="manager", origin="manager")


@pytest.mark.asyncio
async def test_accepting_without_owner_expiry_and_control_is_refused():
    finding = _finding()
    with pytest.raises(HTTPException) as exc:
        await _patch(finding, FindingPatch(status=FindingStatus.accepted, action_reason="ok"))
    assert exc.value.status_code == 422
    assert "risk_acceptance.risk_owner" in exc.value.detail["required"]
    assert finding.status == FindingStatus.open                      # nothing changed


@pytest.mark.asyncio
async def test_refusal_proposes_the_asset_owner():
    asset_id = uuid.uuid4()
    asset = SimpleNamespace(owner=None, tags={"team": "Platform SRE"})
    with pytest.raises(HTTPException) as exc:
        await _patch(_finding(asset_id), FindingPatch(status=FindingStatus.accepted), _db(asset))
    assert exc.value.detail["suggested_owner"] == "Platform SRE"


def test_owner_suggestion_prefers_the_asset_owner_then_tags():
    assert wf.suggest_risk_owner(SimpleNamespace(owner=" Dana ", tags={"team": "x"})) == "Dana"
    assert wf.suggest_risk_owner(SimpleNamespace(owner=None, tags={"owner": "Lee"})) == "Lee"
    assert wf.suggest_risk_owner(SimpleNamespace(owner=None, tags=None)) is None
    assert wf.suggest_risk_owner(None) is None


@pytest.mark.asyncio
async def test_expiry_in_the_past_is_refused():
    body = FindingPatch(status=FindingStatus.accepted, risk_acceptance={
        "risk_owner": "CISO", "expires_at": "2020-01-01T00:00:00+00:00",
        "compensating_controls": "Firewalled to the app subnet"})
    with pytest.raises(HTTPException) as exc:
        await _patch(_finding(), body)
    assert "future" in exc.value.detail


@pytest.mark.asyncio
async def test_complete_acceptance_is_recorded_on_the_event():
    finding = _finding()
    db = _db()
    body = FindingPatch(status=FindingStatus.accepted, action_reason="Business exception", risk_acceptance={
        "risk_owner": "CISO", "expires_at": FUTURE,
        "compensating_controls": "Firewalled to the app subnet"})
    await _patch(finding, body, db)
    assert finding.status == FindingStatus.accepted
    from app.models.finding_event import FindingEvent
    event = next(c.args[0] for c in db.add.call_args_list if isinstance(c.args[0], FindingEvent))
    assert event.detail["risk_owner"] == "CISO"
    assert event.detail["compensating_controls"] == "Firewalled to the app subnet"
    assert event.detail["expires_at"].startswith(FUTURE[:10])


def test_schema_rules():
    with pytest.raises(ValidationError):                              # naive datetime
        FindingPatch(status=FindingStatus.accepted, risk_acceptance={
            "risk_owner": "x", "expires_at": "2099-01-01T00:00:00", "compensating_controls": "abc"})
    with pytest.raises(ValidationError):                              # blank owner
        FindingPatch(status=FindingStatus.accepted, risk_acceptance={
            "risk_owner": "  ", "expires_at": FUTURE, "compensating_controls": "abc"})
    with pytest.raises(ValidationError):                              # only valid for accepted
        FindingPatch(status=FindingStatus.open, risk_acceptance={
            "risk_owner": "x", "expires_at": FUTURE, "compensating_controls": "abc"})


@pytest.mark.asyncio
async def test_other_transitions_are_unaffected():
    finding = _finding()
    await _patch(finding, FindingPatch(status=FindingStatus.confirmed, action_reason="valid"))
    assert finding.status == FindingStatus.confirmed
