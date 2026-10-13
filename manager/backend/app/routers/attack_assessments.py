"""Operator-only, opt-in finding readiness and immutable snapshot transport."""

import uuid

from fastapi import APIRouter, Header, HTTPException, Query, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, select

from app.config import get_settings
from app.dependencies import AuthUser, DB
from app.graph.access_policy import may_access_assessment
from app.graph.finding_readiness import NORMALIZATION_VERSION
from app.graph.local_rule import RULE_ARTIFACT_SHA256
from app.models.attack_assessment import AttackAssessmentSnapshot
from app.models.engagement import Engagement
from app.services.assessment_access import load_assessment_principal
from app.services.attack_assessments import capture_snapshot
from app.utils.db import get_or_404

router = APIRouter(
    prefix="/engagements/{engagement_id}/attack-assessments",
    tags=["attack-assessments"],
)


async def _access(
    db, user, response: Response, operation="read", *, engagement_id: uuid.UUID
):
    response.headers["Cache-Control"] = "no-store"
    if not get_settings().attack_assessments_enabled:
        raise HTTPException(
            404,
            "Attack assessments are not enabled",
            headers={"Cache-Control": "no-store"},
        )
    if operation == "compute":
        await db.connection(execution_options={"isolation_level": "REPEATABLE READ"})
    effective = await load_assessment_principal(db, user, operation)
    if engagement_id not in get_settings().attack_assessment_engagement_allowlist:
        raise HTTPException(
            404, "Engagement not found", headers={"Cache-Control": "no-store"}
        )
    return effective


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
        "requires_reassessment": row.normalization_version != NORMALIZATION_VERSION
        or row.rule_artifact_sha256 != RULE_ARTIFACT_SHA256,
    }


@router.post("", status_code=202)
async def create_assessment(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    response: Response,
    idempotency_key: uuid.UUID | None = Header(default=None, alias="Idempotency-Key"),
):
    current_user = await _access(
        db, current_user, response, "compute", engagement_id=engagement_id
    )
    try:
        snapshot = await capture_snapshot(
            db, current_user.tenant_id, engagement_id, idempotency_key
        )
    except IntegrityError:
        if idempotency_key is None:
            raise
        await db.rollback()
        snapshot = (
            await db.execute(
                select(AttackAssessmentSnapshot).where(
                    AttackAssessmentSnapshot.tenant_id == current_user.tenant_id,
                    AttackAssessmentSnapshot.engagement_id == engagement_id,
                    AttackAssessmentSnapshot.idempotency_key == idempotency_key,
                )
            )
        ).scalar_one_or_none()
        if snapshot is None:
            raise
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
    current_user = await _access(
        db, current_user, response, engagement_id=engagement_id
    )
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
        "can_compute": may_access_assessment(
            current_user, current_user.tenant_id, "compute"
        ),
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
    current_user = await _access(
        db, current_user, response, engagement_id=engagement_id
    )
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
    current_user = await _access(
        db, current_user, response, engagement_id=engagement_id
    )
    row = await _snapshot(db, engagement_id, snapshot_id, current_user)
    for item in (row.result_document or {}).get("assessments", []):
        if item["finding_id"] == str(finding_id):
            return {"snapshot": _summary(row), "assessment": item}
    raise HTTPException(404, "Finding was not assessed in this snapshot")
