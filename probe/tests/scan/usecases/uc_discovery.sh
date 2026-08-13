#!/usr/bin/env bash
# UC1 — Network Discovery (probe use_case: uc_discovery_only)
# "What's alive here?" liveness + open TCP ports. Finds rogue/unknown hosts,
# shadow IT, live mobile devices (via ARP + randomized-MAC detection).
#
#   ./uc_discovery.sh 192.168.1.0/24
#   ./uc_discovery.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "Host discovery (liveness + ARP + mobile)" host_discovery
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
live = [r for r in rows if r["data"].get("alive")]
print(f"   {len(live)}/{len(rows)} ALIVE")
for r in sorted(live, key=lambda x: [int(o) for o in x['target'].split('.')]):
    d = r["data"]
    print(f"   {r['target']:<15} {str(d.get('method')):<8} {str(d.get('mac','-')):<18} {d.get('device_hint') or r.get('evidence','')[:40]}")
PY
echo

uc_run "Port scan (top TCP on the target)" port_scanner
uc_open "$UC_LAST"
