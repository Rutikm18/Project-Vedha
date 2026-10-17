"""
pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.

  ingest          -> Assets (per-host fact aggregation)
  normalize       -> CPECandidates per Fact (rule-based; AI-assisted fallback
                     on a miss, only when use_ai_assist=True — see Phase 2)
  match           -> raw Findings per candidate, against the pinned snapshot
  dedup           -> collapse same (asset, cve, cpe)
  suppress        -> omit inferred findings a better authoritative source negates,
                     while retaining an auditable decision record
  correlate       -> composite cross-fact findings (SMBv1 + missing hotfix)
  enrich          -> CVSS/EPSS/KEV + priority tier

Deterministic and offline at every step except the explicit, separate
update_snapshot.py sync, and the optional Phase 2 AI-assist fallback (which
itself fails closed to the same deterministic behavior when unavailable —
see ai_normalizer.py's module docstring for the hard rules that keep it
from ever becoming a hard dependency or a CVE source).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ai_normalizer import AIClient, AINormalizerCache, extract_raw_text, propose_candidates
from correlate import (
    SuppressionRecord,
    correlate_smb_patch,
    dedup_findings,
    suppress_negated_with_audit,
)
from cpe_normalizer import CPECandidate, normalize
from enrichment import enrich_finding
from enrichment_db import EpssDB, KevDB, load_epss, load_kev
from ingest import IngestResult, ingest_files
from matcher import MATCHER_REVISION, match_candidate
from models import Finding
from exploitability import apply_to_findings as apply_exploitability
from posture_rules import (PostureFinding, detect_all as detect_posture_all,
                           detect_all_traced, summarize_traces, verdict_for_rule)
from verifier import deception_score, verify
from vuln_db import VulnDB, load_snapshot


# match_basis values that are product presence, not a version-range vulnerability:
# kept out of the customer-facing `cve` set (see run_full_detection).
PRODUCT_PRESENCE_BASES = frozenset({"range-open", "range-distro", "range-branch"})


def run_pipeline(jsonl_paths: list[str | Path], vuln_db: VulnDB | None = None,
                 kev_db: KevDB | None = None, epss_db: EpssDB | None = None,
                 exposure: dict[str, dict] | None = None,
                 use_ai_assist: bool = False, ai_client: AIClient | None = None,
                 ai_cache: AINormalizerCache | None = None,
                 suppression_audit: list[SuppressionRecord] | None = None,
                 candidates_out: dict[str, list[CPECandidate]] | None = None,
                 ) -> tuple[list[Finding], IngestResult]:
    """exposure: optional {asset_ip: {"internet_facing": bool, "auth_enforced":
    bool}} — exposure context this pipeline cannot derive from scan facts
    alone (see enrichment.py's docstring); caller-supplied, never guessed.

    use_ai_assist/ai_client: Phase 2 fallback. Off by default — the
    pipeline's core behavior never changes unless explicitly opted into.
    When on, any Fact the rule-based normalizer misses on is retried
    through ai_normalizer.py before being given up on; a missing ai_client
    or any AI-side failure silently yields the same result as
    use_ai_assist=False for that fact (see ai_normalizer.py's hard rules).

    candidates_out: optional caller-supplied dict this fills with the SAME
    per-asset CPE candidates computed internally (asset_ip -> list[CPECandidate]),
    so a caller that needs them (run_full_detection's identified_products) does
    not have to re-derive or re-normalize anything. Additive-only: the return
    tuple is unchanged.
    """
    vuln_db = vuln_db or load_snapshot()
    kev_db = kev_db or load_kev()
    epss_db = epss_db or load_epss()
    exposure = exposure or {}
    if use_ai_assist and ai_client is not None:
        ai_cache = ai_cache or AINormalizerCache()

    ingest_result = ingest_files(jsonl_paths)

    candidates_by_asset: dict[str, list[CPECandidate]] = {}
    all_findings: list[Finding] = []
    for ip, asset in ingest_result.assets.items():
        candidates: list[CPECandidate] = []
        for fact in asset.facts:
            fact_candidates = normalize(fact)
            if not fact_candidates and use_ai_assist and ai_client is not None:
                raw_text = extract_raw_text(fact)
                if raw_text:
                    fact_candidates = propose_candidates(fact, raw_text, ai_client, cache=ai_cache)
            for c in fact_candidates:
                c.port, c.proto = fact.port, fact.proto
            candidates.extend(fact_candidates)
        candidates_by_asset[ip] = candidates
        for c in candidates:
            all_findings.extend(match_candidate(ip, c, vuln_db))

    if candidates_out is not None:
        candidates_out.update(candidates_by_asset)

    all_findings = dedup_findings(all_findings)
    all_findings, suppressed = suppress_negated_with_audit(all_findings, candidates_by_asset)
    if suppression_audit is not None:
        suppression_audit.extend(suppressed)

    for ip, asset in ingest_result.assets.items():
        composite = correlate_smb_patch(asset)
        if composite is not None:
            all_findings.append(composite)
    all_findings = dedup_findings(all_findings)  # composite finding could
                                                  # re-collide on re-runs

    # Per-asset deception score (Phase 3): an implausible vendor spread or
    # contradictory OS signals on one host is a honeypot/tarpit tell.
    deception_by_asset: dict[str, float] = {}
    for ip, cands in candidates_by_asset.items():
        distinct = len({(c.vendor, c.product) for c in cands})
        facts = ingest_result.assets[ip].facts if ip in ingest_result.assets else []
        scanners_seen = {fct.scanner for fct in facts}
        contradictory_os = ("windows_inventory" in scanners_seen
                            and "ssh_inventory" in scanners_seen)
        deception_by_asset[ip] = deception_score(distinct, contradictory_os)

    for f in all_findings:
        exp = exposure.get(f.asset_ip, {})
        f.internet_facing = exp.get("internet_facing")
        f.auth_enforced = exp.get("auth_enforced")
        enrich_finding(f, vuln_db, kev_db, epss_db)
        # Phase 3 — every finding passes through the verifier exactly once,
        # AFTER auth_enforced/exposure is set (verify reads it). Anti-FP:
        # only ever lowers confidence / downgrades state, never raises.
        verify(f, deception=deception_by_asset.get(f.asset_ip, 0.0))

    return all_findings, ingest_result


def identified_products_from(
    candidates_by_asset: dict[str, list[CPECandidate]],
) -> dict[str, list[str]]:
    """{asset_ip: sorted distinct "vendor:product"} — every product the CVE track
    identified on each asset, read from CPE 2.3 fields 3 and 4 of the candidate's
    own cpe23() (the same string matcher.py stamps on a CVE finding's `cpe`), so a
    finding and this map always agree on naming. Lower-cased. An asset with no
    identified product gets no entry."""
    out: dict[str, list[str]] = {}
    for ip, cands in candidates_by_asset.items():
        products: set[str] = set()
        for c in cands:
            parts = c.cpe23().split(":")
            if len(parts) < 5:
                continue
            vendor, product = parts[3].lower(), parts[4].lower()
            if vendor and product and "*" not in (vendor, product):
                products.add(f"{vendor}:{product}")
        if products:
            out[ip] = sorted(products)
    return out


def _os_by_asset(ingest_result: IngestResult) -> dict[str, dict]:
    """{asset_ip: {os_guess, os_release, os_build}} from each host's OS facts, so
    exploitability can gate a KEV link by the real OS (gap #5). Picks the most
    authoritative OS fact per host — a higher confidence, and an explicit SMB-NTLM
    build outranks a bare TTL family guess. Assets with no OS signal are omitted
    (exploitability then fails open for them)."""
    out: dict[str, dict] = {}
    for ip, asset in ingest_result.assets.items():
        best: dict | None = None
        best_rank = -1.0
        for f in asset.facts:
            d = f.data if isinstance(f.data, dict) else {}
            guess = d.get("os_guess") or d.get("os_release")
            build = d.get("os_build")
            if not guess and not isinstance(build, int):
                continue
            rank = float(d.get("confidence") or 0.0) + (1.0 if isinstance(build, int) else 0.0)
            if rank > best_rank:
                best_rank = rank
                best = {"os_guess": d.get("os_guess"),
                        "os_release": d.get("os_release"),
                        "os_build": build if isinstance(build, int) else None}
        if best:
            out[ip] = best
    return out


def host_os_summary(ingest_result: IngestResult) -> dict[str, dict]:
    """{asset_ip: {os, os_version, source}} — the best OS identification each host's
    facts support, for the manager's asset record (testing-round gap 7: the report's
    asset table read "not recorded" although the scan had identified the OS).

    Preference: the distribution release read from the SSH banner ("Ubuntu 16.04",
    the same parser the end-of-life rule uses) > a Windows release from SMB > the
    TTL-family guess. Assets with no OS signal are omitted."""
    from os_release_intel import release_from_ssh_fact
    out: dict[str, dict] = {}
    for ip, asset in ingest_result.assets.items():
        best, best_rank = None, -1.0
        for f in asset.facts:
            d = f.data if isinstance(f.data, dict) else {}
            if f.scanner == "ssh_scan":
                rel = release_from_ssh_fact(d)
                if rel:
                    name, _, ver = rel["os_release"].partition(" ")
                    cand, rank = {"os": name, "os_version": ver or None,
                                  "source": "ssh_banner"}, 3.0
                else:
                    continue
            elif isinstance(d.get("os_release"), str) and d["os_release"].strip():
                release = d["os_release"].strip()
                family = "Windows" if release.lower().startswith("windows") else release
                cand = {"os": family[:100], "os_version": release[:100], "source": f.scanner}
                rank = 2.0 + float(d.get("os_confidence") or d.get("confidence") or 0.0)
            elif (isinstance(d.get("os_guess"), str) and d["os_guess"].strip()
                  and d["os_guess"].strip().lower() != "unknown"):
                cand = {"os": d["os_guess"].strip()[:100], "os_version": None,
                        "source": f.scanner}
                rank = float(d.get("confidence") or 0.0)
            else:
                continue
            if rank > best_rank:
                best, best_rank = cand, rank
        if best:
            out[ip] = best
    return out


def run_full_detection(jsonl_paths: list[str | Path], vuln_db: VulnDB | None = None,
                       kev_db: KevDB | None = None, epss_db: EpssDB | None = None,
                       exposure: dict[str, dict] | None = None,
                       **kwargs) -> dict[str, Any]:
    """Unified detection over one set of ingested facts: the CVE track
    (version→CVE, may be empty when no vuln_db is pinned) AND the posture track
    (config/exposure vulnerabilities from the validated scanners). Shares the SAME
    exposure context so both use one risk model, and returns both finding sets plus
    the ingest result — the whole vulnerability picture, not half of it.

    This is what a full network VA should call: the trusted scanners' facts land
    here and the manager applies its strong detection to them centrally.
    """
    suppression_audit: list[SuppressionRecord] = []
    # Resolve the exploitation snapshots HERE, not only inside run_pipeline: the
    # posture track needs them too, and leaving them None meant every posture
    # finding silently skipped enrichment while the CVE track was enriched fine.
    kev_db = kev_db or load_kev()
    epss_db = epss_db or load_epss()
    # Filled by run_pipeline with the SAME CPE candidates it computed internally —
    # the raw material for identified_products below, so nothing here re-normalizes
    # a fact that normalize() already turned into vendor/product once.
    candidates_by_asset: dict[str, list[CPECandidate]] = {}
    cve_findings, ingest_result = run_pipeline(
        jsonl_paths, vuln_db=vuln_db, kev_db=kev_db, epss_db=epss_db,
        exposure=exposure, suppression_audit=suppression_audit,
        candidates_out=candidates_by_asset, **kwargs)
    # Traced posture run: findings identical to detect_posture_all, PLUS a per-rule
    # evaluation trace so a non-finding can explain itself (drift vs clean vs
    # not-assessed). This is what makes "checked and clean" distinguishable from
    # "never actually checked".
    posture_findings, posture_traces = detect_all_traced(ingest_result, exposure=exposure)
    # Exploitability: join CISA KEV + FIRST EPSS onto the POSTURE track too. The
    # CVE track has had this since enrichment.py; posture findings — which are
    # most of what a Windows estate actually returns — were ranked by a static
    # severity constant with no notion of what attackers are using today.
    posture_findings = apply_exploitability(
        posture_findings, kev_db, epss_db, os_by_asset=_os_by_asset(ingest_result))
    posture_coverage = summarize_traces(posture_traces)
    posture_verdicts = {}
    for rid in sorted({t.rule_id for t in posture_traces}):
        verdict, reasons = verdict_for_rule(posture_traces, rid)
        posture_verdicts[rid] = {"verdict": verdict, "reasons": reasons}

    # Gap #4: a `range-open` finding matched only an open-ended [introduced,
    # unbounded) range from an inferred (banner) source — it carries no version
    # discrimination (it would match every version of the product), so it is
    # product-presence, NOT a version-range vulnerability. Keep it OUT of the
    # customer-facing `cve` set (which the backend persists one-for-one as
    # findings) so a banner-identified host no longer floods with zero-signal
    # CVEs. It is not discarded: it is returned under `cve_product_presence`
    # (and counted) so the signal remains traceable and a future UI can surface
    # it as a low-priority "product present — verify patch level" rollup.
    # The same holds for `range-distro`: a banner that names a backporting distro
    # build (Ubuntu, RHEL, "(Debian)" with no package revision) cannot show which
    # fixes are in, so its version matches are product presence too.
    product_presence = [f for f in cve_findings if f.match_basis in PRODUCT_PRESENCE_BASES]
    cve_findings = [f for f in cve_findings if f.match_basis not in PRODUCT_PRESENCE_BASES]
    return {
        "cve": cve_findings,
        "cve_product_presence": product_presence,
        "posture": posture_findings,
        "posture_traces": [t.to_dict() for t in posture_traces],
        "posture_coverage": posture_coverage,
        "posture_verdicts": posture_verdicts,
        "suppression_audit": [record.to_dict() for record in suppression_audit],
        # What was re-identified, per asset: the evidence a CVE finding needs
        # before its absence from this run can count as clean.
        "identified_products": identified_products_from(candidates_by_asset),
        "matcher_revision": MATCHER_REVISION,
        "host_os": host_os_summary(ingest_result),
        "ingest": ingest_result,
        "counts": {
            "cve": len(cve_findings),
            "cve_product_presence": len(product_presence),
            "cve_suppressed": len(suppression_audit),
            "posture": len(posture_findings),
            "posture_confirmed": sum(1 for f in posture_findings if f.state == "confirmed"),
            "posture_blind_rules": posture_coverage.get("rules_blind", 0),
            "assets": len(ingest_result.assets),
        },
    }


def ab_evaluate(jsonl_paths: list[str | Path], ai_client: AIClient, **kwargs) -> dict:
    """Phase 2 exit criteria: recall gain from AI assist, with zero precision
    regression. Runs the SAME input through the pipeline twice — once
    rule-based-only (the control), once with AI assist on — and reports the
    diff. "Zero precision regression" is checked structurally, not just
    measured: every finding gained ONLY exists with AI assist on (recall_gain
    is a pure addition, never a removal-and-replacement) and every one of
    them is state=suspected (ai_normalizer.py's candidates are never
    source_confidence=authoritative, so matcher.py can never mark them
    confirmed — see matcher.py's rule) — a regression would mean either
    invariant broke, not just a number changing.
    """
    baseline, _ = run_pipeline(jsonl_paths, use_ai_assist=False, **kwargs)
    with_ai, _ = run_pipeline(jsonl_paths, use_ai_assist=True, ai_client=ai_client, **kwargs)

    baseline_ids = {f.finding_id for f in baseline}
    with_ai_ids = {f.finding_id for f in with_ai}
    gained = with_ai_ids - baseline_ids
    lost = baseline_ids - with_ai_ids  # any non-empty set here IS a regression

    gained_findings = [f for f in with_ai if f.finding_id in gained]
    non_suspected_ai = [f for f in gained_findings if f.state.value != "suspected"]

    return {
        "baseline_count": len(baseline),
        "with_ai_count": len(with_ai),
        "recall_gain": len(gained),
        "lost_findings": len(lost),  # must be 0 — AI assist should only add
        "precision_regression": bool(lost) or bool(non_suspected_ai),
        "gained_finding_ids": sorted(gained),
        "non_suspected_ai_findings": [f.finding_id for f in non_suspected_ai],
    }
