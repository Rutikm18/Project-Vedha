"""
Unit tests for the agent/probe protocol changes:
  * agent polling is restricted to network-side job types,
  * the jobs response carries scan `params`,
  * the enqueue endpoint validates job type + engagement ownership.

DB and auth are mocked — these exercise the router logic directly.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.routers import agents as ag
from app.models.enums import ScanJobType


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


# ── AGENT_EXECUTABLE_TYPES guard ────────────────────────────────────────────────

class TestAgentExecutableTypes:

    def test_network_types_included(self):
        assert ScanJobType.discovery in ag.AGENT_EXECUTABLE_TYPES
        assert ScanJobType.lateral in ag.AGENT_EXECUTABLE_TYPES
        assert ScanJobType.cloud_scan in ag.AGENT_EXECUTABLE_TYPES

    def test_server_side_types_excluded(self):
        for t in (ScanJobType.vuln_scan, ScanJobType.ad_enum,
                  ScanJobType.detection, ScanJobType.ai_report):
            assert t not in ag.AGENT_EXECUTABLE_TYPES


# ── enqueue_agent_job ───────────────────────────────────────────────────────────

class TestEnqueueAgentJob:

    @pytest.mark.asyncio
    async def test_rejects_server_side_type(self):
        body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.vuln_scan)
        with pytest.raises(HTTPException) as ei:
            await ag.enqueue_agent_job(body, MagicMock(), _user())
        assert ei.value.status_code == 400

    @pytest.mark.asyncio
    async def test_404_when_engagement_missing(self):
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))
        body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery)
        with pytest.raises(HTTPException) as ei:
            await ag.enqueue_agent_job(body, db, _user())
        assert ei.value.status_code == 404

    @pytest.mark.asyncio
    async def test_success_creates_pending_job(self):
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(
            scalar_one_or_none=lambda: SimpleNamespace(
                id=uuid.uuid4(),
                rules_of_engagement=None,
                scope_cidrs=["10.0.0.0/8"],
            )))
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.commit = AsyncMock()
        body = ag.EnqueueJobRequest(
            engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
            params={"targets": ["10.0.1.0/24"], "ports": "1-1024"},
        )
        out = await ag.enqueue_agent_job(body, db, _user())
        assert out["job_type"] == "discovery"
        assert out["status"] == "pending"
        db.add.assert_called_once()
        created = db.add.call_args[0][0]
        assert created.result == {
            "targets": ["10.0.1.0/24"],
            "ports": "1-1024",
            "scan_type": "discovery",
            "scope_cidrs": ["10.0.0.0/8"],
            "_scope_cidrs": ["10.0.0.0/8"],
        }
        db.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_materializes_direct_job_capability_for_probe(self):
        engagement = SimpleNamespace(
            id=uuid.uuid4(),
            rules_of_engagement=None,
            scope_cidrs=["10.0.0.0/8"],
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(
            scalar_one_or_none=lambda: engagement,
        ))
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.commit = AsyncMock()

        await ag.enqueue_agent_job(
            ag.EnqueueJobRequest(
                engagement_id=engagement.id,
                job_type=ScanJobType.lateral,
            ),
            db,
            _user(),
        )

        created = db.add.call_args.args[0]
        assert created.result["scan_type"] == "smb_enum"

    @pytest.mark.asyncio
    async def test_scope_fields_cannot_override_engagement_scope(self):
        engagement = SimpleNamespace(
            id=uuid.uuid4(),
            rules_of_engagement=None,
            scope_cidrs=["10.0.0.0/24"],
            excluded_cidrs=["10.0.0.250/32"],
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(
            scalar_one_or_none=lambda: engagement,
        ))
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.commit = AsyncMock()

        await ag.enqueue_agent_job(
            ag.EnqueueJobRequest(
                engagement_id=engagement.id,
                params={
                    "scope_cidrs": ["192.0.2.0/24"],
                    "_scope_cidrs": ["192.0.2.0/24"],
                    "_excluded_cidrs": [],
                },
            ),
            db,
            _user(),
        )

        created = db.add.call_args.args[0]
        assert created.result["scope_cidrs"] == ["10.0.0.0/24"]
        assert created.result["_scope_cidrs"] == ["10.0.0.0/24"]
        assert created.result["_excluded_cidrs"] == ["10.0.0.250/32"]


# ── OT profile hard gate ────────────────────────────────────────────────────────
# Mirrors pipeline.py's structural OT block in the Agentic VA Scanner project:
# an unsolicited active probe to a PLC/RTU/safety controller can hang or
# reboot fragile control hardware, so "ot" must be a hard gate at job-creation
# time, not a default an operator can quietly override per job.

class TestOTProfileGate:

    @pytest.mark.asyncio
    async def test_blocks_active_scan_type_on_ot_engagement(self):
        eng = SimpleNamespace(
            id=uuid.uuid4(),
            rules_of_engagement={"scan_profile": "ot"},
            scope_cidrs=["10.0.0.0/8"],
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
        body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery)
        with pytest.raises(HTTPException) as ei:
            await ag.enqueue_agent_job(body, db, _user())
        assert ei.value.status_code == 400
        assert "ot" in ei.value.detail.lower()

    @pytest.mark.asyncio
    async def test_blocks_explicit_active_scan_type_override_on_ot_engagement(self):
        # Even an explicit params.scan_type override can't escape the gate —
        # it must check the RESOLVED scan_type, not just the coarse job_type.
        eng = SimpleNamespace(
            id=uuid.uuid4(),
            rules_of_engagement={"scan_profile": "ot"},
            scope_cidrs=["10.0.0.0/8"],
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
        body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                                    params={"scan_type": "tls_scan"})
        with pytest.raises(HTTPException) as ei:
            await ag.enqueue_agent_job(body, db, _user())
        assert ei.value.status_code == 400

    @pytest.mark.asyncio
    async def test_allows_passive_discovery_on_ot_engagement(self):
        eng = SimpleNamespace(
            id=uuid.uuid4(),
            rules_of_engagement={"scan_profile": "ot"},
            scope_cidrs=["10.0.0.0/8"],
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
        db.add = MagicMock(); db.flush = AsyncMock(); db.refresh = AsyncMock()
        db.commit = AsyncMock()
        body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                                    params={"scan_type": "passive_discovery"})
        out = await ag.enqueue_agent_job(body, db, _user())
        assert out["status"] == "pending"

    @pytest.mark.asyncio
    async def test_it_and_iot_profiles_unaffected(self):
        for profile in ("it", "iot", None):
            roe = {"scan_profile": profile} if profile else None
            eng = SimpleNamespace(
                id=uuid.uuid4(),
                rules_of_engagement=roe,
                scope_cidrs=["10.0.0.0/8"],
            )
            db = MagicMock()
            db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
            db.add = MagicMock(); db.flush = AsyncMock(); db.refresh = AsyncMock()
            db.commit = AsyncMock()
            body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery)
            out = await ag.enqueue_agent_job(body, db, _user())
            assert out["status"] == "pending"


class TestAgentRegistrationRefresh:

    @pytest.mark.asyncio
    async def test_agent_can_refresh_only_its_own_routing_metadata(self):
        agent_id = uuid.uuid4()
        agent = SimpleNamespace(
            id=agent_id,
            capabilities=["discovery"],
            network_segments=[],
            public_key=None,
            status=ag.AgentStatus.offline,
            last_heartbeat=None,
        )
        request = SimpleNamespace(state=SimpleNamespace(user_id=str(agent_id)))
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(
            scalar_one_or_none=lambda: agent,
        ))
        db.flush = AsyncMock()

        out = await ag.refresh_agent_registration(
            agent_id,
            ag.AgentRefreshRequest(
                capabilities=["discovery", "web_tls_scan"],
                network_segments=["10.0.0.0/24"],
                public_key="new-public-key",
            ),
            db,
            request,
        )

        assert out == {"ok": True}
        assert agent.capabilities == ["discovery", "web_tls_scan"]
        assert agent.network_segments == ["10.0.0.0/24"]
        assert agent.public_key == "new-public-key"
        assert agent.status == ag.AgentStatus.online
        db.flush.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_agent_cannot_refresh_another_identity(self):
        agent_id = uuid.uuid4()
        request = SimpleNamespace(
            state=SimpleNamespace(user_id=str(uuid.uuid4())),
        )
        db = MagicMock()

        with pytest.raises(HTTPException) as exc:
            await ag.refresh_agent_registration(
                agent_id,
                ag.AgentRefreshRequest(capabilities=["discovery"]),
                db,
                request,
            )

        assert exc.value.status_code == 403
        db.execute.assert_not_called()


# ── get_agent_jobs returns params ──────────────────────────────────────────────

class TestGetAgentJobs:

    @pytest.mark.asyncio
    async def test_jobs_include_params(self):
        tenant_id = uuid.uuid4()
        agent = SimpleNamespace(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            capabilities=["discovery"],
            network_segments=["10.0.0.0/16"],
        )
        engagement = SimpleNamespace(
            tenant_id=tenant_id,
            scope_cidrs=["10.0.0.0/24"],
        )
        job = SimpleNamespace(
            id=uuid.uuid4(), engagement_id=uuid.uuid4(),
            job_type=SimpleNamespace(value="discovery"),
            status=SimpleNamespace(value="pending"),
            result={"targets": ["10.0.0.0/24"]},
            agent_id=None, started_at=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(all=lambda: [(job, engagement)]),
            MagicMock(first=lambda: (1, 1)),
        ])
        db.flush = AsyncMock()

        out = await ag.get_agent_jobs(agent.id, db, limit=1)
        assert len(out) == 1
        assert out[0]["params"] == {"targets": ["10.0.0.0/24"]}
        assert out[0]["job_type"] == "discovery"
        assert out[0]["status"] == "running"
        assert out[0]["attempt_number"] == 1
        assert out[0]["fence"] == 1
        assert uuid.UUID(out[0]["attempt_id"])
        db.add.assert_called_once()
        db.flush.assert_awaited_once()

        candidate_query = db.execute.await_args_list[1].args[0]
        claim_query = db.execute.await_args_list[2].args[0]
        assert "engagements.tenant_id" in str(candidate_query)
        assert "engagements.tenant_id" in str(claim_query)

    @pytest.mark.asyncio
    async def test_skips_job_when_capability_is_missing(self):
        tenant_id = uuid.uuid4()
        agent = SimpleNamespace(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            capabilities=["tls_scan"],
            network_segments=[],
        )
        engagement = SimpleNamespace(
            tenant_id=tenant_id,
            scope_cidrs=["10.0.0.0/24"],
        )
        job = SimpleNamespace(
            id=uuid.uuid4(),
            engagement_id=uuid.uuid4(),
            job_type=ScanJobType.discovery,
            status=SimpleNamespace(value="pending"),
            result={},
            agent_id=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(all=lambda: [(job, engagement)]),
        ])

        assert await ag.get_agent_jobs(agent.id, db, limit=1) == []
        assert db.execute.await_count == 2

    @pytest.mark.asyncio
    async def test_skips_job_outside_declared_network_segments(self):
        tenant_id = uuid.uuid4()
        agent = SimpleNamespace(
            id=uuid.uuid4(),
            tenant_id=tenant_id,
            capabilities=["discovery"],
            network_segments=["10.20.0.0/16"],
        )
        engagement = SimpleNamespace(
            tenant_id=tenant_id,
            scope_cidrs=["10.30.0.0/24"],
        )
        job = SimpleNamespace(
            id=uuid.uuid4(),
            engagement_id=uuid.uuid4(),
            job_type=ScanJobType.discovery,
            status=SimpleNamespace(value="pending"),
            result={},
            agent_id=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: agent),
            MagicMock(all=lambda: [(job, engagement)]),
        ])

        assert await ag.get_agent_jobs(agent.id, db, limit=1) == []
        assert db.execute.await_count == 2

    @pytest.mark.asyncio
    async def test_404_when_agent_unknown(self):
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))
        with pytest.raises(HTTPException) as ei:
            await ag.get_agent_jobs(uuid.uuid4(), db, limit=1)
        assert ei.value.status_code == 404


class TestAgentJobCompatibility:

    def test_use_case_resolves_to_required_capability(self):
        assert ag._required_scan_type(
            ScanJobType.discovery,
            {"use_case_id": "uc_windows_estate"},
        ) == "smb_enum"

    def test_declared_segment_must_cover_entire_scope(self):
        assert ag._scope_is_reachable(
            ["10.0.0.0/16"],
            ["10.0.1.0/24", "10.0.2.5/32"],
        )
        assert not ag._scope_is_reachable(
            ["10.0.1.0/24"],
            ["10.0.0.0/16"],
        )

    def test_declared_segment_rejects_missing_or_invalid_scope(self):
        assert not ag._scope_is_reachable(["10.0.0.0/8"], [])
        assert not ag._scope_is_reachable(
            ["not-a-network"],
            ["10.0.0.0/24"],
        )

    def test_empty_segments_are_fail_closed(self):
        assert not ag._scope_is_reachable([], ["203.0.113.0/24"])

    def test_empty_capabilities_receive_no_jobs(self):
        agent = SimpleNamespace(capabilities=[], network_segments=[])
        assert not ag._agent_can_execute_job(
            agent,
            ScanJobType.discovery,
            {},
            ["10.0.0.0/24"],
        )

    def test_requested_subset_routes_to_a_subset_probe(self):
        agent = SimpleNamespace(
            capabilities=["discovery"],
            network_segments=["10.0.8.0/24"],
        )
        assert ag._agent_can_execute_job(
            agent,
            ScanJobType.discovery,
            {"targets": ["10.0.8.0/24"]},
            ["10.0.0.0/16"],
        )
        assert not ag._agent_can_execute_job(
            agent,
            ScanJobType.discovery,
            {},
            ["10.0.0.0/16"],
        )

    def test_explicit_out_of_scope_target_is_never_dispatched(self):
        agent = SimpleNamespace(
            capabilities=["discovery"],
            network_segments=[],
        )

    @pytest.mark.parametrize("authoritative_scope", [None, []])
    def test_missing_authoritative_scope_never_uses_job_targets_as_authority(
        self, authoritative_scope,
    ):
        agent = SimpleNamespace(
            capabilities=["discovery"],
            network_segments=["0.0.0.0/0"],
        )

        assert ag._job_reachability_scope(
            {"targets": ["192.0.2.10"]},
            authoritative_scope,
        ) is None
        assert not ag._agent_can_execute_job(
            agent,
            ScanJobType.discovery,
            {"targets": ["192.0.2.10"]},
            authoritative_scope,
        )
        assert not ag._agent_can_execute_job(
            agent,
            ScanJobType.discovery,
            {"target": "192.0.2.10"},
            ["10.0.0.0/8"],
        )

    def test_requested_ip_range_uses_only_its_covered_networks(self):
        assert ag._job_reachability_scope(
            {"targets": ["10.0.8.10-10.0.8.20"]},
            ["10.0.0.0/16"],
        ) == [
            "10.0.8.10/31",
            "10.0.8.12/30",
            "10.0.8.16/30",
            "10.0.8.20/32",
        ]

    def test_hostname_and_explicit_empty_targets_are_not_routable(self):
        assert ag._job_reachability_scope(
            {"targets": ["host.example.com"]},
            ["10.0.0.0/8"],
        ) is None
        assert ag._job_reachability_scope(
            {"targets": []},
            ["10.0.0.0/8"],
        ) is None

    def test_agent_network_segments_are_normalized_and_validated(self):
        request = ag.AgentRegisterRequest(
            name="probe-1",
            network_segments=["10.0.0.1/24", "10.0.0.0/24"],
        )
        assert request.network_segments == ["10.0.0.0/24"]

        with pytest.raises(ValueError, match="invalid probe network CIDR"):
            ag.AgentRefreshRequest(network_segments=["not-a-network"])


# ── list_agents (dashboard) ─────────────────────────────────────────────────────

class TestListAgents:

    @pytest.mark.asyncio
    async def test_lists_with_online_flag(self):
        from datetime import datetime, timezone, timedelta
        fresh = SimpleNamespace(
            id=uuid.uuid4(), name="dmz-probe", location="DMZ",
            status=SimpleNamespace(value="online"), capabilities=["discovery"],
            network_segments=["10.0.1.0/24"], last_heartbeat=datetime.now(timezone.utc),
            current_job_id=None,
        )
        stale = SimpleNamespace(
            id=uuid.uuid4(), name="old-probe", location=None,
            status=SimpleNamespace(value="offline"), capabilities=[],
            network_segments=[], last_heartbeat=datetime.now(timezone.utc) - timedelta(minutes=10),
            current_job_id=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalars=lambda: MagicMock(all=lambda: [fresh, stale])))
        out = await ag.list_agents(db, _user())
        assert out[0]["online"] is True
        assert out[1]["online"] is False
        assert out[0]["capabilities"] == ["discovery"]

    @pytest.mark.asyncio
    async def test_fresh_disconnected_agent_is_not_reported_online(self):
        from datetime import datetime, timezone
        disconnected = SimpleNamespace(
            id=uuid.uuid4(), name="just-disconnected", location=None,
            status=SimpleNamespace(value="offline"), capabilities=[],
            network_segments=[], last_heartbeat=datetime.now(timezone.utc),
            current_job_id=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(
            return_value=MagicMock(
                scalars=lambda: MagicMock(all=lambda: [disconnected])
            )
        )

        out = await ag.list_agents(db, _user())

        assert out[0]["status"] == "offline"
        assert out[0]["online"] is False


# ── heartbeat lifecycle ─────────────────────────────────────────────────────────

class TestHeartbeat:

    @pytest.mark.asyncio
    async def test_online_heartbeat_clears_completed_job(self):
        agent_id = uuid.uuid4()
        agent = SimpleNamespace(
            id=agent_id,
            status=ag.AgentStatus.busy,
            current_job_id=uuid.uuid4(),
            last_heartbeat=None,
        )
        db = MagicMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: agent)
        )
        db.flush = AsyncMock()
        request = SimpleNamespace(state=SimpleNamespace(user_id=str(agent_id)))

        out = await ag.heartbeat(
            ag.HeartbeatRequest(
                agent_id=str(agent_id),
                status="online",
                current_job_id=None,
            ),
            db,
            request,
        )

        assert out == {"ok": True, "lease_valid": True}
        assert agent.status is ag.AgentStatus.online
        assert agent.current_job_id is None
        db.flush.assert_awaited_once()


# ── legacy bootstrap containment ────────────────────────────────────────────────

class TestLegacyBootstrap:

    @pytest.mark.asyncio
    async def test_shared_secret_bootstrap_is_disabled_by_default(self, monkeypatch):
        monkeypatch.setattr(
            ag,
            "get_settings",
            lambda: SimpleNamespace(
                allow_unsafe_legacy_probe_bootstrap=False,
                probe_bootstrap_key="configured-but-must-not-enable-route",
            ),
        )

        with pytest.raises(HTTPException) as exc:
            await ag.bootstrap_agent(
                ag.AgentBootstrapRequest(
                    bootstrap_key="configured-but-must-not-enable-route",
                    name="probe-1",
                ),
                MagicMock(),
            )

        assert exc.value.status_code == 410


# ── register_agent: idempotency + long-lived token (regression for the 115-dup bug) ──

class TestRegisterAgent:

    @pytest.mark.asyncio
    async def test_reuses_existing_probe_by_name(self):
        """Re-registering the same-named probe must reuse the row, not create a dup."""
        from datetime import datetime, timezone
        existing = SimpleNamespace(
            id=uuid.uuid4(), name="dmz-probe-01", location=None,
            capabilities=[], network_segments=[], status=None,
            last_heartbeat=datetime.now(timezone.utc),
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: existing))
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        body = ag.AgentRegisterRequest(name="dmz-probe-01", capabilities=["discovery"],
                                       network_segments=["10.0.1.0/24"])
        out = await ag.register_agent(body, db, _user())

        db.add.assert_not_called()                       # no duplicate row created
        assert out.agent_id == str(existing.id)          # same identity returned
        assert existing.capabilities == ["discovery"]    # fields refreshed
        assert existing.status == ag.AgentStatus.online

    @pytest.mark.asyncio
    async def test_creates_when_none_exists(self):
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: None))
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        body = ag.AgentRegisterRequest(name="new-probe", capabilities=["discovery"])
        out = await ag.register_agent(body, db, _user())
        db.add.assert_called_once()                      # a fresh agent row
        assert out.token                                 # token issued

    @pytest.mark.asyncio
    async def test_agent_token_is_long_lived(self):
        """Agent token must outlive the 15-min access default so it doesn't churn."""
        import jwt as pyjwt
        from datetime import datetime, timezone
        existing = SimpleNamespace(
            id=uuid.uuid4(), name="p", location=None, capabilities=[],
            network_segments=[], status=None,
            last_heartbeat=datetime.now(timezone.utc),
        )
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: existing))
        db.flush = AsyncMock(); db.refresh = AsyncMock(); db.add = MagicMock()
        out = await ag.register_agent(ag.AgentRegisterRequest(name="p"), db, _user())
        payload = pyjwt.decode(out.token, options={"verify_signature": False})
        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        assert (exp - datetime.now(timezone.utc)).days > 300   # ~1 year, not 15 min


