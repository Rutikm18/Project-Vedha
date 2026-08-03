from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.dialects import postgresql

from app.models.outbox import (
    OUTBOX_PENDING, OUTBOX_PROCESSING, OUTBOX_DONE, OUTBOX_FAILED,
)
from app.workers.outbox import (
    PROCESSING_LEASE_SEC,
    is_stale_processing,
    _stale_cutoff,
    _dead_letter_stale_stmt,
    _requeue_stale_stmt,
    _reclaim_stale,
)


def _sql(stmt) -> tuple[str, dict]:
    compiled = stmt.compile(dialect=postgresql.dialect())
    return str(compiled), dict(compiled.params)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def test_fresh_processing_lock_is_not_reclaimed() -> None:
    now = _now()
    locked_at = now - timedelta(seconds=5)  # a worker that just claimed the row
    assert is_stale_processing(OUTBOX_PROCESSING, locked_at, now) is False


def test_expired_processing_lock_is_reclaimed() -> None:
    now = _now()
    locked_at = now - timedelta(seconds=PROCESSING_LEASE_SEC + 1)
    assert is_stale_processing(OUTBOX_PROCESSING, locked_at, now) is True


def test_boundary_at_exactly_the_lease_is_reclaimed() -> None:
    now = _now()
    locked_at = now - timedelta(seconds=PROCESSING_LEASE_SEC)
    assert is_stale_processing(OUTBOX_PROCESSING, locked_at, now) is True


def test_pending_and_done_rows_are_never_reclaimed() -> None:
    now = _now()
    stale = now - timedelta(seconds=PROCESSING_LEASE_SEC + 60)
    # Only PROCESSING rows are candidates; PENDING/DONE must be left alone.
    assert is_stale_processing(OUTBOX_PENDING, stale, now) is False
    assert is_stale_processing(OUTBOX_DONE, stale, now) is False


def test_missing_locked_at_is_not_reclaimed() -> None:
    # A PROCESSING row with no locked_at is malformed; do not touch it blindly.
    assert is_stale_processing(OUTBOX_PROCESSING, None, _now()) is False


def test_stale_cutoff_is_now_minus_lease() -> None:
    now = _now()
    assert _stale_cutoff(now) == now - timedelta(seconds=PROCESSING_LEASE_SEC)
    assert _stale_cutoff(now, lease_sec=10) == now - timedelta(seconds=10)


# ── SQL builder correctness (compiled against the real Postgres dialect) ────────

def test_dead_letter_stmt_targets_exhausted_stranded_rows() -> None:
    sql, params = _sql(_dead_letter_stale_stmt(_now()))
    # Only PROCESSING rows past the lease whose attempts are exhausted.
    assert "outbox_events" in sql
    assert "outbox_events.status = " in sql            # WHERE status = PROCESSING
    assert "outbox_events.locked_at < " in sql          # WHERE locked_at < cutoff
    assert ">= outbox_events.max_attempts" in sql       # attempts >= max_attempts
    # Sets terminal FAILED status; does NOT make the row due again.
    assert OUTBOX_FAILED in params.values()
    assert OUTBOX_PROCESSING in params.values()
    assert "available_at" not in sql


def test_requeue_stmt_makes_retryable_stranded_rows_due_now() -> None:
    sql, params = _sql(_requeue_stale_stmt(_now()))
    assert "outbox_events.status = " in sql
    assert "outbox_events.locked_at < " in sql
    assert "< outbox_events.max_attempts" in sql        # attempts < max_attempts
    # Requeues to PENDING and resets availability to now() so a worker re-claims.
    assert OUTBOX_PENDING in params.values()
    assert OUTBOX_PROCESSING in params.values()
    assert "available_at=now()" in sql.replace(" ", "")


def test_dead_letter_and_requeue_are_mutually_exclusive() -> None:
    # The two sweeps must partition the stranded set (>= vs <) so no row is both
    # dead-lettered and requeued in one pass.
    dead_sql, _ = _sql(_dead_letter_stale_stmt(_now()))
    req_sql, _ = _sql(_requeue_stale_stmt(_now()))
    assert ">= outbox_events.max_attempts" in dead_sql
    assert "< outbox_events.max_attempts" in req_sql
    assert ">= outbox_events.max_attempts" not in req_sql


# ── Orchestration: _reclaim_stale runs both sweeps, commits, sums rowcounts ─────

def _mock_session(execute_side_effect):
    db = AsyncMock()
    db.execute = AsyncMock(side_effect=execute_side_effect)
    db.commit = AsyncMock()
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=db)
    cm.__aexit__ = AsyncMock(return_value=False)
    return db, cm


@pytest.mark.asyncio
async def test_reclaim_runs_both_sweeps_commits_and_sums_rowcounts() -> None:
    dead_res = MagicMock(rowcount=2)
    req_res = MagicMock(rowcount=3)
    db, cm = _mock_session([dead_res, req_res])
    with patch("app.workers.outbox.AsyncSessionLocal", return_value=cm):
        n = await _reclaim_stale()
    assert n == 5
    assert db.execute.await_count == 2      # dead-letter sweep + requeue sweep
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_reclaim_is_noop_when_nothing_is_stranded() -> None:
    db, cm = _mock_session([MagicMock(rowcount=0), MagicMock(rowcount=0)])
    with patch("app.workers.outbox.AsyncSessionLocal", return_value=cm):
        n = await _reclaim_stale()
    assert n == 0
    db.commit.assert_awaited_once()          # still a single clean transaction


@pytest.mark.asyncio
async def test_reclaim_handles_none_rowcount_from_driver() -> None:
    # Some drivers report rowcount as None for UPDATE; must not crash on `+`.
    db, cm = _mock_session([MagicMock(rowcount=None), MagicMock(rowcount=None)])
    with patch("app.workers.outbox.AsyncSessionLocal", return_value=cm):
        n = await _reclaim_stale()
    assert n == 0
