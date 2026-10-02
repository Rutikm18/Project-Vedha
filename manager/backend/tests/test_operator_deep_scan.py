"""Operator Deep scan: one asset, every port, never charged to the customer's plan.

The operator Scanner launches the same single-asset Deep scan the portal offers
(uc_deep_port_sweep on one IP) through the operator enqueue, POST /agents/jobs.
Operators are unlimited: an operator deep scan must not consume — or later
refund — the customer's Deep allowance, and must not land in the customer's
"already deep-scanned" history.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.audit_log import AuditLog
from app.models.enums import ScanJobType
from app.routers import agents as ag
from app.services import entitlements


def _db():
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement=None, scope_cidrs=["10.0.0.0/8"],
                          excluded_cidrs=[])
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.commit = AsyncMock()
    return db


def _job(db):
    return next(c.args[0] for c in db.add.call_args_list if not isinstance(c.args[0], AuditLog))


def _operator_deep_body(ip: str = "10.0.0.5") -> ag.EnqueueJobRequest:
    # Exactly what buildScanLaunchRequest sends for the operator Deep scan card.
    return ag.EnqueueJobRequest(
        engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
        use_case_id="uc_deep_port_sweep",
        params={"targets": [ip], "scope_cidrs": [ip], "intensity": "aggressive"},
    )


@pytest.fixture
def no_fragile(monkeypatch):
    monkeypatch.setattr("app.services.fragile_guard.load_fragile_hosts", AsyncMock(return_value=[]))


@pytest.fixture
def entitlement_spy(monkeypatch):
    calls: list[tuple] = []

    async def consume(*args, **kwargs):
        calls.append(("consume", args, kwargs))

    async def give_back(*args, **kwargs):
        calls.append(("give_back", args, kwargs))

    monkeypatch.setattr(entitlements, "consume_scan", consume)
    monkeypatch.setattr(entitlements, "_give_back", give_back)
    return calls


@pytest.mark.asyncio
async def test_operator_deep_scan_runs_the_full_preset_on_one_asset(no_fragile, entitlement_spy):
    db = _db()
    await ag.enqueue_agent_job(_operator_deep_body("10.0.0.5"), db, AsyncMock(),
                               SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="tester"))
    params = _job(db).result
    assert params["uc"] == ag._USE_CASE_ID_TO_CODE["uc_deep_port_sweep"]      # 82
    assert params["intensity"] == ag._INTENSITY_NAME_TO_CODE["deep"]          # "aggressive" → deep
    assert params["targets"] == ["10.0.0.5"]


@pytest.mark.asyncio
async def test_operator_deep_scan_never_touches_the_customer_allowance(no_fragile, entitlement_spy):
    db = _db()
    await ag.enqueue_agent_job(_operator_deep_body(), db, AsyncMock(),
                               SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin"))
    job = _job(db)
    assert entitlement_spy == []                                  # nothing consumed
    for flag in (entitlements.JOB_QUOTA_FLAG, entitlements.JOB_QUOTA_MODE, entitlements.JOB_DEEP_TARGET):
        assert flag not in job.result                             # nothing to refund later

    # Cancelling or failing that job later must not "refund" a plan it never used.
    await entitlements.refund_for_job(db, job)
    assert entitlement_spy == []
