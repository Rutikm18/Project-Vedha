"""
instance_lock.py — one probe process per state file.

WHY THIS EXISTS (observed 2026-09-05, twice in one session).

The probe's identity lives in STATE_FILE: `agent_id`, the agent token, the device
refresh secret. Start a second probe with the same STATE_FILE and you do not get
two probes — you get two processes impersonating ONE probe. Every consequence of
that is bad, and none of it is obvious from the logs:

  * **Accuracy damage, which is the worst of it.** Both processes scan, so the
    target sees double the probe rate from a single source. Hosts that rate-limit
    their RSTs (common — Windows does it) start suppressing replies, and
    suppressed replies are read as silence, which is reported as `filtered`. Two
    honest probes therefore manufacture false negatives in each other's results.
    The scan gets slower AND less correct at the same time.
  * **Lease and fence conflicts.** Both heartbeat for the same `agent_id`. One
    renews a job attempt; the other reports `current_job_id=None` and clears it.
    A result arriving under a superseded fence is rejected outright.
  * **Double claiming.** Both poll `/agents/{id}/jobs`, so one queue entry can be
    executed twice, wasting the queue cap and the target's patience.
  * **Credential churn.** Both may re-register or refresh, and each
    re-registration mints a new `agent_id` — orphaning any job pinned to the old
    one (see the manager's pinned-agent fallback).

The lock is an ADVISORY `flock` on a sidecar file rather than a PID file on
purpose: the kernel drops a `flock` when the holder dies, however it dies
(SIGKILL, panic, container stop). A PID file survives that and goes stale, which
means the recovery path — the one that runs when things are already broken — is
the one most likely to be wrong. The PID we record is for the ERROR MESSAGE only;
it is never what decides whether the lock is held.

Scope: the lock covers one STATE_FILE. Running several probes on one host is
perfectly legitimate — give each its own STATE_FILE and each gets its own
identity, which is what you actually wanted.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import IO

try:                                    # POSIX only; the probe targets Linux/macOS
    import fcntl
except ImportError:                     # pragma: no cover - non-POSIX
    fcntl = None                        # type: ignore[assignment]


class InstanceLockError(RuntimeError):
    """Another live process already owns this state file."""


def lock_path_for(state_file: str | Path) -> Path:
    """Sidecar lock path for a state file. Never the state file itself — locking
    the file we also rewrite invites truncation races."""
    p = Path(state_file)
    return p.with_name(p.name + ".lock")


def _holder_hint(path: Path) -> str:
    """Best-effort description of the current holder, for the error message only.

    Never used to DECIDE anything: a stale or garbled hint must not be able to
    steal a lock the kernel still considers held.
    """
    try:
        info = json.loads(path.read_text() or "{}")
    except (OSError, ValueError):
        return "another probe process"
    pid = info.get("pid")
    started = info.get("started_at")
    if not pid:
        return "another probe process"
    alive = ""
    try:
        os.kill(int(pid), 0)            # signal 0 = existence check, no effect
        alive = " (running)"
    except (OSError, ValueError, TypeError):
        alive = " (may have exited — retry)"
    return f"PID {pid}{alive}" + (f", started {started}" if started else "")


def acquire_instance_lock(state_file: str | Path) -> IO | None:
    """Take the single-instance lock for `state_file`.

    Returns the open handle, which the CALLER MUST KEEP for the process lifetime
    — closing it (or letting it be garbage-collected) releases the lock. Returns
    None where locking is unavailable (no fcntl), because refusing to run would
    be a worse failure than not having the guard.

    Raises InstanceLockError when another live process holds it.
    """
    path = lock_path_for(state_file)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None                     # unwritable dir — do not block the scan
    if fcntl is None:                   # pragma: no cover - non-POSIX
        return None

    try:
        handle = open(path, "a+")       # never truncate before we own the lock
    except OSError:
        return None

    try:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        hint = _holder_hint(path)
        handle.close()
        raise InstanceLockError(
            f"another Vedha probe is already using this state file "
            f"({state_file}): {hint}"
        ) from None

    # We own it — now it is safe to record who we are, for diagnostics.
    try:
        handle.seek(0)
        handle.truncate()
        handle.write(json.dumps({
            "pid": os.getpid(),
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "state_file": str(state_file),
        }))
        handle.flush()
        os.fsync(handle.fileno())
    except OSError:
        pass                            # the lock is what matters, not the note
    return handle


def release_instance_lock(handle: IO | None) -> None:
    """Release explicitly. Process exit would do this anyway — this is for tests
    and for a clean shutdown path."""
    if handle is None:
        return
    try:
        if fcntl is not None:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError:
        pass
    try:
        handle.close()
    except OSError:
        pass
