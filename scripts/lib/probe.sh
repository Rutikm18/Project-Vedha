#!/usr/bin/env bash
# Probe image and container lifecycle.
set -Eeuo pipefail

probe_defaults() {
  PROBE_IMAGE=${PROBE_IMAGE:-vedha-probe:local}
  PROBE_CONTAINER=${PROBE_CONTAINER:-vedha-probe}
  PROBE_STATE_VOLUME=${PROBE_STATE_VOLUME:-vedha-probe-state}
  PROBE_NAME=${PROBE_NAME:-$(hostname 2>/dev/null || printf 'vedha-probe')}
  PROBE_LOCATION=${PROBE_LOCATION:-}
  PROBE_NETWORK_SEGMENTS=${PROBE_NETWORK_SEGMENTS:-}
  PROBE_MAX_TARGETS=${PROBE_MAX_TARGETS:-4096}
  PROBE_MAX_JOB_SECONDS=${PROBE_MAX_JOB_SECONDS:-7200}
  VERIFY_TLS=${VERIFY_TLS:-true}
  REGISTRATION_TIMEOUT=${REGISTRATION_TIMEOUT:-60}
  POLL_INTERVAL=${POLL_INTERVAL:-2}
  HEARTBEAT_FRESHNESS=${HEARTBEAT_FRESHNESS:-90}
}

probe_validate_config() {
  local normalized_segments
  validate_image_name "$PROBE_IMAGE" || die "Invalid probe image name: $PROBE_IMAGE"
  validate_container_name "$PROBE_CONTAINER" || die "Invalid container name: $PROBE_CONTAINER"
  validate_container_name "$PROBE_STATE_VOLUME" || die "Invalid state volume name: $PROBE_STATE_VOLUME"
  [[ -n "$PROBE_NAME" && ${#PROBE_NAME} -le 255 ]] ||
    die "Probe name must contain 1-255 characters."
  [[ -n "$PROBE_NETWORK_SEGMENTS" ]] ||
    die "--network-segments is required; an empty local execution scope is fail-closed."
  normalized_segments="$(normalize_cidr_csv "$PROBE_NETWORK_SEGMENTS")" ||
    die "Network segments must be a comma-separated list of valid IPv4/IPv6 CIDRs."
  PROBE_NETWORK_SEGMENTS=$normalized_segments
  validate_positive_int "$PROBE_MAX_TARGETS" && (( 10#$PROBE_MAX_TARGETS <= 200000 )) ||
    die "Maximum targets must be between 1 and 200000."
  validate_positive_int "$PROBE_MAX_JOB_SECONDS" && (( 10#$PROBE_MAX_JOB_SECONDS <= 86400 )) ||
    die "Maximum job seconds must be between 1 and 86400."
  validate_positive_int "$REGISTRATION_TIMEOUT" || die "Registration timeout must be positive."
  validate_positive_int "$POLL_INTERVAL" || die "Polling interval must be positive."
}

probe_select_image_source() {
  local choice
  if ! is_interactive; then
    if docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1; then
      IMAGE_SOURCE=local
    elif [[ "$PROBE_IMAGE" == *:local* || "$PROBE_IMAGE" == vedha-probe:* ]]; then
      IMAGE_SOURCE=build
    else
      IMAGE_SOURCE=pull
    fi
    return 0
  fi
  printf '\nProbe image source\n'
  printf '1. Use an existing local image\n'
  printf '2. Build the image from the repository\n'
  printf '3. Pull the image from a registry\n'
  read -r -p 'Choice [1]: ' choice
  case "${choice:-1}" in
    1) IMAGE_SOURCE=local ;;
    2) IMAGE_SOURCE=build ;;
    3) IMAGE_SOURCE=pull ;;
    *) die "Invalid image source selection." ;;
  esac
}

probe_prepare_image() {
  case "${IMAGE_SOURCE:-local}" in
    local)
      docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1 ||
        die "Local image '$PROBE_IMAGE' does not exist."
      log_ok "Using local image $PROBE_IMAGE."
      ;;
    build)
      [[ -f "$VEDHA_ROOT/probe/Dockerfile" ]] ||
        die "Probe Dockerfile not found at probe/Dockerfile."
      if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY-RUN: docker build -t $PROBE_IMAGE $VEDHA_ROOT/probe"
      else
        docker build -t "$PROBE_IMAGE" "$VEDHA_ROOT/probe"
        log_ok "Built $PROBE_IMAGE from probe/Dockerfile."
      fi
      ;;
    pull)
      if [[ "${DRY_RUN:-false}" == "true" ]]; then
        log_info "DRY-RUN: docker pull $PROBE_IMAGE"
      else
        docker pull "$PROBE_IMAGE"
        log_ok "Pulled $PROBE_IMAGE."
      fi
      ;;
    *) die "Unsupported image source: ${IMAGE_SOURCE:-}" ;;
  esac
}

