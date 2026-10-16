"""
audit_logs.py — read, verify and export the audit trail.

  GET /audit-logs              entries, newest first, filtered, keyset-paged    (admin)
  GET /audit-logs/facets       counts by category and outcome for the filters   (admin)
  GET /audit-logs/integrity    verify the tamper-evidence chain                 (admin)
  GET /audit-logs/export       CSV or JSON of everything the filters match      (admin)
  GET /audit-logs/{id}         one entry in full                                (admin)

Only an organisation's administrators read the trail. Customers have their own, narrower
view (GET /portal/audit-log). Exporting is itself recorded, so the trail shows who took a
copy of it.
"""
from __future__ import annotations

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select

from app.auth.rbac import require_role
from app.dependencies import DB, ReadDB
from app.models.audit_log import AuditLog
from app.schemas.auth import CurrentUser
from app.services import audit_catalog, audit_integrity, audit_query, org_settings
from app.services.audit import record_audit
from app.utils.csv_safe import csv_cell

router = APIRouter(prefix="/audit-logs", tags=["audit"])

_ADMIN = require_role(["admin"])
Admin = Annotated[CurrentUser, _ADMIN]


def _filters(
    start: datetime | None = Query(default=None, alias="from", description="Earliest entry (ISO 8601)"),
    end: datetime | None = Query(default=None, alias="to", description="Latest entry (ISO 8601)"),
    actor: str | None = Query(default=None, max_length=255, description="Actor id, or part of an email"),
    action: list[str] = Query(default_factory=list, max_length=20),
    category: str | None = Query(default=None, max_length=32),
    outcome: Literal["success", "failure", "denied"] | None = Query(default=None),
    resource_type: str | None = Query(default=None, max_length=50),
    resource_id: uuid.UUID | None = Query(default=None),
    engagement_id: uuid.UUID | None = Query(default=None),
    ip: str | None = Query(default=None, max_length=45),
    q: str | None = Query(default=None, max_length=200),
) -> audit_query.AuditFilters:
    if category is not None and category not in audit_catalog.CATEGORIES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Unknown category '{category}'")
    return audit_query.AuditFilters(
        start=start, end=end, actor=actor, actions=action, category=category, outcome=outcome,
        resource_type=resource_type, resource_id=resource_id, engagement_id=engagement_id,
        ip=ip, q=q)


Filters = Annotated[audit_query.AuditFilters, Depends(_filters)]


def _tenant_base(user: CurrentUser):
    return select(AuditLog).where(AuditLog.tenant_id == user.tenant_id)


@router.get("", response_model=audit_query.AuditPage, summary="The audit trail, newest first")
async def list_entries(
    db: ReadDB, user: Admin, filters: Filters,
    cursor: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=audit_query.MAX_PAGE),
):
    try:
        return await audit_query.read_page(db, _tenant_base(user), filters, cursor, limit)
    except ValueError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid cursor") from None


@router.get("/facets", summary="Counts by category and outcome, for the filters")
async def entry_facets(db: ReadDB, user: Admin, filters: Filters):
    return await audit_query.facets(db, AuditLog.tenant_id == user.tenant_id, filters)


@router.get("/integrity", summary="Verify the audit trail has not been altered")
async def integrity(db: ReadDB, user: Admin):
    result = await audit_integrity.verify_chain(db, user.tenant_id)
    policy = await org_settings.get_section(db, user.tenant_id, "audit")
    return {
        "ok": result.ok,
        "entries_checked": result.checked,
        "oldest": result.oldest,
        "newest": result.newest,
        "first_problem": None if result.ok else {
            "position": result.first_break_pos, "entry_id": result.first_break_id, "reason": result.reason},
        "retention_days": policy.retention_days,
        "minimum_retention_days": audit_integrity.MIN_RETENTION_DAYS,
        "checked_at": datetime.now(timezone.utc),
        "method": "sha256 hash chain per organisation, enforced by the database",
    }


_CSV_COLUMNS = [
    "timestamp_utc", "entry_id", "action", "description", "category", "outcome",
    "actor_id", "actor_type", "actor", "resource_type", "resource_id", "engagement_id",
    "engagement", "source_ip", "user_agent", "request_id", "detail", "changes",
    "chain_position", "entry_hash",
]


def _csv_row(e: audit_query.AuditEntryOut) -> list:
    return [
        e.timestamp.astimezone(timezone.utc).isoformat(), str(e.id), e.action, e.label, e.category,
        e.outcome, e.actor.id, e.actor.type, e.actor.label, e.resource_type,
        str(e.resource_id) if e.resource_id else None, str(e.engagement_id) if e.engagement_id else None,
        e.engagement_name, e.ip_address, e.user_agent, e.request_id,
        json.dumps(e.detail, sort_keys=True) if e.detail else None,
        json.dumps(e.changes, sort_keys=True) if e.changes else None,
        e.chain_position, e.entry_hash,
    ]


@router.get("/export", summary="Download the audit trail (CSV or JSON)")
async def export_entries(
    db: DB, user: Admin, filters: Filters,
    format: Literal["csv", "json"] = Query(default="csv"),
):
    """Everything the filters match, oldest first, up to 100,000 entries (the response says
    so when it stops there). The export is recorded in the trail."""
    stmt = audit_query.apply_filters(_tenant_base(user), filters).order_by(
        AuditLog.timestamp.asc(), AuditLog.id.asc()).limit(audit_query.EXPORT_CAP + 1)
    rows = list((await db.execute(stmt)).scalars().all())
    truncated = len(rows) > audit_query.EXPORT_CAP
    rows = rows[: audit_query.EXPORT_CAP]
    entries = await audit_query.to_entries(db, rows)

    applied = {k: (v.isoformat() if isinstance(v, datetime) else str(v))
               for k, v in vars(filters).items() if v not in (None, [], "")}
    record_audit(db, actor_id=user.user_id, tenant_id=user.tenant_id, action="audit.exported",
                 resource_type="audit_log",
                 detail={"format": format, "rows": len(entries), "truncated": truncated, "filters": applied})
    await db.flush()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    headers = {"Content-Disposition": f'attachment; filename="audit-log-{stamp}.{format}"',
               "Cache-Control": "no-store"}
    if format == "json":
        check = await audit_integrity.verify_chain(db, user.tenant_id)
        body = json.dumps({
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "tenant_id": str(user.tenant_id),
            "filters": applied,
            "count": len(entries),
            "truncated": truncated,
            "integrity": {"ok": check.ok, "entries_checked": check.checked,
                          "method": "sha256 hash chain per organisation"},
            "entries": [e.model_dump(mode="json") for e in entries],
        }, indent=2)
        return Response(content=body, media_type="application/json", headers=headers)

    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(_CSV_COLUMNS)
    for e in entries:
        w.writerow([csv_cell(v) for v in _csv_row(e)])
    if truncated:
        w.writerow([csv_cell(f"# Export stopped at {audit_query.EXPORT_CAP} entries; narrow the filters for the rest.")])
    return Response(content=("﻿" + out.getvalue()).encode("utf-8"),
                    media_type="text/csv; charset=utf-8", headers=headers)


@router.get("/{entry_id}", response_model=audit_query.AuditEntryOut, summary="One audit entry in full")
async def get_entry(entry_id: uuid.UUID, db: ReadDB, user: Admin):
    row = (await db.execute(_tenant_base(user).where(AuditLog.id == entry_id))).scalar_one_or_none()
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Entry not found")
    return (await audit_query.to_entries(db, [row]))[0]
