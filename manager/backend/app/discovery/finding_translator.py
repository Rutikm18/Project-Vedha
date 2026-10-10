"""
Convert a probe's self-assessed `findings` into persisted Finding rows.

WHY THIS EXISTS: submit_job_result() in routers/agents.py already promotes a
probe's discovered hosts/services into Asset/Service rows via
_promote_assets(), but nothing converted the probe's own severity-tagged
`findings` (tls_scan/smb_enum/mcp_discovery/ai_service_discovery already embed
these directly in their result envelope — see probe/scanners/{tls,smb,mcp_ai}.py)
into dashboard-visible Finding rows. They were silently dropped on arrival,
even though the scanners themselves already computed them. This is the
missing translation step — not a new detection engine, just a bridge.

Deliberately excludes vuln_scan: that scan_type is never agent-dispatched in
practice (see AGENT_EXECUTABLE_TYPES in routers/agents.py) and its nuclei
findings use a different shape (template_id/matched_at/cves) handled by the
existing nessus/nuclei -> run_post_scan_enrichment path instead.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.models.service import Service
from app.services.finding_scan_provenance import record_scan_observation

logger = structlog.get_logger()

# Only these scan_types embed pre-assessed `findings` in their result envelope
# today. The rest (host_discovery, discovery, port_scan, mass_scan,
# service_fingerprint, udp_scan, web_scan) are pure inventory — nothing for
# this translator to do until/unless they grow their own findings list too.
FINDING_PRODUCING_SCAN_TYPES = {"tls_scan", "smb_enum", "mcp_discovery", "ai_service_discovery"}

# A Finding the operator already resolved (remediated/fp) is NOT deduped if the
# same issue reappears on a later scan — that is a real regression signal, not
# noise, and should surface as a fresh finding. Only still-relevant statuses
# suppress a duplicate.
_DEDUP_SUPPRESSING_STATUSES = (FindingStatus.open, FindingStatus.confirmed, FindingStatus.accepted)


def _map_severity(raw: str | None) -> FindingSeverity:
    try:
        return FindingSeverity((raw or "info").lower())
    except ValueError:
        return FindingSeverity.info


class AssetCache(dict):
    """{host: Asset} for one detection run, plus the hosts prime_asset_cache has
    already checked and found absent (so _resolve_asset need not look again)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.known_absent: set[str] = set()


def _host_of(target: str | None) -> str | None:
    """The host part of a probe target ("1.2.3.4" or "1.2.3.4:443"); IPv6 literals
    (several colons) are kept whole. This is the key assets are stored under."""
    if not target:
        return None
    return target.split(":", 1)[0] if target.count(":") == 1 else target


async def prime_asset_cache(db: AsyncSession, engagement_id: uuid.UUID,
                            targets, cache: dict, identity=None) -> int:
    """Fill `cache` with the engagement's existing assets for `targets` in ONE query
    per 1,000 hosts, so _resolve_asset only has to create what is genuinely new
    instead of looking every host up one by one. Returns how many were found.

    Uses the same identity policy as _resolve_asset (find_assets_batch) and the same
    cache keys (host, or (site, host) under per-site identity), so a primed entry is
    exactly the asset a one-by-one lookup would have returned."""
    from app.services.asset_resolution import GLOBAL_IDENTITY, find_assets_batch
    identity = identity or GLOBAL_IDENTITY
    hosts = list(dict.fromkeys(h for h in (_host_of(t) for t in targets) if h))
    found = 0
    for start in range(0, len(hosts), 1000):
        chunk = hosts[start:start + 1000]
        by_host = await find_assets_batch(db, engagement_id, chunk, identity)
        for host, asset in by_host.items():
            scope = identity.scope_for(host)
            cache.setdefault(host if scope is None else (scope, host), asset)
            found += 1
        if isinstance(cache, AssetCache):
            cache.known_absent.update(h for h in chunk if h not in by_host)
    return found


