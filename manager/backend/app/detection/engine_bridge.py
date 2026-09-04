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
from app.discovery.finding_translator import _resolve_asset, _find_open_duplicate
from app.detection.attack_paths import attack_path_findings
from app.detection.prioritization import _posture_risk_on_manager_scale
from app.detection.resolution import build_coverage, evaluate_resolutions
from app.ai.verification_graph import run_verification
from app.config import get_settings

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
    _log_ingest_health."""
    # accepted_facts falls back to the raw list on every path where no ingest
    # verdict exists (engine missing, older engine, hard failure). Without a
    # verdict we cannot say a fact is bad, and silently disabling attack-path
    # correlation would trade one blind spot for another.
    empty_meta: dict = {"coverage": {}, "verdicts": {}, "ingest": {},
                        "accepted_facts": list(facts or [])}
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
                    "accepted_facts": _accepted(facts, rejected)}
            _log_ingest_health(census, len(cve) + len(posture))
            return cve, posture, meta
        except ImportError:                          # older engine: CVE-only
            from pipeline import run_pipeline  # type: ignore
            findings, _ = run_pipeline([tmp])
            return [f.to_dict() for f in findings], [], empty_meta
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
            meta = {"coverage": summarize_traces(traces), "verdicts": verdicts,
                    "ingest": census,
                    "accepted_facts": _accepted(facts, rejected)}
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


async def _find_remediated_match(db, engagement_id, asset_id, title):
    """A remediated finding with the same (engagement, asset, title) — the
    regression candidate. Mirrors _find_open_duplicate but for the closed set."""
    q = select(Finding).where(
        Finding.engagement_id == engagement_id,
        Finding.title == title,
        Finding.status == FindingStatus.remediated,
    )
    q = q.where(Finding.asset_id == asset_id) if asset_id else q.where(Finding.asset_id.is_(None))
    return (await db.execute(q.limit(1))).scalar_one_or_none()


def _posture_description(p: dict) -> str | None:
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
                                    cache: dict | None = None) -> tuple[int, int]:
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
            asset = await _resolve_asset(db, engagement_id, p.get("asset_ip"), cache=cache)
            asset_id = asset.id if asset else None

            dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
            if dup is not None:
                dup.evidence = p
                dup.last_seen = now
                dup.detection_run_id = run_id
                dup.resolution_miss_count = 0
                dup.risk_score = Decimal(str(manager_risk)) if manager_risk is not None else None
                touched.append(dup)
                reaffirmed += 1
                continue

            regressed = await _find_remediated_match(db, engagement_id, asset_id, title)
            if regressed is not None:
                _apply_regression_reopen(regressed, run_id, now)
                regressed.evidence = {**(regressed.evidence or {}), **p, "regression": True}
                regressed.risk_score = Decimal(str(manager_risk)) if manager_risk is not None else None
                touched.append(regressed)
                reaffirmed += 1
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
                detection_run_id=run_id,
                detected_db_version=db_version,
            )
            db.add(f)
            touched.append(f)
            created += 1
        except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
            logger.warning("posture_finding.create_failed",
                           rule_id=p.get("rule_id"), error=str(exc))
    return created, reaffirmed


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
    """ip → {device_role, role_detail} from already-promoted assets, so a prior
    device_inventory scan amplifies today's correlation (Track B2)."""
    rows = (await db.execute(
        select(Asset.ip_address, Asset.device_role, Asset.role_detail).where(
            Asset.engagement_id == engagement_id,
            Asset.device_role.isnot(None),
        )
    )).all()
    return {
        ip: {"device_role": role, "role_detail": detail}
        for ip, role, detail in rows if ip
    }


