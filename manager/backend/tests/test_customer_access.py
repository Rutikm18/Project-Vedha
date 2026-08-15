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
    def test_dispatches_on_the_assigned_agent(self):
        agent = uuid.uuid4()
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=agent, scope_cidrs=["10.0.0.0/24"])
        sr = SimpleNamespace(id=uuid.uuid4(), scan_type="vuln_scan", requested_by=uuid.uuid4())
        job = ca.build_scan_job(sr, eng)
        assert job.agent_id == str(agent)
        assert job.job_type == ScanJobType.vuln_scan
        assert job.engagement_id == eng.id
        assert job.result["scan_request_id"] == str(sr.id)
        assert job.result["scope_cidrs"] == ["10.0.0.0/24"]

    def test_unknown_scan_type_falls_back_to_vuln_scan(self):
        eng = SimpleNamespace(id=uuid.uuid4(), assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        sr = SimpleNamespace(id=uuid.uuid4(), scan_type="bogus", requested_by=None)
        assert ca.build_scan_job(sr, eng).job_type == ScanJobType.vuln_scan

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


class TestApproveScanRequest:
    def test_approve_dispatches_job_and_links_it(self):
        op = _operator()
        eng_id = uuid.uuid4()
        agent = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id,
                              assigned_agent_id=agent, scope_cidrs=["10.0.0.0/24"])
        sr = _pending_request(eng_id, op.tenant_id)
        db = _mock_db([eng, sr])

        out = asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, op))

        job = _added(db, ScanJob)
        assert job is not None and job.agent_id == str(agent)
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
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, op))
        assert e.value.status_code == 409

    def test_approve_non_pending_is_conflict(self):
        op = _operator()
        eng_id = uuid.uuid4()
        eng = SimpleNamespace(id=eng_id, tenant_id=op.tenant_id,
                              assigned_agent_id=uuid.uuid4(), scope_cidrs=[])
        sr = _pending_request(eng_id, op.tenant_id)
        sr.status = "approved"
        db = _mock_db([eng, sr])
        with pytest.raises(HTTPException) as e:
            asyncio.run(ca.approve_scan_request(eng_id, sr.id, db, op))
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
