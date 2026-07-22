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
from app.models.finding import Finding
from app.models.detection_run import (
    DetectionRun, RUN_COMPLETED, RUN_FAILED, TRIGGER_FACTS_READY,
)
from app.discovery.finding_translator import _resolve_asset, _find_open_duplicate

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
                    reaffirmed += 1
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
                    first_seen=now,
                    last_seen=now,
                    detection_run_id=run.id,
                ))
                created += 1
            except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
                logger.warning("detection_finding.create_failed", error=str(exc))

        await db.flush()

        # Snapshot the live risk set after this run (the "current" findings).
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
                    reaffirmed=reaffirmed, current=run.findings_current)
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
