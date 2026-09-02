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


def _rows(items):
    """A result whose .all() returns raw rows (used for the queue-state query)."""
    return MagicMock(all=lambda: items)


# campaign_progress query order: get_or_404, jobs, [agents], runs(all),
# scan_result_ids, queue_rows, findings.


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
                          started_at=None, finished_at=None, scan_result_id=None, stats=None)
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
        _scalars([run]),                                                          # detection runs (all)
        _scalars([]),                                                             # scan_result ids
        _rows([]),                                                                # queue rows
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
        _scalars([]),                                    # no detection runs
        _scalars([]),                                    # scan_result ids
        _rows([]),                                       # queue rows
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
        findings_current=findings, started_at=None, finished_at=None,
        scan_result_id=None, stats=None, error=None)
    fs = [SimpleNamespace(
        id=uuid.uuid4(), title="x", severity=SimpleNamespace(value="high"),
        risk_score=70, cve_ids=None, mitre_techniques=["T1"],
        status=SimpleNamespace(value="open"), remediation="fix", asset_id=None,
        evidence={}) for _ in range(findings)]
    side = [MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
            _scalars([job])]
    # no agent lookup (agent_id None) → runs(all), scan_result ids, queue, findings
    side += [_scalars([run] if run else []), _scalars([]), _rows([]), _scalars(fs)]
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


# ── the completion invariant ─────────────────────────────────────────────────
# "Why does an assessment never complete to 100%?"
#
# `percent` counted phases done using `detection_done` (the LATEST detection run
# completed), while `is_complete` additionally required `evidence_covered` (EVERY
# scan submission consumed by a completed run). Those are different signals, so a
# multi-agent campaign whose newest submission was detected but whose earlier one
# was not showed **percent=100 with is_complete=False** — a progress bar pinned at
# 100% on a campaign that never announced completion.
#
# The invariant below is the fix, stated once: the bar reaching 100 and the
# campaign being complete are the same fact, so they must never disagree.

def _run(status, sr_id=None, started_at=None):
    return SimpleNamespace(
        id=uuid.uuid4(), status=status, scan_result_id=sr_id,
        started_at=started_at, finished_at=None, error=None, stats={},
        facts_count=10, findings_new=1, findings_current=1)


def _job(status="completed"):
    return SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="network_va"),
        status=SimpleNamespace(value=status), agent_id=None,
        result={"facts_count": 10}, created_at=None, started_at=None, completed_at=None)


async def _progress(jobs, runs, sr_ids, queue_rows=(), heartbeat=None):
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(
            id=uuid.uuid4(), name="e", status="active")),
        _scalars(jobs), _scalars(runs), _scalars(list(sr_ids)),
        _rows(list(queue_rows)), _scalars([]),
        MagicMock(scalar_one_or_none=lambda: heartbeat),
    ])
    return await eng.campaign_progress(uuid.uuid4(), db, _user())


@pytest.mark.asyncio
async def test_percent_reaches_100_exactly_when_the_campaign_is_complete():
    """The invariant. Checked across the states a real campaign passes through."""
    from app.models.detection_run import RUN_COMPLETED, RUN_RUNNING
    a, b = uuid.uuid4(), uuid.uuid4()

    cases = [
        ("no jobs yet",              [],                [],                            []),
        ("still scanning",           [_job("running")], [],                            []),
        ("facts in, no run yet",     [_job()],          [],                            []),
        ("run completed, covered",   [_job()],          [_run(RUN_COMPLETED, a)],      [a]),
        ("2 subs, only latest done", [_job(), _job()],  [_run(RUN_COMPLETED, b)],      [a, b]),
        ("run still running",        [_job()],          [_run(RUN_RUNNING, a)],        [a]),
    ]
    for label, jobs, runs, sr_ids in cases:
        out = await _progress(jobs, runs, sr_ids)
        assert (out["percent"] == 100) == out["is_complete"], (
            f"{label}: percent={out['percent']} but is_complete={out['is_complete']} "
            f"(status={out['overall_status']})")


@pytest.mark.asyncio
async def test_uncovered_submission_holds_progress_below_100():
    """The exact regression: the newest submission was detected, an earlier one was
    not. Before the fix this reported 100%."""
    from app.models.detection_run import RUN_COMPLETED
    a, b = uuid.uuid4(), uuid.uuid4()
    out = await _progress([_job(), _job()], [_run(RUN_COMPLETED, b)], [a, b])

    assert out["percent"] < 100
    assert out["is_complete"] is False
    assert out["overall_status"] == "detecting"
    assert any("awaiting detection" in r for r in out["reasons"])
    # scanning + aggregating are genuinely done; the detection half is not
    done = {p["name"] for p in out["phases"] if p["status"] == "done"}
    assert done == {"scanning", "aggregating"}


@pytest.mark.asyncio
async def test_full_coverage_completes_at_100():
    from app.models.detection_run import RUN_COMPLETED
    a, b = uuid.uuid4(), uuid.uuid4()
    out = await _progress([_job(), _job()],
                          [_run(RUN_COMPLETED, b), _run(RUN_COMPLETED, a)], [a, b])
    assert out["percent"] == 100
    assert out["is_complete"] is True
    assert out["overall_status"] == "complete"
    assert all(p["status"] == "done" for p in out["phases"])


