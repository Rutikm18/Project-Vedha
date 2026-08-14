"""
engine_bridge.py — run the deterministic detection_engine on a probe's RAW
FACTS and persist the resulting CVE findings.

The probe ships facts only (no CVEs); detection runs HERE on the manager,
against the pinned vuln DB that lives only on the manager. This is the
new raw-facts path; finding_translator.py handles the legacy self-assessed
path. Both are best-effort: a detection failure must never fail the probe's
result submission.

detection_engine lives outside the backend package (a sibling project). It
is made importable via DETECTION_ENGINE_PATH (set in the image/compose);
if it (or its pinned snapshots) isn't available, this degrades to a no-op
and logs — the probe submission still succeeds.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.asset import Asset
from app.models.finding import Finding
from app.models.detection_run import (
    DetectionRun, RUN_COMPLETED, RUN_FAILED, TRIGGER_FACTS_READY,
)
from app.discovery.finding_translator import _resolve_asset, _find_open_duplicate
from app.detection.attack_paths import attack_path_findings
from app.detection.resolution import build_coverage, evaluate_resolutions
from app.ai.verification_graph import run_verification
from app.config import get_settings

logger = structlog.get_logger()

# Finding statuses that count as "still current" (the live risk set) after a run.
_CURRENT_STATUSES = (FindingStatus.open, FindingStatus.confirmed, FindingStatus.accepted)


def _vuln_db_meta() -> tuple[str | None, str | None]:
    """(content_hash, fetched_at) of the pinned snapshot the engine will use, so
    every run is stamped with its exact vuln-DB basis. Best-effort — returns
    (None, None) if the engine/snapshot isn't importable."""
    if not _ensure_importable():
        return None, None
    try:
        from vuln_db import load_snapshot  # type: ignore
        meta = load_snapshot().meta
        return meta.content_hash, meta.fetched_at
    except Exception as exc:  # noqa: BLE001
        logger.debug("vuln_db.version_unavailable", error=str(exc))
        return None, None

_PRIORITY_TO_SEVERITY = {
    "critical": FindingSeverity.critical, "high": FindingSeverity.high,
    "medium": FindingSeverity.medium, "low": FindingSeverity.low,
    "unknown": FindingSeverity.info,
}


def _ensure_importable() -> bool:
    path = os.environ.get("DETECTION_ENGINE_PATH")
    if not path:
        # dev fallback: manager/detection_engine (sibling of backend/).
        # backend/app/detection/engine_bridge.py -> parents[3] == manager/
        guess = Path(__file__).resolve().parents[3] / "detection_engine"
        path = str(guess) if guess.exists() else ""
    if path and path not in sys.path:
        sys.path.insert(0, path)
    try:
        import pipeline  # noqa: F401  (detection_engine.pipeline)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("detection_engine.unavailable", error=str(exc))
        return False


def detect_findings_from_facts(facts: list[dict]) -> list[dict]:
    """facts (ScanResult dicts) -> detection_engine finding dicts. [] on any
    failure (never raises). Writes facts to a temp JSONL since run_pipeline
    consumes JSONL paths."""
    if not facts or not _ensure_importable():
        return []
    from pipeline import run_pipeline  # type: ignore
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
            for fact in facts:
                fh.write(json.dumps(fact, default=str) + "\n")
            tmp = fh.name
        findings, _ = run_pipeline([tmp])
        return [f.to_dict() for f in findings]
    except Exception as exc:  # noqa: BLE001
        logger.warning("detection_engine.run_failed", error=str(exc))
        return []
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def _apply_regression_reopen(finding, run_id, now) -> None:
    """A previously-remediated finding whose issue reappeared this run: reopen
    the SAME row and flag it as a regression (history preserved)."""
    finding.status = FindingStatus.open
    finding.reopened_count = (finding.reopened_count or 0) + 1
    finding.resolution_miss_count = 0
    finding.resolved_at = None
    finding.resolution_method = None
    finding.resolution_run_id = None
    finding.last_seen = now
    finding.detection_run_id = run_id
    ev = dict(finding.evidence or {})
    ev["regression"] = True
    finding.evidence = ev


async def _find_remediated_match(db, engagement_id, asset_id, title):
    """A remediated finding with the same (engagement, asset, title) — the
    regression candidate. Mirrors _find_open_duplicate but for the closed set."""
    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status == FindingStatus.remediated,
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()


async def _stamp_verification(findings, llm=None) -> None:
    """Best-effort: compute + stamp each finding's verification verdict. A failure
    on one finding must not sink the batch or the detection run."""
    for f in findings:
        try:
            verdict = await run_verification(f.evidence or {}, llm=llm)
            f.verification_state = verdict.state
            f.verification_confidence = verdict.confidence
            f.verification_rationale = verdict.rationale
            f.needs_review = verdict.needs_review
            f.verification_method = verdict.method
        except Exception as exc:  # noqa: BLE001 — verification must never break the run
            logger.warning("verification.stamp_failed", error=str(exc))


