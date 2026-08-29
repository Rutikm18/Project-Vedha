"""VA Campaigns live view: per-probe jobs + pipeline phases + findings+remediation."""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.routers import engagements as eng


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items))


@pytest.mark.asyncio
async def test_campaign_progress_aggregates_jobs_detection_and_findings():
    agent_id = uuid.uuid4()
    job = SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value="completed"), agent_id=agent_id,
        result={"use_case_id": "uc_network_va", "ok": True, "facts_count": 42,
                "scanner_runs": [{"id": "smb_scan"}, {"id": "rdp_scan"}], "profile": "it"},
        created_at=None, started_at=None, completed_at=None,
    )
    agent = SimpleNamespace(id=agent_id, name="scanner-probe-01")
    run = SimpleNamespace(status="completed", facts_count=42, findings_new=3, findings_current=3,
                          started_at=None, finished_at=None)
    smbv1 = SimpleNamespace(
        id=uuid.uuid4(), title="SMBv1 enabled (wormable, deprecated)",
        severity=SimpleNamespace(value="critical"), risk_score=90,
        cve_ids=None, mitre_techniques=["T1210"], status=SimpleNamespace(value="confirmed"),
        remediation="Disable SMBv1.", asset_id=None,
        evidence={"negotiated": "SMBv1"})

    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        _scalars([job]),                                                         # jobs
        _scalars([agent]),                                                       # agents
        MagicMock(scalar_one_or_none=lambda: run),                              # detection run
        _scalars([smbv1]),                                                       # findings
    ])

    out = await eng.campaign_progress(uuid.uuid4(), db, _user())

    # per-probe job + safe raw-result summary
    assert out["jobs"][0]["phase"] == "complete"
    assert out["jobs"][0]["agent_name"] == "scanner-probe-01"
    assert out["jobs"][0]["use_case_id"] == "uc_network_va"
    assert set(out["jobs"][0]["result_summary"]["scanners"]) == {"smb_scan", "rdp_scan"}
    assert out["jobs"][0]["result_summary"]["fact_count"] == 42

    # full pipeline phases
    names = [p["name"] for p in out["phases"]]
    assert names == ["scanning", "aggregating", "detection", "correlation",
                     "prioritization", "remediation"]
    assert all(p["status"] == "done" for p in out["phases"])       # detection complete
    assert out["percent"] == 100
    # authoritative status: complete ONLY when the whole pipeline finished
    assert out["overall_status"] == "complete" and out["is_complete"] is True
    assert out["job_stats"]["total"] == 1 and out["job_stats"]["complete"] == 1
    assert out["summary"]["total_findings"] == 1 and out["summary"]["actionable"] == 1
    assert out["summary"]["top_techniques"][0]["technique"] == "T1210"

    # detection summary + finding with remediation (for step-by-step UI)
    assert out["detection"]["done"] is True and out["detection"]["status"] == "completed"
    assert out["detection"]["by_severity"]["critical"] == 1
    f = out["findings"][0]
    assert "SMBv1" in f["title"] and f["severity"] == "critical"
    assert f["risk_score"] == 90.0 and f["mitre_techniques"] == ["T1210"]
    assert f["remediation"] == "Disable SMBv1."


@pytest.mark.asyncio
async def test_campaign_progress_no_detection_yet_is_scanning():
    job = SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value="running"), agent_id=None,
        result=None, created_at=None, started_at=None, completed_at=None)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([job]),
        MagicMock(scalar_one_or_none=lambda: None),     # no detection run
        _scalars([]),                                    # no findings
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["jobs"][0]["phase"] == "scanning"
    assert out["detection"]["status"] == "pending"
    scanning = next(p for p in out["phases"] if p["name"] == "scanning")
    assert scanning["status"] == "active"
    assert out["percent"] == 0
    # KEY: still scanning → NOT complete (the premature-completed bug)
    assert out["overall_status"] == "scanning" and out["is_complete"] is False


# ── the state machine at EVERY phase (guards the "stuck at detecting" bug) ─────
def _run_scenario(*, job_status, run_status, findings):
    """Build a campaign_progress scenario with a given job + detection-run state."""
    job = SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value=job_status), agent_id=None,
        result={"use_case_id": "uc_network_va"} if job_status else None,
        created_at=None, started_at=None, completed_at=None)
    run = None if run_status is None else SimpleNamespace(
        status=run_status, facts_count=1, findings_new=findings,
        findings_current=findings, started_at=None, finished_at=None)
    fs = [SimpleNamespace(
        id=uuid.uuid4(), title="x", severity=SimpleNamespace(value="high"),
        risk_score=70, cve_ids=None, mitre_techniques=["T1"],
        status=SimpleNamespace(value="open"), remediation="fix", asset_id=None,
        evidence={}) for _ in range(findings)]
    side = [MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
            _scalars([job])]
    # no agent lookup (agent_id None) → next is detection run, then findings
    side += [MagicMock(scalar_one_or_none=lambda: run), _scalars(fs)]
    db = MagicMock()
    db.execute = AsyncMock(side_effect=side)
    return db


import pytest as _pytest


@_pytest.mark.asyncio
@_pytest.mark.parametrize("job_status,run_status,findings,expect_status,expect_complete", [
    ("running",   None,        0, "scanning",    False),  # scan in flight
    ("completed", None,        0, "aggregating", False),  # facts submitted, detection not started
    ("completed", "running",   0, "detecting",   False),  # detection in progress
    ("completed", "completed", 2, "complete",    True),   # ← the fix: reaches complete (was stuck)
    ("completed", "completed", 0, "complete",    True),   # complete with zero findings (clean)
    ("completed", "failed",    0, "error",       False),  # detection errored
])
async def test_pipeline_advances_through_every_phase(job_status, run_status, findings,
                                                     expect_status, expect_complete):
    db = _run_scenario(job_status=job_status, run_status=run_status, findings=findings)
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == expect_status, \
        f"{job_status}/{run_status} → {out['overall_status']} (want {expect_status})"
    assert out["is_complete"] is expect_complete
    # invariant: never 'complete' unless detection actually finished
    if out["overall_status"] == "complete":
        assert out["detection"]["done"] is True


@_pytest.mark.asyncio
async def test_completed_run_is_not_stuck_at_detecting():
    """Regression: RUN_COMPLETED is 'completed', not 'done' — the endpoint must not
    stay at 'detecting' after the backend marks the run completed."""
    db = _run_scenario(job_status="completed", run_status="completed", findings=1)
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "complete" and out["is_complete"] is True
    det = next(p for p in out["phases"] if p["name"] == "detection")
    assert det["status"] == "done"
