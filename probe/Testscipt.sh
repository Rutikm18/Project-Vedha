#!/usr/bin/env bash
#
# Testscipt.sh — probe scanner accuracy harness
#
# Runs the full manual accuracy guide in one shot: sets up known fixtures,
# snapshots ground truth, runs every scanner module, checks each result against
# the ground truth, and prints a PASS/FAIL table.
#
# USAGE:
#   cd "/Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/probe"
#   chmod +x Testscipt.sh
#   ./Testscipt.sh
#
# ROBUSTNESS (why this version is stronger):
#   * Scanner RESULTS (JSONL) come on stdout; LOGS + Python warnings come on
#     stderr. We now capture them SEPARATELY (.json vs .log) and every check
#     reads only the .json — so a "DeprecationWarning: ...TLSVersion..." line can
#     never be mistaken for a real TLS result. This was the #1 source of false
#     FAILs (grep matching a warning, not a finding).
#   * Port checks match the JSON field `"port": N` (+ status), not a bare number
#     that could collide with a timestamp.
#   * Open-port truth is decided by a real TCP connect (/dev/tcp) — the same
#     thing the scanner does — not by `lsof`, whose address filter misses a
#     service bound to `*`/`::1` (e.g. Homebrew MySQL). The expected-port set is
#     therefore DYNAMIC: 3306 is only required when MySQL is actually listening.
#
# Optional env vars:
#   ROUTER_IP     - LAN router IP for the UDP true-positive test (default: auto)
#   LAN_CIDR      - LAN scope for the OT passive test (default: auto)
#   RUN_OT_TEST   - "1" to attempt the OT passive test automatically (default 0)
#   SKIP_TEARDOWN - "1" to leave fixtures running after the run (default 0)
#
set -uo pipefail

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
FIXDIR="/tmp/vafix"
SCOPE_FILE="scope_test.txt"
RESULTS_DIR="./accuracy_test_results_$(date +%Y%m%d_%H%M%S)"
RUN_OT_TEST="${RUN_OT_TEST:-0}"
SKIP_TEARDOWN="${SKIP_TEARDOWN:-0}"

mkdir -p "$RESULTS_DIR"
SUMMARY_FILE="$RESULTS_DIR/SUMMARY.md"
: > "$SUMMARY_FILE"

declare -a ROWS=()

log()   { echo -e "\033[1;34m[*]\033[0m $*"; }
ok()    { echo -e "\033[1;32m[PASS]\033[0m $*"; }
bad()   { echo -e "\033[1;31m[FAIL]\033[0m $*"; }
warn()  { echo -e "\033[1;33m[WARN]\033[0m $*"; }

record() { # step, check, result(PASS/FAIL/INFO), note
  ROWS+=("$1|$2|$3|$4")
  if   [ "$3" = "PASS" ]; then ok  "$1 -- $2"
  elif [ "$3" = "FAIL" ]; then bad "$1 -- $2 ($4)"
  else warn "$1 -- $2 ($4)"; fi
}

# Run a scanner, capturing RESULTS (stdout, JSONL) and LOGS (stderr) separately.
run_and_save() { # name, outfile.json, command...
  local name="$1"; local outfile="$2"; shift 2
  local errlog="${outfile%.json}.log"
  log "Running: $*"
  "$@" > "$outfile" 2> "$errlog"
  local rc=$?
  echo "  -> results: $outfile   logs: $errlog   (exit $rc)"
  return $rc
}

# ── result predicates (operate ONLY on the JSONL results file) ──────────────
has_result() { grep -Eq '^[[:space:]]*\{' "$1" 2>/dev/null; }              # any JSON result line
has_open()   { grep -Eq '"status"[[:space:]]*:[[:space:]]*"open"' "$1" 2>/dev/null; }

