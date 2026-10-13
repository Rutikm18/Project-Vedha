"""
remediation.py — contextual remediation plans and fix bundles (operator-facing).

Per finding:
  * GET  …/remediation?os=        — the asset-grounded KB plan (app/remediation),
    or the cached AI refinement when one exists (flagged ``stale`` when the facts
    it was generated from no longer match). OS defaults to the scanned OS.
  * POST …/remediation/refine     — AI refinement ON TOP of the KB plan, through
    the AI gateway + audit chain; cached per (finding, os); unreviewed until
    published. ``/generate`` is kept as an alias for older clients.
  * POST …/remediation/publish    — approve the cached refinement for customers.

Per engagement (fix bundles, see app/remediation/bundles.py):
  * GET  /engagements/{id}/remediation/bundles?view=fix|host
  * GET  /engagements/{id}/remediation/bundles/{fix_key}
  * POST /engagements/{id}/remediation/bundles/{fix_key}/refine
  * GET  /engagements/{id}/remediation/bundles/{fix_key}/refinement

Tenant-scoped through the engagement join (findings carry no tenant_id).
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Annotated, Any

import structlog
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.remediation_workspace import (
    Advisory,
    AdvisoryRequest,
    FindingContext,
    InvalidWorkspaceInput,
    RemediationWorkspace,
)
from app.auth.rbac import require_role
from app.ratelimit import ai_rate_limit
from app.dependencies import DB, AuthUser
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.remediation_plan import RemediationPlan
from app.remediation import ai_refine
from app.routers import findings as findings_router
from app.remediation import service as remediation_service
from app.remediation.bundles import bundle_link
from app.remediation.loader import load_finding_context, resolve_due
from app.remediation.plan import build_plan, os_for_context
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.schemas.remediation import (
    RemediationPlanOut,
    RemediationWorkspacePreviewOut,
    RemediationWorkspacePreviewRequest,
)
from app.services.audit import record_audit
from app.services.remediation_workspace_context import (
    RemediationContextConflict,
    RemediationContextNotFound,
    load_workspace_contexts,
)
from app.services.remediation_kb import os_key
from app.services.remediation_os import PlatformResolution, is_auto

router = APIRouter(prefix="/findings", tags=["remediation"])
bundles_router = APIRouter(prefix="/engagements", tags=["remediation"])
logger = structlog.get_logger()

_REMEDIATION_READER = require_role(["admin", "manager", "tester", "analyst", "auditor"])
_REMEDIATION_GENERATOR = require_role(["admin", "manager"])


class _WorkspaceAdvisory:
    """Optional explanatory AI port. Executable artifacts are already rendered and
    hashed before this runs, so a model can never change a byte of them. The call
    goes through the manager's AI gateway and its records join the audit chain."""

    def __init__(self, findings: list[FindingContext]):
        self._findings = findings
        self.audit_records: list[dict] = []

    async def advise(self, request: AdvisoryRequest) -> Advisory:
        from app.services.llm import ManagerLlmService

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
        svc = ManagerLlmService()
        try:
            content, runtime, fallback = await svc.generate_with_fallback(ai_request)
        finally:
            self.audit_records = list(getattr(svc, "audit_records", None) or [])
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
    dependencies=[Depends(ai_rate_limit)],
    summary="Build review-only remediation artifacts for an exact finding selection",
)
async def preview_remediation_workspace(
    payload: RemediationWorkspacePreviewRequest,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
):
    from app.ai.audit_chain import persist_ai_calls

    advisory = None
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

    if advisory is not None:
        await persist_ai_calls(db, advisory.audit_records,
                               actor_id=current_user.user_id, engagement_id=result.engagement_id)
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
                       finding_id: uuid.UUID, os: str, plan: dict, publish: bool,
                       facts_fingerprint: str | None = None):
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
        subject_type="finding", os=os, plan=plan, source=source, model=plan.get("model"),
        reviewed=publish, facts_fingerprint=facts_fingerprint,
    )
    return stmt.on_conflict_do_update(
        constraint="uq_remediation_finding_os",
        set_={
            "plan": stmt.excluded.plan,
            "source": stmt.excluded.source,
            "model": stmt.excluded.model,
            "reviewed": stmt.excluded.reviewed,   # = publish; regeneration re-gates review
            "facts_fingerprint": stmt.excluded.facts_fingerprint,
            "generated_at": func.now(),
            "updated_at": func.now(),
        },
    ).returning(RemediationPlan.reviewed, RemediationPlan.generated_at,
                RemediationPlan.model)


