"""
audit.py — the append-only audit-log writer, shared by the operator and portal
routers. Kept as a tiny service (not a router-private helper) so both surfaces
record to the same trail without router-to-router coupling.
"""
from __future__ import annotations

from datetime import datetime, timezone

from app.models.audit_log import AuditLog


def record_audit(db, *, actor_id, action: str, engagement_id=None,
                 resource_type: str | None = None, resource_id=None,
                 detail: dict | None = None, ip: str | None = None) -> None:
    """Append one immutable audit row (caller flushes within its own txn)."""
    db.add(AuditLog(
        actor_id=str(actor_id),
        engagement_id=engagement_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        ip_address=ip,
        timestamp=datetime.now(timezone.utc),
    ))
