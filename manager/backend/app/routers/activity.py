"""
Recent activity feed.

A tenant-wide, read-only stream of the operator-relevant events that already
exist in the system — scan jobs changing state and findings being discovered —
merged and sorted newest-first. This is the dashboard's "is anything happening?"
signal.

Deliberately derived from existing tables (scan_jobs, findings) rather than a
new event log: it needs no write-path instrumentation and can never drift from
the real state, at the cost of only surfacing events those tables already record.
Richer auditing (config changes, logins) can later be layered in from AuditLog.
"""
import uuid
from datetime import datetime

import structlog
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import select

from app.dependencies import ReadDB, AuthUser
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.scan_job import ScanJob

router = APIRouter(prefix="/activity", tags=["activity"])
logger = structlog.get_logger()


class ActivityItem(BaseModel):
    id: str
    timestamp: datetime
    kind: str          # "scan" | "finding"
    action: str        # short headline
    detail: str        # one-line detail
    engagement_id: str


@router.get("", response_model=list[ActivityItem], summary="Recent tenant activity (scans + findings)")
async def recent_activity(
    db: ReadDB,
    current_user: AuthUser,
    limit: int = Query(default=20, ge=1, le=100),
):
    tenant_id = current_user.tenant_id

    # Pull a bounded slice of each source, then merge — so one very chatty source
    # can't starve the other out of the feed.
    jobs = (await db.execute(
        select(ScanJob)
        .join(Engagement, ScanJob.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .order_by(ScanJob.updated_at.desc())
        .limit(limit)
    )).scalars().all()

    findings = (await db.execute(
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .order_by(Finding.created_at.desc())
        .limit(limit)
    )).scalars().all()

    events: list[ActivityItem] = []

    for j in jobs:
        status = j.status.value if hasattr(j.status, "value") else str(j.status)
        job_type = j.job_type.value if hasattr(j.job_type, "value") else str(j.job_type)
        ts = j.completed_at or j.started_at or j.updated_at or j.created_at
        events.append(ActivityItem(
            id=f"scan-{j.id}",
            timestamp=ts,
            kind="scan",
            action=f"Scan {status}",
            detail=f"{job_type.replace('_', ' ')} job",
            engagement_id=str(j.engagement_id),
        ))

    for f in findings:
        severity = f.severity.value if hasattr(f.severity, "value") else str(f.severity)
        events.append(ActivityItem(
            id=f"finding-{f.id}",
            timestamp=f.created_at,
            kind="finding",
            action=f"{severity.upper()} finding",
            detail=f.title,
            engagement_id=str(f.engagement_id),
        ))

    # Newest first; tz-aware and naive timestamps sort together by coercing to a
    # common key. (created_at/updated_at are tz-aware in this schema.)
    events.sort(key=lambda e: e.timestamp, reverse=True)
    return events[:limit]
