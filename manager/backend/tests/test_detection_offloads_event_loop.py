"""
The detection engine is synchronous CPU work; the outbox handler that runs it is
async. Calling it directly froze the worker's event loop for the whole run.

Measured on real facts replicated across hosts: 500 hosts (31,500 facts) takes
6.5s. For that entire time the worker cannot claim another event, renew anything,
or answer its reclaim sweep — and the reclaim lease is 5 minutes, so a big enough
engagement gets its event requeued and DETECTED TWICE while the first run is
still going.

Nothing about the engine changes. It just runs on a worker thread.
"""
from __future__ import annotations

import asyncio
import inspect
import time

import pytest

from app.detection import engine_bridge


@pytest.mark.asyncio
async def test_detection_runs_off_the_event_loop(monkeypatch):
    def _slow_engine(facts):
        time.sleep(0.3)                       # a real, blocking engine run
        return [], [], {"ran": True}

    monkeypatch.setattr(engine_bridge, "detect_all_from_facts_traced",
                        _slow_engine)

    ticks = {"n": 0}

    async def _heartbeat():
        while True:
            await asyncio.sleep(0.005)
            ticks["n"] += 1

    beat = asyncio.create_task(_heartbeat())
    await asyncio.sleep(0.01)
    try:
        _cve, _posture, meta = await engine_bridge._run_detection_engine(
            [{"scanner": "port_scan", "target": "10.0.0.1"}])
    finally:
        beat.cancel()

    assert meta["ran"] is True
    assert ticks["n"] >= 20, (
        f"the event loop only ticked {ticks['n']} times during a 0.3s detection "
        "run — it was blocked")


@pytest.mark.asyncio
async def test_an_empty_fact_list_still_returns_the_engine_result(monkeypatch):
    """The offload must not change the contract, including the trivial path."""
    monkeypatch.setattr(engine_bridge, "detect_all_from_facts_traced",
                        lambda facts: ([], [], {"coverage": {}}))

    cve, posture, meta = await engine_bridge._run_detection_engine([])

    assert (cve, posture) == ([], [])
    assert meta == {"coverage": {}}


def test_the_async_ingest_path_does_not_call_the_blocking_engine_directly():
    """A wiring guard: the seam only helps if the async caller uses it."""
    src = inspect.getsource(engine_bridge.create_findings_from_facts)

    assert "_run_detection_engine(" in src
    assert "detect_all_from_facts_traced(" not in src
