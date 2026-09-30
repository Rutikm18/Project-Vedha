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

SCAN_PROVENANCE_KEY = "scan_provenance"
SCAN_PROVENANCE_RECORDER = "vedha_manager"
SCAN_PROVENANCE_VERSION = 1


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
) -> dict:
    """Return evidence with immutable initial and advancing latest scan context.

    ``previous_evidence`` is separate because several scanner paths replace raw
    evidence on reaffirmation.  Only the prior provenance block is retained;
    stale scanner-specific fields keep their existing replacement semantics.
    Missing identifiers stay explicit ``None`` rather than being inferred.
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
    return out


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
