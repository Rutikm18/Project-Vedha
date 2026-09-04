from __future__ import annotations

import asyncio
import threading
import time
from types import SimpleNamespace

import pytest

from agent.agent import _poll_jobs_or_empty, _run_polled_job_with_heartbeats
from agent.transport import (
    HEARTBEAT_FAILED,
    HEARTBEAT_LEASE_REVOKED,
    HEARTBEAT_OK,
    TransportError,
)
from agent.engine import LeaseLostError, _run_with_cancellation


def test_transient_poll_failure_propagates_to_loop_handler() -> None:
    # A transient network failure is no longer swallowed here: it propagates to
    # the main loop's unified handler, which classifies it, backs off, and (after
    # a sustained streak) surfaces a diagnosed "Manager unreachable" message —
    # instead of silently returning [] and hot-looping.
    class Transport:
        def poll_jobs(self, *, limit: int):
            raise ConnectionError("manager unavailable")

    with pytest.raises(ConnectionError, match="manager unavailable"):
        _poll_jobs_or_empty(Transport(), 1)


def test_poll_auth_failure_is_not_hidden() -> None:
    class Transport:
        def poll_jobs(self, *, limit: int):
            raise TransportError("credential rejected")

    with pytest.raises(TransportError, match="credential rejected"):
        _poll_jobs_or_empty(Transport(), 1)


def test_polled_job_renews_lease_until_runner_finishes() -> None:
    heartbeats: list[tuple[str, str | None, str | None, int | None]] = []

    class Transport:
        def heartbeat_ex(
            self,
            status: str,
            job_id: str | None,
            attempt_id: str | None,
            fence: int | None,
        ) -> str:
            heartbeats.append((status, job_id, attempt_id, fence))
            return HEARTBEAT_OK

    class Runner:
        def run_job(self, job: dict, agent_id: str, cancellation_event=None):
            time.sleep(0.13)
            return SimpleNamespace(job_id=job["job_id"], error=None)

    result = _run_polled_job_with_heartbeats(
        Transport(),
        Runner(),
        {"job_id": "job-lease-test", "attempt_id": "attempt-1", "fence": 7},
        "agent-1",
        heartbeat_interval=0.05,
    )

    assert result.job_id == "job-lease-test"
    assert len(heartbeats) >= 2
    assert set(heartbeats) == {("busy", "job-lease-test", "attempt-1", 7)}


def test_repeated_lease_rejection_cancels_running_attempt(monkeypatch) -> None:
    monkeypatch.setenv("LEASE_LOSS_GRACE_HEARTBEATS", "2")

    class Transport:
        # A GENERIC failure (network, auth) — not a cancel. It must still take the
        # full grace budget before giving up, because it may be transient.
        def heartbeat_ex(self, *args) -> str:
            return HEARTBEAT_FAILED

    class Runner:
        def run_job(self, job: dict, agent_id: str, cancellation_event=None):
            assert cancellation_event is not None
            assert cancellation_event.wait(timeout=1.0)
            return SimpleNamespace(job_id=job["job_id"], error="lease lost")

    result = _run_polled_job_with_heartbeats(
        Transport(),
        Runner(),
        {"job_id": "job-lease-test", "attempt_id": "attempt-1", "fence": 7},
        "agent-1",
        heartbeat_interval=0.05,
    )

    assert result.error == "lease lost"


@pytest.mark.asyncio
async def test_engine_cancellation_stops_async_scan_work() -> None:
    cancelled = asyncio.Event()
    lease_lost = threading.Event()

    async def scan_work():
        try:
            await asyncio.sleep(10)
        finally:
            cancelled.set()

    task = asyncio.create_task(_run_with_cancellation(scan_work(), lease_lost))
    await asyncio.sleep(0)
    lease_lost.set()

    with pytest.raises(LeaseLostError):
        await asyncio.wait_for(task, timeout=1)
    assert cancelled.is_set()


def test_revoked_lease_cancels_the_attempt_immediately() -> None:
    """An operator cancel (409) is DEFINITIVE, unlike a flaky network.

    The grace budget exists so a transient failure doesn't kill a long scan. A
    revoked lease is not transient: the manager will reject our results whatever
    we do, so waiting out the budget just keeps hammering the target after the
    operator pressed stop. This asserts the very first revocation aborts.
    """
    monkeypatched_calls: list[str] = []

    class Transport:
        def heartbeat_ex(self, *args) -> str:
            monkeypatched_calls.append("hb")
            return HEARTBEAT_LEASE_REVOKED

    class Runner:
        def run_job(self, job: dict, agent_id: str, cancellation_event=None):
            assert cancellation_event is not None
            assert cancellation_event.wait(timeout=1.0), "cancel was never signalled"
            return SimpleNamespace(job_id=job["job_id"], error="cancelled")

    result = _run_polled_job_with_heartbeats(
        Transport(),
        Runner(),
        {"job_id": "job-cancel", "attempt_id": "attempt-1", "fence": 7},
        "agent-1",
        heartbeat_interval=0.05,
    )

    assert result.error == "cancelled"
    # ONE rejection was enough — no grace budget spent.
    assert len(monkeypatched_calls) == 1
