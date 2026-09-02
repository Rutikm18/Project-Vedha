"""
explain_plan.py — "which scanners will run against this host, and WHY?"

    python -m agent.explain_plan <target> [--scope FILE] [--profile it|iot|ot]
                                [--services a,b] [--stage <ceiling>] [--dry-run]

The engine decides each deep-scan branch from a gate (gates.py) plus the dynamic
router (router.py). Those decisions are correct but invisible: a completed run
tells you what ran, never what was CONSIDERED and rejected, so "why did the probe
touch that port?" and "why didn't it check X?" both had to be answered by reading
source. This prints the decision table instead.

  --dry-run   Decide from the funnel ONLY (host discovery -> ports -> banners) and
              print the branch table WITHOUT running any deep scanner. This is the
              honest way to audit what a manager job would do to a host: it costs
              the funnel's probes and nothing more.

  (default)   Run the full engagement, then print the same table alongside the
              execution trace, so planned-vs-actual can be compared directly.

Nothing here re-implements a decision: it calls the SAME gates.py / router.py /
branches.py the engine calls, so this can never drift from real behaviour.
"""
from __future__ import annotations

import argparse
import asyncio
import sys

from scanner.scanner_base import ScopeGuard, expand_targets

from workflow.branches import BRANCHES
from workflow.cache import WorkflowCache
from workflow.execution import ExecutionTrace, planned_components
from workflow.gates import PROFILE_DEEP_BRANCHES, PROFILE_PORTS, gate_5_branch_eligible
from workflow.modes import STAGE_ORDER, STAGE_SERVICE_BANNER
from workflow.router import route_branches
from workflow.workflow_engine import run_engagement

_TICK, _CROSS = "RUN ", "skip"


def _why(spec, asset, profile: str, service_filter, routed: dict) -> tuple[bool, str]:
    """Recreate this branch's decision and say, in one line, what drove it."""
    allowed = PROFILE_DEEP_BRANCHES.get(profile, set())
    if spec.branch not in allowed:
        return False, f"profile '{profile}' does not allow this branch"
    if service_filter is not None and spec.branch not in service_filter:
        return False, "excluded by --services filter"

    dynamic = ({p for p, b in routed.items() if spec.dynamic in b}
               if spec.dynamic else set())
    eligible = gate_5_branch_eligible(spec.branch, asset, profile, service_filter,
                                      bool(dynamic))
    open_ports = asset.open_ports_for_deep_scan()

    if spec.host_level:
        return eligible, ("host-level branch; runs once per live host"
                          if eligible else "host not confirmed alive")
    if spec.datagram:
        return eligible, ("datagram probe on %s — needs liveness only, NOT an open "
                          "TCP port (a UDP service is invisible to a TCP port scan)"
                          % ",".join(str(p) for p in sorted(spec.ports)))

    hits = sorted(open_ports & spec.ports)
    if hits and dynamic:
        return eligible, (f"open port(s) {hits} in its table; router also routed "
                          f"{sorted(dynamic)} from observed banners")
    if hits:
        return eligible, f"open port(s) {hits} match its port table"
    if dynamic:
        return eligible, (f"NO port-table match; routed purely by observed banner "
                          f"content on {sorted(dynamic)}")
    return eligible, (f"no open port in its table "
                      f"{sorted(spec.ports)[:8]}{'...' if len(spec.ports) > 8 else ''}")


def _print_table(asset, profile, service_filter) -> None:
    routed = route_branches(asset)
    open_ports = sorted(asset.open_ports_for_deep_scan())
    print(f"\nhost {asset.host}")
    print(f"  alive        : {asset.last_seen_alive is not None}")
    print(f"  open TCP     : {open_ports or 'none'}")
    if asset.os_fact:
        print(f"  os           : {asset.os_fact.get('os_release') or asset.os_fact.get('os_guess')}")
    if routed:
        print("  router       : " + "; ".join(
            f"{p}->{'/'.join(sorted(b))}" for p, b in sorted(routed.items())))
    else:
        print("  router       : no branch routed from banner content")

    print(f"\n  {'branch':<10} {'component':<16} {'':<4} why")
    print("  " + "-" * 88)
    will_run = 0
    for spec in BRANCHES:
        ok, why = _why(spec, asset, profile, service_filter, routed)
        will_run += ok
        print(f"  {spec.branch:<10} {spec.component:<16} {_TICK if ok else _CROSS} {why}")
    print("  " + "-" * 88)
    print(f"  {will_run} of {len(BRANCHES)} deep branches would run "
          f"({len(BRANCHES) - will_run} skipped)\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m agent.explain_plan",
                                 description="Show which scanners run for a host, and why.")
    ap.add_argument("target")
    ap.add_argument("-s", "--scope", default=None,
                    help="authorization allowlist file (default: a /32 of the target)")
    ap.add_argument("--profile", default="it", choices=sorted(PROFILE_PORTS))
    ap.add_argument("--services", default=None,
                    help="comma-separated branch filter, e.g. 'tls,web'")
    ap.add_argument("--stage", default=None, choices=STAGE_ORDER,
                    help="stage ceiling (default: full deep scan)")
    ap.add_argument("--ports", default=None,
                    help="explicit TCP ports for the funnel (default: profile catalog)")
    ap.add_argument("--dry-run", action="store_true",
                    help="stop after banners and only PRINT the branch table")
    args = ap.parse_args(argv)

    service_filter = ({s.strip() for s in args.services.split(",") if s.strip()}
                      if args.services else None)
    scope = (ScopeGuard.from_file(args.scope) if args.scope
             else ScopeGuard.from_list([args.target]))
    targets = expand_targets([args.target])
    ports = None
    if args.ports:
        from scanner.scanner_base import parse_ports
        ports = parse_ports(args.ports)

    ceiling = STAGE_SERVICE_BANNER if args.dry_run else args.stage
    print(f"planned components: "
          f"{planned_components(args.profile, service_filter=service_filter, stop_after_banner=False, ssh_enabled=False, windows_enabled=False, stage_ceiling=args.stage)}")

    cache = WorkflowCache()
    trace = None if args.dry_run else ExecutionTrace(planned_components(
        args.profile, service_filter=service_filter, stop_after_banner=False,
        ssh_enabled=False, windows_enabled=False, stage_ceiling=args.stage))
    assets = asyncio.run(run_engagement(
        targets, scope, profile=args.profile, service_filter=service_filter,
        stage_ceiling=ceiling, port_override=ports, cache=cache, trace=trace))

    for host in targets:
        asset = assets.get(host)
        if asset is not None:
            _print_table(asset, args.profile, service_filter)

    if trace is not None:
        print("  actual execution trace")
        print("  " + "-" * 88)
        for run in trace.as_list():
            print(f"  {run['id']:<16} {run['status']:<10} "
                  f"targets={run.get('attempted_targets', 0)} "
                  f"facts={run.get('fact_count', 0)} "
                  f"errors={run.get('error_count', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
