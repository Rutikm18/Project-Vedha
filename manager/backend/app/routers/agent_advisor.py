"""
agent_advisor.py — API for the agentic AI advisor (recommend-only).

POST /engagements/{id}/advisor/run              — run the advisor over the engagement
GET  /engagements/{id}/advisor/recommendations  — list its recommendations (pending review)

The advisor reasons over real engagement data via a read-only Claude tool-use loop
and writes recommendations that a human approves before anything acts on them.
Running it is admin/manager-gated; it 503s cleanly when no API key is configured.
"""
from __future__ import annotations

import uuid
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.ai.agent import AgentDecisionEngine, AgentUnavailableError
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.agent_recommendation import AgentRecommendation
from app.models.engagement import Engagement
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}/advisor", tags=["ai-advisor"])
logger = structlog.get_logger()


def _rec_dict(r: AgentRecommendation) -> dict:
    return {
        "id": str(r.id),
        "run_id": str(r.run_id),
        "category": r.category,
        "target_type": r.target_type,
        "target_id": str(r.target_id) if r.target_id else None,
        "action": r.action,
        "title": r.title,
        "rationale": r.rationale,
        "confidence": float(r.confidence) if r.confidence is not None else None,
        "priority": r.priority,
        "status": r.status,
        "model": r.model,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


@router.post("/run", summary="Run the agentic AI advisor over this engagement")
async def run_advisor(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    engine = AgentDecisionEngine(db)
    if not engine.available:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "AI advisor unavailable — ANTHROPIC_API_KEY is not configured",
        )
    try:
        summary = await engine.run(engagement_id)
    except AgentUnavailableError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc
    logger.info("advisor.run", engagement=str(engagement_id), **summary)
    return summary


@router.get("/recommendations", summary="List advisor recommendations for this engagement")
async def list_recommendations(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: AuthUser,
    status_filter: str | None = Query(default=None, alias="status"),
    run_id: uuid.UUID | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)

    q = (
        select(AgentRecommendation)
        .where(AgentRecommendation.engagement_id == engagement_id)
        .order_by(AgentRecommendation.created_at.desc())
        .limit(limit)
    )
    if status_filter:
        q = q.where(AgentRecommendation.status == status_filter)
    if run_id:
        q = q.where(AgentRecommendation.run_id == run_id)

    rows = (await db.execute(q)).scalars().all()
    return {"recommendations": [_rec_dict(r) for r in rows]}
