"""
remediation.py — per-finding remediation plans (operator-facing).

Two routes on top of a finding:
  * GET  …/remediation?os=      — the cached AI plan if one exists, else the
    deterministic KB recipe. NEVER empty (there is always a KB fallback).
  * POST …/remediation/generate — generate an AI plan (structured, OS-specific,
    command-safety-validated), cache it per (finding, os), optionally publish it
    (reviewed=true) so the customer portal may show it.

Reuses LLMReportGenerator (transport/retry/safety) + services/remediation_kb.
Tenant-scoped through the engagement join (findings carry no tenant_id).
"""
from __future__ import annotations

import uuid
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.llm_report import LLMReportGenerator, LLMUnavailableError
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.remediation_plan import RemediationPlan
from app.services.remediation_kb import _os_key, recipe_for_finding

router = APIRouter(prefix="/findings", tags=["remediation"])
logger = structlog.get_logger()

_OPERATOR = require_role(["admin", "manager"])


async def _tenant_finding(db: AsyncSession, finding_id: uuid.UUID,
                          tenant_id: uuid.UUID) -> Finding:
    """Fetch a finding scoped to the caller's tenant via its engagement."""
    finding = (await db.execute(
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.id == finding_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if finding is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Finding not found")
    return finding


async def _cached_plan(db: AsyncSession, finding_id: uuid.UUID,
                       os_key: str) -> RemediationPlan | None:
    return (await db.execute(
        select(RemediationPlan).where(
            RemediationPlan.finding_id == finding_id,
            RemediationPlan.os == os_key,
        )
    )).scalar_one_or_none()


def _serialize(finding_id: uuid.UUID, os_key: str, plan: dict, *,
               row: RemediationPlan | None = None) -> dict:
    return {
        "finding_id": str(finding_id),
        "os": os_key,
        "source": plan.get("source", "deterministic_kb"),
        "reviewed": bool(row.reviewed) if row is not None else False,
        "cached": row is not None,
        "generated_at": row.generated_at.isoformat() if row is not None else None,
        "model": (row.model if row is not None else plan.get("model")),
        "plan": plan,
    }


@router.get("/{finding_id}/remediation",
            summary="Remediation plan for a finding (cached AI or KB fallback)")
async def get_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
    os: str = Query(default="generic"),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    os_key = _os_key(os)
    row = await _cached_plan(db, finding_id, os_key)
    if row is not None:
        return _serialize(finding_id, os_key, row.plan, row=row)
    return _serialize(finding_id, os_key, recipe_for_finding(finding, os_key))


@router.post("/{finding_id}/remediation/generate",
             summary="Generate (and cache) an AI remediation plan for a finding")
async def generate_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _OPERATOR],
    os: str = Query(default="generic"),
    force: bool = Query(default=False),
    publish: bool = Query(default=False,
                          description="mark reviewed so the customer portal may show it"),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    os_key = _os_key(os)

    if not force:
        row = await _cached_plan(db, finding_id, os_key)
        if row is not None:
            if publish and not row.reviewed:
                row.reviewed = True
                await db.flush()
            return _serialize(finding_id, os_key, row.plan, row=row)

    # Try the AI; on any unavailability fall back to the KB so we always cache a
    # usable plan. The KB result is deterministic and safe.
    plan: dict | None = None
    gen = LLMReportGenerator(db)
    if gen.available:
        try:
            plan = await gen.generate_remediation_plan(finding, os_key)
        except (LLMUnavailableError, ValueError) as exc:
            logger.warning("remediation.ai_unavailable", finding=str(finding_id), error=str(exc))
    if plan is None:
        plan = recipe_for_finding(finding, os_key)

    row = await _cached_plan(db, finding_id, os_key)
    if row is None:
        row = RemediationPlan(
            tenant_id=current_user.tenant_id, engagement_id=finding.engagement_id,
            finding_id=finding.id, os=os_key, plan=plan,
            source=plan.get("source", "deterministic_kb"), model=plan.get("model"),
            reviewed=publish,
        )
        db.add(row)
    else:
        row.plan = plan
        row.source = plan.get("source", "deterministic_kb")
        row.model = plan.get("model")
        row.reviewed = publish or row.reviewed
    await db.flush()
    await db.refresh(row)
    logger.info("remediation.generated", finding=str(finding_id), os=os_key,
                source=row.source, reviewed=row.reviewed)
    return _serialize(finding_id, os_key, plan, row=row)
