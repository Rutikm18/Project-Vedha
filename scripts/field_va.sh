#!/usr/bin/env bash
# Field VA driver for the Vedha manager API — fails loud, never loops forever.
#
#   export BASE=http://<manager-host>:18080     # inbound TCP 18080 must be open
#   export TOKEN=<jwt>                            # from POST /auth/login
#   export CIDR=192.168.1.0/24
#   ./scripts/field_va.sh
#
set -Eeuo pipefail

# --- preconditions ---------------------------------------------------------
: "${BASE:?set BASE, e.g. export BASE=http://<manager-host>:18080}"
: "${TOKEN:?set TOKEN (JWT from POST /auth/login)}"
: "${CIDR:?set CIDR, e.g. export CIDR=192.168.1.0/24}"
command -v jq >/dev/null || { echo "FATAL: install jq (brew install jq)"; exit 1; }

POLL_INTERVAL="${POLL_INTERVAL:-4}"
POLL_TIMEOUT="${POLL_TIMEOUT:-600}"   # give up after 10 min instead of forever

# api METHOD PATH [json-body] -> prints body, aborts on non-2xx or empty body.
api() {
  local method="$1" path="$2" body="${3:-}" resp code out
  local args=(-sS -m 30 -w '\n%{http_code}' -X "$method"
              -H "Authorization: Bearer $TOKEN")
  [[ -n "$body" ]] && args+=(-H 'Content-Type: application/json' -d "$body")

  resp="$(curl "${args[@]}" "$BASE$path")" || {
    echo "FATAL: curl failed for $method $path (connection refused / bad BASE / firewall?)" >&2
    exit 1
  }
  code="${resp##*$'\n'}"        # last line = HTTP status
  out="${resp%$'\n'*}"          # everything before it = body
  if [[ ! "$code" =~ ^2 ]]; then
    echo "FATAL: $method $path -> HTTP $code" >&2
    echo "$out" >&2
    exit 1
  fi
  printf '%s' "$out"
}

# --- 1. connectivity guard (proves 18080 is reachable) ---------------------
echo ">> health check $BASE/health"
api GET /health >/dev/null
echo "   OK"

# --- 2. create engagement --------------------------------------------------
echo ">> creating engagement (scope $CIDR)"
EID="$(api POST /engagements "{\"name\":\"Field VA\",\"scope_cidrs\":[\"$CIDR\"]}" \
        | jq -er '.id')"
echo "   engagement id = $EID"

# --- 3. dispatch scan job --------------------------------------------------
# POST /agents/jobs enqueues a probe-executable ScanJob. Omitting params.targets
# defaults to the full engagement scope. Pick a use_case_id from GET /agents/use-cases.
USE_CASE="${USE_CASE:-uc_discovery_only}"
echo ">> enqueuing job (use_case=$USE_CASE)"
JID="$(api POST /agents/jobs \
        "{\"engagement_id\":\"$EID\",\"job_type\":\"discovery\",\"use_case_id\":\"$USE_CASE\"}" \
        | jq -er '.job_id')"
echo "   job id = $JID"

# --- 4. poll with a hard timeout ------------------------------------------
echo ">> polling job $JID (interval ${POLL_INTERVAL}s, timeout ${POLL_TIMEOUT}s)"
elapsed=0
while :; do
  status="$(api GET "/agents/jobs/$JID" | jq -er '.status // "unknown"')"
  echo "   status=$status (${elapsed}s)"
  case "$status" in
    completed) echo ">> DONE"; break ;;
    failed|error|cancelled) echo "FATAL: job ended as $status" >&2; exit 1 ;;
  esac
  (( elapsed >= POLL_TIMEOUT )) && { echo "FATAL: timeout after ${POLL_TIMEOUT}s" >&2; exit 1; }
  sleep "$POLL_INTERVAL"; elapsed=$((elapsed + POLL_INTERVAL))
done

echo "EID=$EID JID=$JID"
