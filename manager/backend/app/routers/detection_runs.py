"""
detection_runs.py — temporal detection API ("what changed since last time").

GET /engagements/{id}/detection-runs           — recent detection runs + stats
GET /engagements/{id}/detection-runs/latest/delta
        — the newest completed run's delta: new / reaffirmed / current, plus the
          open findings NOT reaffirmed by that run (resolution candidates —
          surfaced, never auto-closed, because a partial re-scan mustn't wrongly
          resolve findings outside its scope).

Every run is stamped with the vuln-DB snapshot version it ran against, so two
runs are provably comparable (same hash) or visibly a different basis (a
snapshot refresh), and detection can be re-run against a newer DB and diffed.
"""
from __future__ import annotations

import uuid

import structlog
from fastapi import APIRouter, Query
from sqlalchemy import func, select

from app.dependencies import DB, AuthUser
from app.models.detection_run import DetectionRun, RUN_COMPLETED
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.enums import FindingStatus
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}/detection-runs", tags=["detection-runs"])
logger = structlog.get_logger()

_OPEN_STATUSES = (FindingStatus.open, FindingStatus.confirmed, FindingStatus.accepted)


def _run_dict(r: DetectionRun) -> dict:
    return {
        "id": str(r.id),
        "trigger": r.trigger,
        "status": r.status,
        "scan_result_id": str(r.scan_result_id) if r.scan_result_id else None,
        "vuln_db_version": r.vuln_db_version,
        "vuln_db_fetched_at": r.vuln_db_fetched_at,
        "started_at": r.started_at.isoformat() if r.started_at else None,
        "finished_at": r.finished_at.isoformat() if r.finished_at else None,
        "facts_count": r.facts_count,
        "findings_new": r.findings_new,
        "findings_reaffirmed": r.findings_reaffirmed,
        "findings_current": r.findings_current,
        "error": r.error,
    }


@router.get("", summary="List recent detection runs for an engagement")
async def list_detection_runs(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    limit: int = Query(default=20, ge=1, le=100),
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    rows = (await db.execute(
        select(DetectionRun)
        .where(DetectionRun.engagement_id == engagement_id)
        .order_by(DetectionRun.started_at.desc())
        .limit(limit)
    )).scalars().all()
    return {"runs": [_run_dict(r) for r in rows]}


@router.get("/latest/delta", summary="What changed in the newest completed detection run")
async def latest_run_delta(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    candidates_limit: int = Query(default=50, ge=1, le=500),
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    run = (await db.execute(
        select(DetectionRun)
        .where(
            DetectionRun.engagement_id == engagement_id,
            DetectionRun.status == RUN_COMPLETED,
        )
        .order_by(DetectionRun.started_at.desc())
        .limit(1)
    )).scalar_one_or_none()

    if run is None:
        return {"has_runs": False}

    # Resolution candidates: still-open findings NOT reaffirmed by this run —
    # i.e. last_seen predates the run (or is null). Surfaced for operator review;
    # never auto-closed.
    cand_q = (
        select(Finding)
        .where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_(_OPEN_STATUSES),
            (Finding.last_seen.is_(None)) | (Finding.last_seen < run.started_at),
        )
        .order_by(Finding.severity)
    )
    cand_count = (await db.execute(
        select(func.count()).select_from(cand_q.subquery())
    )).scalar_one()
    cand_rows = (await db.execute(cand_q.limit(candidates_limit))).scalars().all()

    return {
        "has_runs": True,
        "run": _run_dict(run),
        "resolution_candidates_count": int(cand_count or 0),
        "resolution_candidates": [
            {
                "id": str(f.id),
                "title": f.title,
                "severity": f.severity.value if f.severity else None,
                "status": f.status.value if f.status else None,
                "last_seen": f.last_seen.isoformat() if f.last_seen else None,
            }
            for f in cand_rows
        ],
    }
