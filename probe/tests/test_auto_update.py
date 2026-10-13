"""auto_update.py — the agent updating itself on Windows (off by default).

The Windows-only parts (a real Scheduled Task, a real installer run) cannot run here, so the
runner is faked and these tests pin every decision around it: when it is allowed to act, what
it writes, which commands it would run, and that it never acts on a stale reply, while a scan
is running, or twice for the same version.
"""
from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from agent import auto_update as au
from agent import release_trust as rt
from agent import update_check as uc

ON = {"PROBE_AUTO_UPDATE": "on"}


@pytest.fixture(autouse=True)
def _idle():
    au._running_jobs = 0
    yield
    au._running_jobs = 0


def _keypair():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    key = ec.generate_private_key(ec.SECP256R1())
    spki = base64.b64encode(key.public_key().public_bytes(
        serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)).decode()
    return key, spki


def _sign(key, data: bytes) -> str:
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
    r, s = decode_dss_signature(key.sign(data, ec.ECDSA(hashes.SHA256())))
    return base64.b64encode(r.to_bytes(32, "big") + s.to_bytes(32, "big")).decode()


PIN_KEY, PIN_SPKI = _keypair()


def make_release(*, latest="2.3.0", version="1.0.500", key=PIN_KEY, installer_spki=PIN_SPKI, expires=None, mutate=None):
    """A signed release as the manager would serve it: installer, manifest, signature."""
    installer = (f"# Vedha installer\n$script:VedhaReleaseP256Spki = '{installer_spki}'\n"
                 f"$script:VedhaReleaseVersion = '{version}'\n").encode()
    manifest = {"schema": 2, "version": version, "agent_version": latest,
                "windows_installer": {"file": "install.ps1", "sha256": hashlib.sha256(installer).hexdigest()}}
    if expires:
        manifest["expires"] = expires
    if mutate:
        mutate(manifest)
    body = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    return SimpleNamespace(installer=installer, manifest=body, sig=_sign(key, body) + "\n")


class FakeTransport:
    def __init__(self, ticket="vet_upd-abc-def", latest="2.3.0", available=True, installer="release", release=None, signed="release"):
        self.reply = {"update_available": available, "latest": latest, "ticket": ticket}
        self.release = release or make_release(latest=latest if latest in ("2.3.0", "2.4.0") else "2.3.0")
        self.installer = self.release.installer if installer == "release" else installer
        self.signed = (self.release.manifest, self.release.sig) if signed == "release" else signed
        self.calls: list[tuple] = []

    def update_ticket(self, current, platform, arch):
        self.calls.append(("ticket", current, platform, arch))
        return self.reply

    def download_installer(self):
        self.calls.append(("installer",))
        return self.installer

    def download_release_manifest(self):
        self.calls.append(("manifest",))
        return self.signed


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


def pin(tmp_path, *, spki=PIN_SPKI, release_version="1.0.400"):
    folder = tmp_path / "vedha-agent" / "release"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "trust.json").write_text(json.dumps({"schema": 1, "p256_spki": spki, "release_version": release_version}))


def apply(tmp_path, transport=None, runner=None, *, env=ON, platform="win32", now=1000.0, i=None, pinned=True):
    transport = transport or FakeTransport()
    runner = runner or FakeRunner()
    if pinned:
        pin(tmp_path)
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
    pin(tmp_path / "has space")
    out = au.apply_update(FakeTransport(), info(), manager_url="https://m", platform="win32", architecture="x",
                          env=ON, base=tmp_path / "has space" / "vedha-agent", now=1.0, runner=FakeRunner())
    assert out.reason == "unsupported"


# ── what it prepares ─────────────────────────────────────────────────────────

def test_it_writes_the_installer_the_ticket_and_a_launcher_and_runs_a_one_shot_task(tmp_path):
    out, transport, runner = apply(tmp_path)
    folder = tmp_path / "vedha-agent" / "update"
    assert out.applied and out.reason == "started" and "2.2.0 to 2.3.0" in out.message
    assert (folder / "install.ps1").read_bytes() == transport.release.installer
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
    assert ("ticket", "2.2.0", "win32", "AMD64") in transport.calls
    assert [c[0] for c in transport.calls] == ["installer", "manifest", "ticket"]       # verified BEFORE the ticket is asked for


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
    rel = make_release()
    broken = SimpleNamespace(update_ticket=lambda *a: (_ for _ in ()).throw(RuntimeError("boom")),
                             download_installer=lambda: rel.installer,
                             download_release_manifest=lambda: (rel.manifest, rel.sig))
    assert apply(tmp_path / "e", transport=broken)[0].reason == "io"
    assert apply(tmp_path / "f", transport=FakeTransport(signed=None))[0].reason == "no-installer"


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


# ── the pinned release key: what a hostile or stale manager cannot get run ────

def refused(tmp_path, reason, **kw):
    out, transport, runner = apply(tmp_path, **kw)
    assert not out.applied and runner.commands == [], out
    assert out.reason == reason, out
    assert ("ticket", "2.2.0", "win32", "AMD64") not in transport.calls          # no ticket spent on a refused update
    assert not (tmp_path / "vedha-agent" / "update" / "install.ps1").exists()     # nothing was written to be run
    return out


def test_without_a_pinned_key_it_will_not_run_anything_the_manager_serves(tmp_path):
    out = refused(tmp_path, "no-pin", pinned=False)
    assert "install command" in out.message


