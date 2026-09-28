"""headroom.py — back off BEFORE the 429. Pure.

Every successful Anthropic / OpenAI-compatible response carries the account's
remaining allowance in its headers (``anthropic-ratelimit-*-remaining`` /
``x-ratelimit-remaining-*``) and when it resets (RFC 3339 instant for Anthropic,
a Go-style duration such as ``1m30s`` for OpenAI and Groq). When any allowance is
at zero the next request is certain to be rejected, so the router steps aside
until the reset instead of spending a request to learn it.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone

HEADROOM_CAP_S = 300.0

_PAIRS = (
    ("anthropic-ratelimit-requests-remaining", "anthropic-ratelimit-requests-reset"),
    ("anthropic-ratelimit-tokens-remaining", "anthropic-ratelimit-tokens-reset"),
    ("anthropic-ratelimit-input-tokens-remaining", "anthropic-ratelimit-input-tokens-reset"),
    ("anthropic-ratelimit-output-tokens-remaining", "anthropic-ratelimit-output-tokens-reset"),
    ("x-ratelimit-remaining-requests", "x-ratelimit-reset-requests"),
    ("x-ratelimit-remaining-tokens", "x-ratelimit-reset-tokens"),
)
_DURATION = re.compile(r"(\d+(?:\.\d+)?)(ms|h|m|s)")
_UNIT_S = {"h": 3600.0, "m": 60.0, "s": 1.0, "ms": 0.001}


def parse_duration(value: str | None) -> float | None:
    if not value:
        return None
    text = value.strip()
    parts = _DURATION.findall(text)
    if not parts or "".join(num + unit for num, unit in parts) != text:
        return None
    return sum(float(num) * _UNIT_S[unit] for num, unit in parts)


def parse_reset(value: str | None, now: datetime | None = None) -> float | None:
    duration = parse_duration(value)
    if duration is not None:
        return duration
    if not value:
        return None
    try:
        when = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    return max(0.0, (when - (now or datetime.now(timezone.utc))).total_seconds())


def headroom_cooldown(headers: dict[str, str], now: datetime | None = None) -> float | None:
    """Seconds to step aside, or None while any allowance remains."""
    waits: list[float] = []
    for remaining_header, reset_header in _PAIRS:
        raw = headers.get(remaining_header)
        if raw is None:
            continue
        try:
            if float(raw) > 0:
                continue
        except ValueError:
            continue
        wait = parse_reset(headers.get(reset_header), now)
        waits.append(wait if wait is not None else 1.0)
    if not waits:
        return None
    return min(HEADROOM_CAP_S, max(1.0, max(waits)))
