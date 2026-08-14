#!/usr/bin/env bash
# smoke.sh — Phase 0 wiring check. Proves the harness can run a scanner and
# parse its output, without depending on your lab TARGET. Uses host_discovery
# against 127.0.0.1 (always reachable) at T3.
#
#   ./smoke.sh
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/_profiles.sh"
. "$HERE/_assert.sh"

harness_init T3 127.0.0.1

run_scanner host_discovery T3
check "harness ran the scanner cleanly" assert_run_clean
check "scanner emitted at least one row" assert_rows_ge 1

finish
