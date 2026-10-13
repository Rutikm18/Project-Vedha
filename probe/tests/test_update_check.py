"""Tests for agent/update_check.py — the agent's "is there a newer agent?" check.

It is version management only: it asks, double-checks the manager's answer and
tells a person. It must never raise into the agent, never block an unattended
agent at a prompt, and never accept a version that is not strictly newer.
"""
from __future__ import annotations

import io
import time
from unittest.mock import MagicMock

import httpx
import pytest

from agent import update_check as uc
from agent.transport import Transport
from agent.version import AGENT_VERSION


class FakeTransport:
    def __init__(self, reply=None, boom: Exception | None = None):
        self.reply, self.boom, self.calls = reply, boom, []

    def update_check(self, version, platform, architecture, **_):
        self.calls.append((version, platform, architecture))
        if self.boom:
            raise self.boom
        return self.reply


def newer(latest="2.2.0"):
    return {"update_available": True, "latest": latest}


# ── versions ─────────────────────────────────────────────────────────────────

class TestVersions:
    @pytest.mark.parametrize("text,expected", [
        ("2.1.0", (2, 1, 0)), ("v2.1", (2, 1)), ("1.0.375", (1, 0, 375)),
        ("2.1.0-rc1", (2, 1, 0)), ("2.1.0+build5", (2, 1, 0)), (" 3 ", (3,)),
    ])
    def test_parse(self, text, expected):
        assert uc.parse_version(text) == expected

    @pytest.mark.parametrize("text", ["", "abc", "2..1", "1.2.3.4.5", None, 2.1, "2.x"])
    def test_unparseable_is_none(self, text):
        assert uc.parse_version(text) is None

    @pytest.mark.parametrize("latest,current,expected", [
        ("2.2.0", "2.1.0", True), ("2.1.1", "2.1.0", True), ("3.0.0", "2.9.9", True),
        ("2.10.0", "2.9.0", True),          # numeric, not lexical
        ("2.1.0", "2.1.0", False), ("2.1", "2.1.0", False),   # equal, padded
        ("2.0.9", "2.1.0", False),          # never a downgrade
        ("garbage", "2.1.0", False), ("2.2.0", "garbage", False),
    ])
    def test_is_newer(self, latest, current, expected):
        assert uc.is_newer(latest, current) is expected

    def test_the_agents_own_version_parses(self):
        assert uc.parse_version(AGENT_VERSION) is not None


# ── settings ─────────────────────────────────────────────────────────────────

class TestSettings:
    def test_enabled_by_default_and_switchable(self):
        assert uc.enabled({}) is True
        for off in ("off", "0", "false", "NO", "Disabled"):
            assert uc.enabled({"PROBE_UPDATE_CHECK": off}) is False
        assert uc.enabled({"PROBE_UPDATE_CHECK": "on"}) is True

    @pytest.mark.parametrize("raw,expected", [
        ("", 6.0), ("12", 12.0), ("0.1", 1.0), ("9999", 168.0), ("nope", 6.0),
    ])
    def test_interval_is_clamped(self, raw, expected):
        assert uc.interval_hours({"PROBE_UPDATE_CHECK_INTERVAL_HOURS": raw}) == expected


# ── the manager's answer ─────────────────────────────────────────────────────

class TestInterpret:
    def test_newer_version_is_available(self):
        info = uc.interpret("2.1.0", newer("2.2.0"))
        assert info.available and info.latest == "2.2.0" and info.current == "2.1.0"

    def test_manager_saying_yes_is_not_enough(self):
        """The agent re-checks: an offer that is not newer is ignored."""
        for latest in ("2.1.0", "2.0.0", "not-a-version", ""):
            assert not uc.interpret("2.1.0", {"update_available": True, "latest": latest}).available

    def test_only_a_real_true_counts(self):
        for flag in ("true", 1, None, "yes"):
            assert not uc.interpret("2.1.0", {"update_available": flag, "latest": "9.9.9"}).available

    @pytest.mark.parametrize("body", [None, [], "x", 5])
    def test_unusable_reply_is_none(self, body):
        assert uc.interpret("2.1.0", body) is None

    def test_message_is_bounded_and_typed(self):
        assert len(uc.interpret("2.1.0", {**newer(), "message": "x" * 5000}).message) == 300
        assert uc.interpret("2.1.0", {**newer(), "message": {"a": 1}}).message == ""


