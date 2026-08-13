#!/usr/bin/env bash
# _assert.sh — shared runner + assertions for the per-scanner test harness.
#
# A per-scanner test script sources this and _profiles.sh, then:
#
#   harness_init "$@"                      # load expected.env, parse level arg
#   for lvl in $LEVELS; do
#       run_scanner port_scanner "$lvl" -p 22,80,443
#       check "port 22 open"  assert_port_open 22
#       check "port 80 open"  assert_port_open 80
#   done
#   finish                                 # print summary, set exit code
#
# Assertions read the JSONL the scanner emitted into $RUN_OUT. Results are pure
# ScanResult rows: {scanner,target,port,proto,status,data,evidence,error}.

# --- locate the probe/ root (this file lives at probe/tests/scan/_assert.sh) ---
_HARNESS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROBE_DIR="$(cd "$_HARNESS_DIR/../.." && pwd)"
PYTHON="${PROBE_PYTHON:-python3}"
LIVE_DIR="$_HARNESS_DIR/.live"        # persisted discovery results (git-ignored)

# --- global state -----------------------------------------------------------
PASS_N=0
FAIL_N=0
FAILED=()
CUR_SCANNER=""
CUR_LEVEL=""
RUN_OUT=""
RUN_RC=0
RUN_ROWS=0
RUN_SECS="0.0"

# ANSI (disabled if stdout is not a tty)
if [ -t 1 ]; then C_G=$'\033[32m'; C_R=$'\033[31m'; C_D=$'\033[2m'; C_0=$'\033[0m'
else C_G=""; C_R=""; C_D=""; C_0=""; fi

# --- harness_init LEVEL [TARGET_OVERRIDE] ------------------------------------
# Loads expected.env (if present) and parses the intensity level argument.
# Positional 1: level (T1..T5 or "all"); default from $DEFAULT_LEVEL or T3.
# Positional 2: optional TARGET override (wins over expected.env — used by
#               smoke.sh to hit 127.0.0.1 without touching the lab host).
# TARGET / EXPECT_* otherwise come from expected.env or the environment.
harness_init() {
    local env_file="$_HARNESS_DIR/expected.env"
    if [ -f "$env_file" ]; then
        # shellcheck disable=SC1090
        . "$env_file"
    fi

    local override="${2:-}"
    if [ -n "$override" ] && [ "$override" != "live" ]; then
        TARGET="$override"
    fi

    local level="${1:-${DEFAULT_LEVEL:-T3}}"
    if [ "$level" = "all" ] || [ "$level" = "ALL" ]; then
        LEVELS="$ALL_PROFILES"
    else
        resolve_profile "$level" || exit 2
        LEVELS="$level"
    fi

    TMPDIR_HARNESS="$(mktemp -d "${TMPDIR:-/tmp}/va_scan_test.XXXXXX")"
    SCOPE_FILE="$TMPDIR_HARNESS/scope.txt"
    trap '[ -n "${KEEP_ARTIFACTS:-}" ] || rm -rf "$TMPDIR_HARNESS"' EXIT

    # HOSTS: the targets to scan, one at a time. In 'live' mode this is the set
    # of hosts a previous host_discovery marked alive; otherwise it's the single
    # target/CIDR given (the scanner expands a CIDR itself).
    if [ "$override" = "live" ]; then
        LIVE_MODE=1
        local list; list="$(load_live_hosts)" || exit 3
        # shellcheck disable=SC2206
        HOSTS=($list)
        [ "${#HOSTS[@]}" -eq 0 ] && {
            echo "no saved live hosts — run host_discovery first" >&2; exit 3; }
        printf '%s\n' "${HOSTS[@]}" > "$SCOPE_FILE"
        TARGET=""
        echo "mode:   live — ${#HOSTS[@]} discovered host(s), scanned one by one"
    else
        LIVE_MODE=0
        : "${TARGET:?TARGET is not set — edit probe/tests/scan/expected.env or pass a target}"
        printf '%s\n' "$TARGET" > "$SCOPE_FILE"
        HOSTS=("$TARGET")
        echo "target: $TARGET"
    fi

    echo "levels: $LEVELS"
    [ -n "${KEEP_ARTIFACTS:-}" ] && echo "artifacts: $TMPDIR_HARNESS"
    echo
}

# --- run_scanner MODULE LEVEL [extra args...] --------------------------------
# Runs `python3 -m scanner.MODULE` at the given intensity against TARGET.
# Captures JSONL into $RUN_OUT and sets RUN_RC / RUN_ROWS / RUN_SECS.
run_scanner() {
    local module="$1"; local level="$2"; shift 2
    resolve_profile "$level" || return 2
    CUR_SCANNER="$module"; CUR_LEVEL="$level"
    RUN_OUT="$TMPDIR_HARNESS/${module}_${level}.jsonl"
    local err="$TMPDIR_HARNESS/${module}_${level}.stderr"

    printf '%s──%s %s @ %s %s(rate=%s conc=%s t/o=%s)%s\n' \
        "$C_D" "$C_0" "$module" "$PROFILE_LABEL" \
        "$C_D" "$PROFILE_RATE" "$PROFILE_CONC" "$PROFILE_TIMEOUT" "$C_0"

    local start end
    start="$(date +%s.%N 2>/dev/null || date +%s)"
    ( cd "$PROBE_DIR" && "$PYTHON" -m "scanner.$module" \
        -t "$TARGET" -s "$SCOPE_FILE" -o "$RUN_OUT" \
        --rate "$PROFILE_RATE" --concurrency "$PROFILE_CONC" --timeout "$PROFILE_TIMEOUT" \
        "$@" ) >/dev/null 2>"$err"
    RUN_RC=$?
    end="$(date +%s.%N 2>/dev/null || date +%s)"

    RUN_SECS="$(awk -v a="$start" -v b="$end" 'BEGIN{printf "%.1f", b-a}' 2>/dev/null || echo "?")"
    RUN_ROWS=0
    [ -f "$RUN_OUT" ] && RUN_ROWS="$(awk 'END{print NR+0}' "$RUN_OUT")"

    printf '   %src=%s rows=%s %ss%s\n' "$C_D" "$RUN_RC" "$RUN_ROWS" "$RUN_SECS" "$C_0"
    if [ "$RUN_RC" -ne 0 ]; then
        echo "   ${C_R}stderr:${C_0}"
        sed 's/^/     /' "$err" | tail -n 8
    fi
}

