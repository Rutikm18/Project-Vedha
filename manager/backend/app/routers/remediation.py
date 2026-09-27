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
from datetime import datetime, timezone
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.llm_report import LLMReportGenerator, LLMUnavailableError
from app.ai.remediation_workspace import (
    Advisory,
    AdvisoryRequest,
    FindingContext,
    InvalidWorkspaceInput,
    RemediationWorkspace,
)
from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.remediation_plan import RemediationPlan
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.schemas.remediation import (
    RemediationPlanOut,
    RemediationWorkspacePreviewOut,
    RemediationWorkspacePreviewRequest,
)
from app.services.audit import record_audit
from app.services.llm import ManagerLlmService
from app.services.remediation_kb import os_key, recipe_for_finding
from app.services.remediation_workspace_context import (
    RemediationContextConflict,
    RemediationContextNotFound,
    load_workspace_contexts,
)

router = APIRouter(prefix="/findings", tags=["remediation"])
logger = structlog.get_logger()

_REMEDIATION_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])
_REMEDIATION_GENERATOR = require_role(["admin", "manager"])


class _WorkspaceAdvisory:
    """Optional explanatory AI port; executable artifacts are already hashed."""

    def __init__(self, findings: list[FindingContext]):
        self._findings = findings

    async def advise(self, request: AdvisoryRequest) -> Advisory:
        context = {
            "workspace": {
                "contextSha256": request.context_sha256,
                "findingCount": len(request.finding_ids),
                "templateIds": list(request.template_ids),
                "artifactSha256s": list(request.artifact_sha256s),
                "reviewOnly": True,
            },
            "selectedFindings": [
                {
                    "id": str(item.finding_id),
                    "title": item.title,
                    "assetId": str(item.asset_id) if item.asset_id else None,
                    "osFamily": item.os_family.value,
                    "osVersion": item.os_version,
                    "remediationKey": item.remediation_key,
                }
                for item in self._findings
            ],
        }
        ai_request = AiGenerateRequest(
            task="advisor",
            messages=[AiMessage(
                role="user",
                content=(
                    "Review this deterministic, review-only remediation workspace. "
                    "In a concise paragraph, explain sequencing, prerequisites, "
                    "validation, and rollback decisions an operator must review. "
                    "Do not provide commands and do not claim that any change ran."
                ),
            )],
            context=context,
            max_tokens=450,
        )
        content, runtime, fallback = await ManagerLlmService().generate_with_fallback(ai_request)
        notes = [f"Advisory served by {runtime.provider}/{runtime.model}."]
        if fallback:
            notes.append("The configured primary provider was unavailable; an approved fallback served this advisory.")
        return Advisory(summary=content, notes=tuple(notes))


def _serialize_workspace(result, *, finding_count: int) -> dict:
    return {
        "engagement_id": result.engagement_id,
        "catalog_version": result.catalog_version,
        "context_sha256": result.context_sha256,
        "generated_at": datetime.now(timezone.utc),
        "review_only": True,
        "finding_count": finding_count,
        "operation_count": len(result.operations),
        "artifacts": [
            {
                "artifact_id": item.artifact_id,
                "asset_id": item.asset_id,
                "os_family": item.os_family.value,
                "format": item.format.value,
                "filename": item.filename,
                "finding_ids": list(item.finding_ids),
                "context_sha256": item.context_sha256,
                "content_sha256": item.content_sha256,
                "content": item.content,
            }
            for item in result.artifacts
        ],
        "blocked": [
            {
                "finding_id": item.finding_id,
                "asset_id": item.asset_id,
                "code": item.code,
                "detail": item.detail,
            }
            for item in result.blocked
        ],
        "advisory": (
            {"summary": result.advisory.summary, "notes": list(result.advisory.notes)}
            if result.advisory else None
        ),
        "warnings": list(result.warnings),
    }


@router.post(
    "/remediation-workspaces/preview",
    response_model=RemediationWorkspacePreviewOut,
    summary="Build review-only remediation artifacts for an exact finding selection",
)
async def preview_remediation_workspace(
    payload: RemediationWorkspacePreviewRequest,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
):
    try:
        contexts = await load_workspace_contexts(
            db,
            tenant_id=current_user.tenant_id,
            finding_ids=payload.finding_ids,
        )
        advisory = _WorkspaceAdvisory(contexts) if payload.include_advisory else None
        result = await RemediationWorkspace(advisory=advisory).prepare(contexts)
    except RemediationContextNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except (RemediationContextConflict, InvalidWorkspaceInput) as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    record_audit(
        db,
        actor_id=current_user.user_id,
        action="remediation.workspace_previewed",
        engagement_id=result.engagement_id,
        resource_type="remediation_workspace",
        detail={
            "finding_count": len(contexts),
            "finding_ids": [str(item.finding_id) for item in contexts],
            "context_sha256": result.context_sha256,
            "catalog_version": result.catalog_version,
            "artifact_sha256s": [item.content_sha256 for item in result.artifacts],
            "blocked_count": len(result.blocked),
            "advisory_requested": payload.include_advisory,
            "advisory_available": result.advisory is not None,
        },
    )
    await db.flush()
    logger.info(
        "remediation.workspace_previewed",
        engagement=str(result.engagement_id),
        findings=len(contexts),
        artifacts=len(result.artifacts),
        blocked=len(result.blocked),
        context_sha256=result.context_sha256,
    )
    return _serialize_workspace(result, finding_count=len(contexts))


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
                       os: str) -> RemediationPlan | None:
    return (await db.execute(
        select(RemediationPlan).where(
            RemediationPlan.finding_id == finding_id,
            RemediationPlan.os == os,
        )
    )).scalar_one_or_none()


