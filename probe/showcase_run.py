#!/usr/bin/env python3
"""showcase_run.py — thin CLI over the REAL probe engine for demos.

Calls agent.engine.run_scan() exactly the way the agent's task_runner does, so
scope enforcement, exclusions, the funnel, and every scanner behave identically
to a manager-issued job — no manager required.

Usage:
    showcase_run.py --list
    showcase_run.py --use-case uc_full_assessment --targets 127.0.0.1 --scope 127.0.0.1/32
    showcase_run.py --scan-type udp_scan --targets 127.0.0.1 --scope 127.0.0.1/32 --exclude 127.0.0.2/32
    showcase_run.py ... --raw     # dump the full JSON result bundle
"""
from __future__ import annotations

import argparse
import json
import sys

from agent.engine import run_scan, CAPABILITIES
from agent.use_cases import USE_CASES, resolve

# ── small ANSI helpers (no dependency) ───────────────────────────────────────
def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if sys.stdout.isatty() else s

BOLD = lambda s: _c("1", s)
DIM = lambda s: _c("2", s)
GREEN = lambda s: _c("32", s)
RED = lambda s: _c("31", s)
YELLOW = lambda s: _c("33", s)
CYAN = lambda s: _c("36", s)


def _split(csv: str | None) -> list[str]:
    return [x.strip() for x in (csv or "").split(",") if x.strip()]


def list_use_cases() -> None:
    print(BOLD("\nUse-case library (probe/agent/use_cases.py):\n"))
    for uc_id, uc in USE_CASES.items():
        st, prof = uc["scan_type"], uc["profile"]
        print(f"  {CYAN(uc_id):<40} {DIM(f'[{st}/{prof}]')}")
        print(f"      {uc['display_name']} — {uc['description']}")
    print(BOLD("\nRaw scan types (CAPABILITIES):"))
    print("  " + ", ".join(CAPABILITIES) + "\n")


def _print_summary(result: dict, targets, scope, excludes) -> None:
    ok = result.get("ok")
    outcome = result.get("outcome", "?")
    stats = result.get("run_stats") or {}
    enforced = stats.get("scope_enforced") or {}

    print(BOLD("\n" + "═" * 66))
    print(BOLD(f" SCAN: {result.get('scan_type')}  "
               f"profile={result.get('profile')}  "
               f"outcome={GREEN(outcome) if ok else RED(outcome)}"))
    print(BOLD("═" * 66))

    # Scope provenance — proves exactly what the probe was allowed to touch.
    print(BOLD("\n Scope enforced (defense-in-depth boundary):"))
    print(f"   allow      : {enforced.get('allow', scope)}")
    print(f"   exclude    : {enforced.get('exclude', excludes) or '—'}")
    print(f"   requested  : {enforced.get('targets_requested', targets)}")
    print(f"   authorized : {GREEN(str(enforced.get('targets_authorized', [])))}")

    if result.get("error"):
        print(RED(f"\n  ⚠ {result['error']}  ({result.get('error_code')})"))
        if result.get("remediation"):
            print(DIM(f"    → {result['remediation']}"))

    print(BOLD("\n Run stats:"))
    print(f"   hosts={stats.get('host_count', 0)}  "
          f"open_ports={stats.get('open_ports', 0)}  "
          f"facts={stats.get('fact_count', 0)}  "
          f"scanners_run={stats.get('scanners_run', [])}")

    facts = result.get("facts") or []
    if facts:
        print(BOLD(f"\n Facts ({len(facts)}):"))
        for f in facts:
            status = f.get("status")
            colour = GREEN if status == "open" else (YELLOW if status in ("observed", "filtered") else DIM)
            head = (f"   {f.get('scanner'):<16} {f.get('target')}"
                    f":{f.get('port')}/{f.get('proto')} {colour(str(status))}")
            print(head)
            data = f.get("data") or {}
            if data:
                # print the interesting fields compactly, one per line
                for k, v in data.items():
                    if k in ("reply_hex_head", "all_headers"):
                        continue
                    print(DIM(f"        {k} = {v}"))
    else:
        print(DIM("\n   (no service facts — host may be quiet, or scope refused the scan)"))
    print()


def main() -> int:
    p = argparse.ArgumentParser(description="Probe showcase runner (real engine).")
    p.add_argument("--list", action="store_true", help="list use-cases + scan types and exit")
    p.add_argument("--use-case", help="use_case_id from the library")
    p.add_argument("--scan-type", help="raw scan_type (see --list)")
    p.add_argument("--targets", help="comma-separated targets (IP/CIDR/host)")
    p.add_argument("--scope", help="comma-separated authoritative allowlist CIDRs")
    p.add_argument("--exclude", default="", help="comma-separated excluded CIDRs")
    p.add_argument("--profile", default=None, help="it | iot | ot (overrides use-case default)")
    p.add_argument("--raw", action="store_true", help="print the full JSON result bundle")
    args = p.parse_args()

    if args.list:
        list_use_cases()
        return 0

    if not args.targets or not args.scope:
        p.error("--targets and --scope are required (or use --list)")

    targets = _split(args.targets)
    scope = _split(args.scope)
    excludes = _split(args.exclude)

    # Resolve scan_type + profile from the use-case, or take them directly.
    if args.use_case:
        try:
            scan_type, profile = resolve(args.use_case, None, {})
        except ValueError as exc:
            print(RED(f"Unknown use-case: {exc}"))
            return 2
    elif args.scan_type:
        scan_type, profile = args.scan_type, args.profile or "it"
    else:
        p.error("provide --use-case or --scan-type")

    if args.profile:
        profile = args.profile

    print(DIM(f"→ engine.run_scan(scan_type={scan_type!r}, profile={profile!r}, "
              f"targets={targets}, scope={scope}, exclude={excludes})"))

    result = run_scan(
        scan_type,
        {"targets": targets, "profile": profile},
        use_case_id=args.use_case,
        validated_scope=scope,
        validated_excludes=excludes,
    )

    if args.raw:
        print(json.dumps(result, indent=2, default=str))
    else:
        _print_summary(result, targets, scope, excludes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