# A result line for this port exists AND is status "open".
port_open() { # file, port
  grep -E "\"port\"[[:space:]]*:[[:space:]]*$2([,}[:space:]])" "$1" 2>/dev/null \
    | grep -Eq '"status"[[:space:]]*:[[:space:]]*"open"'
}
# The port appears as a "port": N field (used for cross-engine, where the
# status field name may differ between engines).
port_field() { # file, port
  grep -Eq "\"port\"[[:space:]]*:[[:space:]]*$2([,}[:space:]])" "$1" 2>/dev/null
}
# The port number appears as a standalone token (for human-formatted output
# like pipeline.py — avoids matching digits inside a timestamp).
port_token() { # file, port
  grep -Eq "(^|[^0-9])$2([^0-9]|$)" "$1" 2>/dev/null
}
# Real TCP connect — the ground truth for "is this port open", matching what the
# scanner itself does. Robust where lsof's address filter is not.
tcp_open() { # host, port
  ( exec 3<>"/dev/tcp/$1/$2" ) 2>/dev/null && { exec 3>&- 3<&- 2>/dev/null; return 0; }
  return 1
}

# ---------------------------------------------------------------------------
# Sanity check: are we in the probe directory?
# ---------------------------------------------------------------------------
if [ ! -d "./scanner" ] || [ ! -f "./pipeline.py" ]; then
  warn "Doesn't look like the probe directory (need ./scanner and ./pipeline.py)."
  warn "cd into the probe/ directory before running this script."
fi

# ---------------------------------------------------------------------------
# Teardown
# ---------------------------------------------------------------------------
teardown() {
  if [ "$SKIP_TEARDOWN" = "1" ]; then
    warn "SKIP_TEARDOWN=1 — leaving fixtures running. Clean up with:"
    echo "  pkill -f 'http.server 8080'; pkill -f '${FIXDIR}/banner.py'; pkill -f 'openssl s_server'; rm -rf ${FIXDIR} ${SCOPE_FILE}"
    return
  fi
  log "STEP 12 — Tearing down fixtures"
  pkill -f "http.server 8080" 2>/dev/null
  pkill -f "${FIXDIR}/banner.py" 2>/dev/null
  pkill -f "openssl s_server" 2>/dev/null
  rm -rf "${FIXDIR}" "${SCOPE_FILE}"
  echo "cleaned up"
}
trap teardown EXIT

# ---------------------------------------------------------------------------
# STEP 0 — fixtures + scope + ground truth
# ---------------------------------------------------------------------------
log "STEP 0 — Setting up fixtures and scope"

if [ -z "${LAN_CIDR:-}" ]; then
  IP_LOCAL=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || true)
  if [ -n "$IP_LOCAL" ]; then
    LAN_CIDR="$(echo "$IP_LOCAL" | awk -F. '{print $1"."$2"."$3".0/24"}')"
  else
    LAN_CIDR="172.18.30.0/24"
  fi
fi
if [ -z "${ROUTER_IP:-}" ]; then
  ROUTER_IP=$(route -n get default 2>/dev/null | awk '/gateway/{print $2}')
  [ -z "$ROUTER_IP" ] && ROUTER_IP="192.168.1.1"
fi
log "Using LAN_CIDR=${LAN_CIDR} ROUTER_IP=${ROUTER_IP}"

printf '127.0.0.1\n%s\n' "$LAN_CIDR" > "$SCOPE_FILE"

mkdir -p "$FIXDIR"
printf '<html><head><title>GROUND-TRUTH-PAGE</title></head><body>hi</body></html>' > "$FIXDIR/index.html"
( cd "$FIXDIR" && python3 -m http.server 8080 --bind 127.0.0.1 >"$FIXDIR/http.log" 2>&1 & )

openssl req -x509 -newkey rsa:2048 -keyout "$FIXDIR/k.pem" -out "$FIXDIR/c.pem" -days 1 -nodes -subj "/CN=localhost" 2>/dev/null
( openssl s_server -key "$FIXDIR/k.pem" -cert "$FIXDIR/c.pem" -accept 8443 -www >"$FIXDIR/tls.log" 2>&1 & )

cat > "$FIXDIR/banner.py" <<'PY'
import socketserver
class H(socketserver.BaseRequestHandler):
    def handle(self):
        try: self.request.sendall(b"GROUND-TRUTH-BANNER-1.0\r\n")
        except OSError: pass
class S(socketserver.ThreadingTCPServer): allow_reuse_address=True
S(("127.0.0.1",3389),H).serve_forever()
PY
( python3 "$FIXDIR/banner.py" >"$FIXDIR/banner.log" 2>&1 & )

sleep 2
echo "fixtures started"

