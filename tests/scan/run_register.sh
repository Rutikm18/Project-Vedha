#!/usr/bin/env bash
# run_register.sh — execute the TEST_REGISTER scenarios and PRINT results.
#
# One command runs the whole suite (foundation + every scanner + pipeline) and
# prints a PASS/FAIL line per scenario plus a final tally. It's the executable
# version of TEST_REGISTER.md.
#
# USAGE:
#   ./run_register.sh                 # core: foundation + scanners + pipeline
#   ./run_register.sh intensity       # add the T1..T5 sweep per scanner (slow)
#   ./run_register.sh all             # everything
#   ./run_register.sh foundation      # just one section (also: scanners pipeline)
#
# Targets come from these env vars (defaults match the register); override e.g.:
#   WIN=10.0.0.5 RTR=10.0.0.1 ./run_register.sh
#
# NOTE: snmp_scan (~18s) and mcp_ai_scan (~1-3min) are genuinely slow. web_scan
#       is run at T2 because T3's 3s timeout misses slow web servers (a known
#       finding). Real scans over WiFi — total core run is a few minutes.
set -u
cd "$(dirname "$0")"

WIN="${WIN:-192.168.1.68}"       # Windows box (135/445/3389)
RTR="${RTR:-192.168.1.254}"      # router / gateway (22/80/443)
NET="${NET:-192.168.1.64/27}"    # small CIDR covering the live hosts

SECTIONS="${*:-foundation scanners pipeline}"
[ "$SECTIONS" = "all" ] && SECTIONS="foundation scanners pipeline intensity"

PASS=0; FAIL=0; FAILED=()
if [ -t 1 ]; then G=$'\e[32m'; R=$'\e[31m'; B=$'\e[1m'; D=$'\e[2m'; Z=$'\e[0m'
else G=""; R=""; B=""; D=""; Z=""; fi

hdr()  { printf '\n%s================ %s ================%s\n' "$B" "$1" "$Z"; }
tally(){ if [ "$1" -eq 0 ]; then PASS=$((PASS+1))
         else FAIL=$((FAIL+1)); FAILED+=("$2"); fi; }
mark() { if [ "$1" -eq 0 ]; then printf '  %sPASS%s %s\n' "$G" "$Z" "$2"
         else printf '  %sFAIL%s %s (exit %s)\n' "$R" "$Z" "$2" "$1"; fi; }

# quiet assertion: run hidden, PASS if exit == want
want() {
    local id="$1" desc="$2" want="$3"; shift 3
    "$@" >/tmp/rr.out 2>&1; local rc=$?
    tally "$([ "$rc" = "$want" ] && echo 0 || echo 1)" "$id $desc"
    if [ "$rc" = "$want" ]; then printf '  %sPASS%s %-4s %s\n' "$G" "$Z" "$id" "$desc"
    else printf '  %sFAIL%s %-4s %s (got exit %s, want %s)\n' "$R" "$Z" "$id" "$desc" "$rc" "$want"; fi
}

# visible scanner run: echo the command, show its output, tally on exit code.
scan() {
    local id="$1" desc="$2"; shift 2
    printf '\n%s$ %s%s\n' "$D" "$*" "$Z"
    "$@"; local rc=$?
    tally "$rc" "$id $desc"; mark "$rc" "$id $desc"
}

run_foundation() {
    hdr "0. FOUNDATION / harness wiring"
    want F1 "smoke test"                 0 ./smoke.sh
    want F2 "help text"                  0 ./run.sh --help
    want F3 "too few args -> usage"      1 ./run.sh "$RTR"
    want F4 "bad profile rejected"       2 ./run.sh "$RTR" T9 port_scan
    want F5 "bad scanner rejected"       2 ./run.sh "$RTR" T3 bogus_scan
    rm -rf .live
    want F8 "live w/o discovery errors"  3 ./run.sh live T3 port_scan
}

run_scanners() {
    hdr "1. PER-SCANNER SMOKE @ T3 (web_scan @ T2 — slow-server timeout)"
    scan S1  "host_discovery"  ./run.sh "$NET" T3 host_discovery
    scan S2  "port_scan"       ./run.sh "$WIN" T3 port_scan
    scan S3  "service_banner"  ./run.sh "$RTR" T3 service_banner
    scan S4  "tls_scan"        ./run.sh "$RTR" T3 tls_scan
    scan S5  "web_scan"        ./run.sh "$RTR" T2 web_scan
    scan S6  "udp_scan"        ./run.sh "$RTR" T3 udp_scan
    scan S7  "smb_scan"        ./run.sh "$WIN" T3 smb_scan
    scan S8  "snmp_scan (~18s)" ./run.sh "$RTR" T3 snmp_scan
    scan S9  "db_scan"         ./run.sh "$WIN" T3 db_scan
    scan S10 "mcp_ai_scan (slow)" ./run.sh "$RTR" T3 mcp_ai_scan
    scan S11 "mass_scan"       ./run.sh "$WIN" T3 mass_scan
}

run_pipeline() {
    hdr "3. DISCOVERY-DRIVEN PIPELINE (live mode)"
    scan P1 "discover + save"  ./run.sh "$NET" T3 host_discovery
    printf '\n%s$ cat .live/hosts.txt%s\n' "$D" "$Z"; cat .live/hosts.txt 2>/dev/null
    scan P4 "live service_banner" ./run.sh live T3 service_banner
    scan P5 "live chain"       ./run.sh live T3 port_scan service_banner
}

run_intensity() {
    hdr "2. INTENSITY MATRIX (T1..T5 per scanner — SLOW)"
    scan I-hd "host_discovery all" ./run.sh "$WIN" all host_discovery
    scan I-ps "port_scan all"      ./run.sh "$WIN" all port_scan
    scan I-sb "service_banner all" ./run.sh "$RTR" all service_banner
    scan I-tl "tls_scan all"       ./run.sh "$RTR" all tls_scan
    scan I-ms "mass_scan all"      ./run.sh "$WIN" all mass_scan
}

echo "targets: WIN=$WIN  RTR=$RTR  NET=$NET"
echo "sections: $SECTIONS"
for s in $SECTIONS; do
    case "$s" in
        foundation) run_foundation ;;
        scanners)   run_scanners ;;
        pipeline)   run_pipeline ;;
        intensity)  run_intensity ;;
        *) echo "unknown section: $s (foundation|scanners|pipeline|intensity|all)" >&2 ;;
    esac
done

hdr "RESULTS"
printf 'scenarios passed: %s%s%s   failed: %s%s%s\n' "$G" "$PASS" "$Z" "$R" "$FAIL" "$Z"
if [ "${#FAILED[@]}" -gt 0 ]; then
    for f in "${FAILED[@]}"; do printf '  %s!%s %s\n' "$R" "$Z" "$f"; done
fi
[ "$FAIL" -eq 0 ]
