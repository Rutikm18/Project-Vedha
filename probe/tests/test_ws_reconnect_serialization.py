"""
A dropped WebSocket must not leave a second job-claiming loop behind.

The probe runs one job at a time. The push loop kept that promise per
CONNECTION: each connection had its own busy-state, lock, heartbeat task and
HTTP poll task, and the tasks were cleaned up only when the connection ended
normally. A connection that died with an exception — an API restart does
exactly that — left its poll task running with state nothing updated. That
task kept polling, believed the probe was idle, and ran the next job alongside
whatever the new connection was running.

A poll task that is mid-job must be told to stop, not cancelled: cancelling
the coroutine awaiting the scan's worker thread would mark the probe idle
while the scan kept going.
"""
from __future__ import annotations

import asyncio
import json
import threading
import time

import websockets.exceptions

from agent import agent as ag

JOB_SECONDS = 1.2


class _Clock:
    def __init__(self):
        self.t0 = time.monotonic()
        self.events: list[tuple[float, str]] = []

    def log(self, msg):
        self.events.append((round(time.monotonic() - self.t0, 2), msg))


class _WS:
    """A fake connection. With `die_after`, iterating it raises the error a
    server that went away produces."""

    def __init__(self, *, die_after=None):
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.acks: list[dict] = []
        self.die_after = die_after

    async def send(self, raw):
        msg = json.loads(raw)
        if msg.get("type") == "job_ack":
            self.acks.append(msg)
            if msg["accepted"]:
                await self.inbox.put(json.dumps({
                    "type": "job_claim", "job_id": msg["job_id"], "claimed": True,
                    "attempt_id": "att-" + msg["job_id"], "fence": 1}))

    async def recv(self):
        return await self.inbox.get()

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.die_after is not None:
            await asyncio.sleep(self.die_after)
            raise websockets.exceptions.ConnectionClosedError(None, None)
        return await self.inbox.get()

    async def close(self):
        pass


class _Spool:
    spool_count = 0
    at_capacity = False


class _Transport:
    agent_token = "t"

    def __init__(self, connections):
        self.connections = list(connections)
        self.pollable: list[dict] = []
        self.poll_times: list[float] = []

    async def connect_ws(self):
        ws = self.connections.pop(0)
        await ws.inbox.put(json.dumps(
            {"type": "hello_ok", "features": ["atomic_job_claim_v1"]}))
        return ws

    def poll_jobs(self, limit=1):
        self.poll_times.append(time.monotonic())
        return [self.pollable.pop(0)] if self.pollable else []

    def heartbeat_ex(self, *a, **k):
        return ag.HEARTBEAT_OK

    def submit_result(self, *a, **k):
        return True


class _Runner:
    def __init__(self, clock):
        self.clock = clock
        self.live = 0
        self.peak = 0
        self._lock = threading.Lock()

    def run_job(self, job, agent_id, cancellation_event=None):
        with self._lock:
            self.live += 1
            self.peak = max(self.peak, self.live)
        self.clock.log(f"start {job['job_id']}")
        time.sleep(JOB_SECONDS)
        with self._lock:
            self.live -= 1
        self.clock.log(f"end {job['job_id']}")

        class _Result:
            error = None
        return _Result()


def _quiet(monkeypatch):
    monkeypatch.setattr(ag, "say", lambda *a, **k: None)
    monkeypatch.setattr(ag, "_result_summary", lambda r: "ok")
    monkeypatch.setattr(ag, "WS_RECONNECT_BACKOFF_MIN", 0.1)


async def _stop(loop_task):
    loop_task.cancel()
    try:
        await loop_task
    except asyncio.CancelledError:
        pass


def test_a_reconnect_does_not_leave_a_second_claimer(monkeypatch):
    """The field sequence: the socket drops, the probe reconnects, job A is
    pushed, and job B becomes pollable while A runs. B must wait for A."""
    _quiet(monkeypatch)
    clock = _Clock()
    runner = _Runner(clock)
    live_ws = _WS()
    transport = _Transport([_WS(die_after=0.05), live_ws])

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, runner, "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(1.5)
        await live_ws.inbox.put(json.dumps(
            {"type": "job_push", "job": {"job_id": "A", "params": {}}}))
        await asyncio.sleep(0.3)
        transport.pollable.append({"job_id": "B", "params": {}})
        await asyncio.sleep(JOB_SECONDS * 2 + 2.5)
        await _stop(loop)

    asyncio.run(scenario())
    assert runner.peak == 1, clock.events
    starts = {m.split()[1]: t for t, m in clock.events if m.startswith("start")}
    ends = {m.split()[1]: t for t, m in clock.events if m.startswith("end")}
    assert set(starts) == {"A", "B"}, clock.events
    assert starts["B"] >= ends["A"], clock.events


def test_a_job_running_when_the_socket_drops_still_makes_the_probe_busy(monkeypatch):
    """The poll fallback is running B when the socket dies. The next
    connection must see a busy probe and decline a push for A."""
    _quiet(monkeypatch)
    clock = _Clock()
    runner = _Runner(clock)
    live_ws = _WS()
    transport = _Transport([_WS(die_after=1.6), live_ws])
    transport.pollable.append({"job_id": "B", "params": {}})

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, runner, "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(2.0)       # B taken at ~1s, socket died at ~1.6s
        await live_ws.inbox.put(json.dumps(
            {"type": "job_push", "job": {"job_id": "A", "params": {}}}))
        await asyncio.sleep(JOB_SECONDS + 1.5)
        await _stop(loop)

    asyncio.run(scenario())
    assert runner.peak == 1, clock.events
    assert live_ws.acks, "the push for A was never answered"
    assert live_ws.acks[0]["job_id"] == "A"
    assert live_ws.acks[0]["accepted"] is False, live_ws.acks


def test_reconnects_do_not_multiply_the_pollers(monkeypatch):
    """Every leaked poll task added another claimer — and another request
    against the manager every interval."""
    _quiet(monkeypatch)
    clock = _Clock()
    transport = _Transport([_WS(die_after=0.05) for _ in range(3)] + [_WS()])

    async def scenario():
        loop = asyncio.create_task(ag._run_ws_push_loop(
            transport, _Runner(clock), "agent-1", _Spool(), 30, 1))
        await asyncio.sleep(1.5)
        before = len(transport.poll_times)
        await asyncio.sleep(3.0)
        window = len(transport.poll_times) - before
        await _stop(loop)
        return window

    window = asyncio.run(scenario())
    assert window <= 4, f"{window} polls in 3s at a 1s interval — pollers are piling up"
