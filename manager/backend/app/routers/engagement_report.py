"""
engagement_report.py — generate the client-ready AI report on the backend.

Replaces the Next.js route that called Anthropic directly. Findings are loaded
server-side (no browser-supplied payload, no 100-finding cap); every model call
goes through the AI gateway and is written to the AI audit chain. The response
keeps the ReportResult shape the Reports page already renders, plus a
``generation`` block (provider, model, per-section status, validation issues).
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.ai.engagement_report import generate_engagement_report
from app.auth.portal_scope import ClientUser, assert_client, reports_gate
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.services.audit import record_audit

router = APIRouter(tags=["ai-report"])
_GENERATOR = require_role(["admin", "manager", "tester", "analyst"])


async def _generate(db, engagement: Engagement, user) -> dict:
    from app.services.llm import AiRuntimeError
    try:
        report = await generate_engagement_report(db, engagement=engagement, tenant_id=user.tenant_id,
                                                  actor_id=user.user_id)
    except AiRuntimeError as exc:
        code = exc.status_code if exc.status_code in (429, 502, 503, 504) else 503
        raise HTTPException(code, f"AI report generation unavailable: {exc}") from exc
    if not report["findings"]:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            "No open findings to report on for this engagement.")
    record_audit(db, actor_id=user.user_id, action="report.ai_generated", engagement_id=engagement.id,
                 resource_type="engagement", resource_id=engagement.id,
                 detail={"model": report["generation"]["model"], "sections": report["generation"]["sections"],
                         "issues": len(report["generation"]["issues"])})
    await db.flush()
    return report


@router.post("/engagements/{engagement_id}/ai-report/engagement",
             summary="Generate the client-ready AI report (backend, gateway-routed)")
async def generate_operator_report(engagement_id: uuid.UUID, db: DB,
                                   current_user: Annotated[AuthUser, _GENERATOR]):
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == engagement_id,
                                 Engagement.tenant_id == current_user.tenant_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return await _generate(db, eng, current_user)


@router.post("/portal/ai-report/engagement", dependencies=[Depends(reports_gate)],
             summary="Generate the AI report for your engagement (portal)")
async def generate_portal_report(user: ClientUser, db: DB):
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == assert_client(user))
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return await _generate(db, eng, user)
