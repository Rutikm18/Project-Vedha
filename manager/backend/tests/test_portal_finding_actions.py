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
    PortalEnrollmentApprove,
    patch_portal_finding,
    router as portal_router,
    portal_workspace_finding_summary,
    portal_workspace_findings,
    portal_workspace_engagement,
    portal_workspace_engagement_assets,
    portal_workspace_update_engagement,
    portal_workspace_scan_launch,
    portal_workspace_fleet_agent_jobs,
    portal_workspace_fleet_approve,
)
from app.routers.agents import EnqueueJobRequest
from app.schemas.auth import CurrentUser
from app.schemas.common import PaginatedResponse
from app.schemas.finding import FindingOut, FindingPatch


def _client(engagement_id: uuid.UUID) -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="client",
        client_engagement_id=engagement_id,
    )


def _finding(engagement_id: uuid.UUID):
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
        updated_at=datetime.now(timezone.utc),
    )


def test_workspace_list_serializes_through_the_manager_finding_contract():
    route = next(
        route for route in portal_router.routes
        if getattr(route, "path", None) == "/portal/workspace/findings"
    )
    assert route.response_model == PaginatedResponse[FindingOut]


@pytest.mark.asyncio
async def test_customer_transition_mutates_shared_row_and_records_origin():
    engagement_id = uuid.uuid4()
    finding = _finding(engagement_id)
    user = _client(engagement_id)
    added = []
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: finding))
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
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))

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
    list_findings = AsyncMock(return_value=object())
    finding_summary = AsyncMock(return_value=object())
    monkeypatch.setattr(finding_routes, "list_findings", list_findings)
    monkeypatch.setattr(finding_routes, "finding_summary", finding_summary)

    await portal_workspace_findings(user=user, db=db, agent_id=agent_id)
    await portal_workspace_finding_summary(user=user, db=db, agent_id=agent_id)

    assert list_findings.await_args.kwargs["engagement_id"] == engagement_id
    assert list_findings.await_args.kwargs["agent_id"] == agent_id
    assert finding_summary.await_args.kwargs == {
        "db": db,
        "current_user": user,
        "engagement_id": engagement_id,
        "agent_id": agent_id,
    }


