"""
asset_identity_report.py — the evidence behind the "should this engagement use
per-site asset identity?" question (P1b-5 of manager/docs/ATTACK_PATH_PLAN.md).

The policy lives in app/detection/asset_identity.py; this module gathers what an
operator needs to decide and to trust the attack-path graph:

  * the engagement's current identity mode and a plain recommendation;
  * which sites authorise overlapping PRIVATE ranges (necessary for a collision);
  * which private IPs different sites report under DIFFERENT host names (the
    concrete proof that two machines are being merged);
  * addresses that currently map to more than one asset (already split);
  * machines seen at several addresses (the dual-homed pivots the graph links);
  * assets too old to trust (stale).

`build_report` is pure; `load_report` is the thin DB adapter around it.
"""
from __future__ import annotations

import uuid
from collections import Counter
from datetime import datetime
from typing import Any, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.detection.asset_identity import (
    DEFAULT_FRESHNESS_DAYS, identity_conflicts, is_stale, link_machines,
    mode_from_roe, overlapping_private_ranges, recommend,
)
from app.models.agent import Agent
from app.models.asset import Asset
from app.models.probe_site import ProbeSite
from app.models.scan_result import ScanResult

# Facts are large JSON; look at the most recent results only. The report says so.
SAMPLED_SCAN_RESULTS = 500

_NAME_KEYS = ("hostname", "dns_name", "netbios_name", "computer_name", "fqdn")


def observation_names(rows: Iterable[tuple[Any, Any]]) -> list[tuple[Any, str, str]]:
    """(site_id, facts) rows -> (site_id, ip, host name) triples for identity_conflicts.
    Best effort: a fact contributes only if it names a host for a target IP."""
    out: list[tuple[Any, str, str]] = []
    for site_id, facts in rows:
        for fact in facts or []:
            if not isinstance(fact, dict) or not fact.get("target"):
                continue
            data = fact.get("data")
            if not isinstance(data, dict):
                continue
            name = next((data[k] for k in _NAME_KEYS if isinstance(data.get(k), str) and data[k].strip()), None)
            if name:
                out.append((site_id, str(fact["target"]).split(":", 1)[0], name))
    return out


def build_report(*, mode: str, sites: list[dict[str, Any]], observations: Iterable[tuple[Any, str, str]],
                 assets: list[Any], now: datetime | None = None,
                 freshness_days: int | None = DEFAULT_FRESHNESS_DAYS,
                 sampled_results: int | None = None) -> dict[str, Any]:
    overlaps = overlapping_private_ranges({str(s["site_id"]): s.get("authorized_cidrs") or [] for s in sites})
    conflicts = identity_conflicts(observations)

    labels = {str(a.id): (getattr(a, "hostname", None) or getattr(a, "ip_address", None) or str(a.id))
              for a in assets}
    by_ip = Counter(a.ip_address for a in assets if getattr(a, "ip_address", None))
    shared = sorted(ip for ip, n in by_ip.items() if n > 1)
    machines = [{**g, "labels": [labels.get(m, m) for m in g["members"]]}
                for g in link_machines(assets, mode, now=now, freshness_days=freshness_days)]
    stale = sorted(str(a.id) for a in assets if is_stale(getattr(a, "last_seen", None), now, freshness_days))

    return {
        "mode": mode,
        "recommendation": recommend(mode, overlaps, conflicts),
        "sites": sites,
        "overlapping_private_ranges": overlaps,
        "identity_conflicts": conflicts,
        "addresses_with_several_assets": shared,
        "linked_machines": machines,
        "stale_assets": {"count": len(stale), "window_days": freshness_days, "asset_ids": stale[:200]},
        "assets": len(assets),
        "evidence_sampled_from": sampled_results,
    }


async def load_report(db: AsyncSession, engagement: Any, *, now: datetime | None = None) -> dict[str, Any]:
    from app.graph.builder import freshness_days_from_roe
    roe = getattr(engagement, "rules_of_engagement", None)
    mode = mode_from_roe(roe)

    assets = list((await db.execute(
        select(Asset).where(Asset.engagement_id == engagement.id)
    )).scalars().all())

    rows = (await db.execute(
        select(Agent.site_id, ScanResult.facts)
        .join(Agent, Agent.id == ScanResult.agent_id)
        .where(ScanResult.engagement_id == engagement.id)
        .order_by(ScanResult.created_at.desc())
        .limit(SAMPLED_SCAN_RESULTS)
    )).all()

    site_ids = {r[0] for r in rows if r[0] is not None} | {a.site_id for a in assets if a.site_id is not None}
    sites: list[dict[str, Any]] = []
    if site_ids:
        per_site_assets = Counter(str(a.site_id) for a in assets if a.site_id is not None)
        for s in (await db.execute(select(ProbeSite).where(ProbeSite.id.in_(site_ids)))).scalars().all():
            sites.append({"site_id": str(s.id), "name": s.name,
                          "authorized_cidrs": list(s.authorized_cidrs or []),
                          "assets": per_site_assets.get(str(s.id), 0)})
        sites.sort(key=lambda s: s["name"] or s["site_id"])

    return build_report(mode=mode, sites=sites, observations=observation_names(rows), assets=assets,
                        now=now, freshness_days=freshness_days_from_roe(roe), sampled_results=len(rows))
