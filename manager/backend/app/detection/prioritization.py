"""Persist the canonical Manager risk score for all active findings.

WHY THIS EXISTS: findings arrive from three paths — the CVE detection engine
(engine_bridge), the probe's self-assessed findings (finding_translator), and
network-service hygiene (service_vuln) — but only the separate nessus/nuclei
path (app/vuln/enrichment.py, live-API) ever computed Finding.risk_score. So the
numeric score every dashboard/portal/report sorts by was NULL for the bulk of
findings, leaving them effectively unprioritized. This module gives every
finding one comparable, offline, reproducible risk_score.

The formula itself lives in :mod:`app.services.risk_rank`; keeping one pure
implementation prevents ingestion paths from silently drifting onto different
scales. Posture rules may carry their own 0-100 score as evidence, but it never
bypasses the Manager formula or maps 100 directly to the Manager ceiling.

OFFLINE: EPSS/KEV come from the detection_engine's pinned snapshots (never a live
API), so the same findings score the same on any machine, any day.
"""
from __future__ import annotations

import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import AssetCriticality, FindingStatus
from app.models.finding import Finding
from app.models.service import Service
from app.services.risk_rank import compute_risk_rank

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
    """Score a posture finding with the Manager formula.

    The historical name is retained for compatibility with the ingestion seam.
    Crucially, the rule's upstream 0-100 value is not multiplied by ten: Manager
    recomputes from severity, exploitability, context, and evidence quality.
    """
    if (not isinstance(evidence, dict) or not evidence.get("rule_id")
            or not (evidence.get("severity") or evidence.get("priority"))):
        return None

    try:
        confidence = int(evidence["confidence"]) if evidence.get("confidence") is not None else None
    except (TypeError, ValueError, OverflowError):
        confidence = None

    internet_facing = evidence.get("internet_facing")
    auth_enforced = evidence.get("auth_enforced")
    return float(compute_risk_rank(
        severity=str(evidence.get("severity") or evidence.get("priority") or "info"),
        cvss_score=None,
        epss_score=None,
        kev=bool(evidence.get("kev")),
        exploit_validated=bool(evidence.get("exploit_validated")),
        verification_state=str(evidence.get("state")) if evidence.get("state") else None,
        confidence=confidence,
        asset_criticality=(str(evidence.get("asset_criticality"))
                           if evidence.get("asset_criticality") else None),
        internet_facing=internet_facing if isinstance(internet_facing, bool) else None,
        auth_enforced=auth_enforced if isinstance(auth_enforced, bool) else None,
    ))


def composite_risk_score(
    *,
    cvss: float,
    epss: float,
    kev: bool,
    exploit_validated: bool,
    severity: str = "info",
    asset_criticality: str = "medium",
    exposure: str | None = None,
    verification_state: str | None = None,
    confidence: int | None = None,
    auth_enforced: bool | None = None,
) -> float:
    """Compatibility wrapper around the canonical 0-1000 risk function."""
    exposure_value = (exposure or "").lower()
    internet_facing = (
        True if exposure_value in {"external", "internet"}
        else False if exposure_value in {"internal", "isolated"}
        else None
    )
    return float(compute_risk_rank(
        severity=severity,
        cvss_score=cvss,
        epss_score=epss,
        kev=kev,
        exploit_validated=exploit_validated,
        verification_state=verification_state,
        confidence=confidence,
        asset_criticality=asset_criticality,
        internet_facing=internet_facing,
        auth_enforced=auth_enforced,
    ))


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

        score = composite_risk_score(
            cvss=float(f.cvss_score) if f.cvss_score is not None else 0.0,
            epss=epss,
            kev=kev,
            exploit_validated=bool(f.exploit_validated),
            severity=getattr(f.severity, "value", str(f.severity)),
            asset_criticality=crit,
            exposure=exposure,
            verification_state=f.verification_state,
            confidence=f.verification_confidence,
            auth_enforced=(evidence.get("auth_enforced")
                           if isinstance(evidence.get("auth_enforced"), bool) else None),
        )
        if f.risk_score is None or float(f.risk_score) != score:
            f.risk_score = score
            changed += 1

    if changed:
        await db.flush()
        logger.info("prioritization.scored", engagement_id=str(engagement_id),
                    findings=len(findings), changed=changed)
    return changed
