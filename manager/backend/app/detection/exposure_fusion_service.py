"""
exposure_fusion_service.py — apply multi-probe vantage fusion to Service rows.

Track A3 stamped each Service with the exposure verdict from the ingesting probe
alone. That is single-vantage: an internet-open port scanned by an INTERNAL probe
is recorded `internal_only`. This service gathers EVERY probe's exposure_matrix
observations for an engagement, fuses them (app/detection/vantage_fusion.py), and
corrects Service.exposure to the fleet-wide verdict — so a port any external probe
saw open is finally marked `external`.

The fusion itself is pure and unit-tested; this module is the thin, defensive DB
adapter (gather → fuse → stamp). Best-effort: it never raises into the caller.
"""
from __future__ import annotations

import uuid
from typing import Any

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.detection.asset_identity import MODE_GLOBAL, identity_site, mode_from_roe
from app.detection.vantage_fusion import fused_service_exposure
from app.models.agent import Agent
from app.models.asset import Asset
from app.models.engagement import Engagement
from app.models.scan_result import ScanResult
from app.models.service import Service
from app.services.asset_resolution import pick_asset

logger = structlog.get_logger()


def _results_from_scan_rows(rows) -> list[dict]:
    """Reconstruct one {"exposure": [...]} dict per probe from persisted facts.

    Each exposure_matrix fact carries the per-target matrix in `data`; `target`
    is the ip. We group by agent so each probe contributes its own vantage(s).
    """
    per_agent: dict = {}
    for agent_id, facts in rows:
        entries = per_agent.setdefault(agent_id, [])
        for f in facts or []:
            if (
                isinstance(f, dict)
                and f.get("scanner") == "exposure_matrix"
                and isinstance(f.get("data"), dict)
                and f.get("target")
            ):
                entries.append({"ip": f["target"], **f["data"]})
    return [{"exposure": entries} for entries in per_agent.values() if entries]


def _exposure_entries(facts) -> list[dict]:
    entries: list[dict] = []
    for f in facts or []:
        if (
            isinstance(f, dict)
            and f.get("scanner") == "exposure_matrix"
            and isinstance(f.get("data"), dict)
            and f.get("target")
        ):
            entries.append({"ip": f["target"], **f["data"]})
    return entries


def scoped_results(rows, mode: str = MODE_GLOBAL) -> dict[Any, list[dict]]:
    """Group persisted exposure observations by the ASSET SCOPE they describe.

    `rows` are (agent_id, site_id, facts). The fusion compares vantages for the
    SAME host, so it must only ever see observations of one host:

      * a globally-routable IP is one host everywhere        -> scope None, every
        probe's view of it is fused (an external probe + an internal one);
      * a private IP under `per_site` identity is a different host at each site
        -> scope = the observing probe's site, so site A's 10.0.0.5 and site B's
        10.0.0.5 are fused separately and never with each other.

    In `global` mode every IP is scope None: exactly the behaviour before P1b."""
    per_agent: dict[Any, tuple[Any, list[dict]]] = {}
    for agent_id, site_id, facts in rows:
        entries = _exposure_entries(facts)
        if entries:
            per_agent.setdefault(agent_id, (site_id, []))[1].extend(entries)
    out: dict[Any, list[dict]] = {}
    for site_id, entries in per_agent.values():
        by_scope: dict[Any, list[dict]] = {}
        for entry in entries:
            by_scope.setdefault(identity_site(entry["ip"], site_id, mode), []).append(entry)
        for scope, scoped in by_scope.items():
            out.setdefault(scope, []).append({"exposure": scoped})
    return out


async def recompute_fused_exposure(
    db: AsyncSession, engagement_id: uuid.UUID, *, external_vantages=None,
) -> int:
    """Fuse all probes' exposure_matrix observations for an engagement and stamp
    the fleet-wide verdict onto Service rows. Returns the number of services
    updated. Best-effort — logs and returns 0 on any failure.

    Site-aware (P1b-3): observations are fused per asset scope (see
    `scoped_results`) and stamped onto the asset that scope resolves to, so one
    site's exposure is never written onto another site's machine."""
    try:
        engagement = await db.get(Engagement, engagement_id)
        mode = mode_from_roe(getattr(engagement, "rules_of_engagement", None))
        rows = (await db.execute(
            select(ScanResult.agent_id, Agent.site_id, ScanResult.facts)
            .outerjoin(Agent, Agent.id == ScanResult.agent_id)
            .where(
                ScanResult.engagement_id == engagement_id,
                ScanResult.scan_type == "exposure_matrix",
            )
        )).all()
        scoped = scoped_results(rows, mode)
        if not scoped:
            return 0

        # scope → ip → {(proto, port): verdict}
        verdicts: dict[Any, dict[str, dict[tuple[str, int], str]]] = {}
        for scope, results in scoped.items():
            fused = fused_service_exposure(results, external_vantages=external_vantages)
            for (ip, proto, port), verdict in fused.items():
                verdicts.setdefault(scope, {}).setdefault(ip, {})[(proto, port)] = verdict
        wanted_ips = {ip for by_ip in verdicts.values() for ip in by_ip}
        if not wanted_ips:
            return 0

        candidates: dict[str, list[Asset]] = {}
        for asset in (await db.execute(
            select(Asset).where(
                Asset.engagement_id == engagement_id,
                Asset.ip_address.in_(list(wanted_ips)),
            )
        )).scalars().all():
            candidates.setdefault(asset.ip_address, []).append(asset)

        updated = 0
        for scope, by_ip in verdicts.items():
            for ip, wanted in by_ip.items():
                # The same lookup ingest uses; adoption is ingest's job, not ours.
                asset, _ = pick_asset(candidates.get(ip, []), scope)
                if asset is None:
                    continue
                services = (await db.execute(
                    select(Service).where(Service.asset_id == asset.id)
                )).scalars().all()
                for svc in services:
                    verdict = wanted.get((str(svc.protocol).lower(), int(svc.port)))
                    if verdict and svc.exposure != verdict:
                        svc.exposure = verdict
                        updated += 1
        await db.flush()
        return updated
    except Exception as exc:  # noqa: BLE001 — fusion is advisory, never fatal
        logger.warning("exposure_fusion.failed", engagement_id=str(engagement_id), error=str(exc))
        return 0
