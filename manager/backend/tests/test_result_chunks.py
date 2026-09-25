"""
Per-host evidence must survive a probe that never gets to submit a result.

A job's facts reached the manager exactly once, at the end. If the probe process
died mid-scan — OOM-killed on a deep sweep, host rebooted, container evicted —
every host it had already finished died with it, the lease expired, and the retry
started from zero. Three attempts later the job failed having scanned the same
hosts three times and reported none of them.

A chunk is one HOST's facts, committed as soon as that host is done. It is a
buffer, not a second result path: the job still completes with one scan_results
row (the final submission, merged with any chunk the payload does not already
cover), so detection, coverage and campaign progress see exactly what they saw
before. What changes is that a job which never reaches its final submission still
has its finished hosts on the manager.

The safety properties of the result path apply here too — a chunk from a
superseded attempt is refused, and a chunk naming a host outside the job's
authorized scope is refused permanently.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest

from app.models.enums import ScanJobStatus
from app.models.scan_result_chunk import ScanResultChunk
from app.services.result_chunk_service import committed_hosts, process_result_chunk

ENGAGEMENT = uuid.uuid4()
JOB = uuid.uuid4()
AGENT = uuid.uuid4()
ATTEMPT = uuid.uuid4()
FENCE = 7
HOST = "10.20.0.8"


def _facts(host=HOST, port=445):
    return [{"scanner": "port_scan", "target": host, "port": port,
             "proto": "tcp", "status": "open"}]


def _job(status=ScanJobStatus.running, attempt_id=ATTEMPT, fence=FENCE):
    return SimpleNamespace(
        id=JOB, engagement_id=ENGAGEMENT, status=status,
        current_attempt_id=attempt_id, current_fence=fence,
        result={"_scope_cidrs": ["10.20.0.0/24"], "_excluded_cidrs": []},
    )


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
    def __init__(self, job=None, chunks=()):
        self.job = job
        self.chunks = list(chunks)
        self.added: list = []
        self.flushes = 0

    async def execute(self, stmt):
        entity = stmt.column_descriptions[0]["entity"]
        if entity is ScanResultChunk:
            wanted = set()
            for value in stmt.compile().params.values():
                wanted.add(value)
            return _Rows([c for c in self.chunks
                          if c.job_id in wanted
                          and (c.host in wanted or len(wanted) <= 2)])
        return _Rows([self.job] if self.job is not None else [])

    def add(self, obj):
        self.added.append(obj)
        self.chunks.append(obj)

    async def flush(self):
        self.flushes += 1


async def _send(db, **over):
    kwargs = dict(attempt_id=ATTEMPT, fence=FENCE, host=HOST,
                  facts=_facts(), scan_type="network_va")
    kwargs.update(over)
    return await process_result_chunk(db, AGENT, JOB, **kwargs)


class TestStoring:
    @pytest.mark.asyncio
    async def test_a_finished_host_is_committed(self):
        db = _FakeSession(job=_job())

        out = await _send(db)

        assert out["ok"] is True and out["stored"] is True
        chunk = db.added[0]
        assert chunk.host == HOST
        assert chunk.fact_count == 1
        assert chunk.facts[0]["port"] == 445

    @pytest.mark.asyncio
    async def test_the_same_chunk_twice_is_not_duplicated(self):
        """Delivery is at-least-once: the ACK can be lost after we committed."""
        db = _FakeSession(job=_job())

        first = await _send(db)
        second = await _send(db)

        assert first["stored"] is True
        assert second.get("duplicate") is True
        assert len(db.added) == 1

    @pytest.mark.asyncio
    async def test_a_rescan_of_the_same_host_replaces_its_facts(self):
        """A later attempt re-scanned the host; its evidence is the fresher one."""
        db = _FakeSession(job=_job())
        await _send(db)

        await _send(db, facts=_facts(port=3389))

        assert len(db.added) == 1                       # still one row per host
        assert db.added[0].facts[0]["port"] == 3389


class TestRefusals:
    @pytest.mark.asyncio
    async def test_a_superseded_attempt_cannot_commit(self):
        """Same fencing rule as the result path: a cancelled/reassigned attempt
        must not be able to write evidence."""
        db = _FakeSession(job=_job(fence=FENCE + 1))

        out = await _send(db)

        assert out["accepted"] is False and out["stale"] is True
        assert db.added == []

    @pytest.mark.asyncio
    async def test_a_terminal_job_accepts_no_more_evidence(self):
        db = _FakeSession(job=_job(status=ScanJobStatus.completed))

        out = await _send(db)

        assert out["ok"] is False and out["status_code"] == 409
        assert db.added == []

    @pytest.mark.asyncio
    async def test_a_host_outside_the_authorized_scope_is_refused(self):
        db = _FakeSession(job=_job())

        out = await _send(db, host="8.8.8.8", facts=_facts(host="8.8.8.8"))

        assert out["ok"] is False
        assert out["status_code"] == 422
        assert out["permanent_rejection"] is True
        assert db.added == []

    @pytest.mark.asyncio
    async def test_an_unknown_job_is_refused(self):
        db = _FakeSession(job=None)

        out = await _send(db)

        assert out["ok"] is False and db.added == []


class TestResume:
    @pytest.mark.asyncio
    async def test_committed_hosts_lists_what_the_manager_already_has(self):
        """What a retrying probe asks for so it does not rescan finished hosts."""
        db = _FakeSession(job=_job(), chunks=[
            ScanResultChunk(job_id=JOB, engagement_id=ENGAGEMENT, host="10.20.0.8",
                            facts=[], fact_count=0),
            ScanResultChunk(job_id=JOB, engagement_id=ENGAGEMENT, host="10.20.0.9",
                            facts=[], fact_count=0),
        ])

        assert await committed_hosts(db, JOB, agent_id=AGENT) == ["10.20.0.8", "10.20.0.9"]