async def _persist_attack_paths(
    db: AsyncSession, engagement_id: uuid.UUID, run, facts: list[dict], now,
    cache: dict | None = None,
) -> int:
    """Correlate composite attack paths from the run's facts and persist them as
    Finding rows (deduped by title, reaffirmed across runs). Returns NEW count."""
    device_roles = await _engagement_device_roles(db, engagement_id)
    created = 0
    for d in attack_path_findings(facts, device_roles):
        try:
            asset = await _resolve_asset(db, engagement_id, d.get("target"), cache=cache)
            asset_id = asset.id if asset else None
            title = d["title"][:500]
            evidence = {
                "rule_id": d["rule_id"], "correlation": True,
                "remediation": d.get("remediation"),
                "mitre_techniques": d.get("mitre_techniques"),
                **(d.get("evidence") or {}),
            }
            dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
            if dup is not None:
                dup.severity = d["severity"]     # re-amplify if the role changed
                dup.evidence = evidence
                dup.last_seen = now
                dup.detection_run_id = run.id
                dup.resolution_miss_count = 0
                continue
            db.add(Finding(
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
                detection_run_id=run.id,
            ))
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

    # Serialise this engagement's detection before reading anything — see
    # _lock_engagement_for_detection. Held until this transaction ends.
    await _lock_engagement_for_detection(db, engagement_id)

    now = datetime.now(timezone.utc)
    db_version, db_fetched = _vuln_db_meta()

    # Open the run first, so every finding created below can reference run.id and
    # the run row is the single provenance record for this detection execution.
    # Stamp a lease: if this worker dies mid-detection, the run stays RUNNING past
    # lease_expires_at and the outbox reaper fails it precisely (vs guessing from age).
    run = DetectionRun(
        engagement_id=engagement_id,
        scan_result_id=scan_result_id,
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
        asset_cache: dict = {}
        # ONE full-detection pass over the raw facts → BOTH the CVE/version track
        # and the posture/config-exposure track (the verified scanners' findings),
        # plus the detection-trace coverage roll-up (which rules were blind/clean/
        # not-assessed) so a non-finding can explain itself.
        cve_dicts, posture_dicts, detect_meta = detect_all_from_facts_traced(facts)
        for d in cve_dicts:
            try:
                cve = d.get("cve_id") or "finding"
                title = f"{cve} — {d.get('cpe', '').split(':')[4] if d.get('cpe') else ''}".strip(" —")[:500]
                asset = await _resolve_asset(db, engagement_id, d.get("asset_ip"), cache=asset_cache)
                asset_id = asset.id if asset else None

                dup = await _find_open_duplicate(db, engagement_id, asset_id, title)
                if dup is not None:
                    # Same issue still present → reaffirm: advance last_seen and
                    # point it at this run (first_seen is preserved).
                    dup.evidence = d
                    dup.last_seen = now
                    dup.detection_run_id = run.id
                    dup.resolution_miss_count = 0   # re-observed → out of the resolution window
                    touched.append(dup)
                    reaffirmed += 1
                    continue

                regressed = await _find_remediated_match(db, engagement_id, asset_id, title)
                if regressed is not None:
                    # An auto/manually-resolved issue is back → reopen the SAME row
                    # and flag the regression (its history is preserved).
                    _apply_regression_reopen(regressed, run.id, now)
                    regressed.evidence = {**(regressed.evidence or {}), **d, "regression": True}
                    touched.append(regressed)
                    reaffirmed += 1
                    continue

                state = d.get("state")
                new_finding = Finding(
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
                    detected_db_version=db_version,
                )
                db.add(new_finding)
                touched.append(new_finding)
                created += 1
            except Exception as exc:  # noqa: BLE001 — one bad finding must not sink the batch
                logger.warning("detection_finding.create_failed", error=str(exc))

        # ── Posture / config-exposure track (the VERIFIED scanners' findings) ──
        # SMBv1, RDP-without-NLA, deprecated TLS, exposed RPC, UDP amplifiers — the
        # weaknesses the CVE loop cannot see because they are configuration, not a
        # vulnerable version. Same dedup/regression lifecycle, ready for the portal.
        try:
            p_created, p_reaffirmed = await _persist_posture_findings(
                db, engagement_id, run.id, now, posture_dicts, touched, db_version,
                cache=asset_cache)
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
                cache=asset_cache)
            created += corr_new
        except Exception as exc:  # noqa: BLE001 — correlation must not sink the run
            logger.warning("detection_run.correlation_failed", error=str(exc))

        # Coverage ledger + coverage-gated auto-resolution (Phase 0/1). Best-effort:
        # never let resolution failure sink an otherwise-good detection run.
        resolved = 0
        try:
            coverage = build_coverage(result.get("scanner_runs"), facts)
            resolved = await evaluate_resolutions(db, engagement_id, run, coverage, now)
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

        run.status = RUN_COMPLETED
        run.finished_at = datetime.now(timezone.utc)
        run.findings_new = created
        run.findings_reaffirmed = reaffirmed
        run.findings_current = int(current or 0)
        await db.flush()
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
