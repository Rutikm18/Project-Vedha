"""The build gate and the push-mode fallback.

A compiled agent once registered with the manager and then could not open its live connection:
`websockets` loads `websockets.asyncio.client` lazily by name, a compiler cannot follow that, and
the old `runtime-check` only imported the top-level package. These tests pin the three fixes:
the gate exercises the real entry points, a missing WebSocket library falls back to HTTP polling,
and `status` stops saying ONLINE when the connection is lost.
"""
from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path

import pytest

from agent import runtime_status as rs

PROBE = Path(__file__).resolve().parent.parent


class TestLibraryEntryPointGate:
    def test_healthy_environment_passes(self):
        import agent.agent as ag
        assert ag._library_entry_point_failures() == []

    def test_missing_websocket_submodule_is_caught(self):
        """Simulate the compiled build: the package imports, its lazy submodule does not."""
        script = (
            "import sys\n"
            "sys.modules['websockets.asyncio'] = None\n"      # blocks websockets.asyncio.client
            "sys.modules['websockets.legacy'] = None\n"       # and the pre-13 location
            "from agent.agent import _library_entry_point_failures\n"
            "print('FAILURES:', _library_entry_point_failures())\n"
        )
        result = subprocess.run([sys.executable, "-c", script], cwd=str(PROBE),
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stderr
        assert "websockets (live connection)" in result.stdout, result.stdout

    def test_the_command_still_reports_ok(self):
        result = subprocess.run([sys.executable, "-m", "agent.agent", "runtime-check"], cwd=str(PROBE),
                                capture_output=True, text=True, timeout=90)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "runtime-check OK" in result.stdout


class FakeTransport:
    """Only what _run_ws_push_loop touches before it has a connection."""

    def __init__(self, errors):
        self._errors = list(errors)
        self.calls = 0

    async def connect_ws(self):
        self.calls += 1
        raise self._errors.pop(0)


class TestPushModeFallback:
    def _run(self, transport):
        import agent.agent as ag
        return asyncio.run(ag._run_ws_push_loop(transport, None, "agent-1", None, 30, 10))

    def test_missing_websocket_library_falls_back_to_polling_instead_of_looping(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        transport = FakeTransport([ModuleNotFoundError("No module named 'websockets.asyncio'")])
        assert self._run(transport) is False        # False = "push mode unavailable, poll over HTTP"
        assert transport.calls == 1                 # it did not retry a connection that can never work

    def test_a_lost_connection_is_recorded_as_retrying(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")

        async def no_wait(_seconds):
            return None

        monkeypatch.setattr(ag.asyncio, "sleep", no_wait)
        # first attempt: network trouble (loop retries); second: library missing (loop ends)
        transport = FakeTransport([OSError("network is unreachable"), ModuleNotFoundError("websockets.asyncio")])
        assert self._run(transport) is False
        record = rs.read(tmp_path / "status.json")
        assert record["state"] == "retrying"
        assert "unavailable" in record["reason"] and record["remediation"]

    def test_status_helper_names_what_was_lost_and_how_to_get_help(self, tmp_path, monkeypatch):
        import agent.agent as ag
        monkeypatch.setattr(ag, "_STATUS_PATH", tmp_path / "status.json")
        ag._status("online", detail="connected to the manager (live connection); waiting for jobs")
        assert rs.read(tmp_path / "status.json")["state"] == "online"
        ag._status_connection_lost("live connection closed (code 1006)")
        record = rs.read(tmp_path / "status.json")
        assert record["state"] == "retrying" and "1006" in record["reason"] and "support-bundle" in record["remediation"]


def test_build_script_includes_the_whole_websockets_package():
    text = (PROBE / "windows" / "build-agent-exe.ps1").read_text(encoding="utf-8")
    assert "--include-package=websockets" in text
