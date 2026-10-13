from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.dependencies import DB, AuthUser
from app.ai.audit_chain import ACTION as AI_AUDIT_ACTION, persist_ai_calls, verify_chain
from app.auth.rbac import require_role
from app.compliance.citations import check_citations
from app.ratelimit import ai_rate_limit
from app.models.audit_log import AuditLog
from app.models.engagement import Engagement
from app.schemas.ai import AiGenerateRequest, AiGenerateResponse, AiStatusResponse
from app.services.domain_context import domain_brief_for
from app.services.llm import AiRuntimeError, ManagerLlmService
from app.utils.db import get_or_404

router = APIRouter(prefix="/ai", tags=["ai"])


# Operator roles only. Customers (role "client") have their own grounded assistant
# in the portal; letting them reach the generic model would bypass that grounding.
# The auth middleware's path allowlist already keeps them out; this is the second lock.
_OPERATOR = require_role(["admin", "manager", "tester", "analyst", "auditor"])


@router.get("/status", response_model=AiStatusResponse, summary="Manager AI providers and selectable models")
async def ai_status(current_user: Annotated[AuthUser, _OPERATOR]):
    del current_user
    return await ManagerLlmService().status()


@router.post("/generate", dependencies=[Depends(ai_rate_limit)], response_model=AiGenerateResponse, summary="Generate grounded defensive guidance")
async def ai_generate(request: AiGenerateRequest, current_user: Annotated[AuthUser, _OPERATOR], db: DB):
    brief = None
    if request.engagement_id is not None:
        # Tenant-scoped: another tenant's engagement id is a 404, never a brief.
        eng = await get_or_404(db, Engagement, request.engagement_id, current_user.tenant_id)
        brief = await domain_brief_for(db, eng)
    svc = ManagerLlmService()
    try:
        content, runtime, fallback = await svc.generate_with_fallback(
            request, domain_brief=brief.text if brief else None)
    except AiRuntimeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    await persist_ai_calls(db, list(svc.audit_records or []), actor_id=current_user.user_id,
                           engagement_id=request.engagement_id)
    return AiGenerateResponse(
        content=content,
        provider=runtime.provider,
        model=runtime.model,
        privacy=runtime.privacy,
        fallback=fallback,
        tier=getattr(runtime, "tier", None),
        skill=brief.skill_id if brief else None,
        skill_label=brief.skill_label if brief else None,
        jurisdictions=brief.jurisdictions if brief else [],
        unverified_citations=check_citations(content)["unverified"],
    )


@router.get("/audit/verify", summary="Verify the tamper-evident AI call audit chain")
async def ai_audit_verify(db: DB, current_user: Annotated[AuthUser, require_role(["admin"])]):
    """Walks every ai.call record oldest-first and recomputes the hash chain.
    ``broken_at`` is the first record that was edited, inserted or follows a deletion."""
    del current_user
    rows = (await db.execute(
        select(AuditLog).where(AuditLog.action == AI_AUDIT_ACTION).order_by(AuditLog.timestamp.asc())
    )).scalars().all()
    return verify_chain(rows)
