"""Per-run finding membership (detection_run_findings).

Run-level counts (findings_new/reaffirmed/current) can't answer "what did scan X
find" or diff two scans. `_record_run_membership` writes one row per finding a run
touched, derived from the finding rows' own run pointers AFTER every write so it is
exactly as consistent as the run itself:
  - detection_run_id == run.id  → created (first_seen == last_seen) or reaffirmed.
  - resolution_run_id == run.id → this run closed it (disjoint from the set above,
    since evaluate_resolutions only considers detection_run_id != run.id).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge
from app.models.detection_run_finding import (
    RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED, RUN_FINDING_RESOLVED,
)

_NOW = datetime(2026, 3, 1, 12, 0, tzinfo=timezone.utc)
# (severity, risk_score, status) as the finding row carries them.
_SNAP = ("high", 640, "open")


def _membership_db(touched_rows, resolved_ids):
    """A db whose two membership queries return, in order: the (id, first_seen,
    last_seen) rows for detection_run_id == run.id, then the resolved ids for
    resolution_run_id == run.id. Captures every row added."""
    added = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.execute = AsyncMock(side_effect=[
        MagicMock(all=lambda: touched_rows),
        MagicMock(scalars=lambda: MagicMock(all=lambda: resolved_ids)),
    ])
    return db, added


class TestClassification:
    @pytest.mark.asyncio
    async def test_new_reaffirmed_resolved_each_get_the_right_outcome(self):
        run = SimpleNamespace(id=uuid.uuid4())
        new_id, reaff_id, resolved_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        touched = [
            (new_id, _NOW, _NOW, *_SNAP),                   # created THIS run
            (reaff_id, _NOW - timedelta(days=7), _NOW, *_SNAP),  # carried over → reaffirmed
        ]
        db, added = _membership_db(touched, [resolved_id])

        await engine_bridge._record_run_membership(db, run)

        by_finding = {m.finding_id: m.outcome for m in added}
        assert by_finding == {
            new_id: RUN_FINDING_NEW,
            reaff_id: RUN_FINDING_REAFFIRMED,
            resolved_id: RUN_FINDING_RESOLVED,
        }
        assert all(m.run_id == run.id for m in added)

    @pytest.mark.asyncio
    async def test_a_touched_finding_is_snapshotted_as_this_scan_saw_it(self):
        """Severity, score and status are copied onto the membership row so a later
        diff can say what changed; a resolved row carries no snapshot."""
        run = SimpleNamespace(id=uuid.uuid4())
        fid, rid = uuid.uuid4(), uuid.uuid4()
        db, added = _membership_db([(fid, _NOW, _NOW, "critical", 911, "confirmed")], [rid])

        await engine_bridge._record_run_membership(db, run)

        by_finding = {m.finding_id: m for m in added}
        assert (by_finding[fid].severity, by_finding[fid].risk_score, by_finding[fid].status) == (
            "critical", 911, "confirmed")
        assert by_finding[rid].severity is None and by_finding[rid].risk_score is None

    @pytest.mark.asyncio
    async def test_first_seen_equal_last_seen_is_the_only_new_signal(self):
        """A reaffirm only advances last_seen; a created finding shares the run's
        one instant. Equality — not a run-id guess — is what separates them."""
        run = SimpleNamespace(id=uuid.uuid4())
        created, reaffirmed = uuid.uuid4(), uuid.uuid4()
        touched = [
            (created, _NOW, _NOW, *_SNAP),
            (reaffirmed, _NOW, _NOW + timedelta(seconds=1), *_SNAP),
        ]
        db, added = _membership_db(touched, [])

        await engine_bridge._record_run_membership(db, run)

        outcomes = {m.finding_id: m.outcome for m in added}
        assert outcomes[created] == RUN_FINDING_NEW
        assert outcomes[reaffirmed] == RUN_FINDING_REAFFIRMED

    @pytest.mark.asyncio
    async def test_no_findings_touched_records_nothing(self):
        run = SimpleNamespace(id=uuid.uuid4())
        db, added = _membership_db([], [])
        await engine_bridge._record_run_membership(db, run)
        assert added == []


class TestPipelineWiring:
    @pytest.mark.asyncio
    async def test_completed_run_records_membership(self):
        """create_findings_from_facts must stamp membership on the way to
        RUN_COMPLETED — otherwise a scan's finding set is never recoverable."""
        engagement_id = uuid.uuid4()
        result = {
            "facts": [{"scanner": "tls_scan", "target": "10.0.0.5:443", "status": "open"}],
            "scanner_runs": [{"id": "tls_scan", "status": "completed"}],
        }
        db = MagicMock()
        db.add = MagicMock()
        db.flush = AsyncMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

        with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
             patch.object(engine_bridge, "detect_all_from_facts_traced",
                          return_value=([], [], {"coverage": {}, "verdicts": {}})), \
             patch.object(engine_bridge, "evaluate_resolutions",
                          new=AsyncMock(return_value=0)), \
             patch.object(engine_bridge, "_record_run_membership",
                          new=AsyncMock()) as mock_membership:
            await engine_bridge.create_findings_from_facts(db, engagement_id, result)

        mock_membership.assert_awaited_once()
        # Called with the same DetectionRun the run wrote its status onto.
        run_arg = mock_membership.await_args.args[1]
        assert run_arg.status == engine_bridge.RUN_COMPLETED
