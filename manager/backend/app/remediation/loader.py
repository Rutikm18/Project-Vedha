"""
loader.py — the only IO in the remediation core.

Loads the Asset and Service rows a plan is grounded in. Single-finding callers
issue two queries; engagement-wide callers (bundles, report, export) load each
table ONCE and join in memory, so plan/bundle cost never scales with an N+1.
"""
from __future__ import annotations

import uuid
from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.finding import Finding
from app.models.service import Service
from app.remediation.context import RemediationContext, build_context, pick_service


async def load_finding_context(db: AsyncSession, finding: Any) -> RemediationContext:
    """Asset + its services for one finding (≤ 2 queries), then the pure context."""
    asset = None
    services: list[Any] = []
    asset_id = getattr(finding, "asset_id", None)
    if asset_id is not None:
        asset = (await db.execute(select(Asset).where(Asset.id == asset_id))).scalar_one_or_none()
        if asset is not None:
            services = list((await db.execute(
                select(Service).where(Service.asset_id == asset_id)
            )).scalars().all())
    return build_context(finding, asset, pick_service(finding, services))


async def load_engagement_items(db: AsyncSession, engagement_id: uuid.UUID,
                                *, statuses: tuple | None = None) -> list[tuple[Any, RemediationContext]]:
    """Every finding of an engagement with its context — three queries total."""
    q = select(Finding).where(Finding.engagement_id == engagement_id)
    if statuses:
        q = q.where(Finding.status.in_(statuses))
    findings = list((await db.execute(q)).scalars().all())
    assets = {a.id: a for a in (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id)
    )).scalars().all()}
    by_asset: dict[Any, list[Any]] = defaultdict(list)
    if assets:
        for s in (await db.execute(
            select(Service).where(Service.asset_id.in_(list(assets)))
        )).scalars().all():
            by_asset[s.asset_id].append(s)
    items: list[tuple[Any, RemediationContext]] = []
    for f in findings:
        asset = assets.get(f.asset_id)
        service = pick_service(f, by_asset.get(f.asset_id, []))
        items.append((f, build_context(f, asset, service)))
    return items
