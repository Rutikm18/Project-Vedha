"""Truthful scan provenance for findings produced outside the detection engine.

Probe-side findings are persisted before the asynchronous detection run exists.
They therefore record the concrete ScanResult first; the outbox worker links the
eventual DetectionRun only after that run has completed.  Manager-only scanners
record their real ScanJob and deliberately leave detection-run fields null.
"""
from __future__ import annotations

import uuid
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.finding import Finding
from app.services.evidence_integrity import (
    CANONICAL_SHA256_BASIS,
    item_content_sha256,
)

SCAN_PROVENANCE_KEY = "scan_provenance"
SCAN_PROVENANCE_RECORDER = "vedha_manager"
SCAN_PROVENANCE_VERSION = 1

CUSTODY_CAPTURED_BY_PROBE = "vedha_probe"
CUSTODY_CAPTURED_BY_MANAGER = SCAN_PROVENANCE_RECORDER


def stamp_chain_of_custody(
    evidence: dict | None,
    *,
    source_host: str | None,
    captured_by: str,
    tool: str | None = None,
    captured_at: datetime | None = None,
) -> dict:
    """Stamp integrity custody (who/where/when + a content digest) onto evidence.

    The digest covers only the OBSERVED content: custody and provenance keys are
    excluded (see ``content_for_integrity``) so advancing the scan_provenance
    block, re-stamping on reaffirmation, or linking a detection run never
    invalidates it. A re-stamp over identical content therefore yields the same
    hash; new scanner content yields a new one, which is the intended signal.

    Content that cannot be canonicalized (non-JSON) leaves no hash behind rather
    than a false one, so the report flags it ``evidence_integrity_hash_absent``.
    """
    out = dict(evidence) if isinstance(evidence, dict) else {}
    out["captured_by"] = captured_by
    if source_host is not None:
        out["source_host"] = source_host
    if tool is not None and not out.get("tool"):
        out["tool"] = tool
    out["captured_at"] = (captured_at or datetime.now(timezone.utc)).isoformat()
    digest = item_content_sha256(out)
    if digest is not None:
        out["sha256"] = digest
        out["sha256_basis"] = CANONICAL_SHA256_BASIS
    else:
        out.pop("sha256", None)
        out.pop("sha256_basis", None)
    return out


def preserve_trusted_scan_provenance(
    evidence: dict | None,
    *,
    previous_evidence: dict | None,
) -> dict:
    """Replace scanner evidence without losing manager-recorded scan identity.

    Scanner payloads are untrusted, so any provenance block in ``evidence`` is
    discarded. A previous block survives only when it carries the exact manager
    recorder and schema-version contract used by this service.
    """
    out = dict(evidence) if isinstance(evidence, dict) else {}
    out.pop(SCAN_PROVENANCE_KEY, None)
    previous = previous_evidence if isinstance(previous_evidence, dict) else {}
    provenance = previous.get(SCAN_PROVENANCE_KEY)
    if (
        isinstance(provenance, dict)
        and provenance.get("recorded_by") == SCAN_PROVENANCE_RECORDER
        and provenance.get("schema_version") == SCAN_PROVENANCE_VERSION
    ):
        out[SCAN_PROVENANCE_KEY] = deepcopy(provenance)
    return out


