"""
prioritization.py — the single risk-scoring engine for ALL findings.

WHY THIS EXISTS: findings arrive from three paths — the CVE detection engine
(engine_bridge), the probe's self-assessed findings (finding_translator), and
network-service hygiene (service_vuln) — but only the separate nessus/nuclei
path (app/vuln/enrichment.py, live-API) ever computed Finding.risk_score. So the
numeric score every dashboard/portal/report sorts by was NULL for the bulk of
findings, leaving them effectively unprioritized. This module gives every
finding one comparable, offline, reproducible risk_score.

THE SCORE (0-1000, unified with app/vuln/enrichment.compute_composite_risk so the
two paths agree):

    risk = ( cvss·0.25 + epss·0.20 + kev·0.20 + exploit_validated·0.15
             + asset_criticality·0.10 + exposure·0.10 ) · 1000

Only difference from the nessus formula: its two attack-path terms (path_depth,
lateral_impact — 0.05 each, unavailable when a finding is first persisted) are
replaced by a single `exposure` term. Exposure — is the vulnerable service
actually internet-reachable — was missing from risk entirely, yet it is the
strongest real-world amplifier: the same CVE on an external service is far more
urgent than on an isolated one.

OFFLINE: EPSS/KEV come from the detection_engine's pinned snapshots (never a live
API), so the same findings score the same on any machine, any day.
"""
from __future__ import annotations

import math
import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import AssetCriticality, FindingStatus
from app.models.finding import Finding
from app.models.service import Service

logger = structlog.get_logger()

# Asset criticality → 0-1 weight. Mirrors app/vuln/enrichment._CRIT_WEIGHT so the
# two scoring paths stay consistent.
_CRIT_WEIGHT: dict[str, float] = {
    AssetCriticality.critical.value: 1.0,
    AssetCriticality.high.value:     0.75,
    AssetCriticality.medium.value:   0.5,
    AssetCriticality.low.value:      0.25,
}

# Service exposure → 0-1 amplifier. Unknown defaults to 0.5 (neutral) so a scan
# that never ran exposure_matrix neither inflates nor suppresses the score.
_EXPOSURE_WEIGHT: dict[str, float] = {
    "external": 1.0, "internet": 1.0,
    "partial": 0.6, "dmz": 0.6,
    "internal": 0.2, "isolated": 0.1,
}
_EXPOSURE_DEFAULT = 0.5
# Rank used to pick an asset's single strongest exposure across its services.
_EXPOSURE_RANK = {"external": 4, "internet": 4, "partial": 3, "dmz": 3,
                  "internal": 2, "isolated": 1}


def _posture_risk_on_manager_scale(evidence: object) -> float | None:
    """Return an engine posture score on Finding.risk_score's 0-1000 scale.

    Posture rules own a separate 0-100 model that already incorporates severity,
    evidence state, reachability, and authentication.  Re-running the CVE formula
    would both erase those signals (posture findings have no CVSS) and make them
    incomparable with Manager findings.  `rule_id` is the provenance guard that
    prevents arbitrary imported `risk_score` fields from receiving this conversion.
    """
    if not isinstance(evidence, dict) or not evidence.get("rule_id"):
        return None
    raw = evidence.get("risk_score")
    try:
        score = float(raw)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(score) or not 0.0 <= score <= 100.0:
        return None
    return round(score * 10.0, 2)


def composite_risk_score(
    *,
    cvss: float,
    epss: float,
    kev: bool,
    exploit_validated: bool,
    asset_criticality: str = "medium",
    exposure: str | None = None,
) -> float:
    """The unified 0-1000 composite (see module docstring). Pure + deterministic."""
    cvss_n = min(max(float(cvss), 0.0), 10.0) / 10.0
    epss_n = min(max(float(epss), 0.0), 1.0)
    kev_n = 1.0 if kev else 0.0
    expl_n = 1.0 if exploit_validated else 0.0
    crit_n = _CRIT_WEIGHT.get(asset_criticality, 0.5)
    exp_n = _EXPOSURE_WEIGHT.get((exposure or "").lower(), _EXPOSURE_DEFAULT)
    score = (
        cvss_n * 0.25
        + epss_n * 0.20
        + kev_n * 0.20
        + expl_n * 0.15
        + crit_n * 0.10
        + exp_n * 0.10
    ) * 1000
    return round(score, 2)