async def _resolve_asset(db: AsyncSession, engagement_id: uuid.UUID, target: str | None,
                         *, cache: dict | None = None, identity=None) -> Asset | None:
    """Find the Asset for a probe-reported target IP, creating a minimal one if needed.

    A probe's tls_scan/smb_enum/etc. can run standalone (no prior discovery job
    promoted this host yet), so the asset may not exist — create a bare-bones
    row rather than dropping the finding for lack of somewhere to attach it.

    Delegates to services/asset_resolution.resolve_asset, the single identity
    policy (global by default; per-site for private IPs when the engagement opts
    in). `identity` is the submission's IdentityContext; None = global. `cache`
    (caller-owned, one run; an AssetCache also knows which hosts were primed and found
    absent) resolves each host once instead of per finding.
    """
    from app.services.asset_resolution import resolve_asset
    return await resolve_asset(db, engagement_id, target, identity=identity, cache=cache)


def _finding_port(f: dict) -> int | None:
    """Best-effort port for a probe finding: explicit `port`, else the ':NNN'
    suffix of `target` (host:port). None when neither is present/parseable."""
    raw = f.get("port")
    if raw is not None:
        try:
            return int(raw)
        except (TypeError, ValueError):
            return None
    target = f.get("target") or ""
    if target.count(":") == 1:
        _host, _sep, port_s = target.partition(":")
        try:
            return int(port_s)
        except ValueError:
            return None
    return None


async def _escalate_by_exposure(
    db: AsyncSession, asset_id: uuid.UUID | None, f: dict, severity: FindingSeverity,
) -> tuple[FindingSeverity, str | None]:
    """Bump severity one rung when the finding's service is internet-reachable
    (Service.exposure == 'external', stamped by a prior exposure_matrix scan).

    Returns (severity, exposure) so the caller can record WHY it escalated.
    Best-effort: any lookup problem leaves the severity unchanged.
    """
    if asset_id is None:
        return severity, None
    port = _finding_port(f)
    if port is None:
        return severity, None
    try:
        svc = (await db.execute(
            select(Service).where(Service.asset_id == asset_id, Service.port == port)
        )).scalars().first()
    except Exception:  # noqa: BLE001 — escalation is advisory, never fatal
        return severity, None
    if svc is None or not svc.exposure:
        return severity, None
    from app.discovery.exposure import escalate_for_exposure
    return escalate_for_exposure(severity, svc.exposure), svc.exposure


# Gap #2 — cross-producer dedup. Several producers (the detection-engine posture
# track, the probe self-assessment, legacy bridges) can each raise a finding for
# the SAME underlying condition on the same (host, port) but with DIFFERENT
# titles, and the dedup key is (asset, title) — so they never merged, giving 3-6
# rows for one service. A producer may therefore stamp a stable, title-independent
# CONDITION key into evidence[_DEDUP_KEY] (e.g. "exposed:23"); dedup then matches
# on (asset, condition) across producers, regardless of title, in addition to the
# (asset, title) match.
DEDUP_KEY = "dedup_key"
_COND = "\x00cond\x00"   # sentinel so a condition key can't collide with a title

# Probe self-assessed finding categories that describe an EXPOSED SERVICE on a
# port (one finding per (asset, port), whatever producer/title). Kept narrow so a
# per-port condition key never merges two genuinely different findings that share
# a port (e.g. weak-crypto vs a web issue on 443).
_EXPOSED_CATEGORIES = {"cleartext_protocol", "exposure", "amplification"}


def _condition_of(evidence) -> str | None:
    if isinstance(evidence, dict):
        v = evidence.get(DEDUP_KEY)
        if isinstance(v, str) and v:
            return v
    return None


def condition_index_key(asset_id, condition: str) -> tuple:
    """The in-memory dedup-index key for a cross-producer condition (gap #2).
    Callers that maintain an index must register a created finding under this key
    (in addition to (asset_id, title)) when it carries a condition."""
    return (asset_id, _COND, condition)


