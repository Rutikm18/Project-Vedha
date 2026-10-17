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

import asyncio
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import structlog
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DetectionStatus, FindingSeverity, FindingStatus
from app.models.asset import Asset
from app.models.finding import Finding
from app.models.detection_run import (
    DetectionRun, RUN_COMPLETED, RUN_FAILED, TRIGGER_FACTS_READY,
)
from app.models.detection_run_finding import (
    DetectionRunFinding, RUN_FINDING_NEW, RUN_FINDING_REAFFIRMED,
    RUN_FINDING_RESOLVED,
)
from app.discovery.finding_translator import (
    AssetCache, _resolve_asset, _find_open_duplicate, prime_asset_cache,
    exposed_service_condition, condition_index_key, DEDUP_KEY,
    merge_signals, prune_stale_signals, stronger_severity,
)
from app.detection.attack_paths import attack_path_findings
from app.detection.cve_text import (
    cve_description, cve_remediation, is_engine_notes_description,
)
from app.detection.prioritization import _posture_risk_on_manager_scale
from app.detection.resolution import (
    build_coverage, evaluate_resolutions, host_of, normalize_port,
)
from app.ai.verification_graph import run_verification
from app.config import get_settings
from app.services.finding_events import record_event
from app.services.finding_scan_provenance import (
    CUSTODY_CAPTURED_BY_MANAGER,
    preserve_trusted_scan_provenance,
    stamp_chain_of_custody,
)

logger = structlog.get_logger()

# A detection run's lease. If the worker crashes mid-run, the run stays RUNNING past
# this and the outbox reaper fails it. Kept equal to the worker's reaper threshold
# (app.workers.outbox.DETECTION_RUN_STALE_SEC) so a run is never reaped early.
DETECTION_RUN_LEASE_SEC = 10 * 60

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


# ── ingest health ─────────────────────────────────────────────────────────────
# Every detection rule — CVE and posture alike — reads the Assets that ingest
# builds. A fact the ingester rejects therefore reaches NOTHING: it is not a
# degraded result, it is an absent one. ingest quarantines silently by design (one
# corrupt line must not sink a 100k-record pass), and the pipeline returned that
# quarantine list to a caller that dropped it on the floor. The failure mode that
# produced was the worst kind: facts arrive, the run completes, findings are zero,
# and "we scanned and you are clean" is indistinguishable from "we understood
# nothing you sent". These two helpers make the difference observable.


def _ingest_census(ingest_result, submitted: int) -> tuple[dict, set[int]]:
    """(census, rejected_line_numbers) from the engine's IngestResult.

    The census — {submitted, ingested, quarantined, assets, reasons} — is what gets
    stamped onto the DetectionRun. The line numbers are 1-based and index the JSONL
    we just wrote one-fact-per-line, so they map straight back to the caller's list;
    that is how a caller filters to the facts ingest actually accepted WITHOUT
    re-implementing (and drifting from) ingest's own validation.

    Best-effort — an older engine may not return an IngestResult at all."""
    census = {"submitted": submitted, "ingested": 0, "quarantined": 0,
              "assets": 0, "reasons": {}}
    rejected: set[int] = set()
    if ingest_result is None:
        return census, rejected
    try:
        census["ingested"] = int(getattr(ingest_result, "fact_count", 0) or 0)
        census["assets"] = len(getattr(ingest_result, "assets", {}) or {})
        quarantined = list(getattr(ingest_result, "quarantined", []) or [])
        census["quarantined"] = len(quarantined)
        reasons: dict[str, int] = {}
        for q in quarantined:
            reason = str(getattr(q, "reason", "unknown"))
            reasons[reason] = reasons.get(reason, 0) + 1
            line = getattr(q, "source_line", None)
            if isinstance(line, int):
                rejected.add(line)
        # Cap the reason cardinality — this is stamped onto every DetectionRun.
        census["reasons"] = dict(sorted(reasons.items(), key=lambda kv: -kv[1])[:10])
    except Exception as exc:  # noqa: BLE001 — census must never break detection
        logger.debug("ingest_census.failed", error=str(exc))
    return census, rejected


def _accepted(facts: list[dict], rejected_lines: set[int]) -> list[dict]:
    """The subset of `facts` ingest accepted. We wrote one fact per line in order,
    so line N is facts[N-1]. Every downstream consumer must agree on what counts as
    a usable fact — a fact too malformed for the CVE and posture tracks must not be
    good enough for the attack-path track either."""
    if not rejected_lines:
        return facts
    return [f for i, f in enumerate(facts, start=1) if i not in rejected_lines]


# ── evaluation evidence for auto-resolution ───────────────────────────────────
# A finding may only accrue a clean miss when this run re-ran the SAME check on
# the SAME asset. These two helpers turn the engine's output into the evidence
# resolution.finding_coverage reads. Both are in-memory only; neither set is
# persisted, since a large engagement makes them large.

# The engine's OUTCOME_MATCH / OUTCOME_NO_MATCH: the only trace outcomes where a
# rule actually reached a verdict. Every other outcome is blind or unassessed and
# proves nothing about whether the weakness is still there.
_EVALUATED_OUTCOMES = frozenset({"match", "no_match"})


def _evaluated_checks(traces) -> set[tuple[str, str, int | None]]:
    """(rule_id, host, port) for every posture trace row that reached a verdict.
    The host is host_of(asset_ip), the form _resolve_asset stores on the Asset
    row the finding is joined to. A row with no rule id, no host or an
    unreadable port is dropped: it cannot prove anything."""
    out: set[tuple[str, str, int | None]] = set()
    for t in traces or []:
        if not isinstance(t, dict) or t.get("outcome") not in _EVALUATED_OUTCOMES:
            continue
        rule_id = t.get("rule_id")
        host = host_of(str(t.get("asset_ip") or ""))
        if not rule_id or not host:
            continue
        try:
            port = normalize_port(t.get("port"))
        except ValueError:
            continue
        out.add((str(rule_id), host, port))
    return out