def record_scan_observation(
    evidence: dict | None,
    *,
    scan_result_id: uuid.UUID | None,
    scan_job_id: uuid.UUID | None,
    scan_type: str | None,
    source: str,
    tool: str | None,
    recorded_at: datetime | None,
    initial: bool,
    previous_evidence: dict | None = None,
    source_host: str | None = None,
    captured_by: str = CUSTODY_CAPTURED_BY_PROBE,
) -> dict:
    """Return evidence with immutable initial and advancing latest scan context.

    ``previous_evidence`` is separate because several scanner paths replace raw
    evidence on reaffirmation.  Only the prior provenance block is retained;
    stale scanner-specific fields keep their existing replacement semantics.
    Missing identifiers stay explicit ``None`` rather than being inferred.

    Chain of custody is stamped last: ``source_host`` (the scanned target) and
    ``captured_by`` (the probe by default — these paths persist probe-submitted
    evidence) plus a content digest, so the engagement report can prove the
    recorded evidence is unchanged instead of flagging its integrity hash absent.
    """
    # Raw scanner evidence is untrusted and may itself contain a provenance
    # key. Reuse the same trust boundary as every evidence-replacement path.
    out = preserve_trusted_scan_provenance(
        evidence,
        previous_evidence=previous_evidence,
    )
    provenance = dict(out.pop(SCAN_PROVENANCE_KEY, {}))
    provenance["recorded_by"] = SCAN_PROVENANCE_RECORDER
    provenance["schema_version"] = SCAN_PROVENANCE_VERSION
    timestamp = recorded_at or datetime.now(timezone.utc)
    observation: dict[str, Any] = {
        "scan_result_id": str(scan_result_id) if scan_result_id is not None else None,
        "scan_job_id": str(scan_job_id) if scan_job_id is not None else None,
        "detection_run_id": None,
        "scan_type": scan_type,
        "source": source,
        "tool": tool,
        "recorded_at": timestamp.isoformat(),
        "timestamp_basis": "manager_recorded",
    }

    if initial and not isinstance(provenance.get("initial"), dict):
        provenance["initial"] = dict(observation)
    provenance["latest"] = dict(observation)
    out[SCAN_PROVENANCE_KEY] = provenance
    return stamp_chain_of_custody(
        out,
        source_host=source_host,
        captured_by=captured_by,
        tool=tool,
        captured_at=timestamp,
    )


async def attach_detection_run_to_scan_findings(
    db: AsyncSession,
    engagement_id: uuid.UUID,
    scan_result_id: uuid.UUID,
    detection_run_id: uuid.UUID,
) -> int:
    """Link a real completed DetectionRun to findings from its exact ScanResult.

    Initial and latest observations are matched independently.  This matters
    when scan B updates a finding before scan A's outbox event is processed: A
    must still become the initial run without overwriting B as the latest scan.
    """
    scan_result_text = str(scan_result_id)
    trusted_marker = {
        "recorded_by": SCAN_PROVENANCE_RECORDER,
        "schema_version": SCAN_PROVENANCE_VERSION,
    }
    initial_match = {
        SCAN_PROVENANCE_KEY: {
            **trusted_marker,
            "initial": {"scan_result_id": scan_result_text},
        }
    }
    latest_match = {
        SCAN_PROVENANCE_KEY: {
            **trusted_marker,
            "latest": {"scan_result_id": scan_result_text},
        }
    }
    rows = (
        (
            await db.execute(
                select(Finding).where(
                    Finding.engagement_id == engagement_id,
                    or_(
                        Finding.evidence.contains(initial_match),
                        Finding.evidence.contains(latest_match),
                    ),
                )
            )
        )
        .scalars()
        .all()
    )

    linked = 0
    run_text = str(detection_run_id)
    for finding in rows:
        evidence = finding.evidence if isinstance(finding.evidence, dict) else {}
        stored = evidence.get(SCAN_PROVENANCE_KEY)
        if (
            not isinstance(stored, dict)
            or stored.get("recorded_by") != SCAN_PROVENANCE_RECORDER
            or stored.get("schema_version") != SCAN_PROVENANCE_VERSION
        ):
            continue
        provenance = dict(stored)
        changed = False

        initial_observation = provenance.get("initial")
        if (
            isinstance(initial_observation, dict)
            and initial_observation.get("scan_result_id") == scan_result_text
            and finding.initial_detection_run_id is None
        ):
            finding.initial_detection_run_id = detection_run_id
            initial_observation = dict(initial_observation)
            initial_observation["detection_run_id"] = run_text
            provenance["initial"] = initial_observation
            changed = True

        latest_observation = provenance.get("latest")
        if (
            isinstance(latest_observation, dict)
            and latest_observation.get("scan_result_id") == scan_result_text
            and (
                finding.detection_run_id != detection_run_id
                or latest_observation.get("detection_run_id") != run_text
            )
        ):
            finding.detection_run_id = detection_run_id
            latest_observation = dict(latest_observation)
            latest_observation["detection_run_id"] = run_text
            provenance["latest"] = latest_observation
            changed = True

        if changed:
            finding.evidence = {**evidence, SCAN_PROVENANCE_KEY: provenance}
            linked += 1

    if linked:
        await db.flush()
    return linked
