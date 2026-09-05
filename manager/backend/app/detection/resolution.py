"""
resolution.py — coverage-gated auto-resolution of findings.

Split into a PURE core (host_of / build_coverage / decide_resolution) that is
fully unit-testable without a database, and a thin async applier
(evaluate_resolutions) that walks the engagement's still-open findings and
applies the pure decision. Wired into engine_bridge.create_findings_from_facts.

Safety rule: absence of a finding is only meaningful if we PROVED we looked.
A host counts as covered this run only if a *completed* scanner produced a fact
about it; a degraded/failed/skipped scanner is not proof.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.services.finding_events import record_event


def host_of(target: str) -> str:
    """IP/host part of a probe target: '10.0.0.5:443' -> '10.0.0.5'.
    Mirrors finding_translator._resolve_asset's host extraction."""
    if not target:
        return ""
    return target.split(":", 1)[0] if target.count(":") == 1 else target


def build_coverage(scanner_runs: list[dict] | None, facts: list[dict] | None) -> dict:
    """What this run PROVABLY re-observed. An asset is covered only if a
    completed scanner produced a fact about it. Fail-closed: no scanner_runs
    (older probe) → empty coverage → nothing auto-resolves."""
    scanner_runs = scanner_runs or []
    facts = facts or []
    completed = {sr.get("id") for sr in scanner_runs if sr.get("status") == "completed"}
    # "degraded" and "skipped" are both non-proof for coverage, but they are NOT
    # the same event and must not share a label. A scanner that stood down
    # because the service isn't on the host ("No eligible target or service was
    # observed.") is the funnel working; reporting it as degraded made a healthy
    # full run look like ten broken scanners. Keep the coverage semantics —
    # `assets` is still built from `completed` alone, so neither state can prove
    # we looked — and only split what the operator reads.
    degraded = {
        sr.get("id") for sr in scanner_runs
        if sr.get("status") in ("degraded", "failed")
    }
    skipped = {sr.get("id") for sr in scanner_runs if sr.get("status") == "skipped"}
    assets = {
        host_of(f.get("target", "")) for f in facts
        if f.get("scanner") in completed and host_of(f.get("target", ""))
    }
    return {
        "assets": sorted(a for a in assets if a),
        "scanners_completed": sorted(c for c in completed if c),
        "scanners_degraded": sorted(d for d in degraded if d),
        "scanners_skipped": sorted(s for s in skipped if s),
    }


def resolution_threshold(severity: FindingSeverity) -> int:
    """Consecutive coverage-proven clean runs required before auto-close.
    critical/high demand a SECOND confirmation — a premature 'you're safe' on a
    critical is the costliest false signal in the product."""
    return 2 if severity in (FindingSeverity.critical, FindingSeverity.high) else 1


@dataclass(frozen=True)
class ResolutionOutcome:
    action: str        # "skip" | "pending" | "resolve"
    miss_count: int    # the new resolution_miss_count to persist
    reason: str


def decide_resolution(*, covered: bool, db_changed: bool,
                      miss_count: int, severity: FindingSeverity) -> ResolutionOutcome:
    """Pure heart of auto-resolution. Given whether the finding's asset was
    re-observed this run (covered), whether the vuln-DB basis changed, and the
    current miss streak, decide what to do. Never resolves without coverage."""
    if not covered:
        return ResolutionOutcome("skip", miss_count, "asset not re-observed (out of coverage)")
    if db_changed:
        return ResolutionOutcome("skip", miss_count,
                                 "absent under a changed vuln-DB basis; not a confirmed fix")
    new_count = miss_count + 1
    threshold = resolution_threshold(severity)
    if new_count >= threshold:
        return ResolutionOutcome("resolve", new_count,
                                 f"coverage-proven clean for {new_count} run(s) >= threshold {threshold}")
    return ResolutionOutcome("pending", new_count,
                             f"coverage-proven clean {new_count}/{threshold} runs")


async def evaluate_resolutions(
    db: AsyncSession, engagement_id: uuid.UUID, run, coverage: dict, now: datetime,
) -> int:
    """Apply decide_resolution to every engine-managed open/confirmed finding
    NOT touched by `run` (i.e. detection_run_id != run.id). Returns the number
    auto-resolved. Findings with no detection_run_id (probe self-assessed path,
    legacy) are intentionally NOT governed here."""
    covered = set(coverage.get("assets") or [])
    rows = (await db.execute(
        select(Finding, Asset.ip_address)
        .join(Asset, Finding.asset_id == Asset.id)
        .where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_((FindingStatus.open, FindingStatus.confirmed)),
            Finding.detection_run_id.isnot(None),
            Finding.detection_run_id != run.id,
        )
    )).all()

    resolved = 0
    for finding, ip in rows:
        db_changed = (
            run.vuln_db_version is not None
            and finding.detected_db_version is not None
            and finding.detected_db_version != run.vuln_db_version
        )
        outcome = decide_resolution(
            covered=ip in covered, db_changed=db_changed,
            miss_count=finding.resolution_miss_count, severity=finding.severity,
        )
        finding.resolution_miss_count = outcome.miss_count
        if outcome.action == "resolve":
            finding.status = FindingStatus.remediated
            finding.resolved_at = now
            finding.resolution_method = "auto"
            finding.resolution_run_id = run.id
            await record_event(
                db, finding, "resolved", actor="auto-resolution", actor_type="system",
                from_status="open", to_status=FindingStatus.remediated,
                detail={
                    "method": "auto", "run_id": str(run.id),
                    "miss_count": outcome.miss_count, "reason": outcome.reason,
                },
            )
            resolved += 1
    await db.flush()
    return resolved


def apply_manual_reopen(finding, *, by: str, now) -> None:
    """Operator reopens an auto/'manually'-resolved finding. Mirrors the engine's
    regression reopen but records the human who did it. History preserved."""
    finding.status = FindingStatus.open
    finding.reopened_count = (finding.reopened_count or 0) + 1
    finding.resolution_miss_count = 0
    finding.resolved_at = None
    finding.resolution_method = None
    finding.resolution_run_id = None
    ev = dict(finding.evidence or {})
    ev["reopened_by"] = by
    finding.evidence = ev