log "Snapshotting ground truth independently"
GT_FILE="$RESULTS_DIR/00_ground_truth.txt"
{
  echo "== lsof listeners on 127.0.0.1 =="
  lsof -nP -iTCP@127.0.0.1 -sTCP:LISTEN 2>/dev/null | awk 'NR==1 || /127.0.0.1/{print $1, $9}'
  echo
  echo "== 8080 title =="
  curl -s http://127.0.0.1:8080/ | grep -o '<title>.*</title>'
  echo
  echo "== 8443 TLS protocol =="
  echo | openssl s_client -connect 127.0.0.1:8443 2>/dev/null | grep -i protocol
  echo
  echo "== 3389 banner =="
  (nc 127.0.0.1 3389 <<< "" | head -c 40; echo)
  echo
  echo "== mysql version (if installed) =="
  mysql --version 2>/dev/null || echo "(no local mysql client / not checked)"
} > "$GT_FILE" 2>&1
cat "$GT_FILE"

# Decide the TRUE open-port set by real TCP connect (not lsof / not assumptions).
# 3389/8080/8443 are our fixtures; 3306 is included only if MySQL is really up.
declare -a EXPECTED_PORTS=()
for p in 3306 3389 8080 8443; do
  if tcp_open 127.0.0.1 "$p"; then EXPECTED_PORTS+=("$p"); fi
done
MYSQL_UP=1; tcp_open 127.0.0.1 3306 || MYSQL_UP=0
log "Truly-open ports on 127.0.0.1 (by TCP connect): ${EXPECTED_PORTS[*]:-none}   (mysql_up=${MYSQL_UP})"

record "Step0" "Fixtures started + ground truth snapshotted" "INFO" "open=${EXPECTED_PORTS[*]:-none}; see $GT_FILE"

# ---------------------------------------------------------------------------
# STEP 1 — host_discovery
# ---------------------------------------------------------------------------
log "STEP 1 — host_discovery"
OUT="$RESULTS_DIR/01_host_discovery.json"
run_and_save host_discovery "$OUT" python3 -m scanner.host_discovery -t 127.0.0.1 -s "$SCOPE_FILE"
if grep -Eqi '"alive"[[:space:]]*:[[:space:]]*true' "$OUT" && grep -Eqi '"status"[[:space:]]*:[[:space:]]*"open"' "$OUT"; then
  record "Step1 host_discovery" "host reported alive/open" "PASS" ""
else
  record "Step1 host_discovery" "host reported alive/open" "FAIL" "check $OUT"
fi

# ---------------------------------------------------------------------------
# STEP 2 — port_scanner
# ---------------------------------------------------------------------------
log "STEP 2 — port_scanner"
OUT="$RESULTS_DIR/02_port_scanner.json"
run_and_save port_scanner "$OUT" python3 -m scanner.port_scanner -t 127.0.0.1 -s "$SCOPE_FILE"
MISSING=""
if [ "${#EXPECTED_PORTS[@]}" -gt 0 ]; then
  for p in "${EXPECTED_PORTS[@]}"; do port_open "$OUT" "$p" || MISSING="$MISSING $p"; done
fi
if [ -z "$MISSING" ]; then
  record "Step2 port_scanner" "all truly-open ports (${EXPECTED_PORTS[*]}) detected" "PASS" ""
else
  record "Step2 port_scanner" "all truly-open ports (${EXPECTED_PORTS[*]}) detected" "FAIL" "missing open:$MISSING (check $OUT)"
fi

OUT_NEG="$RESULTS_DIR/02b_port_scanner_negctrl.json"
run_and_save port_scanner_negctrl "$OUT_NEG" python3 -m scanner.port_scanner -t 127.0.0.1 -s "$SCOPE_FILE" -p 22
if ! port_open "$OUT_NEG" 22; then
  record "Step2 port_scanner" "negative control: closed port 22 not reported open" "PASS" ""
else
  record "Step2 port_scanner" "negative control: closed port 22 not reported open" "FAIL" "false positive, check $OUT_NEG"
fi

# ---------------------------------------------------------------------------
# STEP 3 — service_banner
# ---------------------------------------------------------------------------
log "STEP 3 — service_banner"
OUT="$RESULTS_DIR/03_service_banner.json"
run_and_save service_banner "$OUT" python3 -m scanner.service_banner -t 127.0.0.1 -s "$SCOPE_FILE" -p 3306,3389,8080,8443
if grep -q "GROUND-TRUTH-BANNER-1.0" "$OUT"; then
  record "Step3 service_banner" "3389 banner matches ground truth verbatim" "PASS" ""