def test_a_damaged_pin_file_counts_as_no_pin(tmp_path):
    folder = tmp_path / "vedha-agent" / "release"
    folder.mkdir(parents=True)
    (folder / "trust.json").write_text("{nope")
    refused(tmp_path, "no-pin", pinned=False)


def test_an_installer_swapped_by_the_manager_is_refused(tmp_path):
    evil = b"# Vedha\nrun-something-else\n"
    out = refused(tmp_path, "untrusted", transport=FakeTransport(installer=evil))
    assert "installer-mismatch" in out.message


def test_a_manifest_signed_by_another_key_is_refused(tmp_path):
    other_key, other_spki = _keypair()
    rel = make_release(key=other_key, installer_spki=other_spki)
    out = refused(tmp_path, "untrusted", transport=FakeTransport(release=rel))
    assert "bad-signature" in out.message


def test_a_tampered_manifest_is_refused(tmp_path):
    rel = make_release()
    t = FakeTransport(release=rel, signed=(rel.manifest.replace(b"2.3.0", b"9.9.9"), rel.sig))
    assert "bad-signature" in refused(tmp_path, "untrusted", transport=t).message


def test_a_signed_installer_carrying_a_different_key_is_refused(tmp_path):
    _, other_spki = _keypair()
    rel = make_release(installer_spki=other_spki)                       # signed by the pinned key, but embeds another key
    assert "key-mismatch" in refused(tmp_path, "untrusted", transport=FakeTransport(release=rel)).message


def test_an_older_release_than_the_one_installed_is_refused(tmp_path):
    pin(tmp_path, release_version="1.0.900")
    out, _, runner = apply(tmp_path, pinned=False, transport=FakeTransport(release=make_release(version="1.0.500")))
    assert out.reason == "untrusted" and "older-release" in out.message and runner.commands == []


def test_the_same_release_version_is_not_an_older_release(tmp_path):
    pin(tmp_path, release_version="1.0.500")
    assert apply(tmp_path, pinned=False, transport=FakeTransport(release=make_release(version="1.0.500")))[0].applied


def test_an_expired_release_is_refused_and_a_valid_one_is_not(tmp_path):
    past = refused(tmp_path / "a", "untrusted", transport=FakeTransport(release=make_release(expires="2000-01-01T00:00:00+00:00")))
    assert "expired" in past.message
    future = make_release(expires="2999-01-01T00:00:00Z")
    assert apply(tmp_path / "b", transport=FakeTransport(release=future))[0].applied


def test_an_unreadable_expiry_is_refused_not_ignored(tmp_path):
    rel = make_release(expires="next tuesday")
    assert "malformed" in refused(tmp_path, "untrusted", transport=FakeTransport(release=rel)).message


def test_a_signed_release_that_offers_no_newer_agent_is_refused(tmp_path):
    rel = make_release(latest="2.2.0")                                  # the manager says 2.3.0, the signature says 2.2.0
    t = FakeTransport(release=rel)
    assert "not-newer" in refused(tmp_path, "untrusted", transport=t).message


def test_a_manager_offering_a_different_version_than_the_signed_release_is_refused(tmp_path):
    t = FakeTransport(release=make_release(latest="2.4.0"))             # signed for 2.4.0 ...
    t.reply["latest"] = "2.3.0"                                          # ... but the ticket says 2.3.0
    out, _, runner = apply(tmp_path, transport=t)
    assert out.reason == "untrusted" and "offer-mismatch" in out.message and runner.commands == []


def test_a_manifest_without_an_installer_entry_is_refused(tmp_path):
    rel = make_release(mutate=lambda m: m.pop("windows_installer"))
    assert "malformed" in refused(tmp_path, "untrusted", transport=FakeTransport(release=rel)).message


def test_verify_update_directly_reports_ok_with_the_manifest(tmp_path):
    rel = make_release()
    verdict = rt.verify_update(rt.Pin(PIN_SPKI, "1.0.400"), rel.manifest, rel.sig, rel.installer, current_agent_version="2.2.0")
    assert verdict.ok and verdict.reason == "ok" and verdict.manifest["version"] == "1.0.500"


def test_oversized_inputs_are_refused_before_any_crypto(tmp_path):
    verdict = rt.verify_update(rt.Pin(PIN_SPKI), b"x" * (rt.MAX_MANIFEST_BYTES + 1), "sig", b"", current_agent_version="2.2.0")
    assert verdict.reason == "malformed"


def test_the_agent_logs_how_the_last_update_ended(tmp_path, caplog):
    import logging
    folder = tmp_path / "vedha-agent" / "update"
    folder.mkdir(parents=True)
    assert au.report_last_update(tmp_path / "vedha-agent") == ""
    (folder / "last-update.json").write_text(json.dumps(
        {"result": "rolled-back", "from": "2.2.8", "to": "2.2.9", "reason": "the new agent stayed 'failed'"}))
    with caplog.at_level(logging.INFO, logger="agent.auto_update"):
        assert au.report_last_update(tmp_path / "vedha-agent") == "rolled-back"
    assert any(r.levelno == logging.WARNING and "2.2.8 -> 2.2.9" in r.getMessage() and "failed" in r.getMessage() for r in caplog.records)
    (folder / "last-update.json").write_text("{broken")
    assert au.report_last_update(tmp_path / "vedha-agent") == ""
    # and the start-up cleanup reports it too, without touching the record
    (folder / "last-update.json").write_text(json.dumps({"result": "updated", "from": "2.2.8", "to": "2.2.9"}))
    au.cleanup_after_update(tmp_path / "vedha-agent", runner=FakeRunner())
    assert (folder / "last-update.json").exists()