def _build_bundle_upsert_stmt(*, tenant_id: uuid.UUID, engagement_id: uuid.UUID, fix_key: str,
                              os: str, plan: dict, publish: bool, facts_fingerprint: str):
    """Bundle rows: same semantics, keyed by the partial unique index
    uq_remediation_bundle_os (engagement_id, fix_key, os) WHERE subject_type='bundle'."""
    stmt = pg_insert(RemediationPlan).values(
        tenant_id=tenant_id, engagement_id=engagement_id, finding_id=None, subject_type="bundle",
        fix_key=fix_key, os=os, plan=plan, source=plan.get("source", "ai"), model=plan.get("model"),
        reviewed=publish, facts_fingerprint=facts_fingerprint,
    )
    return stmt.on_conflict_do_update(
        index_elements=["engagement_id", "fix_key", "os"],
        index_where=text("subject_type = 'bundle'"),
        set_={
            "plan": stmt.excluded.plan, "source": stmt.excluded.source, "model": stmt.excluded.model,
            "reviewed": stmt.excluded.reviewed, "facts_fingerprint": stmt.excluded.facts_fingerprint,
            "generated_at": func.now(), "updated_at": func.now(),
        },
    ).returning(RemediationPlan.reviewed, RemediationPlan.generated_at, RemediationPlan.model)


def _serialize(finding_id: uuid.UUID, os: str, plan: dict, *,
               row: Any = None, bundle: dict | None = None, stale: bool = False,
               platform: dict | None = None) -> dict:
    return {
        "platform": platform,
        "bundle": bundle,
        "finding_id": str(finding_id),
        "os": os,
        "source": plan.get("source", "deterministic_kb"),
        "reviewed": bool(row.reviewed) if row is not None else False,
        "cached": row is not None,
        "generated_at": row.generated_at.isoformat() if row is not None else None,
        "model": (row.model if row is not None else plan.get("model")),
        "stale": stale,
        "plan": plan,
    }


def platform_for(requested: str | None, ctx: Any) -> PlatformResolution:
    """`auto` (default) → the platform detected for the asset (services/
    remediation_os, resolved once in the loader); any explicit OS overrides."""
    if is_auto(requested):
        return ctx.platform or PlatformResolution("generic", None, "no_asset", None, None)
    return PlatformResolution(os_key(requested), None, "requested", None, None)


def platform_out(requested: str | None, platform: PlatformResolution) -> dict:
    return {"requested": "auto" if is_auto(requested) else platform.os, **platform.to_dict()}


_OS_QUERY = "auto = detect from the asset; or linux|windows|macos|generic"


def _is_stale(row: Any, fingerprint: str) -> bool:
    stored = getattr(row, "facts_fingerprint", None)
    return bool(stored) and stored != fingerprint


def _ai_error(exc: Exception) -> HTTPException:
    code = getattr(exc, "status_code", 503)
    code = code if code in (409, 429, 502, 503, 504) else 503
    return HTTPException(code, f"AI refinement unavailable: {exc}")


@router.get("/{finding_id}/remediation",
            response_model=RemediationPlanOut,
            summary="Remediation plan for a finding (asset-grounded KB, or cached AI refinement)")
async def get_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
    os: str = Query(default="auto", description=_OS_QUERY),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    ctx = await load_finding_context(db, finding)
    platform = platform_for(os, ctx)
    key = platform.os
    shown = platform_out(os, platform)
    row = await _cached_plan(db, finding_id, key)
    due = await resolve_due(db, finding, current_user.tenant_id)
    link = bundle_link(finding, ctx)
    if row is not None:
        # The due date is live (extensions/policy changes), never the cached one.
        return _serialize(finding_id, key, {**row.plan, "due": due}, row=row, bundle=link,
                          stale=_is_stale(row, ai_refine.facts_fingerprint([ctx])), platform=shown)
    return _serialize(finding_id, key, build_plan(finding, ctx, os=key, due=due), bundle=link,
                      platform=shown)


@router.post("/{finding_id}/remediation/refine", dependencies=[Depends(ai_rate_limit)],
             response_model=RemediationPlanOut,
             summary="Refine the plan with AI (gateway-routed, cached, unreviewed until published)")