@pytest.mark.asyncio
async def test_workspace_engagement_uses_session_binding(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    db = MagicMock()
    from app.routers import engagements as engagement_routes
    get_engagement = AsyncMock(return_value=object())
    monkeypatch.setattr(engagement_routes, "get_engagement", get_engagement)

    await portal_workspace_engagement(user=user, db=db)

    assert get_engagement.await_args.kwargs == {
        "engagement_id": engagement_id,
        "db": db,
        "current_user": user,
    }


@pytest.mark.asyncio
async def test_portal_engagement_update_pins_session_identity(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    db = MagicMock()
    db.flush = AsyncMock()
    db.add = MagicMock()
    from app.routers import engagements as engagement_routes
    updated = object()
    update_engagement = AsyncMock(return_value=updated)
    monkeypatch.setattr(engagement_routes, "update_engagement", update_engagement)

    result = await portal_workspace_update_engagement(
        body={"name": "Customer-updated name", "scope_cidrs": ["192.0.2.0/24"]},
        user=user,
        db=db,
    )

    assert result is updated
    assert update_engagement.await_args.kwargs["engagement_id"] == engagement_id
    assert update_engagement.await_args.kwargs["current_user"] is user
    assert update_engagement.await_args.kwargs["body"].scope_cidrs == ["192.0.2.0/24"]


@pytest.mark.asyncio
async def test_portal_assets_use_session_engagement(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    db = MagicMock()
    from app.routers import engagements as engagement_routes
    list_assets = AsyncMock(return_value=[])
    monkeypatch.setattr(engagement_routes, "list_engagement_assets", list_assets)

    await portal_workspace_engagement_assets(user=user, db=db)

    assert list_assets.await_args.kwargs == {
        "engagement_id": engagement_id,
        "db": db,
        "current_user": user,
    }


@pytest.mark.asyncio
async def test_portal_scan_launch_pins_session_engagement_and_assigned_probe(monkeypatch):
    engagement_id = uuid.uuid4()
    assigned_agent_id = uuid.uuid4()
    user = _client(engagement_id)
    engagement = SimpleNamespace(
        id=engagement_id,
        tenant_id=user.tenant_id,
        assigned_agent_id=assigned_agent_id,
    )
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: engagement))
    db.flush = AsyncMock()
    db.add = MagicMock()

    from app.routers import agents as agent_routes
    enqueue = AsyncMock(return_value={"job_id": str(uuid.uuid4()), "status": "pending"})
    monkeypatch.setattr(agent_routes, "enqueue_agent_job", enqueue)
    from app.services import entitlements
    monkeypatch.setattr(entitlements, "consume_scan", AsyncMock())

    body = EnqueueJobRequest(
        engagement_id=uuid.uuid4(),
        use_case_id="uc_network_va",
        params={"intensity": "normal"},
    )
    await portal_workspace_scan_launch(
        body=body, user=user, db=db, redis=MagicMock(),
    )

    pinned = enqueue.await_args.kwargs["body"]
    assert pinned.engagement_id == engagement_id
    assert pinned.params["preferred_agent_id"] == str(assigned_agent_id)


@pytest.mark.asyncio
async def test_portal_probe_history_is_filtered_by_engagement(monkeypatch):
    engagement_id = uuid.uuid4()
    assigned_agent_id = uuid.uuid4()
    user = _client(engagement_id)
    engagement = SimpleNamespace(id=engagement_id, assigned_agent_id=assigned_agent_id)
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: engagement))

    from app.routers import agents as agent_routes
    history = AsyncMock(return_value=[])
    monkeypatch.setattr(agent_routes, "get_agent_job_history", history)

    await portal_workspace_fleet_agent_jobs(
        agent_id=assigned_agent_id, user=user, db=db, limit=10,
    )

    assert history.await_args.kwargs["agent_id"] == assigned_agent_id
    assert history.await_args.kwargs["engagement_id"] == engagement_id


@pytest.mark.asyncio
async def test_portal_enrollment_binds_device_to_session_engagement_scope(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    engagement = SimpleNamespace(
        id=engagement_id,
        tenant_id=user.tenant_id,
        assigned_agent_id=None,
        scope_cidrs=["192.0.2.0/24"],
        excluded_cidrs=["192.0.2.128/25"],
    )
    request_row = SimpleNamespace(
        id=uuid.uuid4(),
        tenant_id=None,
        expires_at=datetime.now(timezone.utc).replace(year=2099),
        state="awaiting_approval",
        reported_capabilities=["network_va"],
    )
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: engagement),
        MagicMock(scalar_one_or_none=lambda: request_row),
    ])
    db.flush = AsyncMock()
    db.add = MagicMock()

    from app.routers import probe_enrollment
    monkeypatch.setattr(probe_enrollment, "_keyed_hash", lambda _value: "hash")
    provisioned = SimpleNamespace(id=uuid.uuid4())
    provision = AsyncMock(return_value=provisioned)
    monkeypatch.setattr(probe_enrollment, "_provision_agent_for_site", provision)

    result = await portal_workspace_fleet_approve(
        body=PortalEnrollmentApprove(user_code="ABCD-EFGH", probe_name="edge-agent"),
        user=user,
        db=db,
    )

    assert engagement.assigned_agent_id == provisioned.id
    assert result["agent_id"] == str(provisioned.id)
    site = provision.await_args.kwargs["site"]
    assert site.tenant_id == user.tenant_id
    assert site.authorized_cidrs == ["192.0.2.0/24"]
    assert site.excluded_cidrs == ["192.0.2.128/25"]
    assert provision.await_args.kwargs["probe_name"] == "edge-agent"


from app.routers.agents import _USE_CASE_CODES