probe_container_exists() {
  docker container inspect "$PROBE_CONTAINER" >/dev/null 2>&1
}

probe_container_running() {
  [[ "$(docker inspect -f '{{.State.Running}}' "$PROBE_CONTAINER" 2>/dev/null || true)" == "true" ]]
}

probe_sanitized_logs() {
  local lines=${1:-50}
  if ! probe_container_exists; then
    log_warn "Probe container '$PROBE_CONTAINER' does not exist."
    return 1
  fi
  docker logs --tail "$lines" "$PROBE_CONTAINER" 2>&1 | sed -E \
    -e 's/(vpat_)[A-Za-z0-9_-]+/\1[REDACTED]/g' \
    -e 's/(Bearer )[A-Za-z0-9._-]+/\1[REDACTED]/g' \
    -e 's/(PROBE_LICENSE=)[^[:space:]]+/\1[REDACTED]/g' \
    -e 's/(token["=: ]+)[A-Za-z0-9._-]+/\1[REDACTED]/Ig'
}

probe_env_file() {
  local include_pat=$1 path
  local value
  for value in "$PLATFORM_URL" "$PROBE_NAME" "$PROBE_LOCATION" \
    "$PROBE_NETWORK_SEGMENTS" "$PROBE_MAX_TARGETS" "$PROBE_MAX_JOB_SECONDS" \
    "${PAT_TOKEN:-}"; do
    state_value_safe "$value" || die "Probe configuration values cannot contain newlines."
  done
  path="$(secure_temp_file)"
  {
    printf 'PLATFORM_URL=%s\n' "$PLATFORM_URL"
    printf 'VERIFY_TLS=%s\n' "$VERIFY_TLS"
    printf 'PROBE_NAME=%s\n' "$PROBE_NAME"
    printf 'PROBE_LOCATION=%s\n' "$PROBE_LOCATION"
    printf 'PROBE_NETWORK_SEGMENTS=%s\n' "$PROBE_NETWORK_SEGMENTS"
    printf 'PROBE_MAX_TARGETS=%s\n' "$PROBE_MAX_TARGETS"
    printf 'PROBE_MAX_JOB_SECONDS=%s\n' "$PROBE_MAX_JOB_SECONDS"
    printf 'LICENSE_ENFORCED=%s\n' "${LICENSE_ENFORCED:-false}"
    printf 'HW_BIND_FINGERPRINT=%s\n' "$PROBE_HW_ID"
    if [[ "${LICENSE_ENFORCED:-false}" == "true" ]]; then
      printf 'PROBE_LICENSE_FILE=/var/lib/vedha-probe/license.token\n'
      printf 'PROBE_LICENSE_PUBKEY=%s\n' "$PROBE_LICENSE_PUBKEY"
    fi
    if [[ "$include_pat" == "true" ]]; then
      printf 'OPERATOR_TOKEN=%s\n' "$PAT_TOKEN"
    fi
  } > "$path"
  chmod 600 "$path"
  printf '%s\n' "$path"
}

