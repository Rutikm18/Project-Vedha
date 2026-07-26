from __future__ import annotations

import time
from types import SimpleNamespace

from agent.agent import _run_polled_job_with_heartbeats


def test_polled_job_renews_lease_until_runner_finishes() -> None:
    heartbeats: list[tuple[str, str | None]] = []

    class Transport:
        def heartbeat(self, status: str, job_id: str | None) -> bool:
            heartbeats.append((status, job_id))
            return True

    class Runner:
        def run_job(self, job: dict, agent_id: str):
            time.sleep(0.13)
            return SimpleNamespace(job_id=job["job_id"], error=None)

    result = _run_polled_job_with_heartbeats(
        Transport(),
        Runner(),
        {"job_id": "job-lease-test"},
        "agent-1",
        heartbeat_interval=0.05,
    )

    assert result.job_id == "job-lease-test"
    assert len(heartbeats) >= 2
    assert set(heartbeats) == {("busy", "job-lease-test")}
