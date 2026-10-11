"""An agent that fell back to HTTP polling must find its way back to push mode.

Seen on a real PC on 11 Oct 2026: the log showed
    WebSocket auth error: Cannot connect WebSocket: device credential refresh failed — falling back to HTTP poll.
and nothing more. That message was raised for ANY failed credential refresh, including "the manager could not be
reached", and the agent then polled over HTTP until it was restarted: the polling loop never looked at push mode
again. Three things are pinned here:

  1. the transport tells a transient refresh failure (manager unreachable / 5xx) from a real rejection;
  2. the push loop retries the transient kind with backoff instead of giving up, and still gives up on a
     rejection or a missing library;
  3. the polling loop hands control back to push mode on a timer, unless push can never work in this build.
"""
from __future__ import annotations

import asyncio

import pytest

import agent.agent as ag
from agent import transport as tr


class _FakeTransport:
    """Only what the push loop touches before it has a connection."""

    def __init__(self, errors):
        self._errors = list(errors)
        self.calls = 0

    async def connect_ws(self):
        self.calls += 1
        raise self._errors.pop(0)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
    monkeypatch.setattr(ag, "say", lambda *a, **k: None)
    monkeypatch.setattr(ag, "WS_RECONNECT_BACKOFF_MIN", 0.01)
    monkeypatch.setattr(ag, "_PUSH_UNAVAILABLE_FOR_GOOD", False)


def _run(transport):
    return asyncio.run(ag._run_ws_push_loop(transport, None, "agent-1", None, 30, 10))


# ── 1. the transport tells the two kinds of failure apart ─────────────────────────────

class TestConnectWsClassifiesTheFailure:
    def _transport(self, outcome):
        t = tr.Transport("https://manager.example.com", agent_token="tok")
        t.ensure_device_access = lambda **kw: False
        t._last_refresh_outcome = outcome
        return t

    def test_an_unreachable_manager_is_transient(self):
        with pytest.raises(tr.TransportUnavailableError, match="could not be reached"):
            asyncio.run(self._transport(tr.DEVICE_REFRESH_UNAVAILABLE).connect_ws())

    def test_a_rejected_credential_is_not_transient(self):
        with pytest.raises(tr.TransportError, match="refresh failed") as caught:
            asyncio.run(self._transport(tr.DEVICE_REFRESH_REJECTED).connect_ws())
        assert not isinstance(caught.value, tr.TransportUnavailableError)

    def test_the_transient_error_is_still_a_transport_error(self):
        # Code that already catches TransportError keeps working.
        assert issubclass(tr.TransportUnavailableError, tr.TransportError)


# ── 2. the push loop retries the transient kind and still gives up on the others ──────

class TestPushLoop:
    def test_a_manager_blip_is_retried_not_treated_as_the_end_of_push_mode(self):
        transport = _FakeTransport([
            tr.TransportUnavailableError("the manager could not be reached"),
            tr.TransportUnavailableError("the manager could not be reached"),
            ModuleNotFoundError("No module named 'websockets.asyncio'"),     # ends the test deterministically
        ])
        assert _run(transport) is False
        assert transport.calls == 3          # it tried again twice instead of falling back at the first blip

    def test_a_rejected_credential_still_falls_back_at_once(self):
        transport = _FakeTransport([tr.TransportError("credential rejected")])
        assert _run(transport) is False
        assert transport.calls == 1

    def test_a_missing_library_marks_push_mode_unavailable_for_good(self):
        transport = _FakeTransport([ModuleNotFoundError("No module named 'websockets.asyncio'")])
        assert _run(transport) is False
        assert ag._PUSH_UNAVAILABLE_FOR_GOOD is True

    def test_a_blip_does_not_mark_push_mode_unavailable(self):
        transport = _FakeTransport([tr.TransportUnavailableError("x"), tr.TransportError("rejected")])
        assert _run(transport) is False
        assert ag._PUSH_UNAVAILABLE_FOR_GOOD is False


# ── 3. the polling loop goes back to push mode on a timer ─────────────────────────────

class TestPushRetryTimer:
    def test_not_before_the_interval_has_passed(self):
        assert not ag._push_retry_due(enabled=True, unavailable_for_good=False, now=99.0, next_attempt=100.0)

    def test_at_and_after_the_interval(self):
        assert ag._push_retry_due(enabled=True, unavailable_for_good=False, now=100.0, next_attempt=100.0)
        assert ag._push_retry_due(enabled=True, unavailable_for_good=False, now=500.0, next_attempt=100.0)

    def test_never_when_push_mode_is_switched_off(self):
        assert not ag._push_retry_due(enabled=False, unavailable_for_good=False, now=500.0, next_attempt=100.0)

    def test_never_when_the_build_cannot_do_push_mode(self):
        assert not ag._push_retry_due(enabled=True, unavailable_for_good=True, now=500.0, next_attempt=100.0)


class TestAttemptPushMode:
    def test_false_means_carry_on_polling(self, monkeypatch):
        async def gave_up(*a, **k):
            return False
        monkeypatch.setattr(ag, "_run_ws_push_loop", gave_up)
        assert ag._attempt_push_mode(None, None, "a", None, 30, 10) is False

    def test_true_means_stop_the_probe(self, monkeypatch):
        async def done(*a, **k):
            return True
        monkeypatch.setattr(ag, "_run_ws_push_loop", done)
        assert ag._attempt_push_mode(None, None, "a", None, 30, 10) is True

    def test_a_crash_falls_back_to_polling_instead_of_killing_the_probe(self, monkeypatch):
        async def boom(*a, **k):
            raise RuntimeError("push loop crashed")
        monkeypatch.setattr(ag, "_run_ws_push_loop", boom)
        assert ag._attempt_push_mode(None, None, "a", None, 30, 10) is False

    def test_ctrl_c_stops_the_probe_cleanly(self, monkeypatch):
        async def interrupted(*a, **k):
            raise KeyboardInterrupt
        monkeypatch.setattr(ag, "_run_ws_push_loop", interrupted)
        with pytest.raises(SystemExit) as stop:
            ag._attempt_push_mode(None, None, "a", None, 30, 10)
        assert stop.value.code == 0

    def test_the_retry_interval_is_bounded(self, monkeypatch):
        monkeypatch.setenv("PROBE_PUSH_RETRY_SECS", "1")            # too small: would hammer the manager
        assert ag._bounded_env_int("PROBE_PUSH_RETRY_SECS", 300, 60, 3600) == 60
        monkeypatch.setenv("PROBE_PUSH_RETRY_SECS", "999999")
        assert ag._bounded_env_int("PROBE_PUSH_RETRY_SECS", 300, 60, 3600) == 3600
