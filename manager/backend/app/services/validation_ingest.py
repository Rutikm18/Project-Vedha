"""
validation_ingest.py — turn a probe's safe active-validation result into a
finding verdict (P3 Task 7).

The pure transition (`apply_validation_outcome`) mutates a finding object per the
P2/P3 invariants: **confirmation is the only path to raise certainty**
(→ verification_state=confirmed, exploit_validated=True, status=confirmed),
contradiction marks a false-positive signal, and inconclusive leaves the finding
unchanged (never downgrades). `ingest_validation_result` is the DB glue, wired
into the existing job-result submit path — best-effort, so a validation hiccup
never breaks normal scan ingestion.
"""
from __future__ import annotations

import uuid

import structlog
from sqlalchemy import select

from app.detection.active_validation import ValidationOutcome, interpret_validation
from app.models.enums import FindingStatus
from app.models.finding import Finding
from app.models.validation_request import ValidationRequest

logger = structlog.get_logger()

_VALIDATION_OUTCOMES = ("confirmed", "contradicted", "inconclusive")
# A validation result never downgrades a finding that a human has already closed.
_TERMINAL = (FindingStatus.remediated, FindingStatus.accepted, FindingStatus.fp)


def apply_validation_outcome(finding, outcome: ValidationOutcome) -> None:
    """Apply a validation verdict to a finding object (pure — no DB/session)."""
    if outcome.outcome == "confirmed":
        finding.verification_state = "confirmed"
        finding.exploit_validated = True
        if finding.status not in _TERMINAL:
            finding.status = FindingStatus.confirmed
    elif outcome.outcome == "contradicted":
        finding.verification_state = "contradicted"
    # inconclusive → unchanged (never lowers below current state)


def looks_like_validation_result(result) -> bool:
    """Cheap gate so normal scan submissions never trigger a lookup: a probe
    validate payload carries a top-level outcome of confirmed/contradicted/
    inconclusive, whereas a scan result's outcome is ok/partial/error."""
    return isinstance(result, dict) and result.get("outcome") in _VALIDATION_OUTCOMES


async def ingest_validation_result(db, job_id: uuid.UUID, result: dict) -> bool:
    """If ``job_id`` belongs to a ValidationRequest, store the result, set its
    outcome, and apply the verdict to the finding. Returns False (no-op) when
    this is not a validation job."""
    if not looks_like_validation_result(result):
        return False
    vr = (await db.execute(
        select(ValidationRequest).where(ValidationRequest.job_id == job_id)
    )).scalar_one_or_none()
    if vr is None:
        return False

    outcome = interpret_validation(result)
    vr.result = result
    vr.outcome = outcome.outcome

    if vr.finding_id is not None:
        finding = (await db.execute(
            select(Finding).where(Finding.id == vr.finding_id)
        )).scalar_one_or_none()
        if finding is not None:
            apply_validation_outcome(finding, outcome)

    await db.flush()
    logger.info("validation.result.ingested", request_id=str(vr.id),
                job_id=str(job_id), outcome=outcome.outcome)
    return True
