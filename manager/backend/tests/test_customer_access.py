"""
test_customer_access.py — Phase 1: operator provisioning + scan-request inbox.
Handlers are called directly with a mocked async db (repo convention), so no live
database is needed.
"""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import ScanJobType, UserRole
from app.models.scan_job import ScanJob
from app.models.user import User
from app.routers import customer_access as ca
from app.schemas.auth import CurrentUser


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _mock_db(scalar_returns: list):
    """db.execute yields the given scalar_one_or_none values in order."""
    db = MagicMock()
    results = []
    for v in scalar_returns:
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=v)
        r.first = MagicMock(return_value=v)   # also drives .first()-based queries
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    db.add = MagicMock()
    db.flush = AsyncMock()

    async def _refresh(obj):
        if getattr(obj, "id", None) is None:
            obj.id = uuid.uuid4()

    db.refresh = _refresh
    return db


def _added(db, cls):
    for call in db.add.call_args_list:
        obj = call.args[0]
        if isinstance(obj, cls):
            return obj
    return None


# ── build_scan_job (pure) ─────────────────────────────────────────────────────

class TestBuildScanJob:
    def test_preferred_agent_in_params_not_db_column(self):
        # RC-FIX-2: agent_id must NOT be pre-assigned on the DB column — that blocks
        # the HTTP poll query (agent_id IS NULL filter). Instead it lives in params.
        agent = uuid.uuid4()
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=agent, scope_cidrs=["10.0.0.0/24"])
        sr = SimpleNamespace(id=uuid.uuid4(), scan_type="discovery", requested_by=uuid.uuid4())
        job = ca.build_scan_job(sr, eng)
        assert job.agent_id is None, "agent_id on the ScanJob row must stay NULL for HTTP poll"
        assert job.result["preferred_agent_id"] == str(agent)
        assert job.job_type == ScanJobType.discovery
        assert job.engagement_id == eng.id
        assert job.result["scan_request_id"] == str(sr.id)
        assert job.result["scope_cidrs"] == ["10.0.0.0/24"]

    def test_use_case_scan_type_falls_back_to_discovery_not_vuln_scan(self):
        # RC-FIX-1: use-case scan types (deep_port_sweep, full_port_audit, …) are NOT
        # ScanJobType enum values. The old fallback to vuln_scan excluded the job from
        # AGENT_EXECUTABLE_TYPES so no probe could ever claim it. discovery is correct.
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        for scan_type in ("deep_port_sweep", "full_port_audit", "bogus_use_case"):
            sr = SimpleNamespace(id=uuid.uuid4(), scan_type=scan_type, requested_by=None)
            job = ca.build_scan_job(sr, eng)
            assert job.job_type == ScanJobType.discovery, (
                f"scan_type='{scan_type}' fell back to {job.job_type.value!r}, "
                f"expected 'discovery' (vuln_scan is not agent-executable)"
            )

    def test_server_side_scan_type_remapped_to_discovery(self):
        # RC-FIX-4 (manager-level stuck): scan types that ARE valid ScanJobType enum
        # values but are server-side only (vuln_scan, detection, ai_report …) are
        # excluded from AGENT_EXECUTABLE_TYPES. A probe's HTTP poll query requires
        # job_type IN AGENT_EXECUTABLE_TYPES — so a job built with job_type=vuln_scan
        # is permanently invisible to every probe. The hard guard remaps them to
        # discovery so the job is always claimable. This was the primary reason jobs
        # got stuck "at manager level" — the ScanJob was created but never dispatched.
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        for server_side_type in ("vuln_scan", "detection", "ai_report", "exploit", "ad_enum"):
            sr = SimpleNamespace(id=uuid.uuid4(), scan_type=server_side_type, requested_by=None)
            job = ca.build_scan_job(sr, eng)
            assert job.job_type == ScanJobType.discovery, (
                f"scan_type='{server_side_type}' produced job_type={job.job_type.value!r}; "
                f"server-side types must be remapped to discovery so the probe can claim the job"
            )

    def test_quota_spend_moves_from_request_to_job(self):
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        sr = SimpleNamespace(id=uuid.uuid4(), scan_type="vuln_scan", requested_by=None,
                             quota_consumed=True)
        assert ca.build_scan_job(sr, eng).result["_quota_consumed"] is True
        sr.quota_consumed = False
        assert "_quota_consumed" not in ca.build_scan_job(sr, eng).result

    def test_no_assigned_agent_raises(self):
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=None, scope_cidrs=[])
        sr = SimpleNamespace(id=uuid.uuid4(), scan_type="vuln_scan", requested_by=None)
        with pytest.raises(ValueError):
            ca.build_scan_job(sr, eng)


