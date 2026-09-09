from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import ScanJobType
from app.routers import agents
from app.routers.agents import EnqueueJobRequest
from app.routers.portal import launch_portal_workspace_job
from app.schemas.auth import CurrentUser


def _client(engagement_id: uuid.UUID) -> CurrentUser:
    return CurrentUser(
        user_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        role="client",
        client_engagement_id=engagement_id,
    )


@pytest.mark.asyncio
async def test_launch_rejects_caller_supplied_other_engagement():
    user = _client(uuid.uuid4())
    body = EnqueueJobRequest(
        engagement_id=uuid.uuid4(),
        job_type=ScanJobType.discovery,
        use_case_id="uc_network_va",
    )

    with pytest.raises(HTTPException) as exc:
        await launch_portal_workspace_job(body, user, MagicMock(), MagicMock())

    assert exc.value.status_code == 403


@pytest.mark.asyncio
async def test_launch_is_pinned_to_assigned_probe_even_when_it_is_offline(monkeypatch):
    engagement_id = uuid.uuid4()
    assigned_agent_id = uuid.uuid4()
    user = _client(engagement_id)
    engagement = SimpleNamespace(
        id=engagement_id,
        tenant_id=user.tenant_id,
        assigned_agent_id=assigned_agent_id,
    )
    db_result = MagicMock(scalar_one_or_none=lambda: engagement)
    db = MagicMock()
    db.execute = AsyncMock(return_value=db_result)
    db.add = MagicMock()
    db.flush = AsyncMock()
    captured = {}

    async def fake_enqueue_agent_job_for_actor(
        *, body, db, redis, current_user, audit_origin, audit_actor_type
    ):
        captured["body"] = body
        captured["user"] = current_user
        captured["audit_origin"] = audit_origin
        captured["audit_actor_type"] = audit_actor_type
        return {
            "job_id": str(uuid.uuid4()),
            "status": "pending",
            "job_type": "discovery",
            "use_case_id": "uc_network_va",
        }

    monkeypatch.setattr(
        agents, "enqueue_agent_job_for_actor", fake_enqueue_agent_job_for_actor
    )
    body = EnqueueJobRequest(
        engagement_id=engagement_id,
        job_type=ScanJobType.discovery,
        use_case_id="uc_network_va",
        params={"intensity": "normal"},
    )

    result = await launch_portal_workspace_job(body, user, db, MagicMock())

    assert result["status"] == "pending"
    assert captured["user"] == user
    assert captured["body"].engagement_id == engagement_id
    assert captured["body"].params["preferred_agent_id"] == str(assigned_agent_id)
    assert captured["audit_origin"] == "portal"
    assert captured["audit_actor_type"] == "customer"
