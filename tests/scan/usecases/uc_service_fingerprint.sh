#!/usr/bin/env bash
# UC2 — Service Fingerprint (probe use_case: uc_iot_device_survey style / service_fingerprint)
# Open ports + version banners. Finds exposed services and version disclosure
# (e.g. old OpenSSH/Dropbear, exposed Telnet, HTTP server strings).
#
#   ./uc_service_fingerprint.sh 192.168.1.10
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "Port scan (find open ports)" port_scanner
uc_open "$UC_LAST"

uc_run "Service banners (version strings)" service_banner -p "$UC_BANNER_PORTS"
"$PY" - "$UC_LAST" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows: print("   (no banners)"); raise SystemExit
for r in sorted(rows, key=lambda x: x.get("port") or 0):
    d = r.get("data") or {}
    fl = d.get("first_line") or d.get("banner") or r.get("evidence")
    fl = (str(fl) or "").replace("\r", " ").replace("\n", " ")[:80]
    print(f"   port {str(r.get('port')):<6} {fl}")
PY
echo