async def _engagement_device_roles(db: AsyncSession, engagement_id: uuid.UUID) -> dict[str, dict]:
    """ip → {device_role, role_detail} from already-promoted assets, so a prior
    device_inventory scan amplifies today's correlation (Track B2)."""
    rows = (await db.execute(
        select(Asset.ip_address, Asset.device_role, Asset.role_detail).where(
            Asset.engagement_id == engagement_id,
            Asset.device_role.isnot(None),
        )
    )).all()
    return {
        ip: {"device_role": role, "role_detail": detail}
        for ip, role, detail in rows if ip
    }


async def _persist_attack_paths(
    db: AsyncSession, engagement_id: uuid.UUID, run, facts: list[dict], now,
) -> int:
    """Correlate composite attack paths from the run's facts and persist them as
    Finding rows (deduped by title, reaffirmed across runs). Returns NEW count."""
    device_roles = await _engagement_device_roles(db, engagement_id)
    created = 0
    for d in attack_path_findings(facts, device_roles):
        try:
            asset = await _resolve_asset(db, engagement_id, d.get("target"))
            asset_id = asset.id if asset else None
            title = d["title"][:500]
            evidence = {
                "rule_id": d["rule_id"], "correlation": True,
                "remediation": d.get("remediation"),
                "mitre_techniques": d.get("mitre_techniques"),
                **(d.get("evidence") or {}),
            }
            dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
            if dup is not None:
                dup.severity = d["severity"]     # re-amplify if the role changed
                dup.evidence = evidence
                dup.last_seen = now
                dup.detection_run_id = run.id
                dup.resolution_miss_count = 0
                continue
            db.add(Finding(
                engagement_id=engagement_id,
                asset_id=asset_id,
                title=title,
                description=d.get("description"),
                severity=d["severity"],
                status=FindingStatus.open,
                detection_status=DetectionStatus.detected,
                mitre_techniques=d.get("mitre_techniques"),
                remediation=d.get("remediation"),
                evidence=evidence,
                first_seen=now,
                last_seen=now,
                detection_run_id=run.id,
            ))
            created += 1
        except Exception as exc:  # noqa: BLE001 — one composite must not sink the batch
            logger.warning("attack_path.create_failed", rule_id=d.get("rule_id"), error=str(exc))
    await db.flush()
    return created


