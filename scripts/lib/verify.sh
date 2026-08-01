#!/usr/bin/env bash
# Registration polling, heartbeat freshness, and diagnostics.
set -Eeuo pipefail

verify_runtime_ready() {
  local deadline now logs
  deadline=$(( $(date +%s) + REGISTRATION_TIMEOUT ))
  log_info "Waiting for the probe runtime to persist identity and enter a job-receive loop..."
  while :; do
    logs="$(docker logs --tail 120 "$PROBE_CONTAINER" 2>&1 || true)"
    if probe_container_running &&
      printf '%s\n' "$logs" | grep -Eq 'Registered as|Resumed as' &&
      printf '%s\n' "$logs" | grep -Eq 'WebSocket connected|Push mode active|Waiting for scan jobs'; then
      if probe_volume_has_identity; then
        log_ok "Probe runtime is ready and its agent identity is persisted."
        return 0
      fi
    fi
    if printf '%s\n' "$logs" | grep -Eq \
      'Setup needed:|HARDWARE BINDING CHECK FAILED|License is malformed|No license found'; then
      log_error "Probe runtime reported a non-retryable bootstrap error."
      return 1
    fi
    now=$(date +%s)
    (( now >= deadline )) && break
    sleep "$POLL_INTERVAL"
  done
  log_error "Probe runtime did not become ready within ${REGISTRATION_TIMEOUT}s."
  return 1
}

verify_fetch_agent() {
  local response result rc
  response="$(secure_temp_file)"
  auth_curl GET "$MANAGER_API_URL/agents" "$PAT_TOKEN" "$response"
  [[ "$HTTP_CODE" == "200" ]] || return 1
  # Agent absence/staleness is an expected polling state. Disable errtrace
  # inheritance while the JSON selector returns its explicit retry codes.
  set +E
  if result="$(python3 - "$response" "${PROBE_AGENT_ID:-}" "$PROBE_NAME" "$HEARTBEAT_FRESHNESS" <<'PY'
import datetime as dt
import json
import sys

path, expected_id, expected_name, freshness = sys.argv[1:]
with open(path, encoding="utf-8") as handle:
    agents = json.load(handle)

match = None
if expected_id:
    match = next((a for a in agents if str(a.get("id")) == expected_id), None)
if match is None:
    candidates = [a for a in agents if a.get("name") == expected_name]
    if len(candidates) == 1:
        match = candidates[0]
    elif candidates:
        candidates.sort(key=lambda a: a.get("last_heartbeat") or "", reverse=True)
        match = candidates[0]
if match is None:
    sys.exit(2)

last = match.get("last_heartbeat")
age = 10**9
if last:
    stamp = dt.datetime.fromisoformat(last.replace("Z", "+00:00"))
    age = (dt.datetime.now(dt.timezone.utc) - stamp).total_seconds()

print("|".join([
    str(match.get("id", "")),
    "true" if match.get("online") else "false",
    str(match.get("status", "")),
    str(int(age)),
    last or "",
]))
sys.exit(0 if match.get("online") and age <= int(freshness) else 3)
PY
  )"; then
    rc=0
  else
    rc=$?
  fi
  set -E
  VERIFY_AGENT_RESULT=$result
  return "$rc"
}

verify_registration() {
  local deadline now rc=1
  [[ -n "${PAT_TOKEN:-}" ]] || die "PAT is required to verify registration through the manager."
  if ! verify_runtime_ready; then
    log_error "Last 50 sanitized probe log lines:"
    probe_sanitized_logs 50 >&2 || true
    return 1
  fi
  deadline=$(( $(date +%s) + REGISTRATION_TIMEOUT ))
  log_info "Waiting up to ${REGISTRATION_TIMEOUT}s for '$PROBE_NAME' to become online..."
  while :; do
    if verify_fetch_agent; then
      IFS='|' read -r PROBE_AGENT_ID agent_online agent_status agent_age agent_heartbeat \
        <<< "$VERIFY_AGENT_RESULT"
      log_ok "Probe registered and online (agent $PROBE_AGENT_ID, heartbeat ${agent_age}s ago)."
      save_state
      return 0
    else
      rc=$?
    fi
    now=$(date +%s)
    (( now >= deadline )) && break
    sleep "$POLL_INTERVAL"
  done

  log_error "Registration verification timed out (last stage: manager agent lookup, result $rc)."
  if curl -fsS --connect-timeout 3 --max-time 5 "$MANAGER_API_URL/health" >/dev/null 2>&1; then
    log_info "Manager connectivity: healthy."
  else
    log_error "Manager connectivity: failed."
  fi
  log_error "Last 50 sanitized probe log lines:"
  probe_sanitized_logs 50 >&2 || true
  log_error "Check PAT scopes, PLATFORM_URL, TLS trust, licensing, and container networking."
  return 1
}

