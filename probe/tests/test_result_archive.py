"""
test_result_archive.py — the local result archive written before submission.

The operator needs to audit what a scan actually found BEFORE trusting what the
manager stored. The result spool cannot serve that purpose: it is a delivery
buffer and deletes each file the moment upload succeeds, so a healthy probe
leaves nothing behind.

The guarantee under test is identity: the JSON on disk is the object handed to
the transport, so an accuracy review of the file is a review of what the manager
received. And the archive is best-effort — a read-only filesystem must never
cost a completed scan.
"""

from __future__ import annotations

import json

import pytest

from agent import task_runner as tr
from agent.task_runner import TaskRunner, prepare_result_dir


@pytest.fixture(autouse=True)
def _reset_archive_latch():
    """The disable latch is module state; keep tests independent."""
    tr._ARCHIVE_DISABLED = False
    yield
    tr._ARCHIVE_DISABLED = False


def _runner(submitted: list, **kw) -> TaskRunner:
    return TaskRunner(
        http_get=lambda path: {"scope_cidrs": ["10.0.0.0/8"], "excluded_cidrs": []},
        submit_result=lambda job_id, payload: submitted.append((job_id, payload)) or True,
        run_scan_fn=kw.pop("run_scan_fn", None),
        **kw,
    )


def _job(job_id="job-1"):
    return {
        "job_id": job_id,
        "attempt_id": "att-1",
        "fence": 1,
        "engagement_id": "eng-1",
        "job_type": "port_scan",
        "params": {"targets": ["10.0.0.5"], "scope_cidrs": ["10.0.0.0/8"]},
    }


def _ok_result(**over):
    base = {
        "result_schema_version": "1.1", "ok": True, "outcome": "completed",
        "facts": [{"scanner": "port_scan", "target": "10.0.0.5", "port": 22,
                   "status": "open", "timestamp": "2026-01-01T00:00:00Z"}],
        "hosts": [{"ip": "10.0.0.5", "hostname": None, "ports": [{"port": 22}]}],
        "run_stats": {"host_count": 1, "open_ports": 1},
    }
    base.update(over)
    return base


@pytest.mark.result_archive
class TestArchiveIdentity:
    def test_archived_json_equals_the_submitted_payload(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path))
        submitted: list = []
        runner = _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result())

        runner.run_job(_job(), "agent-1")

        files = sorted(tmp_path.glob("result*.json"))
        assert len(files) == 1, f"expected exactly one archived result, got {files}"
        on_disk = json.loads(files[0].read_text())
        assert submitted, "nothing was submitted"
        _, sent = submitted[0]
        assert on_disk == json.loads(json.dumps(sent, default=str)), (
            "the archived file must be the payload the manager receives")
        assert on_disk["result"]["facts"][0]["port"] == 22

    def test_filename_is_result_plus_timestamp(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path))
        submitted: list = []
        _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result()).run_job(_job(), "a")
        name = next(iter(tmp_path.glob("result*.json"))).name
        assert name.startswith("result") and name.endswith(".json")
        stamp = name[len("result"):-len(".json")]
        # Project-local (IST) wall clock: 20260903T231550. Deliberately NO "Z" —
        # the archive is named in the operator's timezone, and a Z suffix would
        # claim UTC. Still fixed-width and lexicographically sortable.
        assert not stamp.endswith("Z"), f"local stamp must not claim UTC: {stamp!r}"
        assert len(stamp) == 15, f"unexpected stamp {stamp!r}"
        from datetime import datetime
        datetime.strptime(stamp, "%Y%m%dT%H%M%S")     # parses as a real instant

    def test_failure_envelopes_are_archived_too(self, tmp_path, monkeypatch):
        """A rejected job is exactly the case an operator wants to inspect."""
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path))
        submitted: list = []
        runner = _runner(submitted)
        bad = _job()
        bad["params"] = {"targets": ["203.0.113.9"], "scope_cidrs": ["10.0.0.0/8"]}

        runner.run_job(bad, "agent-1")

        files = sorted(tmp_path.glob("result*.json"))
        assert len(files) == 1
        assert json.loads(files[0].read_text())["success"] is False

    def test_two_jobs_in_the_same_second_do_not_clobber(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path))
        submitted: list = []
        runner = _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result())
        for i in range(3):
            runner.run_job(_job(f"job-{i}"), "agent-1")
        assert len(list(tmp_path.glob("result*.json"))) == 3

    def test_no_partial_files_are_left_behind(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path))
        submitted: list = []
        _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result()).run_job(_job(), "a")
        assert list(tmp_path.glob("*.partial")) == []