def probe_finding_condition(finding: dict) -> str | None:
    """The cross-producer condition for a probe self-assessed finding, or None —
    only for the exposed-service class, keyed by port (gap #2)."""
    if isinstance(finding, dict) and finding.get("category") in _EXPOSED_CATEGORIES:
        return exposed_service_condition(finding.get("port"), finding.get("proto"))
    return None


async def load_finding_index(
    db: AsyncSession, engagement_id: uuid.UUID, statuses,
) -> dict[tuple, Finding]:
    """{(asset_id, title): Finding} for one engagement, in ONE query — plus a
    (asset_id, _COND, condition) entry for any finding carrying a condition key,
    so cross-producer dedup (gap #2) can look up by condition too.

    Detection asks "have I seen this finding before?" once per finding, which is
    thousands of sequential round trips on a large engagement. This is the same
    caller-owned-cache idiom `_resolve_asset(..., cache=...)` already uses for
    the asset lookups in that loop: load once per run, then look up in memory.

    First row wins per key, matching the `.limit(1)` the per-finding query used.
    """
    rows = (await db.execute(
        select(Finding).where(
            Finding.engagement_id == engagement_id,
            Finding.status.in_(statuses),
        )
    )).scalars().all()
    index: dict[tuple, Finding] = {}
    for row in rows:
        index.setdefault((row.asset_id, row.title), row)
        cond = _condition_of(row.evidence)
        if cond:
            index.setdefault((row.asset_id, _COND, cond), row)
    return index


async def load_open_finding_index(
    db: AsyncSession, engagement_id: uuid.UUID,
) -> dict[tuple[uuid.UUID | None, str], Finding]:
    """The dedup-suppressing set: what `_find_open_duplicate` would match."""
    return await load_finding_index(db, engagement_id,
                                    _DEDUP_SUPPRESSING_STATUSES)


async def _find_open_duplicate(
    db: AsyncSession, engagement_id: uuid.UUID, asset_id: uuid.UUID | None, title: str,
    *, condition: str | None = None, index: dict | None = None,
) -> Finding | None:
    """A still-relevant Finding that is the same issue, if any.

    Matches on the cross-producer CONDITION key first (gap #2) — so a finding
    another producer already raised for the same (asset, condition) is reaffirmed
    instead of duplicated under a different title — then falls back to the classic
    (asset, title) match. `condition` None → title-only (prior behaviour).

    Re-running the same probe scan weekly must not pile up duplicate rows for
    an unchanged issue — but a finding the operator already remediated/marked
    fp is intentionally NOT matched here (see _DEDUP_SUPPRESSING_STATUSES):
    if it reappears on a later scan that's a regression worth a fresh row,
    not noise to suppress.

    `index` (from load_open_finding_index) answers from memory instead of a
    query. A caller that passes one MUST add the findings it creates to it, or
    two findings with the same identity in one run would both be created.
    """
    if index is not None:
        if condition:
            hit = index.get((asset_id, _COND, condition))
            if hit is not None:
                return hit
        return index.get((asset_id, title))

    if condition:
        qc = select(Finding).where(
            Finding.engagement_id == engagement_id,
            Finding.evidence[_DEDUP_KEY].astext == condition,
            Finding.status.in_(_DEDUP_SUPPRESSING_STATUSES),
        )
        qc = qc.where(Finding.asset_id == asset_id) if asset_id else qc.where(Finding.asset_id.is_(None))
        hit = (await db.execute(qc.limit(1))).scalar_one_or_none()
        if hit is not None:
            return hit

    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status.in_(_DEDUP_SUPPRESSING_STATUSES),
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()


def exposed_service_condition(port: int | None, proto: str | None = None) -> str | None:
    """The cross-producer condition key for an exposed-service finding (gap #2):
    one such finding per (asset, port), whatever producer raised it or how it is
    titled. None when there is no port to key on. UDP gets its own `/udp` key so
    UDP/161 and TCP/161 stay two services (spelling shared with the engine's
    `posture_rules.condition_key`, which is the canonical definition)."""
    if not isinstance(port, int):
        return None
    return f"exposed:{port}/udp" if str(proto or "").lower() == "udp" else f"exposed:{port}"


_SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
_MAX_SIGNALS = 12


def stronger_severity(current, incoming):
    """The higher of two FindingSeverity values (merging two signals into one finding
    must never LOWER what the strongest signal said)."""
    cur = _SEVERITY_ORDER.get(getattr(current, "value", current), -1)
    inc = _SEVERITY_ORDER.get(getattr(incoming, "value", incoming), -1)
    return incoming if inc > cur else current


def merge_signals(previous_evidence, *, existing_rule_id=None, existing_title=None,
                  existing_severity=None, existing_run_id=None, incoming: dict | None = None,
                  run_id=None) -> list[dict]:
    """The signals (producer rows) that collapsed into one finding, for the report's
    roll-up: one `{rule_id, title, severity, run_id}` per distinct rule/title, bounded.

    The finding's own first signal is seeded from the stored row so it is not lost when a
    later producer's evidence replaces the evidence body. `run_id` stamps the signals the
    CURRENT run observed; `prune_stale_signals` drops the rest at the end of the run, so a
    producer that stopped matching disappears instead of lingering."""
    prev = previous_evidence if isinstance(previous_evidence, dict) else {}
    signals: list[dict] = [dict(s) for s in (prev.get("signals") or []) if isinstance(s, dict)]
    stamp = str(run_id) if run_id is not None else None

    def _add(rule_id, title, severity, run):
        sev = getattr(severity, "value", severity)
        ident = rule_id or title
        for s in signals:
            if (s.get("rule_id") or s.get("title")) == ident:
                s.update({"title": title, "severity": sev, "run_id": run})
                return
        signals.append({"rule_id": rule_id, "title": title, "severity": sev, "run_id": run})

    if not signals and (existing_rule_id or existing_title):
        _add(existing_rule_id or prev.get("rule_id"), existing_title, existing_severity,
             str(existing_run_id) if existing_run_id is not None else None)
    if incoming:
        _add(incoming.get("rule_id"), incoming.get("title"), incoming.get("severity"), stamp)
    return signals[:_MAX_SIGNALS]


def prune_stale_signals(findings, run_id) -> None:
    """After a run: keep only the signals this run observed. A finding left with a single
    signal is no longer a merge, so its `signals` key is removed. Best-effort and in place."""
    stamp = str(run_id)
    for f in findings:
        ev = f.evidence if isinstance(f.evidence, dict) else None
        if not ev or not ev.get("signals"):
            continue
        fresh = [s for s in ev["signals"] if isinstance(s, dict) and s.get("run_id") == stamp]
        new_ev = {k: v for k, v in ev.items() if k != "signals"}
        if len(fresh) > 1:
            new_ev["signals"] = fresh
        f.evidence = new_ev


