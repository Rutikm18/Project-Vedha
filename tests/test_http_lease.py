from __future__ import annotations

import asyncio
import threading
import time
from types import SimpleNamespace

import pytest

from agent.agent import _poll_jobs_or_empty, _run_polled_job_with_heartbeats
from agent.transport import TransportError
from agent.engine import LeaseLostError, _run_with_cancellation


def test_transient_poll_failure_returns_no_jobs() -> None:
    class Transport:
        def poll_jobs(self, *, limit: int):
            raise ConnectionError("manager unavailable")

    assert _poll_jobs_or_empty(Transport(), 1) == []


def test_poll_auth_failure_is_not_hidden() -> None:
    class Transport:
        def poll_jobs(self, *, limit: int):
            raise TransportError("credential rejected")

    with pytest.raises(TransportError, match="credential rejected"):
        _poll_jobs_or_empty(Transport(), 1)


def test_polled_job_renews_lease_until_runner_finishes() -> None:
    heartbeats: list[tuple[str, str | None, str | None, int | None]] = []

    class Transport:
        def heartbeat(
            self,
            status: str,
            job_id: str | None,
            attempt_id: str | None,
            fence: int | None,
        ) -> bool:
            heartbeats.append((status, job_id, attempt_id, fence))
            return True

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
        def heartbeat(self, *args) -> bool:
            return False

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
