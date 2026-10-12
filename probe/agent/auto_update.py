"""auto_update.py — apply an agent update by itself (Windows, OFF by default).

update_check.py already asks the manager "is there a newer agent?". This is the next step:
when the answer is yes AND the owner has switched it on, the agent updates itself by running
the SAME installer a person would run, so every safety rule of the installer applies unchanged
(signature and SHA-256 checks against the signed manifest, no downgrade, in-place replace, the
agent's identity and saved results kept).

How, in order:
  1. Gates. Switched on (PROBE_AUTO_UPDATE=on, a line in agent.env, which the installer keeps
     across updates), Windows, no scan running right now, and this version was not already
     attempted in the last 24 hours (so a failing update cannot loop).
  2. Download the installer script and the signed release manifest from the manager, and CHECK
     them against the release key pinned on this machine (release_trust.py): the manifest must be
     signed by that key, list this exact script's SHA-256, offer a newer agent, not be older than
     the newest release already installed here, and not be expired. A manager that has been broken
     into cannot get a different script run this way.
  3. Ask the manager for an update ticket (a short-lived, single-use download token that only
     exists when the manager has decided this agent should update; see
     manager/backend/app/services/agent_update_ticket.py).
  4. Run the verified script as SYSTEM through a ONE-SHOT Scheduled Task, not as a child of this
     process: the installer stops this agent's own task, and a child process would die with it.
  5. The installer replaces the agent, starts it, and waits up to 5 minutes for it to connect. If
     it does not, the installer puts the previous version back (program, settings, identity) and
     records "rolled-back" in update/last-update.json, which this agent logs when it next starts.

What it does NOT do yet (be honest about it):
  * No staged rollout or pause switch: every agent with this on updates when the manager offers.
  * A machine installed before the pin existed has no pinned key: it refuses to update itself
    (reason "no-pin") until the install command is run once more.
  * The first install is trusted on first use (TLS to the manager); the pin protects what follows.
  * Not run on a real Windows machine yet.
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

LOG = logging.getLogger("agent.auto_update")

TASK_NAME = "VedhaAgentUpdate"
RETRY_AFTER_SECONDS = 24 * 3600
_MAX_INSTALLER_BYTES = 2 * 1024 * 1024

# ── switch ───────────────────────────────────────────────────────────────────

def enabled(env: dict[str, str] | None = None) -> bool:
    value = (env if env is not None else os.environ).get("PROBE_AUTO_UPDATE", "off")
    return value.strip().lower() in ("on", "1", "true", "yes", "enabled")


# ── idle gate: never replace the agent while it is scanning ──────────────────

_lock = threading.Lock()
_running_jobs = 0


def mark_job_started() -> None:
    global _running_jobs
    with _lock:
        _running_jobs += 1


def mark_job_finished() -> None:
    global _running_jobs
    with _lock:
        _running_jobs = max(0, _running_jobs - 1)


def is_busy() -> bool:
    with _lock:
        return _running_jobs > 0


# ── result ───────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Outcome:
    applied: bool
    reason: str      # off | unsupported | busy | recently-tried | no-pin | untrusted | no-ticket | no-installer | io | schedule | started
    message: str

    @property
    def retry_soon(self) -> bool:
        """True when a later attempt is likely to succeed (the agent was busy)."""
        return self.reason == "busy"


# ── paths and commands (pure, tested) ────────────────────────────────────────

def data_dir(env: dict[str, str] | None = None) -> Path:
    env = env if env is not None else os.environ
    state = env.get("STATE_FILE", "").strip()
    if state:
        return Path(state).parent
    base = env.get("ProgramData") or env.get("PROGRAMDATA") or r"C:\ProgramData"
    return Path(base) / "vedha-agent"


def update_dir(base: Path) -> Path:
    return base / "update"


def launcher_text(*, installer: str, manager: str, ticket_file: str, log_file: str) -> str:
    """run-update.cmd. Kept as a file because schtasks /TR is limited to 261 characters and
    has awkward quoting. The ticket is read from its own file (single use, 15 minutes), so the
    launcher itself holds no secret. install.ps1 here is the manager-served installer
    (probe/windows/install-remote.ps1): it takes -Manager and -Token, verifies the signed
    manifest, downloads the package with the token, and keeps the agent's scope when -Scope is
    not given."""
    powershell = r"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
    return (
        "@echo off\r\n"
        f'set /p VEDHA_TICKET=<"{ticket_file}"\r\n'
        f'"{powershell}" -NoProfile -ExecutionPolicy Bypass -File "{installer}" '
        f'-Manager "{manager}" -Token "%VEDHA_TICKET%" > "{log_file}" 2>&1\r\n'
        f'del /f /q "{ticket_file}" >nul 2>&1\r\n'
    )


def create_task_command(launcher: str) -> list[str]:
    return ["schtasks", "/Create", "/TN", TASK_NAME, "/TR", launcher, "/SC", "ONCE", "/ST", "00:00",
            "/RU", "SYSTEM", "/RL", "HIGHEST", "/F"]


def run_task_command() -> list[str]:
    return ["schtasks", "/Run", "/TN", TASK_NAME]


def delete_task_command() -> list[str]:
    return ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"]


# ── attempt guard ────────────────────────────────────────────────────────────

def _attempt_file(base: Path) -> Path:
    return update_dir(base) / "last-attempt.json"


def recently_attempted(base: Path, version: str, now: float) -> bool:
    try:
        data = json.loads(_attempt_file(base).read_text(encoding="utf-8"))
        return data.get("version") == version and now - float(data.get("at", 0)) < RETRY_AFTER_SECONDS
    except (OSError, ValueError, TypeError):
        return False


def _record_attempt(base: Path, version: str, now: float) -> None:
    _attempt_file(base).write_text(json.dumps({"version": version, "at": now}), encoding="utf-8")


# ── the update ───────────────────────────────────────────────────────────────

Runner = Callable[[list[str]], Any]


def _default_runner(cmd: list[str]) -> Any:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)


def apply_update(
    transport: Any,
    info: Any,
    *,
    manager_url: str,
    platform: str,
    architecture: str,
    env: dict[str, str] | None = None,
    base: Path | None = None,
    now: float | None = None,
    runner: Runner = _default_runner,
) -> Outcome:
    """Start the update. Never raises; the Outcome says what happened and why."""
    from agent import release_trust, update_check

    if not enabled(env):
        return Outcome(False, "off", "Automatic update is off (set PROBE_AUTO_UPDATE=on in agent.env to enable it).")
    if not platform.startswith("win"):
        return Outcome(False, "unsupported", "Automatic update is only available for the Windows agent so far.")
    if is_busy():
        return Outcome(False, "busy", "A scan is running; the update will be tried again when the agent is idle.")
    base = base if base is not None else data_dir(env)
    now = now if now is not None else time.time()
    if recently_attempted(base, info.latest, now):
        return Outcome(False, "recently-tried",
                       f"Version {info.latest} was already attempted in the last 24 hours; not trying again yet.")
    if " " in str(base):
        return Outcome(False, "unsupported", "The agent's data folder path contains a space; run the installer by hand.")

    pin = release_trust.load_pin(base)
    if pin is None:
        return Outcome(False, "no-pin",
                       "This computer has no pinned release key (the agent was installed before keys were pinned), "
                       "so it will not run an installer the manager serves. Run the install command from Fleet once "
                       "more to pin it.")

    try:
        script = transport.download_installer()
        if not script:
            return Outcome(False, "no-installer", "Could not download the installer from the manager.")
        if len(script) > _MAX_INSTALLER_BYTES:
            return Outcome(False, "no-installer", "The installer the manager sent is larger than expected; not running it.")
        signed = transport.download_release_manifest()
        if not signed:
            return Outcome(False, "no-installer", "Could not download the signed release manifest from the manager.")
        verdict = release_trust.verify_update(pin, signed[0], signed[1], script, current_agent_version=info.current)
        if not verdict.ok:
            LOG.warning("auto-update refused (%s): %s", verdict.reason, verdict.message)
            return Outcome(False, "untrusted", f"Update refused ({verdict.reason}): {verdict.message}")

        reply = transport.update_ticket(info.current, platform, architecture)
        ticket = reply.get("ticket") if isinstance(reply, dict) else None
        latest = reply.get("latest") if isinstance(reply, dict) else None
        # The manager decides, but the agent re-checks: never act on a stale or hostile reply.
        if not (isinstance(ticket, str) and reply.get("update_available") is True
                and update_check.is_newer(latest, info.current)):
            return Outcome(False, "no-ticket", "The manager did not offer an update ticket.")
        if str((verdict.manifest or {}).get("agent_version")) != str(latest):
            return Outcome(False, "untrusted",
                           "Update refused (offer-mismatch): the manager offered a different agent version than the signed release lists.")

        folder = update_dir(base)
        folder.mkdir(parents=True, exist_ok=True)
        installer = folder / "install.ps1"
        ticket_file = folder / "ticket.txt"
        log_file = folder / "update.log"
        launcher = folder / "run-update.cmd"
        installer.write_bytes(script)
        ticket_file.write_bytes(ticket.encode("ascii"))
        # Bytes, not write_text: on Windows text mode would turn the CRLFs into CR CR LF.
        launcher.write_bytes(launcher_text(installer=str(installer), manager=manager_url.rstrip("/"),
                                           ticket_file=str(ticket_file), log_file=str(log_file)).encode("ascii"))
        _record_attempt(base, str(latest), now)
    except Exception as exc:  # noqa: BLE001 — an update attempt must never stop the agent
        LOG.warning("auto-update could not prepare: %r", exc)
        return Outcome(False, "io", f"Could not prepare the update: {exc}")

    for command in (create_task_command(str(launcher)), run_task_command()):
        try:
            result = runner(command)
            code = getattr(result, "returncode", 0)
        except Exception as exc:  # noqa: BLE001
            return Outcome(False, "schedule", f"Could not start the update task: {exc}")
        if code != 0:
            detail = (getattr(result, "stderr", "") or getattr(result, "stdout", "") or "").strip()[:200]
            return Outcome(False, "schedule", f"Could not start the update task ({command[1]} exit {code}): {detail}")
    return Outcome(True, "started",
                   f"Updating the agent from {info.current} to {latest}. The agent will restart; "
                   f"the installer's output is in {log_file}.")


def report_last_update(base: Path) -> str:
    """Log how the installer's last update ended (update/last-update.json), once per start. A
    rolled-back update is a WARNING: the new version could not connect and the old one is running.
    Returns the result word ('' when there is no record)."""
    try:
        data = json.loads((update_dir(base) / "last-update.json").read_text(encoding="utf-8-sig"))
        result = str(data.get("result", ""))[:40]
        text = f"{data.get('from', '?')} -> {data.get('to', '?')}"
    except (OSError, ValueError, AttributeError):
        return ""
    if result in ("rolled-back", "rollback-failed"):
        LOG.warning("the last update (%s) ended as %s: %s", text, result, str(data.get("reason", ""))[:200])
    elif result:
        LOG.info("the last update (%s) ended as %s", text, result)
    return result


def cleanup_after_update(base: Path | None = None, *, runner: Runner = _default_runner,
                         env: dict[str, str] | None = None) -> None:
    """Called when the agent starts: remove the one-shot task and the downloaded installer and
    ticket. The log and the attempt record are kept for diagnosis."""
    base = base if base is not None else data_dir(env)
    folder = update_dir(base)
    if not folder.exists():
        return
    report_last_update(base)
    try:
        runner(delete_task_command())
    except Exception:  # noqa: BLE001
        pass
    for name in ("install.ps1", "ticket.txt", "run-update.cmd"):
        try:
            (folder / name).unlink()
        except OSError:
            pass
