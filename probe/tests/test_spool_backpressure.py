"""
B4 — a probe that has stopped accepting work must say so, on every path.

TWO DEFECTS, ONE CAUSE
----------------------
`ResultSpool.at_capacity` is the probe's back-pressure: once pending results
hit the high-water mark, taking on more work just produces more undeliverable
results. It was checked in exactly ONE place — the HTTP-only poll loop:

    if spool.at_capacity: say("...pausing new jobs until uploads recover.")
    else:                 jobs = _poll_jobs_or_empty(...)

1. THE WEBSOCKET PATH IGNORED IT ENTIRELY. WS push is the default
   (PROBE_WS_ENABLED=true), and neither `_ws_stage_job_offer` nor
   `_ws_http_poll_fallback` consulted the spool. So on the path most
   deployments actually run, a probe with a full spool kept claiming jobs and
   kept adding to the pile. The back-pressure existed and was wired to the
   path least used.

2. THE PAUSE WAS INVISIBLE. The probe still heartbeats `online`, so the
   manager sees a healthy idle probe and keeps pushing jobs at it (push_job
   only skips agents whose status is not "online"). From the fleet view,
   "paused indefinitely" and "idle, ready for work" look identical.

Reporting `paused` fixes both halves of the second problem at once: the
operator sees the real state, AND the manager stops dispatching to a probe
that cannot take the work.
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock

import pytest

from agent import agent as ag


class _Spool:
    def __init__(self, at_capacity=False, count=0, nbytes=0):
        self.at_capacity = at_capacity
        self.spool_count = count
        self.spool_bytes = nbytes

    def flush_spool(self, _fn):
        return 0


def _state(**over):
    base = {"current_job_id": None, "pending_job": None,
            "pending_since": None, "claiming": False}
    base.update(over)
    return base


# ── the gate reaches every path ─────────────────────────────────────────────

class TestBackPressureOnTheWebSocketPath:
    def test_a_full_spool_declines_a_pushed_offer(self):
        """The default path. Accepting here just grows the undeliverable pile."""
        ws = AsyncMock()
        state = _state()
        accepted = asyncio.run(ag._ws_stage_job_offer(
            ws, {"job_id": "job-1"}, state, spool=_Spool(at_capacity=True)))
        assert accepted is False
        assert state["pending_job"] is None

    def test_a_healthy_spool_still_accepts(self):
        ws = AsyncMock()
        state = _state()
        assert asyncio.run(ag._ws_stage_job_offer(
            ws, {"job_id": "job-1"}, state,
            spool=_Spool(at_capacity=False))) is True

    def test_no_spool_supplied_is_not_a_refusal(self):
        """Standalone/unit callers pass none; absence is not back-pressure."""
        ws = AsyncMock()
        assert asyncio.run(ag._ws_stage_job_offer(
            ws, {"job_id": "job-1"}, _state())) is True

    @pytest.mark.asyncio
    async def test_the_poll_fallback_does_not_claim_while_saturated(self):
        polls = []

        class _Transport:
            def poll_jobs(self, limit):
                polls.append(1)
                return []

        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1",
            _Spool(at_capacity=True), 1, asyncio.Lock(), _state()))
        await asyncio.sleep(1.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        assert not polls, "claimed work with a full spool"

    @pytest.mark.asyncio
    async def test_the_poll_fallback_resumes_once_the_spool_drains(self):
        """Back-pressure must be a pause, not a latch."""
        polls = []
        spool = _Spool(at_capacity=True)

        class _Transport:
            def poll_jobs(self, limit):
                polls.append(1)
                return []

        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1", spool, 1,
            asyncio.Lock(), _state()))
        await asyncio.sleep(1.2)
        assert not polls
        spool.at_capacity = False
        await asyncio.sleep(1.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        assert polls, "stayed paused after the spool drained"


# ── the pause is reported, not silent ───────────────────────────────────────

class TestThePauseIsVisible:
    def test_a_saturated_probe_reports_paused(self):
        assert ag._heartbeat_status(_Spool(at_capacity=True), None) == "paused"

    def test_an_idle_probe_reports_online(self):
        assert ag._heartbeat_status(_Spool(), None) == "online"

    def test_a_running_job_still_reports_busy(self):
        """A job in flight outranks spool pressure: the manager must keep
        renewing that lease, and `busy` is what carries current_job_id."""
        assert ag._heartbeat_status(_Spool(at_capacity=True), "job-1") == "busy"

    def test_no_spool_reports_online(self):
        assert ag._heartbeat_status(None, None) == "online"

    def test_paused_is_a_status_the_manager_understands(self):
        """A value the manager coerces back to `online` would re-hide the
        pause — the manager's AgentStatus must carry it."""
        assert ag.PAUSED_STATUS == "paused"
