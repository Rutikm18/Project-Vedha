"""runtime_status.py — what the running agent is doing, written where a human can read it.

The agent runs headless on Windows (a Scheduled Task with no console), so the
installer, `vedha-agent status` and the support bundle cannot ask it anything.
Instead the running agent records its state in `status.json` next to its state
file, and those tools read it. Nothing secret goes in here: no tokens, no keys —
only a state, a short reason and the plain-language fix.

States (in the order a healthy agent passes through them):
  starting           process is up, loading configuration
  enrolling          registering with the manager (an install token auto-approves)
  awaiting-approval  needs a person to enter `pairing_code` in Fleet
  online             registered with the manager; streaming or polling for jobs
  retrying           the manager could not be reached yet; the agent keeps trying
  failed             gave up; `reason` and `remediation` say why and what to do

Writes are atomic, best effort, and never raise: reporting status must never be
the thing that stops an agent.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

STATES = ("starting", "enrolling", "awaiting-approval", "online", "retrying", "failed")
STALE_AFTER_SECONDS = 15 * 60       # a state this old, with a live process, is still current
FILE_NAME = "status.json"


def path_for(state_file: str | Path) -> Path:
    """status.json lives beside the agent's state file."""
    return Path(state_file).with_name(FILE_NAME)


def write(
    path: str | Path | None,
    state: str,
    *,
    detail: str = "",
    reason: str = "",
    remediation: str = "",
    pairing_code: str = "",
    pairing_url: str = "",
    version: str = "",
    manager: str = "",
    now: float | None = None,
) -> bool:
    """Record the agent's current state. True if written; never raises."""
    if not path or state not in STATES:
        return False
    stamp = now if now is not None else time.time()
    try:
        target = Path(path)
        previous = read(target)
        since = previous.get("since", stamp) if previous and previous.get("state") == state else stamp
        record: dict[str, Any] = {
            "state": state,
            "detail": detail[:300],
            "reason": reason[:200],
            "remediation": remediation[:400],
            "pairing_code": pairing_code[:32],
            "pairing_url": pairing_url[:300],
            "pid": os.getpid(),
            "version": version[:64],
            "manager": manager[:300],
            "since": since,
            "updated_at": stamp,
        }
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(".tmp")
        tmp.write_text(json.dumps(record), encoding="utf-8")
        os.replace(tmp, target)
        return True
    except OSError:
        return False


def read(path: str | Path) -> dict[str, Any] | None:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("state") in STATES else None


def process_alive(pid: Any) -> bool:
    """Is a process with this id running? Works on Windows and POSIX."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            handle = kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
            if not handle:
                return False
            try:
                code = ctypes.c_ulong()
                ok = kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
                return bool(ok) and code.value == 259           # STILL_ACTIVE
            finally:
                kernel32.CloseHandle(handle)
        except Exception:  # noqa: BLE001 — a probe of a process must never raise
            return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def effective(record: dict[str, Any] | None, *, now: float | None = None,
              alive=process_alive) -> dict[str, Any]:
    """Turn what was last written into what is true now: a record whose process is
    gone is not 'online', whatever it says."""
    stamp = now if now is not None else time.time()
    if not record:
        return {"state": "not-running", "running": False,
                "detail": "The agent has not written a status yet (not started, or not installed)."}
    running = alive(record.get("pid"))
    out = dict(record)
    out["running"] = running
    out["age_seconds"] = max(0, int(stamp - float(record.get("updated_at", stamp))))
    if not running:
        out["recorded_state"] = record.get("state")
        out["state"] = "not-running"
        out["detail"] = (f"The agent is not running (it last reported '{record.get('state')}'"
                         f"{': ' + record['reason'] if record.get('reason') else ''}).")
    return out