async def refine_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
    os: str = Query(default="auto", description=_OS_QUERY),
    force: bool = Query(default=False),
    publish: bool = Query(default=False,
                          description="mark reviewed so the customer portal may show it"),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    ctx = await load_finding_context(db, finding)
    platform = platform_for(os, ctx)
    key = platform.os
    shown = platform_out(os, platform)
    fingerprint = ai_refine.facts_fingerprint([ctx])
    link = bundle_link(finding, ctx)

    if not force:
        row = await _cached_plan(db, finding_id, key)
        if row is not None and not _is_stale(row, fingerprint) and row.source == "ai":
            if publish and not row.reviewed:
                row.reviewed = True
                await db.flush()
            return _serialize(finding_id, key, row.plan, row=row, bundle=link, platform=shown)

    due = await resolve_due(db, finding, current_user.tenant_id)
    kb = build_plan(finding, ctx, os=key, due=due)
    engagement = (await db.execute(
        select(Engagement).where(Engagement.id == finding.engagement_id)
    )).scalar_one_or_none()
    from app.services.llm import AiRuntimeError
    try:
        plan = await ai_refine.refine(db, engagement=engagement, kb_plan=kb, contexts=[ctx],
                                      findings=[finding], actor_id=current_user.user_id)
    except AiRuntimeError as exc:
        logger.warning("remediation.refine_unavailable", finding=str(finding_id), error=str(exc))
        raise _ai_error(exc) from exc

    row = (await db.execute(_build_upsert_stmt(
        tenant_id=current_user.tenant_id, engagement_id=finding.engagement_id, finding_id=finding.id,
        os=key, plan=plan, publish=publish, facts_fingerprint=fingerprint,
    ))).one()
    logger.info("remediation.refine_cached", finding=str(finding_id), os=key, reviewed=row.reviewed)
    return _serialize(finding_id, key, plan, row=row, bundle=link, platform=shown)


@router.post("/{finding_id}/remediation/generate", dependencies=[Depends(ai_rate_limit)],
             response_model=RemediationPlanOut,
             summary="Deprecated alias of /remediation/refine")
async def generate_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
    os: str = Query(default="auto", description=_OS_QUERY),
    force: bool = Query(default=False),
    publish: bool = Query(default=False),
):
    return await refine_remediation(finding_id, db, current_user, os=os, force=force, publish=publish)


@router.post("/{finding_id}/remediation/publish",
             response_model=RemediationPlanOut,
             summary="Approve the cached AI refinement for the customer portal")
async def publish_remediation(
    finding_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
    os: str = Query(default="auto", description=_OS_QUERY),
):
    finding = await _tenant_finding(db, finding_id, current_user.tenant_id)
    ctx = await load_finding_context(db, finding)
    platform = platform_for(os, ctx)
    key = platform.os
    row = await _cached_plan(db, finding_id, key)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No AI refinement to publish for this OS")
    if _is_stale(row, ai_refine.facts_fingerprint([ctx])):
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "The refinement is stale (the asset changed) — regenerate before publishing")
    row.reviewed = True
    await db.flush()
    from app.services.audit import record_audit
    record_audit(db, actor_id=current_user.user_id, action="remediation.published",
                 engagement_id=finding.engagement_id, resource_type="finding", resource_id=finding.id,
                 detail={"os": key, "model": row.model})
    return _serialize(finding_id, key, row.plan, row=row, bundle=bundle_link(finding, ctx),
                      platform=platform_out(os, platform))


# ── fix bundles (engagement-level) ───────────────────────────────────────────

