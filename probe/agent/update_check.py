"""update_check.py — is a newer agent available? (version management only)

The agent asks its manager "is there a newer agent than mine?" once when it
starts and then every few hours while it runs. The manager owns the answer: it
knows which release it is serving. This module only asks, double-checks the
answer, and tells a person.

What it does:
  * start-up check — if a newer version exists and a person is at the terminal,
    ask "update now? [y/N]"; a headless agent (service, container) only logs it.
  * periodic check — logs a newer version once and never prompts.

What it deliberately does NOT do yet: download or install anything. Answering
yes records the intent and prints the manual update step; the authorised
download route is a later phase (request_update is the single place to fill in).

Safety rules baked in:
  * best effort — a check never raises into the agent and never delays a scan;
  * the agent re-validates the manager's answer and never accepts a version that
    is not strictly newer (a stale or hostile reply cannot trigger a downgrade);
  * an unattended agent is never blocked on a prompt (30 s timeout, default no).

Environment:
  PROBE_UPDATE_CHECK=off                  disable the check entirely
  PROBE_UPDATE_CHECK_INTERVAL_HOURS=6     periodic interval (1–168)
"""
from __future__ import annotations

import logging
import os
import random
import re
import sys
import threading
from dataclasses import dataclass
from typing import Any, Callable

LOG = logging.getLogger("agent.update_check")

DEFAULT_INTERVAL_HOURS = 6.0
MIN_INTERVAL_HOURS = 1.0
MAX_INTERVAL_HOURS = 168.0
PROMPT_TIMEOUT_SECONDS = 30.0
FIRST_CHECK_SECONDS = 180.0        # with auto-update on, look soon after start instead of in 6 h
RETRY_SOON_SECONDS = 15 * 60.0     # the agent was busy scanning: try again when it may be idle
_JITTER = 0.10  # ±10 %, so a fleet restarted together does not call in lockstep

_VERSION_RE = re.compile(r"\d+(\.\d+){0,3}")


# ── versions ─────────────────────────────────────────────────────────────────

def parse_version(text: Any) -> tuple[int, ...] | None:
    """'2.1.0' -> (2, 1, 0). Tolerates a leading 'v' and a '-rc1' / '+build'
    suffix (ignored). Anything else is None, never a guess."""
    if not isinstance(text, str):
        return None
    core = re.split(r"[-+]", text.strip().lstrip("vV"), maxsplit=1)[0]
    if not _VERSION_RE.fullmatch(core):
        return None
    return tuple(int(part) for part in core.split("."))


def is_newer(latest: Any, current: Any) -> bool:
    """True only when both parse and `latest` is strictly greater."""
    a, b = parse_version(latest), parse_version(current)
    if a is None or b is None:
        return False
    width = max(len(a), len(b))
    return a + (0,) * (width - len(a)) > b + (0,) * (width - len(b))


# ── settings ─────────────────────────────────────────────────────────────────

def enabled(env: dict[str, str] | None = None) -> bool:
    value = (env if env is not None else os.environ).get("PROBE_UPDATE_CHECK", "on")
    return value.strip().lower() not in ("off", "0", "false", "no", "disabled")


def interval_hours(env: dict[str, str] | None = None) -> float:
    raw = (env if env is not None else os.environ).get("PROBE_UPDATE_CHECK_INTERVAL_HOURS", "")
    try:
        hours = float(raw) if raw.strip() else DEFAULT_INTERVAL_HOURS
    except ValueError:
        hours = DEFAULT_INTERVAL_HOURS
    return min(MAX_INTERVAL_HOURS, max(MIN_INTERVAL_HOURS, hours))


# ── the answer ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class UpdateInfo:
    available: bool
    current: str
    latest: str = ""
    message: str = ""


def interpret(current: str, body: Any) -> UpdateInfo | None:
    """Turn the manager's reply into an UpdateInfo, or None when it is unusable.
    `available` is true only if the manager says so AND the version really is
    newer than ours."""
    if not isinstance(body, dict):
        return None
    latest = body.get("latest")
    latest = latest if isinstance(latest, str) else ""
    message = body.get("message")
    message = message[:300] if isinstance(message, str) else ""
    available = body.get("update_available") is True and is_newer(latest, current)
    return UpdateInfo(available=available, current=current, latest=latest if available else "", message=message)


def check(transport: Any, current: str, *, platform: str, architecture: str) -> UpdateInfo | None:
    """Ask the manager. Never raises; None means 'could not find out'."""
    try:
        return interpret(current, transport.update_check(current, platform, architecture))
    except Exception as exc:  # best effort by design
        LOG.debug("update check failed: %r", exc)
        return None


def update_hint(platform: str) -> str:
    """The manual update step available today. Re-running the installer upgrades
    in place and keeps the agent's identity."""
    if platform.startswith("win"):
        return ("run install.cmd from the newest Vedha agent package as Administrator "
                "(it replaces the agent and keeps its identity).")
    return ("run the install command from Fleet → Add agent again "
            "(it replaces the agent and keeps its identity).")


