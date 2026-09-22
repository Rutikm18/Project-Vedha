"""
T1.5 — the probe must not abandon work the manager is still holding for it.

THE ASYMMETRY
-------------
A running job keeps its claim through heartbeats, and the two sides disagreed
about how long a silence may last:

    manager : lease 300 s, reaper sweeps every 60 s
              -> the claim survives 300-360 s of missed heartbeats
    probe   : gives up after LEASE_LOSS_GRACE_HEARTBEATS (3) failures
              -> WS push / HTTP path  (heartbeat 30 s) -> quits at  90 s
              -> WS poll-fallback path (heartbeat 10 s) -> quits at  30 s

So a 35-second blip on the fallback path threw away a two-hour scan that the
manager would have kept for another four and a half minutes — and burned one of
the job's three attempts doing it.

Counting failures cannot be right, because the count says nothing about how
much lease is left: the same three misses mean 30 s on one path and 90 s on
another. The claim already carries `lease_expires_at`, and the probe simply
never read it.

THE RULE
--------
Abandon when the lease has actually expired, not after an arbitrary number of
failed heartbeats. A successful heartbeat renews it, so the local deadline
advances by the lease duration observed at claim time — no new protocol, and it
self-corrects if the manager's configured lease changes.

Fallbacks preserved: a 409 (operator cancel / reassignment) is still immediate
and definitive, and a claim with no usable `lease_expires_at` — an older
manager — still uses the count.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from agent import agent as ag
from agent.transport import HEARTBEAT_FAILED, HEARTBEAT_LEASE_REVOKED


def _iso(seconds_from_now: float) -> str:
    return (datetime.now(timezone.utc)
            + timedelta(seconds=seconds_from_now)).isoformat()


# ── reading the lease off the claim ─────────────────────────────────────────

class TestLeaseDeadline:
    def test_parses_the_claim_s_expiry(self):
        deadline = ag._lease_deadline({"lease_expires_at": _iso(300)})
        assert deadline is not None
        assert 290 <= deadline - ag.time.monotonic() <= 310

    def test_a_missing_expiry_is_none(self):
        assert ag._lease_deadline({}) is None

    def test_an_unparseable_expiry_is_none(self):
        """An older manager, or a malformed frame: fall back, never crash."""
        assert ag._lease_deadline({"lease_expires_at": "not-a-date"}) is None
        assert ag._lease_deadline({"lease_expires_at": None}) is None

    def test_a_naive_timestamp_is_treated_as_utc(self):
        """The manager sends UTC; a frame without a tz must not be read as
        local time, which on a UTC+5:30 host would look 5.5 hours expired."""
        naive = (datetime.now(timezone.utc) + timedelta(seconds=300)
                 ).replace(tzinfo=None).isoformat()
        deadline = ag._lease_deadline({"lease_expires_at": naive})
        assert deadline is not None
        assert deadline - ag.time.monotonic() > 200

    def test_an_already_expired_lease_is_in_the_past(self):
        deadline = ag._lease_deadline({"lease_expires_at": _iso(-10)})
        assert deadline is not None and deadline < ag.time.monotonic()


# ── the decision ────────────────────────────────────────────────────────────

class TestGiveUpDecision:
    def test_keeps_working_while_the_lease_is_alive(self):
        """The headline: three failed heartbeats are NOT a reason to quit if
        the manager is still holding the claim."""
        assert ag._should_abandon_lease(
            failures=3, failure_limit=3,
            lease_deadline=ag.time.monotonic() + 200) is False

    def test_abandons_once_the_lease_has_expired(self):
        assert ag._should_abandon_lease(
            failures=1, failure_limit=3,
            lease_deadline=ag.time.monotonic() - 1) is True

    def test_falls_back_to_the_count_when_the_lease_is_unknown(self):
        """An older manager sends no expiry — keep the previous behaviour
        rather than scanning forever against a claim that may be long gone."""
        assert ag._should_abandon_lease(
            failures=2, failure_limit=3, lease_deadline=None) is False
        assert ag._should_abandon_lease(
            failures=3, failure_limit=3, lease_deadline=None) is True

    @pytest.mark.parametrize("interval,failures", [(10, 3), (30, 3)])
    def test_the_verdict_no_longer_depends_on_the_heartbeat_interval(
        self, interval, failures,
    ):
        """The bug in one assertion: the same three misses meant 30 s on the
        poll-fallback path and 90 s on the push path. With a real deadline the
        interval stops changing the answer."""
        deadline = ag.time.monotonic() + 120
        assert ag._should_abandon_lease(
            failures=failures, failure_limit=3, lease_deadline=deadline) is False


# ── renewal advances the local deadline ─────────────────────────────────────

class TestRenewal:
    def test_a_successful_heartbeat_extends_the_deadline(self):
        now = ag.time.monotonic()
        extended = ag._renewed_deadline(now + 10, lease_duration=300.0, now=now)
        assert 299 <= extended - now <= 301

    def test_renewal_uses_the_observed_duration_not_a_hardcoded_one(self):
        """Self-correcting: if an operator sets job_lease_seconds to 900, the
        probe follows without a code change."""
        now = ag.time.monotonic()
        assert ag._renewed_deadline(now, lease_duration=900.0, now=now) - now \
            == pytest.approx(900.0, abs=1)

    def test_an_unknown_duration_leaves_the_deadline_alone(self):
        now = ag.time.monotonic()
        assert ag._renewed_deadline(now + 50, lease_duration=None, now=now) \
            == now + 50


# ── the end-to-end promise ──────────────────────────────────────────────────

class TestTheRunnerHonoursTheLease:
    def _drive(self, *, outcomes, lease_seconds, interval=0.01):
        """Run a job that never finishes, feeding scripted heartbeat outcomes."""
        cancelled = {"at": None}
        calls = {"n": 0}

        class _Transport:
            def heartbeat_ex(self, *a, **kw):
                calls["n"] += 1
                if calls["n"] <= len(outcomes):
                    return outcomes[calls["n"] - 1]
                return HEARTBEAT_FAILED

        class _Runner:
            def run_job(self, job, agent_id, cancellation_event=None):
                for _ in range(400):
                    if cancellation_event.wait(interval):
                        cancelled["at"] = calls["n"]
                        return "cancelled"
                return "finished"

        job = {"job_id": "j1", "attempt_id": "a1", "fence": 1}
        if lease_seconds is not None:
            job["lease_expires_at"] = _iso(lease_seconds)
        ag._run_polled_job_with_heartbeats(
            _Transport(), _Runner(), job, "agent-1",
            heartbeat_interval=interval)
        return cancelled["at"]

    def test_a_blip_no_longer_kills_a_job_with_lease_left(self):
        cancelled_at = self._drive(
            outcomes=[HEARTBEAT_FAILED] * 8, lease_seconds=60)
        assert cancelled_at is None, \
            f"abandoned after {cancelled_at} failures despite a live lease"

    def test_an_expired_lease_still_stops_the_job(self):
        assert self._drive(
            outcomes=[HEARTBEAT_FAILED] * 8, lease_seconds=-1) is not None

    def test_an_operator_cancel_is_still_immediate(self):
        """409 is definitive regardless of how much lease remains."""
        cancelled_at = self._drive(
            outcomes=[HEARTBEAT_LEASE_REVOKED], lease_seconds=300)
        assert cancelled_at == 1

    def test_an_old_manager_still_gets_count_based_grace(self):
        assert self._drive(
            outcomes=[HEARTBEAT_FAILED] * 8, lease_seconds=None) is not None