doctor_ok=0
doctor_warn=0
doctor_fail=0
doctor_pass() { log_ok "$*"; doctor_ok=$((doctor_ok + 1)); }
doctor_note() { log_warn "$*"; doctor_warn=$((doctor_warn + 1)); }
doctor_bad() { log_error "$*"; doctor_fail=$((doctor_fail + 1)); }

doctor_command() {
  local command mode
  printf 'Vedha Probe Manager diagnostics\n\n'
  doctor_pass "Operating system: $(uname -s) $(uname -m)"
  doctor_pass "Bash version: ${BASH_VERSION%%(*}"

  for command in bash docker curl python3; do
    if command -v "$command" >/dev/null 2>&1; then
      doctor_pass "$command is available"
    else
      doctor_bad "$command is missing"
    fi
  done

  [[ -d "$VEDHA_ROOT/.git" ]] && doctor_pass "Repository root: $VEDHA_ROOT" ||
    doctor_bad "Repository root could not be validated"
  [[ -f "$VEDHA_ROOT/probe/tools/issue_license.py" ]] &&
    doctor_pass "License tool exists" || doctor_bad "License tool is missing"
  [[ -f "$VEDHA_ROOT/probe/Dockerfile" ]] &&
    doctor_pass "Probe Dockerfile exists" || doctor_bad "Probe Dockerfile is missing"

  if docker info >/dev/null 2>&1; then
    doctor_pass "Docker daemon is running"
  else
    doctor_bad "Docker daemon is unavailable"
  fi
  if docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1; then
    doctor_pass "Probe image exists: $PROBE_IMAGE"
  else
    doctor_note "Probe image is not present: $PROBE_IMAGE"
  fi

  if curl -fsS --connect-timeout 3 --max-time 8 "$MANAGER_API_URL/health" >/dev/null 2>&1; then
    doctor_pass "Manager API is reachable"
    manager_login_endpoint_check
  else
    doctor_bad "Manager API is unreachable at $MANAGER_API_URL"
  fi

  if docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1; then
    if manager_container_connectivity; then
      doctor_pass "Container-to-manager connectivity works"
    else
      doctor_note "Container-to-manager connectivity failed"
    fi
  fi

  if probe_container_exists; then
    doctor_pass "Probe container exists"
    if probe_container_running; then
      doctor_pass "Probe container is running"
    else
      doctor_bad "Probe container is not running"
    fi
    mode="$(stat -f '%Lp' "$VEDHA_STATE_FILE" 2>/dev/null || stat -c '%a' "$VEDHA_STATE_FILE" 2>/dev/null || true)"
    [[ ! -f "$VEDHA_STATE_FILE" || "$mode" == "600" ]] &&
      doctor_pass "State-file permissions are restrictive" ||
      doctor_bad "State file mode is $mode; expected 600"
    if probe_sanitized_logs 20 | grep -Eq 'Registered as|Resumed as|WebSocket connected|Push mode active'; then
      doctor_pass "Probe logs show successful manager communication"
    else
      doctor_note "Probe logs do not show a recent registration/connection marker"
    fi
  else
    doctor_note "Probe container is not installed"
  fi

  PAT_TOKEN=${PAT_TOKEN:-${VEDHA_PAT:-${PROBE_PAT:-}}}
  if [[ -n "$PAT_TOKEN" ]]; then
    if verify_fetch_agent; then
      doctor_pass "Current probe registration and heartbeat are healthy"
    else
      doctor_note "PAT works, but the configured probe is absent or stale"
    fi
  else
    doctor_note "Set VEDHA_PAT to verify manager-side registration and heartbeat"
  fi

  if [[ "$PLATFORM_URL" == https://* ]] || is_local_platform_url "$PLATFORM_URL"; then
    doctor_pass "Platform URL TLS/locality policy is valid"
  else
    doctor_bad "Remote platform URL is not HTTPS"
  fi

  if git -C "$VEDHA_ROOT" check-ignore -q scripts/state/probe.env; then
    doctor_pass "scripts/state is protected by .gitignore"
  else
    doctor_bad "scripts/state/probe.env is not ignored by Git"
  fi

  printf '\nDiagnostics: %d passed, %d warning(s), %d failure(s)\n' \
    "$doctor_ok" "$doctor_warn" "$doctor_fail"
  (( doctor_fail == 0 ))
}