async def create_findings_from_probe_result(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
    *,
    scan_result_id: uuid.UUID | None = None,
    scan_job_id: uuid.UUID | None = None,
    recorded_at: datetime | None = None,
    identity=None,
) -> int:
    """Convert a probe's self-assessed `findings` list into persisted Finding rows.

    Best-effort per finding: one bad/malformed entry must never abort the rest
    or fail the probe's result submission (mirrors _promote_assets' philosophy
    in routers/agents.py). Returns the number of NEW Finding rows created
    (re-touching an existing open duplicate does not count).
    """
    scan_type = result.get("scan_type")
    if scan_type not in FINDING_PRODUCING_SCAN_TYPES:
        return 0
    raw_findings = result.get("findings") or []
    if not raw_findings:
        return 0

    now = recorded_at or datetime.now(timezone.utc)
    created = 0
    for f in raw_findings:
        if not isinstance(f, dict):
            continue
        try:
            asset = await _resolve_asset(db, engagement_id, f.get("target"), identity=identity)
            title = (f.get("title") or f"{scan_type} finding")[:500]
            asset_id = asset.id if asset else None
            # gap #2: an exposed-service probe finding carries a per-port condition
            # key so it merges with the posture engine's finding for the same
            # service instead of adding a second, differently-titled row.
            condition = probe_finding_condition(f)

            dup = await _find_open_duplicate(db, engagement_id, asset_id, title,
                                             condition=condition)
            if dup is not None:
                # Still relevant and still present — touch evidence (bumps
                # updated_at) and advance last_seen rather than creating a
                # literal duplicate row. (No detection_run: this is the probe's
                # own self-assessed path, not the detection engine.)
                merged_signals = None
                if condition and dup.title != title:
                    # A different producer for the same condition: the merged finding must not
                    # LOWER what the strongest signal said, and remembers who else reported it.
                    dup.severity = stronger_severity(dup.severity, _map_severity(f.get("severity")))
                    merged_signals = merge_signals(
                        dup.evidence, existing_rule_id=(dup.evidence or {}).get("rule_id"),
                        existing_title=dup.title, existing_severity=dup.severity,
                        incoming={"rule_id": f.get("rule_id"), "title": title,
                                  "severity": f.get("severity")})
                dup.evidence = record_scan_observation(
                    {**f, "scan_type": scan_type, "engine": result.get("engine"),
                     **({DEDUP_KEY: condition} if condition else {})},
                    scan_result_id=scan_result_id,
                    scan_job_id=scan_job_id,
                    scan_type=scan_type,
                    source="probe",
                    tool=result.get("engine") or result.get("scanner"),
                    recorded_at=now,
                    initial=False,
                    previous_evidence=dup.evidence,
                    source_host=f.get("target"),
                )
                if merged_signals:
                    dup.evidence = {**dup.evidence, "signals": merged_signals}
                dup.last_seen = now
                continue

            severity = _map_severity(f.get("severity"))
            severity, exposure = await _escalate_by_exposure(db, asset_id, f, severity)
            evidence = {**f, "scan_type": scan_type, "engine": result.get("engine")}
            if condition:
                evidence[DEDUP_KEY] = condition
            if exposure == "external":
                evidence["exposure_escalated"] = True
                evidence["exposure"] = exposure
            evidence = record_scan_observation(
                evidence,
                scan_result_id=scan_result_id,
                scan_job_id=scan_job_id,
                scan_type=scan_type,
                source="probe",
                tool=result.get("engine") or result.get("scanner"),
                recorded_at=now,
                initial=True,
                source_host=f.get("target"),
            )
            db.add(Finding(
                engagement_id=engagement_id,
                asset_id=asset_id,
                title=title,
                description=f.get("detail"),
                severity=severity,
                status=FindingStatus.open,
                evidence=evidence,
                first_seen=now,
                last_seen=now,
                initial_detection_run_id=None,
                detection_run_id=None,
            ))
            created += 1
        except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
            logger.warning("probe_finding.create_failed", scan_type=scan_type, error=str(exc))

    if created or raw_findings:
        await db.flush()
    return created


_SCOPE_REJECTED_TITLE = "Scan evidence dropped — targets outside authorized scope"


