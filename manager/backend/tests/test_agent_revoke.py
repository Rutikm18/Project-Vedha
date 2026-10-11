"""Revoking an agent from Fleet: cut off for good, nothing deleted.

Before this there was only an access-expiry date: no way to say "this machine is lost / retired / compromised,
never accept it again". The enforcement side already existed (the HTTP middleware and the WebSocket endpoint
refuse any agent whose lifecycle_status is not `active`); what was missing was something that sets it, and a way
to close a socket that is ALREADY open (it never passes the HTTP authentication again).
"""
from __future__ import annotations

import asyncio
import json
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.agent import AgentStatus
from app.routers import agents as agents_router
from app.schemas.auth import CurrentUser
from app.websocket.manager import AgentConnectionManager


def _operator():
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role="admin", email="op@example.com")


def _agent(user, **kw):
    base = dict(id=uuid.uuid4(), tenant_id=user.tenant_id, lifecycle_status="active", credential_generation=4,
                status=AgentStatus.busy, current_job_id=uuid.uuid4())
    base.update(kw)
    return SimpleNamespace(**base)


def _db(agent, released=()):
    """execute() is called in a fixed order: find the agent, revoke credentials, list engagements, release them."""
    db = MagicMock()

    def result(**attrs):
        r = MagicMock()
        r.scalar_one_or_none = MagicMock(return_value=attrs.get("one"))
        scalars = MagicMock()
        scalars.all = MagicMock(return_value=list(attrs.get("many", [])))
        r.scalars = MagicMock(return_value=scalars)
        return r

    sequence = [result(one=agent)]
    if agent is not None:
        sequence += [result(), result(many=released)]
        if released:
            sequence.append(result())
    db.execute = AsyncMock(side_effect=sequence)
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.commit = AsyncMock()
    return db


def _redis():
    r = MagicMock()
    r.publish = AsyncMock()
    return r


def _revoke(agent, user, *, released=(), reason=None, db=None, redis=None, monkeypatch=None):
    db = db or _db(agent, released)
    redis = redis or _redis()
    return asyncio.run(agents_router.revoke_agent(
        agent.id if agent else uuid.uuid4(), agents_router.AgentRevoke(reason=reason), db, redis, user)), db, redis


@pytest.fixture(autouse=True)
def _no_real_sockets(monkeypatch):
    from app.websocket import manager as ws
    monkeypatch.setattr(ws.agent_ws_manager, "revoke_connection", AsyncMock(return_value=True))


def test_revoking_cuts_the_agent_off_and_moves_its_credential_on():
    user = _operator()
    agent = _agent(user)
    out, db, _ = _revoke(agent, user)
    assert agent.lifecycle_status == "revoked"
    assert agent.credential_generation == 5                   # tokens it holds are now stale
    assert agent.status == AgentStatus.offline and agent.current_job_id is None
    assert out["lifecycle_status"] == "revoked" and out["already_revoked"] is False
    db.commit.assert_awaited()


def test_a_running_job_is_left_for_the_reaper_not_touched_here():
    # The job's own rows are not updated by the endpoint: the dead agent stops renewing the lease and the
    # reaper requeues (or fails) the job. Only agent, credential and engagement rows are written.
    user = _operator()
    _, db, _ = _revoke(_agent(user), user)
    statements = [str(call.args[0]).lower() for call in db.execute.await_args_list]
    assert not any("scan_jobs" in s for s in statements), statements
    assert any("agent_credentials" in s for s in statements)


def test_its_stored_credentials_are_revoked_so_it_cannot_mint_a_new_token():
    user = _operator()
    _, db, _ = _revoke(_agent(user), user)
    update = [str(call.args[0]) for call in db.execute.await_args_list if "agent_credentials" in str(call.args[0]).lower()]
    assert update and "revoked_at" in update[0].lower()


def test_engagements_assigned_to_it_are_released_so_a_replacement_can_enrol():
    user = _operator()
    eng = uuid.uuid4()
    out, db, _ = _revoke(_agent(user), user, released=[eng])
    assert out["released_engagements"] == [str(eng)]
    assert any("engagements" in str(c.args[0]).lower() and "update" in str(c.args[0]).lower()
               for c in db.execute.await_args_list)


def test_the_revocation_is_audited_with_who_why_and_what_it_was_doing():
    user = _operator()
    agent = _agent(user)
    _, db, _ = _revoke(agent, user, reason="  laptop lost  ")
    row = db.add.call_args.args[0]
    assert row.action == "agent.revoked" and row.resource_id == agent.id
    assert row.actor_id == str(user.user_id)
    assert row.detail["reason"] == "laptop lost"
    assert row.detail["previous"]["lifecycle_status"] == "active"
    assert row.detail["previous"]["current_job_id"] is not None


