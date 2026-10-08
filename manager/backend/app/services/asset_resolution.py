"""
asset_resolution.py — the ONE place that decides which Asset row an observed IP
belongs to (P1b of manager/docs/ATTACK_PATH_PLAN.md).

Before this, five code paths each ran their own `SELECT … WHERE engagement_id = ?
AND ip_address = ?` and called `scalar_one_or_none()`. Two problems:

  * identity was the IP alone, so two sites using the same private range merged
    into one asset (FM-14);
  * nothing enforced uniqueness, so a concurrent insert or any intentional
    second row for an IP made every one of those lookups raise
    MultipleResultsFound and abort the caller (the identity policy below creates
    such rows on purpose).

Every path now resolves through here. The policy (which observations share an
asset) lives in app/detection/asset_identity.py; this module applies it to the
database:

  scope None (global identity)
      → the row with site_id NULL if there is one, else the oldest row for the IP.
  scope = site S (per-site identity, private IP, probe of site S)
      → the row for (ip, S); else ADOPT the legacy NULL-scoped row for the IP
        (an engagement that switches to per-site keeps its existing history on
        the first site to report it); else a new row scoped to S.

Lookups are deterministic (ordered by created_at, id) and never raise on
duplicates.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.detection.asset_identity import MODE_GLOBAL, identity_site, mode_from_roe
from app.models.asset import Asset
from app.models.enums import AssetType

logger = structlog.get_logger()


@dataclass(frozen=True)
class IdentityContext:
    """How observations from ONE submission are scoped: the engagement's identity
    mode and the site of the probe that produced them."""
    mode: str = MODE_GLOBAL
    site_id: uuid.UUID | None = None

    def scope_for(self, ip: Any) -> uuid.UUID | None:
        return identity_site(ip, self.site_id, self.mode)


GLOBAL_IDENTITY = IdentityContext()


async def identity_context(db: AsyncSession, engagement_id: uuid.UUID, *,
                           agent_id: Any = None,
                           scan_result_id: Any = None) -> IdentityContext:
    """Build the context for one submission. Best-effort: any failure yields the
    global context, which is exactly today's behaviour."""
    try:
        from app.models.agent import Agent
        from app.models.engagement import Engagement
        from app.models.scan_result import ScanResult

        engagement = await db.get(Engagement, engagement_id)
        mode = mode_from_roe(getattr(engagement, "rules_of_engagement", None))
        if mode == MODE_GLOBAL:
            return IdentityContext(mode=mode)
        if agent_id is None and scan_result_id is not None:
            sr = await db.get(ScanResult, scan_result_id)
            agent_id = getattr(sr, "agent_id", None)
        site_id = None
        if agent_id is not None:
            agent = await db.get(Agent, agent_id if isinstance(agent_id, uuid.UUID)
                                 else uuid.UUID(str(agent_id)))
            site_id = getattr(agent, "site_id", None)
        return IdentityContext(mode=mode, site_id=site_id)
    except Exception as exc:  # noqa: BLE001 — identity must never fail ingest
        logger.warning("asset_identity.context_failed", engagement_id=str(engagement_id),
                       error=str(exc))
        return GLOBAL_IDENTITY


def host_of(target: Any) -> str | None:
    """'10.0.0.5:443' → '10.0.0.5'; IPv6 and bare hosts unchanged; None if empty."""
    if not target:
        return None
    t = str(target)
    return t.split(":", 1)[0] if t.count(":") == 1 else t


def _ordered(rows: Iterable[Asset]) -> list[Asset]:
    return sorted(rows, key=lambda a: (getattr(a, "created_at", None) or datetime.min.replace(tzinfo=timezone.utc),
                                       str(getattr(a, "id", ""))))


def pick_asset(rows: Iterable[Asset], scope: Any) -> tuple[Asset | None, bool]:
    """Choose the row for one IP from its candidate rows. Returns (asset, adopt)
    where adopt=True means a legacy NULL-scoped row must be claimed for `scope`.
    Pure — the DB-facing functions below share it, so single and batch paths
    can never disagree."""
    rows = _ordered(rows)
    if scope is None:
        unscoped = [a for a in rows if a.site_id is None]
        return (unscoped[0] if unscoped else (rows[0] if rows else None)), False
    exact = [a for a in rows if a.site_id == scope]
    if exact:
        return exact[0], False
    legacy = [a for a in rows if a.site_id is None]
    if legacy:
        return legacy[0], True
    return None, False


def _adopt(asset: Asset, scope: Any) -> None:
    logger.info("asset_identity.adopted", asset_id=str(asset.id), site_id=str(scope))
    asset.site_id = scope


async def find_asset(db: AsyncSession, engagement_id: uuid.UUID, host: str,
                     identity: IdentityContext = GLOBAL_IDENTITY) -> Asset | None:
    """Existing asset for one host under the identity policy, or None."""
    rows = (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id, Asset.ip_address == host)
    )).scalars().all()
    scope = identity.scope_for(host)
    asset, adopt = pick_asset(rows, scope)
    if asset is not None and adopt:
        _adopt(asset, scope)
    return asset


async def resolve_asset(db: AsyncSession, engagement_id: uuid.UUID, target: Any, *,
                        identity: IdentityContext | None = None,
                        cache: dict | None = None) -> Asset | None:
    """Find or create the Asset for a probe-reported target.

    `cache` is a caller-owned dict for one run — keyed by the host (global
    identity) or (site, host) (per-site) — so a host with many findings is
    resolved once."""
    host = host_of(target)
    if not host:
        return None
    identity = identity or GLOBAL_IDENTITY
    scope = identity.scope_for(host)
    key = host if scope is None else (scope, host)
    if cache is not None and key in cache:
        return cache[key]
    asset = await find_asset(db, engagement_id, host, identity)
    if asset is None:
        asset = Asset(engagement_id=engagement_id, ip_address=host, site_id=scope,
                      asset_type=AssetType.server, last_seen=datetime.now(timezone.utc))
        db.add(asset)
        await db.flush()
    if cache is not None:
        cache[key] = asset
    return asset


async def find_assets_batch(db: AsyncSession, engagement_id: uuid.UUID,
                            hosts: Iterable[str],
                            identity: IdentityContext = GLOBAL_IDENTITY) -> dict[str, Asset]:
    """{host: existing Asset} for many hosts in ONE query, same policy as
    find_asset. Hosts with no matching row are absent from the result."""
    hosts = [h for h in dict.fromkeys(hosts) if h]
    if not hosts:
        return {}
    by_ip: dict[str, list[Asset]] = {}
    for a in (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id, Asset.ip_address.in_(hosts))
    )).scalars().all():
        by_ip.setdefault(a.ip_address, []).append(a)
    out: dict[str, Asset] = {}
    for host in hosts:
        scope = identity.scope_for(host)
        asset, adopt = pick_asset(by_ip.get(host, []), scope)
        if asset is None:
            continue
        if adopt:
            _adopt(asset, scope)
        out[host] = asset
    return out