def _identified_products(raw) -> dict[str, set[str]]:
    """The engine's {ip: ["vendor:product", ...]} as {host: {"vendor:product"}},
    keyed the way _resolve_asset keys the Asset row. Anything malformed is
    dropped rather than guessed at."""
    out: dict[str, set[str]] = {}
    if not isinstance(raw, dict):
        return out
    for ip, products in raw.items():
        host = host_of(str(ip or ""))
        if not host or not isinstance(products, (list, tuple, set)):
            continue
        keys = {p.lower() for p in products if isinstance(p, str) and p}
        if keys:
            out.setdefault(host, set()).update(keys)
    return out


def _log_ingest_health(census: dict, findings: int) -> None:
    """Escalate by severity of loss. A TOTAL wipeout with facts submitted is the
    agent/manager contract breaking — the one case that must never be quiet."""
    submitted = census.get("submitted") or 0
    quarantined = census.get("quarantined") or 0
    if not submitted or not quarantined:
        return
    if census.get("ingested"):
        logger.warning("detection_engine.facts_partially_rejected",
                       submitted=submitted, ingested=census.get("ingested"),
                       quarantined=quarantined, reasons=census.get("reasons"))
        return
    logger.error("detection_engine.all_facts_rejected",
                 submitted=submitted, quarantined=quarantined,
                 assets=census.get("assets"), findings=findings,
                 reasons=census.get("reasons"),
                 hint="probe/manager fact-shape drift — detection saw NOTHING; "
                      "a zero-finding result here does not mean the host is clean")


async def _run_detection_engine(
    facts: list[dict],
) -> tuple[list[dict], list[dict], dict]:
    """`detect_all_from_facts_traced` on a worker thread.

    The engine is synchronous CPU work (measured: 6.5s for 500 hosts' facts) and
    its only async caller is the outbox handler. Run inline, it froze that
    worker's whole event loop for the duration — no other event claimed, no
    reclaim sweep — and the reclaim lease is 5 minutes, so a large enough
    engagement had its event requeued and detected a second time while the first
    run was still going. Same engine, same contract; it just stops owning the loop.
    """
    return await asyncio.to_thread(detect_all_from_facts_traced, facts)


def detect_all_from_facts_traced(
    facts: list[dict],
) -> tuple[list[dict], list[dict], dict]:
    """Raw scanner facts -> (cve_finding_dicts, posture_finding_dicts, meta), running
    the FULL detection engine ONCE. `meta` carries the detection-trace roll-up:
    `{"coverage": {...}, "verdicts": {rule_id: {"verdict","reasons"}}}` — the
    machine-readable record of which rules were assessed, which were BLIND (drift /
    unparseable / error), and which had no evidence. That is what lets a non-finding
    explain itself instead of collapsing into an empty list. []/[]/{} on any failure
    (never raises). Falls back to CVE-only on an old engine.

    `meta["ingest"]` carries the INGEST census — how many submitted facts actually
    became assets and how many the ingester rejected. Without it, a fact shape the
    ingester refuses is indistinguishable from a clean network: every rule reads
    ingest's Assets, so zero assets means zero findings, silently. See
    _log_ingest_health.

    `meta["evaluated_checks"]` and `meta["identified_products"]` are the in-memory
    evidence auto-resolution needs per finding (see _evaluated_checks and
    _identified_products). Empty on every path that did not run that track."""
    # accepted_facts falls back to the raw list on every path where no ingest
    # verdict exists (engine missing, older engine, hard failure). Without a
    # verdict we cannot say a fact is bad, and silently disabling attack-path
    # correlation would trade one blind spot for another.
    # Every path without a full engine run carries EMPTY evaluation evidence, so
    # auto-resolution can prove nothing and resolves nothing.
    empty_meta: dict = {"coverage": {}, "verdicts": {}, "ingest": {},
                        "accepted_facts": list(facts or []),
                        "evaluated_checks": set(), "identified_products": {}}
    if not facts or not _ensure_importable():
        return [], [], empty_meta
    tmp = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as fh:
            for fact in facts:
                fh.write(json.dumps(fact, default=str) + "\n")
            tmp = fh.name
        try:
            from pipeline import run_full_detection  # type: ignore
            res = run_full_detection([tmp])
            cve = [f.to_dict() for f in res.get("cve", [])]
            posture = [f.to_dict() for f in res.get("posture", [])]
            census, rejected = _ingest_census(res.get("ingest"), len(facts))
            meta = {"coverage": res.get("posture_coverage") or {},
                    "verdicts": res.get("posture_verdicts") or {},
                    "ingest": census,
                    # NOT persisted — an in-memory view for this run's other
                    # consumers (attack paths). Same list objects, not a copy.
                    "accepted_facts": _accepted(facts, rejected),
                    # NOT persisted — what auto-resolution may count as re-checked.
                    "evaluated_checks": _evaluated_checks(res.get("posture_traces")),
                    "identified_products": _identified_products(
                        res.get("identified_products")),
                    # The CVE matcher's logic revision: a CVE finding stamped
                    # with another one is not auto-resolved by its absence.
                    "matcher_revision": res.get("matcher_revision")}
            _log_ingest_health(census, len(cve) + len(posture))
            return cve, posture, meta
        except ImportError:                          # older engine: CVE-only
            from pipeline import run_pipeline  # type: ignore
            findings, _ = run_pipeline([tmp])
            # Mirror run_full_detection's gap #4 partition: a `range-open` match
            # is product-presence (open-ended range, no version signal), not a
            # customer-facing CVE — withhold it here too so this degraded path
            # cannot reintroduce the banner-host flood.
            cve = [f.to_dict() for f in findings
                   if getattr(f, "match_basis", None) not in ("range-open", "range-distro")]
            return cve, [], empty_meta
    except Exception as exc:  # noqa: BLE001
        # The CVE track can fail on its own (e.g. a missing/oversized NVD snapshot);
        # the POSTURE track must NOT go down with it — config-exposure findings need
        # no vuln DB. Try posture standalone (traced) before giving up.
        logger.warning("detection_engine.full_run_failed", error=str(exc))
        try:
            from ingest import ingest_files      # type: ignore
            from posture_rules import (detect_all_traced,  # type: ignore
                                       summarize_traces, verdict_for_rule)
            ing = ingest_files([tmp])
            posture_f, traces = detect_all_traced(ing)
            posture = [f.to_dict() for f in posture_f]
            verdicts = {}
            for rid in sorted({t.rule_id for t in traces}):
                v, reasons = verdict_for_rule(traces, rid)
                verdicts[rid] = {"verdict": v, "reasons": reasons}
            census, rejected = _ingest_census(ing, len(facts))
            _log_ingest_health(census, len(posture))
            # The posture rules did run, so their verdicts are evidence; the CVE
            # track did not, so no product counts as re-identified.
            meta = {"coverage": summarize_traces(traces), "verdicts": verdicts,
                    "ingest": census,
                    "accepted_facts": _accepted(facts, rejected),
                    "evaluated_checks": _evaluated_checks(
                        [t.to_dict() for t in traces]),
                    "identified_products": {}}
            if posture:
                logger.info("detection_engine.posture_only_fallback", count=len(posture))
            return [], posture, meta
        except Exception as exc2:  # noqa: BLE001
            logger.warning("detection_engine.posture_fallback_failed", error=str(exc2))
            return [], [], empty_meta
    finally:
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass


