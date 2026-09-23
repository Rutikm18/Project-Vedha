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


def sanitize_jsonb(obj):
    """Recursively strip NUL (U+0000) from every string in a result payload.

    Defense-in-depth at the persistence boundary: scan banners (SSH/HTTP) can
    carry raw NUL bytes, and PostgreSQL ``jsonb`` cannot store ``\\u0000`` — the
    insert then raises DataError and the whole result submission 500s, leaving
    the job stuck in ``running`` forever. The probe scrubs on its side too, but
    the manager must never trust any single probe/version to send clean data.
    Deterministic, so an already-clean payload is a no-op and the idempotency
    checksum stays stable across retries.
    """
    if isinstance(obj, str):
        return obj.replace("\x00", "") if "\x00" in obj else obj
    if isinstance(obj, dict):
        return {sanitize_jsonb(k): sanitize_jsonb(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize_jsonb(v) for v in obj]
    return obj


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


#: Scanners whose fact describes the SCAN RUN rather than a host. Their
#: ``target`` is the local interface that was swept — or the literal string
#: ``"auto"`` when none resolved — so it is not a network identity and must not
#: be scope-checked as one.
#:
#: Without this, a completed job was rejected wholesale with 422
#: (``rejected=[{'path': 'facts[0].target', 'value': 'auto'}]``), discarding every
#: legitimate finding in the payload. The job then sat ``running`` until its lease
#: expired, was requeued, exhausted ``max_attempts`` and failed — which presents
#: to an operator as "stuck in scanning, no results".
#:
#: Mirrors ``agent/engine.py::_RUN_SCOPED_SCANNERS`` on the probe, which already
#: skips these during asset promotion so a phantom asset named "auto" is never
#: invented. Keep the two sets in step.
_RUN_SCOPED_SCANNERS = frozenset({"ipv6_discovery"})


def _result_network_identities(result: dict) -> list[tuple[str, str]]:
    """Return network identities that could create assets or findings.

    Scanner-level control records use targets such as ``<nmap-run>`` to report
    process failures. They describe the scanner itself, not a network target,
    and therefore do not participate in scope authorization. Run-scoped scanner
    facts (see ``_RUN_SCOPED_SCANNERS``) are excluded for the same reason.

    Exclusion here is strictly SAFER than exempting the value later: the record
    contributes no identity at all, so naming a fact ``ipv6_discovery`` cannot
    launder an out-of-scope host into the inventory — it is dropped, not trusted.
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
            # Describes the run, not a host — carries no network identity.
            if item.get("scanner") in _RUN_SCOPED_SCANNERS:
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


def _authorizer(
    scope_cidrs: list[str] | None,
    excluded_cidrs: list[str] | None = None,
):
    """Build the ONE predicate that decides whether an identity is authorized.

    Extracted so validate_result_scope() (which reports) and
    partition_result_scope() (which enforces) cannot drift apart. Two
    implementations of one security rule is how a gate silently opens.

    Fails closed on a missing/malformed scope and on non-IP identities:
    engagement authorization is IP/CIDR-only, so accepting a hostname would let
    Manager DNS resolution disagree with what the probe actually scanned.
    """
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

    def authorized(value: str) -> bool:
        address = _identity_ip(value)
        return bool(
            address is not None
            and any(address.version == net.version and address in net for net in allowed)
            and not any(address.version == net.version and address in net for net in excluded)
        )

    return authorized


def validate_result_scope(
    result: dict,
    scope_cidrs: list[str] | None,
    excluded_cidrs: list[str] | None = None,
) -> list[dict[str, str]]:
    """Return result identities outside the job's authoritative IP scope.

    Detection only — the caller decides what to do about it. Semantics are
    unchanged and pinned by tests/test_run_scoped_fact_scope.py.
    """
    identities = _result_network_identities(result)
    if not identities:
        return []
    authorized = _authorizer(scope_cidrs, excluded_cidrs)
    return [{"path": path, "value": value}
            for path, value in identities if not authorized(value)]


def _drop_orphaned_metrics(result: dict, filtered: dict, dropped_facts: set[int]) -> None:
    """Take a dropped host's coverage metrics with its facts.

    `scan_metrics` is a top-level copy the probe pre-computes from every fact
    whose status is `scan_summary`: that fact's `data`, stamped with the
    fact's own `target` (`agent/engine.py::_scan_metrics_from_facts`), so the
    manager need not filter facts to find them and scan_health_summary() can
    group a host's several summaries (first pass + tail) together. The
    identity traversal never sees `scan_metrics` itself — it walks `facts`,
    and a summary's `data` blob carries `vantage`, not a target — so without
    this a host's metrics row would outlive the evidence the partition
    discarded, and scan_health_summary() would aggregate a host absent from
    the result.

    Matched by VALUE, removing one occurrence per dropped fact, rather than
    re-deriving the list: the manager does not get to recompute a field the
    probe declared, only to remove what it just dropped. The target stamp
    means two hosts that happen to report byte-identical `data` are
    unambiguous to remove — only the dropped host's own entry matches.
    """
    metrics = result.get("scan_metrics")
    facts = result.get("facts")
    if not dropped_facts or not isinstance(metrics, list) or not isinstance(facts, list):
        return
    survivors = list(metrics)
    for index in sorted(dropped_facts):
        fact = facts[index]
        if fact.get("status") != "scan_summary":
            continue
        try:
            # The same construction the probe used when it built
            # scan_metrics: this fact's data, stamped with this fact's target.
            survivors.remove({**fact.get("data", {}), "target": fact.get("target")})
        except ValueError:      # this summary was never surfaced at top level
            continue
    filtered["scan_metrics"] = survivors


def partition_result_scope(
    result: dict,
    scope_cidrs: list[str] | None,
    excluded_cidrs: list[str] | None = None,
) -> tuple[dict, list[dict[str, str]]]:
    """Split a result into (authorized evidence, rejected identities).

    WHY THIS EXISTS. The all-or-nothing gate meant one unparseable row
    discarded an entire scan, permanently — the probe maps 422 to a terminal
    rejection and quarantines the payload. That probability scales with host
    count, so the widest and most expensive scans were the likeliest to lose
    everything.

    THIS IS NOT A WEAKENING. Every rejected identity is still dropped; the same
    rows never reach the database. What changes is that authorized evidence
    beside them stops being collateral damage. The caller still fails closed
    when NOTHING survives.

    An entry that contributes no identity is KEPT, never filtered: run-scoped
    facts (ipv6_discovery), scanner control records, and rows without the key
    are exempt by design, and dropping them would re-create the same data loss
    more quietly.
    """
    rejected = validate_result_scope(result, scope_cidrs, excluded_cidrs)
    if not rejected:
        return result, []

    # Rebuild the identity list the SAME way the detector did, so indices line
    # up with what was judged rather than with a second, re-derived traversal.
    authorized = _authorizer(scope_cidrs, excluded_cidrs)
    drop: dict[str, set[int]] = {}
    for path, value in _result_network_identities(result):
        if authorized(value):
            continue
        collection, _, rest = path.partition("[")
        index, _, _ = rest.partition("]")
        try:
            drop.setdefault(collection, set()).add(int(index))
        except ValueError:                      # unparseable path — never keep it
            drop.setdefault(collection, set())

    filtered = dict(result)
    for collection, indices in drop.items():
        rows = result.get(collection)
        if not isinstance(rows, list):
            continue
        filtered[collection] = [row for i, row in enumerate(rows)
                                if i not in indices]
    _drop_orphaned_metrics(result, filtered, drop.get("facts", set()))
    return filtered, rejected


def surviving_entry_count(result: dict) -> int:
    """How much evidence is left after a partition."""
    return sum(len(result.get(name) or [])
               for name in ("hosts", "facts", "findings"))


def apply_scope_gate(
    result: dict,
    scope_cidrs: list[str] | None,
    excluded_cidrs: list[str] | None = None,
) -> tuple[dict, list[dict[str, str]], dict | None]:
    """Partition a result and decide what to do about it.

    Returns (filtered_result, rejected_identities, refusal). `refusal` is a
    ready-to-return error dict when the whole payload must be refused, else
    None.

    Kept pure and DB-free so the POLICY — which is a security decision — is
    testable without mocking the entire ingest pipeline behind it.
    """
    result, rejected = partition_result_scope(result, scope_cidrs, excluded_cidrs)
    if not rejected:
        return result, [], None

    # FAIL CLOSED when nothing survives. Accepting an empty result would record
    # "we scanned and found nothing", which is a worse lie than a rejection —
    # and it is the pre-existing verdict for a wholly out-of-scope payload,
    # which must not change.
    survivors = surviving_entry_count(result)
    if survivors == 0:
        return result, rejected, {
            "ok": False,
            "error": "Result contains target identities outside the authorized job scope",
            "status_code": 422,
            "permanent_rejection": True,
            "rejected_targets": rejected[:10],
        }

    # Ride along in the payload so the evidence is persisted and a finding can
    # be raised from it (the same route scan_metrics takes).
    result["scope_rejected"] = {
        "count": len(rejected),
        "surviving_entries": survivors,
        "sample": rejected[:10],
    }
    return result, rejected, None


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
    # Defense-in-depth: strip jsonb-hostile NUL bytes before the checksum is
    # computed and before anything is persisted, so a probe that sends a raw
    # banner can never 500 the ingest and hang the job (see sanitize_jsonb).
    result = sanitize_jsonb(result)
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
    # PARTITION, don't reject wholesale. Out-of-scope rows are still dropped —
    # they never reach the database — but authorized evidence beside them is no
    # longer collateral damage. See partition_result_scope() for why this is not
    # a weakening of the control.
    result, rejected_identities, refusal = apply_scope_gate(
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
            surviving_entries=surviving_entry_count(result),
            refused=refusal is not None,
            rejected=rejected_identities[:10],
        )
    if refusal is not None:
        return refusal

    # ── Fold in the per-host evidence this job buffered while it ran ───────
    # Chunks are a buffer, not a second result path: everything downstream still
    # reads ONE scan_results row. This is where hosts finished by an attempt that
    # died (and so never made it into this payload) rejoin the result. Deliberately
    # AFTER the scope check and the idempotency checksum — a rejected or duplicate
    # submission must not drain the buffer, and the checksum has to describe what
    # the probe actually sent.
    from app.services.result_chunk_service import (
        apply_chunks_to_result,
        discard_chunks,
    )
    result = await apply_chunks_to_result(db, job_id, result)

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
        # Distil the probe's per-host completeness/health into one verdict the UI
        # can show as a coverage banner without re-scanning the raw metrics.
        from app.discovery.scan_health import scan_health_summary
        row.result = {
            **lean,
            "fact_count": len(facts),
            "error": error,
            "scan_health": scan_health_summary(result),
        }
    else:
        row.result = {**result, "error": error}

    await db.flush()   # assigns scan_result_row.id (needed for the outbox event)

    # ── Durable detection via transactional outbox ─────────────────────────
    # Enqueue in THIS transaction so the event commits atomically with the facts
    # above. The outbox worker (python -m app.workers.outbox) runs the detection
    # pipeline. This replaces the old asyncio.create_task, which ran in-process
    # and silently dropped work on any crash/restart between the commit and the
    # coroutine executing (no durability, retry, or DLQ).
    #
    # Gated on "did we STORE facts", NOT on `success`. Those are two different
    # questions and coupling detection to the wrong one loses data: a submission
    # that reports ok=false can still carry real facts (the probe sets ok from
    # its successful-fact count, and `success` is a wire field any caller can
    # set), and those facts were persisted just above. Detection never ran on
    # them, nothing logged, and the orphan scan_results row also blocked the
    # campaign's evidence_covered check forever. If it was worth storing, it is
    # worth detecting on. See docs/adr/0001-manager-detection-pipeline.md.
    if scan_result_row is not None:
        from app.models.outbox import TOPIC_FACTS_READY
        from app.workers.outbox import enqueue
        enqueue(
            db, TOPIC_FACTS_READY,
            engagement_id=row.engagement_id,
            scan_result_id=scan_result_row.id,
        )

    # The buffer has landed in scan_results (or there was nothing to land), so
    # drop it. Runs after the flush above: a rolled-back transaction keeps it.
    await discard_chunks(db, job_id)

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

        # ── Network-service weaknesses from banner facts ──────────────────
        # Bridges the gap the package-CVE engine and the probe self-assessment
        # both miss: outdated/weak network services (old SSH, SHA-1/DSA crypto,
        # cleartext protocols) surfaced straight from the service_banner facts.
        try:
            from app.discovery.service_vuln import create_service_vuln_findings
            async with db.begin_nested():
                findings_created += await create_service_vuln_findings(
                    db, row.engagement_id, result,
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning("job.service_vuln_failed", job_id=str(job_id), error=str(exc))

        # ── Prioritize inline findings (fallback) ─────────────────────────
        # The outbox facts_ready handler re-scores once the engine findings land
        # too; this fallback ensures self-assessed / service_vuln findings still
        # get a risk_score even if the worker is down. Idempotent, best-effort.
        try:
            from app.detection.prioritization import prioritize_engagement_findings
            async with db.begin_nested():
                await prioritize_engagement_findings(db, row.engagement_id)
        except Exception as exc:  # noqa: BLE001
            logger.warning("job.prioritize_failed", job_id=str(job_id), error=str(exc))

        # ── Multi-probe vantage fusion (exposure_matrix) ──────────────────
        # A3 stamped this probe's single-vantage verdict; now that a new probe's
        # observations have landed, re-fuse ALL probes so a port any external
        # vantage saw open is corrected to `external`. Best-effort.
        if result.get("scan_type") == "exposure_matrix":
            try:
                from app.detection.exposure_fusion_service import recompute_fused_exposure
                async with db.begin_nested():
                    await recompute_fused_exposure(db, row.engagement_id)
            except Exception as exc:  # noqa: BLE001
                logger.warning("job.exposure_fusion_failed", job_id=str(job_id), error=str(exc))

        # ── Scan coverage/health (false-negative guard) ───────────────────
        # The probe's per-host completeness/health metrics say whether this scan
        # can be trusted. Surface a degraded/incomplete scan so a firewall-
        # truncated run is not mistaken for a genuinely clean host.
        try:
            from app.discovery.finding_translator import create_scan_health_finding
            async with db.begin_nested():
                findings_created += await create_scan_health_finding(
                    db, row.engagement_id, result,
                )
        except Exception as exc:  # noqa: BLE001
            logger.warning("job.scan_health_failed", job_id=str(job_id), error=str(exc))

        # ── Scope divergence (authorization-boundary guard) ───────────────
        # A partially-accepted result means the probe reported hosts this
        # engagement did not authorize. Ingesting the rest is right; letting
        # that fact go unseen is not.
        if result.get("scope_rejected"):
            try:
                from app.discovery.finding_translator import (
                    create_scope_rejection_finding,
                )
                async with db.begin_nested():
                    findings_created += await create_scope_rejection_finding(
                        db, row.engagement_id, result,
                    )
            except Exception as exc:  # noqa: BLE001
                logger.warning("job.scope_rejection_finding_failed",
                               job_id=str(job_id), error=str(exc))

    logger.info(
        "job.result_processed",
        agent_id=str(agent_id),
        job_id=str(job_id),
        success=success,
        assets_promoted=promoted,
        findings_created=findings_created,
    )
    summary = {"ok": True, "assets_promoted": promoted,
               "findings_created": findings_created}
    if rejected_identities:
        # Tell the probe what was dropped. It submitted in good faith, and a
        # silent partial acceptance is how a scope divergence stays invisible.
        summary["scope_rejected_count"] = len(rejected_identities)
        summary["rejected_targets"] = rejected_identities[:10]
    return summary


# ── Private helpers ─────────────────────────────────────────────────────────

def _apply_device_profile(asset, prof: dict | None) -> None:
    """Stamp the probe's evidence-based device role onto an Asset (create/update).

    None-safe and non-destructive: a missing profile is a no-op, and an
    unmappable role (unknown/ambiguous → asset_type None) leaves the coarse
    asset_type untouched while still recording the fine-grained role + confidence.
    """
    if not prof:
        return
    if prof.get("asset_type"):
        asset.asset_type = prof["asset_type"]
    if prof.get("device_role"):
        asset.device_role = prof["device_role"]
    if prof.get("role_detail"):
        asset.role_detail = prof["role_detail"]
    if prof.get("role_confidence") is not None:
        asset.role_confidence = prof["role_confidence"]


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
    if not hosts:
        return 0
    promoted = 0
    # Evidence-based device roles from the probe's device_inventory use-case,
    # keyed by ip. Empty for every other scan_type — a no-op then.
    from app.discovery.device_profile import device_profiles
    profiles = device_profiles(result)
    # Path-dependent reachability from the exposure_matrix use-case, keyed by
    # (ip, proto, port). Empty for every other scan_type — a no-op then.
    from app.discovery.exposure import service_exposure
    exposure_map = service_exposure(result)
    # One probe result can contain multiple facts for the same host/port
    # (for example an HTTP redirect fact plus a web fingerprint fact). Keep an
    # in-batch cache so repeated ports update one Service object instead of
    # creating two pending inserts that violate uq_service_asset_port_proto.
    service_cache: dict[tuple[uuid.UUID | None, int, str], Service] = {}

    # ── Which of these IPs do we already have? ONE query, not one per host ──
    # This runs inside the submit request, under a FOR UPDATE lock on the job
    # row, so every round trip here is latency the probe waits on: a 1,000-host
    # result used to cost ~11,000 sequential queries and blow the probe's 30s
    # read timeout, which then re-uploaded the whole payload.
    ips = list(dict.fromkeys(h.get("ip") for h in hosts if h.get("ip")))
    if not ips:
        return 0
    known: dict[str, Asset] = {
        a.ip_address: a
        for a in (await db.execute(
            select(Asset).where(
                Asset.engagement_id == engagement_id,
                Asset.ip_address.in_(ips),
            )
        )).scalars().all()
    }
    assets_by_ip: dict[str, Asset] = {}

    for h in hosts:
        ip = h.get("ip")
        if not ip:
            continue

        asset = known.get(ip)

        prof = profiles.get(ip)
        if asset:
            asset.hostname = h.get("hostname") or asset.hostname
            asset.os = h.get("os") or asset.os
            asset.last_seen = datetime.now(timezone.utc)
            _apply_device_profile(asset, prof)
        else:
            asset = Asset(
                engagement_id=engagement_id,
                ip_address=ip,
                hostname=h.get("hostname"),
                os=h.get("os"),
                # Use the classified role when the probe evidenced one, else the
                # historical default. Never downgrade a known role to a guess.
                asset_type=(prof["asset_type"] if prof and prof["asset_type"] else AssetType.server),
                last_seen=datetime.now(timezone.utc),
            )
            _apply_device_profile(asset, prof)
            db.add(asset)
            # A payload can name the same IP twice; reuse the pending object
            # rather than inserting it again.
            known[ip] = asset
            promoted += 1
        assets_by_ip[ip] = asset

    # ONE flush assigns every new asset its id (services below need them), and
    # ONE query fetches the services those assets already have.
    if promoted:
        await db.flush()
    asset_ids = [a.id for a in assets_by_ip.values() if a.id is not None]
    if asset_ids:
        for svc_row in (await db.execute(
            select(Service).where(Service.asset_id.in_(asset_ids))
        )).scalars().all():
            service_cache[(svc_row.asset_id, svc_row.port,
                           svc_row.protocol)] = svc_row

    for h in hosts:
        ip = h.get("ip")
        if not ip:
            continue
        asset = assets_by_ip[ip]

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

            # The cache was pre-loaded with every service these assets already
            # have, so a miss means "new service" — no per-port lookup.
            svc = service_cache.get(key)
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
            svc.exposure = exposure_map.get((ip, proto, port_no)) or svc.exposure
            extra = p.get("extra_info") or p.get("data")
            if isinstance(extra, dict):
                svc.extra_info = {**(svc.extra_info or {}), **extra}

    await db.flush()
    return promoted