probe_state_volume_writable() {
  docker run --rm \
    --network none \
    --read-only \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --user 10001:10001 \
    -v "$PROBE_STATE_VOLUME:/state" \
    --entrypoint python \
    "$PROBE_IMAGE" -c \
    'import os; p="/state/.vedha-write-test"; fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600); os.close(fd); os.remove(p)' \
    >/dev/null 2>&1
}

probe_prepare_state_volume() {
  docker volume create "$PROBE_STATE_VOLUME" >/dev/null
  if probe_state_volume_writable; then
    return 0
  fi

  log_info "Migrating probe state volume ownership to runtime UID 10001."
  docker run --rm \
    --network none \
    --read-only \
    --cap-drop ALL \
    --cap-add CHOWN \
    --cap-add DAC_OVERRIDE \
    --cap-add DAC_READ_SEARCH \
    --security-opt no-new-privileges:true \
    --user 0:0 \
    -v "$PROBE_STATE_VOLUME:/state" \
    --entrypoint chown \
    "$PROBE_IMAGE" -R 10001:10001 /state >/dev/null ||
    die "Could not migrate state volume '$PROBE_STATE_VOLUME' to runtime UID 10001."
  probe_state_volume_writable ||
    die "State volume '$PROBE_STATE_VOLUME' is not writable by runtime UID 10001."
}

probe_run_container() {
  local include_pat=${1:-true} env_file
  local -a runtime_args=(
    --read-only
    --tmpfs /tmp:size=64m,mode=1777
    --cap-drop ALL
    --security-opt no-new-privileges:true
    --pids-limit 256
    --init
  )
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_info "DRY-RUN: create '$PROBE_CONTAINER' from '$PROBE_IMAGE' (secrets masked)."
    return 0
  fi
  env_file="$(probe_env_file "$include_pat")"
  probe_prepare_state_volume
  if linux_host_gateway_required; then
    docker run -d --name "$PROBE_CONTAINER" --hostname "$PROBE_CONTAINER" \
      --mac-address "$PROBE_MAC_ADDRESS" --restart unless-stopped \
      "${runtime_args[@]}" \
      --add-host host.docker.internal:host-gateway --env-file "$env_file" \
      -v "$PROBE_STATE_VOLUME:/var/lib/vedha-probe" \
      "$PROBE_IMAGE" >/dev/null
  else
    docker run -d --name "$PROBE_CONTAINER" --hostname "$PROBE_CONTAINER" \
      --mac-address "$PROBE_MAC_ADDRESS" --restart unless-stopped \
      "${runtime_args[@]}" \
      --env-file "$env_file" -v "$PROBE_STATE_VOLUME:/var/lib/vedha-probe" \
      "$PROBE_IMAGE" >/dev/null
  fi
  rm -f -- "$env_file"
  log_ok "Started probe container '$PROBE_CONTAINER'."
}

probe_remove_container() {
  probe_container_exists || return 0
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_info "DRY-RUN: remove container '$PROBE_CONTAINER'."
    return 0
  fi
  docker rm -f "$PROBE_CONTAINER" >/dev/null
}

probe_existing_install_action() {
  local choice
  probe_container_exists || return 0
  if ! is_interactive; then
    [[ "${FORCE:-false}" == "true" ]] ||
      die "Container '$PROBE_CONTAINER' already exists. Use --force to recreate it."
    EXISTING_ACTION=recreate
    return 0
  fi
  printf '\nExisting container %s detected\n' "$PROBE_CONTAINER"
  printf '1. Restart the existing container\n'
  printf '2. Recreate the container\n'
  printf '3. Re-register the existing probe\n'
  printf '4. Cancel\n'
  read -r -p 'Choice: ' choice
  case "$choice" in
    1) EXISTING_ACTION=restart ;;
    2) EXISTING_ACTION=recreate ;;
    3) EXISTING_ACTION=reregister ;;
    4) EXISTING_ACTION=cancel ;;
    *) die "Invalid existing-container selection." ;;
  esac
}