@dataclass(frozen=True)
class ApplyResult:
    applied: bool
    message: str


def request_update(info: UpdateInfo, platform: str) -> ApplyResult:
    """The one place the automatic download/install plugs in later. Today it only
    explains the manual step, because the authorised download route is not
    enabled yet."""
    return ApplyResult(
        applied=False,
        message=(f"Automatic download is not enabled yet. To move to {info.latest}, "
                 + update_hint(platform)),
    )


# ── talking to a person ──────────────────────────────────────────────────────

def can_prompt(stdin: Any = None, stdout: Any = None) -> bool:
    """True only when a person can answer: both ends are a terminal."""
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    try:
        return bool(stdin.isatty() and stdout.isatty())
    except (AttributeError, ValueError, OSError):
        return False


def ask_yes_no(question: str, *, input_fn: Callable[[str], str] = input,
               timeout: float = PROMPT_TIMEOUT_SECONDS) -> bool:
    """Ask, wait up to `timeout` seconds, default NO. Runs the read on a daemon
    thread so an unattended terminal can never hold the agent at its prompt."""
    answer: list[str] = []

    def _read() -> None:
        try:
            answer.append(input_fn(question))
        except (EOFError, KeyboardInterrupt, OSError):
            pass

    reader = threading.Thread(target=_read, name="update-prompt", daemon=True)
    reader.start()
    reader.join(timeout)
    return bool(answer) and answer[0].strip().lower() in ("y", "yes")


def run_startup_check(
    transport: Any,
    current: str,
    *,
    platform: str,
    architecture: str,
    say: Callable[[str], None],
    interactive: bool | None = None,
    input_fn: Callable[[str], str] = input,
    timeout: float = PROMPT_TIMEOUT_SECONDS,
) -> UpdateInfo | None:
    """The check made every time the agent starts. Returns what it learned."""
    if not enabled():
        return None
    info = check(transport, current, platform=platform, architecture=architecture)
    if info is None or not info.available:
        return info

    say(f"A newer Vedha agent is available: {info.latest} (this one is {info.current}).")
    if info.message:
        say(f"  {info.message}")
    if not (can_prompt() if interactive is None else interactive):
        say("  Not applied: no one is at this terminal. To update, " + update_hint(platform))
        return info
    if ask_yes_no("Update to the new version now? [y/N] ", input_fn=input_fn, timeout=timeout):
        say(request_update(info, platform).message)
    else:
        say(f"  Staying on {info.current}. You will be asked again the next time the agent starts.")
    return info


# ── while running ────────────────────────────────────────────────────────────

class PeriodicUpdateChecker:
    """Re-checks every few hours and logs a newer version once. Never prompts and
    never applies anything: nobody is at the keyboard of a long-running agent."""

    def __init__(self, transport: Any, current: str, *, platform: str, architecture: str,
                 say: Callable[[str], None], hours: float | None = None,
                 apply: Callable[[UpdateInfo], Any] | None = None) -> None:
        # `apply` is the optional auto-update hook (agent/auto_update.py). It is only called for
        # a version the manager offered and the agent re-validated as strictly newer. It returns
        # an object with `.message` and `.retry_soon`, or None.
        self._apply = apply
        self._retry_soon = False
        self._first = True
        self._transport = transport
        self._current = current
        self._platform = platform
        self._architecture = architecture
        self._say = say
        self._hours = hours if hours is not None else interval_hours()
        self._announced = ""
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def delay_seconds(self) -> float:
        if self._apply is not None and self._first:
            self._first = False
            return FIRST_CHECK_SECONDS * (1.0 + random.uniform(-_JITTER, _JITTER))
        if self._retry_soon:
            self._retry_soon = False
            return RETRY_SOON_SECONDS * (1.0 + random.uniform(-_JITTER, _JITTER))
        return self._hours * 3600.0 * (1.0 + random.uniform(-_JITTER, _JITTER))

    def check_once(self) -> UpdateInfo | None:
        info = check(self._transport, self._current,
                     platform=self._platform, architecture=self._architecture)
        if info is not None and info.available and info.latest != self._announced:
            self._announced = info.latest
            self._say(f"A newer Vedha agent is available: {info.latest} (this one is {info.current}). "
                      + ("Automatic update is on." if self._apply is not None
                         else "It will be offered the next time the agent is started in a terminal."))
        if info is not None and info.available and self._apply is not None:
            try:
                outcome = self._apply(info)
            except Exception as exc:  # noqa: BLE001 — an update attempt never stops the agent
                LOG.warning("auto-update hook failed: %r", exc)
                outcome = None
            if outcome is not None:
                self._say(f"  {outcome.message}")
                self._retry_soon = bool(getattr(outcome, "retry_soon", False))
        return info

    def _loop(self) -> None:
        while not self._stop.wait(self.delay_seconds()):
            self.check_once()

    def start(self) -> None:
        if self._thread is not None or not enabled():
            return
        self._thread = threading.Thread(target=self._loop, name="update-check", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
