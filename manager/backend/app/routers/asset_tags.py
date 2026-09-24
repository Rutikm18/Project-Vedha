"""
asset_tags.py — operator control over asset tags.

Auto tags are derived from scan evidence (app/intel/tagging.py) every time an
asset is promoted; these endpoints let an operator add business context the
scanner cannot see (owner team, business service, data owner) and backfill auto
tags for assets promoted before tagging existed.
"""
from __future__ import annotations

import uuid
from typing import Annotated

import structlog
from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.auth.rbac import require_role
from app.dependencies import DB, AuthUser
from app.intel.tagging import TAGS_VERSION, retag, tag_strings
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.service import Service
from app.schemas.asset import ManualTagsIn
from app.services.audit import record_audit
from app.utils.db import get_or_404

logger = structlog.get_logger()
router = APIRouter(prefix="/engagements/{engagement_id}/assets", tags=["asset-tags"])

Operator = Annotated[AuthUser, require_role(["admin", "manager", "tester"])]


@router.put("/{asset_id}/tags", summary="Replace an asset's manual tags")
async def set_manual_tags(
    engagement_id: uuid.UUID, asset_id: uuid.UUID, body: ManualTagsIn, db: DB,
    current_user: Operator,
):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    asset = (await db.execute(
        select(Asset).where(Asset.id == asset_id, Asset.engagement_id == engagement_id)
    )).scalar_one_or_none()
    if asset is None:
        raise HTTPException(404, "asset not found in this engagement")

    manual: list[dict] = []
    for t in body.tags:
        entry = {"key": t.key, "value": t.value.strip(), "source": "manual"}
        if entry not in manual:
            manual.append(entry)
    current = asset.tags if isinstance(asset.tags, dict) else {}
    before = tag_strings({"manual": current.get("manual") or []})
    asset.tags = {"v": TAGS_VERSION, "auto": current.get("auto") or [], "manual": manual}

    record_audit(db, actor_id=current_user.user_id, action="asset.tags.update",
                 engagement_id=engagement_id, resource_type="asset", resource_id=asset.id,
                 detail={"before": before, "after": tag_strings({"manual": manual})})
    await db.flush()
    return {"id": str(asset.id), "tags": asset.tags, "tag_strings": tag_strings(asset.tags)}


@router.post("/retag", summary="Recompute evidence-based tags for every asset")
async def retag_engagement_assets(engagement_id: uuid.UUID, db: DB, current_user: Operator):
    await get_or_404(db, Engagement, engagement_id, current_user.tenant_id)
    assets = (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id)
    )).scalars().all()
    by_asset: dict = {}
    if assets:
        for svc in (await db.execute(
            select(Service).where(Service.asset_id.in_([a.id for a in assets]))
        )).scalars().all():
            by_asset.setdefault(svc.asset_id, []).append(svc)
    for asset in assets:
        retag(asset, by_asset.get(asset.id, ()))
    await db.flush()
    logger.info("assets.retag", engagement=str(engagement_id), count=len(assets))
    return {"retagged": len(assets)}
