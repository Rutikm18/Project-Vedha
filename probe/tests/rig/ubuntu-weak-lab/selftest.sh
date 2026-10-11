#!/usr/bin/env bash
# Self-test for the lab's own tooling: starts every emulator on an unprivileged port,
# runs the matching independent verifier against it, and checks BOTH directions:
#   - the weak emulator is CONFIRMED (exit 0)
#   - a "wrong port" probe is not confirmed (exit 2), so a pass cannot be vacuous.
# No root, no packages, no network exposure (binds 127.0.0.1). Works on macOS and Linux.
#
#   ./selftest.sh
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EMU="$HERE/lab_emulators.py"
PROBE="$HERE/lab_probe.py"
PY="${PYTHON:-python3}"
export VEDHA_LAB_ROOTDESC_PORT=18500
PIDS=()
PASS=0
FAIL=0

cleanup() {
  for p in "${PIDS[@]:-}"; do [ -n "$p" ] && kill "$p" 2>/dev/null; done
}
trap cleanup EXIT

start() { # name tcp udp
  local args=(serve "$1" --bind 127.0.0.1)
  [ -n "${2:-}" ] && args+=(--tcp "$2")
  [ -n "${3:-}" ] && args+=(--udp "$3")
  "$PY" "$EMU" "${args[@]}" >/dev/null 2>&1 &
  PIDS+=("$!")
}

expect() { # label expected_exit command...
  local label="$1" want="$2"
  shift 2
  local out rc
  out="$("$@" 2>&1)"
  rc=$?
  if [ "$rc" -eq "$want" ]; then
    PASS=$((PASS + 1))
    printf 'PASS  %-34s %s\n' "$label" "$out"
  else
    FAIL=$((FAIL + 1))
    printf 'FAIL  %-34s want exit %s got %s: %s\n' "$label" "$want" "$rc" "$out"
  fi
}

start rtsp 18554,18555
start cwmp 18547
start adb 18556
start ollama 18434
start ssdp "" 18900
start ntp "" 18123
start sip 18060 18060
start ipmi "" 18623
start listen 18786 18177
sleep 1.5

P() { "$PY" "$PROBE" "$@"; }
H=127.0.0.1

expect "T19 rtsp OPTIONS"        0 P check rtsp-options  $H 18554
expect "G05 rtsp DESCRIBE no-auth" 0 P check rtsp-describe $H 18555
expect "T20 cwmp"                0 P check cwmp          $H 18547
expect "T21 adb no AUTH"         0 P check adb-noauth    $H 18556
expect "T22 ollama no auth"      0 P check ollama        $H 18434
expect "G02 ssdp+IGD"            0 P check ssdp-igd      $H 18900
expect "G04 ntp monlist"         0 P check ntp-monlist   $H 18123
expect "G09 sip OPTIONS"         0 P check sip-options   $H 18060
expect "T05 ipmi cipher-0"       0 P check ipmi-cipher0  $H 18623
expect "G14.. tcp port-only"     0 P up tcp $H 18786
expect "G16.. udp port-only"     0 P up udp $H 18177
# negative controls: nothing listens here, so the verifier must say UNREACHABLE (2)
expect "neg: rtsp on dead port"  2 P check rtsp-options  $H 18999
expect "neg: adb on dead port"   2 P check adb-noauth    $H 18998
expect "neg: ollama dead port"   2 P check ollama        $H 18997

echo
echo "self-test: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
