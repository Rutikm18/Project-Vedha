"""
project_time — one place that decides what "now" looks like to a human.

The manager stores instants, not wall clocks: 88 call sites already use
``datetime.now(timezone.utc)`` and Postgres ``timestamptz`` keeps an instant
regardless of the offset it was written with. None of that changes here.

What changes is RENDERING. Anything an operator reads — a websocket event, an
exported filename, a report header — is rendered in the project timezone (IST by
default) so the time on screen matches the clock on the wall. Rendering a scan
as 12:01 for work the operator watched at 17:31 is a translation step that
invites mistakes during an incident.

Two rules make this safe:

  * Values stay TIMEZONE-AWARE (``...+05:30``). An aware timestamp is still an
    exact instant: it sorts correctly against the UTC rows already in the
    database and round-trips through ``timestamptz`` unchanged. Naive local
    strings would silently corrupt ordering and break interop, which is a far
    worse bug than the readability one being fixed.
  * ``datetime.utcnow()`` is never used. It returns a NAIVE datetime whose
    ``isoformat()`` carries no offset at all, so a client cannot tell what zone
    it is in — ambiguous on the wire and deprecated since 3.12.

Mirrors ``probe/main_scripts/scanner_base.py``'s helpers so both halves of the
product agree. Override with ``VEDHA_TZ`` (any IANA name).
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

try:                                    # stdlib since 3.9
    from zoneinfo import ZoneInfo
except ImportError:                     # pragma: no cover - ancient runtime
    ZoneInfo = None                     # type: ignore[assignment]

_DEFAULT_TZ_NAME = "Asia/Kolkata"


def _resolve_project_tz():
    """The project timezone, degrading safely when tzdata is unavailable."""
    name = (os.environ.get("VEDHA_TZ") or "").strip() or _DEFAULT_TZ_NAME
    if ZoneInfo is not None:
        try:
            return ZoneInfo(name)
        except Exception:
            pass
    # A slim image without tzdata, or a typo'd VEDHA_TZ, must never break the
    # API. IST observes no DST, so a fixed offset is an EXACT stand-in for the
    # default; any other zone falls back to UTC rather than guessing an offset.
    if name == _DEFAULT_TZ_NAME:
        return timezone(timedelta(hours=5, minutes=30), "IST")
    return timezone.utc


PROJECT_TZ = _resolve_project_tz()


def project_now() -> datetime:
    """Current time as an AWARE datetime in the project timezone."""
    return datetime.now(PROJECT_TZ)


def project_timestamp() -> str:
    """ISO-8601 instant in the project timezone: 2026-09-03T23:15:05+05:30."""
    return project_now().isoformat()


def to_project_tz(value: datetime | None) -> datetime | None:
    """Re-render an existing datetime in the project timezone.

    The instant is preserved. A naive input is ASSUMED to be UTC, which is what
    every naive datetime in this codebase's history actually was (they came from
    ``utcnow()``); assuming local instead would shift historical rows by 5h30m.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(PROJECT_TZ)


def project_file_stamp(fmt: str = "%Y%m%dT%H%M%S") -> str:
    """Compact project-local stamp for FILE and DIRECTORY names.

    Carries no offset suffix: a ``Z`` would be an outright lie on a local-time
    stamp, and an offset is not filename-safe everywhere. The format keeps
    lexicographic order equal to chronological order.
    """
    return project_now().strftime(fmt)