def test_generate_password_is_unique_and_nonempty():
    a, b = ca.generate_password(), ca.generate_password()
    assert a and b and a != b


# ── provisioning ──────────────────────────────────────────────────────────────

class TestProvisionClientUser:
    def test_creates_a_scoped_client_login(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id)
        # get_or_404 engagement, no existing client, no tenant-email collision,
        # then no portal-slug collision
        db = _mock_db([eng, None, None, None])
        body = ca.ClientUserCreate(email="customer@acme.com")

        out = asyncio.run(ca.provision_client_user(eng_id, body, db, op))

        user = _added(db, User)
        assert user is not None
        assert user.role == UserRole.client
        assert user.client_engagement_id == eng_id
        assert user.tenant_id == op.tenant_id
        assert user.hashed_password and user.hashed_password != "customer@acme.com"
        assert out.temp_password  # returned exactly once
        # a portal handle ("user as domain") is auto-generated + returned
        assert user.portal_slug == "customer"     # eng has no name -> email local-part
        assert out.portal_slug == user.portal_slug
        # provisioning is audited
        assert _added(db, __import__("app.models.audit_log", fromlist=["AuditLog"]).AuditLog)

    def test_duplicate_is_conflict(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id)
        existing = SimpleNamespace(id=uuid.uuid4())
        db = _mock_db([eng, existing])
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.provision_client_user(eng_id, ca.ClientUserCreate(email="x@y.com"), db, op))
        assert e.value.status_code == 409

    def test_duplicate_email_in_tenant_is_conflict(self):
        """An email already used elsewhere in the tenant (the operator's own login,
        or a client login already made for another engagement — "one more") must be
        a clean 409, not the DB-constraint 500 that uq_user_tenant_email would raise."""
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id)
        existing_email_user = SimpleNamespace(id=uuid.uuid4(), email="dupe@acme.com")
        # get_or_404 -> eng; no per-engagement client; THEN the tenant-email pre-check hits a dup
        db = _mock_db([eng, None, existing_email_user])
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.provision_client_user(
                eng_id, ca.ClientUserCreate(email="dupe@acme.com"), db, op))
        assert e.value.status_code == 409


# ── scan-request inbox ────────────────────────────────────────────────────────

def _pending_request(eng_id, tenant_id):
    return SimpleNamespace(
        id=uuid.uuid4(), engagement_id=eng_id, tenant_id=tenant_id, status="pending",
        scan_type="vuln_scan", requested_by=uuid.uuid4(), scan_job_id=None,
        reviewed_by=None, reviewed_at=None, review_reason=None,
    )


def _mock_redis():
    """Minimal redis mock for routes that inject RedisConn."""
    return AsyncMock()


