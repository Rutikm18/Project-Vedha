"""
The queue defects: a probe claiming two jobs, and a probe going deaf.

D1 — DOUBLE CLAIM (a job that fails without ever running)
----------------------------------------------------------
The WS receive loop and the HTTP poll fallback both claim jobs, and the
fallback checked "am I free?" BEFORE an await:

    poll_fallback:  check state (free) --> await poll_jobs -----> job_lock --> run
    main loop:                  job_push arrives --> stage (state STILL free) --> claim

Both claims succeed. `job_lock` then serialises EXECUTION, so the second job
waits — but its 300 s lease started at claim time, and nothing renews a job
that is not running (the WS heartbeat reports only `current_job_id`). Behind a
two-hour deep scan the lease expires, the reaper requeues, the cycle repeats
until attempt_count hits max_attempts, and the job lands in `failed` with
"maximum execution attempts exhausted" having never executed a single probe.

That is the reported symptom: send a second job, and instead of waiting its
turn it breaks.

The fix is to RESERVE before yielding, not after: the fallback marks itself
claiming before the await, and an offer arriving mid-poll is declined.

D2 — PERMANENT DEAFNESS
-----------------------
`pending_job` was cleared ONLY by a matching `job_claim` frame. If the manager
never sent one — multi-worker deployment, Redis backplane miss, socket
displaced between ack and claim — the field stayed set forever, and the poll
fallback's own guard then skipped every cycle:

    if job_state.get("pending_job") is not None: continue

The probe kept heartbeating, looked online, and never took another job. A
staged offer now expires, so an unanswered ack costs one TTL instead of the
process lifetime.
"""
from __future__ import annotations

import asyncio
import json
import time
from unittest.mock import AsyncMock

import pytest

from agent import agent as ag


def _state(**over):
    base = {"current_job_id": None, "pending_job": None,
            "pending_since": None, "claiming": False}
    base.update(over)
    return base


# ── D1: the reservation closes the window ───────────────────────────────────

