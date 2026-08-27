"""
cli.py — the two operator verbs for the offline CVE layer.

    python -m cve.cli ingest    --db vuln.db [--kev --epss --nvd] [--resume] [--max-pages N]
    python -m cve.cli correlate --db vuln.db --facts findings.jsonl --out cve_findings.jsonl

`ingest` builds/refreshes the mirror from the public feeds (see ingest.py).
`correlate` reads the probe's fact stream (one JSON object per line — the same
records the scanners emit) and writes prioritized CVE findings to a SEPARATE
stream, never mixed with the probe's own findings.jsonl. The probe emits no CVE
claim; this is the manager-side interpretation step.
"""

from __future__ import annotations

import argparse
import json
import sys

from .correlator import correlate, mirror_age_note, summarize
from .online import enrich_findings
from .vulndb import VulnDB
from .weakness_map import correlate_weaknesses, missing_from_mirror, WEAKNESS_CVES


def _read_facts(path: str):
    """Yield fact dicts from a JSONL file ('-' = stdin). Blank/comment/bad lines
    are skipped so a partial scan stream still correlates."""
    fh = sys.stdin if path == "-" else open(path, "r", encoding="utf-8")
    try:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
    finally:
        if fh is not sys.stdin:
            fh.close()


def cmd_ingest(args) -> int:
    from .ingest import ingest_all
    # If no feed flag is given, refresh them all.
    any_flag = args.nvd or args.kev or args.epss
    nvd = args.nvd or not any_flag
    kev = args.kev or not any_flag
    epss = args.epss or not any_flag
    db = VulnDB(args.db, create=True)
    try:
        # Progress to stderr so stdout stays a clean, machine-readable result line.
        counts = ingest_all(db, nvd=nvd, kev=kev, epss=epss,
                            api_key=args.api_key, resume=not args.no_resume,
                            max_pages=args.max_pages,
                            log=lambda m: print(m, file=sys.stderr))
    finally:
        db.close()
    print(f"ingest complete: {counts}", file=sys.stderr)
    print(json.dumps({"ingested": counts}))
    return 0


def _merge_findings(*groups):
    """Merge CVE-finding lists, dedup by (cve_id, target, port), highest risk first.
    The CPE path and the weakness path can reach the SAME CVE by different routes;
    the first (higher-risk, since inputs are pre-sorted) wins the slot."""
    seen: set[tuple] = set()
    out = []
    for group in groups:
        for f in group:
            key = (f.cve_id, f.target, f.port)
            if key in seen:
                continue
            seen.add(key)
            out.append(f)
    return sorted(out, key=lambda x: x.risk_score, reverse=True)


def cmd_correlate(args) -> int:
    db = VulnDB(args.db)
    try:
        age_note = mirror_age_note(db)
        facts = list(_read_facts(args.facts))
        exposed = set(args.exposed.split(",")) if args.exposed else None
        # Two complementary routes to a CVE: version-range CPE matches, and the
        # curated weakness->canonical-CVE map (SMBv1->EternalBlue, etc.) driven by
        # the probe's detect-stage findings in the same stream.
        cpe_findings = correlate(facts, db, exposed_targets=exposed)
        weakness_findings = ([] if args.no_weakness_map else
                             correlate_weaknesses(facts, db, exposed_targets=exposed))
        findings = _merge_findings(cpe_findings, weakness_findings)
    finally:
        db.close()
    print(age_note, file=sys.stderr)

    # OPT-IN live enrichment: fill mirror gaps / flag stale scores from NVD, and
    # (with a key) note public exploits from Vulners. Fail-open — an offline box
    # or a failed lookup leaves the offline result untouched.
    if args.online:
        enrich_findings(findings, api_key=args.online_api_key,
                        vulners_key=args.vulners_key,
                        only_missing=not args.online_all,
                        log=lambda m: print(m, file=sys.stderr))
        findings.sort(key=lambda x: x.risk_score, reverse=True)

    out = sys.stdout if args.out == "-" else open(args.out, "w", encoding="utf-8")
    try:
        for f in findings:
            out.write(json.dumps(f.to_dict()) + "\n")
    finally:
        if out is not sys.stdout:
            out.close()
    print(f"correlate: {summarize(findings)}", file=sys.stderr)
    return 0


