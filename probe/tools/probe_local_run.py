#!/usr/bin/env python3
"""
probe_local_run.py — drive the probe's REAL pipeline (workflow.run_engagement)
locally, one use case at a time, without the manager. For LAN validation.

Run from the probe/ directory:

    export PYTHONPATH="$PWD"
    echo "192.168.1.0/24" > /tmp/s.txt         # scope allowlist (must contain the target)
    .venv/bin/python3 tools/probe_local_run.py <target> [profile] [stage] [service_filter]

  profile        : it | iot | ot                       (default: it)
  stage          : host_discovery | port_scan | service_banner | deep_scan
                   ('-' or omitted = full deep_scan)
  service_filter : comma list to isolate ONE deep branch,
                   e.g. tls | web | smb | snmp | db | mcp_ai | udp

Examples:
    tools/probe_local_run.py 192.168.1.254 it host_discovery   # UC1 liveness
    tools/probe_local_run.py 192.168.1.254 it service_banner   # UC3 + banner + os_fingerprint
    tools/probe_local_run.py 192.168.1.254 it deep_scan        # UC4 full pipeline
    tools/probe_local_run.py 192.168.1.254 it deep_scan tls    # only the TLS branch
    tools/probe_local_run.py 192.168.1.254 iot deep_scan       # IoT profile

This is a LOCAL driver for the same engine the production probe runs; it does not
talk to the manager. For the manager-connected flow use `./probe validate ...`.
"""
import asyncio
import json
import sys

from scanner.scanner_base import ScopeGuard
from workflow.workflow_engine import run_engagement

SCOPE_FILE = "/tmp/s.txt"
# A small port set keeps demo runs fast. Set to None to scan the full profile catalog.
PORT_OVERRIDE = [22, 80, 443]


def summarize(a) -> dict:
    if a is None:
        return {"note": "target not in scope / no asset produced"}
    return {
        "alive": a.last_seen_alive is not None,
        "open_ports": sorted(a.open_ports.keys()),
        "services": {p: (v.get("service") or v.get("product")) for p, v in a.services.items()},
        "os_fact": a.os_fact,               # from os_fingerprint (Gate 4b)
        "enrichment": a.enrichment,         # from service_enum   (Gate 5a)
        "tls_ports": sorted(a.tls_facts.keys()),
        "web_ports": sorted(a.web_facts.keys()),
        "smb": bool(a.smb_state),
        "snmp_ports": sorted(a.snmp_state.keys()),
        "db_ports": sorted(a.db_facts.keys()),
    }


async def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = sys.argv[1]
    profile = sys.argv[2] if len(sys.argv) > 2 else "it"
    stage = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] not in ("-", "") else None
    svc = set(sys.argv[4].split(",")) if len(sys.argv) > 4 and sys.argv[4] else None

    scope = ScopeGuard.from_file(SCOPE_FILE)
    kw = dict(profile=profile, timeout=3.0, disc_timeout=1.5)
    if PORT_OVERRIDE is not None:
        kw["port_override"] = PORT_OVERRIDE
    if stage:
        kw["stage_ceiling"] = stage
    if svc:
        kw["service_filter"] = svc

    assets = await run_engagement([target], scope, **kw)
    print(json.dumps(summarize(assets.get(target)), default=str, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
