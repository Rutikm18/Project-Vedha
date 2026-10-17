"""risk_context.py — the asset context a finding's risk rank is computed from, in bulk.

The Findings list, a finding's detail, the customer portal and the report all show the SAME
0-1000 rank, so they all get it from here: criticality and exposure come from the finding's
real asset (two bulk queries however many rows), never from a per-surface guess. A report
that quoted the stored score while the Findings page quoted this one would hand a customer
two different numbers for one finding.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.finding import Finding
from app.models.service import Service
from app.services.risk_inputs import risk_inputs, strongest_exposure
from app.services.risk_rank import compute_risk_rank


def build_context(assets: Iterable[tuple], exposures: Mapping[Any, list]) -> dict:
    """(asset id, ip, hostname, criticality) rows plus each asset's service exposures,
    shaped the way ``rank_for`` reads them. The one place that shape is made, so a caller
    that already holds its assets (the report) cannot drift from one that queries them."""
    return {aid: {"ip": ip, "hostname": host,
                  "criticality": getattr(crit, "value", crit),
                  "exposure": strongest_exposure(exposures.get(aid, []))}
            for aid, ip, host, crit in assets}


async def asset_risk_context(db: AsyncSession, findings: list[Finding]) -> dict:
    """Per-asset identity, criticality and strongest service exposure for a page of
    findings: TWO bulk queries however many rows, never one per row. Everything the
    risk rank needs about the asset comes from here, in every list-shaped response."""
    ids = {f.asset_id for f in findings if f.asset_id is not None}
    if not ids:
        return {}
    rows = (await db.execute(
        select(Asset.id, Asset.ip_address, Asset.hostname, Asset.criticality)
        .where(Asset.id.in_(ids))
    )).all()
    svc = (await db.execute(
        select(Service.asset_id, Service.exposure).where(Service.asset_id.in_(ids))
    )).all()
    grouped: dict = {}
    for aid, exp in svc:
        grouped.setdefault(aid, []).append(exp)
    return build_context(rows, grouped)


def rank_for(finding: Finding, ctx: dict) -> int:
    a = ctx.get(finding.asset_id, {})
    return compute_risk_rank(**risk_inputs(
        finding, asset_criticality=a.get("criticality"), exposure=a.get("exposure")))


async def risk_ranks_for(db: AsyncSession, findings: list[Finding]) -> dict:
    """finding id → the canonical rank. For list-shaped responses that do not go
    through FindingOut (the customer portal's legacy rows). The report loads its assets itself,
    tenant-scoped, and builds the same context with ``build_context``."""
    ctx = await asset_risk_context(db, findings)
    return {f.id: rank_for(f, ctx) for f in findings}
