"""Per-host evidence committed while a job is still running.

See app/models/scan_result_chunk.py for why this exists. This module owns the
rules around it, which are deliberately the SAME rules the final result path
enforces (app/services/job_result_service.py):

  * a superseded attempt cannot write evidence (fencing);
  * a chunk naming a host outside the job's authorized scope is refused
    permanently, never quarantined silently;
  * delivery is at-least-once, so re-sending an identical chunk is a no-op.
"""
from __future__ import annotations

import hashlib
import json
import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import ScanJobStatus
from app.models.scan_job import ScanJob
from app.models.scan_result_chunk import ScanResultChunk
from app.services.job_result_service import sanitize_jsonb, validate_result_scope

logger = structlog.get_logger()

# A job in one of these states will never produce another fact.
_TERMINAL = (ScanJobStatus.completed, ScanJobStatus.failed, ScanJobStatus.cancelled)


def chunk_checksum(host: str, facts: list) -> str:
    """Stable identity for one host's evidence, so an at-least-once redelivery
    of the SAME chunk is recognised instead of overwriting itself."""
    payload = json.dumps({"host": host, "facts": facts}, sort_keys=True,
                         default=str)
    return hashlib.sha256(payload.encode()).hexdigest()


async def process_result_chunk(
    db: AsyncSession,
    agent_id: uuid.UUID,
    job_id: uuid.UUID,
    *,
    attempt_id: uuid.UUID | None,
    fence: int | None,
    host: str,
    facts: list,
    scan_type: str | None = None,
    complete: bool = True,
) -> dict:
    """Commit ONE host's facts for a running job.

    `complete` says whether this is the host's final word. It defaults to
    True so an older probe — which only ever committed finished hosts —
    behaves identically against this manager."""
    if attempt_id is None or fence is None:
        return {"ok": False, "status_code": 422, "permanent_rejection": True,
                "error": "attempt_id and fence are required"}
    if not host or not isinstance(facts, list):
        return {"ok": False, "status_code": 422, "permanent_rejection": True,
                "error": "host and a facts array are required"}

    row = (await db.execute(
        select(ScanJob).where(
            ScanJob.id == job_id,
            ScanJob.agent_id == str(agent_id),
        )
    )).scalar_one_or_none()
    if row is None:
        return {"ok": False, "status_code": 404,
                "error": "Job not found or not assigned to this agent"}

    # A terminal job's evidence is settled; accepting more would mean facts that
    # no scan_results row will ever carry.
    if row.status in _TERMINAL:
        return {"ok": False, "status_code": 409,
                "error": f"job is already {row.status.value if hasattr(row.status, 'value') else row.status}"}

    # Fencing, exactly as the result path: a cancelled or reassigned attempt is
    # answered with a terminal receipt so its sender stops retrying, but it can
    # never write.
    if (getattr(row, "current_attempt_id", None) != attempt_id
            or getattr(row, "current_fence", None) != fence):
        logger.warning("job.chunk_stale_fence", job_id=str(job_id),
                       agent_id=str(agent_id), host=host, fence=fence)
        return {"ok": True, "accepted": False, "stale": True, "stored": False}

    facts = sanitize_jsonb(facts)
    job_params = row.result if isinstance(row.result, dict) else {}
    rejected = validate_result_scope(
        {"facts": facts, "hosts": [{"ip": host}]},
        job_params.get("_scope_cidrs") or job_params.get("scope_cidrs"),
        job_params.get("_excluded_cidrs") or job_params.get("excluded_cidrs"),
    )
    if rejected:
        logger.warning("job.chunk_scope_rejected", job_id=str(job_id),
                       agent_id=str(agent_id), host=host,
                       rejected=rejected[:10])
        return {"ok": False, "status_code": 422, "permanent_rejection": True,
                "error": "Chunk contains target identities outside the authorized job scope",
                "rejected_targets": rejected[:10]}

    checksum = chunk_checksum(host, facts)
    existing = (await db.execute(
        select(ScanResultChunk).where(
            ScanResultChunk.job_id == job_id,
            ScanResultChunk.host == host,
        )
    )).scalar_one_or_none()

    if existing is not None:
        if existing.content_checksum == checksum:
            return {"ok": True, "duplicate": True, "stored": False}
        # A later attempt rescanned this host: its evidence is the fresher one.
        existing.facts = facts
        existing.fact_count = len(facts)
        existing.content_checksum = checksum
        existing.attempt_id = attempt_id
        existing.agent_id = agent_id
        existing.scan_type = scan_type or existing.scan_type
        # Completion only ever moves forward: a later partial commit must
        # not un-finish a host an earlier one already completed.
        existing.complete = bool(existing.complete or complete)
        await db.flush()
        return {"ok": True, "stored": True, "replaced": True}

    db.add(ScanResultChunk(
        engagement_id=row.engagement_id,
        job_id=job_id,
        attempt_id=attempt_id,
        agent_id=agent_id,
        host=host,
        scan_type=scan_type,
        content_checksum=checksum,
        fact_count=len(facts),
        facts=facts,
        complete=complete,
    ))
    await db.flush()
    return {"ok": True, "stored": True}


async def committed_hosts(db: AsyncSession, job_id: uuid.UUID) -> list[str]:
    """Hosts this job has FINISHED — what a retrying probe skips.

    Complete chunks only. Mid-pipeline evidence is committed for durability
    (a probe killed during the port sweep must not lose hours of work), but a
    host that was merely discovered has not been scanned, and skipping it on
    retry would deliver a liveness fact and call the host done.
    """
    rows = (await db.execute(
        select(ScanResultChunk)
        .where(
            ScanResultChunk.job_id == job_id,
            ScanResultChunk.complete.is_(True),
        )
        .order_by(ScanResultChunk.host)
    )).scalars().all()
    return [r.host for r in rows]


