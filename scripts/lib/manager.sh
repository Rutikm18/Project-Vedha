#!/usr/bin/env bash
# Manager URL resolution and connectivity checks.
set -Eeuo pipefail

manager_defaults() {
  local os_name
  os_name="$(uname -s)"
  MANAGER_API_URL=${MANAGER_API_URL:-http://localhost:18080}
  if [[ -z "${PLATFORM_URL:-}" ]]; then
    case "$os_name" in
      Darwin) PLATFORM_URL="http://host.docker.internal:18080" ;;
      Linux) PLATFORM_URL="http://host.docker.internal:18080" ;;
      *) PLATFORM_URL="$MANAGER_API_URL" ;;
    esac
  fi
}

manager_validate_urls() {
  validate_url "$MANAGER_API_URL" || die "Invalid manager URL: $MANAGER_API_URL"
  validate_url "$PLATFORM_URL" || die "Invalid platform URL: $PLATFORM_URL"
  MANAGER_API_URL=${MANAGER_API_URL%/}
  PLATFORM_URL=${PLATFORM_URL%/}

  if ! is_loopback_url "$MANAGER_API_URL" && [[ "$MANAGER_API_URL" != https://* ]]; then
    die "Remote manager authentication requires HTTPS. Use --manager-url https://..."
  fi
  if ! is_local_platform_url "$PLATFORM_URL" && [[ "$PLATFORM_URL" != https://* ]]; then
    die "Remote probe communication requires HTTPS. Use --platform-url https://..."
  fi
  if [[ "${VERIFY_TLS:-true}" == "false" ]] &&
    { [[ "$MANAGER_API_URL" == https://* ]] || [[ "$PLATFORM_URL" == https://* ]]; }; then
    die "TLS verification cannot be disabled for a remote HTTPS manager."
  fi
  if [[ "$PLATFORM_URL" == http://* ]]; then
    log_warn "HTTP is permitted only for this explicitly local development target."
  fi
}

manager_health() {
  local response code
  response="$(secure_temp_file)"
  code="$(curl -sS --connect-timeout 5 --max-time 15 -o "$response" -w '%{http_code}' \
    "$MANAGER_API_URL/health" 2>/dev/null || printf '000')"
  if [[ "$code" != "200" ]]; then
    die "Manager health failed at $MANAGER_API_URL/health (HTTP $code)."
  fi
  log_ok "Manager API is reachable at $MANAGER_API_URL."
}

manager_login_endpoint_check() {
  local code
  code="$(curl -sS --connect-timeout 5 --max-time 15 -o /dev/null -w '%{http_code}' \
    -X POST -H 'Content-Type: application/json' -d '{}' \
    "$MANAGER_API_URL/auth/login" 2>/dev/null || printf '000')"
  case "$code" in
    400|401|422) log_ok "Login endpoint is reachable." ;;
    *) log_warn "Login endpoint returned HTTP $code; expected a validation/authentication response." ;;
  esac
}

linux_host_gateway_required() {
  [[ "$(uname -s)" == "Linux" && "$PLATFORM_URL" == *host.docker.internal* ]]
}

manager_container_connectivity() {
  [[ -n "${PROBE_IMAGE:-}" ]] || return 1
  docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1 || return 1
  local output rc=0
  if linux_host_gateway_required; then
    output="$(docker run --rm --add-host host.docker.internal:host-gateway \
      -e URL="$PLATFORM_URL" "$PROBE_IMAGE" \
      python -c 'import os,sys,urllib.request; r=urllib.request.urlopen(os.environ["URL"]+"/health",timeout=10); sys.exit(0 if r.status==200 else 1)' \
      2>&1)" || rc=$?
  else
    output="$(docker run --rm -e URL="$PLATFORM_URL" "$PROBE_IMAGE" \
      python -c 'import os,sys,urllib.request; r=urllib.request.urlopen(os.environ["URL"]+"/health",timeout=10); sys.exit(0 if r.status==200 else 1)' \
      2>&1)" || rc=$?
  fi
  if (( rc == 0 )); then
    log_ok "A probe container can reach $PLATFORM_URL."
    return 0
  fi
  [[ -n "$output" && "${VERBOSE:-false}" == "true" ]] &&
    log_warn "$(sanitize_single_line "$output")"
  return "$rc"
}
