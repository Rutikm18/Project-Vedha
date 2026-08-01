from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.dependencies import AuthUser
from app.schemas.ai import AiGenerateRequest, AiGenerateResponse, AiStatusResponse
from app.services.llm import AiRuntimeError, ManagerLlmService

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/status", response_model=AiStatusResponse, summary="Manager AI providers and selectable models")
async def ai_status(current_user: AuthUser):
    del current_user
    return await ManagerLlmService().status()


@router.post("/generate", response_model=AiGenerateResponse, summary="Generate grounded defensive guidance")
async def ai_generate(request: AiGenerateRequest, current_user: AuthUser):
    del current_user
    try:
        content, runtime = await ManagerLlmService().generate(request)
    except AiRuntimeError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
    return AiGenerateResponse(
        content=content,
        provider=runtime.provider,
        model=runtime.model,
        privacy=runtime.privacy,
    )