def detect_all_from_facts(facts: list[dict]) -> tuple[list[dict], list[dict]]:
    """Backward-compatible (cve, posture) view — drops the trace meta."""
    cve, posture, _meta = detect_all_from_facts_traced(facts)
    return cve, posture


def detect_findings_from_facts(facts: list[dict]) -> list[dict]:
    """CVE finding dicts only — backward-compatible wrapper over the full run."""
    return detect_all_from_facts_traced(facts)[0]


# Posture severities are already critical/high/medium/low/info — the same vocabulary
# the backend uses, so the map is a straight pass-through with an info fallback.
_POSTURE_SEV = {
    "critical": FindingSeverity.critical, "high": FindingSeverity.high,
    "medium": FindingSeverity.medium, "low": FindingSeverity.low,
    "info": FindingSeverity.info,
}


# (port, superseded exposed-service rule) pairs the port catalog has relabelled.
# 9100 was "JetDirect / Prometheus node-exporter" under ADMIN_UI on every printer; it
# is raw printing (POSTURE-EXPOSED-PRINTER) unless HTTP was observed.
_CATALOG_RELABELS = {(9100, "POSTURE-EXPOSED-ADMIN_UI")}


def _is_catalog_relabel(prev_ev: dict, incoming: dict) -> bool:
    try:
        port = int(incoming.get("port") or prev_ev.get("port") or 0)
    except (TypeError, ValueError):
        return False
    old_rule, new_rule = prev_ev.get("rule_id"), incoming.get("rule_id")
    return (bool(new_rule) and old_rule != new_rule
            and str(new_rule).startswith("POSTURE-EXPOSED-")
            and (port, old_rule) in _CATALOG_RELABELS)


def _backfill_cve_text(finding, d: dict) -> None:
    """A CVE finding created before cve_text existed has no remediation and the
    matcher's raw notes as its description. Fill those on reaffirmation; never touch
    text a person wrote or edited."""
    if not finding.remediation:
        finding.remediation = cve_remediation(d)
    if not finding.description or is_engine_notes_description(finding.description):
        finding.description = cve_description(d)


def _posture_title(p: dict) -> str:
    """Stable, human title for a posture finding — the same string across runs so
    dedup/regression tracking works. Port is folded in so a rule that fires on two
    ports of one host stays two findings, not one collapsed row."""
    base = p.get("title") or p.get("rule_id") or "configuration weakness"
    port = p.get("port")
    return (f"{base} (port {port})" if port else base)[:500]


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


async def _record_regression_reopen(db, finding, run_id, now) -> None:
    """Reopen a regression and persist the prior closure provenance."""
    previous_status = finding.status
    prior_method = finding.resolution_method
    prior_run_id = finding.resolution_run_id
    prior_resolved_at = finding.resolved_at
    _apply_regression_reopen(finding, run_id, now)
    await record_event(
        db,
        finding,
        "reopened",
        actor="detection-engine",
        actor_type="system",
        from_status=previous_status,
        to_status=FindingStatus.open,
        detail={
            "origin": "detection_engine_regression",
            "reason": "finding re-observed in a later detection run",
            "run_id": str(run_id),
            "observed_at": now.isoformat(),
            "prior_resolution_method": prior_method,
            "prior_resolution_run_id": (
                str(prior_run_id) if prior_run_id is not None else None
            ),
            "prior_resolved_at": (
                prior_resolved_at.isoformat()
                if prior_resolved_at is not None
                else None
            ),
        },
    )


async def _load_remediated_index(db, engagement_id) -> dict:
    """The regression candidates, in ONE query. See load_finding_index."""
    from app.discovery.finding_translator import load_finding_index
    return await load_finding_index(db, engagement_id,
                                    [FindingStatus.remediated])


async def _find_remediated_match(db, engagement_id, asset_id, title, *,
                                 index: dict | None = None):
    """A remediated finding with the same (engagement, asset, title) — the
    regression candidate. Mirrors _find_open_duplicate but for the closed set.

    `index` (from _load_remediated_index) answers from memory. A row reopened
    through it must be removed from the index by the caller, so one run cannot
    reopen the same row twice.
    """
    if index is not None:
        return index.get((asset_id, title))
    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status == FindingStatus.remediated,
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()


def _posture_description(p: dict) -> str | None:
    """What a reader sees as the finding's description: a plain-language sentence about the
    weakness from the knowledge base. The rule's own metadata (CWE, ATT&CK, scanner, false-
    positive note) lives in the evidence and in the report's `detection_rationale`, not here.
    Falls back to that metadata line only when the KB has nothing for the rule."""
    try:
        from types import SimpleNamespace
        from app.services import report_enrichment as enrich
        probe = SimpleNamespace(evidence=p, title=p.get("title"), description="",
                                remediation=p.get("remediation"), cve_ids=None,
                                severity=p.get("severity"))
        sentence = enrich.first_sentence(enrich.kb_narrative(probe)["technical_details"])
        if sentence:
            return sentence
    except Exception:  # noqa: BLE001 — a description is decoration, never a reason to drop a finding
        pass
    bits: list[str] = []
    if p.get("cwe"):
        bits.append(p["cwe"])
    if p.get("mitre"):
        bits.append(f"ATT&CK {p['mitre']}")
    if p.get("scanner"):
        bits.append(f"observed by {p['scanner']}")
    if p.get("fp_notes"):
        bits.append(p["fp_notes"])
    return "; ".join(bits) or None


