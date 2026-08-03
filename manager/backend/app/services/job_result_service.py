"""
job_result_service.py — shared job result processing.
Single source of truth for what happens when a probe submits scan results.
Both the HTTP router (agents.py) and WebSocket handler (agent_ws.py) call
process_job_result().  No more copy-paste.
"""
from __future__ import annotations

import ipaddress
import hashlib
import json
import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import AssetType, ScanJobStatus
from app.models.scan_job import ScanJob
from app.models.scan_job_attempt import ScanJobAttempt
from app.models.scan_result import ScanResult
from app.models.service import Service

logger = structlog.get_logger()


def result_checksum(success: bool, result: dict, error: str | None) -> str:
    """Stable idempotency checksum for one attempt completion payload."""
    canonical = json.dumps(
        {"success": success, "result": result, "error": error},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _result_network_identities(result: dict) -> list[tuple[str, str]]:
    """Return network identities that could create assets or findings.

    Scanner-level control records use targets such as ``<nmap-run>`` to report
    process failures. They describe the scanner itself, not a network target,
    and therefore do not participate in scope authorization.
    """
    identities: list[tuple[str, str]] = []
    collections = (
        ("hosts", "ip"),
        ("facts", "target"),
        ("findings", "target"),
    )
    for collection_name, key in collections:
        collection = result.get(collection_name)
        if not isinstance(collection, list):
            continue
        for index, item in enumerate(collection):
            if not isinstance(item, dict):
                continue
            raw = item.get(key)
            if not isinstance(raw, str) or not raw.strip():
                continue
            value = raw.strip()
            if value.startswith("<") and value.endswith(">"):
                continue
            identities.append((f"{collection_name}[{index}].{key}", value))
    return identities


def _identity_ip(value: str):
    """Parse a probe identity as an IP, tolerating common host:port notation."""
    candidate = value.strip()
    if candidate.startswith("[") and "]:" in candidate:
        candidate = candidate[1:candidate.index("]")]
    elif candidate.count(":") == 1:
        host, port = candidate.rsplit(":", 1)
        if port.isdigit():
            candidate = host
    try:
        return ipaddress.ip_address(candidate)
    except ValueError:
        return None


def validate_result_scope(
    result: dict,
    scope_cidrs: list[str] | None,
    excluded_cidrs: list[str] | None = None,
) -> list[dict[str, str]]:
    """Return result identities outside the job's authoritative IP scope.

    Fail closed on a missing/malformed scope and on non-IP target identities.
    Engagement authorization is IP/CIDR-only, so accepting a hostname here
    would allow Manager DNS resolution to disagree with what the probe scanned.
    """
    identities = _result_network_identities(result)
    if not identities:
        return []

    try:
        allowed = [
            ipaddress.ip_network(str(value).strip(), strict=False)
            for value in (scope_cidrs or [])
        ]
        excluded = [
            ipaddress.ip_network(str(value).strip(), strict=False)
            for value in (excluded_cidrs or [])
        ]
    except (TypeError, ValueError):
        allowed = []
        excluded = []

    rejected: list[dict[str, str]] = []
    for path, value in identities:
        address = _identity_ip(value)
        authorized = bool(
            address is not None
            and any(address.version == net.version and address in net for net in allowed)
            and not any(address.version == net.version and address in net for net in excluded)
        )
        if not authorized:
            rejected.append({"path": path, "value": value})
    return rejected


async def process_job_result(
    db: AsyncSession,
    agent_id: uuid.UUID,
    job_id: uuid.UUID,
    success: bool,
    result: dict | None,
    error: str | None,
    attempt_id: uuid.UUID | None = None,
    fence: int | None = None,
) -> dict:
    """Process a scan job result.  Called from both HTTP and WebSocket paths.

    Returns {"ok": True, "assets_promoted": int, "findings_created": int}.
    """
    row = (await db.execute(
        select(ScanJob).where(
            ScanJob.id == job_id,
            ScanJob.agent_id == str(agent_id),
        ).with_for_update()
    )).scalar_one_or_none()

    if not row:
        return {"ok": False, "error": "Job not found or not assigned to this agent"}

    result = result or {}
    checksum = result_checksum(success, result, error)
    if attempt_id is None or fence is None:
        return {
            "ok": False,
            "error": "attempt_id and fence are required",
            "status_code": 422,
            "permanent_rejection": True,
        }

    # A stale attempt receives a terminal receipt so its durable spool can stop
    # retrying, but it can never mutate the logical job or promote evidence.
    if (
        getattr(row, "current_attempt_id", None) != attempt_id
        or getattr(row, "current_fence", None) != fence
    ):
        logger.warning(
            "job.result_stale_fence",
            job_id=str(job_id),
            agent_id=str(agent_id),
            attempt_id=str(attempt_id),
            fence=fence,
        )
        return {"ok": True, "accepted": False, "stale": True,
                "assets_promoted": 0, "findings_created": 0}

    attempt = (await db.execute(
        select(ScanJobAttempt).where(
            ScanJobAttempt.id == attempt_id,
            ScanJobAttempt.job_id == job_id,
            ScanJobAttempt.agent_id == agent_id,
            ScanJobAttempt.fence == fence,
        ).with_for_update()
    )).scalar_one_or_none()
    if attempt is None:
        return {"ok": True, "accepted": False, "stale": True,
                "assets_promoted": 0, "findings_created": 0}

    # ── Idempotency: result submission is at-least-once ─────────────────────
    # A probe retries when it doesn't see an ACK (the ACK can be lost even after
    # we committed). Without this guard a retry appends a duplicate scan_results
    # row and re-enqueues the detection pipeline → duplicate findings. If this
    # job already reached a terminal state, treat the resubmission as a no-op
    # and return HTTP 200 so the probe clears its spool. Failed submissions are
    # retried after a lost ACK just like successful ones.
    if attempt.status in ("succeeded", "failed"):
        if attempt.result_checksum != checksum:
            logger.warning(
                "job.result_checksum_conflict",
                job_id=str(job_id),
                attempt_id=str(attempt_id),
            )
            return {
                "ok": False,
                "error": "Attempt already completed with a different result checksum",
                "status_code": 409,
                "permanent_rejection": True,
            }
        logger.info(
            "job.result_duplicate_ignored",
            job_id=str(job_id),
            agent_id=str(agent_id),
            terminal_status=attempt.status,
        )
        return {"ok": True, "duplicate": True,
                "assets_promoted": 0, "findings_created": 0}

    job_params = row.result if isinstance(row.result, dict) else {}
    rejected_identities = validate_result_scope(
        result,
        job_params.get("_scope_cidrs") or job_params.get("scope_cidrs"),
        job_params.get("_excluded_cidrs") or job_params.get("excluded_cidrs"),
    )
    if rejected_identities:
        logger.warning(
            "job.result_scope_rejected",
            agent_id=str(agent_id),
            job_id=str(job_id),
            rejected_count=len(rejected_identities),
            rejected=rejected_identities[:10],
        )
        return {
            "ok": False,
            "error": "Result contains target identities outside the authorized job scope",
            "status_code": 422,
            "permanent_rejection": True,
            "rejected_targets": rejected_identities[:10],
        }

    # ── Update job status ──────────────────────────────────────────────────
    row.status = ScanJobStatus.completed if success else ScanJobStatus.failed
    row.completed_at = datetime.now(timezone.utc)
    row.lease_expires_at = None
    attempt.status = "succeeded" if success else "failed"
    attempt.ended_at = row.completed_at
    attempt.result_checksum = checksum
    attempt.error = error

    facts = result.get("facts") if isinstance(result, dict) else None

    # ── Persist raw facts to the append-only scan_results table ─────────────
    scan_result_row: ScanResult | None = None
    if isinstance(facts, list) and facts:
        scan_result_row = ScanResult(
            engagement_id=row.engagement_id,
            job_id=row.id,
            attempt_id=attempt_id,
            agent_id=agent_id,
            content_checksum=checksum,
            validation_state="accepted",
            scan_type=result.get("scan_type"),
            fact_count=len(facts),
            facts=facts,
        )
        db.add(scan_result_row)
        lean = {k: v for k, v in result.items() if k != "facts"}
        row.result = {**lean, "fact_count": len(facts), "error": error}
    else:
        row.result = {**result, "error": error}

    await db.flush()   # assigns scan_result_row.id (needed for the outbox event)

    # ── Promote discovered hosts ───────────────────────────────────────────
    promoted = 0
    findings_created = 0
    if success and isinstance(result, dict):
        if result.get("hosts"):
            try:
                async with db.begin_nested():
                    promoted = await _promote_assets(db, row.engagement_id, result)
            except Exception as exc:  # noqa: BLE001 — best-effort, never fail the submit
                logger.warning("job.promote_failed", job_id=str(job_id), error=str(exc))

        # ── Self-assessed findings (tls_scan, smb_enum, etc.) ─────────────
        try:
            from app.discovery.finding_translator import create_findings_from_probe_result
            async with db.begin_nested():
                findings_created = await create_findings_from_probe_result(
                    db, row.engagement_id, result,
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning("job.findings_failed", job_id=str(job_id), error=str(exc))

        # ── Durable detection via transactional outbox ─────────────────────
        # Enqueue in THIS transaction so the event commits atomically with the
        # facts above. The outbox worker (python -m app.workers.outbox) runs the
        # detection pipeline. This replaces the old asyncio.create_task, which
        # ran in-process and silently dropped work on any crash/restart between
        # the commit and the coroutine executing (no durability, retry, or DLQ).
        if scan_result_row is not None:
            from app.models.outbox import TOPIC_FACTS_READY
            from app.workers.outbox import enqueue
            enqueue(
                db, TOPIC_FACTS_READY,
                engagement_id=row.engagement_id,
                scan_result_id=scan_result_row.id,
            )

    logger.info(
        "job.result_processed",
        agent_id=str(agent_id),
        job_id=str(job_id),
        success=success,
        assets_promoted=promoted,
        findings_created=findings_created,
    )
    return {"ok": True, "assets_promoted": promoted, "findings_created": findings_created}


# ── Private helpers ─────────────────────────────────────────────────────────

async def _promote_assets(
    db: AsyncSession,
    engagement_id: uuid.UUID,
    result: dict,
) -> int:
    """Upsert discovered hosts/services into the asset inventory.

    Keyed by (engagement_id, ip) for assets and (asset, port, protocol) for
    services, so repeated scans update in place instead of duplicating.
    Returns the number of newly-created assets.
    """
    hosts = (result or {}).get("hosts") or []
    promoted = 0
    # One probe result can contain multiple facts for the same host/port
    # (for example an HTTP redirect fact plus a web fingerprint fact). Keep an
    # in-batch cache so repeated ports update one Service object instead of
    # creating two pending inserts that violate uq_service_asset_port_proto.
    service_cache: dict[tuple[uuid.UUID | None, int, str], Service] = {}

    for h in hosts:
        ip = h.get("ip")
        if not ip:
            continue

        asset = (await db.execute(
            select(Asset).where(
                Asset.engagement_id == engagement_id,
                Asset.ip_address == ip,
            )
        )).scalar_one_or_none()

        if asset:
            asset.hostname = h.get("hostname") or asset.hostname
            asset.os = h.get("os") or asset.os
            asset.last_seen = datetime.now(timezone.utc)
        else:
            asset = Asset(
                engagement_id=engagement_id,
                ip_address=ip,
                hostname=h.get("hostname"),
                os=h.get("os"),
                asset_type=AssetType.server,
                last_seen=datetime.now(timezone.utc),
            )
            db.add(asset)
            await db.flush()
            promoted += 1

        # Upsert services
        for p in h.get("ports") or []:
            port_no = p.get("port")
            if port_no is None:
                continue
            try:
                port_no = int(port_no)
            except (TypeError, ValueError):
                continue

            proto = str(p.get("protocol") or "tcp").lower()
            cpe = p.get("cpe")
            cpe_str = ",".join(cpe) if isinstance(cpe, list) else cpe
            key = (asset.id, port_no, proto)

            svc = service_cache.get(key)
            if svc is None:
                svc = (await db.execute(
                    select(Service).where(
                        Service.asset_id == asset.id,
                        Service.port == port_no,
                        Service.protocol == proto,
                    )
                )).scalar_one_or_none()

                if svc is None:
                    svc = Service(
                        asset_id=asset.id,
                        port=port_no,
                        protocol=proto,
                    )
                    db.add(svc)
                service_cache[key] = svc

            svc.service_name = p.get("service") or svc.service_name
            svc.product = p.get("product") or svc.product
            svc.version = p.get("version") or svc.version
            svc.cpe = cpe_str or svc.cpe
            svc.banner = p.get("banner") or svc.banner
            extra = p.get("extra_info") or p.get("data")
            if isinstance(extra, dict):
                svc.extra_info = {**(svc.extra_info or {}), **extra}
        await db.flush()

    return promoted
