"""
test_portal_read.py — Phase 2: the customer-facing read API. Verifies the two
data-exposure controls that matter most — the ClientFindingOut whitelist and the
approved-only report gate — plus scoping and posture reuse. Handlers are called
directly with a mocked async db (repo convention).
"""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.audit_log import AuditLog
from app.models.enums import EngagementStatus, FindingSeverity, FindingStatus
from app.models.scan_request import ScanRequest
from app.routers import portal
from app.schemas.auth import CurrentUser
from app.schemas.portal import ClientFindingOut, ScanRequestCreate


def _client(engagement: uuid.UUID | None = None) -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="client",
                       client_engagement_id=engagement or uuid.uuid4())


def _operator() -> CurrentUser:
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="manager")


def _db_list(*lists):
    """Each db.execute(...) → result whose .scalars().all() is the next list."""
    db = MagicMock()
    results = []
    for lst in lists:
        r = MagicMock()
        r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=lst)))
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    return db


def _db_scalar(*vals):
    db = MagicMock()
    results = []
    for v in vals:
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=v)
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    return db


def _finding_with_internal():
    """A finding-like ORM object carrying BOTH whitelisted and internal fields."""
    return SimpleNamespace(
        id=uuid.uuid4(), title="Unauth RCE", description="bad", severity=FindingSeverity.critical,
        status=FindingStatus.open, cvss_score=None, cve_ids=["CVE-2024-1"], risk_score=None,
        remediation="patch now", first_seen=None,
        # internal — MUST NOT appear in customer output:
        exploitable=True, exploit_validated=True, detection_status="missed",
        needs_review=True, verification_rationale="internal analyst note",
        verification_confidence=42, evidence={"raw": "exploit payload"},
        resolution_miss_count=3, detected_db_version="dbhash", reopened_count=1,
        last_seen=None, epss_score=0.5,
    )


_INTERNAL = {
    "exploitable", "exploit_validated", "detection_status", "needs_review",
    "verification_state", "verification_confidence", "verification_rationale",
    "verification_method", "resolution_miss_count", "resolution_method",
    "resolution_run_id", "detected_db_version", "reopened_count",
    "detection_run_id", "evidence", "last_seen", "mitre_techniques", "epss_score",
}


class TestClientFindingWhitelist:
    def test_schema_is_a_whitelist(self):
        fields = set(ClientFindingOut.model_fields)
        leaks = fields & _INTERNAL
        assert not leaks, f"ClientFindingOut leaks internal fields: {leaks}"
        assert {"id", "title", "severity", "status", "remediation", "cve_ids"} <= fields

    def test_serialization_drops_internal_fields(self):
        out = ClientFindingOut.model_validate(_finding_with_internal())
        d = out.model_dump()
        assert not (set(d) & _INTERNAL), f"leaked: {set(d) & _INTERNAL}"
        assert d["remediation"] == "patch now"
        assert d["cve_ids"] == ["CVE-2024-1"]


class TestPortalFindings:
    def test_findings_scoped_and_serialized(self):
        res = asyncio.run(portal.portal_findings(_client(), _db_list([_finding_with_internal()])))
        assert len(res) == 1
        assert not (set(res[0].model_dump()) & _INTERNAL)

    def test_operator_is_forbidden(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.portal_findings(_operator(), _db_list([])))
        assert e.value.status_code == 403

    def test_single_finding_404_when_out_of_scope(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.portal_finding(uuid.uuid4(), _client(), _db_scalar(None)))
        assert e.value.status_code == 404


class TestPortalReports:
    def test_unapproved_or_missing_report_is_404(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.portal_report(uuid.uuid4(), _client(), _db_scalar(None)))
        assert e.value.status_code == 404

    def test_lists_approved_reports(self):
        rep = SimpleNamespace(id=uuid.uuid4(), output_type="exec_summary",
                              model="claude", generated_at=datetime.now(timezone.utc))
        res = asyncio.run(portal.portal_reports(_client(), _db_list([rep])))
        assert len(res) == 1 and res[0].output_type == "exec_summary"

    def test_download_returns_content_for_approved(self):
        rep = SimpleNamespace(id=uuid.uuid4(), output_type="exec_summary", model="claude",
                              generated_at=datetime.now(timezone.utc), output="the report body")
        res = asyncio.run(portal.portal_report(rep.id, _client(), _db_scalar(rep)))
        assert res.content == "the report body"


class TestPortalPostureAndEngagement:
    def test_posture_scores_open_findings(self):
        f = SimpleNamespace(id=uuid.uuid4(), severity=FindingSeverity.critical, risk_score=900,
                            epss_score=0.9, exploitable=True, exploit_validated=False,
                            first_seen=None, last_seen=None)
        res = asyncio.run(portal.portal_posture(_client(), _db_list([f])))
        assert 0 <= res.risk_index <= 100
        assert res.open_findings == 1
        assert res.grade in ("A", "B", "C", "D", "F")

    def test_engagement_summary(self):
        eng = SimpleNamespace(id=uuid.uuid4(), name="Acme Q3", status=EngagementStatus.active,
                              scope_cidrs=["10.0.0.0/24", "10.0.1.0/24"], assigned_agent_id=uuid.uuid4())
        res = asyncio.run(portal.portal_engagement(_client(eng.id), _db_scalar(eng)))
        assert res.name == "Acme Q3"
        assert res.scope_cidr_count == 2
        assert res.has_assigned_agent is True


def _db_first(*firsts):
    """Each db.execute(...) → result whose .scalars().first() is the next value;
    plus add/flush/refresh for the create path."""
    db = MagicMock()
    results = []
    for v in firsts:
        r = MagicMock()
        r.scalars = MagicMock(return_value=MagicMock(first=MagicMock(return_value=v)))
        results.append(r)
    db.execute = AsyncMock(side_effect=results)
    db.add = MagicMock()
    db.flush = AsyncMock()

    async def _refresh(o):
        if getattr(o, "id", None) is None:
            o.id = uuid.uuid4()

    db.refresh = _refresh
    return db


def _added(db, cls):
    for call in db.add.call_args_list:
        if isinstance(call.args[0], cls):
            return call.args[0]
    return None


class TestCreateScanRequest:
    def test_creates_pending_request_and_audits(self):
        db = _db_first(None)  # no existing pending
        out = asyncio.run(portal.create_scan_request(
            ScanRequestCreate(scan_type="vuln_scan", note="please rescan"), _client(), db))
        assert out.status == "pending"
        sr = _added(db, ScanRequest)
        assert sr is not None and sr.scan_type == "vuln_scan" and sr.status == "pending"
        assert _added(db, AuditLog) is not None          # client action audited

    def test_duplicate_pending_is_conflict(self):
        db = _db_first(SimpleNamespace(id=uuid.uuid4()))  # a pending already exists
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(ScanRequestCreate(), _client(), db))
        assert e.value.status_code == 409

    def test_operator_cannot_create(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(ScanRequestCreate(), _operator(), _db_first(None)))
        assert e.value.status_code == 403
