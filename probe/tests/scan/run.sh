#!/usr/bin/env bash
# run.sh — single-command driver for the per-scanner intensity test harness.
#
# USAGE:
#   ./run.sh <target> <profile> [scanner ...]
#
#   target    IP, CIDR, hostname, or range (e.g. 192.168.1.10, 10.0.0.0/24).
#             Use '-'    to fall back to TARGET from expected.env.
#             Use 'live' to scan only the hosts a previous host_discovery run
#                        marked alive (saved in .live/), one host at a time.
#   profile   T1 | T2 | T3 | T4 | T5 | all
#   scanner   zero or more of:
#               host_discovery port_scan service_banner tls_scan web_scan
#               udp_scan smb_scan snmp_scan db_scan mcp_ai_scan mass_scan
#             (default: all, in that order)
#
# EXAMPLES:
#   ./run.sh 192.168.1.10 T3                    # every scanner, normal intensity
#   ./run.sh 192.168.1.10 T3 port_scan          # just one scanner (test one by one)
#   ./run.sh 192.168.1.0/24 all                 # every scanner, T1..T5 sweep
#   ./run.sh 192.168.1.10 T4 port_scan tls_scan # a subset at aggressive timing
#   ./run.sh - T3                               # use TARGET from expected.env
#
#   # discovery-driven pipeline (discover once, then scan only live hosts):
#   ./run.sh 192.168.1.0/24 T3 host_discovery   # discovers + saves live hosts
#   ./run.sh live T3 service_banner             # scans ONLY those hosts, 1-by-1
#   ./run.sh live T3 port_scan service_banner   # a chain over the live set
#
# EXPECT_* values in expected.env drive the findings assertions. When an
# EXPECT_* is unset for a scanner, that scanner is only checked for "ran clean"
# (no crash) — a scanner finding nothing is not a harness failure.
#
# NOTE: T1/T2 over a whole CIDR is intentionally slow (paranoid rate limiting).
#       Use a single host for T1/T2, or T3+ for CIDRs.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/_profiles.sh"
. "$HERE/_assert.sh"

ALL_SCANNERS="host_discovery port_scan service_banner tls_scan web_scan \
udp_scan smb_scan snmp_scan db_scan mcp_ai_scan mass_scan"

usage() { sed -n '2,33p' "$0"; exit "${1:-0}"; }

case "${1:-}" in -h|--help|help) usage 0;; esac
[ "$#" -lt 2 ] && usage 1

TARGET_ARG="$1"; PROFILE_ARG="$2"; shift 2
SCANNERS="$*"; [ -z "$SCANNERS" ] && SCANNERS="$ALL_SCANNERS"

TGT_OVERRIDE=""; [ "$TARGET_ARG" != "-" ] && TGT_OVERRIDE="$TARGET_ARG"

# Validate scanner names up front so a typo fails loudly (exit 2) instead of
# silently scanning nothing.
for _sc in $SCANNERS; do
    case " $ALL_SCANNERS " in
        *" $_sc "*) ;;
        *) echo "unknown scanner: $_sc (see --help)" >&2; exit 2 ;;
    esac
done

harness_init "$PROFILE_ARG" "$TGT_OVERRIDE"

first_port() { echo "${1%%,*}"; }   # "445,139" -> "445"

# ports_for_target — per-host EXPECT_PORTS_<ip> if set, else the shared
# EXPECT_PORTS. Used for scan BREADTH (what to point a scanner at).
ports_for_target() {
    local hv="EXPECT_PORTS_${TARGET//./_}"
    echo "${!hv:-${EXPECT_PORTS:-}}"
}

# host_expect_ports — per-host EXPECT_PORTS_<ip> ONLY (no global fallback).
# Used as the ASSERTION basis: we only claim a specific port/banner when we
# have a per-host expectation for it — never from the host-agnostic global list
# (which would wrongly fail every phone/IoT device that has no services).
host_expect_ports() {
    local hv="EXPECT_PORTS_${TARGET//./_}"
    echo "${!hv:-}"
}

# check_finding — like check, but a no-op in 'live' mode. Live hosts are
# heterogeneous (phones, routers, PCs), so global EXPECT_* findings assertions
# don't apply per-host; we only verify those scanners 'ran clean' there.
check_finding() {
    [ "${LIVE_MODE:-0}" = 1 ] && return 0
    check "$@"
}