def test_the_open_websocket_is_closed_through_the_manager():
    from app.websocket import manager as ws
    user = _operator()
    agent = _agent(user)
    redis = _redis()
    out, _, _ = _revoke(agent, user, redis=redis)
    ws.agent_ws_manager.revoke_connection.assert_awaited_once()
    assert ws.agent_ws_manager.revoke_connection.await_args.args[1] == str(agent.id)
    assert out["disconnected"] is True


def test_revoking_twice_is_harmless_and_changes_nothing():
    user = _operator()
    agent = _agent(user, lifecycle_status="revoked", credential_generation=9)
    out, db, _ = _revoke(agent, user)
    assert out["already_revoked"] is True
    assert agent.credential_generation == 9
    assert db.execute.await_count == 1                       # it only looked the agent up
    db.add.assert_not_called()


def test_another_tenants_agent_is_a_404():
    user = _operator()
    with pytest.raises(HTTPException) as exc:
        _revoke(None, user)
    assert exc.value.status_code == 404


def test_only_admins_and_managers_may_revoke():
    route = next(r for r in agents_router.router.routes if getattr(r, "path", "") == "/agents/{agent_id}/revoke")
    assert "POST" in route.methods
    checks = [d.call for d in route.dependant.dependencies if d.call.__name__ == "_check"]
    assert len(checks) == 1, "the endpoint must carry exactly one role check"
    check = checks[0]
    for role in ("admin", "manager"):
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role=role, email="x@example.com")
        assert asyncio.run(check(user)) is user
    for role in ("viewer", "tester", "client"):
        user = CurrentUser(user_id=uuid.uuid4(), tenant_id=uuid.uuid4(), role=role, email="x@example.com")
        with pytest.raises(HTTPException) as denied:
            asyncio.run(check(user))
        assert denied.value.status_code == 403, role


# ── closing a socket that is already open ────────────────────────────────────

class _Socket:
    def __init__(self):
        self.sent, self.closed = [], None

    async def send_json(self, message):
        self.sent.append(message)

    async def close(self, code=1000, reason=""):
        self.closed = (code, reason)


def test_disconnect_closes_and_forgets_a_local_socket():
    async def go():
        manager = AgentConnectionManager()
        sock = _Socket()
        await manager.register("a1", "t1", sock)
        assert await manager.disconnect_agent("a1", reason="This agent was revoked in Fleet.") is True
        assert sock.sent == [{"type": "revoked", "message": "This agent was revoked in Fleet."}]
        assert sock.closed[0] == 4003
        assert not manager.is_connected("a1")
        return await manager.disconnect_agent("a1", reason="x")
    assert asyncio.run(go()) is False                          # nothing left to close


def test_a_long_reason_never_breaks_the_close_frame():
    async def go():
        manager = AgentConnectionManager()
        sock = _Socket()
        await manager.register("a1", "t1", sock)
        await manager.disconnect_agent("a1", reason="é" * 200)
        return sock.closed[1]
    assert len(asyncio.run(go()).encode("utf-8")) <= 123       # the WebSocket limit


def test_a_socket_on_another_worker_is_closed_through_the_backplane():
    async def go():
        manager = AgentConnectionManager()
        redis = _redis()
        closed_here = await manager.revoke_connection(redis, "a1", "revoked")
        return closed_here, redis.publish.await_args.args
    closed_here, (channel, payload) = asyncio.run(go())
    assert closed_here is False
    assert channel == AgentConnectionManager._BACKPLANE_CHANNEL
    assert json.loads(payload) == {"action": "disconnect", "agent_id": "a1", "reason": "revoked"}


def test_the_worker_that_holds_the_socket_acts_on_the_backplane_message_and_the_others_ignore_it():
    async def go():
        holder, other = AgentConnectionManager(), AgentConnectionManager()
        sock = _Socket()
        await holder.register("a1", "t1", sock)
        message = {"action": "disconnect", "agent_id": "a1", "reason": "revoked"}
        await other._handle_backplane_message(message)
        untouched = sock.closed is None
        await holder._handle_backplane_message(message)
        return untouched, sock.closed
    untouched, closed = asyncio.run(go())
    assert untouched and closed[0] == 4003


def test_a_job_push_message_is_still_handled_as_before():
    async def go():
        manager = AgentConnectionManager()
        manager.push_job = AsyncMock(return_value=True)
        sock = _Socket()
        await manager.register("a1", "t1", sock)
        await manager._handle_backplane_message({"agent_id": "a1", "job": {"job_id": "j"}, "required_feature": "f"})
        return manager.push_job.await_args
    call = asyncio.run(go())
    assert call.args == ("a1", {"job_id": "j"}) and call.kwargs == {"required_feature": "f"}
