from __future__ import annotations

import importlib.util
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import ScanJobStatus, ScanJobType
from app.routers import agent_ws
from app.websocket.manager import AgentConnectionManager


class TestUseCaseCatalogParity:

    def test_manager_and_probe_route_use_cases_identically(self):
        probe_use_cases_path = (
            Path(__file__).resolve().parents[3]
            / "probe"
            / "agent"
            / "use_cases.py"
        )
        spec = importlib.util.spec_from_file_location(
            "_probe_use_cases_for_contract_test",
            probe_use_cases_path,
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        from app.routers.agents import _USE_CASES

        assert set(_USE_CASES) == set(module.USE_CASES)
        for use_case_id, manager_entry in _USE_CASES.items():
            probe_entry = module.USE_CASES[use_case_id]
            assert manager_entry["scan_type"] == probe_entry["scan_type"]
            assert manager_entry["profile"] == probe_entry["profile"]

        assert _USE_CASES["uc_external_web_triage"]["scan_type"] == "web_tls_scan"


class TestTenantWebSocketSelection:

    @pytest.mark.asyncio
    async def test_displaced_socket_cannot_unregister_reconnect(self):
        manager = AgentConnectionManager()
        tenant_id = str(uuid.uuid4())
        agent_id = str(uuid.uuid4())
        old_ws = AsyncMock()
        new_ws = AsyncMock()

        await manager.register(agent_id, tenant_id, old_ws)
        await manager.register(agent_id, tenant_id, new_ws)

        old_ws.close.assert_awaited_once()
        assert await manager.unregister(agent_id, old_ws) is False
        assert manager.is_connected(agent_id) is True

        await manager.record_features(agent_id, ["atomic_job_claim_v1"])
        pushed = await manager.push_job(
            agent_id,
            {"job_id": str(uuid.uuid4())},
            required_feature="atomic_job_claim_v1",
        )

        assert pushed is True
        new_ws.send_json.assert_awaited_once()
        assert await manager.unregister(agent_id, new_ws) is True
        assert manager.is_connected(agent_id) is False

    @pytest.mark.asyncio
    async def test_only_returns_online_agents_in_requested_tenant(self):
        manager = AgentConnectionManager()
        tenant_a = str(uuid.uuid4())
        tenant_b = str(uuid.uuid4())
        agent_a = str(uuid.uuid4())
        agent_b = str(uuid.uuid4())
        ws_a = AsyncMock()
        ws_b = AsyncMock()

        await manager.register(agent_a, tenant_a, ws_a)
        await manager.register(agent_b, tenant_b, ws_b)

        assert manager.online_agents_for_tenant(tenant_a) == [agent_a]
        assert manager.online_agents_for_tenant(tenant_b) == [agent_b]
        assert manager.online_agents_for_tenant(str(uuid.uuid4())) == []
        assert manager.online_agents_for_tenant(
            tenant_a,
            required_feature="atomic_job_claim_v1",
        ) == []

        await manager.record_features(agent_a, ["atomic_job_claim_v1"])
        assert manager.online_agents_for_tenant(
            tenant_a,
            required_feature="atomic_job_claim_v1",
        ) == [agent_a]

    @pytest.mark.asyncio
    async def test_first_online_push_cannot_cross_tenants(self):
        manager = AgentConnectionManager()
        tenant_a = str(uuid.uuid4())
        tenant_b = str(uuid.uuid4())
        agent_a = str(uuid.uuid4())
        agent_b = str(uuid.uuid4())
        ws_a = AsyncMock()
        ws_b = AsyncMock()

        await manager.register(agent_a, tenant_a, ws_a)
        await manager.register(agent_b, tenant_b, ws_b)

        assert await manager.push_job_to_first_online(
            {"job_id": str(uuid.uuid4())},
            tenant_b,
            required_feature="atomic_job_claim_v1",
        ) is None

        await manager.record_features(agent_b, ["atomic_job_claim_v1"])
        selected = await manager.push_job_to_first_online(
            {"job_id": str(uuid.uuid4())},
            tenant_b,
            required_feature="atomic_job_claim_v1",
        )

        assert selected == agent_b
        ws_a.send_json.assert_not_awaited()
        ws_b.send_json.assert_awaited_once()


def _claim_fixture(*, capabilities=None, network_segments=None):
    tenant_id = uuid.uuid4()
    agent_id = uuid.uuid4()
    job_id = uuid.uuid4()
    agent = SimpleNamespace(
        id=agent_id,
        tenant_id=tenant_id,
        capabilities=capabilities or ["discovery"],
        network_segments=network_segments or ["10.0.0.0/16"],
    )
    job = SimpleNamespace(
        id=job_id,
        engagement_id=uuid.uuid4(),
        status=ScanJobStatus.pending,
        agent_id=None,
        job_type=ScanJobType.discovery,
        result={},
    )
    engagement = SimpleNamespace(
        tenant_id=tenant_id,
        scope_cidrs=["10.0.1.0/24"],
    )
    return tenant_id, agent_id, job_id, agent, job, engagement


class TestAtomicWebSocketClaim:

    @pytest.mark.asyncio
    async def test_claim_commits_before_confirmation(self):
        tenant_id, agent_id, job_id, agent, job, engagement = _claim_fixture()
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(one_or_none=lambda: (job, engagement)),
            SimpleNamespace(rowcount=1),
        ])
        db.commit = AsyncMock()

        claimed, reason = await agent_ws._claim_pushed_job(
            db,
            str(agent_id),
            str(tenant_id),
            job_id,
        )

        assert claimed is True
        assert reason == "claimed"
        db.commit.assert_awaited_once()
        assert "agents.tenant_id" in str(db.execute.await_args_list[0].args[0])
        assert "engagements.tenant_id" in str(db.execute.await_args_list[1].args[0])
        assert "engagements.tenant_id" in str(db.execute.await_args_list[2].args[0])

    @pytest.mark.asyncio
    async def test_incompatible_capability_is_never_claimed(self):
        fixture = _claim_fixture(capabilities=["tls_scan"])
        tenant_id, agent_id, job_id, agent, job, engagement = fixture
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(one_or_none=lambda: (job, engagement)),
        ])
        db.commit = AsyncMock()

        claimed, reason = await agent_ws._claim_pushed_job(
            db,
            str(agent_id),
            str(tenant_id),
            job_id,
        )

        assert claimed is False
        assert reason == "not_eligible"
        assert db.execute.await_count == 2
        db.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_lost_atomic_update_is_reported_as_unclaimed(self):
        tenant_id, agent_id, job_id, agent, job, engagement = _claim_fixture()
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(one_or_none=lambda: (job, engagement)),
            SimpleNamespace(rowcount=0),
        ])
        db.commit = AsyncMock()

        claimed, reason = await agent_ws._claim_pushed_job(
            db,
            str(agent_id),
            str(tenant_id),
            job_id,
        )

        assert claimed is False
        assert reason == "claim_lost"
        db.commit.assert_awaited_once()
