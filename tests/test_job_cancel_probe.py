"""
Probe-side operator job control + polling-noise suppression.

Two independent behaviours:

  1. A 409 on the in-job heartbeat means the manager has REVOKED this attempt's
     lease — the operator cancelled the job, or it was reassigned. That is a
     definitive answer, so the probe must abandon the job at once rather than
     spend its retry budget as if the network were flaky. Getting this wrong is
     expensive in both directions: too eager and a blip kills a long scan, too
     lazy and a "stopped" scan keeps hammering the target for minutes.

  2. The probe polls the manager every POLL_INTERVAL seconds forever. httpx logs
     one INFO line per request, so at the old level the terminal filled with
     `HTTP Request: GET .../jobs "200 OK"` and hid everything worth reading.
"""
from __future__ import annotations

import logging
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agent import agent as ag
from agent.transport import (
    HEARTBEAT_FAILED,
    HEARTBEAT_LEASE_REVOKED,
    HEARTBEAT_OK,
    Transport,
)


@pytest.fixture
def transport(tmp_path: Path):
    t = Transport("http://localhost:8000", verify_tls=False,
                  state_file=tmp_path / "state.json")
    t._client = MagicMock()
    t.agent_id, t.agent_token = "abc", "tok"
    return t


class TestHeartbeatOutcomes:
    def test_409_is_reported_as_a_revoked_lease(self, transport):
        transport._client.post.return_value = MagicMock(status_code=409)
        assert transport.heartbeat_ex("busy", "j", "a", 4) == HEARTBEAT_LEASE_REVOKED

    def test_200_is_ok(self, transport):
        transport._client.post.return_value = MagicMock(status_code=200)
        assert transport.heartbeat_ex("busy", "j", "a", 4) == HEARTBEAT_OK

    @pytest.mark.parametrize("code", [401, 403, 422])
    def test_other_rejections_are_plain_failures(self, transport, code):
        """These may be transient/refreshable, so they must NOT read as a cancel
        — otherwise an expired token would silently abandon a running scan."""
        transport._client.post.return_value = MagicMock(status_code=code)
        assert transport.heartbeat_ex("busy", "j", "a", 4) == HEARTBEAT_FAILED

    def test_network_error_is_a_plain_failure(self, transport):
        import httpx
        transport._client.post.side_effect = httpx.ConnectError("down")
        assert transport.heartbeat_ex("busy", "j", "a", 4) == HEARTBEAT_FAILED

    def test_bool_heartbeat_contract_is_unchanged(self, transport):
        for code, expected in ((200, True), (401, False), (409, False)):
            transport._client.post.return_value = MagicMock(status_code=code)
            assert transport.heartbeat("online") is expected

    def test_revoked_lease_is_distinct_from_failure(self):
        assert HEARTBEAT_LEASE_REVOKED != HEARTBEAT_FAILED != HEARTBEAT_OK


class TestPollingNoiseIsSuppressed:
    """The probe polls forever; routine transport chatter must stay out of the
    terminal while real problems still surface."""

    def _configure(self, monkeypatch, **env):
        for k in ("LOG_LEVEL", "PROBE_DEBUG"):
            monkeypatch.delenv(k, raising=False)
        for k, v in env.items():
            monkeypatch.setenv(k, v)
        monkeypatch.setattr(ag, "_DEBUG", False)
        return ag.configure_logging()

    @pytest.mark.parametrize("noisy", ["httpx", "httpcore", "websockets",
                                       "asyncio", "urllib3"])
    def test_transport_loggers_are_quiet_by_default(self, monkeypatch, noisy):
        self._configure(monkeypatch)
        assert logging.getLogger(noisy).level == logging.WARNING

    def test_per_request_info_lines_are_suppressed(self, monkeypatch):
        """The actual regression: one INFO line per poll, every POLL_INTERVAL."""
        self._configure(monkeypatch)
        assert not logging.getLogger("httpx").isEnabledFor(logging.INFO)

    def test_transport_errors_still_surface(self, monkeypatch):
        """Quieting must not hide a genuinely unreachable manager."""
        self._configure(monkeypatch)
        httpx_log = logging.getLogger("httpx")
        assert httpx_log.isEnabledFor(logging.WARNING)
        assert httpx_log.isEnabledFor(logging.ERROR)

    def test_probe_debug_restores_full_tracing(self, monkeypatch):
        self._configure(monkeypatch, PROBE_DEBUG="1")
        assert logging.getLogger("httpx").level == logging.DEBUG

    def test_probe_own_narration_is_unaffected_at_info(self, monkeypatch):
        level = self._configure(monkeypatch)
        assert level == "INFO"
        assert logging.getLogger("agent").isEnabledFor(logging.INFO)
