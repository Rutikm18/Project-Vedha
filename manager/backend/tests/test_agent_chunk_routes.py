"""
Per-host result chunks must reach the probe — and only its own jobs.

  * agent_jwt_path_allows() omitted both chunk routes, so the middleware 403'd
    every probe (legacy AND device tokens are role=agent) before the handler:
    mid-scan durability and resume were dead in production.
  * Opening them exposed a latent IDOR: committed_hosts() filtered by job_id
    alone, so any enrolled probe could list the finished-host IPs of ANY job in
    ANY tenant. The resume list is now scoped through ScanJob.agent_id, exactly
    as the POST path (process_result_chunk) already was.
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.dialects import postgresql

from app.auth.middleware import agent_jwt_path_allows
from app.routers import agents as ag
from app.services import result_chunk_service

CHUNKS = "/agents/7b0c2a1e-1111-4222-8333-944455556666/jobs/0a1b2c3d-1111-4222-8333-944455556666/chunks"


@pytest.mark.parametrize("method", ["GET", "POST"])
def test_agent_token_may_reach_chunk_routes(method):
    assert agent_jwt_path_allows(CHUNKS, method) is True


@pytest.mark.parametrize(("path", "method"), [
    (CHUNKS, "PUT"),
    (CHUNKS, "DELETE"),
    (CHUNKS + "/extra", "GET"),
    ("/agents/a/jobs/b/chunks/../../../engagements", "GET"),
    ("/agents/a/jobs/chunks", "GET"),
])
def test_chunk_allowlist_is_exact(path, method):
    assert agent_jwt_path_allows(path, method) is False


@pytest.mark.asyncio
async def test_resume_list_is_scoped_to_the_calling_agents_job():
    """The IDOR guard: the query must join through ScanJob.agent_id."""
    captured = {}

    async def execute(stmt):
        captured["sql"] = str(stmt.compile(dialect=postgresql.dialect()))
        return MagicMock(scalars=lambda: MagicMock(all=list))

    db = MagicMock()
    db.execute = AsyncMock(side_effect=execute)
    agent = uuid.uuid4()

    await result_chunk_service.committed_hosts(db, uuid.uuid4(), agent_id=agent)

    sql = captured["sql"]
    assert "JOIN scan_jobs" in sql
    assert "scan_jobs.agent_id" in sql


def test_committed_hosts_requires_agent_scope():
    """Required keyword, so no future caller can forget the ownership scope."""
    import inspect
    param = inspect.signature(result_chunk_service.committed_hosts).parameters["agent_id"]
    assert param.default is inspect.Parameter.empty
    assert param.kind is inspect.Parameter.KEYWORD_ONLY


@pytest.mark.asyncio
async def test_list_endpoint_passes_the_path_agent(monkeypatch):
    monkeypatch.setattr(ag, "_agent_ownership_check", lambda *a, **k: None)
    seen = {}

    async def _hosts(db, job_id, *, agent_id):
        seen["agent_id"] = agent_id
        return []

    monkeypatch.setattr(result_chunk_service, "committed_hosts", _hosts)
    agent, job = uuid.uuid4(), uuid.uuid4()

    await ag.list_result_chunks(agent, job, MagicMock(), MagicMock())

    assert seen["agent_id"] == agent
