"""
Chunks are a buffer, so they have to disappear into the normal result exactly
once — and never leave the job reporting less than it actually scanned.

Two moments matter:

  * the job COMPLETES — its final submission is merged with any chunk the
    payload does not already cover, so the single scan_results row every
    consumer reads (detection, coverage, campaign progress) is unchanged in
    shape and complete in content;
  * the job DIES — attempts exhausted after a lease expiry, i.e. the probe never
    came back. That is the case the buffer exists for: the finished hosts are
    promoted into a scan_results row instead of being thrown away, and detection
    runs on them.

A host present in BOTH wins from the payload: it is the same host scanned by the
attempt that actually finished, so it is at least as fresh.
"""
from __future__ import annotations

import inspect
import uuid
from types import SimpleNamespace

import pytest

from app.models.scan_result import ScanResult
from app.models.scan_result_chunk import ScanResultChunk
from app.services import result_chunk_service as rcs

ENGAGEMENT = uuid.uuid4()
JOB = uuid.uuid4()


def _fact(host, port, scanner="port_scan", status="open"):
    return {"scanner": scanner, "target": host, "port": port, "proto": "tcp",
            "status": status}


def _chunk(host, facts):
    return ScanResultChunk(job_id=JOB, engagement_id=ENGAGEMENT, host=host,
                           facts=facts, fact_count=len(facts),
                           scan_type="network_va")


class _Rows:
    def __init__(self, rows):
        self._rows = list(rows)

    def scalars(self):
        rows = self._rows

        class _S:
            def all(self):
                return list(rows)
        return _S()

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None


class _FakeSession:
    def __init__(self, chunks=(), scan_results=()):
        self.chunks = list(chunks)
        self.scan_results = list(scan_results)
        self.added: list = []
        self.deleted: list = []
        self.executed: list = []

    async def execute(self, stmt):
        self.executed.append(stmt)
        desc = stmt.column_descriptions[0]["entity"] if stmt.column_descriptions else None
        if desc is ScanResultChunk:
            return _Rows(self.chunks)
        if desc is ScanResult:
            return _Rows(self.scan_results)
        return _Rows([])

    def add(self, obj):
        self.added.append(obj)

    async def delete(self, obj):
        self.deleted.append(obj)

    async def flush(self):
        pass


class TestMerge:
    def test_a_host_only_the_buffer_has_is_merged_in(self):
        payload = [_fact("10.0.0.1", 22)]
        chunks = [_chunk("10.0.0.2", [_fact("10.0.0.2", 445)])]

        facts, hosts = rcs.merge_chunk_facts(payload, chunks)

        assert {f["target"] for f in facts} == {"10.0.0.1", "10.0.0.2"}
        assert [h["ip"] for h in hosts] == ["10.0.0.2"]

    def test_the_final_payload_wins_for_a_host_it_already_covers(self):
        """Same host, two sources: the attempt that finished is at least as
        fresh, and duplicating its facts would double-count the evidence."""
        payload = [_fact("10.0.0.1", 22)]
        chunks = [_chunk("10.0.0.1", [_fact("10.0.0.1", 445)])]

        facts, hosts = rcs.merge_chunk_facts(payload, chunks)

        assert facts == payload
        assert hosts == []

    def test_merged_hosts_carry_their_open_ports(self):
        """Otherwise a rescued host lands with facts but no inventory."""
        chunks = [_chunk("10.0.0.2", [_fact("10.0.0.2", 445),
                                      _fact("10.0.0.2", 3389),
                                      _fact("10.0.0.2", 21, status="closed")])]

        _facts, hosts = rcs.merge_chunk_facts([], chunks)

        assert [p["port"] for p in hosts[0]["ports"]] == [445, 3389]

    def test_no_chunks_changes_nothing(self):
        payload = [_fact("10.0.0.1", 22)]

        facts, hosts = rcs.merge_chunk_facts(payload, [])

        assert facts == payload and hosts == []


class TestFinalSubmissionWiring:
    @pytest.mark.asyncio
    async def test_apply_merges_and_reports_what_it_added(self):
        db = _FakeSession(chunks=[_chunk("10.0.0.2", [_fact("10.0.0.2", 445)])])
        result = {"facts": [_fact("10.0.0.1", 22)], "hosts": [{"ip": "10.0.0.1"}]}

        merged = await rcs.apply_chunks_to_result(db, JOB, result)

        assert {f["target"] for f in merged["facts"]} == {"10.0.0.1", "10.0.0.2"}
        assert {h["ip"] for h in merged["hosts"]} == {"10.0.0.1", "10.0.0.2"}

    @pytest.mark.asyncio
    async def test_the_buffer_is_discarded_once_it_has_landed(self):
        db = _FakeSession(chunks=[_chunk("10.0.0.2", [])])

        removed = await rcs.discard_chunks(db, JOB)

        assert removed == 1 and len(db.deleted) == 1

    def test_the_result_path_merges_and_discards(self):
        """A buffer nothing drains is a leak; one nothing merges loses evidence."""
        from app.services.job_result_service import process_job_result
        src = inspect.getsource(process_job_result)

        assert "apply_chunks_to_result" in src
        assert "discard_chunks" in src


class TestPromotionOnFailure:
    @pytest.mark.asyncio
    async def test_a_dead_job_promotes_its_finished_hosts(self, monkeypatch):
        enqueued: list = []
        monkeypatch.setattr(rcs, "_enqueue_facts_ready",
                            lambda db, engagement_id, scan_result: enqueued.append(scan_result))
        db = _FakeSession(chunks=[_chunk("10.0.0.2", [_fact("10.0.0.2", 445)])])
        job = SimpleNamespace(id=JOB, engagement_id=ENGAGEMENT, result={})

        promoted = await rcs.promote_chunks_to_result(db, job)

        assert promoted == 1
        row = [o for o in db.added if isinstance(o, ScanResult)][0]
        assert row.job_id == JOB and row.fact_count == 1
        assert row.facts[0]["target"] == "10.0.0.2"
        assert enqueued, "detection never ran on the rescued evidence"
        assert db.deleted, "the buffer was not drained after promotion"

    @pytest.mark.asyncio
    async def test_a_job_that_already_reported_is_not_promoted_twice(self, monkeypatch):
        monkeypatch.setattr(rcs, "_enqueue_facts_ready", lambda *a, **k: None)
        db = _FakeSession(chunks=[_chunk("10.0.0.2", [])],
                          scan_results=[ScanResult(engagement_id=ENGAGEMENT,
                                                   job_id=JOB, facts=[],
                                                   fact_count=0)])
        job = SimpleNamespace(id=JOB, engagement_id=ENGAGEMENT, result={})

        promoted = await rcs.promote_chunks_to_result(db, job)

        assert promoted == 0
        assert [o for o in db.added if isinstance(o, ScanResult)] == []

    @pytest.mark.asyncio
    async def test_a_job_with_no_buffer_promotes_nothing(self, monkeypatch):
        monkeypatch.setattr(rcs, "_enqueue_facts_ready", lambda *a, **k: None)
        db = _FakeSession()
        job = SimpleNamespace(id=JOB, engagement_id=ENGAGEMENT, result={})

        assert await rcs.promote_chunks_to_result(db, job) == 0
        assert db.added == []

    def test_the_reaper_rescues_a_job_it_gives_up_on(self):
        from app.workers import reaper
        src = inspect.getsource(reaper.reap_once)

        assert "promote_chunks_to_result" in src