async def _persist_posture_findings(db, engagement_id, run_id, now, posture_dicts,
                                    touched: list, db_version,
                                    cache: dict | None = None,
                                    open_index: dict | None = None,
                                    remediated_index: dict | None = None,
                                    identity=None,
                                    ) -> tuple[int, int]:
    """Translate posture/config-exposure findings (from the VERIFIED scanners) into
    backend Finding rows, reusing the SAME dedup + regression-reopen lifecycle as
    the CVE loop so they track across runs identically. Returns (created, reaffirmed).
    These carry severity, risk_score, MITRE technique and remediation straight from
    the detection-as-code rule — ready for prioritization and the portal."""
    created = reaffirmed = 0
    for p in posture_dicts:
        try:
            title = _posture_title(p)
            manager_risk = _posture_risk_on_manager_scale(p)
            asset = await _resolve_asset(db, engagement_id, p.get("asset_ip"), cache=cache,
                                         identity=identity)
            asset_id = asset.id if asset else None

            # gap #2: an exposed-service posture finding (POSTURE-EXPOSED-*) carries
            # a per-port condition key so it is the SAME issue as any other
            # producer's exposed-service finding on that port, merging instead of
            # adding a second, differently-titled row. Dedicated-scanner findings
            # (SMB/RDP/TLS) are not keyed by port — two real issues can share one.
            # Every rule carries its canonical condition key (posture_rules.condition_key),
            # so dedicated-scanner findings merge with port-intel rows of the SAME
            # (service, weakness-class) while a different weakness on the same port stays
            # its own finding. Older engine output without the key keeps the legacy rule.
            ev_in = p.get("evidence") if isinstance(p.get("evidence"), dict) else {}
            condition = ev_in.get(DEDUP_KEY) or (
                exposed_service_condition(p.get("port"), p.get("proto"))
                if str(p.get("rule_id") or "").startswith("POSTURE-EXPOSED-") else None)
            if condition:
                p[DEDUP_KEY] = condition

            dup = await _find_open_duplicate(db, engagement_id, asset_id, title,
                                             condition=condition, index=open_index)
            if dup is not None:
                new_sev = _POSTURE_SEV.get(p.get("severity"), FindingSeverity.info)
                prev_ev = dup.evidence if isinstance(dup.evidence, dict) else {}
                if _is_catalog_relabel(prev_ev, p):
                    # Our own port catalog corrected its label for this port: the
                    # open finding takes the corrected title (it is the same
                    # producer, not a second signal). Severity never goes down.
                    dup.title = title
                    dup.severity = stronger_severity(dup.severity, new_sev)
                    prev_ev = {**{k: v for k, v in prev_ev.items() if k != "signals"},
                               "rule_id": p.get("rule_id")}
                different_producer = bool(condition) and (
                    dup.title != title or prev_ev.get("rule_id") != p.get("rule_id"))
                if different_producer or prev_ev.get("signals"):
                    # Another producer/rule describing the SAME condition: keep the strongest
                    # severity and remember every signal (stamped with this run) for the
                    # report roll-up. A finding already carrying signals refreshes its own.
                    p["signals"] = merge_signals(
                        prev_ev, existing_rule_id=prev_ev.get("rule_id"),
                        existing_title=dup.title, existing_severity=dup.severity,
                        existing_run_id=dup.detection_run_id, run_id=run_id,
                        incoming={"rule_id": p.get("rule_id"), "title": title,
                                  "severity": p.get("severity")})
                    if different_producer:
                        dup.severity = stronger_severity(dup.severity, new_sev)
                dup.evidence = preserve_trusted_scan_provenance(
                    p,
                    previous_evidence=dup.evidence,
                )
                dup.last_seen = now
                dup.detection_run_id = run_id
                dup.resolution_miss_count = 0
                dup.risk_score = Decimal(str(manager_risk)) if manager_risk is not None else None
                touched.append(dup)
                reaffirmed += 1
                continue

            regressed = await _find_remediated_match(db, engagement_id, asset_id,
                                                     title,
                                                     index=remediated_index)
            if regressed is not None:
                await _record_regression_reopen(db, regressed, run_id, now)
                previous_evidence = regressed.evidence
                regressed.evidence = preserve_trusted_scan_provenance(
                    {**(previous_evidence or {}), **p, "regression": True},
                    previous_evidence=previous_evidence,
                )
                regressed.risk_score = Decimal(str(manager_risk)) if manager_risk is not None else None
                touched.append(regressed)
                reaffirmed += 1
                # Reopened: it is no longer a regression candidate, and it IS now
                # the open row this identity dedups against.
                if remediated_index is not None:
                    remediated_index.pop((asset_id, title), None)
                if open_index is not None:
                    open_index[(asset_id, title)] = regressed
                    if condition:
                        open_index[condition_index_key(asset_id, condition)] = regressed
                continue

            state = p.get("state")
            f = Finding(
                engagement_id=engagement_id,
                asset_id=asset_id,
                cve_ids=None,
                title=title,
                description=_posture_description(p),
                risk_score=(Decimal(str(manager_risk))
                            if manager_risk is not None else None),
                severity=_POSTURE_SEV.get(p.get("severity"), FindingSeverity.info),
                status=(FindingStatus.confirmed if state == "confirmed"
                        else FindingStatus.open),
                detection_status=DetectionStatus.detected,
                mitre_techniques=[p["mitre"]] if p.get("mitre") else None,
                remediation=p.get("remediation"),
                evidence=p,
                first_seen=now,
                last_seen=now,
                initial_detection_run_id=run_id,
                detection_run_id=run_id,
                detected_db_version=db_version,
            )
            db.add(f)
            touched.append(f)
            created += 1
            if open_index is not None and condition:
                open_index[condition_index_key(asset_id, condition)] = f
            # The dedup lookup no longer autoflushes into a query, so a second
            # finding with this identity in the SAME run only collapses onto
            # this row if the index knows about it.
            if open_index is not None:
                open_index[(asset_id, title)] = f
        except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
            logger.warning("posture_finding.create_failed",
                           rule_id=p.get("rule_id"), error=str(exc))
    return created, reaffirmed