class TestNoDoubleClaim:
    def test_a_free_probe_accepts_an_offer(self):
        ws = AsyncMock()
        state = _state()
        accepted = asyncio.run(
            ag._ws_stage_job_offer(ws, {"job_id": "job-1"}, state))
        assert accepted is True
        assert state["pending_job"]["job_id"] == "job-1"

    def test_an_offer_arriving_mid_poll_is_declined(self):
        """The exact race. `claiming` is set before the fallback yields."""
        ws = AsyncMock()
        state = _state(claiming=True)
        accepted = asyncio.run(
            ag._ws_stage_job_offer(ws, {"job_id": "job-2"}, state))
        assert accepted is False
        assert state["pending_job"] is None
        frame = json.loads(ws.send.await_args.args[0])
        assert frame["accepted"] is False

    def test_a_busy_probe_still_declines(self):
        ws = AsyncMock()
        state = _state(current_job_id="job-1")
        assert asyncio.run(
            ag._ws_stage_job_offer(ws, {"job_id": "job-2"}, state)) is False

    def test_a_probe_with_an_offer_already_staged_declines(self):
        ws = AsyncMock()
        state = _state(pending_job={"job_id": "job-1"},
                       pending_since=time.monotonic())
        assert asyncio.run(
            ag._ws_stage_job_offer(ws, {"job_id": "job-2"}, state)) is False

    @pytest.mark.asyncio
    async def test_the_fallback_reserves_before_it_yields(self):
        """Drive the real race: a job_push lands while poll_jobs is in flight.

        Without the reservation this stages the pushed job and the probe holds
        two claims.
        """
        observed = []

        class _Transport:
            def poll_jobs(self, limit):
                # The manager pushes while we are blocked here.
                observed.append(("offer_accepted",
                                 asyncio.run_coroutine_threadsafe(
                                     ag._ws_stage_job_offer(
                                         AsyncMock(), {"job_id": "pushed"},
                                         state),
                                     loop).result()))
                return []

        loop = asyncio.get_running_loop()
        state = _state()
        lock = asyncio.Lock()
        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1", None, 1, lock, state))
        await asyncio.sleep(2.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        assert observed, "the poll never ran"
        assert all(accepted is False for _, accepted in observed), \
            "an offer was staged while a claim was already in flight"

    @pytest.mark.asyncio
    async def test_the_reservation_is_released_when_the_poll_finds_nothing(self):
        """Reserving must not become its own permanent block."""
        class _Transport:
            def poll_jobs(self, limit):
                return []

        state = _state()
        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1", None, 1,
            asyncio.Lock(), state))
        await asyncio.sleep(1.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        assert state["claiming"] is False

    @pytest.mark.asyncio
    async def test_the_reservation_is_released_when_the_poll_raises(self):
        class _Transport:
            def poll_jobs(self, limit):
                raise RuntimeError("manager unreachable")

        state = _state()
        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1", None, 1,
            asyncio.Lock(), state))
        await asyncio.sleep(1.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
        assert state["claiming"] is False


# ── D2: a staged offer cannot strand the probe ──────────────────────────────

class TestAStagedOfferExpires:
    def test_a_fresh_offer_is_not_expired(self):
        state = _state(pending_job={"job_id": "job-1"},
                       pending_since=time.monotonic())
        assert ag._ws_expire_stale_offer(state) is False
        assert state["pending_job"] is not None

    def test_an_unconfirmed_offer_expires_after_the_ttl(self):
        state = _state(
            pending_job={"job_id": "job-1"},
            pending_since=time.monotonic() - ag.WS_OFFER_TTL_SECONDS - 1)
        assert ag._ws_expire_stale_offer(state) is True
        assert state["pending_job"] is None
        assert state["pending_since"] is None

    def test_no_staged_offer_is_a_no_op(self):
        state = _state()
        assert ag._ws_expire_stale_offer(state) is False

    def test_the_ttl_is_far_below_the_manager_lease(self):
        """A staged offer must resolve long before the 300 s job lease, or the
        recovery is slower than the failure it prevents."""
        assert 5 <= ag.WS_OFFER_TTL_SECONDS <= 60

    def test_an_expired_offer_lets_the_probe_accept_again(self):
        ws = AsyncMock()
        state = _state(
            pending_job={"job_id": "stranded"},
            pending_since=time.monotonic() - ag.WS_OFFER_TTL_SECONDS - 1)
        accepted = asyncio.run(ag._ws_stage_job_offer(ws, {"job_id": "new"}, state))
        assert accepted is True
        assert state["pending_job"]["job_id"] == "new"

    @pytest.mark.asyncio
    async def test_a_stranded_offer_no_longer_deafens_the_poll_fallback(self):
        """The wedge: before the TTL this polled zero times, forever."""
        polls = []

        class _Transport:
            def poll_jobs(self, limit):
                polls.append(1)
                return []

        state = _state(
            pending_job={"job_id": "stranded"},
            pending_since=time.monotonic() - ag.WS_OFFER_TTL_SECONDS - 1)
        task = asyncio.create_task(ag._ws_http_poll_fallback(
            AsyncMock(), _Transport(), None, "a1", None, 1,
            asyncio.Lock(), state))
        await asyncio.sleep(1.5)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        assert polls, "the probe stayed deaf behind a stranded offer"
        assert state["pending_job"] is None

    def test_confirmation_clears_the_staging_timestamp(self):
        """A leftover timestamp would expire the NEXT offer prematurely."""
        state = _state(pending_job={"job_id": "job-1"},
                       pending_since=time.monotonic())
        job = ag._ws_take_confirmed_job(
            {"job_id": "job-1", "claimed": True, "attempt_id": "a",
             "fence": 1}, state)
        assert job is not None
        assert state["pending_job"] is None
        assert state["pending_since"] is None

    def test_a_declined_claim_also_clears_the_timestamp(self):
        state = _state(pending_job={"job_id": "job-1"},
                       pending_since=time.monotonic())
        assert ag._ws_take_confirmed_job(
            {"job_id": "job-1", "claimed": False}, state) is None
        assert state["pending_job"] is None
        assert state["pending_since"] is None
