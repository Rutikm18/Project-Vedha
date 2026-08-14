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

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.detection.vantage_fusion import fused_service_exposure
from app.models.asset import Asset
from app.models.scan_result import ScanResult
from app.models.service import Service

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


async def recompute_fused_exposure(
    db: AsyncSession, engagement_id: uuid.UUID, *, external_vantages=None,
) -> int:
    """Fuse all probes' exposure_matrix observations for an engagement and stamp
    the fleet-wide verdict onto Service rows. Returns the number of services
    updated. Best-effort — logs and returns 0 on any failure."""
    try:
        rows = (await db.execute(
            select(ScanResult.agent_id, ScanResult.facts).where(
                ScanResult.engagement_id == engagement_id,
                ScanResult.scan_type == "exposure_matrix",
            )
        )).all()
        results = _results_from_scan_rows(rows)
        if not results:
            return 0
        fused = fused_service_exposure(results, external_vantages=external_vantages)
        if not fused:
            return 0

        # ip → {(proto, port): verdict}
        by_ip: dict[str, dict[tuple[str, int], str]] = {}
        for (ip, proto, port), verdict in fused.items():
            by_ip.setdefault(ip, {})[(proto, port)] = verdict

        assets = (await db.execute(
            select(Asset.id, Asset.ip_address).where(
                Asset.engagement_id == engagement_id,
                Asset.ip_address.in_(list(by_ip.keys())),
            )
        )).all()
        updated = 0
        for asset_id, ip in assets:
            wanted = by_ip.get(ip) or {}
            if not wanted:
                continue
            services = (await db.execute(
                select(Service).where(Service.asset_id == asset_id)
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