async def _tenant_engagement(db: AsyncSession, engagement_id: uuid.UUID,
                             tenant_id: uuid.UUID) -> Engagement:
    eng = (await db.execute(
        select(Engagement).where(Engagement.id == engagement_id, Engagement.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if eng is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Engagement not found")
    return eng


@bundles_router.get("/{engagement_id}/remediation/bundles",
                    summary="Fix bundles for an engagement (by fix or by host)")
async def get_engagement_bundles(
    engagement_id: uuid.UUID,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
    view: str = Query(default="fix", pattern="^(fix|host)$"),
):
    eng = await _tenant_engagement(db, engagement_id, current_user.tenant_id)
    data = await remediation_service.engagement_bundles(db, eng, current_user.tenant_id)
    return remediation_service.view_payload(data["bundles"], view, data["sla_source"])


@bundles_router.get("/{engagement_id}/remediation/bundles/{fix_key}",
                    summary="One fix bundle with its per-host checklist")
async def get_engagement_bundle(
    engagement_id: uuid.UUID,
    fix_key: str,
    db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
):
    eng = await _tenant_engagement(db, engagement_id, current_user.tenant_id)
    data = await remediation_service.engagement_bundles(db, eng, current_user.tenant_id)
    bundle = remediation_service.find_bundle(data["bundles"], fix_key)
    if bundle is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Bundle not found")
    return bundle


def _bundle_members(data: dict, bundle: dict) -> tuple[list[Any], list[Any]]:
    ids = set(bundle["open_finding_ids"] or bundle["resolves"])
    members = [(f, ctx) for f, ctx, _due in data["items"] if str(f.id) in ids]
    return [f for f, _ in members], [ctx for _, ctx in members]


def _bundle_kb_plan(bundle: dict, members: list[Any], contexts: list[Any], os: str) -> dict:
    """The KB plan a bundle refinement starts from: the representative plan for
    the OS, carrying the bundle's own target, title and verification."""
    rep = next((i for i, c in enumerate(contexts) if os_for_context(c) == os), 0)
    plan = build_plan(members[rep], contexts[rep], os=os)
    plan.update({"title": bundle["title"], "target_state": bundle["target_state"],
                 "summary": f"{bundle['title']}. Target: {bundle['target_state']}."})
    return plan


async def _cached_bundle_plan(db: AsyncSession, engagement_id: uuid.UUID, fix_key: str,
                              os: str) -> RemediationPlan | None:
    return (await db.execute(
        select(RemediationPlan).where(
            RemediationPlan.engagement_id == engagement_id, RemediationPlan.subject_type == "bundle",
            RemediationPlan.fix_key == fix_key, RemediationPlan.os == os)
    )).scalar_one_or_none()


def _bundle_payload(bundle: dict, os: str, plan: dict, row: Any, stale: bool) -> dict:
    return {"fix_key": bundle["fix_key"], "ref": bundle["ref"], "os": os, "source": plan.get("source"),
            "reviewed": bool(getattr(row, "reviewed", False)),
            "generated_at": row.generated_at.isoformat() if row is not None else None,
            "model": getattr(row, "model", None) or plan.get("model"), "stale": stale, "plan": plan}


@bundles_router.get("/{engagement_id}/remediation/bundles/{fix_key}/refinement",
                    summary="The cached AI refinement of a fix bundle, if any")
async def get_bundle_refinement(
    engagement_id: uuid.UUID, fix_key: str, db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
    os: str = Query(default="generic"),
):
    eng = await _tenant_engagement(db, engagement_id, current_user.tenant_id)
    key = os_key(os)
    data = await remediation_service.engagement_bundles(db, eng, current_user.tenant_id)
    bundle = remediation_service.find_bundle(data["bundles"], fix_key)
    if bundle is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Bundle not found")
    row = await _cached_bundle_plan(db, eng.id, fix_key, key)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No AI refinement for this bundle and OS")
    _members, contexts = _bundle_members(data, bundle)
    return _bundle_payload(bundle, key, row.plan, row, _is_stale(row, ai_refine.facts_fingerprint(contexts)))


@bundles_router.post("/{engagement_id}/remediation/bundles/{fix_key}/refine",
                     summary="Refine a fix bundle with AI (all hosts it covers)")
async def refine_bundle(
    engagement_id: uuid.UUID, fix_key: str, db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_GENERATOR],
    os: str = Query(default="generic"),
    publish: bool = Query(default=False),
):
    eng = await _tenant_engagement(db, engagement_id, current_user.tenant_id)
    key = os_key(os)
    data = await remediation_service.engagement_bundles(db, eng, current_user.tenant_id)
    bundle = remediation_service.find_bundle(data["bundles"], fix_key)
    if bundle is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Bundle not found")
    members, contexts = _bundle_members(data, bundle)
    if not members:
        raise HTTPException(status.HTTP_409_CONFLICT, "This bundle has no findings to refine")
    kb = _bundle_kb_plan(bundle, members, contexts, key)
    fingerprint = ai_refine.facts_fingerprint(contexts)
    from app.services.llm import AiRuntimeError
    try:
        plan = await ai_refine.refine(db, engagement=eng, kb_plan=kb, contexts=contexts,
                                      findings=members, actor_id=current_user.user_id)
    except AiRuntimeError as exc:
        logger.warning("remediation.bundle_refine_unavailable", fix_key=fix_key, error=str(exc))
        raise _ai_error(exc) from exc
    row = (await db.execute(_build_bundle_upsert_stmt(
        tenant_id=current_user.tenant_id, engagement_id=eng.id, fix_key=fix_key, os=key, plan=plan,
        publish=publish, facts_fingerprint=fingerprint,
    ))).one()
    return _bundle_payload(bundle, key, plan, row, False)


@bundles_router.get("/{engagement_id}/remediation/export",
                    summary="Download the remediation tracker (XLSX workbook or CSV zip)")
async def export_remediation(
    engagement_id: uuid.UUID, db: DB,
    current_user: Annotated[AuthUser, _REMEDIATION_READER],
    format: str = Query(default="xlsx", pattern="^(xlsx|csv)$"),
    sheet: str | None = Query(default=None, pattern="^(findings|by_fix|by_host)$",
                              description="With format=csv: return this one sheet as a .csv, not the zip"),
    filters: Annotated[findings_router.FindingFilters, Depends(findings_router.finding_filters)] = None,
):
    """Accepts the findings-list filters (severity, status, search, asset_ip,
    scan, …) so a filtered report exports exactly what it shows."""
    eng = await _tenant_engagement(db, engagement_id, current_user.tenant_id)
    ids = await findings_router.filtered_finding_ids(
        db, current_user, eng.id, filters or findings_router.FindingFilters())
    content, media, filename = await remediation_service.export_tracker(
        db, eng, current_user.tenant_id, format, sheet, ids)
    return Response(content=content, media_type=media,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})
