"""
The chunk endpoints are the probe's half of the buffer.

Thin on purpose: ownership check, delegate to the service, map its verdict onto
HTTP. The interesting rules (fencing, scope, idempotency) are the service's and
are tested in test_result_chunks.py — what matters here is that a refusal
REACHES the probe as the right status, because a probe that reads "permanently
rejected" stops retrying while one that reads 5xx keeps a chunk queued forever.
"""
from __future__ import annotations

import uuid
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.routers import agents as ag

AGENT = uuid.uuid4()
JOB = uuid.uuid4()
ATTEMPT = uuid.uuid4()


def _body(**over):
    payload = dict(attempt_id=ATTEMPT, fence=3, host="10.20.0.8",
                   facts=[{"scanner": "port_scan", "target": "10.20.0.8",
                           "port": 445, "status": "open"}],
                   scan_type="network_va")
    payload.update(over)
    return ag.JobResultChunkRequest(**payload)


@pytest.mark.asyncio
async def test_a_stored_chunk_is_acknowledged(monkeypatch):
    seen = {}

    async def _fake(db, agent_id, job_id, **kwargs):
        seen.update(kwargs)
        return {"ok": True, "stored": True}

    monkeypatch.setattr(ag, "_agent_ownership_check", lambda *a, **k: None)
    monkeypatch.setattr("app.services.result_chunk_service.process_result_chunk",
                        _fake)

    out = await ag.submit_result_chunk(AGENT, JOB, _body(), MagicMock(),
                                       MagicMock())

    assert out["stored"] is True
    assert seen["host"] == "10.20.0.8" and seen["fence"] == 3


@pytest.mark.asyncio
async def test_a_refusal_reaches_the_probe_with_its_status(monkeypatch):
    async def _fake(db, agent_id, job_id, **kwargs):
        return {"ok": False, "status_code": 422, "permanent_rejection": True,
                "error": "outside the authorized job scope"}

    monkeypatch.setattr(ag, "_agent_ownership_check", lambda *a, **k: None)
    monkeypatch.setattr("app.services.result_chunk_service.process_result_chunk",
                        _fake)

    with pytest.raises(HTTPException) as excinfo:
        await ag.submit_result_chunk(AGENT, JOB, _body(), MagicMock(), MagicMock())

    assert excinfo.value.status_code == 422


@pytest.mark.asyncio
async def test_a_stale_attempt_is_acknowledged_not_errored(monkeypatch):
    """A superseded attempt must stop retrying, so this is a 200 receipt."""
    async def _fake(db, agent_id, job_id, **kwargs):
        return {"ok": True, "accepted": False, "stale": True, "stored": False}

    monkeypatch.setattr(ag, "_agent_ownership_check", lambda *a, **k: None)
    monkeypatch.setattr("app.services.result_chunk_service.process_result_chunk",
                        _fake)

    out = await ag.submit_result_chunk(AGENT, JOB, _body(), MagicMock(),
                                       MagicMock())

    assert out["accepted"] is False and out["stale"] is True


@pytest.mark.asyncio
async def test_the_probe_can_ask_which_hosts_are_already_committed(monkeypatch):
    """What a retrying probe uses to skip hosts it already finished."""
    monkeypatch.setattr(ag, "_agent_ownership_check", lambda *a, **k: None)

    async def _hosts(db, job_id):
        return ["10.20.0.8", "10.20.0.9"]

    monkeypatch.setattr("app.services.result_chunk_service.committed_hosts",
                        _hosts)

    out = await ag.list_result_chunks(AGENT, JOB, MagicMock(), MagicMock())

    assert out == {"job_id": str(JOB), "hosts": ["10.20.0.8", "10.20.0.9"],
                   "count": 2}
