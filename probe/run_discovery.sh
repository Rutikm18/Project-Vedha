#!/usr/bin/env bash
# run_discovery.sh — run Vedha host discovery against a target. You provide ONLY
# the target(s); the scope allowlist (the required authorization guard) is
# auto-generated to authorize exactly what you scan, then deleted.
#
# Usage:
#   ./run_discovery.sh <target> [<target> ...]
#     target = IP (192.168.1.68), CIDR (192.168.1.0/24), hostname, or range a-b
#
# Optional env vars:
#   VEDHA_OUT=results.jsonl   also write JSONL results to this file
#   VEDHA_TIMEOUT=1.0         per-probe timeout seconds (default 3.0)
#   VEDHA_RATE=200            max operations/sec (default 200)
#   VEDHA_VERBOSE=1           debug logging
#
# Examples:
#   ./run_discovery.sh 192.168.1.68
#   ./run_discovery.sh 192.168.1.0/24
#   VEDHA_OUT=hosts.jsonl VEDHA_TIMEOUT=1 ./run_discovery.sh 10.0.0.1 10.0.0.2
set -euo pipefail

cd "$(dirname "$0")"                              # -> probe/

if [ "$#" -lt 1 ]; then
  echo "usage: $0 <target> [target ...]" >&2
  exit 2
fi

# Activate the project venv if present (pure-stdlib scanner, but keeps parity).
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
export PYTHONPATH="$PWD"

# Scope = exactly the target(s) you passed. Authorizes only what you scan.
SCOPE="$(mktemp -t vedha-scope.XXXXXX)"
trap 'rm -f "$SCOPE"' EXIT
printf '%s\n' "$@" > "$SCOPE"

# Assemble optional flags from env.
args=(-t "$@" -s "$SCOPE" --timeout "${VEDHA_TIMEOUT:-3.0}" --rate "${VEDHA_RATE:-200}")
[ -n "${VEDHA_OUT:-}" ]     && args+=(-o "$VEDHA_OUT")
[ -n "${VEDHA_VERBOSE:-}" ] && args+=(-v)

exec python -m scanner.host_discovery "${args[@]}"
