"""Every finding response carries the scan that produced/confirmed it.

Task 3 of per-scan-findings: FindingOut.scan = {reference, use_case_id, intensity,
scanned_at, run_id, job_id}, resolved in ONE batched query per page from
detection_run_id → detection_runs → scan_jobs. So the UI can label and group
findings by scan (SCN-YYMMDD-XXXXXX) without exposing run/job UUIDs, and without
an N+1. Legacy/self-assessed findings (no run link) get scan=None and no query.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.routers import findings as findings_router

_SCANNED = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)


def _orm_finding(asset_id=None, detection_run_id=None):
    now = datetime.now(timezone.utc)
    f = Finding(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), asset_id=asset_id, cve_ids=None,
        title="t", description=None, cvss_score=None, cvss_vector=None, epss_score=None,
        risk_score=None, severity=FindingSeverity.high, status=FindingStatus.open,
        exploitable=False, exploit_validated=False, mitre_techniques=None,
        detection_status=DetectionStatus.detected, evidence={}, remediation=None,
        needs_review=False, reopened_count=0, created_at=now, updated_at=now,
    )
    f.detection_run_id = detection_run_id
    return f


def _scan_row(run_id, job_id, *, reference, use_case_id, intensity,
              run_started, job_done, job_started):
    # Column order matches the select in _scan_refs.
    return (run_id, run_started, job_id, reference, use_case_id, intensity,
            job_done, job_started)


@pytest.mark.asyncio
async def test_scan_block_resolved_in_one_query():
    run_id, job_id = uuid.uuid4(), uuid.uuid4()
    f = _orm_finding(asset_id=None, detection_run_id=run_id)  # no asset → skip that query
    result = MagicMock()
    result.all.return_value = [_scan_row(
        run_id, job_id, reference="SCN-260301-ABC123",
        use_case_id="uc_network_sweep", intensity="aggressive",
        run_started=_SCANNED - timedelta(hours=1), job_done=_SCANNED,
        job_started=_SCANNED - timedelta(minutes=5))]
    db = MagicMock()
    db.execute = AsyncMock(return_value=result)

    out = await findings_router._with_asset_identity(db, [f])

    assert db.execute.await_count == 1  # no asset ids → only the scan query
    s = out[0].scan
    assert s is not None
    assert (s.reference, s.use_case_id, s.intensity) == (
        "SCN-260301-ABC123", "uc_network_sweep", "aggressive")
    assert s.scanned_at == _SCANNED           # scan completion wins
    assert s.run_id == run_id and s.job_id == job_id


@pytest.mark.asyncio
async def test_no_run_link_means_no_scan_block_and_no_query():
    f = _orm_finding(asset_id=None, detection_run_id=None)
    db = MagicMock()
    db.execute = AsyncMock()
    out = await findings_router._with_asset_identity(db, [f])
    assert db.execute.await_count == 0
    assert out[0].scan is None


@pytest.mark.asyncio
async def test_scanned_at_falls_back_when_scan_completion_missing():
    """A scan still running/cancelled has no completed_at; fall back to its start,
    then to the detection run's start — never leave scanned_at null when we have a run."""
    run_id = uuid.uuid4()
    only_run_started = _SCANNED - timedelta(hours=2)
    f = _orm_finding(detection_run_id=run_id)
    refs_db = MagicMock()
    r = MagicMock()
    r.all.return_value = [_scan_row(
        run_id, None, reference=None, use_case_id=None, intensity=None,
        run_started=only_run_started, job_done=None, job_started=None)]
    refs_db.execute = AsyncMock(return_value=r)

    refs = await findings_router._scan_refs(refs_db, [f])

    assert refs[run_id].scanned_at == only_run_started
    assert refs[run_id].reference is None
