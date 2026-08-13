#!/usr/bin/env bash
# UC8 — UDP Service Exposure (probe use_case: uc_udp_service_exposure)
# UDP attack surface + amplification. Finds NTP monlist (123), DNS open
# recursion (53), memcached (11211), SNMP public (161), NetBIOS-NS (137), SSDP.
#
#   ./uc_udp_exposure.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "UDP service + amplification probes" udp_scanner
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no UDP rows)"); raise SystemExit
responded = [r for r in rows if r.get("status") in ("open", "observed")]
for r in sorted(rows, key=lambda x: x.get("port") or 0):
    d = r.get("data") or {}
    amp = ""
    if d.get("amplification") or d.get("monlist") or d.get("recursion"):
        amp = "  *** AMPLIFICATION / OPEN SERVICE ***"
    print(f"   {str(r.get('port')):<6}/udp {r.get('status'):<9} {r.get('evidence') or ''}{amp}")
print(f"   {'-'*50}\n   {len(responded)} responded / {len(rows)} probed")
PY
echo