class TestApproveScanRequest:
    def test_approve_dispatches_job_and_links_it(self):
        op = _operator()
        eng_id = uuid.uuid4()
        agent = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id,
                              assigned_agent_id=agent, scope_cidrs=["10.0.0.0/24"])
        sr = _pending_request(eng_id, op.tenant_id)
        # scalars: eng, sr, fragile-asset lookup (None), org scan policy (None),
        # WS push: online agents query (empty → scalars().all() = [])
        db = _mock_db([eng, sr, None, None])
        scalars_mock = MagicMock()
        scalars_mock.all = MagicMock(return_value=[])
        last_result = MagicMock()
        last_result.scalars = MagicMock(return_value=scalars_mock)
        db.execute = AsyncMock(side_effect=[
            # get_or_404 engagement
            MagicMock(scalar_one_or_none=MagicMock(return_value=eng)),
            # _get_scan_request
            MagicMock(scalar_one_or_none=MagicMock(return_value=sr),
                      first=MagicMock(return_value=sr)),
            # fragile guard: no fragile assets
            MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))),
            # org scan policy
            MagicMock(scalar_one_or_none=MagicMock(return_value=None)),
            # WS push: online agents query
            last_result,
        ])
        redis = _mock_redis()

        out = asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, redis, op))

        job = _added(db, ScanJob)
        assert job is not None
        # RC-FIX-2: agent_id must be NULL on the DB row so HTTP poll can find it
        assert job.agent_id is None, "agent_id must not be pre-assigned — breaks HTTP poll"
        assert job.result["preferred_agent_id"] == str(agent)
        assert sr.status == "approved"
        assert sr.scan_job_id == job.id
        assert sr.reviewed_by == op.user_id
        assert out["approved"] is True

    def test_approve_without_assigned_agent_is_conflict(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id,
                              assigned_agent_id=None, scope_cidrs=[])
        sr = _pending_request(eng_id, op.tenant_id)
        db = _mock_db([eng, sr])
        redis = _mock_redis()
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, redis, op))
        assert e.value.status_code == 409

    def test_approve_non_pending_is_conflict(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id,
                              assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        sr = _pending_request(eng_id, op.tenant_id)
        sr.status = "approved"
        db = _mock_db([eng, sr])
        redis = _mock_redis()
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, redis, op))
        assert e.value.status_code == 409


class TestRejectScanRequest:
    def test_reject_records_reason(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id)
        sr = _pending_request(eng_id, op.tenant_id)
        db = _mock_db([eng, sr])
        out = asyncio.run(ca.reject_scan_request(eng_id, sr.id, ca.RejectBody(reason="out of window"), db, op))
        assert sr.status == "rejected"
        assert sr.review_reason == "out of window"
        assert out["rejected"] is True

    def test_reject_gives_the_scan_back(self, monkeypatch):
        from app.services import entitlements
        refund = AsyncMock()
        monkeypatch.setattr(entitlements, "refund_for_request", refund)
        op = _operator()
        eng_id = uuid.uuid4()
        sr = _pending_request(eng_id, op.tenant_id)
        db = _mock_db([SimpleNamespace(id=eng_id, tenant_id=op.tenant_id), sr])
        asyncio.run(ca.reject_scan_request(eng_id, sr.id, ca.RejectBody(), db, op))
        refund.assert_awaited_once_with(db, sr)


class TestAssignAgent:
    def test_assigns_agent_to_engagement(self):
        op = _operator()
        eng_id = uuid.uuid4()
        agent_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id, assigned_agent_id=None)
        agent = SimpleNamespace(id=agent_id, tenant_id=op.tenant_id)
        db = _mock_db([eng, agent])
        out = asyncio.run(ca.assign_agent(eng_id, ca.AssignAgentBody(agent_id=agent_id), db, op))
        assert eng.assigned_agent_id == agent_id
        assert out["assigned_agent_id"] == str(agent_id)

    def test_unknown_agent_is_404(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id, assigned_agent_id=None)
        db = _mock_db([eng, None])
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.assign_agent(eng_id, ca.AssignAgentBody(agent_id=uuid.uuid4()), db, op))
        assert e.value.status_code == 404


class TestApproveScanRequestFragileGuard:
    def test_customer_scan_never_touches_fragile_hosts(self, monkeypatch):
        from unittest.mock import AsyncMock as _AM
        from app.intel.fragile import FragileHost
        monkeypatch.setattr("app.services.fragile_guard.load_fragile_hosts",
                            _AM(return_value=[FragileHost("10.0.0.20", ["sector_fn:swift"])]))
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id, assigned_agent_id=uuid.uuid4(),
                              scope_cidrs=["10.0.0.0/24"], excluded_cidrs=["10.0.0.99/32"])
        sr = _pending_request(eng_id, op.tenant_id)
        db = _mock_db([eng, sr, None])     # 3rd: the tenant's scan policy (defaults)
        redis = _mock_redis()
        asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, redis, op))
        job = _added(db, ScanJob)
        assert job.result["_excluded_cidrs"] == ["10.0.0.99/32", "10.0.0.20/32"]
        assert job.result["_fragile_excluded"] == [{"ip": "10.0.0.20", "reasons": ["sector_fn:swift"]}]