async def create_scope_rejection_finding(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
) -> int:
    """Raise ONE finding when a submission carried out-of-scope identities.

    The manager now ingests the authorized part of a mixed payload instead of
    refusing all of it (see job_result_service.apply_scope_gate). That is the
    right call for the evidence, but it must not make the divergence silent:
    something asked this probe to report a host the engagement did not
    authorize, and a human needs to decide whether that is a misconfigured
    scope, a probe/manager scope-model disagreement, or a probe that should not
    be trusted.

    `medium`, not `low` like scan coverage: this is an authorization-boundary
    event, not a quality one.

    Deduped by title so a chronic divergence refreshes one finding instead of
    piling up. Best-effort — never sinks the result submission.
    """
    rejected = (result or {}).get("scope_rejected")
    if not isinstance(rejected, dict) or not rejected.get("count"):
        return 0
    count = int(rejected["count"])
    samples = ", ".join(
        str(entry.get("value")) for entry in (rejected.get("sample") or [])[:5]
    )
    description = (
        f"{count} target identity(ies) in this scan result fell outside the "
        f"engagement's authorized scope and were dropped before ingest; "
        f"{rejected.get('surviving_entries', 0)} authorized entry(ies) were "
        f"kept. Sample: {samples or 'n/a'}. Confirm the engagement scope and "
        f"the probe's configured segments agree."
    )
    now = datetime.now(timezone.utc)
    try:
        dup = await _find_open_duplicate(db, engagement_id, None, _SCOPE_REJECTED_TITLE)
        evidence = {"scope_rejected": rejected,
                    "scan_type": result.get("scan_type"),
                    "engine": result.get("engine")}
        if dup is not None:
            dup.evidence = evidence
            dup.description = description
            dup.last_seen = now
            return 0
        db.add(Finding(
            engagement_id=engagement_id,
            asset_id=None,
            title=_SCOPE_REJECTED_TITLE,
            description=description,
            severity=FindingSeverity.medium,
            status=FindingStatus.open,
            evidence=evidence,
            first_seen=now,
            last_seen=now,
        ))
        await db.flush()
        return 1
    except Exception as exc:  # noqa: BLE001 — a scope note must not sink the batch
        logger.warning("scope_rejection.finding_failed", error=str(exc))
        return 0


_SCAN_HEALTH_TITLE = "Scan coverage degraded — results may under-report exposure"


async def create_scan_health_finding(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
    *,
    scan_result_id: uuid.UUID | None = None,
    scan_job_id: uuid.UUID | None = None,
    recorded_at: datetime | None = None,
) -> int:
    """Raise ONE engagement-level finding when the probe's own metrics say the
    scan was degraded/incomplete (a false-NEGATIVE risk: real services may have
    gone unseen). Returns 1 if a new finding was created, else 0.

    Deduped by title so a chronically firewalled segment refreshes one finding
    instead of piling up. Best-effort — never sinks the result submission.
    """
    from app.discovery.scan_health import scan_health_summary

    summary = scan_health_summary(result)
    if not summary["should_warn"]:
        return 0
    now = recorded_at or datetime.now(timezone.utc)
    try:
        dup = await _find_open_duplicate(db, engagement_id, None, _SCAN_HEALTH_TITLE)
        evidence = {"scan_health": summary, "scan_type": result.get("scan_type"),
                    "engine": result.get("engine")}
        if dup is not None:
            dup.evidence = record_scan_observation(
                evidence,
                scan_result_id=scan_result_id,
                scan_job_id=scan_job_id,
                scan_type=result.get("scan_type"),
                source="probe",
                tool=result.get("engine") or result.get("scanner"),
                recorded_at=now,
                initial=False,
                previous_evidence=dup.evidence,
            )
            dup.last_seen = now
            return 0
        evidence = record_scan_observation(
            evidence,
            scan_result_id=scan_result_id,
            scan_job_id=scan_job_id,
            scan_type=result.get("scan_type"),
            source="probe",
            tool=result.get("engine") or result.get("scanner"),
            recorded_at=now,
            initial=True,
        )
        db.add(Finding(
            engagement_id=engagement_id,
            asset_id=None,
            title=_SCAN_HEALTH_TITLE,
            description=summary["reason"],
            severity=FindingSeverity.low,
            status=FindingStatus.open,
            evidence=evidence,
            first_seen=now,
            last_seen=now,
            initial_detection_run_id=None,
            detection_run_id=None,
        ))
        await db.flush()
        return 1
    except Exception as exc:  # noqa: BLE001 — coverage warning must not sink the batch
        logger.warning("scan_health.finding_failed", error=str(exc))
        return 0
