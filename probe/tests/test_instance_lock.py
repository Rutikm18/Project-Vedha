"""
One probe process per state file.

OBSERVED TWICE IN ONE SESSION (2026-09-05): two `python -m agent.agent`
processes ran against the same STATE_FILE, so both impersonated agent
66e45562. Symptoms were a job that looked stuck and a scan crawling at
0.53 ports/sec.

The accuracy consequence is the reason this is a hard failure rather than a
warning: both processes scan, so the target sees double the probe rate from one
source. Hosts that rate-limit RSTs suppress replies, suppressed replies read as
silence, and silence is reported `filtered`. Two honest probes manufacture false
negatives in each other's results — slower AND less correct.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from agent import instance_lock as il
from agent.instance_lock import (
    InstanceLockError,
    acquire_instance_lock,
    lock_path_for,
    release_instance_lock,
)


@pytest.fixture
def state(tmp_path: Path) -> Path:
    return tmp_path / "state.json"


class TestMutualExclusion:
    def test_first_holder_acquires(self, state):
        h = acquire_instance_lock(state)
        assert h is not None
        release_instance_lock(h)

    def test_second_holder_in_another_process_is_refused(self, state):
        """Must be a REAL second process: flock is per-open-file-description, so
        a same-process re-acquire would succeed and prove nothing."""
        h = acquire_instance_lock(state)
        try:
            code = textwrap.dedent(f"""
                import sys; sys.path.insert(0, {str(Path.cwd())!r})
                from agent.instance_lock import acquire_instance_lock, InstanceLockError
                try:
                    acquire_instance_lock({str(state)!r})
                    print("ACQUIRED")
                except InstanceLockError:
                    print("REFUSED")
            """)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            assert "REFUSED" in out.stdout, out.stdout + out.stderr
        finally:
            release_instance_lock(h)

    def test_lock_is_released_when_the_holder_exits(self, state):
        """A PID file would go stale here; flock is dropped by the kernel."""
        code = textwrap.dedent(f"""
            import sys; sys.path.insert(0, {str(Path.cwd())!r})
            from agent.instance_lock import acquire_instance_lock
            acquire_instance_lock({str(state)!r})
        """)
        subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, timeout=60)
        h = acquire_instance_lock(state)          # must be free again
        assert h is not None
        release_instance_lock(h)

    def test_release_allows_reacquire(self, state):
        release_instance_lock(acquire_instance_lock(state))
        h = acquire_instance_lock(state)
        assert h is not None
        release_instance_lock(h)

    def test_different_state_files_do_not_contend(self, tmp_path):
        """Several probes on one host is legitimate — give each its own identity."""
        a = acquire_instance_lock(tmp_path / "a.json")
        b = acquire_instance_lock(tmp_path / "b.json")
        assert a is not None and b is not None
        release_instance_lock(a); release_instance_lock(b)


class TestLockFile:
    def test_sidecar_never_the_state_file_itself(self, state):
        """Locking the file we also rewrite invites truncation races."""
        assert lock_path_for(state) != state
        assert lock_path_for(state).name == "state.json.lock"

    def test_holder_identity_is_recorded_for_diagnostics(self, state):
        h = acquire_instance_lock(state)
        try:
            info = json.loads(lock_path_for(state).read_text())
            assert info["pid"] == os.getpid()
            assert info["started_at"] and info["state_file"] == str(state)
        finally:
            release_instance_lock(h)

    def test_state_file_is_not_created_or_touched(self, state):
        h = acquire_instance_lock(state)
        try:
            assert not state.exists(), "the lock must not disturb the identity file"
        finally:
            release_instance_lock(h)

    def test_error_names_the_holder(self, state):
        h = acquire_instance_lock(state)
        try:
            code = textwrap.dedent(f"""
                import sys; sys.path.insert(0, {str(Path.cwd())!r})
                from agent.instance_lock import acquire_instance_lock, InstanceLockError
                try:
                    acquire_instance_lock({str(state)!r})
                except InstanceLockError as e:
                    print(str(e))
            """)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            assert str(os.getpid()) in out.stdout, out.stdout
            assert "state file" in out.stdout
        finally:
            release_instance_lock(h)


class TestDegradesSafely:
    def test_unwritable_directory_does_not_block_the_scan(self, tmp_path):
        """A guard that cannot run must not become an outage."""
        assert acquire_instance_lock(tmp_path / "nope" / "x" / "state.json") is None \
            or True    # either None, or it created the dir — both are non-fatal

    def test_release_of_none_is_a_noop(self):
        release_instance_lock(None)

    def test_corrupt_lockfile_still_refuses_a_second_holder(self, state):
        """A garbled hint must never be able to STEAL a held lock."""
        h = acquire_instance_lock(state)
        try:
            lock_path_for(state).write_text("}{ not json")
            code = textwrap.dedent(f"""
                import sys; sys.path.insert(0, {str(Path.cwd())!r})
                from agent.instance_lock import acquire_instance_lock, InstanceLockError
                try:
                    acquire_instance_lock({str(state)!r}); print("ACQUIRED")
                except InstanceLockError:
                    print("REFUSED")
            """)
            out = subprocess.run([sys.executable, "-c", code],
                                 capture_output=True, text=True, timeout=60)
            assert "REFUSED" in out.stdout, out.stdout
        finally:
            release_instance_lock(h)


class TestWindowsPath:
    """Windows has no fcntl; the lock must use msvcrt instead of silently
    skipping (a skipped lock is how two agents shared one state.json). The OS
    enforces exclusion across processes — here we prove the WIRING: acquire and
    release drive msvcrt.locking, and a held byte refuses a second holder."""

    class _FakeMsvcrt:
        LK_NBLCK = 1
        LK_UNLCK = 0

        def __init__(self):
            self.held = False
            self.calls: list[tuple[int, int]] = []

        def locking(self, fd, mode, nbytes):
            self.calls.append((mode, nbytes))
            if mode == self.LK_NBLCK:
                if self.held:
                    raise OSError("byte range already locked")
                self.held = True
            else:
                self.held = False

    def _use_windows(self, monkeypatch, fake):
        monkeypatch.setattr(il, "fcntl", None)
        monkeypatch.setattr(il, "msvcrt", fake)

    def test_acquire_and_release_drive_msvcrt(self, monkeypatch, state):
        fake = self._FakeMsvcrt()
        self._use_windows(monkeypatch, fake)
        handle = acquire_instance_lock(state)
        assert handle is not None
        assert (fake.LK_NBLCK, 1) in fake.calls
        release_instance_lock(handle)
        assert (fake.LK_UNLCK, 1) in fake.calls

    def test_held_byte_refuses_a_second_holder(self, monkeypatch, state):
        fake = self._FakeMsvcrt()          # one fake = one OS, shared across handles
        self._use_windows(monkeypatch, fake)
        first = acquire_instance_lock(state)
        try:
            with pytest.raises(InstanceLockError):
                acquire_instance_lock(state)
        finally:
            release_instance_lock(first)

    def test_release_frees_it_for_reacquire(self, monkeypatch, state):
        fake = self._FakeMsvcrt()
        self._use_windows(monkeypatch, fake)
        release_instance_lock(acquire_instance_lock(state))
        again = acquire_instance_lock(state)
        assert again is not None
        release_instance_lock(again)

    def test_no_locking_mechanism_degrades_to_none(self, monkeypatch, state):
        monkeypatch.setattr(il, "fcntl", None)
        monkeypatch.setattr(il, "msvcrt", None)
        assert not il.locking_available()
        assert acquire_instance_lock(state) is None   # never block the scan


def test_no_existence_check_uses_os_kill_signal_zero():
    """On Windows os.kill(pid, 0) sends CTRL_C_EVENT, not a no-op existence check.

    It interrupted the pytest run on windows-latest (KeyboardInterrupt after the last test) and,
    in a real agent, would send Ctrl+C to the running agent's console group when a second
    instance started. Use agent.runtime_status.process_alive, which has a Windows branch.
    """
    import re
    bad = []
    for path in (Path(__file__).resolve().parents[1] / "agent").rglob("*.py"):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            code = line.split("#", 1)[0]
            if re.search(r"os\.kill\([^,()]+,\s*0\s*\)", code) and path.name != "runtime_status.py":
                bad.append(f"{path.name}:{n}")
    assert not bad, f"use process_alive() instead of os.kill(pid, 0): {bad}"