async def create_findings_from_facts(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
    *, scan_result_id: uuid.UUID | None = None, trigger: str = TRIGGER_FACTS_READY,
) -> int:
    """New raw-facts path: detect CVE findings from result['facts'] and persist
    them as Finding rows, wrapped in a DetectionRun so the outcome is a temporal
    record (new vs reaffirmed, against a stamped vuln-DB version). Returns the
    count of NEW rows (reaffirmed ones don't count). Best-effort per finding."""
    facts = result.get("facts")
    if not isinstance(facts, list) or not facts:
        return 0

    now = datetime.now(timezone.utc)
    db_version, db_fetched = _vuln_db_meta()

    # Open the run first, so every finding created below can reference run.id and
    # the run row is the single provenance record for this detection execution.
    run = DetectionRun(
        engagement_id=engagement_id,
        scan_result_id=scan_result_id,
        trigger=trigger,
        vuln_db_version=db_version,
        vuln_db_fetched_at=db_fetched,
        started_at=now,
        facts_count=len(facts),
    )
    db.add(run)
    await db.flush()   # assigns run.id

    created = 0
    reaffirmed = 0
    try:
        touched: list = []
        for d in detect_findings_from_facts(facts):
            try:
                cve = d.get("cve_id") or "finding"
                title = f"{cve} — {d.get('cpe', '').split(':')[4] if d.get('cpe') else ''}".strip(" —")[:500]
                asset = await _resolve_asset(db, engagement_id, d.get("asset_ip"))
                asset_id = asset.id if asset else None

                dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
                if dup is not None:
                    # Same issue still present → reaffirm: advance last_seen and
                    # point it at this run (first_seen is preserved).
                    dup.evidence = d
                    dup.last_seen = now
                    dup.detection_run_id = run.id
                    dup.resolution_miss_count = 0   # re-observed → out of the resolution window
                    touched.append(dup)
                    reaffirmed += 1
                    continue

                regressed = await _find_remediated_match(db, engagement_id, asset_id, title)
                if regressed is not None:
                    # An auto/manually-resolved issue is back → reopen the SAME row
                    # and flag the regression (its history is preserved).
                    _apply_regression_reopen(regressed, run.id, now)
                    regressed.evidence = {**(regressed.evidence or {}), **d, "regression": True}
                    touched.append(regressed)
                    reaffirmed += 1
                    continue

                state = d.get("state")
                new_finding = Finding(
                    engagement_id=engagement_id,
                    asset_id=asset_id,
                    cve_ids=[cve] if d.get("cve_id") else None,
                    title=title,
                    description="; ".join(d.get("notes") or []) or None,
                    cvss_score=Decimal(str(d["cvss_score"])) if d.get("cvss_score") is not None else None,
                    cvss_vector=d.get("cvss_vector"),
                    epss_score=Decimal(str(d["epss_score"])) if d.get("epss_score") is not None else None,
                    severity=_PRIORITY_TO_SEVERITY.get(d.get("priority"), FindingSeverity.info),
                    status=FindingStatus.confirmed if state == "confirmed" else FindingStatus.open,
                    detection_status=DetectionStatus.detected,
                    evidence=d,
                    first_seen=now,
                    last_seen=now,
                    detection_run_id=run.id,
                    detected_db_version=db_version,
                )
                db.add(new_finding)
                touched.append(new_finding)
                created += 1
            except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
                logger.warning("detection_finding.create_failed", error=str(exc))

        await db.flush()

        # ── Composite attack-path correlation (Track B) ──────────────────────
        # The CVE loop above scores single facts; this pass chains weaknesses on
        # one host into the attack PATH an operator must fix first (NTLM relay,
        # legacy-Windows surface, cleartext cluster, exposed-DB+unauth, default
        # SNMP on infra), amplified by the host's device role. Best-effort.
        try:
            corr_new = await _persist_attack_paths(db, engagement_id, run, facts, now)
            created += corr_new
        except Exception as exc:  # noqa: BLE001 — correlation must not sink the run
            logger.warning("detection_run.correlation_failed", error=str(exc))

        # Coverage ledger + coverage-gated auto-resolution (Phase 0/1). Best-effort:
        # never let resolution failure sink an otherwise-good detection run.
        resolved = 0
        try:
            coverage = build_coverage(result.get("scanner_runs"), facts)
            resolved = await evaluate_resolutions(db, engagement_id, run, coverage, now)
            run.stats = {"coverage": coverage, "auto_resolved": resolved}
        except Exception as exc:  # noqa: BLE001 — resolution must not fail the run
            logger.warning("detection_run.resolution_failed", error=str(exc))
            run.stats = {"coverage": {}, "auto_resolved": 0}

        # Passive verification (P2): stamp a normalized verdict on findings touched
        # this run. Flagged + best-effort; never breaks the run.
        if get_settings().verification_enabled:
            try:
                await _stamp_verification(touched)
                await db.flush()
            except Exception as exc:  # noqa: BLE001 — verification must not fail the run
                logger.warning("detection_run.verification_failed", error=str(exc))

        # Snapshot the live risk set AFTER resolution (auto-resolved findings drop out).
        current = (await db.execute(
            select(func.count()).select_from(Finding).where(
                Finding.engagement_id == engagement_id,
                Finding.status.in_(_CURRENT_STATUSES),
            )
        )).scalar_one()

        run.status = RUN_COMPLETED
        run.finished_at = datetime.now(timezone.utc)
        run.findings_new = created
        run.findings_reaffirmed = reaffirmed
        run.findings_current = int(current or 0)
        await db.flush()
        logger.info("detection_run.completed", run_id=str(run.id),
                    engagement_id=str(engagement_id), new=created,
                    reaffirmed=reaffirmed, resolved=resolved,
                    current=run.findings_current)
    except Exception as exc:  # noqa: BLE001 — record the failure on the run, don't lose it
        run.status = RUN_FAILED
        run.finished_at = datetime.now(timezone.utc)
        run.error = f"{type(exc).__name__}: {exc}"[:2000]
        await db.flush()
        logger.error("detection_run.failed", run_id=str(run.id), error=str(exc))

    return created


async def run_detection_job(engagement_id: uuid.UUID, result: dict) -> None:
    """Background entry point (P1: keep detection OFF the probe-result request
    path). Runs the full detection_engine pipeline on the facts payload in its
    OWN DB session — a FastAPI BackgroundTask executes AFTER the response, by
    which point the request's session is closed. Mirrors the codebase's
    existing BackgroundTasks pattern (vuln_scans/_run_nuclei_and_save).
    Self-contained and best-effort: never raises into the task runner.
    """
    from app.database import AsyncSessionLocal
    try:
        async with AsyncSessionLocal() as db:
            n = await create_findings_from_facts(db, engagement_id, result)
            await db.commit()
        logger.info("detection.background.done", engagement_id=str(engagement_id), findings=n)
    except Exception as exc:  # noqa: BLE001
        logger.warning("detection.background.failed", engagement_id=str(engagement_id), error=str(exc))