else
  record "Step3 service_banner" "3389 banner matches ground truth verbatim" "FAIL" "check $OUT"
fi
if grep -qi "SimpleHTTP" "$OUT"; then
  record "Step3 service_banner" "8080 reports SimpleHTTP server header" "PASS" ""
else
  record "Step3 service_banner" "8080 reports SimpleHTTP server header" "FAIL" "check $OUT"
fi

# ---------------------------------------------------------------------------
# STEP 4 — tls_scanner
# ---------------------------------------------------------------------------
log "STEP 4 — tls_scanner"
OUT="$RESULTS_DIR/04_tls_scanner.json"
run_and_save tls_scanner "$OUT" python3 -m scanner.tls_scanner -t 127.0.0.1 -s "$SCOPE_FILE" -p 8443
# Positive: a real open TLS result on 8443 that accepted a modern TLS version.
if port_open "$OUT" 8443 && grep -Eqi 'TLSv1[_.]3|TLSv1[_.]2' "$OUT"; then
  GT_HAS_13=""; echo | openssl s_client -connect 127.0.0.1:8443 2>/dev/null | grep -qi '1\.3' && GT_HAS_13="1"
  if grep -Eqi 'TLSv1[_.]3' "$OUT" && [ -n "$GT_HAS_13" ]; then
    record "Step4 tls_scanner" "accepted TLSv1.3 matches openssl ground truth" "PASS" ""
  else
    record "Step4 tls_scanner" "accepted a modern TLS version on 8443" "PASS" "versions differ from openssl -- diff $OUT vs $GT_FILE"
  fi
else
  record "Step4 tls_scanner" "TLS negotiated on 8443" "FAIL" "no open TLS result, check $OUT"
fi

# Negative control: plain HTTP on 8080 must yield NO tls result line
# (logs/warnings on stderr are in the .log, never in the .json — so this is clean).
OUT_NEG="$RESULTS_DIR/04b_tls_scanner_negctrl.json"
run_and_save tls_scanner_negctrl "$OUT_NEG" python3 -m scanner.tls_scanner -t 127.0.0.1 -s "$SCOPE_FILE" -p 8080
if ! has_result "$OUT_NEG"; then
  record "Step4 tls_scanner" "negative control: 8080 (plain HTTP) yields no TLS result" "PASS" ""
else
  record "Step4 tls_scanner" "negative control: 8080 (plain HTTP) yields no TLS result" "FAIL" "false positive, check $OUT_NEG"
fi

# ---------------------------------------------------------------------------
# STEP 5 — web_scanner
# ---------------------------------------------------------------------------
log "STEP 5 — web_scanner"
OUT="$RESULTS_DIR/05_web_scanner.json"
run_and_save web_scanner "$OUT" python3 -m scanner.web_scanner -t 127.0.0.1 -s "$SCOPE_FILE" -p 8080,8443
if grep -q "GROUND-TRUTH-PAGE" "$OUT"; then
  record "Step5 web_scanner" "8080 title exactly matches planted GROUND-TRUTH-PAGE" "PASS" ""
else
  record "Step5 web_scanner" "8080 title exactly matches planted GROUND-TRUTH-PAGE" "FAIL" "check $OUT"
fi

# ---------------------------------------------------------------------------
# STEP 6 — db_scanner  (expectation driven by a REAL connect, not lsof)
# ---------------------------------------------------------------------------
log "STEP 6 — db_scanner"
OUT="$RESULTS_DIR/06_db_scanner.json"
run_and_save db_scanner "$OUT" python3 -m scanner.db_scanner -t 127.0.0.1 -s "$SCOPE_FILE"
if [ "$MYSQL_UP" = "1" ]; then
  if port_open "$OUT" 3306 && grep -Eqi 'mysql|mariadb' "$OUT"; then
    record "Step6 db_scanner" "true positive: mysql/mariadb engine detected on 3306" "PASS" ""
  else
    record "Step6 db_scanner" "true positive: mysql/mariadb engine detected on 3306" "FAIL" "3306 is open but not fingerprinted, check $OUT"
  fi