# run_one <scanner> <level> — run one scanner at one intensity and assert.
run_one() {
    local sc="$1" lvl="$2"
    case "$sc" in
        host_discovery)
            run_scanner host_discovery "$lvl"
            check "ran clean" assert_run_clean
            check "host reachable" assert_host_alive
            print_alive_hosts
            save_live_hosts        # persist for later 'run.sh live ...'
            ;;
        port_scan)
            # Full default top-port scan, then assert the per-host expected
            # ports (EXPECT_PORTS_<ip>) are among the open ones. Hosts with no
            # per-host expectation (phones, unknown devices) are only checked
            # for 'ran clean'.
            local he; he="$(host_expect_ports)"
            run_scanner port_scanner "$lvl"
            check "ran clean" assert_run_clean
            if [ -n "$he" ]; then
                local p; for p in ${he//,/ }; do
                    check "port $p open" assert_port_open "$p"; done
            fi
            ;;
        service_banner)
            # Breadth: prefer the host's discovered-open ports (chained from
            # discovery), then per-host expected, then a default banner set.
            # Assert a banner only when we KNOW this host has an open port
            # (discovered-open OR per-host expected) — never for silent devices.
            local disc he; disc="$(open_ports_for "$TARGET")"; he="$(host_expect_ports)"
            local sb="${disc:-${he:-${EXPECT_PORTS:-21,22,25,80,443,3306,3389,8080,8443}}}"
            run_scanner service_banner "$lvl" -p "$sb"
            check "ran clean" assert_run_clean
            [ -n "$disc$he" ] && check "banner(s) reported" assert_scanner_reported
            ;;
        tls_scan)
            run_scanner tls_scanner "$lvl" ${EXPECT_TLS:+-p $EXPECT_TLS}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_TLS:-}" ] && check_finding "tls reported" assert_scanner_reported
            ;;
        web_scan)
            run_scanner web_scanner "$lvl" ${EXPECT_WEB:+-p $EXPECT_WEB}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_WEB:-}" ] && check_finding "web reported" assert_scanner_reported
            ;;
        udp_scan)
            run_scanner udp_scanner "$lvl" ${EXPECT_UDP:+-p $EXPECT_UDP}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_UDP:-}" ] && check_finding "udp reported" assert_scanner_reported
            ;;
        smb_scan)
            run_scanner smb_scanner "$lvl" ${EXPECT_SMB:+--port $(first_port "$EXPECT_SMB")}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_SMB:-}" ] && check_finding "smb reported" assert_scanner_reported
            ;;
        snmp_scan)
            run_scanner snmp_scanner "$lvl" ${EXPECT_SNMP:+--port $(first_port "$EXPECT_SNMP")}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_SNMP:-}" ] && check_finding "snmp reported" assert_scanner_reported
            ;;
        db_scan)
            run_scanner db_scanner "$lvl" ${EXPECT_DB:+-p $EXPECT_DB}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_DB:-}" ] && check_finding "db reported" assert_scanner_reported
            ;;
        mcp_ai_scan)
            run_scanner mcp_ai_scanner "$lvl" ${EXPECT_AI:+-p $EXPECT_AI}
            check "ran clean" assert_run_clean
            [ -n "${EXPECT_AI:-}" ] && check_finding "ai endpoint reported" assert_scanner_reported
            ;;
        mass_scan)
            local he; he="$(host_expect_ports)"
            local mp; mp="$(ports_for_target)"
            run_scanner mass_scan "$lvl" -p "${mp:-1-1000}" --fallback
            check "ran clean" assert_run_clean
            if [ -n "$he" ]; then
                local p; for p in ${he//,/ }; do
                    check "port $p open" assert_port_open "$p"; done
            fi
            ;;
        *) echo "unknown scanner: $sc (see --help)" >&2; return 2 ;;
    esac
    echo
}

for lvl in $LEVELS; do
    resolve_profile "$lvl"
    echo "################  intensity $PROFILE_LABEL  ################"
    echo
    for h in "${HOSTS[@]}"; do
        TARGET="$h"                       # run_scanner + ports_for_target read $TARGET
        [ "${#HOSTS[@]}" -gt 1 ] && echo "==================  host $h  =================="
        for sc in $SCANNERS; do run_one "$sc" "$lvl"; done
    done
done

finish
