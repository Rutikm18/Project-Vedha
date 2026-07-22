"""
Dashboard exposure analytics endpoint.

Serves protocol-risk + zone-health aggregates computed by app.services.analytics
from real assets / services / open findings. Read-only → routed to the read
replica when one is configured.
"""
import uuid

import structlog
from fastapi import APIRouter, Query
from pydantic import BaseModel
from sqlalchemy import select

from app.dependencies import ReadDB, AuthUser
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.service import Service
from app.services import analytics as analytics_service

router = APIRouter(prefix="/analytics", tags=["analytics"])
logger = structlog.get_logger()


class ProtocolRisk(BaseModel):
    name: str
    value: int


class ZoneHealth(BaseModel):
    name: str
    score: int


class ExposureAnalytics(BaseModel):
    protocols: list[ProtocolRisk]
    zones: list[ZoneHealth]


@router.get("/exposure", response_model=ExposureAnalytics, summary="Protocol risk + zone health")
async def exposure(
    db: ReadDB,
    current_user: AuthUser,
    engagement_id: uuid.UUID | None = Query(default=None),
):
    tenant_id = current_user.tenant_id

    asset_q = (
        select(Asset)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    service_q = (
        select(Service)
        .join(Asset, Service.asset_id == Asset.id)
        .join(Engagement, Asset.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
    )
    finding_q = (
        select(Finding)
        .join(Engagement, Finding.engagement_id == Engagement.id)
        .where(Engagement.tenant_id == tenant_id)
        .where(Finding.status.in_([FindingStatus.open, FindingStatus.confirmed]))
    )
    if engagement_id:
        asset_q = asset_q.where(Asset.engagement_id == engagement_id)
        service_q = service_q.where(Asset.engagement_id == engagement_id)
        finding_q = finding_q.where(Finding.engagement_id == engagement_id)

    assets = (await db.execute(asset_q)).scalars().all()
    services = (await db.execute(service_q)).scalars().all()
    findings = (await db.execute(finding_q)).scalars().all()

    return analytics_service.compute_exposure(list(assets), list(services), list(findings))