else
  if ! has_result "$OUT"; then
    record "Step6 db_scanner" "correct negative: no DB on 3306, no output" "PASS" ""
  else
    record "Step6 db_scanner" "correct negative: no DB on 3306, no output" "FAIL" "spurious result with 3306 closed, check $OUT"
  fi
fi

# ---------------------------------------------------------------------------
# STEP 7 — udp / smb / snmp (localhost negatives)
# ---------------------------------------------------------------------------
log "STEP 7 — udp_scanner / smb_scanner / snmp_scanner (localhost negatives)"
for pair in "udp_scanner:07a" "smb_scanner:07b" "snmp_scanner:07c"; do
  mod="${pair%%:*}"; tag="${pair##*:}"
  OUT="$RESULTS_DIR/${tag}_${mod}_localhost.json"
  run_and_save "$mod" "$OUT" python3 -m "scanner.$mod" -t 127.0.0.1 -s "$SCOPE_FILE"
  if has_open "$OUT"; then
    record "Step7 $mod" "localhost negative control (no false positives)" "FAIL" "unexpected open result, check $OUT"
  else
    record "Step7 $mod" "localhost negative control (no false positives)" "PASS" ""
  fi
done

log "STEP 7b — udp_scanner true-positive attempt against router ${ROUTER_IP}"
OUT="$RESULTS_DIR/07d_udp_scanner_router.json"
run_and_save udp_scanner_router "$OUT" python3 -m scanner.udp_scanner -t "$ROUTER_IP" -s "$SCOPE_FILE"
if has_open "$OUT"; then
  record "Step7 udp_scanner" "true positive: router service (e.g. DNS 53) detected" "PASS" ""
else
  record "Step7 udp_scanner" "true positive: router service (e.g. DNS 53) detected" "INFO" "router may not answer UDP or ROUTER_IP wrong; check $OUT"
fi

# ---------------------------------------------------------------------------
# STEP 8 — mcp_ai_scanner (deliberate false-positive lesson)
# ---------------------------------------------------------------------------
log "STEP 8 — mcp_ai_scanner"
OUT="$RESULTS_DIR/08_mcp_ai_scanner.json"
run_and_save mcp_ai_scanner "$OUT" python3 -m scanner.mcp_ai_scanner -t 127.0.0.1 -s "$SCOPE_FILE"
if port_field "$OUT" 5000 && grep -Eqi 'ollama|mcp' "$OUT"; then
  record "Step8 mcp_ai_scanner" "AirPlay-on-5000 false positive reproduced (known issue)" "INFO" "flagged 5000 as AI server -- documented FP to filter"
else
  record "Step8 mcp_ai_scanner" "no AirPlay false positive on 5000 this run" "PASS" "run 'ollama serve' for a true positive on 11434"
fi

# ---------------------------------------------------------------------------
# STEP 9 — nmap_wrapper / mass_scan cross-engine agreement
# ---------------------------------------------------------------------------
log "STEP 9 — nmap_wrapper / mass_scan cross-engine agreement"
OUT_NMAP="$RESULTS_DIR/09a_nmap_wrapper.json"
run_and_save nmap_wrapper "$OUT_NMAP" python3 -m scanner.nmap_wrapper -t 127.0.0.1 -s "$SCOPE_FILE" --profile fast
OUT_MASS="$RESULTS_DIR/09b_mass_scan.json"
run_and_save mass_scan "$OUT_MASS" python3 -m scanner.mass_scan -t 127.0.0.1 -s "$SCOPE_FILE" -p 1-10000 --fallback

DISAGREE=""
if [ "${#EXPECTED_PORTS[@]}" -gt 0 ]; then
  for p in "${EXPECTED_PORTS[@]}"; do
    port_field "$OUT_NMAP" "$p" || DISAGREE="$DISAGREE nmap:$p"
    port_field "$OUT_MASS" "$p" || DISAGREE="$DISAGREE mass:$p"
  done
fi
if [ -z "$DISAGREE" ]; then
  record "Step9 cross-engine" "nmap_wrapper & mass_scan agree with port_scanner on ${EXPECTED_PORTS[*]}" "PASS" ""
else
  record "Step9 cross-engine" "nmap_wrapper & mass_scan agree with port_scanner on ${EXPECTED_PORTS[*]}" "FAIL" "disagreements:$DISAGREE"
