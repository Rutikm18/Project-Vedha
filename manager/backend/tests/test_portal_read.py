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


def _finding(severity="high", status=FindingStatus.open, resolved_at=None,
             first_seen=None):
    return SimpleNamespace(
        id=uuid.uuid4(), severity=severity, status=status,
        risk_score=None, epss_score=None, exploitable=False, exploit_validated=False,
        first_seen=first_seen, last_seen=first_seen, resolved_at=resolved_at,
    )


class TestSummary:
    def test_aggregates_posture_counts_and_queue(self):
        # findings list, then two count scalars (pending, running)
        findings = [_finding("critical"), _finding("high"),
                    _finding("low", status=FindingStatus.remediated,
                             resolved_at=datetime.now(timezone.utc))]
        db = MagicMock()
        f_res = MagicMock()
        f_res.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=findings)))
        pending_res = MagicMock(); pending_res.scalar_one = MagicMock(return_value=2)
        running_res = MagicMock(); running_res.scalar_one = MagicMock(return_value=1)
        db.execute = AsyncMock(side_effect=[f_res, pending_res, running_res])

        out = asyncio.run(portal.portal_summary(_client(), db))
        assert out.open_findings == 2 and out.closed_findings == 1
        assert out.severity_counts["critical"] == 1 and out.severity_counts["low"] == 0
        assert out.pending_requests == 2 and out.running_jobs == 1


class TestTrends:
    def test_returns_severity_and_timeline(self):
        findings = [_finding("high", first_seen=datetime.now(timezone.utc))]
        out = asyncio.run(portal.portal_trends(_client(), _db_list(findings)))
        assert out.by_severity["high"] == 1
        assert len(out.timeline) == 6            # last 6 months, zero-filled


def _db_for_create(engagement, pending_count: int = 0):
    """Mock the create_scan_request db flow: execute#1 → engagement lookup
    (.scalar_one_or_none), execute#2 → pending count (.scalar_one). Plus
    add/flush/refresh for the insert path."""
    db = MagicMock()
    eng_result = MagicMock()
    eng_result.scalar_one_or_none = MagicMock(return_value=engagement)
    count_result = MagicMock()
    count_result.scalar_one = MagicMock(return_value=pending_count)
    db.execute = AsyncMock(side_effect=[eng_result, count_result])
    db.add = MagicMock()
    db.flush = AsyncMock()

    async def _refresh(o):
        if getattr(o, "id", None) is None:
            o.id = uuid.uuid4()

    db.refresh = _refresh
    return db


def _engagement(eng_id: uuid.UUID, scope=("10.0.0.0/24",), excluded=()):
    return SimpleNamespace(id=eng_id, scope_cidrs=list(scope),
                           excluded_cidrs=list(excluded))


class TestCreateScanRequest:
    def test_creates_pending_request_with_targets_and_intensity(self):
        user = _client()
        eng = _engagement(user.client_engagement_id, scope=["10.0.0.0/24"])
        db = _db_for_create(eng, pending_count=0)
        out = asyncio.run(portal.create_scan_request(
            ScanRequestCreate(scan_type="vuln_scan", targets=["10.0.0.5"],
                              intensity="deep", note="please rescan"), user, db))
        assert out.status == "pending"
        sr = _added(db, ScanRequest)
        assert sr is not None and sr.scan_type == "vuln_scan"
        # target normalized to a /32 and persisted; intensity carried through
        assert sr.targets == ["10.0.0.5/32"]
        assert sr.intensity == "deep"
        assert _added(db, AuditLog) is not None          # client action audited

    def test_whole_scope_when_no_targets(self):
        user = _client()
        eng = _engagement(user.client_engagement_id)
        db = _db_for_create(eng, pending_count=0)
        out = asyncio.run(portal.create_scan_request(
            ScanRequestCreate(scan_type="discovery"), user, db))
        assert out.status == "pending"
        assert _added(db, ScanRequest).targets is None    # None = whole scope

    def test_unknown_scan_type_is_422(self):
        user = _client()
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(
                ScanRequestCreate(scan_type="rm_rf_slash"), user,
                _db_for_create(_engagement(user.client_engagement_id))))
        assert e.value.status_code == 422

    def test_out_of_scope_target_is_422(self):
        user = _client()
        eng = _engagement(user.client_engagement_id, scope=["10.0.0.0/24"])
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(
                ScanRequestCreate(scan_type="vuln_scan", targets=["192.0.2.9"]),
                user, _db_for_create(eng)))
        assert e.value.status_code == 422

    def test_excluded_target_is_422(self):
        user = _client()
        eng = _engagement(user.client_engagement_id,
                          scope=["10.0.0.0/24"], excluded=["10.0.0.0/28"])
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(
                ScanRequestCreate(scan_type="vuln_scan", targets=["10.0.0.5"]),
                user, _db_for_create(eng)))
        assert e.value.status_code == 422

    def test_queue_cap_is_conflict(self):
        user = _client()
        eng = _engagement(user.client_engagement_id)
        db = _db_for_create(eng, pending_count=5)         # already at the cap
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(
                ScanRequestCreate(scan_type="vuln_scan"), user, db))
        assert e.value.status_code == 409

    def test_operator_cannot_create(self):
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.create_scan_request(
                ScanRequestCreate(), _operator(), MagicMock()))
        assert e.value.status_code == 403
