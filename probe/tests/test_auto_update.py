"""auto_update.py — the agent updating itself on Windows (off by default).

The Windows-only parts (a real Scheduled Task, a real installer run) cannot run here, so the
runner is faked and these tests pin every decision around it: when it is allowed to act, what
it writes, which commands it would run, and that it never acts on a stale reply, while a scan
is running, or twice for the same version.
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from agent import auto_update as au
from agent import update_check as uc

ON = {"PROBE_AUTO_UPDATE": "on"}


@pytest.fixture(autouse=True)
def _idle():
    au._running_jobs = 0
    yield
    au._running_jobs = 0


class FakeTransport:
    def __init__(self, ticket="vet_upd-abc-def", latest="2.3.0", available=True, installer=b"# Vedha installer\n"):
        self.reply = {"update_available": available, "latest": latest, "ticket": ticket}
        self.installer = installer
        self.calls: list[tuple] = []

    def update_ticket(self, current, platform, arch):
        self.calls.append(("ticket", current, platform, arch))
        return self.reply

    def download_installer(self):
        self.calls.append(("installer",))
        return self.installer


class FakeRunner:
    def __init__(self, fail_on=None):
        self.commands: list[list[str]] = []
        self.fail_on = fail_on

    def __call__(self, cmd):
        self.commands.append(cmd)
        code = 1 if self.fail_on and cmd[1] == self.fail_on else 0
        return SimpleNamespace(returncode=code, stdout="", stderr="Access is denied." if code else "")


def info(latest="2.3.0", current="2.2.0"):
    return uc.UpdateInfo(available=True, current=current, latest=latest)


def apply(tmp_path, transport=None, runner=None, *, env=ON, platform="win32", now=1000.0, i=None):
    transport = transport or FakeTransport()
    runner = runner or FakeRunner()
    out = au.apply_update(transport, i or info(), manager_url="https://api.example.com/", platform=platform,
                          architecture="AMD64", env=env, base=tmp_path / "vedha-agent", now=now, runner=runner)
    return out, transport, runner


# ── gates ────────────────────────────────────────────────────────────────────

def test_it_is_off_unless_switched_on(tmp_path):
    for env in ({}, {"PROBE_AUTO_UPDATE": "off"}, {"PROBE_AUTO_UPDATE": ""}, {"PROBE_AUTO_UPDATE": "maybe"}):
        out, transport, runner = apply(tmp_path, env=env)
        assert out.reason == "off" and not out.applied
        assert transport.calls == [] and runner.commands == []          # nothing was even asked
    assert au.enabled({"PROBE_AUTO_UPDATE": "ON"}) and au.enabled({"PROBE_AUTO_UPDATE": "true"})


def test_only_windows_for_now(tmp_path):
    for platform in ("linux", "darwin"):
        out, transport, runner = apply(tmp_path, platform=platform)
        assert out.reason == "unsupported" and transport.calls == [] and runner.commands == []


def test_it_never_replaces_the_agent_while_a_scan_runs(tmp_path):
    au.mark_job_started()
    out, transport, runner = apply(tmp_path)
    assert out.reason == "busy" and out.retry_soon and not out.applied
    assert transport.calls == [] and runner.commands == []
    au.mark_job_finished()
    assert apply(tmp_path)[0].applied                                     # idle again: it goes ahead


def test_the_busy_counter_survives_overlapping_jobs_and_never_goes_negative():
    au.mark_job_started(); au.mark_job_started()
    au.mark_job_finished()
    assert au.is_busy()
    au.mark_job_finished(); au.mark_job_finished()
    assert not au.is_busy()


def test_the_same_version_is_not_retried_for_24_hours(tmp_path):
    assert apply(tmp_path, now=1000.0)[0].applied
    again = apply(tmp_path, now=1000.0 + 3600)[0]
    assert again.reason == "recently-tried" and not again.applied
    # a different (newer) version is tried at once, and the same one again after a day
    assert apply(tmp_path, transport=FakeTransport(latest="2.4.0"), i=info("2.4.0"), now=1000.0 + 3600)[0].applied
    assert apply(tmp_path, transport=FakeTransport(latest="2.4.0"), i=info("2.4.0"),
                 now=1000.0 + 3600 + au.RETRY_AFTER_SECONDS + 1)[0].applied


def test_it_does_not_trust_a_reply_that_is_not_strictly_newer(tmp_path):
    for reply in (dict(latest="2.2.0"), dict(latest="2.1.0"), dict(latest="junk"), dict(available=False), dict(ticket=None)):
        out, _, runner = apply(tmp_path, transport=FakeTransport(**reply))
        assert out.reason == "no-ticket" and runner.commands == [], reply


def test_a_data_folder_with_a_space_is_refused_rather_than_mis_quoted(tmp_path):
    out = au.apply_update(FakeTransport(), info(), manager_url="https://m", platform="win32", architecture="x",
                          env=ON, base=tmp_path / "has space", now=1.0, runner=FakeRunner())
    assert out.reason == "unsupported"


# ── what it prepares ─────────────────────────────────────────────────────────

def test_it_writes_the_installer_the_ticket_and_a_launcher_and_runs_a_one_shot_task(tmp_path):
    out, transport, runner = apply(tmp_path)
    folder = tmp_path / "vedha-agent" / "update"
    assert out.applied and out.reason == "started" and "2.2.0 to 2.3.0" in out.message
    assert (folder / "install.ps1").read_bytes() == b"# Vedha installer\n"
    assert (folder / "ticket.txt").read_text() == "vet_upd-abc-def"
    raw = (folder / "run-update.cmd").read_bytes()
    launcher = raw.decode("ascii")
    assert "-Manager \"https://api.example.com\"" in launcher                      # trailing slash removed
    assert f'set /p VEDHA_TICKET=<"{folder / "ticket.txt"}"' in launcher             # the launcher itself holds no secret
    assert '-Token "%VEDHA_TICKET%"' in launcher and "-TokenFile" not in launcher   # the manager-served installer has no -TokenFile
    assert "vet_upd" not in launcher and "-Scope" not in launcher                   # scope is kept by the installer
    assert "-ExecutionPolicy Bypass -File" in launcher and "> " in launcher         # output goes to update.log
    assert raw.count(b"\r\n") == raw.count(b"\n") == 4 and b"\r\r" not in raw   # CRLF, exactly once
    assert json.loads((folder / "last-attempt.json").read_text())["version"] == "2.3.0"
    # runs as SYSTEM, once, outside this process's own task, then starts it
    create, run = runner.commands
    assert create[:2] == ["schtasks", "/Create"] and "SYSTEM" in create and "/F" in create
    assert create[create.index("/TR") + 1] == str(folder / "run-update.cmd")
    assert run == ["schtasks", "/Run", "/TN", au.TASK_NAME]
    assert transport.calls[0] == ("ticket", "2.2.0", "win32", "AMD64")


def test_the_task_command_stays_inside_schtasks_261_character_limit_for_normal_paths():
    path = r"C:\ProgramData\vedha-agent\update\run-update.cmd"
    assert len(au.create_task_command(path)[au.create_task_command(path).index("/TR") + 1]) < 261


def test_failures_are_reported_and_never_raise(tmp_path):
    assert apply(tmp_path / "a", transport=FakeTransport(ticket=None))[0].reason == "no-ticket"
    assert apply(tmp_path / "b", transport=FakeTransport(installer=None))[0].reason == "no-installer"
    big = apply(tmp_path / "c", transport=FakeTransport(installer=b"x" * (3 * 1024 * 1024)))[0]
    assert big.reason == "no-installer"
    out = apply(tmp_path / "d", runner=FakeRunner(fail_on="/Create"))[0]
    assert out.reason == "schedule" and "Access is denied" in out.message and not out.applied
    broken = SimpleNamespace(update_ticket=lambda *a: (_ for _ in ()).throw(RuntimeError("boom")),
                             download_installer=lambda: b"")
    assert apply(tmp_path / "e", transport=broken)[0].reason == "io"


def test_an_unreadable_attempt_file_does_not_block_updates(tmp_path):
    folder = tmp_path / "vedha-agent" / "update"
    folder.mkdir(parents=True)
    (folder / "last-attempt.json").write_text("{not json")
    assert apply(tmp_path)[0].applied


def test_data_dir_follows_the_installers_state_file():
    assert au.data_dir({"STATE_FILE": r"D:\vedha\state.json"}) == Path(r"D:\vedha\state.json").parent
    assert str(au.data_dir({"ProgramData": "/pd"})).replace("\\", "/") == "/pd/vedha-agent"


# ── cleanup after the update ─────────────────────────────────────────────────

def test_cleanup_removes_the_task_installer_and_ticket_but_keeps_the_log(tmp_path):
    apply(tmp_path)
    folder = tmp_path / "vedha-agent" / "update"
    (folder / "update.log").write_text("installer output")
    runner = FakeRunner()
    au.cleanup_after_update(tmp_path / "vedha-agent", runner=runner)
    assert runner.commands == [["schtasks", "/Delete", "/TN", au.TASK_NAME, "/F"]]
    assert not (folder / "install.ps1").exists() and not (folder / "ticket.txt").exists()
    assert (folder / "update.log").exists() and (folder / "last-attempt.json").exists()


def test_cleanup_with_nothing_to_clean_does_nothing(tmp_path):
    runner = FakeRunner()
    au.cleanup_after_update(tmp_path / "never-updated", runner=runner)
    assert runner.commands == []


# ── the periodic checker uses it ─────────────────────────────────────────────

class _T:
    def __init__(self):
        self.n = 0

    def update_check(self, current, platform, arch):
        return {"update_available": True, "latest": "2.3.0", "message": ""}


def test_the_periodic_checker_calls_the_hook_only_for_an_offered_newer_version():
    said: list[str] = []
    calls: list[str] = []

    def hook(i):
        calls.append(i.latest)
        return au.Outcome(False, "busy", "A scan is running; the update will be tried again when the agent is idle.")

    checker = uc.PeriodicUpdateChecker(_T(), "2.2.0", platform="win32", architecture="x", say=said.append, hours=6, apply=hook)
    checker.check_once()
    assert calls == ["2.3.0"] and any("Automatic update is on" in s for s in said)
    assert any("A scan is running" in s for s in said)
    assert checker.delay_seconds() < 6 * 3600                     # first look comes soon after start
    assert checker.delay_seconds() < 6 * 3600                     # busy: retry in about 15 minutes
    assert checker.delay_seconds() > 5 * 3600                     # then back to the normal interval

    # not offered / not newer: the hook is not called
    class Same(_T):
        def update_check(self, *a):
            return {"update_available": True, "latest": "2.2.0"}
    calls.clear()
    uc.PeriodicUpdateChecker(Same(), "2.2.0", platform="win32", architecture="x", say=said.append, apply=hook).check_once()
    assert calls == []


def test_without_the_hook_the_checker_behaves_exactly_as_before():
    said: list[str] = []
    checker = uc.PeriodicUpdateChecker(_T(), "2.2.0", platform="win32", architecture="x", say=said.append, hours=6)
    checker.check_once()
    assert any("next time the agent is started in a terminal" in s for s in said)
    assert checker.delay_seconds() > 5 * 3600


def test_a_hook_that_raises_never_stops_the_checker():
    def boom(i):
        raise RuntimeError("no")
    checker = uc.PeriodicUpdateChecker(_T(), "2.2.0", platform="win32", architecture="x", say=lambda s: None, apply=boom)
    assert checker.check_once().available