class TestPromoteAssets:
    """Discovery results → assets/services promotion (makes the Attack Surface populate)."""

    @pytest.mark.asyncio
    async def test_creates_asset_and_services_with_cpe(self):
        eng = uuid.uuid4()
        result = {"hosts": [
            {"ip": "10.0.0.5", "hostname": "web01", "os": "Linux",
             "ports": [{"port": 443, "protocol": "tcp", "service": "https",
                        "product": "nginx", "version": "1.25",
                        "cpe": ["cpe:/a:nginx:nginx:1.25"]}]},
            {"ip": None, "ports": []},  # malformed host → skipped
        ]}
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: None),   # asset lookup → new
            MagicMock(scalar_one_or_none=lambda: None),   # service lookup → new
        ])
        db.add = MagicMock(); db.flush = AsyncMock()

        promoted = await ag._promote_assets(db, eng, result)
        assert promoted == 1
        added = [c.args[0] for c in db.add.call_args_list]
        assert any(isinstance(a, ag.Asset) and a.ip_address == "10.0.0.5" for a in added)
        svc = next(s for s in added if isinstance(s, ag.Service))
        assert svc.port == 443 and svc.cpe == "cpe:/a:nginx:nginx:1.25"   # list → joined string

    @pytest.mark.asyncio
    async def test_dedupes_duplicate_services_in_same_probe_result(self):
        """A single web scan can emit multiple facts for the same host:port."""
        eng = uuid.uuid4()
        result = {"hosts": [
            {"ip": "10.0.0.5", "hostname": "api", "ports": [
                {"port": 8000, "protocol": "tcp", "service": "HTTP/1.1 307 Temporary Redirect"},
                {"port": 8000, "protocol": "tcp", "service": "http"},
            ]},
        ]}
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: None),   # asset lookup → new
            MagicMock(scalar_one_or_none=lambda: None),   # service lookup → new
        ])
        db.add = MagicMock()
        db.flush = AsyncMock()

        promoted = await ag._promote_assets(db, eng, result)

        assert promoted == 1
        services = [c.args[0] for c in db.add.call_args_list if isinstance(c.args[0], ag.Service)]
        assert len(services) == 1
        assert services[0].port == 8000
        assert services[0].service_name == "http"

    @pytest.mark.asyncio
    async def test_skips_host_without_ip(self):
        db = MagicMock(); db.execute = AsyncMock(); db.add = MagicMock(); db.flush = AsyncMock()
        promoted = await ag._promote_assets(db, uuid.uuid4(), {"hosts": [{"ip": None}]})
        assert promoted == 0
        db.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_empty_result_is_noop(self):
        db = MagicMock(); db.execute = AsyncMock(); db.add = MagicMock(); db.flush = AsyncMock()
        assert await ag._promote_assets(db, uuid.uuid4(), {}) == 0


class TestAccessTokenExpiry:

    def test_custom_expiry_overrides_default(self):
        import jwt as pyjwt
        from datetime import datetime, timezone
        from app.auth import jwt as jwtmod
        long = pyjwt.decode(
            jwtmod.create_access_token("s", "t", "agent", expires_minutes=60 * 24 * 365),
            options={"verify_signature": False})
        short = pyjwt.decode(
            jwtmod.create_access_token("s", "t", "user"),
            options={"verify_signature": False})
        now = datetime.now(timezone.utc)
        assert (datetime.fromtimestamp(long["exp"], tz=timezone.utc) - now).days > 300
        assert (datetime.fromtimestamp(short["exp"], tz=timezone.utc) - now).total_seconds() < 3600
