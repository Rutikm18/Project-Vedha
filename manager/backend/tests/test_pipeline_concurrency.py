"""
test_pipeline_concurrency.py — the two correctness fixes from ADR-0001.

R1: the outbox worker processes a claimed batch with asyncio.gather, so two
    facts.ready events for the SAME engagement run detection concurrently. Dedup
    is a read-then-write with no unique constraint underneath, so both passes
    read "absent" and both insert — one issue, two rows, and every count built on
    findings (open totals, posture, SLA) is then wrong.

R2: an outbox is at-least-once. The handler commits, then _mark_done commits
    separately; a crash between leaves the event PROCESSING and it is redelivered.
    Detecting the same submission twice adds a phantom DetectionRun, which
    campaign coverage counts.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge as EB
from app.workers import outbox as OB


# ── R1: the critical section ─────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_detection_locks_the_engagement_before_reading_anything():
    """The lock must be taken BEFORE the first read, or the race it prevents can
    still happen in the window before it."""
    eng = uuid.uuid4()
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock())
    await EB._lock_engagement_for_detection(db, eng)

    sql = str(db.execute.await_args.args[0])
    assert "pg_advisory_xact_lock" in sql
    assert db.execute.await_args.args[1]["k"] >= 0


@pytest.mark.asyncio
async def test_the_lock_is_transaction_scoped_not_session_scoped():
    """pg_advisory_lock (session) would leak on any path that forgets to unlock.
    The xact variant releases on COMMIT *and* ROLLBACK, so a failed detection
    cannot strand an engagement."""
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock())
    await EB._lock_engagement_for_detection(db, uuid.uuid4())
    sql = str(db.execute.await_args.args[0])
    assert "pg_advisory_xact_lock" in sql
    assert "pg_advisory_lock(" not in sql


@pytest.mark.asyncio
async def test_the_same_engagement_always_maps_to_the_same_key():
    """Two concurrent handlers must contend, so the key has to be a pure function
    of the engagement."""
    eng = uuid.uuid4()
    keys = []
    for _ in range(2):
        db = MagicMock(); db.execute = AsyncMock(return_value=MagicMock())
        await EB._lock_engagement_for_detection(db, eng)
        keys.append(db.execute.await_args.args[1]["k"])
    assert keys[0] == keys[1]


@pytest.mark.asyncio
async def test_different_engagements_generally_do_not_contend():
    """Collisions are harmless (two unrelated engagements briefly serialise) but
    should be rare, or the lock becomes a global one."""
    keys = set()
    for _ in range(5000):
        db = MagicMock(); db.execute = AsyncMock(return_value=MagicMock())
        await EB._lock_engagement_for_detection(db, uuid.uuid4())
        keys.add(db.execute.await_args.args[1]["k"])
    assert len(keys) >= 4995, f"only {len(keys)} distinct keys from 5000 engagements"


@pytest.mark.asyncio
async def test_the_key_fits_a_postgres_bigint():
    """pg_advisory_xact_lock takes a signed bigint; an out-of-range key raises."""
    for _ in range(1000):
        db = MagicMock(); db.execute = AsyncMock(return_value=MagicMock())
        await EB._lock_engagement_for_detection(db, uuid.uuid4())
        k = db.execute.await_args.args[1]["k"]
        assert 0 <= k <= 0x7FFFFFFFFFFFFFFF


# ── R2: redelivery must not re-detect ────────────────────────────────────────

def _event(scan_result_id):
    return SimpleNamespace(id=str(uuid.uuid4()), topic="facts.ready",
                           engagement_id=str(uuid.uuid4()),
                           scan_result_id=str(scan_result_id),
                           payload={}, attempts=1)


def _db_with(scan_result, existing_run):
    db = MagicMock()
    db.get = AsyncMock(return_value=scan_result)
    db.execute = AsyncMock(return_value=MagicMock(first=lambda: existing_run))
    db.commit = AsyncMock()
    db.__aenter__ = AsyncMock(return_value=db)
    db.__aexit__ = AsyncMock(return_value=False)
    return db


@pytest.mark.asyncio
async def test_a_redelivered_submission_is_not_detected_twice():
    sr_id = uuid.uuid4()
    # job_id is part of the real ScanResult (the handler reads it to recover the
    # job's scanner_runs for coverage); None here = an older submission with none.
    sr = SimpleNamespace(id=sr_id, engagement_id=uuid.uuid4(), job_id=None,
                         facts=[{"scanner": "x"}])
    db = _db_with(sr, existing_run=(uuid.uuid4(),))      # a completed run exists
    create = AsyncMock(return_value=3)

    with patch.object(OB, "AsyncSessionLocal", return_value=db), \
         patch("app.detection.engine_bridge.create_findings_from_facts", create):
        await OB._handle_facts_ready(_event(sr_id))

    assert create.await_count == 0, "detection re-ran for an already-detected submission"


@pytest.mark.asyncio
async def test_a_first_delivery_still_runs_detection():
    """The guard must not swallow real work."""
    sr_id = uuid.uuid4()
    # job_id is part of the real ScanResult (the handler reads it to recover the
    # job's scanner_runs for coverage); None here = an older submission with none.
    sr = SimpleNamespace(id=sr_id, engagement_id=uuid.uuid4(), job_id=None,
                         facts=[{"scanner": "x"}])
    db = _db_with(sr, existing_run=None)                 # no completed run yet
    create = AsyncMock(return_value=3)

    with patch.object(OB, "AsyncSessionLocal", return_value=db), \
         patch("app.detection.engine_bridge.create_findings_from_facts", create), \
         patch("app.detection.prioritization.prioritize_engagement_findings", AsyncMock()):
        await OB._handle_facts_ready(_event(sr_id))

    assert create.await_count == 1


@pytest.mark.asyncio
async def test_a_missing_submission_is_not_an_error():
    """Pre-existing behaviour: a vanished scan_result logs and returns rather
    than throwing the event into the retry/dead-letter path forever."""
    db = _db_with(scan_result=None, existing_run=None)
    with patch.object(OB, "AsyncSessionLocal", return_value=db):
        await OB._handle_facts_ready(_event(uuid.uuid4()))   # must not raise