# --- check LABEL assertion-cmd [args...] -------------------------------------
# Runs an assertion; records PASS/FAIL and prints a line.
check() {
    local label="$1"; shift
    if "$@"; then
        PASS_N=$((PASS_N + 1)); printf '   %sPASS%s %s\n' "$C_G" "$C_0" "$label"
    else
        FAIL_N=$((FAIL_N + 1)); printf '   %sFAIL%s %s\n' "$C_R" "$C_0" "$label"
        FAILED+=("$CUR_SCANNER @ $CUR_LEVEL — $label")
    fi
}

# --- assertions (operate on $RUN_OUT) ----------------------------------------
assert_run_clean() { [ "$RUN_RC" -eq 0 ]; }

assert_rows_ge() { [ "$RUN_ROWS" -ge "$1" ]; }

assert_host_alive() {
    "$PYTHON" - "$RUN_OUT" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sys.exit(0 if any(r.get("data", {}).get("alive") for r in rows) else 1)
PY
}

# assert_port_open PORT — a row for PORT with status "open".
assert_port_open() {
    "$PYTHON" - "$RUN_OUT" "$1" <<'PY'
import json, sys
port = int(sys.argv[2])
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sys.exit(0 if any(r.get("port") == port and r.get("status") == "open" for r in rows) else 1)
PY
}

# assert_port_status PORT STATUS — a row for PORT with the given status.
assert_port_status() {
    "$PYTHON" - "$RUN_OUT" "$1" "$2" <<'PY'
import json, sys
port, status = int(sys.argv[2]), sys.argv[3]
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sys.exit(0 if any(r.get("port") == port and r.get("status") == status for r in rows) else 1)
PY
}

# save_live_hosts — persist the live hosts from a host_discovery $RUN_OUT so
# later scanners can target only active hosts ('run.sh live ...'). Overwrites:
# the most recent discovery wins. Writes hosts.txt (one IP/line) + hosts.jsonl
# (full discovery rows: mac, vendor, device_hint, open ports).
save_live_hosts() {
    mkdir -p "$LIVE_DIR"
    "$PYTHON" - "$RUN_OUT" "$LIVE_DIR" <<'PY'
import json, os, sys
out = sys.argv[2]
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
live = [r for r in rows if r.get("data", {}).get("alive")]
with open(os.path.join(out, "hosts.jsonl"), "w") as f:
    for r in live:
        f.write(json.dumps(r) + "\n")
with open(os.path.join(out, "hosts.txt"), "w") as f:
    for r in live:
        f.write(r["target"] + "\n")
print("   saved %d live host(s) -> tests/scan/.live/hosts.txt" % len(live))
PY
}

# load_live_hosts — print saved live IPs space-separated; err+return 1 if none.
load_live_hosts() {
    local f="$LIVE_DIR/hosts.txt"
    if [ ! -s "$f" ]; then
        echo "no saved live hosts at $f — run host_discovery first" >&2
        return 1
    fi
    tr '\n' ' ' < "$f"
}

# open_ports_for <ip> — from saved discovery, print that host's open TCP ports
# (comma-separated) if host_discovery recorded any; else empty.
open_ports_for() {
    local f="$LIVE_DIR/hosts.jsonl"
    [ -s "$f" ] || return 0
    "$PYTHON" - "$f" "$1" <<'PY'
import json, sys
ip = sys.argv[2]
for l in open(sys.argv[1]):
    r = json.loads(l)
    if r.get("target") == ip:
        ports = [str(p["port"]) for p in r.get("data", {}).get("responding_ports", [])
                 if p.get("state") == "open"]
        if ports:
            print(",".join(ports))
        break
PY
}

# print_alive_hosts — for host_discovery: list the live targets + count.
print_alive_hosts() {
    "$PYTHON" - "$RUN_OUT" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
alive = [r for r in rows if r.get("data", {}).get("alive")]
print("   live hosts: %d / %d probed" % (len(alive), len(rows)))
for r in alive:
    print("     %-15s  %s" % (r["target"], r.get("evidence", "")))
PY
}

# assert_alive_ge N — at least N hosts came back alive.
assert_alive_ge() {
    "$PYTHON" - "$RUN_OUT" "$1" <<'PY'
import json, sys
n = int(sys.argv[2])
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
alive = sum(1 for r in rows if r.get("data", {}).get("alive"))
sys.exit(0 if alive >= n else 1)
PY
}

# assert_scanner_reported — at least one non-error row from this scanner.
assert_scanner_reported() {
    "$PYTHON" - "$RUN_OUT" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
sys.exit(0 if any(not r.get("error") for r in rows) else 1)
PY
}

# --- finish ------------------------------------------------------------------
finish() {
    echo
    echo "================================================================"
    printf 'passed: %s   failed: %s\n' "$PASS_N" "$FAIL_N"
    if [ "${#FAILED[@]}" -gt 0 ]; then
        local f
        for f in "${FAILED[@]}"; do printf '  %s!%s %s\n' "$C_R" "$C_0" "$f"; done
    fi
    echo "================================================================"
    [ "$FAIL_N" -eq 0 ]
}
