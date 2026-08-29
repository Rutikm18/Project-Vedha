"""Fleet: tenant-wide job feed with probe + engagement name resolution and filters."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import agents as ag


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items))


@pytest.mark.asyncio
async def test_lists_jobs_with_probe_and_engagement_names():
    agent_id = uuid.uuid4()
    eng_id = uuid.uuid4()
    job = SimpleNamespace(
        id=uuid.uuid4(), agent_id=agent_id, engagement_id=eng_id,
        job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value="running"),
        result={"use_case_id": "uc_network_va"},
        created_at=None, started_at=None, completed_at=None)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        _scalars([job]),                                                # jobs
        _scalars([SimpleNamespace(id=agent_id, name="scanner-probe-01")]),  # agents
        MagicMock(all=lambda: [(eng_id, "Lab Engagement")]),           # engagements
    ])
    out = await ag.list_all_jobs(db, _user())
    assert len(out) == 1
    r = out[0]
    assert r["agent_name"] == "scanner-probe-01"
    assert r["engagement_name"] == "Lab Engagement"
    assert r["status"] == "running" and r["use_case_id"] == "uc_network_va"


@pytest.mark.asyncio
async def test_running_filter_is_accepted():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_scalars([])])   # no jobs → no name lookups
    out = await ag.list_all_jobs(db, _user(), running=True)
    assert out == []


@pytest.mark.asyncio
async def test_filter_by_probe_and_engagement_run_without_error():
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[_scalars([])])
    out = await ag.list_all_jobs(db, _user(), agent_id=uuid.uuid4(),
                                 engagement_id=uuid.uuid4())
    assert out == []
