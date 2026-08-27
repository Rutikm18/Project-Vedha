"""
finding_events.py — the finding lifecycle audit trail.

Two sources feed one timeline:

  * STORED events (finding_events table) — appended on the write path when an
    actor causes a transition (analyst confirms, operator reopens, the engine
    auto-resolves). These carry the exact actor + timestamp.

  * SYNTHESIZED events — derived, read-time, from the finding's own durable
    columns (created_at/first_seen -> DETECTED, last_seen -> RE-OBSERVED,
    resolved_at -> RESOLVED, status -> the current terminal state). This mirrors
    the activity-feed philosophy: derived from tables that already exist, so a
    complete, detailed timeline renders even for findings created before this log,
    and it can never silently drift from the finding's real state.

`build_timeline` merges them — a stored event of a given kind supersedes the
synthesized one — and returns the ordered, human-labelled sequence the UI draws
as a vertical timeline. `synthesize_events` is pure (no DB) and unit-tested alone.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import FindingEventType
from app.models.finding_event import FindingEvent

# Advancing last_seen by less than this is treated as the same observation, not a
# distinct RE-OBSERVED event (avoids a spurious entry one second after genesis).
_REOBSERVE_GAP_SECONDS = 60

# Human labels for the timeline. Keyed by FindingEventType value.
_LABELS: dict[str, str] = {
    "detected": "DETECTED",
    "reaffirmed": "RE-OBSERVED",
    "confirmed": "CONFIRMED",
    "remediated": "REMEDIATED",
    "resolved": "AUTO-RESOLVED",
    "accepted": "RISK ACCEPTED",
    "false_positive": "FALSE POSITIVE",
    "reopened": "REOPENED",
    "status_changed": "STATUS CHANGED",
    "verification_changed": "VERIFICATION UPDATED",
    "risk_changed": "RISK RESCORED",
    "note": "NOTE",
}


def _val(x: Any) -> str | None:
    """Accept a FindingEventType/FindingStatus enum or a bare string."""
    if x is None:
        return None
    return getattr(x, "value", x)


def _ev(event_type: str, occurred_at: datetime, *, actor: str | None,
        actor_type: str, from_status: str | None = None, to_status: str | None = None,
        detail: dict | None = None, synthesized: bool, approx: bool = False) -> dict:
    d = dict(detail or {})
    if approx:
        d["approx"] = True          # timestamp inferred (no dedicated column)
    return {
        "id": None,
        "event_type": event_type,
        "actor": actor,
        "actor_type": actor_type,
        "from_status": from_status,
        "to_status": to_status,
        "detail": d or None,
        "occurred_at": occurred_at,
        "synthesized": synthesized,
    }


# ── source attribution for the genesis (DETECTED) event ───────────────────────
def _detected_actor(finding) -> str:
    """Best label for who first produced this finding, from its provenance.
    A network-VA campaign / probe self-assessment reads its source from evidence;
    an engine run is attributed to the detection engine."""
    ev = finding.evidence if isinstance(finding.evidence, dict) else {}
    src = str(ev.get("source") or ev.get("source_scanner") or ev.get("scanner") or "").lower()
    if "campaign" in src or "network-va" in src or "network_va" in src:
        return "network-VA campaign"
    if src:
        return src
    if getattr(finding, "detection_run_id", None):
        return "detection-engine"
    return "system"


def _detected_detail(finding) -> dict:
    d: dict[str, Any] = {}
    if getattr(finding, "detection_run_id", None):
        d["detection_run_id"] = str(finding.detection_run_id)
    if getattr(finding, "detected_db_version", None):
        d["vuln_db_version"] = finding.detected_db_version
    sev = getattr(finding.severity, "value", finding.severity)
    d["severity"] = str(sev)
    return d


# ── pure derivation from the finding's own columns ────────────────────────────
def synthesize_events(finding) -> list[dict]:
    """Derive the canonical lifecycle events that the finding's timestamp columns
    already prove. No DB, no side effects — safe to call anywhere."""
    out: list[dict] = []
    genesis = finding.first_seen or finding.created_at
    if genesis:
        out.append(_ev("detected", genesis, actor=_detected_actor(finding),
                       actor_type="system", to_status="open",
                       detail=_detected_detail(finding), synthesized=True))

    # RE-OBSERVED: last_seen advanced meaningfully past genesis.
    last_seen = getattr(finding, "last_seen", None)
    if last_seen and genesis and (last_seen - genesis).total_seconds() > _REOBSERVE_GAP_SECONDS:
        out.append(_ev("reaffirmed", last_seen, actor="detection-engine",
                       actor_type="system",
                       detail={"note": "re-observed in a later coverage-proven run"},
                       synthesized=True))

    # Resolution — resolved_at is the true close time.
    if getattr(finding, "resolved_at", None):
        method = finding.resolution_method or "manual"
        etype = "resolved" if method == "auto" else "remediated"
        detail: dict[str, Any] = {"method": method}
        if getattr(finding, "resolution_run_id", None):
            detail["run_id"] = str(finding.resolution_run_id)
        out.append(_ev(etype, finding.resolved_at,
                       actor="auto-resolution" if method == "auto" else "operator",
                       actor_type="system" if method == "auto" else "user",
                       to_status="remediated", detail=detail, synthesized=True))

    # REOPENED — no dedicated timestamp; infer from reopened_count while open.
    status_val = _val(finding.status)
    if (getattr(finding, "reopened_count", 0) or 0) > 0 and status_val == "open" \
            and not getattr(finding, "resolved_at", None):
        ev = finding.evidence if isinstance(finding.evidence, dict) else {}
        out.append(_ev("reopened", finding.updated_at,
                       actor=ev.get("reopened_by") or "operator", actor_type="user",
                       to_status="open",
                       detail={"reopened_count": finding.reopened_count}, synthesized=True,
                       approx=True))

    # Current terminal state that isn't otherwise timed (confirmed/accepted/fp).
    terminal = {"confirmed": "confirmed", "accepted": "accepted", "fp": "false_positive"}
    if status_val in terminal:
        out.append(_ev(terminal[status_val], finding.updated_at, actor="operator",
                       actor_type="user", to_status=status_val,
                       detail=None, synthesized=True, approx=True))

    return out


# ── write path ────────────────────────────────────────────────────────────────
async def record_event(db: AsyncSession, finding, event_type, *, actor: str | None,
                        actor_type: str = "user", from_status=None, to_status=None,
                        detail: dict | None = None) -> FindingEvent:
    """Append one immutable audit row. The caller owns the transaction/flush."""
    row = FindingEvent(
        finding_id=finding.id, event_type=_val(event_type), actor=actor,
        actor_type=actor_type, from_status=_val(from_status), to_status=_val(to_status),
        detail=detail,
    )
    db.add(row)
    return row


def event_type_for_status(to_status) -> str:
    """Map a target FindingStatus to its specific event kind (so 'confirmed' reads
    CONFIRMED, not a generic STATUS CHANGED)."""
    mapping = {
        "confirmed": FindingEventType.confirmed.value,
        "remediated": FindingEventType.remediated.value,
        "accepted": FindingEventType.accepted.value,
        "fp": FindingEventType.false_positive.value,
        "open": FindingEventType.reopened.value,
    }
    return mapping.get(_val(to_status), FindingEventType.status_changed.value)


# ── read path ─────────────────────────────────────────────────────────────────
def _row_to_dict(r: FindingEvent) -> dict:
    return {
        "id": r.id,
        "event_type": r.event_type,
        "actor": r.actor,
        "actor_type": r.actor_type,
        "from_status": r.from_status,
        "to_status": r.to_status,
        "detail": r.detail,
        "occurred_at": r.occurred_at,
        "synthesized": False,
    }


def _decorate(e: dict) -> dict:
    e["label"] = _LABELS.get(e["event_type"], e["event_type"].replace("_", " ").upper())
    return e


def merge_timeline(stored: list[dict], synthesized: list[dict]) -> list[dict]:
    """Merge stored + synthesized events, oldest-first. A stored event of a given
    kind supersedes the synthesized one (real actor/timestamp beats inferred), so
    synthesized events are dropped for any type that has a stored record."""
    have = {e["event_type"] for e in stored}
    merged = list(stored) + [e for e in synthesized if e["event_type"] not in have]
    merged.sort(key=lambda e: e["occurred_at"])
    return [_decorate(e) for e in merged]


async def build_timeline(db: AsyncSession, finding) -> list[dict]:
    """The finding's full lifecycle timeline: stored audit rows merged with the
    events its columns imply, ready for the UI to render top-to-bottom."""
    rows = (await db.execute(
        select(FindingEvent)
        .where(FindingEvent.finding_id == finding.id)
        .order_by(FindingEvent.occurred_at)
    )).scalars().all()
    stored = [_row_to_dict(r) for r in rows]
    return merge_timeline(stored, synthesize_events(finding))