_DEEP_SWEEP_UC = next(c for c, u in _USE_CASE_CODES.items() if u == "uc_deep_port_sweep")


def _launch_fixture(monkeypatch):
    engagement_id = uuid.uuid4()
    user = _client(engagement_id)
    engagement = SimpleNamespace(id=engagement_id, tenant_id=user.tenant_id,
                                 assigned_agent_id=uuid.uuid4())
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: engagement))
    db.flush = AsyncMock()
    db.add = MagicMock()
    from app.routers import agents as agent_routes
    enqueue = AsyncMock(return_value={"job_id": str(uuid.uuid4()), "status": "pending"})
    monkeypatch.setattr(agent_routes, "enqueue_agent_job", enqueue)
    from app.services import entitlements
    monkeypatch.setattr(entitlements, "consume_scan", AsyncMock())
    return user, db, enqueue


@pytest.mark.asyncio
@pytest.mark.parametrize("kwargs", [
    {"params": {"intensity": "aggressive"}},
    {"intensity": "deep"},
    {"intensity": 3},
    {"use_case_id": "uc_full_port_audit"},
    {"uc": _DEEP_SWEEP_UC},        # deep-only use case by numeric code
])
async def test_portal_scan_launch_refuses_aggressive(monkeypatch, kwargs):
    from fastapi import HTTPException
    user, db, enqueue = _launch_fixture(monkeypatch)
    body = EnqueueJobRequest(engagement_id=uuid.uuid4(), **kwargs)
    with pytest.raises(HTTPException) as e:
        await portal_workspace_scan_launch(body=body, user=user, db=db, redis=MagicMock())
    assert e.value.status_code == 403
    enqueue.assert_not_awaited()


@pytest.mark.asyncio
async def test_portal_scan_launch_strips_tuning_and_pins_a_safe_preset(monkeypatch):
    user, db, enqueue = _launch_fixture(monkeypatch)
    body = EnqueueJobRequest(
        engagement_id=uuid.uuid4(), use_case_id="uc_network_va",
        params={"intensity": "stealth", "rate": 9000, "concurrency": 2000,
                "allow_degraded_kernel": True},
        allow_fragile=True, fragile_override_reason="customer says it is fine really",
    )
    await portal_workspace_scan_launch(body=body, user=user, db=db, redis=MagicMock())
    pinned = enqueue.await_args.kwargs["body"]
    assert pinned.intensity == "light"
    assert "rate" not in pinned.params and "concurrency" not in pinned.params
    assert "allow_degraded_kernel" not in pinned.params
    assert pinned.allow_fragile is False


@pytest.mark.asyncio
async def test_portal_scan_launch_spends_quota_and_flags_the_job(monkeypatch):
    user, db, enqueue = _launch_fixture(monkeypatch)
    from app.services import entitlements
    consume = AsyncMock()
    monkeypatch.setattr(entitlements, "consume_scan", consume)
    body = EnqueueJobRequest(engagement_id=uuid.uuid4(), use_case_id="uc_network_va")
    await portal_workspace_scan_launch(body=body, user=user, db=db, redis=MagicMock())
    consume.assert_awaited_once()
    assert enqueue.await_args.kwargs["body"].params["_quota_consumed"] is True


@pytest.mark.asyncio
async def test_portal_scan_launch_refused_by_plan_enqueues_nothing(monkeypatch):
    from fastapi import HTTPException
    user, db, enqueue = _launch_fixture(monkeypatch)
    from app.services import entitlements
    monkeypatch.setattr(entitlements, "consume_scan",
                        AsyncMock(side_effect=HTTPException(403, "You've used all 5 scans")))
    body = EnqueueJobRequest(engagement_id=uuid.uuid4(), use_case_id="uc_network_va")
    with pytest.raises(HTTPException) as e:
        await portal_workspace_scan_launch(body=body, user=user, db=db, redis=MagicMock())
    assert e.value.status_code == 403
    enqueue.assert_not_awaited()
