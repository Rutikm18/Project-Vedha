#!/usr/bin/env bash
# UC11 — Full Assessment (probe use_case: uc_full_assessment)
# The complete probe funnel against one target:
#   host_discovery -> port_scan -> service_banner -> deep_scan
#   (tls, web, smb, db, snmp, udp, mcp_ai)
# This is what the probe runs end-to-end for a full engagement.
#
#   ./uc_full_assessment.sh 192.168.1.10
#
# Point it at a SINGLE host (deep scans on a whole /24 are slow).
set -u
. "$(dirname "$0")/_uc_lib.sh"
uc_init "${1:-}"

uc_run "1. Host discovery" host_discovery
uc_findings "$UC_LAST"

uc_run "2. Port scan" port_scanner
uc_open "$UC_LAST"

uc_run "3. Service banners" service_banner -p "$UC_BANNER_PORTS"
uc_findings "$UC_LAST"

echo "${B}===== DEEP SCAN BRANCHES =====${Z}"
uc_run "4. TLS/cert"   tls_scanner   -p "$UC_TLS_PORTS";  uc_findings "$UC_LAST"
uc_run "5. Web"        web_scanner   -p "$UC_WEB_PORTS";  uc_findings "$UC_LAST"
uc_run "6. SMB"        smb_scanner   --port 445;          uc_findings "$UC_LAST"
uc_run "7. Database"   db_scanner    -p "$UC_DB_PORTS";   uc_findings "$UC_LAST"
uc_run "8. SNMP"       snmp_scanner  --port 161;          uc_findings "$UC_LAST"
uc_run "9. UDP"        udp_scanner;                        uc_findings "$UC_LAST"
uc_run "10. AI/MCP"    mcp_ai_scanner -p "$UC_AI_PORTS";  uc_findings "$UC_LAST"

echo "${B}full assessment complete — raw JSONL in $UC_OUT/${Z}"
