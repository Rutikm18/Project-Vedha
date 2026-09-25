"""Diff two scans: what's new, fixed, and still present.

Task 5 of per-scan-findings. A finding is 'present' in a scan when that scan saw it
new or reaffirmed (resolved is excluded — a scan that closed a finding did not have
it). Then new = present in b not a; fixed = present in a not b; still_present = both.
counts are true totals; each list is capped, most-severe first. Unknown scan → 404.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.routers import findings as findings_router
from app.schemas.auth import CurrentUser
from app.schemas.finding import FindingOut, FindingScanRef

_TENANT = uuid.uuid4()


def _user():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=_TENANT, role="manager")


def _finding_out(fid, sev=FindingSeverity.high):
    now = datetime.now(timezone.utc)
    orm = Finding(
        id=fid, engagement_id=uuid.uuid4(), asset_id=None, cve_ids=None,
        title="t", description=None, cvss_score=None, cvss_vector=None, epss_score=None,
        risk_score=None, severity=sev, status=FindingStatus.open,
        exploitable=False, exploit_validated=False, mitre_techniques=None,
        detection_status=DetectionStatus.detected, evidence={}, remediation=None,
        needs_review=False, reopened_count=0, created_at=now, updated_at=now,
    )
    return FindingOut.model_validate(orm)


def _scalars(values):
    r = MagicMock()
    r.scalars.return_value.all.return_value = values
    return r


@pytest.mark.asyncio
async def test_compare_buckets_new_fixed_still_present():
    n_id, f_id, s_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    # present_a = {fixed, still}; present_b = {new, still}
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        _scalars([f_id, s_id]),          # present in a
        _scalars([n_id, s_id]),          # present in b
        _scalars([object(), object(), object()]),  # finding load (patched serializer ignores)
    ])
    outs = [_finding_out(n_id), _finding_out(f_id), _finding_out(s_id)]

    with patch.object(findings_router, "_resolve_scan_run_ids",
                      new=AsyncMock(side_effect=[{uuid.uuid4()}, {uuid.uuid4()}])), \
         patch.object(findings_router, "_with_asset_identity",
                      new=AsyncMock(return_value=outs)), \
         patch.object(findings_router, "_scan_meta",
                      new=AsyncMock(side_effect=[
                          FindingScanRef(reference="SCN-260301-AAAAAA"),
                          FindingScanRef(reference="SCN-260302-BBBBBB")])):
        out = await findings_router.compare_scans(
            db=db, current_user=_user(), a="SCN-260301-AAAAAA", b="SCN-260302-BBBBBB")

    assert (out.counts.new, out.counts.fixed, out.counts.still_present) == (1, 1, 1)
    assert {f.id for f in out.new} == {n_id}
    assert {f.id for f in out.fixed} == {f_id}
    assert {f.id for f in out.still_present} == {s_id}
    assert out.a.reference == "SCN-260301-AAAAAA"
    assert out.b.reference == "SCN-260302-BBBBBB"


@pytest.mark.asyncio
async def test_identical_scans_are_all_still_present():
    s1, s2 = uuid.uuid4(), uuid.uuid4()
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        _scalars([s1, s2]),
        _scalars([s1, s2]),
        _scalars([object(), object()]),
    ])
    with patch.object(findings_router, "_resolve_scan_run_ids",
                      new=AsyncMock(side_effect=[{uuid.uuid4()}, {uuid.uuid4()}])), \
         patch.object(findings_router, "_with_asset_identity",
                      new=AsyncMock(return_value=[_finding_out(s1), _finding_out(s2)])), \
         patch.object(findings_router, "_scan_meta",
                      new=AsyncMock(side_effect=[FindingScanRef(), FindingScanRef()])):
        out = await findings_router.compare_scans(
            db=db, current_user=_user(), a="A", b="B")
    assert (out.counts.new, out.counts.fixed) == (0, 0)
    assert out.counts.still_present == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("a_runs,b_runs", [(set(), {uuid.uuid4()}), ({uuid.uuid4()}, set())])
async def test_unknown_scan_is_404(a_runs, b_runs):
    with patch.object(findings_router, "_resolve_scan_run_ids",
                      new=AsyncMock(side_effect=[a_runs, b_runs])):
        with pytest.raises(HTTPException) as e:
            await findings_router.compare_scans(
                db=MagicMock(), current_user=_user(), a="A", b="B")
    assert e.value.status_code == 404