def cmd_status(args) -> int:
    """Verify the offline mirror: feed counts, freshness, and — critically — whether
    every canonical CVE the weakness map depends on is actually present. A stale or
    partial mirror silently misses new CVEs and drops enrichment for known mappings;
    this is the pre-flight check an operator runs before trusting a correlation."""
    db = VulnDB(args.db)
    try:
        counts = db.counts()
        age_note = mirror_age_note(db)
        missing = missing_from_mirror(db)
        wanted = sorted({a.cve_id for m in WEAKNESS_CVES.values() for a in m.assocs})
    finally:
        db.close()
    report = {
        "db": args.db,
        "counts": counts,
        "mirror_age": age_note,
        "stale": age_note.startswith("WARNING"),
        "weakness_map_rules": len(WEAKNESS_CVES),
        "weakness_map_cves": wanted,
        "weakness_map_missing_from_mirror": missing,
        "healthy": (not age_note.startswith("WARNING")
                    and counts.get("cve", 0) > 0 and not missing),
    }
    print(age_note, file=sys.stderr)
    if missing:
        print(f"WARNING: {len(missing)} weakness-map CVE(s) absent from mirror: "
              f"{', '.join(missing)} — re-run `cve.cli ingest`.", file=sys.stderr)
    print(json.dumps(report, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cve", description="Offline CVE correlation")
    sub = p.add_subparsers(dest="cmd", required=True)

    ing = sub.add_parser("ingest", help="build/refresh the offline vuln mirror")
    ing.add_argument("--db", required=True, help="SQLite mirror path")
    ing.add_argument("--nvd", action="store_true", help="pull NVD (default: all feeds)")
    ing.add_argument("--kev", action="store_true", help="pull CISA KEV")
    ing.add_argument("--epss", action="store_true", help="pull EPSS")
    ing.add_argument("--api-key", default=None, help="NVD API key (raises the rate limit)")
    ing.add_argument("--no-resume", action="store_true",
                     help="restart NVD from index 0 instead of resuming")
    ing.add_argument("--max-pages", type=int, default=None,
                     help="cap NVD pages (smoke test); run stays resumable")
    ing.set_defaults(func=cmd_ingest)

    cor = sub.add_parser("correlate", help="facts.jsonl -> cve_findings.jsonl")
    cor.add_argument("--db", required=True, help="SQLite mirror path")
    cor.add_argument("--facts", required=True, help="fact stream JSONL ('-' = stdin)")
    cor.add_argument("--out", default="-", help="output JSONL ('-' = stdout)")
    cor.add_argument("--exposed", default=None,
                     help="comma-separated internet-exposed targets (risk boost)")
    cor.add_argument("--no-weakness-map", action="store_true",
                     help="skip the weakness->canonical-CVE map (CPE matches only)")
    cor.add_argument("--online", action="store_true",
                     help="opt-in: enrich from live NVD/Vulners (default: fully offline)")
    cor.add_argument("--online-all", action="store_true",
                     help="with --online, also cross-check CVEs the mirror scored "
                          "(default: only fill mirror gaps)")
    cor.add_argument("--online-api-key", default=None,
                     help="NVD API key for the live lookup (raises the rate limit)")
    cor.add_argument("--vulners-key", default=None,
                     help="Vulners API key — enables public-exploit lookup")
    cor.set_defaults(func=cmd_correlate)

    st = sub.add_parser("status", help="verify mirror freshness + weakness-map coverage")
    st.add_argument("--db", required=True, help="SQLite mirror path")
    st.set_defaults(func=cmd_status)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