fi

# ---------------------------------------------------------------------------
# STEP 10 — full pipeline (human-formatted output → token match)
# ---------------------------------------------------------------------------
log "STEP 10 — full pipeline (IT profile)"
OUT="$RESULTS_DIR/10_pipeline_it.json"
run_and_save pipeline_it "$OUT" python3 pipeline.py -t 127.0.0.1 -s "$SCOPE_FILE" --profile it
MISSING=""
if [ "${#EXPECTED_PORTS[@]}" -gt 0 ]; then
  for p in "${EXPECTED_PORTS[@]}"; do port_token "$OUT" "$p" || MISSING="$MISSING $p"; done
fi
if [ -z "$MISSING" ]; then
  record "Step10 pipeline" "reproduces all truly-open ports (${EXPECTED_PORTS[*]})" "PASS" ""
else
  record "Step10 pipeline" "reproduces all truly-open ports (${EXPECTED_PORTS[*]})" "FAIL" "missing:$MISSING (check $OUT)"
fi

# ---------------------------------------------------------------------------
# STEP 11 — OT passive test (optional)
# ---------------------------------------------------------------------------
if [ "$RUN_OT_TEST" = "1" ]; then
  log "STEP 11 — OT passive listen + tcpdump verification (needs sudo)"
  OUT="$RESULTS_DIR/11_pipeline_ot.json"
  TCPD_OUT="$RESULTS_DIR/11_tcpdump.txt"
  MY_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "")
  if [ -z "$MY_IP" ]; then
    record "Step11 OT passive" "auto-run skipped" "INFO" "could not detect local LAN IP; run manually per the guide"
  else
    ( sudo tcpdump -i any -n "udp and src host ${MY_IP}" -c 5 > "$TCPD_OUT" 2>&1 & )
    run_and_save pipeline_ot "$OUT" python3 pipeline.py -t "$LAN_CIDR" -s "$SCOPE_FILE" --profile ot --listen-seconds 20 -v
    sleep 2
    if [ -s "$TCPD_OUT" ] && grep -Eq "[1-9][0-9]* packets captured" "$TCPD_OUT"; then
      record "Step11 OT passive" "no outbound probes captured during OT scan" "FAIL" "tcpdump saw traffic, check $TCPD_OUT (0 expected)"
    else
      record "Step11 OT passive" "no outbound probes captured during OT scan" "PASS" ""
    fi
  fi
else
  record "Step11 OT passive" "skipped by default (RUN_OT_TEST=1 to enable)" "INFO" "run manually per guide, or set RUN_OT_TEST=1"
fi

# ---------------------------------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------------------------------
echo
echo "=================================================================="
echo " ACCURACY TEST SUMMARY"
echo "=================================================================="
printf "%-28s | %-58s | %-6s | %s\n" "STEP" "CHECK" "RESULT" "NOTE"
printf "%s\n" "------------------------------------------------------------------------------------------------------------------------"
{
  echo "| Step | Check | Result | Note |"
  echo "|---|---|---|---|"
} >> "$SUMMARY_FILE"

PASS_COUNT=0; FAIL_COUNT=0; INFO_COUNT=0
for row in "${ROWS[@]}"; do
  IFS='|' read -r step check result note <<< "$row"
  printf "%-28s | %-58s | %-6s | %s\n" "$step" "$check" "$result" "$note"
  echo "| $step | $check | $result | $note |" >> "$SUMMARY_FILE"
  case "$result" in
    PASS) PASS_COUNT=$((PASS_COUNT+1));;
    FAIL) FAIL_COUNT=$((FAIL_COUNT+1));;
    *)    INFO_COUNT=$((INFO_COUNT+1));;
  esac
done
echo "=================================================================="
echo "PASS: $PASS_COUNT   FAIL: $FAIL_COUNT   INFO: $INFO_COUNT"
echo "Full outputs + summary saved in: $RESULTS_DIR"
echo "=================================================================="

{
  echo
  echo "**Totals:** PASS=$PASS_COUNT FAIL=$FAIL_COUNT INFO=$INFO_COUNT"
} >> "$SUMMARY_FILE"

[ "$FAIL_COUNT" -gt 0 ] && exit 1
exit 0
