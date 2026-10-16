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
from app.schemas.finding import FindingOut, FindingScanRef, ScanCompareSnapshot

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
         patch.object(findings_router, "_scan_snapshots", new=AsyncMock(return_value={})), \
         patch.object(findings_router, "_scan_meta",
                      new=AsyncMock(side_effect=[
                          FindingScanRef(reference="SCN-260301-AAAAAA"),
                          FindingScanRef(reference="SCN-260302-BBBBBB")])):
        out = await findings_router.compare_scans(
            db=db, current_user=_user(), a="SCN-260301-AAAAAA", b="SCN-260302-BBBBBB",
            engagement_id=None)

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
         patch.object(findings_router, "_scan_snapshots", new=AsyncMock(return_value={})), \
         patch.object(findings_router, "_scan_meta",
                      new=AsyncMock(side_effect=[FindingScanRef(), FindingScanRef()])):
        out = await findings_router.compare_scans(
            db=db, current_user=_user(), a="A", b="B", engagement_id=None)
    assert (out.counts.new, out.counts.fixed) == (0, 0)
    assert out.counts.still_present == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("a_runs,b_runs", [(set(), {uuid.uuid4()}), ({uuid.uuid4()}, set())])
async def test_unknown_scan_is_404(a_runs, b_runs):
    with patch.object(findings_router, "_resolve_scan_run_ids",
                      new=AsyncMock(side_effect=[a_runs, b_runs])):
        with pytest.raises(HTTPException) as e:
            await findings_router.compare_scans(
                db=MagicMock(), current_user=_user(), a="A", b="B", engagement_id=None)
    assert e.value.status_code == 404


def _snap(sev, risk, status="open"):
    return ScanCompareSnapshot(severity=sev, risk_score=risk, status=status)


async def _compare_with(present_a, present_b, outs, snaps_a, snaps_b, cap=500):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        _scalars(present_a), _scalars(present_b), _scalars([object()] * len(outs))])
    with patch.object(findings_router, "_resolve_scan_run_ids",
                      new=AsyncMock(side_effect=[{uuid.uuid4()}, {uuid.uuid4()}])), \
         patch.object(findings_router, "_with_asset_identity", new=AsyncMock(return_value=outs)), \
         patch.object(findings_router, "_scan_snapshots",
                      new=AsyncMock(side_effect=[snaps_a, snaps_b])), \
         patch.object(findings_router, "_scan_meta",
                      new=AsyncMock(side_effect=[FindingScanRef(reference="SCN-A"),
                                                 FindingScanRef(reference="SCN-B")])):
        return await findings_router.build_scan_compare(
            db, _TENANT, "SCN-A", "SCN-B", cap=cap)


@pytest.mark.asyncio
async def test_changed_is_the_part_of_still_present_whose_snapshot_differs():
    up, same, sev_up, gone, fresh = (uuid.uuid4() for _ in range(5))
    outs = [_finding_out(i) for i in (up, same, sev_up, gone, fresh)]
    out = await _compare_with(
        [up, same, sev_up, gone], [up, same, sev_up, fresh], outs,
        {up: _snap("high", 600), same: _snap("high", 600), sev_up: _snap("medium", 400),
         gone: _snap("low", 150)},
        {up: _snap("high", 640), same: _snap("high", 600), sev_up: _snap("high", 520),
         fresh: _snap("critical", 900)})
    assert out.counts.still_present == 3 and out.counts.changed == 2
    # A severity change outranks a bigger score move.
    assert [c.finding.id for c in out.changed] == [sev_up, up]
    first, second = out.changed
    assert first.severity_changed and first.risk_delta == 120
    assert not second.severity_changed and second.risk_delta == 40
    # An unchanged finding stays in still_present but is not in changed.
    assert same in {f.id for f in out.still_present}
    assert same not in {c.finding.id for c in out.changed}


@pytest.mark.asyncio
async def test_status_only_change_counts_as_changed():
    f = uuid.uuid4()
    out = await _compare_with(
        [f], [f], [_finding_out(f)],
        {f: _snap("high", 600, "open")}, {f: _snap("high", 600, "confirmed")})
    assert out.counts.changed == 1
    assert out.changed[0].status_changed and out.changed[0].risk_delta == 0


@pytest.mark.asyncio
async def test_a_scan_without_snapshots_never_invents_a_change():
    f = uuid.uuid4()
    out = await _compare_with(
        [f], [f], [_finding_out(f)],
        {f: ScanCompareSnapshot()}, {f: _snap("critical", 900)})
    assert out.counts.still_present == 1 and out.counts.changed == 0


@pytest.mark.asyncio
async def test_summaries_count_severity_from_the_snapshot_and_flag_fallbacks():
    a, b = uuid.uuid4(), uuid.uuid4()
    outs = [_finding_out(a, FindingSeverity.low), _finding_out(b, FindingSeverity.low)]
    out = await _compare_with(
        [a], [a, b], outs,
        {a: _snap("critical", 900)}, {a: _snap("high", 700), b: ScanCompareSnapshot()})
    # Scan A: from the snapshot (critical), not today's row (low).
    assert out.summary_a.by_severity["critical"] == 1 and out.summary_a.from_snapshot
    assert out.summary_a.average_risk == 900
    # Scan B: b has no snapshot, so its severity falls back to today and says so.
    assert out.summary_b.by_severity["high"] == 1 and out.summary_b.by_severity["low"] == 1
    assert out.summary_b.from_snapshot is False


@pytest.mark.asyncio
async def test_export_is_uncapped_and_csv_cells_cannot_run_as_formulas():
    n = uuid.uuid4()
    f = _finding_out(n)
    f.title = "=HYPERLINK(\"http://evil\")"
    out = await _compare_with([], [n], [f], {}, {n: _snap("high", 600)}, cap=None)
    text = findings_router.compare_to_csv(out)
    lines = text.lstrip("\ufeff").splitlines()
    assert lines[0].startswith("bucket,finding_id,title")
    assert lines[1].startswith("new,") and "'=HYPERLINK" in lines[1]


@pytest.mark.asyncio
@pytest.mark.parametrize("fmt,media,ext", [("csv", "text/csv", ".csv"), ("json", "application/json", ".json")])
async def test_export_endpoint_names_the_file_after_both_scans(fmt, media, ext):
    n = uuid.uuid4()
    result = await _compare_with([], [n], [_finding_out(n)], {}, {n: _snap("high", 600)}, cap=None)
    with patch.object(findings_router, "build_scan_compare", new=AsyncMock(return_value=result)) as built:
        resp = await findings_router.export_scan_compare(
            db=MagicMock(), current_user=_user(), a="SCN-A", b="SCN-B", format=fmt, engagement_id=None)
    assert built.await_args.kwargs["cap"] is None
    assert resp.media_type.startswith(media)
    assert resp.headers["content-disposition"] == f'attachment; filename="compare-SCN-A-vs-SCN-B{ext}"'