def _stamp_chain_of_custody(findings, now) -> None:
    """Stamp integrity custody on every finding this detection run touched.

    These rows (CVE, posture, attack-path) record their scan lineage in DB
    columns, not an evidence ``scan_provenance`` block, so they never passed
    through ``record_scan_observation`` and would otherwise reach the report with
    no integrity hash. ``captured_by`` is the manager (it computed the digest);
    ``source_host`` is the asset IP the rule fired on when the evidence carries
    one. A failure on one finding must not sink the batch or the run.
    """
    for f in findings:
        try:
            evidence = f.evidence if isinstance(f.evidence, dict) else {}
            f.evidence = stamp_chain_of_custody(
                evidence,
                source_host=evidence.get("asset_ip") or evidence.get("target"),
                captured_by=CUSTODY_CAPTURED_BY_MANAGER,
                tool=evidence.get("scanner") or evidence.get("engine"),
                captured_at=now,
            )
        except Exception as exc:  # noqa: BLE001 — custody must never break the run
            logger.warning("custody.stamp_failed", error=str(exc))


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
    """ip → {device_role, role_detail, role_confidence, os} from already-promoted assets, so a
    prior device_inventory scan amplifies today's correlation (Track B2). The confidence and OS
    let the correlator ignore a role that is not trustworthy (see intel.device_role)."""
    rows = (await db.execute(
        select(Asset.ip_address, Asset.device_role, Asset.role_detail,
               Asset.role_confidence, Asset.os).where(
            Asset.engagement_id == engagement_id,
            Asset.device_role.isnot(None),
        )
    )).all()
    return {
        ip: {"device_role": role, "role_detail": detail,
             "role_confidence": confidence, "os": os_name}
        for ip, role, detail, confidence, os_name in rows if ip
    }


async def _persist_attack_paths(
    db: AsyncSession, engagement_id: uuid.UUID, run, facts: list[dict], now,
    cache: dict | None = None, open_index: dict | None = None,
    remediated_index: dict | None = None,
    touched: list | None = None,
    identity=None,
) -> int:
    """Correlate composite attack paths from the run's facts and persist them as
    Finding rows (deduped by title, reaffirmed across runs). Returns NEW count."""
    device_roles = await _engagement_device_roles(db, engagement_id)
    created = 0
    for d in attack_path_findings(facts, device_roles):
        try:
            asset = await _resolve_asset(db, engagement_id, d.get("target"), cache=cache,
                                         identity=identity)
            asset_id = asset.id if asset else None
            title = d["title"][:500]
            evidence = {
                "rule_id": d["rule_id"], "correlation": True,
                "remediation": d.get("remediation"),
                "mitre_techniques": d.get("mitre_techniques"),
                **(d.get("evidence") or {}),
            }
            dup = await _find_open_duplicate(db, engagement_id, asset_id, title,
                                             index=open_index)
            if dup is not None:
                dup.severity = d["severity"]     # re-amplify if the role changed
                dup.evidence = preserve_trusted_scan_provenance(
                    evidence,
                    previous_evidence=dup.evidence,
                )
                dup.last_seen = now
                dup.detection_run_id = run.id
                dup.resolution_miss_count = 0
                if touched is not None:
                    touched.append(dup)
                continue
            regressed = await _find_remediated_match(
                db,
                engagement_id,
                asset_id,
                title,
                index=remediated_index,
            )
            if regressed is not None:
                await _record_regression_reopen(db, regressed, run.id, now)
                regressed.severity = d["severity"]
                regressed.evidence = preserve_trusted_scan_provenance(
                    {**evidence, "regression": True},
                    previous_evidence=regressed.evidence,
                )
                if touched is not None:
                    touched.append(regressed)
                if remediated_index is not None:
                    remediated_index.pop((asset_id, title), None)
                if open_index is not None:
                    open_index[(asset_id, title)] = regressed
                continue
            path_finding = Finding(
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
                initial_detection_run_id=run.id,
                detection_run_id=run.id,
            )
            db.add(path_finding)
            if touched is not None:
                touched.append(path_finding)
            if open_index is not None:
                open_index[(asset_id, title)] = path_finding
            created += 1
        except Exception as exc:  # noqa: BLE001 — one composite must not sink the batch
            logger.warning("attack_path.create_failed", rule_id=d.get("rule_id"), error=str(exc))
    await db.flush()
    return created


# ── R1: one engagement's detection is a critical section ──────────────────────
# The outbox worker processes a claimed batch with asyncio.gather, so two
# facts.ready events for the SAME engagement (two probes, or a re-submission) run
# detection concurrently. Everything below — duplicate detection, regression
# reopening, resolution evaluation — is read-then-write against the same Finding
# rows, with no unique constraint underneath. Concurrently, both passes read
# "absent" and both insert, and the customer sees one issue twice.
#
# A transaction-scoped Postgres advisory lock serialises detection PER ENGAGEMENT
# and nothing else: different engagements still run fully in parallel, which is
# the axis that actually scales. pg_advisory_xact_lock releases on COMMIT or
# ROLLBACK, so no path can leak it — that is why the xact variant is used rather
# than the session one.
#
# See docs/adr/0001-manager-detection-pipeline.md.
async def _lock_engagement_for_detection(db: AsyncSession, engagement_id: uuid.UUID) -> None:
    # A UUID is 128 bits and the lock key is 64, so fold it. Collisions across
    # engagements are harmless: the worst case is two unrelated engagements
    # briefly serialising with each other.
    key = (engagement_id.int ^ (engagement_id.int >> 64)) & 0x7FFFFFFFFFFFFFFF
    await db.execute(text("SELECT pg_advisory_xact_lock(:k)"), {"k": key})


