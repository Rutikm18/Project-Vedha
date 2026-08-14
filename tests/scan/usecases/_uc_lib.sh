#!/usr/bin/env bash
# _uc_lib.sh — shared helpers for the network-VA use-case scripts.
#
# Each use-case script runs the SAME scanner modules the probe runs in the field
# (python3 -m scanner.<module>), against one target, and prints the ACTUAL
# findings so you can review them by hand. This is the manual, per-use-case
# mirror of the probe's funnel: host_discovery -> port_scan -> service_banner ->
# deep_scan (tls/web/smb/db/snmp/udp/mcp_ai).
#
# Source this, then:
#   uc_init "$1"                       # sets TARGET + a scope allowlist
#   uc_run "Web fingerprint" web_scanner -p "$UC_WEB_PORTS"
#   uc_findings "$UC_LAST"             # generic pretty-print
#
# Tunables (env): RATE (300) CONC (100) TOUT (4) UC_OUT (/tmp/vedha_uc)

# tests/scan/usecases -> probe/
PROBE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PY="${PROBE_PYTHON:-python3}"
UC_OUT="${UC_OUT:-/tmp/vedha_uc}"
mkdir -p "$UC_OUT"

if [ -t 1 ]; then B=$'\e[1m'; D=$'\e[2m'; C=$'\e[36m'; Z=$'\e[0m'
else B=""; D=""; C=""; Z=""; fi

# Deep-scan port sets — copied from the scanner modules' DEFAULT_*_PORTS so the
# manual runs match the probe exactly.
UC_WEB_PORTS="80,443,8080,8443,8000,8888,9000,9200"
UC_TLS_PORTS="443,8443,993,995,465,636,989,990,5986"
UC_DB_PORTS="3306,33060,5432,1433,6379,27017,1521"
UC_AI_PORTS="11434,8000,8080,5000,3000,1234,8001,7860,11435"
UC_IOT_PORTS="23,554,1883,8883,9100,37777,80,8080"
UC_BANNER_PORTS="21,22,23,25,53,80,110,143,443,445,3306,3389,5432,6379,8080,8443"

uc_init() {
    TARGET="${1:?usage: $(basename "$0") <target-ip-or-CIDR>   e.g. 192.168.1.10 or 192.168.1.0/24}"
    SCOPE="$UC_OUT/scope.txt"
    printf '%s\n' "$TARGET" > "$SCOPE"
    printf '%starget:%s %s   %sscope:%s %s\n\n' "$B" "$Z" "$TARGET" "$D" "$Z" "$SCOPE"
}

# uc_run <label> <module> [extra scanner args...]
# Runs the REAL scanner module; result JSONL -> $UC_LAST. Prints the command.
uc_run() {
    local label="$1" mod="$2"; shift 2
    UC_LAST="$UC_OUT/${mod}.jsonl"
    printf '%s── %s%s  %s(scanner.%s)%s\n' "$B" "$label" "$Z" "$C" "$mod" "$Z"
    printf '%s$ python3 -m scanner.%s -t %s -s scope --timeout %s %s%s\n' \
        "$D" "$mod" "$TARGET" "${TOUT:-4}" "$*" "$Z"
    ( cd "$PROBE_DIR" && "$PY" -m "scanner.$mod" \
        -t "$TARGET" -s "$SCOPE" \
        --rate "${RATE:-300}" --concurrency "${CONC:-100}" --timeout "${TOUT:-4}" \
        "$@" -o "$UC_LAST" ) >/dev/null 2>&1
    local rc=$?
    [ "$rc" -ne 0 ] && printf '   %s(scanner exited %s)%s\n' "$D" "$rc" "$Z"
}

# uc_findings <jsonl> — generic pretty-print of every row (port/status/evidence).
uc_findings() {
    "$PY" - "$1" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
if not rows:
    print("   (no findings)"); raise SystemExit
for r in rows:
    p = r.get("port"); pr = r.get("proto") or ""
    port = f"{p}/{pr}" if p is not None else "-"
    print(f"   {r.get('target'):<15} {port:<10} {r.get('status'):<9} {r.get('evidence') or ''}")
print(f"   {'-'*60}\n   {len(rows)} row(s)")
PY
    echo
}

# uc_open <jsonl> — just the OPEN ports (for discovery/port scans).
uc_open() {
    "$PY" - "$1" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
opn = sorted((r for r in rows if r.get("status") == "open"), key=lambda x: x.get("port") or 0)
if not opn:
    print("   (no open ports)"); raise SystemExit
for r in opn:
    print(f"   {r.get('target'):<15} {str(r.get('port')):<7} OPEN   {r.get('evidence') or ''}")
print(f"   {len(opn)} open")
PY
    echo
}
