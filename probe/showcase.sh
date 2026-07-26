#!/usr/bin/env bash
#
# showcase.sh — demonstrate the probe end-to-end without a manager.
#
#   ./showcase.sh              interactive menu (pick a scan, enter scope/target)
#   ./showcase.sh --demo       scripted tour of capabilities + scope safety
#   ./showcase.sh --list       list use-cases and raw scan types
#   ./showcase.sh --use-case uc_full_assessment --targets 127.0.0.1 --scope 127.0.0.1/32 [--exclude ...]
#
# Every scan runs through the REAL engine (agent.engine.run_scan) — the same
# code path a manager-issued job takes. Scope + excludes are enforced by the
# probe itself, so out-of-scope / excluded targets are refused, not scanned.
#
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PY="./.venv/bin/python"
[ -x "$PY" ] || PY="python3"

hr(){ printf '\033[2m%s\033[0m\n' "──────────────────────────────────────────────────────────────────"; }
banner(){ echo; hr; printf '\033[1m▶ %s\033[0m\n' "$*"; hr; }

probe(){ "$PY" showcase_run.py "$@"; }

demo(){
  echo "Probe capability + scope-safety tour (target: 127.0.0.1)."
  echo "Nothing outside the given scope is ever contacted."

  banner "1/7  Network discovery — host liveness + open ports"
  probe --use-case uc_discovery_only --targets 127.0.0.1 --scope 127.0.0.1/32

  banner "2/7  Full assessment — funnel: discovery → ports → banner → service branches"
  probe --use-case uc_full_assessment --targets 127.0.0.1 --scope 127.0.0.1/32

  banner "3/7  Web triage — HTTP methods via OPTIONS + headers  (Task 5)"
  probe --use-case uc_web_app_triage --targets 127.0.0.1 --scope 127.0.0.1/32

  banner "4/7  UDP exposure — real monlist / open-recursion / memcached  (Task 4)"
  probe --use-case uc_udp_service_exposure --targets 127.0.0.1 --scope 127.0.0.1/32

  banner "5/7  Windows estate — SMB signing detection  (Task 2)"
  probe --use-case uc_windows_estate --targets 127.0.0.1 --scope 127.0.0.1/32

  banner "6/7  SCOPE SAFETY — 8.8.8.8 is OUTSIDE scope 127.0.0.1/32  → must be REFUSED"
  probe --scan-type discovery --targets 8.8.8.8 --scope 127.0.0.1/32

  banner "7/7  EXCLUDE — 127.0.0.1 carved out of 127.0.0.0/8  → must be REFUSED"
  probe --scan-type discovery --targets 127.0.0.1 --scope 127.0.0.0/8 --exclude 127.0.0.1/32

  echo; echo "Demo complete. Steps 6 & 7 prove the probe refuses anything outside scope."
}

interactive(){
  IDS=()
  while IFS= read -r l; do IDS+=("$l"); done \
    < <("$PY" -c "from agent.use_cases import USE_CASES; print(chr(10).join(USE_CASES))")

  echo "Choose a scan:"
  i=1
  for id in "${IDS[@]}"; do printf "  %2d) %s\n" "$i" "$id"; i=$((i+1)); done
  printf "Selection [1]: "; read -r sel; sel=${sel:-1}
  uc="${IDS[$((sel-1))]:-${IDS[0]}}"

  printf "Targets            [127.0.0.1]: ";      read -r tg; tg=${tg:-127.0.0.1}
  printf "Scope allowlist    [127.0.0.1/32]: ";   read -r sc; sc=${sc:-127.0.0.1/32}
  printf "Excludes (blank=none): ";               read -r ex

  probe --use-case "$uc" --targets "$tg" --scope "$sc" --exclude "$ex"
}

case "${1:-}" in
  --demo)                 demo ;;
  --selftest)             "$PY" selftest_live.py ;;
  --list)                 probe --list ;;
  ""|-i|--interactive)    interactive ;;
  *)                      probe "$@" ;;   # pass straight through to showcase_run.py
esac