@pytest.mark.result_archive
class TestArchiveIsBestEffort:
    def test_unwritable_directory_does_not_fail_the_job(self, tmp_path, monkeypatch):
        """A read-only filesystem must cost a warning, never a scan result."""
        blocker = tmp_path / "not-a-dir"
        blocker.write_text("this is a file, so mkdir() below must fail")
        monkeypatch.setenv("PROBE_RESULT_DIR", str(blocker / "result"))
        submitted: list = []
        runner = _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result())

        outcome = runner.run_job(_job(), "agent-1")

        assert outcome.success is True
        assert submitted, "submission must proceed when archiving fails"
        assert tr._ARCHIVE_DISABLED is True, "the failure should latch, not warn per job"

    def test_empty_env_var_disables_archiving(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", "")
        submitted: list = []
        runner = _runner(submitted, run_scan_fn=lambda *a, **k: _ok_result())
        runner.run_job(_job(), "agent-1")
        assert submitted
        assert list(tmp_path.glob("result*.json")) == []

    def test_default_location_is_the_probe_root(self, monkeypatch):
        """Unset env => alongside agent/ scanner/ workflow/ (in the image, /app/result)."""
        monkeypatch.delenv("PROBE_RESULT_DIR", raising=False)
        target = tr._result_dir()
        assert target is not None
        assert target.name == "result"
        assert (target.parent / "agent").is_dir(), (
            "the archive must sit next to the probe's own packages")


@pytest.mark.result_archive
class TestPrepareAtStartup:
    """The agent creates the archive directory at boot so the operator sees the
    path immediately, and so an unwritable location is reported before a scan has
    already been run rather than after."""

    def test_creates_the_directory_including_parents(self, tmp_path, monkeypatch):
        target = tmp_path / "deep" / "nested" / "result"
        monkeypatch.setenv("PROBE_RESULT_DIR", str(target))
        assert not target.exists()
        assert prepare_result_dir() == target
        assert target.is_dir()

    def test_leaves_no_canary_file_behind(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path / "r"))
        prepare_result_dir()
        assert list((tmp_path / "r").iterdir()) == []

    def test_is_idempotent_across_restarts(self, tmp_path, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", str(tmp_path / "r"))
        assert prepare_result_dir() is not None
        assert prepare_result_dir() is not None

    def test_existing_but_unwritable_directory_is_caught_at_startup(
            self, tmp_path, monkeypatch):
        """The Linux bind-mount case: Docker creates the source as root, so the
        directory EXISTS but the probe's uid cannot write to it. mkdir(exist_ok)
        alone would not notice."""
        target = tmp_path / "readonly"
        target.mkdir()
        target.chmod(0o500)
        monkeypatch.setenv("PROBE_RESULT_DIR", str(target))
        try:
            assert prepare_result_dir() is None
            assert tr._ARCHIVE_DISABLED is True
        finally:
            target.chmod(0o700)

    def test_disabled_when_env_is_empty(self, monkeypatch):
        monkeypatch.setenv("PROBE_RESULT_DIR", "")
        assert prepare_result_dir() is None
        assert tr._ARCHIVE_DISABLED is False, "off by config is not a failure"

    def test_startup_failure_does_not_raise(self, tmp_path, monkeypatch):
        blocker = tmp_path / "file"
        blocker.write_text("not a directory")
        monkeypatch.setenv("PROBE_RESULT_DIR", str(blocker / "result"))
        assert prepare_result_dir() is None
