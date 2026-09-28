"""failures.py — what a provider failure MEANS for routing.

The chain walker asks one question of every failed attempt: should this provider
be skipped for a while, and for how long? The status code alone cannot answer it.
Anthropic reports a monthly spend cap as 429 — the same code as a per-minute rate
limit — and OpenAI reports an empty balance as ``429 insufficient_quota``. So the
provider's error text is checked first, most permanent state first. Pure; no I/O.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# Checked before billing: a spend cap is the one money state that does not clear
# until the calendar month turns (Anthropic pauses the API until the 1st).
SPEND_CAP_SIGNALS = ("spend limit", "spending limit", "usage limit", "regain access")
BILLING_SIGNALS = (
    "credit balance", "purchase credit", "billing", "insufficient_quota",
    "insufficient quota", "insufficient funds", "payment required", "out of credit",
    # OpenAI's wording when a prepaid balance is empty (observed live, HTTP 429).
    "no credits", "credits remaining",
)
AUTH_SIGNALS = (
    "invalid x-api-key", "authentication_error", "invalid api key", "invalid_api_key",
    "could not authenticate", "unauthorized",
)

BILLING_RECHECK_S = 3600.0
AUTH_RECHECK_S = 3600.0
RATE_LIMIT_DEFAULT_S = 60.0
OVERLOAD_BASE_S = 30.0
ESCALATION_CAP_S = 600.0


@dataclass(frozen=True)
class Failure:
    # spend_cap | billing | auth | rate_limit | overloaded | timeout | network |
    # request | invalid_output
    kind: str
    # None: the fault was this request's (malformed body, unusable output) — the
    # provider stays eligible for the next request.
    cooldown_s: float | None
    # Waiting will not fix it: someone has to add money or fix a key.
    blocked: bool = False
    # Repeated failures double the cooldown (circuit-breaker backoff).
    escalates: bool = False


TIMEOUT = Failure("timeout", 60.0, escalates=True)
NETWORK = Failure("network", 30.0, escalates=True)
INVALID_OUTPUT = Failure("invalid_output", None)


def seconds_until_next_month(now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    year, month = (now.year + 1, 1) if now.month == 12 else (now.year, now.month + 1)
    first = datetime(year, month, 1, tzinfo=now.tzinfo or timezone.utc)
    return (first - now).total_seconds()


def parse_retry_after(value: str | None, now: datetime | None = None) -> float | None:
    """``Retry-After`` is either delay-seconds or an HTTP date (RFC 9110)."""
    if not value or not value.strip():
        return None
    try:
        seconds = float(value.strip())
    except ValueError:
        try:
            when = parsedate_to_datetime(value.strip())
        except (TypeError, ValueError):
            return None
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        seconds = (when - (now or datetime.now(timezone.utc))).total_seconds()
    return max(1.0, seconds)


def classify_http(status: int, reason: str, retry_after: float | None = None) -> Failure:
    low = (reason or "").lower()
    if any(sig in low for sig in SPEND_CAP_SIGNALS):
        return Failure("spend_cap", seconds_until_next_month(), blocked=True)
    if status == 402 or any(sig in low for sig in BILLING_SIGNALS):
        return Failure("billing", BILLING_RECHECK_S, blocked=True)
    if status in (401, 403) or any(sig in low for sig in AUTH_SIGNALS):
        return Failure("auth", AUTH_RECHECK_S, blocked=True)
    if status == 429 or "rate limit" in low or "rate_limit" in low:
        return Failure("rate_limit", retry_after or RATE_LIMIT_DEFAULT_S)
    if status >= 500 or "overloaded" in low:
        return Failure("overloaded", OVERLOAD_BASE_S, escalates=True)
    return Failure("request", None)
