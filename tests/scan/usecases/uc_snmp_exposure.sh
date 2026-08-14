#!/usr/bin/env bash
# UC7 — SNMP Exposure (probe use_case: uc_snmp_exposure)
# Read-only SNMP sysDescr with common community strings. Finds default/weak
# read communities (public/private) on routers, printers, switches, appliances.
#
#   ./uc_snmp_exposure.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "SNMP community check (public/private/...)" snmp_scanner --port 161
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no SNMP reply)"); raise SystemExit
for r in rows:
    d = r.get("data") or {}
    print(f"   {r.get('target')} :161  {r.get('status')}  {r.get('evidence')}")
    if d.get("community"):
        print(f"      *** WEAK COMMUNITY '{d.get('community')}' ACCEPTED ***")
    if d.get("sysDescr") or d.get("sys_descr"):
        print(f"      sysDescr: {d.get('sysDescr') or d.get('sys_descr')}")
PY
echo
