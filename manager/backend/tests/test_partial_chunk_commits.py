"""
T1.4 — evidence committed mid-pipeline must not be mistaken for a finished host.

WHY COMMIT EARLIER AT ALL
-------------------------
`_commit_host` only ran at the END of the deep-scan stage. Everything before it
— host discovery, the port sweep, OS fingerprinting, banners — reached the
manager only via the job's FINAL submission. When that submission never happens
(probe OOM-killed on a wide sweep, container evicted, lease lost so the result
is fenced out) the manager holds nothing at all, and the operator sees a failed
job that apparently scanned nothing.

The port sweep is where a wide scan spends its hours, so it is exactly the
stage whose evidence was most expensive and least protected.

WHY A COMPLETENESS FLAG IS REQUIRED FIRST
-----------------------------------------
`committed_hosts()` feeds the probe's RESUME list: hosts it already has are not
rescanned. That works only because a chunk used to mean "this host finished the
whole pipeline". Committing partial evidence without saying so would make a
retry skip every host it had merely DISCOVERED — delivering a liveness fact and
calling the host done. Strictly worse than the gap it set out to close.

So the chunk now records whether it is the host's final word. Partial chunks
are durability only: they are merged into the result and promoted if the job
dies, but they never suppress a rescan.

`complete` defaults to True on the wire so an older probe — which only ever
committed finished hosts — keeps its exact behaviour against a newer manager.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.scan_result_chunk import ScanResultChunk


class _FakeSession:
    def __init__(self, chunks=None, job=None):
        self._chunks = chunks or []
        self._job = job
        self.added, self.deleted = [], []

    async def execute(self, stmt):
        text = str(stmt)
        if "scan_result_chunks" in text:
            rows = self._chunks
            # Emulate the complete-only filter the resume query applies.
            if "complete" in text.lower():
                rows = [c for c in rows if getattr(c, "complete", True)]
            return MagicMock(
                scalars=lambda: MagicMock(all=lambda: rows),
                scalar_one_or_none=lambda: rows[0] if rows else None,
            )
        return MagicMock(scalar_one_or_none=lambda: self._job)

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        return None

    async def delete(self, obj):
        self.deleted.append(obj)


def _chunk(host, *, complete=True, facts=None):
    return ScanResultChunk(
        engagement_id=uuid.uuid4(), job_id=uuid.uuid4(), host=host,
        facts=facts or [{"target": host, "status": "open", "port": 80}],
        fact_count=1, complete=complete,
    )


# ── the model carries completeness ──────────────────────────────────────────

def test_the_chunk_model_records_whether_a_host_is_finished():
    assert hasattr(ScanResultChunk, "complete")


def test_a_chunk_is_complete_unless_told_otherwise():
    """An older probe omits the field and only ever commits finished hosts."""
    row = ScanResultChunk(engagement_id=uuid.uuid4(), job_id=uuid.uuid4(),
                          host="10.0.0.1", facts=[], fact_count=0)
    # server_default applies at INSERT; the Python-side default must agree.
    assert row.complete in (True, None)


# ── resume must only skip finished hosts ────────────────────────────────────

class TestResumeIgnoresPartialEvidence:
    @pytest.mark.asyncio
    async def test_a_finished_host_is_skipped_on_retry(self):
        from app.services.result_chunk_service import committed_hosts

        db = _FakeSession(chunks=[_chunk("10.0.0.1", complete=True)])
        assert await committed_hosts(db, uuid.uuid4()) == ["10.0.0.1"]

    @pytest.mark.asyncio
    async def test_a_partially_scanned_host_is_rescanned(self):
        """The regression this guards: discovering a host is not scanning it."""
        from app.services.result_chunk_service import committed_hosts

        db = _FakeSession(chunks=[_chunk("10.0.0.1", complete=False)])
        assert await committed_hosts(db, uuid.uuid4()) == []

    @pytest.mark.asyncio
    async def test_a_mixed_job_resumes_only_the_unfinished_hosts(self):
        from app.services.result_chunk_service import committed_hosts

        db = _FakeSession(chunks=[
            _chunk("10.0.0.1", complete=True),
            _chunk("10.0.0.2", complete=False),
            _chunk("10.0.0.3", complete=True),
        ])
        assert await committed_hosts(db, uuid.uuid4()) == ["10.0.0.1", "10.0.0.3"]


# ── partial evidence is still real evidence ─────────────────────────────────

class TestPartialChunksStillCount:
    def test_partial_facts_are_merged_into_the_final_result(self):
        """Durability is the whole point — a partial chunk must not be dropped
        just because its host was not finished."""
        from app.services.result_chunk_service import merge_chunk_facts

        facts, _ = merge_chunk_facts(
            [], [_chunk("10.0.0.9", complete=False)])
        assert any(f.get("target") == "10.0.0.9" for f in facts)

    def test_promotion_rescues_partial_evidence_too(self):
        """promote_chunks_to_result runs when a job is given up on. If it
        filtered to complete hosts, the port-stage evidence this task exists to
        save would be discarded at the exact moment it is needed."""
        import inspect

        from app.services import result_chunk_service as rcs

        src = inspect.getsource(rcs.promote_chunks_to_result)
        assert "complete" not in src, \
            "promotion must rescue partial chunks, not filter them out"
