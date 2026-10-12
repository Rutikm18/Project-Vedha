"""Operator-only, opt-in finding readiness and immutable snapshot transport."""

import uuid

from fastapi import APIRouter, HTTPException, Query, Response
from sqlalchemy import or_, select

from app.config import get_settings
from app.dependencies import AuthUser, DB
from app.graph.access_policy import may_access_assessment
from app.models.attack_assessment import AttackAssessmentSnapshot
from app.models.engagement import Engagement
from app.services.attack_assessments import capture_snapshot
from app.utils.db import get_or_404

router = APIRouter(
    prefix="/engagements/{engagement_id}/attack-assessments",
    tags=["attack-assessments"],
)


def _access(user, response: Response, operation="read"):
    response.headers["Cache-Control"] = "no-store"
    if not get_settings().attack_assessments_enabled:
        raise HTTPException(
            404,
            "Attack assessments are not enabled",
            headers={"Cache-Control": "no-store"},
        )
    if not may_access_assessment(user, user.tenant_id, operation):
        raise HTTPException(
            403,
            "Attack assessment access is not permitted",
            headers={"Cache-Control": "no-store"},
        )


def _summary(row):
    if row is None:
        return None
    return {
        "id": str(row.id),
        "status": row.status,
        "request_sequence": row.request_sequence,
        "effective_as_of": row.effective_as_of.isoformat(),
        "known_at_cutoff": row.known_at_cutoff.isoformat(),
        "input_hash": row.input_hash,
        "normalization_version": row.normalization_version,
        "rule_pack_version": row.rule_pack_version,
        "failure_code": row.failure_code,
        "coverage": "partial",
        "rule_activation": "experimental_not_activated",
    }


@router.post("", status_code=202)
async def create_assessment(
    engagement_id: uuid.UUID, db: DB, current_user: AuthUser, response: Response
):
    _access(current_user, response, "compute")
    try:
        snapshot = await capture_snapshot(db, current_user.tenant_id, engagement_id)
    except ValueError as exc:
        if str(exc) == "snapshot_input_size_limit":
            raise HTTPException(
                413, "Assessment input exceeds the scoped snapshot budget"
            ) from exc
        raise
    return _summary(snapshot)


@router.get("")
async def latest_assessment(
    engagement_id: uuid.UUID, db: DB, current_user: AuthUser, response: Response
):
    _access(current_user, response)
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    scope = (
        AttackAssessmentSnapshot.tenant_id == current_user.tenant_id,
        AttackAssessmentSnapshot.engagement_id == engagement_id,
    )
    latest_sequence = (
        select(AttackAssessmentSnapshot.request_sequence)
        .where(*scope)
        .order_by(AttackAssessmentSnapshot.request_sequence.desc())
        .limit(1)
        .scalar_subquery()
    )
    completed_sequence = (
        select(AttackAssessmentSnapshot.request_sequence)
        .where(*scope, AttackAssessmentSnapshot.status == "completed")
        .order_by(AttackAssessmentSnapshot.request_sequence.desc())
        .limit(1)
        .scalar_subquery()
    )
    rows = (
        (
            await db.execute(
                select(AttackAssessmentSnapshot)
                .where(
                    *scope,
                    or_(
                        AttackAssessmentSnapshot.request_sequence == latest_sequence,
                        AttackAssessmentSnapshot.request_sequence == completed_sequence,
                    ),
                )
                .order_by(AttackAssessmentSnapshot.request_sequence.desc())
            )
        )
        .scalars()
        .all()
    )
    latest = rows[0] if rows else None
    completed = next((r for r in rows if r.status == "completed"), None)
    return {
        "latest_request": _summary(latest),
        "last_completed": _summary(completed),
        "state": "not_evaluated" if latest is None else latest.status,
    }


async def _snapshot(db, engagement_id, snapshot_id, user):
    await get_or_404(db, Engagement, engagement_id, user.tenant_id)
    row = (
        await db.execute(
            select(AttackAssessmentSnapshot).where(
                AttackAssessmentSnapshot.id == snapshot_id,
                AttackAssessmentSnapshot.engagement_id == engagement_id,
                AttackAssessmentSnapshot.tenant_id == user.tenant_id,
            )
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "Assessment not found")
    return row


@router.get("/{snapshot_id}")
async def assessment_detail(
    engagement_id: uuid.UUID,
    snapshot_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    response: Response,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    _access(current_user, response)
    row = await _snapshot(db, engagement_id, snapshot_id, current_user)
    result = row.result_document or {}
    items = result.get("assessments", [])
    return {
        "snapshot": _summary(row),
        "total": len(items),
        "total_findings": result.get("total_findings"),
        "page": page,
        "page_size": page_size,
        "items": items[(page - 1) * page_size : page * page_size],
        "compute": result.get("compute", "not_evaluated"),
        "coverage": result.get("coverage", "partial"),
        "unsupported_families": result.get("unsupported_families", []),
    }


@router.get("/{snapshot_id}/findings/{finding_id}")
async def finding_assessment(
    engagement_id: uuid.UUID,
    snapshot_id: uuid.UUID,
    finding_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    response: Response,
):
    _access(current_user, response)
    row = await _snapshot(db, engagement_id, snapshot_id, current_user)
    for item in (row.result_document or {}).get("assessments", []):
        if item["finding_id"] == str(finding_id):
            return {"snapshot": _summary(row), "assessment": item}
    raise HTTPException(404, "Finding was not assessed in this snapshot")