class TestCheck:
    def test_asks_with_version_platform_and_architecture(self):
        t = FakeTransport(newer())
        info = uc.check(t, "2.1.0", platform="win32", architecture="AMD64")
        assert info.available and t.calls == [("2.1.0", "win32", "AMD64")]

    @pytest.mark.parametrize("boom", [httpx.ConnectError("down"), RuntimeError("x"), ValueError("y")])
    def test_never_raises(self, boom):
        assert uc.check(FakeTransport(boom=boom), "2.1.0", platform="linux", architecture="x86_64") is None

    def test_no_answer_is_none(self):
        assert uc.check(FakeTransport(None), "2.1.0", platform="linux", architecture="x86_64") is None


# ── talking to a person ──────────────────────────────────────────────────────

class TestPrompt:
    @pytest.mark.parametrize("answer,expected", [
        ("y", True), ("Y", True), ("yes", True), (" YES ", True),
        ("n", False), ("", False), ("maybe", False), ("yep", False),
    ])
    def test_only_yes_means_yes(self, answer, expected):
        assert uc.ask_yes_no("?", input_fn=lambda _q: answer, timeout=1) is expected

    def test_eof_means_no(self):
        def eof(_q):
            raise EOFError
        assert uc.ask_yes_no("?", input_fn=eof, timeout=1) is False

    def test_an_unattended_prompt_times_out_to_no(self):
        started = time.monotonic()
        assert uc.ask_yes_no("?", input_fn=lambda _q: time.sleep(5) or "y", timeout=0.2) is False
        assert time.monotonic() - started < 2

    def test_can_prompt_needs_both_ends_on_a_terminal(self):
        tty, pipe = MagicMock(), MagicMock()
        tty.isatty.return_value, pipe.isatty.return_value = True, False
        assert uc.can_prompt(tty, tty) is True
        assert uc.can_prompt(pipe, tty) is False
        assert uc.can_prompt(tty, pipe) is False
        assert uc.can_prompt(io.StringIO(), io.StringIO()) is False   # StringIO is not a tty

    def test_can_prompt_survives_a_closed_stream(self):
        closed = MagicMock()
        closed.isatty.side_effect = ValueError("closed file")
        assert uc.can_prompt(closed, closed) is False


# ── start-up check ───────────────────────────────────────────────────────────

class TestStartup:
    def run(self, transport, *, interactive, answer="n", monkeypatch=None):
        said: list[str] = []
        asked: list[str] = []

        def answer_fn(q):
            asked.append(q)
            return answer

        info = uc.run_startup_check(
            transport, "2.1.0", platform="linux", architecture="x86_64",
            say=said.append, interactive=interactive, input_fn=answer_fn, timeout=1,
        )
        return info, said, asked

    def test_nothing_new_says_nothing(self):
        info, said, asked = self.run(FakeTransport({"update_available": False}), interactive=True)
        assert info.available is False and said == [] and asked == []

    def test_manager_unreachable_says_nothing(self):
        info, said, asked = self.run(FakeTransport(None), interactive=True)
        assert info is None and said == [] and asked == []

    def test_a_person_is_asked_and_yes_explains_the_manual_step(self):
        info, said, asked = self.run(FakeTransport(newer("2.2.0")), interactive=True, answer="y")
        assert info.available and len(asked) == 1
        text = "\n".join(said)
        assert "2.2.0" in text and "2.1.0" in text
        assert "not enabled yet" in text and "Fleet" in text   # nothing was downloaded

    def test_no_keeps_the_current_version_and_asks_again_next_start(self):
        _, said, asked = self.run(FakeTransport(newer()), interactive=True, answer="n")
        assert len(asked) == 1
        assert "Staying on 2.1.0" in "\n".join(said) and "asked again" in "\n".join(said)

    def test_headless_agent_is_never_prompted(self):
        _, said, asked = self.run(FakeTransport(newer()), interactive=False)
        assert asked == []
        assert "Not applied" in "\n".join(said)

    def test_windows_hint_names_install_cmd(self):
        said: list[str] = []
        uc.run_startup_check(FakeTransport(newer()), "2.1.0", platform="win32",
                             architecture="AMD64", say=said.append, interactive=False)
        assert "install.cmd" in "\n".join(said)

    def test_switched_off_makes_no_request(self, monkeypatch):
        monkeypatch.setenv("PROBE_UPDATE_CHECK", "off")
        t = FakeTransport(newer())
        info, said, asked = self.run(t, interactive=True)
        assert info is None and t.calls == [] and said == [] and asked == []


