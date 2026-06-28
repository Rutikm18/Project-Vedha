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
from decimal import Decimal
from pathlib import Path

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.discovery.finding_translator import _resolve_asset, _find_open_duplicate

logger = structlog.get_logger()

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


async def create_findings_from_facts(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
) -> int:
    """New raw-facts path: detect CVE findings from result['facts'] and persist
    them as Finding rows. Returns the count of NEW rows (dedup-touched ones
    don't count). Best-effort per finding."""
    facts = result.get("facts")
    if not isinstance(facts, list) or not facts:
        return 0

    created = 0
    for d in detect_findings_from_facts(facts):
        try:
            cve = d.get("cve_id") or "finding"
            title = f"{cve} — {d.get('cpe', '').split(':')[4] if d.get('cpe') else ''}".strip(" —")[:500]
            asset = await _resolve_asset(db, engagement_id, d.get("asset_ip"))
            asset_id = asset.id if asset else None

            dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
            if dup is not None:
                dup.evidence = d
                continue

            state = d.get("state")
            db.add(Finding(
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
            ))
            created += 1
        except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
            logger.warning("detection_finding.create_failed", error=str(exc))

    if created:
        await db.flush()
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