probe_clear_identity() {
  [[ "${FORCE:-false}" == "true" ]] ||
    confirm_action "Clear the cached probe identity and re-register it?" ||
    die "Re-registration cancelled."
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_info "DRY-RUN: clear state.json in volume '$PROBE_STATE_VOLUME'."
    return 0
  fi
  if probe_container_running; then
    docker stop "$PROBE_CONTAINER" >/dev/null
  fi
  probe_prepare_state_volume
  docker run --rm --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --user 10001:10001 \
    -v "$PROBE_STATE_VOLUME:/state" --entrypoint python "$PROBE_IMAGE" \
    -c 'import os; p="/state/state.json"; os.path.exists(p) and os.remove(p)' >/dev/null
}

probe_seal_registration() {
  [[ "${DRY_RUN:-false}" == "true" ]] && return 0
  log_info "Removing the bootstrap PAT from persistent container metadata."
  probe_remove_container
  probe_run_container false
}

probe_volume_has_identity() {
  docker volume inspect "$PROBE_STATE_VOLUME" >/dev/null 2>&1 || return 1
  docker run --rm --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --user 10001:10001 \
    -v "$PROBE_STATE_VOLUME:/state:ro" --entrypoint python \
    "$PROBE_IMAGE" -c \
    'import json; d=json.load(open("/state/state.json",encoding="utf-8")); raise SystemExit(0 if d.get("agent_id") and d.get("token") else 1)' \
    >/dev/null 2>&1
}

probe_abort_bootstrap() {
  log_warn "Bootstrap did not verify; removing the container copy that contains the PAT."
  probe_remove_container
  if probe_volume_has_identity; then
    log_info "A registered agent identity exists; restarting without the bootstrap PAT."
    probe_run_container false
  else
    log_warn "No registered identity was saved; the failed probe container remains removed."
  fi
}

probe_restart() {
  probe_container_exists || die "Probe container '$PROBE_CONTAINER' does not exist."
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_info "DRY-RUN: docker restart $PROBE_CONTAINER"
  else
    docker restart "$PROBE_CONTAINER" >/dev/null
    log_ok "Restarted '$PROBE_CONTAINER'."
  fi
}

probe_status() {
  if ! probe_container_exists; then
    log_warn "Probe container '$PROBE_CONTAINER' is not installed."
    return 1
  fi
  local status image started
  status="$(docker inspect -f '{{.State.Status}}' "$PROBE_CONTAINER")"
  image="$(docker inspect -f '{{.Config.Image}}' "$PROBE_CONTAINER")"
  started="$(docker inspect -f '{{.State.StartedAt}}' "$PROBE_CONTAINER")"
  printf 'Container: %s\nStatus:    %s\nImage:     %s\nStarted:   %s\n' \
    "$PROBE_CONTAINER" "$status" "$image" "$started"
  [[ "$status" == "running" ]]
}

probe_uninstall() {
  probe_container_exists || {
    log_info "Probe container '$PROBE_CONTAINER' is already absent."
    return 0
  }
  [[ "${FORCE:-false}" == "true" ]] ||
    confirm_action "Remove probe container '$PROBE_CONTAINER'?" ||
    die "Uninstall cancelled."
  probe_remove_container
  log_ok "Removed probe container '$PROBE_CONTAINER'."
  log_info "State volume '$PROBE_STATE_VOLUME' was preserved for recovery."
  if is_interactive && confirm_action "Also permanently remove the probe state volume?"; then
    docker volume rm "$PROBE_STATE_VOLUME" >/dev/null
    log_ok "Removed state volume '$PROBE_STATE_VOLUME'."
  fi
}