def _build_upsert_stmt(*, tenant_id: uuid.UUID, engagement_id: uuid.UUID,
                       finding_id: uuid.UUID, os: str, plan: dict, publish: bool):
    """Build the atomic INSERT … ON CONFLICT DO UPDATE for a cached plan.

    Pure (no IO) so the SQL semantics can be unit-tested. A single statement
    avoids the read-then-write race two concurrent generates would hit against
    UNIQUE(finding_id, os) (double insert → IntegrityError). On conflict the row
    is replaced with the freshly-generated plan: `generated_at` is refreshed, and
    `reviewed` follows the caller's `publish` intent ONLY — it must NOT inherit a
    prior approval, or regenerated (new, unreviewed) content would leak to the
    customer portal through the stale review gate."""
    source = plan.get("source", "deterministic_kb")
    stmt = pg_insert(RemediationPlan).values(
        tenant_id=tenant_id, engagement_id=engagement_id, finding_id=finding_id,
        os=os, plan=plan, source=source, model=plan.get("model"), reviewed=publish,
    )
    return stmt.on_conflict_do_update(
        constraint="uq_remediation_finding_os",
        set_={
            "plan": stmt.excluded.plan,
            "source": stmt.excluded.source,
            "model": stmt.excluded.model,
            "reviewed": stmt.excluded.reviewed,   # = publish; regeneration re-gates review
            "generated_at": func.now(),
            "updated_at": func.now(),
        },
    ).returning(RemediationPlan.reviewed, RemediationPlan.generated_at,
                RemediationPlan.model)


async def _upsert_plan(db: AsyncSession, *, tenant_id: uuid.UUID,
                       engagement_id: uuid.UUID, finding_id: uuid.UUID,
                       os: str, plan: dict, publish: bool):
    """Execute the atomic upsert and return the RETURNING row for serialization."""
    stmt = _build_upsert_stmt(
        tenant_id=tenant_id, engagement_id=engagement_id, finding_id=finding_id,
        os=os, plan=plan, publish=publish,
    )
    return (await db.execute(stmt)).one()


def _serialize(finding_id: uuid.UUID, os: str, plan: dict, *,
               row: RemediationPlan | None = None) -> dict:
    return {
        "finding_id": str(finding_id),
        "os": os,
        "source": plan.get("source", "deterministic_kb"),
        "reviewed": bool(row.reviewed) if row is not None else False,
        "cached": row is not None,
        "generated_at": row.generated_at.isoformat() if row is not None else None,
        "model": (row.model if row is not None else plan.get("model")),
        "plan": plan,
    }


@router.get("/{finding_id}/remediation",
            response_model=RemediationPlanOut,
            summary="Remediation plan for a finding (cached AI or KB fallback)")
async def get_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
    os: str = Query(default="generic"),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    key = os_key(os)
    row = await _cached_plan(db, finding_id, key)
    if row is not None:
        return _serialize(finding_id, key, row.plan, row=row)
    return _serialize(finding_id, key, recipe_for_finding(finding, key))


@router.post("/{finding_id}/remediation/generate",
             response_model=RemediationPlanOut,
             summary="Generate (and cache) an AI remediation plan for a finding")
async def generate_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
    os: str = Query(default="generic"),
    force: bool = Query(default=False),
    publish: bool = Query(default=False,
                          description="mark reviewed so the customer portal may show it"),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    key = os_key(os)

    if not force:
        row = await _cached_plan(db, finding_id, key)
        if row is not None:
            if publish and not row.reviewed:
                row.reviewed = True
                await db.flush()
            return _serialize(finding_id, key, row.plan, row=row)

    # Try the AI; on any unavailability fall back to the KB so we always cache a
    # usable plan. The KB result is deterministic and safe.
    plan: dict | None = None
    gen = LLMReportGenerator(db)
    if gen.available:
        try:
            plan = await gen.generate_remediation_plan(finding, key)
        except (LLMUnavailableError, ValueError) as exc:
            logger.warning("remediation.ai_unavailable", finding=str(finding_id), error=str(exc))
    if plan is None:
        plan = recipe_for_finding(finding, key)

    # Atomic insert-or-update — no read-then-write race under concurrent generates.
    row = await _upsert_plan(
        db, tenant_id=current_user.tenant_id, engagement_id=finding.engagement_id,
        finding_id=finding.id, os=key, plan=plan, publish=publish,
    )
    logger.info("remediation.generated", finding=str(finding_id), os=key,
                source=plan.get("source"), reviewed=row.reviewed)
    return _serialize(finding_id, key, plan, row=row)