# ── while running ────────────────────────────────────────────────────────────

class TestPeriodic:
    def make(self, transport, said):
        return uc.PeriodicUpdateChecker(
            transport, "2.1.0", platform="linux", architecture="x86_64",
            say=said.append, hours=6,
        )

    def test_announces_a_version_once(self):
        said: list[str] = []
        checker = self.make(FakeTransport(newer("2.2.0")), said)
        checker.check_once(); checker.check_once(); checker.check_once()
        assert len(said) == 1 and "2.2.0" in said[0]

    def test_announces_again_for_a_newer_one(self):
        said: list[str] = []
        t = FakeTransport(newer("2.2.0"))
        checker = self.make(t, said)
        checker.check_once()
        t.reply = newer("2.3.0")
        checker.check_once()
        assert len(said) == 2 and "2.3.0" in said[1]

    def test_never_prompts_and_never_raises(self):
        said: list[str] = []
        checker = self.make(FakeTransport(boom=RuntimeError("x")), said)
        assert checker.check_once() is None and said == []

    def test_delay_is_the_interval_with_jitter(self):
        checker = self.make(FakeTransport(), [])
        for _ in range(50):
            assert 6 * 3600 * 0.9 <= checker.delay_seconds() <= 6 * 3600 * 1.1

    def test_start_is_idempotent_and_stoppable(self, monkeypatch):
        monkeypatch.setattr(uc.PeriodicUpdateChecker, "delay_seconds", lambda self: 3600.0)
        checker = self.make(FakeTransport(), [])
        checker.start()
        thread = checker._thread
        checker.start()
        assert checker._thread is thread and thread.daemon and thread.is_alive()
        checker.stop()
        thread.join(2)
        assert not thread.is_alive()

    def test_disabled_never_starts_a_thread(self, monkeypatch):
        monkeypatch.setenv("PROBE_UPDATE_CHECK", "off")
        checker = self.make(FakeTransport(), [])
        checker.start()
        assert checker._thread is None


# ── transport ────────────────────────────────────────────────────────────────

@pytest.fixture
def transport(tmp_path):
    t = Transport("http://localhost:8000", verify_tls=False, state_file=tmp_path / "state.json",
                  agent_id="agent-1", agent_token="tok")
    t._client = MagicMock()
    return t


def _resp(status=200, body=None):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = body if body is not None else {}
    return r


class TestTransport:
    def test_update_check_posts_identity_and_versions(self, transport):
        transport._client.post.return_value = _resp(200, newer())
        assert transport.update_check("2.1.0", "win32", "AMD64") == newer()
        args, kwargs = transport._client.post.call_args
        assert args[0] == "/agents/update-check"
        assert kwargs["headers"] == {"Authorization": "Bearer tok"}
        assert kwargs["json"] == {"agent_id": "agent-1", "agent_version": "2.1.0",
                                  "platform": "win32", "architecture": "AMD64"}
        assert kwargs["timeout"] == 5.0

    @pytest.mark.parametrize("status", [401, 403, 404, 422, 500])
    def test_any_error_status_is_no_answer(self, transport, status):
        transport._client.post.return_value = _resp(status)
        assert transport.update_check("2.1.0", "linux", "x86_64") is None

    def test_network_failure_is_no_answer(self, transport):
        transport._client.post.side_effect = httpx.ConnectError("down")
        assert transport.update_check("2.1.0", "linux", "x86_64") is None

    def test_bad_json_is_no_answer(self, transport):
        r = _resp(200)
        r.json.side_effect = ValueError("not json")
        transport._client.post.return_value = r
        assert transport.update_check("2.1.0", "linux", "x86_64") is None

    def test_non_object_json_is_no_answer(self, transport):
        transport._client.post.return_value = _resp(200, ["x"])
        assert transport.update_check("2.1.0", "linux", "x86_64") is None

    def test_not_enrolled_makes_no_request(self, tmp_path):
        t = Transport("http://localhost:8000", state_file=tmp_path / "s.json")
        t._client = MagicMock()
        assert t.update_check("2.1.0", "linux", "x86_64") is None
        t._client.post.assert_not_called()

    def test_heartbeat_reports_the_running_version(self, transport):
        transport._client.post.return_value = _resp(200)
        transport.ensure_device_access = lambda **_: True
        transport.heartbeat_ex("online", None, None, None)
        assert transport._client.post.call_args.kwargs["json"]["agent_version"] == AGENT_VERSION
