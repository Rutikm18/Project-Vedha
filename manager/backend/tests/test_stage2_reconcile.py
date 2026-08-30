"""Stage 2 — reconciled campaign completion + worker liveness.

Proves the correctness properties the research's Stage 2 asks for:
  * completion is PROVEN by evidence coverage, so a multi-agent campaign is not
    'complete' while an earlier submission is still undetected (F11/F12);
  * a detection queue that isn't draining shows 'stalled', not a forever spinner (F2);
  * a dead-lettered facts event shows 'error';
  * a DetectionRun a crashed worker left RUNNING gets reaped to FAILED (F4).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.outbox import OUTBOX_PENDING, OUTBOX_PROCESSING, OUTBOX_FAILED
from app.routers import engagements as eng
from app.workers import outbox


def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


def _scalars(items):
    return MagicMock(scalars=lambda: MagicMock(all=lambda: items))


def _rows(items):
    return MagicMock(all=lambda: items)


def _job(status="completed"):
    return SimpleNamespace(
        id=uuid.uuid4(), job_type=SimpleNamespace(value="discovery"),
        status=SimpleNamespace(value=status), agent_id=None,
        result={"use_case_id": "uc_network_va"}, created_at=None,
        started_at=None, completed_at=None)


def _run(status="completed", scan_result_id=None, stats=None):
    return SimpleNamespace(
        id=uuid.uuid4(), status=status, facts_count=1, findings_new=0,
        findings_current=0, started_at=None, finished_at=None, error=None,
        scan_result_id=scan_result_id, stats=stats)


# ── the pure state machine (no DB) ────────────────────────────────────────────
_BASE = dict(jobs_exist=True, any_running=False, scanning_done=True,
             run_exists=True, latest_failed=False, detection_done=True,
             evidence_covered=True, has_gaps=False, queue_pending=False,
             queue_overdue=False, queue_dead=False)


@pytest.mark.parametrize("over,expect,complete", [
    ({"jobs_exist": False}, "pending", False),
    ({"any_running": True}, "scanning", False),
    ({"queue_dead": True}, "error", False),                       # dead-letter beats all runs
    ({"queue_pending": True, "queue_overdue": True}, "stalled", False),
    # worker heartbeat sharpens stalled: dead worker (alive=False) + pending → stalled
    # even before events go overdue; unknown (None) falls back to overdue-only.
    ({"queue_pending": True, "worker_alive": False}, "stalled", False),
    ({"queue_pending": True, "worker_alive": None}, "aggregating", False),
    ({"queue_pending": True, "worker_alive": True}, "aggregating", False),
    ({"queue_pending": True}, "aggregating", False),              # queued, draining
    ({"run_exists": False}, "aggregating", False),               # facts done, no run yet
    ({"latest_failed": True}, "error", False),
    ({"detection_done": False}, "detecting", False),
    ({"evidence_covered": False}, "detecting", False),           # ← F11/F12: uncovered submission
    ({"has_gaps": True}, "complete_with_gaps", True),
    ({}, "complete", True),
])
def test_reconcile_status_precedence(over, expect, complete):
    status, is_complete = eng._reconcile_status(**{**_BASE, **over})
    assert status == expect and is_complete is complete


def test_reconcile_dead_letter_wins_over_a_completed_run():
    # a completed+covered run still reports error if a facts event dead-lettered:
    # some submission genuinely never got detected.
    status, is_complete = eng._reconcile_status(**{**_BASE, "queue_dead": True})
    assert status == "error" and is_complete is False


# ── coverage-proven completion through campaign_progress (multi-agent) ─────────
@pytest.mark.asyncio
async def test_multi_agent_latest_done_but_earlier_uncovered_is_detecting():
    sr1, sr2 = uuid.uuid4(), uuid.uuid4()
    # latest run completed and covers sr1; sr2 has NO completed run yet.
    runs = [_run(status="completed", scan_result_id=sr1)]
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        _scalars([_job(), _job()]),                                              # jobs (2 probes)
        _scalars(runs),                                                          # runs (all)
        _scalars([sr1, sr2]),                                                    # scan_result ids
        _rows([]),                                                               # queue
        _scalars([]),                                                            # findings
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    # NOT complete — the premature-complete bug the single-run check had.
    assert out["overall_status"] == "detecting"
    assert out["is_complete"] is False
    assert out["evidence"]["submissions"] == 2 and out["evidence"]["covered"] == 1
    assert out["evidence"]["fully_covered"] is False
    assert any("awaiting detection" in r for r in out["reasons"])


@pytest.mark.asyncio
async def test_multi_agent_all_covered_is_complete():
    sr1, sr2 = uuid.uuid4(), uuid.uuid4()
    runs = [_run(status="completed", scan_result_id=sr2),
            _run(status="completed", scan_result_id=sr1)]
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job(), _job()]),
        _scalars(runs),
        _scalars([sr1, sr2]),
        _rows([]),
        _scalars([]),
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "complete" and out["is_complete"] is True
    assert out["evidence"]["fully_covered"] is True


@pytest.mark.asyncio
async def test_stalled_when_queue_overdue():
    old = datetime.now(timezone.utc) - timedelta(seconds=300)   # > _QUEUE_STALL_SEC
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job()]),                                      # jobs done
        _scalars([]),                                            # no runs yet
        _scalars([]),                                            # scan_result ids
        _rows([(OUTBOX_PENDING, old)]),                          # an overdue pending event
        _scalars([]),
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "stalled" and out["is_complete"] is False
    assert out["queue"]["overdue"] is True
    assert any("not draining" in r for r in out["reasons"])


@pytest.mark.asyncio
async def test_dead_lettered_facts_event_is_error():
    now = datetime.now(timezone.utc)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job()]),
        _scalars([]),
        _scalars([]),
        _rows([(OUTBOX_FAILED, now)]),
        _scalars([]),
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["overall_status"] == "error"
    assert out["queue"]["dead"] is True
    assert any("dead-lettered" in r for r in out["reasons"])


# ── the DetectionRun reaper ───────────────────────────────────────────────────
class _CM:
    def __init__(self, db): self._db = db
    async def __aenter__(self): return self._db
    async def __aexit__(self, *a): return False


@pytest.mark.asyncio
async def test_reap_stale_runs_marks_running_as_failed(monkeypatch):
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(rowcount=3))
    db.commit = AsyncMock()
    monkeypatch.setattr(outbox, "AsyncSessionLocal", lambda: _CM(db))
    n = await outbox._reap_stale_runs()
    assert n == 3
    db.execute.assert_awaited_once()
    db.commit.assert_awaited_once()


def test_reap_stmt_targets_running_detection_runs():
    now = datetime.now(timezone.utc)
    stmt = outbox._reap_runs_stmt(now, now - timedelta(seconds=600))
    sql = str(stmt).lower()
    # precise lease clause AND the started_at age fallback for legacy runs
    assert "detection_runs" in sql and "lease_expires_at" in sql and "started_at" in sql


@pytest.mark.asyncio
async def test_write_heartbeat_upserts(monkeypatch):
    db = MagicMock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    monkeypatch.setattr(outbox, "AsyncSessionLocal", lambda: _CM(db))
    await outbox._write_heartbeat("outbox")
    db.execute.assert_awaited_once()
    db.commit.assert_awaited_once()


# ── worker heartbeat sharpens stalled through campaign_progress ────────────────
def _hb(dt):
    return MagicMock(scalar_one_or_none=lambda: dt)


@pytest.mark.asyncio
async def test_fresh_heartbeat_reports_worker_alive():
    now = datetime.now(timezone.utc)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),  # get_or_404
        _scalars([_job()]),                                                      # jobs
        _scalars([_run(status="completed")]),                                    # runs
        _scalars([]),                                                            # scan_result ids
        _rows([]),                                                               # queue
        _scalars([]),                                                            # findings
        _hb(now),                                                                # heartbeat (fresh)
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["queue"]["worker_alive"] is True
    assert out["overall_status"] == "complete"


@pytest.mark.asyncio
async def test_stale_heartbeat_with_pending_is_stalled_before_overdue():
    now = datetime.now(timezone.utc)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=uuid.uuid4())),
        _scalars([_job()]),
        _scalars([]),                                            # no runs
        _scalars([]),                                            # scan_result ids
        _rows([(OUTBOX_PENDING, now)]),                          # pending but NOT overdue
        _scalars([]),                                            # findings
        _hb(now - timedelta(seconds=300)),                       # stale heartbeat → worker down
    ])
    out = await eng.campaign_progress(uuid.uuid4(), db, _user())
    assert out["queue"]["worker_alive"] is False
    assert out["overall_status"] == "stalled"          # caught BEFORE events aged out