async def _record_run_membership(db: AsyncSession, run: DetectionRun) -> None:
    """One membership row per finding this run touched, so a scan's exact finding
    set — and a diff between two scans (new / fixed / still-present) — is later
    recoverable. Run-level counts (findings_new/reaffirmed/current) can't do that.

    Derived from the finding rows' own run pointers AFTER every write and the
    auto-resolution pass, so it is exactly as consistent as the run itself:
      - detection_run_id == run.id → created or reaffirmed this run; first_seen ==
        last_seen distinguishes the two (a reaffirm only advances last_seen, and a
        finding created this run is deduped, so it is never re-touched within it).
      - resolution_run_id == run.id → this run's coverage closed it. Disjoint from
        the set above: evaluate_resolutions only considers detection_run_id != run.id.
    Best-effort — membership bookkeeping must never sink an otherwise-good run."""
    touched = (await db.execute(
        select(Finding.id, Finding.first_seen, Finding.last_seen,
               Finding.severity, Finding.risk_score, Finding.status).where(
            Finding.detection_run_id == run.id)
    )).all()
    for fid, first_seen, last_seen, severity, risk_score, fstatus in touched:
        outcome = RUN_FINDING_NEW if first_seen == last_seen else RUN_FINDING_REAFFIRMED
        # Snapshot the finding as this scan saw it, so a later diff can say what changed.
        db.add(DetectionRunFinding(
            run_id=run.id, finding_id=fid, outcome=outcome,
            severity=getattr(severity, "value", severity),
            risk_score=risk_score,
            status=getattr(fstatus, "value", fstatus)))
    resolved_ids = (await db.execute(
        select(Finding.id).where(Finding.resolution_run_id == run.id)
    )).scalars().all()
    for fid in resolved_ids:
        db.add(DetectionRunFinding(
            run_id=run.id, finding_id=fid, outcome=RUN_FINDING_RESOLVED))


async def _notify_new_findings(db: AsyncSession, engagement_id: uuid.UUID, run_id: uuid.UUID) -> None:
    """Tell the tenant about the Critical / High findings this run opened (one
    message per severity, per run), if their notification rules say so. Never
    raises, and runs in a savepoint so even a database error here cannot spoil the
    detection run's own transaction."""
    try:
        from app.models.engagement import Engagement
        from app.services.notification_rules import notify_event_safe

        async with db.begin_nested():
            opened = (await db.execute(
                select(Finding.severity, Finding.title).where(
                    Finding.initial_detection_run_id == run_id,
                    Finding.severity.in_([FindingSeverity.critical, FindingSeverity.high]),
                )
            )).all()
            if not opened:
                return
            eng = (await db.execute(
                select(Engagement.tenant_id, Engagement.name).where(Engagement.id == engagement_id)
            )).one_or_none()
            if eng is None:
                return
            tenant_id, name = eng
            for severity, label, event in (
                (FindingSeverity.critical, "Critical", "critical_finding"),
                (FindingSeverity.high, "High", "high_finding"),
            ):
                titles = [t for s, t in opened if s == severity]
                if not titles:
                    continue
                shown = "\n".join(f"- {t}" for t in titles[:5])
                more = f"\n…and {len(titles) - 5} more" if len(titles) > 5 else ""
                await notify_event_safe(
                    db, tenant_id, event,
                    f"Vedha: {len(titles)} new {label} finding{'s' if len(titles) != 1 else ''} in {name}",
                    f"A scan of '{name}' opened {len(titles)} {label} finding{'s' if len(titles) != 1 else ''}:\n"
                    f"{shown}{more}")
    except Exception as exc:  # noqa: BLE001 — notification must not fail the run
        logger.warning("detection_run.notify_failed", run_id=str(run_id), error=str(exc))


async def _notify_coverage_gap(db: AsyncSession, engagement_id: uuid.UUID, ingest: dict | None) -> None:
    """Tell the tenant when a scan's facts were partly or wholly rejected: the checks
    for those facts never ran, so a quiet result is not a clean one. Same guarantees
    as _notify_new_findings: a savepoint, and it never raises."""
    try:
        census = ingest if isinstance(ingest, dict) else {}
        quarantined = int(census.get("quarantined") or 0)
        if quarantined <= 0:
            return
        from app.models.engagement import Engagement
        from app.services.notification_rules import notify_event_safe

        submitted = int(census.get("submitted") or 0)
        ingested = int(census.get("ingested") or 0)
        reasons = census.get("reasons") if isinstance(census.get("reasons"), dict) else {}
        async with db.begin_nested():
            eng = (await db.execute(
                select(Engagement.tenant_id, Engagement.name).where(Engagement.id == engagement_id)
            )).one_or_none()
            if eng is None:
                return
            tenant_id, name = eng
            why = "; ".join(f"{str(k)[:80]} ({int(v)})" for k, v in list(reasons.items())[:3]) or "no reason recorded"
            await notify_event_safe(
                db, tenant_id, "coverage_gap",
                f"Vedha: detection coverage gap in {name}",
                f"A scan of '{name}' submitted {submitted} facts but {quarantined} could not be "
                f"understood ({ingested} checked), so those hosts and services were not "
                f"assessed. Top reasons: {why}.")
    except Exception as exc:  # noqa: BLE001 — notification must not fail the run
        logger.warning("detection_run.coverage_notify_failed", error=str(exc))
async def _refresh_attack_paths(db: AsyncSession, engagement_id: uuid.UUID) -> None:
    """Best-effort refresh of an engagement's stored attack paths (see
    attack_paths.refresh_if_materialised). Imported lazily: the router pulls in the
    web layer, which detection must not depend on at import time."""
    try:
        from app.routers.attack_paths import refresh_if_materialised
        await refresh_if_materialised(db, engagement_id)
    except Exception as exc:  # noqa: BLE001 — a stale path list must not fail detection
        logger.warning("detection_run.attack_path_refresh_failed",
                       engagement_id=str(engagement_id), error=str(exc))


async def _refresh_attack_paths(db: AsyncSession, engagement_id: uuid.UUID) -> None:
    """Best-effort refresh of an engagement's stored attack paths (see
    attack_paths.refresh_if_materialised). Imported lazily: the router pulls in the
    web layer, which detection must not depend on at import time."""
    try:
        from app.routers.attack_paths import refresh_if_materialised
        await refresh_if_materialised(db, engagement_id)
    except Exception as exc:  # noqa: BLE001 — a stale path list must not fail detection
        logger.warning("detection_run.attack_path_refresh_failed",
                       engagement_id=str(engagement_id), error=str(exc))


