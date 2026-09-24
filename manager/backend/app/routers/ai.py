from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.dependencies import DB, AuthUser
from app.compliance.citations import check_citations
from app.models.engagement import Engagement
from app.schemas.ai import AiGenerateRequest, AiGenerateResponse, AiStatusResponse
from app.services.domain_context import domain_brief_for
from app.services.llm import AiRuntimeError, ManagerLlmService
from app.utils.db import get_or_404

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status", response_model=AiStatusResponse, summary="Manager AI providers and selectable models")
async def ai_status(current_user: AuthUser):
    del current_user
    return await ManagerLlmService().status()


@router.post("/generate", response_model=AiGenerateResponse, summary="Generate grounded defensive guidance")
async def ai_generate(request: AiGenerateRequest, current_user: AuthUser, db: DB):
    brief = None
    if request.engagement_id is not None:
        # Tenant-scoped: another tenant's engagement id is a 404, never a brief.
        eng = await get_or_404(db, Engagement, request.engagement_id, current_user.tenant_id)
        brief = await domain_brief_for(db, eng)
    try:
        content, runtime, fallback = await ManagerLlmService().generate_with_fallback(
            request, domain_brief=brief.text if brief else None)
    except AiRuntimeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    return AiGenerateResponse(
        content=content,
        provider=runtime.provider,
        model=runtime.model,
        privacy=runtime.privacy,
        fallback=fallback,
        skill=brief.skill_id if brief else None,
        skill_label=brief.skill_label if brief else None,
        jurisdictions=brief.jurisdictions if brief else [],
        unverified_citations=check_citations(content)["unverified"],
    )