@pytest.mark.asyncio
async def test_a_wedged_detection_run_explains_itself():
    """The other way a campaign never finishes: a run that starts and never
    completes. The outbox event is already consumed, so the queue signals say
    nothing — without this the UI shows 'detecting' forever with no reason."""
    from datetime import datetime, timedelta, timezone
    from app.models.detection_run import RUN_RUNNING
    a = uuid.uuid4()
    long_ago = datetime.now(timezone.utc) - timedelta(minutes=45)
    out = await _progress([_job()], [_run(RUN_RUNNING, a, started_at=long_ago)], [a])

    assert out["is_complete"] is False and out["percent"] < 100
    assert out["overall_status"] == "detecting"
    assert any("without finishing" in r for r in out["reasons"]), out["reasons"]


@pytest.mark.asyncio
async def test_a_briefly_running_run_is_not_called_stalled():
    """A run that started seconds ago is busy, not wedged — no alarming reason."""
    from datetime import datetime, timezone
    from app.models.detection_run import RUN_RUNNING
    a = uuid.uuid4()
    out = await _progress([_job()],
                          [_run(RUN_RUNNING, a, started_at=datetime.now(timezone.utc))], [a])
    assert not any("without finishing" in r for r in out["reasons"])


@pytest.mark.asyncio
async def test_naive_started_at_does_not_crash_the_page():
    """started_at can come back tz-naive depending on the driver; subtracting it
    from an aware `now` would raise and blank the whole campaign page."""
    from datetime import datetime, timedelta, timezone
    from app.models.detection_run import RUN_RUNNING
    a = uuid.uuid4()
    # tz-naive on purpose — that is the shape the guard exists for.
    naive = (datetime.now(timezone.utc) - timedelta(minutes=45)).replace(tzinfo=None)
    out = await _progress([_job()], [_run(RUN_RUNNING, a, started_at=naive)], [a])
    assert out["overall_status"] == "detecting"


# ── the stall verdict is CORROBORATED, not a stopwatch ───────────────────────
# A bare duration cannot tell a wedged run from a big one. Calling a long
# legitimate run "stalled" cries wolf at exactly the customers with the most to
# scan, so duration is only half the evidence — worker liveness is the other half.

def _beat(minutes_ago: float):
    from datetime import datetime, timedelta, timezone
    return datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)


async def _running_run(minutes: float, heartbeat):
    from datetime import datetime, timedelta, timezone
    from app.models.detection_run import RUN_RUNNING
    a = uuid.uuid4()
    started = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    return await _progress([_job()], [_run(RUN_RUNNING, a, started_at=started)], [a],
                           heartbeat=heartbeat)


@pytest.mark.asyncio
async def test_a_long_run_with_a_live_worker_is_not_stalled():
    """THE CRY-WOLF CASE. 90 minutes in, worker heartbeating — this is a large
    scope being scanned, not a defect. Saying otherwise trains people to ignore
    the warning."""
    out = await _running_run(90, heartbeat=_beat(0.2))
    assert not any("without finishing" in r or "died mid-run" in r for r in out["reasons"])
    assert out["overall_status"] == "detecting"      # honest: still working


@pytest.mark.asyncio
async def test_a_dead_worker_is_called_out_quickly():
    """No patience needed when the thing that would finish the run has stopped
    heartbeating — waiting longer only delays the diagnosis."""
    out = await _running_run(5, heartbeat=_beat(30))
    assert any("stopped heartbeating" in r for r in out["reasons"]), out["reasons"]
    assert out["is_complete"] is False


@pytest.mark.asyncio
async def test_a_briefly_running_run_with_a_dead_worker_is_still_given_a_moment():
    """Under the floor: a heartbeat gap of a few seconds around a restart must not
    immediately be reported as a dead worker."""
    out = await _running_run(1, heartbeat=_beat(30))
    assert not any("stopped heartbeating" in r for r in out["reasons"])


@pytest.mark.asyncio
async def test_unknown_worker_liveness_falls_back_to_patience():
    """No heartbeat table (migration not yet run) — duration is all we have, so the
    threshold is generous and the wording hedges."""
    out_short = await _running_run(20, heartbeat=None)
    assert not any("without finishing" in r for r in out_short["reasons"])

    out_long = await _running_run(45, heartbeat=None)
    reason = next((r for r in out_long["reasons"] if "without finishing" in r), None)
    assert reason is not None
    assert "may still be legitimate" in reason      # hedged, not accusatory


@pytest.mark.asyncio
async def test_stall_never_claims_completion_either_way():
    """Whatever the verdict, a stalled run must not flip the campaign complete."""
    for hb in (_beat(0.2), _beat(30), None):
        out = await _running_run(45, heartbeat=hb)
        assert out["is_complete"] is False
        assert (out["percent"] == 100) == out["is_complete"]
