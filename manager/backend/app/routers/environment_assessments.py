"""Operator selection API; raw observations and inferred effects are never HTTP inputs."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Query, Response
from pydantic import Field, model_validator
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from app.config import get_settings
from app.dependencies import DB, AuthUser
from app.graph.environment_engine import ENGINE_DIGEST
from app.graph.finding_readiness import NORMALIZATION_VERSION
from app.graph.local_rule import ContractModel
from app.models.engagement import Engagement
from app.models.environment_assessment import EnvironmentAssessment
from app.services.assessment_access import load_assessment_principal
from app.services.environment_assessments import capture_environment

router = APIRouter(
    prefix="/attack-paths/environment-assessments", tags=["environment-assessments"]
)


class Selection(ContractModel):
    engagement_ids: tuple[uuid.UUID, ...] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def unique(self):
        if len(set(self.engagement_ids)) != len(self.engagement_ids):
            raise ValueError("duplicate engagement selection")
        return self


async def access(db, user, response, operation="read"):
    response.headers["Cache-Control"] = "no-store"
    if not get_settings().attack_assessments_enabled:
        raise HTTPException(
            404,
            "Environment analysis is not enabled",
            headers={"Cache-Control": "no-store"},
        )
    if operation == "compute":
        await db.connection(execution_options={"isolation_level": "REPEATABLE READ"})
    return await load_assessment_principal(db, user, operation)


async def authorize_selection(db, user, ids):
    allowed = get_settings().attack_assessment_engagement_allowlist
    if not set(ids).issubset(allowed):
        raise HTTPException(404, "Selection not available")
    found = set(
        (
            await db.execute(
                select(Engagement.id).where(
                    Engagement.tenant_id == user.tenant_id, Engagement.id.in_(ids)
                )
            )
        )
        .scalars()
        .all()
    )
    if found != set(ids):
        raise HTTPException(404, "Selection not available")


def summary(row):
    return {
        "id": str(row.id),
        "status": row.status,
        "engagement_ids": [str(i) for i in row.engagement_ids],
        "effective_as_of": row.effective_as_of.isoformat(),
        "failure_code": row.failure_code,
        "requires_reassessment": (
            row.input_document["engine_digest"] != ENGINE_DIGEST
            or row.input_document.get("normalization_version") != NORMALIZATION_VERSION
        ),
    }


@router.get("/options")
async def options(db: DB, current_user: AuthUser, response: Response):
    user = await access(db, current_user, response)
    rows = (
        await db.execute(
            select(Engagement.id, Engagement.name)
            .where(
                Engagement.tenant_id == user.tenant_id,
                Engagement.id.in_(
                    get_settings().attack_assessment_engagement_allowlist
                ),
            )
            .order_by(Engagement.name, Engagement.id)
            .limit(201)
        )
    ).all()
    from app.graph.access_policy import may_access_assessment

    return {
        "items": [{"id": str(r.id), "name": r.name} for r in rows[:200]],
        "truncated": len(rows) > 200,
        "can_compute": may_access_assessment(user, user.tenant_id, "compute"),
    }


@router.post("", status_code=202)
async def create(
    selection: Selection,
    db: DB,
    current_user: AuthUser,
    response: Response,
    idempotency_key: Annotated[
        uuid.UUID | None, Header(alias="Idempotency-Key")
    ] = None,
):
    user = await access(db, current_user, response, "compute")
    await authorize_selection(db, user, selection.engagement_ids)
    try:
        row = await capture_environment(
            db, user.tenant_id, selection.engagement_ids, idempotency_key
        )
    except IntegrityError:
        if idempotency_key is None:
            raise
        await db.rollback()
        row = (
            await db.execute(
                select(EnvironmentAssessment).where(
                    EnvironmentAssessment.tenant_id == user.tenant_id,
                    EnvironmentAssessment.idempotency_key == idempotency_key,
                )
            )
        ).scalar_one_or_none()
        if row is None:
            raise
        if set(row.engagement_ids) != set(selection.engagement_ids):
            raise HTTPException(
                409, "Request key belongs to a different selection"
            ) from None
    except ValueError as exc:
        if str(exc) == "selection_input_size_limit":
            raise HTTPException(
                413, "Selected inputs exceed the combined assessment budget"
            ) from exc
        raise HTTPException(409, str(exc)) from exc
    return summary(row)


@router.get("")
async def latest(
    db: DB,
    current_user: AuthUser,
    response: Response,
    engagement_ids: str = Query(min_length=36, max_length=740),
):
    user = await access(db, current_user, response)
    try:
        selection = Selection(engagement_ids=tuple(engagement_ids.split(",")))
    except ValueError as exc:
        raise HTTPException(422, "Select 1–20 unique engagement IDs") from exc
    ids = sorted(selection.engagement_ids)
    await authorize_selection(db, user, ids)
    scope = (
        EnvironmentAssessment.tenant_id == user.tenant_id,
        EnvironmentAssessment.engagement_ids == ids,
    )
    newest = (
        select(EnvironmentAssessment.request_sequence)
        .where(*scope)
        .order_by(EnvironmentAssessment.request_sequence.desc())
        .limit(1)
        .scalar_subquery()
    )
    completed = (
        select(EnvironmentAssessment.request_sequence)
        .where(*scope, EnvironmentAssessment.status == "completed")
        .order_by(EnvironmentAssessment.request_sequence.desc())
        .limit(1)
        .scalar_subquery()
    )
    rows = (
        (
            await db.execute(
                select(EnvironmentAssessment)
                .where(
                    *scope,
                    or_(
                        EnvironmentAssessment.request_sequence == newest,
                        EnvironmentAssessment.request_sequence == completed,
                    ),
                )
                .order_by(EnvironmentAssessment.request_sequence.desc())
            )
        )
        .scalars()
        .all()
    )
    return {
        "latest_request": summary(rows[0]) if rows else None,
        "last_completed": next(
            (summary(row) for row in rows if row.status == "completed"), None
        ),
    }


@router.get("/{assessment_id}")
async def detail(
    assessment_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    response: Response,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    user = await access(db, current_user, response)
    row = (
        await db.execute(
            select(EnvironmentAssessment).where(
                EnvironmentAssessment.id == assessment_id,
                EnvironmentAssessment.tenant_id == user.tenant_id,
            )
        )
    ).scalar_one_or_none()
    if row is None:
        raise HTTPException(404, "Assessment not found")
    await authorize_selection(db, user, row.engagement_ids)
    result = dict(row.result_document or {})
    items = result.pop("items", [])
    return {
        "snapshot": summary(row),
        **result,
        "total": len(items),
        "page": page,
        "page_size": page_size,
        "items": items[(page - 1) * page_size : page * page_size],
    }