def _strongest_exposure(values: list[str | None]) -> str | None:
    """The most-exposed value among an asset's services (external beats internal)."""
    ranked = [(v, _EXPOSURE_RANK.get((v or "").lower(), 0)) for v in values if v]
    return max(ranked, key=lambda t: t[1])[0] if ranked else None


def _load_offline_kev_epss():
    """(kev_db, epss_db) from the pinned snapshots, or (None, None) if the
    detection_engine isn't importable. Best-effort: findings then fall back to
    whatever EPSS/KEV they already carry."""
    try:
        from app.detection.engine_bridge import _ensure_importable
        if not _ensure_importable():
            return None, None
        from enrichment_db import load_kev, load_epss  # type: ignore
        return load_kev(), load_epss()
    except Exception as exc:  # noqa: BLE001 — enrichment is advisory, never fatal
        logger.warning("prioritization.kev_epss_unavailable", error=str(exc))
        return None, None


async def prioritize_engagement_findings(
    db: AsyncSession, engagement_id: uuid.UUID,
) -> int:
    """(Re)compute risk_score for every still-relevant finding in the engagement.

    Idempotent — safe to run after any finding-producing path. Also backfills a
    finding's epss_score / evidence.kev when the offline snapshots know a value
    the finding was created without (e.g. service_vuln findings). Returns the
    number of findings whose score changed.
    """
    findings = (await db.execute(
        select(Finding).where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_((FindingStatus.open, FindingStatus.confirmed)),
        )
    )).scalars().all()
    if not findings:
        return 0

    # Asset criticality + per-asset strongest exposure, in two bulk queries.
    assets = {a.id: a for a in (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id)
    )).scalars().all()}
    exposure_by_asset: dict[uuid.UUID, str | None] = {}
    svc_rows = (await db.execute(
        select(Service.asset_id, Service.exposure).where(
            Service.asset_id.in_(list(assets.keys()) or [uuid.uuid4()])
        )
    )).all()
    grouped: dict[uuid.UUID, list[str | None]] = {}
    for asset_id, exposure in svc_rows:
        grouped.setdefault(asset_id, []).append(exposure)
    for asset_id, vals in grouped.items():
        exposure_by_asset[asset_id] = _strongest_exposure(vals)

    kev_db, epss_db = _load_offline_kev_epss()

    changed = 0
    for f in findings:
        cve = (f.cve_ids or [None])[0]

        epss = float(f.epss_score) if f.epss_score is not None else 0.0
        if f.epss_score is None and epss_db is not None and cve:
            rec = epss_db.get(cve)
            if rec and rec.get("epss") is not None:
                epss = float(rec["epss"])
                f.epss_score = rec["epss"]

        evidence = f.evidence if isinstance(f.evidence, dict) else {}
        kev = bool((evidence.get("enrichment") or {}).get("kev") or evidence.get("kev"))
        if not kev and kev_db is not None and cve:
            kev = kev_db.is_kev(cve)
            if kev:
                evidence = {**evidence, "kev": True}
                f.evidence = evidence

        asset = assets.get(f.asset_id) if f.asset_id else None
        crit = asset.criticality.value if asset and asset.criticality else "medium"
        exposure = exposure_by_asset.get(f.asset_id) if f.asset_id else None

        posture_score = _posture_risk_on_manager_scale(evidence)
        score = posture_score if posture_score is not None else composite_risk_score(
            cvss=float(f.cvss_score) if f.cvss_score is not None else 0.0,
            epss=epss,
            kev=kev,
            exploit_validated=bool(f.exploit_validated),
            asset_criticality=crit,
            exposure=exposure,
        )
        if f.risk_score is None or float(f.risk_score) != score:
            f.risk_score = score
            changed += 1

    if changed:
        await db.flush()
        logger.info("prioritization.scored", engagement_id=str(engagement_id),
                    findings=len(findings), changed=changed)
    return changed
