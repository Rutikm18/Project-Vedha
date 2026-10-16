"""
audit.py — the append-only audit-log writer, shared by the operator and portal
routers. Kept as a tiny service (not a router-private helper) so both surfaces
record to the same trail without router-to-router coupling.

What an entry carries (so it answers who / what / when / where from / outcome):
  actor_id, actor_type, actor_label   who — id, kind, and the identity frozen at the time
  action, resource_type, resource_id  what — and detail / changes for before-and-after
  timestamp (UTC)                      when
  ip_address, user_agent, request_id   where from, and the handle that ties the entry to
                                       the request's other logs
  outcome                              success | failure | denied
  tenant_id, engagement_id             whose

Source address, user agent, request id, tenant and the authenticated actor are filled in
from the request context (app.audit_context) when the caller does not pass them.

Two ways to write:
  * record_audit        — joins the caller's transaction. Right for a change that
                          succeeded: the entry commits with the change or not at all.
  * record_audit_independent — its own transaction, committed immediately. Right for an
                          event that happens on a path that RAISES (a failed sign-in, a
                          denied request): the request's transaction rolls back, and an
                          entry written inside it would roll back with it.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import structlog

from app import audit_context
from app.models.audit_log import AuditLog

logger = structlog.get_logger()

OUTCOMES = ("success", "failure", "denied")
_TEXT_LIMITS = {"user_agent": 255, "actor_label": 255, "request_id": 64}


def _clip(value: str | None, field: str) -> str | None:
    if value is None:
        return None
    return str(value)[: _TEXT_LIMITS[field]]


def build_entry(
    *, actor_id, action: str, engagement_id=None, resource_type: str | None = None,
    resource_id=None, detail: dict | None = None, ip: str | None = None,
    tenant_id=None, outcome: str = "success", actor_type: str | None = None,
    actor_label: str | None = None, changes: dict | None = None,
    request_id: str | None = None, user_agent: str | None = None,
) -> AuditLog:
    if outcome not in OUTCOMES:
        raise ValueError(f"outcome must be one of {OUTCOMES}, got {outcome!r}")
    ctx = audit_context.current()
    tenant = tenant_id if tenant_id is not None else ctx.get("tenant_id")
    return AuditLog(
        actor_id=str(actor_id),
        engagement_id=engagement_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        changes=changes,
        ip_address=ip or ctx.get("ip"),
        user_agent=_clip(user_agent or ctx.get("user_agent"), "user_agent"),
        request_id=_clip(request_id or ctx.get("request_id"), "request_id"),
        tenant_id=_as_uuid(tenant),
        outcome=outcome,
        actor_type=actor_type or ctx.get("actor_type"),
        actor_label=_clip(actor_label, "actor_label"),
        timestamp=datetime.now(timezone.utc),
    )


def _as_uuid(value: Any):
    if value is None:
        return None
    import uuid
    return value if isinstance(value, uuid.UUID) else uuid.UUID(str(value))


def record_audit(db, **kwargs) -> None:
    """Append one immutable audit row (caller flushes within its own txn)."""
    db.add(build_entry(**kwargs))


async def _commit_entry(entry: AuditLog) -> None:
    """The database half of record_audit_independent (a seam the unit tests replace)."""
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        session.add(entry)
        await session.commit()


async def record_audit_independent(**kwargs) -> None:
    """Append one audit row in its own transaction, committed now. Never raises: losing
    an audit entry is bad, but it must not turn a refused sign-in into a 500."""
    try:
        await _commit_entry(build_entry(**kwargs))
    except Exception as exc:  # noqa: BLE001 — see docstring
        logger.error("audit.independent_write_failed", action=kwargs.get("action"), error=str(exc))
