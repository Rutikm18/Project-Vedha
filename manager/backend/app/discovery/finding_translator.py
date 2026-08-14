"""
Convert a probe's self-assessed `findings` into persisted Finding rows.

WHY THIS EXISTS: submit_job_result() in routers/agents.py already promotes a
probe's discovered hosts/services into Asset/Service rows via
_promote_assets(), but nothing converted the probe's own severity-tagged
`findings` (tls_scan/smb_enum/mcp_discovery/ai_service_discovery already embed
these directly in their result envelope — see probe/scanners/{tls,smb,mcp_ai}.py)
into dashboard-visible Finding rows. They were silently dropped on arrival,
even though the scanners themselves already computed them. This is the
missing translation step — not a new detection engine, just a bridge.

Deliberately excludes vuln_scan: that scan_type is never agent-dispatched in
practice (see AGENT_EXECUTABLE_TYPES in routers/agents.py) and its nuclei
findings use a different shape (template_id/matched_at/cves) handled by the
existing nessus/nuclei -> run_post_scan_enrichment path instead.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import AssetType, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.models.service import Service

logger = structlog.get_logger()

# Only these scan_types embed pre-assessed `findings` in their result envelope
# today. The rest (host_discovery, discovery, port_scan, mass_scan,
# service_fingerprint, udp_scan, web_scan) are pure inventory — nothing for
# this translator to do until/unless they grow their own findings list too.
FINDING_PRODUCING_SCAN_TYPES = {"tls_scan", "smb_enum", "mcp_discovery", "ai_service_discovery"}

# A Finding the operator already resolved (remediated/fp) is NOT deduped if the
# same issue reappears on a later scan — that is a real regression signal, not
# noise, and should surface as a fresh finding. Only still-relevant statuses
# suppress a duplicate.
_DEDUP_SUPPRESSING_STATUSES = (FindingStatus.open, FindingStatus.confirmed, FindingStatus.accepted)


def _map_severity(raw: str | None) -> FindingSeverity:
    try:
        return FindingSeverity((raw or "info").lower())
    except ValueError:
        return FindingSeverity.info


async def _resolve_asset(db: AsyncSession, engagement_id: uuid.UUID, target: str | None) -> Asset | None:
    """Find the Asset for a probe-reported target IP, creating a minimal one if needed.

    A probe's tls_scan/smb_enum/etc. can run standalone (no prior discovery job
    promoted this host yet), so the asset may not exist — create a bare-bones
    row rather than dropping the finding for lack of somewhere to attach it.
    """
    if not target:
        return None
    host = target.split(":", 1)[0] if target.count(":") == 1 else target
    existing = (await db.execute(
        select(Asset).where(Asset.engagement_id == engagement_id, Asset.ip_address == host)
    )).scalar_one_or_none()
    if existing:
        return existing
    asset = Asset(engagement_id=engagement_id, ip_address=host,
                  asset_type=AssetType.server, last_seen=datetime.now(timezone.utc))
    db.add(asset)
    await db.flush()
    return asset


def _finding_port(f: dict) -> int | None:
    """Best-effort port for a probe finding: explicit `port`, else the ':NNN'
    suffix of `target` (host:port). None when neither is present/parseable."""
    raw = f.get("port")
    if raw is not None:
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
    target = f.get("target") or ""
    if target.count(":") == 1:
        _host, _sep, port_s = target.partition(":")
        try:
            return int(port_s)
        except ValueError:
            return None
    return None


async def _escalate_by_exposure(
    db: AsyncSession, asset_id: uuid.UUID | None, f: dict, severity: FindingSeverity,
) -> tuple[FindingSeverity, str | None]:
    """Bump severity one rung when the finding's service is internet-reachable
    (Service.exposure == 'external', stamped by a prior exposure_matrix scan).

    Returns (severity, exposure) so the caller can record WHY it escalated.
    Best-effort: any lookup problem leaves the severity unchanged.
    """
    if asset_id is None:
        return severity, None
    port = _finding_port(f)
    if port is None:
        return severity, None
    try:
        svc = (await db.execute(
            select(Service).where(Service.asset_id == asset_id, Service.port == port)
        )).scalars().first()
    except Exception:  # noqa: BLE001 — escalation is advisory, never fatal
        return severity, None
    if svc is None or not svc.exposure:
        return severity, None
    from app.discovery.exposure import escalate_for_exposure
    return escalate_for_exposure(severity, svc.exposure), svc.exposure


async def _find_open_duplicate(
    db: AsyncSession, engagement_id: uuid.UUID, asset_id: uuid.UUID | None, title: str,
) -> Finding | None:
    """A still-relevant Finding with the same (engagement, asset, title), if any.

    Re-running the same probe scan weekly must not pile up duplicate rows for
    an unchanged issue — but a finding the operator already remediated/marked
    fp is intentionally NOT matched here (see _DEDUP_SUPPRESSING_STATUSES):
    if it reappears on a later scan that's a regression worth a fresh row,
    not noise to suppress.
    """
    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status.in_(_DEDUP_SUPPRESSING_STATUSES),
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()


async def create_findings_from_probe_result(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
) -> int:
    """Convert a probe's self-assessed `findings` list into persisted Finding rows.

    Best-effort per finding: one bad/malformed entry must never abort the rest
    or fail the probe's result submission (mirrors _promote_assets' philosophy
    in routers/agents.py). Returns the number of NEW Finding rows created
    (re-touching an existing open duplicate does not count).
    """
    scan_type = result.get("scan_type")
    if scan_type not in FINDING_PRODUCING_SCAN_TYPES:
        return 0
    raw_findings = result.get("findings") or []
    if not raw_findings:
        return 0

    now = datetime.now(timezone.utc)
    created = 0
    for f in raw_findings:
        if not isinstance(f, dict):
            continue
        try:
            asset = await _resolve_asset(db, engagement_id, f.get("target"))
            title = (f.get("title") or f"{scan_type} finding")[:500]
            asset_id = asset.id if asset else None

            dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
            if dup is not None:
                # Still relevant and still present — touch evidence (bumps
                # updated_at) and advance last_seen rather than creating a
                # literal duplicate row. (No detection_run: this is the probe's
                # own self-assessed path, not the detection engine.)
                dup.evidence = {**f, "scan_type": scan_type, "engine": result.get("engine")}
                dup.last_seen = now
                continue

            severity = _map_severity(f.get("severity"))
            severity, exposure = await _escalate_by_exposure(db, asset_id, f, severity)
            evidence = {**f, "scan_type": scan_type, "engine": result.get("engine")}
            if exposure == "external":
                evidence["exposure_escalated"] = True
                evidence["exposure"] = exposure
            db.add(Finding(
                engagement_id=engagement_id,
                asset_id=asset_id,
                title=title,
                description=f.get("detail"),
                severity=severity,
                status=FindingStatus.open,
                evidence=evidence,
                first_seen=now,
                last_seen=now,
            ))
            created += 1
        except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
            logger.warning("probe_finding.create_failed", scan_type=scan_type, error=str(exc))

    if created or raw_findings:
        await db.flush()
    return created


_SCAN_HEALTH_TITLE = "Scan coverage degraded — results may under-report exposure"


async def create_scan_health_finding(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
) -> int:
    """Raise ONE engagement-level finding when the probe's own metrics say the
    scan was degraded/incomplete (a false-NEGATIVE risk: real services may have
    gone unseen). Returns 1 if a new finding was created, else 0.

    Deduped by title so a chronically firewalled segment refreshes one finding
    instead of piling up. Best-effort — never sinks the result submission.
    """
    from app.discovery.scan_health import scan_health_summary

    summary = scan_health_summary(result)
    if not summary["should_warn"]:
        return 0
    now = datetime.now(timezone.utc)
    try:
        dup = await _find_open_duplicate(db, engagement_id, None, _SCAN_HEALTH_TITLE)
        evidence = {"scan_health": summary, "scan_type": result.get("scan_type"),
                    "engine": result.get("engine")}
        if dup is not None:
            dup.evidence = evidence
            dup.last_seen = now
            return 0
        db.add(Finding(
            engagement_id=engagement_id,
            asset_id=None,
            title=_SCAN_HEALTH_TITLE,
            description=summary["reason"],
            severity=FindingSeverity.low,
            status=FindingStatus.open,
            evidence=evidence,
            first_seen=now,
            last_seen=now,
        ))
        await db.flush()
        return 1
    except Exception as exc:  # noqa: BLE001 — coverage warning must not sink the batch
        logger.warning("scan_health.finding_failed", error=str(exc))
        return 0