async def create_findings_from_facts(
    db: AsyncSession, engagement_id: uuid.UUID, result: dict,
    *, scan_result_id: uuid.UUID | None = None, job_id: uuid.UUID | None = None,
    trigger: str = TRIGGER_FACTS_READY,
) -> int:
    """New raw-facts path: detect CVE findings from result['facts'] and persist
    them as Finding rows, wrapped in a DetectionRun so the outcome is a temporal
    record (new vs reaffirmed, against a stamped vuln-DB version). Returns the
    count of NEW rows (reaffirmed ones don't count). Best-effort per finding."""
    facts = result.get("facts")
    if not isinstance(facts, list) or not facts:
        return 0

    # Serialise this engagement's detection before reading anything — see
    # _lock_engagement_for_detection. Held until this transaction ends.
    await _lock_engagement_for_detection(db, engagement_id)

    # The outbox is at-least-once. Its fast pre-check avoids normal replays, but
    # two duplicate events can both pass that check before either transaction
    # commits. Re-check under the per-engagement advisory lock so exactly one
    # completed DetectionRun is created for a concrete ScanResult. A failed run
    # is deliberately retryable.
    if scan_result_id is not None:
        completed_run_id = (
            await db.execute(
                select(DetectionRun.id)
                .where(
                    DetectionRun.scan_result_id == scan_result_id,
                    DetectionRun.status == RUN_COMPLETED,
                )
                .limit(1)
            )
        ).scalar_one_or_none()
        if completed_run_id is not None:
            logger.info(
                "detection_run.scan_result_already_completed",
                engagement_id=str(engagement_id),
                scan_result_id=str(scan_result_id),
                detection_run_id=str(completed_run_id),
            )
            return 0

    now = datetime.now(timezone.utc)
    db_version, db_fetched = _vuln_db_meta()

    # Open the run first, so every finding created below can reference run.id and
    # the run row is the single provenance record for this detection execution.
    # Stamp a lease: if this worker dies mid-detection, the run stays RUNNING past
    # lease_expires_at and the outbox reaper fails it precisely (vs guessing from age).
    run = DetectionRun(
        engagement_id=engagement_id,
        scan_result_id=scan_result_id,
        job_id=job_id,
        trigger=trigger,
        vuln_db_version=db_version,
        vuln_db_fetched_at=db_fetched,
        started_at=now,
        lease_expires_at=now + timedelta(seconds=DETECTION_RUN_LEASE_SEC),
        facts_count=len(facts),
    )
    db.add(run)
    await db.flush()   # assigns run.id

    created = 0
    reaffirmed = 0
    try:
        touched: list = []
        # One asset cache shared by the CVE, posture and attack-path loops: the same
        # host is resolved ONCE per run instead of once per finding (kills the N+1).
        asset_cache: AssetCache = AssetCache()
        # Asset identity for this submission (P1b): global by default; private IPs
        # scoped to the submitting probe's site when the engagement opts in.
        # Resolved ONCE so the CVE, posture and composite loops agree.
        from app.services.asset_resolution import identity_context
        identity = await identity_context(db, engagement_id, scan_result_id=scan_result_id)
        # The same treatment for the dedup/regression lookups, which were the
        # other N+1 in these loops: TWO queries load this engagement's existing
        # findings, instead of one or two per finding produced (~12 per host, so
        # thousands of round trips on a large run — inside the outbox handler,
        # whose lease is 5 minutes). Both loops must keep these dicts current as
        # they create or reopen rows; see _find_open_duplicate.
        from app.discovery.finding_translator import load_open_finding_index
        open_index = await load_open_finding_index(db, engagement_id)
        remediated_index = await _load_remediated_index(db, engagement_id)
        # ONE full-detection pass over the raw facts → BOTH the CVE/version track
        # and the posture/config-exposure track (the verified scanners' findings),
        # plus the detection-trace coverage roll-up (which rules were blind/clean/
        # not-assessed) so a non-finding can explain itself.
        cve_dicts, posture_dicts, detect_meta = await _run_detection_engine(facts)
        # Every host this run can touch, looked up in ONE query per 1,000 instead of
        # one per host (the remaining per-host N+1: ~1 SELECT per distinct host).
        await prime_asset_cache(
            db, engagement_id,
            [f.get("target") for f in facts if isinstance(f, dict)]
            + [d.get("asset_ip") for d in cve_dicts]
            + [p.get("asset_ip") for p in posture_dicts],
            asset_cache, identity=identity)
        for d in cve_dicts:
            try:
                cve = d.get("cve_id") or "finding"
                title = f"{cve} — {d.get('cpe', '').split(':')[4] if d.get('cpe') else ''}".strip(" —")[:500]
                asset = await _resolve_asset(db, engagement_id, d.get("asset_ip"),
                                             cache=asset_cache, identity=identity)
                asset_id = asset.id if asset else None

                dup = await _find_open_duplicate(db, engagement_id, asset_id, title,
                                                 index=open_index)
                if dup is not None:
                    # Same issue still present → reaffirm: advance last_seen and
                    # point it at this run (first_seen is preserved).
                    dup.evidence = preserve_trusted_scan_provenance(
                        d,
                        previous_evidence=dup.evidence,
                    )
                    _backfill_cve_text(dup, d)
                    dup.last_seen = now
                    dup.detection_run_id = run.id
                    dup.resolution_miss_count = 0   # re-observed → out of the resolution window
                    touched.append(dup)
                    reaffirmed += 1
                    continue

                regressed = await _find_remediated_match(db, engagement_id, asset_id,
                                                         title,
                                                         index=remediated_index)
                if regressed is not None:
                    # An auto/manually-resolved issue is back → reopen the SAME row
                    # and flag the regression (its history is preserved).
                    await _record_regression_reopen(db, regressed, run.id, now)
                    previous_evidence = regressed.evidence
                    regressed.evidence = preserve_trusted_scan_provenance(
                        {**(previous_evidence or {}), **d, "regression": True},
                        previous_evidence=previous_evidence,
                    )
                    _backfill_cve_text(regressed, d)
                    touched.append(regressed)
                    reaffirmed += 1
                    # Reopened rows leave the regression set and join the open one.
                    remediated_index.pop((asset_id, title), None)
                    open_index[(asset_id, title)] = regressed
                    continue

                state = d.get("state")
                new_finding = Finding(
                    engagement_id=engagement_id,
                    asset_id=asset_id,
                    cve_ids=[cve] if d.get("cve_id") else None,
                    title=title,
                    description=cve_description(d),
                    remediation=cve_remediation(d),
                    cvss_score=Decimal(str(d["cvss_score"])) if d.get("cvss_score") is not None else None,
                    cvss_vector=d.get("cvss_vector"),
                    epss_score=Decimal(str(d["epss_score"])) if d.get("epss_score") is not None else None,
                    severity=_PRIORITY_TO_SEVERITY.get(d.get("priority"), FindingSeverity.info),
                    status=FindingStatus.confirmed if state == "confirmed" else FindingStatus.open,
                    detection_status=DetectionStatus.detected,
                    evidence=d,
                    first_seen=now,
                    last_seen=now,
                    initial_detection_run_id=run.id,
                    detection_run_id=run.id,
                    detected_db_version=db_version,
                )
                db.add(new_finding)
                touched.append(new_finding)
                created += 1
                # Index it: without the autoflush the old per-finding query
                # relied on, a second identical finding in this run would
                # otherwise be created twice.
                open_index[(asset_id, title)] = new_finding
            except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
                logger.warning("detection_finding.create_failed", error=str(exc))

        # ── Posture / config-exposure track (the VERIFIED scanners' findings) ──
        # SMBv1, RDP-without-NLA, deprecated TLS, exposed RPC, UDP amplifiers — the
        # weaknesses the CVE loop cannot see because they are configuration, not a
        # vulnerable version. Same dedup/regression lifecycle, ready for the portal.
        try:
            p_created, p_reaffirmed = await _persist_posture_findings(
                db, engagement_id, run.id, now, posture_dicts, touched, db_version,
                cache=asset_cache, open_index=open_index,
                remediated_index=remediated_index, identity=identity)
            created += p_created
            reaffirmed += p_reaffirmed
        except Exception as exc:  # noqa: BLE001 — posture must not sink the run
            logger.warning("posture_findings.batch_failed", error=str(exc))

        await db.flush()

        # ── Composite attack-path correlation (Track B) ──────────────────────
        # The CVE loop above scores single facts; this pass chains weaknesses on
        # one host into the attack PATH an operator must fix first (NTLM relay,
        # legacy-Windows surface, cleartext cluster, exposed-DB+unauth, default
        # SNMP on infra), amplified by the host's device role. Best-effort.
        # Correlate over the facts INGEST ACCEPTED, not the raw submission. A fact
        # the CVE and posture tracks refused is not evidence this track may use
        # either — otherwise a submission rejected wholesale still emits an
        # "NTLM relay attack path", which is a finding built on nothing.
        try:
            corr_new = await _persist_attack_paths(
                db, engagement_id, run, detect_meta.get("accepted_facts") or [], now,
                cache=asset_cache, open_index=open_index,
                remediated_index=remediated_index, touched=touched, identity=identity)
            created += corr_new
        except Exception as exc:  # noqa: BLE001 — correlation must not sink the run
            logger.warning("detection_run.correlation_failed", error=str(exc))

        # Chain of custody: stamp an integrity digest on every finding this run
        # touched BEFORE resolution reads them, so the engagement report can prove
        # the recorded evidence is unchanged. Unconditional (unlike verification)
        # and best-effort; the final flush persists it.
        prune_stale_signals(touched, run.id)
        _stamp_chain_of_custody(touched, now)

        # Coverage ledger + coverage-gated auto-resolution (Phase 0/1). Best-effort:
        # never let resolution failure sink an otherwise-good detection run.
        # Host coverage alone never closes a finding: each one also needs this
        # run's evidence that its own check was re-run (see finding_coverage).
        resolved = 0
        try:
            coverage = build_coverage(result.get("scanner_runs"), facts)
            skips: dict[str, int] = {}
            resolved = await evaluate_resolutions(
                db, engagement_id, run, coverage, now,
                evaluated_checks=detect_meta.get("evaluated_checks") or set(),
                identified_products=detect_meta.get("identified_products") or {},
                matcher_revision=detect_meta.get("matcher_revision"),
                skips=skips)
            # Counts only: why nothing auto-closed, readable by an operator.
            coverage["resolution_skips"] = dict(sorted(skips.items()))
            run.stats = {"coverage": coverage, "auto_resolved": resolved,
                         "posture_coverage": detect_meta.get("coverage") or {},
                         "posture_verdicts": detect_meta.get("verdicts") or {},
                         "ingest": detect_meta.get("ingest") or {}}
        except Exception as exc:  # noqa: BLE001 — resolution must not fail the run
            logger.warning("detection_run.resolution_failed", error=str(exc))
            run.stats = {"coverage": {}, "auto_resolved": 0,
                         "posture_coverage": detect_meta.get("coverage") or {},
                         "posture_verdicts": detect_meta.get("verdicts") or {},
                         "ingest": detect_meta.get("ingest") or {}}

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

        # Record which findings this run touched (new/reaffirmed/resolved) so a
        # scan's exact finding set and a scan-to-scan diff are recoverable later.
        try:
            await _record_run_membership(db, run)
            await db.flush()
        except Exception as exc:  # noqa: BLE001 — membership must not fail the run
            logger.warning("detection_run.membership_failed", error=str(exc))

        run.status = RUN_COMPLETED
        run.finished_at = datetime.now(timezone.utc)
        run.findings_new = created
        run.findings_reaffirmed = reaffirmed
        run.findings_current = int(current or 0)
        await db.flush()
        if created:
            await _notify_new_findings(db, engagement_id, run.id)
        await _notify_coverage_gap(db, engagement_id, (run.stats or {}).get("ingest"))



        # Stored attack paths and the fix-first analysis describe the findings as of
        # their last computation. When this run changed the live set (something new,
        # something resolved) refresh them — only if the engagement already has
        # stored results, and never at the cost of the run itself.
        if created or resolved:
            await _refresh_attack_paths(db, engagement_id)
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
