"""supervisor.py — restart supervisor with a per-class policy (0b contract).

- success        → stop.
- fatal-config   → stop immediately (no backoff — the config won't fix itself).
- fatal-identity → bounded re-enroll attempts (no backoff between).
- retryable      → capped retries with duration-based backoff.
- awaiting-approval → poll (does NOT count toward the restart cap).
- kill switch    → stop immediately.

Backoff is DURATION-based (`sleep(seconds)` derived from a counter), never
computed from wall-clock timestamps, so an NTP step can't cause a retry storm or
a multi-hour stall. The restart cap (`max_retries`) is the StartLimitBurst
equivalent that keeps a deliberate stop from looking like malware fighting
removal.
"""
from __future__ import annotations

import time
from typing import Callable

from agent import exit_state


def supervise(
    cmd,
    *,
    spawn: Callable[[object], int],
    sleep: Callable[[float], None] = time.sleep,
    max_retries: int = 6,
    poll_interval: float = 5.0,
    backoff_cap: float = 30.0,
    stop_check: Callable[[], bool] | None = None,
) -> int:
    stop_check = stop_check or (lambda: False)
    heal = 0
    while True:
        if stop_check():
            return 0
        code = spawn(cmd)
        cls = exit_state.class_for_code(code)

        if cls == "success":
            return code
        if cls == "fatal-config":
            return code
        if cls == "awaiting-approval":
            sleep(poll_interval)      # poll; not counted toward the cap
            continue

        # retryable / fatal-identity / unknown(→retryable)
        heal += 1
        if heal >= max_retries:
            return code
        if cls == "fatal-identity":
            continue                   # re-enroll immediately, no backoff
        sleep(min(heal * 5.0, backoff_cap))