# ── draining the buffer ──────────────────────────────────────────────────────
# A chunk exists only until the job's evidence lands in scan_results — either
# because the job completed (merged into its final submission) or because it
# died and the chunks were promoted in its place. Both paths end with the
# buffer discarded, so this table stays small and can never become a second,
# divergent copy of the evidence.

def _hosts_from_chunk_facts(host: str, facts: list) -> dict:
    """A minimal inventory entry for a host only the buffer knows about.

    Mirrors the probe's own promotion rule (agent/engine.py::_hosts_from_facts):
    only affirmative, port-scoped evidence becomes a service. Without this a
    rescued host would land with facts but nothing in the asset inventory.
    """
    ports: dict[tuple[int, str], dict] = {}
    hostname = None
    for fact in facts:
        if not isinstance(fact, dict) or fact.get("error"):
            continue
        if fact.get("status") not in {"open", "observed"}:
            continue
        data = fact.get("data") or {}
        hostname = hostname or data.get("hostname")
        port = fact.get("port")
        if port is None:
            continue
        proto = fact.get("proto") or "tcp"
        key = (int(port), proto)
        if key not in ports:
            ports[key] = {"port": int(port), "protocol": proto,
                          "service": data.get("service") or data.get("first_line")}
    return {"ip": host, "hostname": hostname,
            "ports": [ports[k] for k in sorted(ports)]}


def merge_chunk_facts(payload_facts: list, chunks: list) -> tuple[list, list]:
    """(facts, extra_hosts) after folding in the chunks the payload misses.

    A host present in the final payload WINS: that payload came from the attempt
    that actually finished, so it is at least as fresh, and adding the buffered
    copy as well would double-count the same evidence.
    """
    facts = list(payload_facts or [])
    covered = {f.get("target") for f in facts
               if isinstance(f, dict) and f.get("target")}
    extra_hosts: list[dict] = []
    for chunk in chunks:
        if chunk.host in covered:
            continue
        chunk_facts = list(chunk.facts or [])
        facts.extend(chunk_facts)
        extra_hosts.append(_hosts_from_chunk_facts(chunk.host, chunk_facts))
    return facts, extra_hosts


async def _load_chunks(db: AsyncSession, job_id: uuid.UUID) -> list:
    return list((await db.execute(
        select(ScanResultChunk)
        .where(ScanResultChunk.job_id == job_id)
        .order_by(ScanResultChunk.host)
    )).scalars().all())


async def apply_chunks_to_result(db: AsyncSession, job_id: uuid.UUID,
                                 result: dict) -> dict:
    """Fold this job's buffered hosts into its final result payload."""
    chunks = await _load_chunks(db, job_id)
    if not chunks:
        return result
    facts, extra_hosts = merge_chunk_facts(result.get("facts") or [], chunks)
    if not extra_hosts and len(facts) == len(result.get("facts") or []):
        return result
    merged = dict(result)
    merged["facts"] = facts
    merged["hosts"] = list(result.get("hosts") or []) + extra_hosts
    logger.info("job.chunks_merged", job_id=str(job_id),
                hosts_recovered=len(extra_hosts), facts=len(facts))
    return merged


async def discard_chunks(db: AsyncSession, job_id: uuid.UUID) -> int:
    """Drop the buffer once its evidence lives in scan_results."""
    chunks = await _load_chunks(db, job_id)
    for chunk in chunks:
        await db.delete(chunk)
    return len(chunks)


def _enqueue_facts_ready(db, engagement_id, scan_result) -> None:
    """Detection runs on rescued evidence exactly as it does on a submission."""
    from app.models.outbox import TOPIC_FACTS_READY
    from app.workers.outbox import enqueue
    enqueue(db, TOPIC_FACTS_READY, engagement_id=engagement_id,
            scan_result_id=scan_result.id)


async def promote_chunks_to_result(db: AsyncSession, job) -> int:
    """Rescue a dead job's finished hosts into a scan_results row.

    Called when a job is given up on (attempts exhausted after a lease expiry) —
    the probe never came back, so no final submission is coming. Without this the
    hosts it HAD finished are discarded and the operator sees a failed job that
    scanned nothing, which is what used to happen every time a deep scan was
    OOM-killed.
    """
    from app.models.scan_result import ScanResult

    chunks = await _load_chunks(db, job.id)
    if not chunks:
        return 0

    # If a submission already landed, the evidence is not lost and a second row
    # would be a duplicate detection run.
    existing = (await db.execute(
        select(ScanResult).where(ScanResult.job_id == job.id).limit(1)
    )).scalar_one_or_none()
    if existing is not None:
        await discard_chunks(db, job.id)
        return 0

    facts, hosts = merge_chunk_facts([], chunks)
    scan_type = next((c.scan_type for c in chunks if c.scan_type), None)
    row = ScanResult(
        engagement_id=job.engagement_id,
        job_id=job.id,
        # No attempt owns this row: it is assembled from several attempts'
        # chunks, and scan_results.attempt_id is unique per attempt.
        attempt_id=None,
        agent_id=None,
        content_checksum=chunk_checksum(str(job.id), facts),
        validation_state="accepted",
        scan_type=scan_type,
        fact_count=len(facts),
        facts=facts,
    )
    db.add(row)
    await db.flush()
    _enqueue_facts_ready(db, job.engagement_id, row)

    prior = job.result if isinstance(job.result, dict) else {}
    job.result = {
        **prior,
        "recovered_from_chunks": {"hosts": len(hosts), "facts": len(facts)},
    }
    await discard_chunks(db, job.id)
    logger.warning("job.chunks_promoted", job_id=str(job.id),
                   hosts=len(hosts), facts=len(facts))
    return len(chunks)
