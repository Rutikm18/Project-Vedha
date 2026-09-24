"""
compliance.py — engagement regulatory profile + regional compliance intelligence.

  GET  /engagements/{id}/profile                    sector + jurisdictions (+ options)
  PUT  /engagements/{id}/profile                    set them (audited)
  GET  /engagements/{id}/compliance                 applicable frameworks + reporting clocks
  GET  /engagements/{id}/findings/{fid}/obligations per-finding regional obligations
"""
from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.auth.rbac import require_role
from app.compliance.profile import JURISDICTIONS, SECTORS, EngagementProfile, profile_from_roe
from app.compliance.registry import (
    DISCLAIMER,
    applicable_frameworks,
    finding_obligations,
    reporting_clocks,
)
from app.dependencies import DB, AuthUser
from app.intel.tagging import tag_strings
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.services.audit import record_audit
from app.services.domain_context import engagement_tag_set
from app.utils.db import get_or_404

router = APIRouter(prefix="/engagements/{engagement_id}", tags=["compliance"])


def _framework_summary(fw) -> dict:
    return {"id": fw.id, "name": fw.name, "authority": fw.authority,
            "jurisdictions": list(fw.jurisdictions), "source": fw.source,
            "granularity": fw.granularity, "note": fw.note or None,
            "tag_triggered": bool(fw.trigger_tags)}


@router.get("/profile", summary="Engagement regulatory profile")
async def get_profile(engagement_id: uuid.UUID, db: DB, current_user: AuthUser):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    return {"profile": profile_from_roe(eng.rules_of_engagement).model_dump(),
            "options": {"sectors": list(SECTORS), "jurisdictions": JURISDICTIONS}}


@router.put("/profile", summary="Set the engagement's sector and jurisdictions")
async def set_profile(
    engagement_id: uuid.UUID, body: EngagementProfile, db: DB,
    current_user: Annotated[AuthUser, require_role(["admin", "manager"])],
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    before = profile_from_roe(eng.rules_of_engagement).model_dump()
    eng.rules_of_engagement = {**(eng.rules_of_engagement or {}), "profile": body.model_dump()}
    record_audit(db, actor_id=current_user.user_id, action="engagement.profile.update",
                 engagement_id=engagement_id, resource_type="engagement", resource_id=engagement_id,
                 detail={"before": before, "after": body.model_dump()})
    await db.flush()
    return {"profile": body.model_dump()}


@router.get("/compliance", summary="Applicable regional frameworks and incident-reporting clocks")
async def engagement_compliance(engagement_id: uuid.UUID, db: DB, current_user: AuthUser):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    profile = profile_from_roe(eng.rules_of_engagement)
    frameworks = applicable_frameworks(profile, await engagement_tag_set(db, engagement_id))
    return {"profile": profile.model_dump(),
            "frameworks": [_framework_summary(fw) for fw in frameworks],
            "reporting": reporting_clocks(frameworks), "disclaimer": DISCLAIMER}


@router.get("/findings/{finding_id}/obligations", summary="Regional obligations a finding implicates")
async def finding_obligations_route(
    engagement_id: uuid.UUID, finding_id: uuid.UUID, db: DB, current_user: AuthUser,
):
    eng = await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    finding = (await db.execute(
        select(Finding).where(Finding.id == finding_id, Finding.engagement_id == engagement_id)
    )).scalar_one_or_none()
    if finding is None:
        raise HTTPException(404, "finding not found in this engagement")
    tags: set[str] = set()
    if finding.asset_id is not None:
        asset_tags = (await db.execute(
            select(Asset.tags).where(Asset.id == finding.asset_id)
        )).scalar_one_or_none()
        tags = set(tag_strings(asset_tags))
    out = finding_obligations(finding, profile_from_roe(eng.rules_of_engagement), tags)
    out["asset_tags"] = sorted(tags)
    return out


# ── finding-scoped (the findings drawer has a finding id, not an engagement id) ─

finding_router = APIRouter(prefix="/findings", tags=["compliance"])


async def _tenant_finding_and_engagement(db, finding_id: uuid.UUID, tenant_id: uuid.UUID):
    row = (await db.execute(
        select(Finding, Engagement).join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Finding.id == finding_id, Engagement.tenant_id == tenant_id)
    )).one_or_none()
    if not row:
        raise HTTPException(404, "Finding not found")
    return row[0], row[1]


@finding_router.get("/{finding_id}/obligations", summary="Regional obligations for a finding")
async def finding_obligations_by_id(finding_id: uuid.UUID, db: DB, current_user: AuthUser):
    from app.services.compliance_brief import finding_compliance_view
    finding, eng = await _tenant_finding_and_engagement(db, finding_id, current_user.tenant_id)
    return await finding_compliance_view(db, finding, eng)


@finding_router.post("/{finding_id}/compliance-brief",
                     summary="Sector-expert compliance impact brief for a finding (AI, grounded)")
async def finding_compliance_brief(finding_id: uuid.UUID, db: DB, current_user: AuthUser):
    from app.services.compliance_brief import generate_compliance_brief
    finding, eng = await _tenant_finding_and_engagement(db, finding_id, current_user.tenant_id)
    out = await generate_compliance_brief(db, finding, eng, actor_id=current_user.user_id)
    record_audit(db, actor_id=current_user.user_id, action="finding.compliance_brief",
                 engagement_id=eng.id, resource_type="finding", resource_id=finding.id,
                 detail={"skill": out["skill"], "generated": out["content"] is not None,
                         "unverified_citations": out["unverified_citations"]})
    await db.flush()
    return out
