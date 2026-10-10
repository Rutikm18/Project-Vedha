"""
changes.py — what changed between the two most recent completed scans (H5).

The "Re-scan & Change Detection" use case promises to highlight "new hosts, newly
opened ports, and configuration drift". The detection-run delta already answered
the findings half (new findings, resolution candidates); this is the whole picture
an operator wants when they re-scan: against the PREVIOUS completed detection run,
what hosts are new, what services are newly observed, and which findings opened,
resolved or reopened.

Read-only. One completed run is not a comparison — the response says so (`compared:
false`) rather than calling an initial baseline "no change". The boundary is the
previous completed run's start: anything first seen at or after it is "new since the
last scan". That is a conservative window (a host re-seen but unchanged is not
re-listed); it does not claim deep per-service configuration diffing, which the
model does not compute.
"""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.dependencies import DB, AuthUser
from app.models.asset import Asset
from app.models.detection_run import RUN_COMPLETED, DetectionRun
from app.models.engagement import Engagement
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.service import Service
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}", tags=["changes"])

_OPEN = (FindingStatus.open, FindingStatus.confirmed)
_RESOLVED = (FindingStatus.remediated, FindingStatus.accepted, FindingStatus.fp)


async def _two_latest_completed(db, engagement_id):
    rows = (await db.execute(
        select(DetectionRun)
        .where(DetectionRun.engagement_id == engagement_id,
               DetectionRun.status == RUN_COMPLETED)
        .order_by(DetectionRun.started_at.desc())
        .limit(2)
    )).scalars().all()
    return (rows[0] if rows else None), (rows[1] if len(rows) > 1 else None)


def _finding_row(f: Finding) -> dict:
    return {
        "id": str(f.id),
        "title": f.title,
        "severity": f.severity.value if f.severity else None,
        "status": f.status.value if f.status else None,
        "asset_id": str(f.asset_id) if f.asset_id else None,
    }


@router.get("/changes", summary="What changed since the previous completed scan (beta, read-only)")
async def engagement_changes(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    limit: int = Query(default=100, ge=1, le=500),
):
    """New hosts, newly observed services, and findings opened / resolved / reopened
    since the previous completed detection run. Read-only: it reads what is stored and
    computes nothing."""
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    latest, prev = await _two_latest_completed(db, engagement_id)
    if latest is None:
        return {"has_runs": False}
    if prev is None:
        # One scan is a baseline, not a comparison — never report it as "no change".
        return {"has_runs": True, "compared": False,
                "latest_run_at": latest.started_at.isoformat(),
                "detail": "Only one completed scan; nothing to compare yet."}

    since = prev.started_at
    asset_ids = (select(Asset.id).where(Asset.engagement_id == engagement_id)).subquery()

    async def _count(q) -> int:
        return int((await db.execute(select(func.count()).select_from(q.subquery()))).scalar_one() or 0)

    # New hosts: assets first recorded at or after the previous scan.
    new_hosts_q = (select(Asset.id, Asset.hostname, Asset.ip_address)
                   .where(Asset.engagement_id == engagement_id, Asset.created_at >= since)
                   .order_by(Asset.created_at.desc()))
    # Newly observed services on this engagement's assets.
    new_svc_q = (select(Service.id, Service.asset_id, Service.port, Service.protocol,
                        Service.service_name)
                 .where(Service.asset_id.in_(select(asset_ids.c.id)), Service.created_at >= since)
                 .order_by(Service.created_at.desc()))
    new_find_q = (select(Finding).where(Finding.engagement_id == engagement_id,
                                        Finding.first_seen.is_not(None), Finding.first_seen >= since)
                  .order_by(Finding.severity))
    resolved_q = (select(Finding).where(Finding.engagement_id == engagement_id,
                                        Finding.status.in_(_RESOLVED),
                                        Finding.resolved_at.is_not(None), Finding.resolved_at >= since)
                  .order_by(Finding.severity))
    reopened_q = (select(Finding).where(Finding.engagement_id == engagement_id,
                                        Finding.reopened_count > 0, Finding.status.in_(_OPEN),
                                        Finding.last_seen.is_not(None), Finding.last_seen >= since)
                  .order_by(Finding.severity))

    new_hosts = (await db.execute(new_hosts_q.limit(limit))).all()
    new_services = (await db.execute(new_svc_q.limit(limit))).all()
    new_findings = (await db.execute(new_find_q.limit(limit))).scalars().all()
    resolved = (await db.execute(resolved_q.limit(limit))).scalars().all()
    reopened = (await db.execute(reopened_q.limit(limit))).scalars().all()

    return {
        "has_runs": True,
        "compared": True,
        "latest_run_at": latest.started_at.isoformat(),
        "previous_run_at": prev.started_at.isoformat(),
        "new_hosts_count": await _count(new_hosts_q),
        "new_hosts": [{"id": str(r[0]), "label": r[1] or r[2] or str(r[0]), "ip": r[2]} for r in new_hosts],
        "new_services_count": await _count(new_svc_q),
        "new_services": [{"id": str(r[0]), "asset_id": str(r[1]), "port": r[2],
                          "protocol": r[3], "service": r[4]} for r in new_services],
        "new_findings_count": await _count(new_find_q),
        "new_findings": [_finding_row(f) for f in new_findings],
        "resolved_findings_count": await _count(resolved_q),
        "resolved_findings": [_finding_row(f) for f in resolved],
        "reopened_findings_count": await _count(reopened_q),
        "reopened_findings": [_finding_row(f) for f in reopened],
    }
