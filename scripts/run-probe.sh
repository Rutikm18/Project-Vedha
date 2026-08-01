#!/usr/bin/env bash
# Vedha Probe Manager — secure bootstrap and lifecycle automation.
set -Eeuo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"
# shellcheck source=scripts/lib/manager.sh
source "$SCRIPT_DIR/lib/manager.sh"
# shellcheck source=scripts/lib/auth.sh
source "$SCRIPT_DIR/lib/auth.sh"
# shellcheck source=scripts/lib/license.sh
source "$SCRIPT_DIR/lib/license.sh"
# shellcheck source=scripts/lib/probe.sh
source "$SCRIPT_DIR/lib/probe.sh"
# shellcheck source=scripts/lib/verify.sh
source "$SCRIPT_DIR/lib/verify.sh"

COMMAND=
NON_INTERACTIVE=false
DRY_RUN=false
FORCE=false
VERBOSE=false
INSTALL_MODE=

usage() {
  cat <<'EOF'
Usage:
  ./scripts/run-probe.sh
  ./scripts/run-probe.sh <command> [options]

Commands:
  install      Install and register a probe
  status       Show container and manager registration status
  logs         Show sanitized probe logs
  restart      Restart the probe container
  register     Re-register an existing probe
  uninstall    Remove the probe container (state is preserved by default)
  doctor       Run read-only diagnostics

Options:
  --manager-url URL       Host-visible manager API
  --platform-url URL      Manager URL visible inside the probe container
  --admin-email EMAIL     Admin account used only to create a PAT
  --pat TOKEN             Existing PAT (prefer VEDHA_PAT to avoid shell history)
  --probe-image IMAGE     Probe image tag or registry reference
  --probe-container NAME  Container name
  --state-volume NAME     Persistent probe state volume
  --probe-name NAME       Probe display name
  --probe-location TEXT   Probe location label
  --network-segments CSV  Authorized local IPv4/IPv6 CIDR ceiling (required)
  --max-targets COUNT     Per-job target ceiling (default: 4096)
  --max-job-seconds SEC   Per-job runtime ceiling (default: 7200)
  --customer NAME         License customer name
  --license-days DAYS     License validity
  --timeout SECONDS       Registration timeout
  --poll-interval SEC     Registration polling interval
  --non-interactive       Never prompt
  --dry-run               Show sanitized install actions without mutation
  --force                 Confirm destructive lifecycle actions
  --verbose               Include sanitized diagnostic detail
  --help                  Show this help

Secret inputs:
  VEDHA_ADMIN_PASSWORD    Admin password for PAT creation
  VEDHA_PAT               Existing PAT
  VEDHA_PROBE_LICENSE     Existing signed probe license
EOF
}

need_option_value() {
  [[ $# -ge 2 && -n "$2" ]] || die "Option '$1' requires a value."
}

parse_args() {
  while (( $# > 0 )); do
    case "$1" in
      install|status|logs|restart|register|uninstall|doctor)
        [[ -z "$COMMAND" ]] || die "Only one command may be specified."
        COMMAND=$1
        shift
        ;;
      --manager-url) need_option_value "$@"; MANAGER_API_URL=$2; shift 2 ;;
      --platform-url) need_option_value "$@"; PLATFORM_URL=$2; shift 2 ;;
      --admin-email) need_option_value "$@"; ADMIN_EMAIL=$2; shift 2 ;;
      --pat)
        need_option_value "$@"
        PAT_TOKEN=$2
        log_warn "--pat can be retained in shell history/process listings; prefer VEDHA_PAT."
        shift 2
        ;;
      --probe-image) need_option_value "$@"; PROBE_IMAGE=$2; shift 2 ;;
      --probe-container) need_option_value "$@"; PROBE_CONTAINER=$2; shift 2 ;;
      --state-volume) need_option_value "$@"; PROBE_STATE_VOLUME=$2; shift 2 ;;
      --probe-name) need_option_value "$@"; PROBE_NAME=$2; shift 2 ;;
      --probe-location) need_option_value "$@"; PROBE_LOCATION=$2; shift 2 ;;
      --network-segments) need_option_value "$@"; PROBE_NETWORK_SEGMENTS=$2; shift 2 ;;
      --max-targets) need_option_value "$@"; PROBE_MAX_TARGETS=$2; shift 2 ;;
      --max-job-seconds) need_option_value "$@"; PROBE_MAX_JOB_SECONDS=$2; shift 2 ;;
      --customer) need_option_value "$@"; CUSTOMER_NAME=$2; shift 2 ;;
      --license-days) need_option_value "$@"; LICENSE_DAYS=$2; shift 2 ;;
      --timeout) need_option_value "$@"; REGISTRATION_TIMEOUT=$2; shift 2 ;;
      --poll-interval) need_option_value "$@"; POLL_INTERVAL=$2; shift 2 ;;
      --non-interactive) NON_INTERACTIVE=true; shift ;;
      --dry-run) DRY_RUN=true; shift ;;
      --force) FORCE=true; shift ;;
      --verbose) VERBOSE=true; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown argument: $1" ;;
    esac
  done
}

initialize_config() {
  load_state
  manager_defaults
  probe_defaults
  PAT_NAME=${PAT_NAME:-Vedha Probe CLI}
  PAT_DAYS=${PAT_DAYS:-90}
  LICENSE_DAYS=${LICENSE_DAYS:-365}
  CUSTOMER_NAME=${CUSTOMER_NAME:-Vedha Local Lab}
}

interactive_menu() {
  local choice
  cat <<'EOF'
Vedha Probe Manager

1. Install and register a local probe
2. Install and register a remote probe
3. Re-register an existing probe
4. Check probe status
5. View probe logs
6. Restart probe
7. Run diagnostics
8. Remove probe
9. Exit
EOF
  read -r -p 'Choice: ' choice
  case "$choice" in
    1) COMMAND=install; INSTALL_MODE=local ;;
    2) COMMAND=install; INSTALL_MODE=remote; MANAGER_API_URL=; PLATFORM_URL= ;;
    3) COMMAND=register ;;
    4) COMMAND=status ;;
    5) COMMAND=logs ;;
    6) COMMAND=restart ;;
    7) COMMAND=doctor ;;
    8) COMMAND=uninstall ;;
    9) exit 0 ;;
    *) die "Invalid menu selection." ;;
  esac
}

preflight() {
  local command
  for command in bash docker curl python3; do
    require_command "$command"
  done
  docker info >/dev/null 2>&1 ||
    die "Docker daemon is not running. Start Docker Desktop/Engine."
  [[ -f "$VEDHA_ROOT/probe/tools/issue_license.py" ]] ||
    die "Required license tool is missing."
  [[ -f "$VEDHA_ROOT/probe/Dockerfile" ]] ||
    die "Required probe Dockerfile is missing."
}

prompt_install_config() {
  if [[ "$INSTALL_MODE" == "remote" ]]; then
    prompt_value MANAGER_API_URL "Manager API URL (host-visible)"
    prompt_value PLATFORM_URL "Platform URL visible from the remote probe"
  else
    prompt_value MANAGER_API_URL "Manager API URL (host-visible)" "$MANAGER_API_URL"
    prompt_value PLATFORM_URL "Platform URL visible from the probe container" "$PLATFORM_URL"
  fi
  prompt_value PROBE_IMAGE "Probe image" "$PROBE_IMAGE"
  prompt_value PROBE_CONTAINER "Probe container name" "$PROBE_CONTAINER"
  prompt_value PROBE_NAME "Probe display name" "$PROBE_NAME"
  prompt_value PROBE_LOCATION "Probe location" "$PROBE_LOCATION"
  prompt_value PROBE_NETWORK_SEGMENTS "Reachable network segments (comma-separated)" "$PROBE_NETWORK_SEGMENTS"
  prompt_value CUSTOMER_NAME "License customer" "$CUSTOMER_NAME"
  prompt_value LICENSE_DAYS "License validity in days" "$LICENSE_DAYS"
}

show_dry_run_plan() {
  cat <<EOF
[INFO] DRY-RUN plan
  Repository:      $VEDHA_ROOT
  Manager API:     $MANAGER_API_URL
  Probe platform:  $PLATFORM_URL
  Image:           $PROBE_IMAGE (${IMAGE_SOURCE:-auto})
  Container:       $PROBE_CONTAINER
  State volume:    $PROBE_STATE_VOLUME
  Probe name:      $PROBE_NAME
  Local scope:     $PROBE_NETWORK_SEGMENTS
  Target ceiling:  $PROBE_MAX_TARGETS
  Job deadline:    ${PROBE_MAX_JOB_SECONDS}s
  License:         ${LICENSE_ENFORCED:-auto/local-development}
  PAT:             create or validate without persisting the secret

No PAT, license, image, container, registration, or state mutation was performed.
EOF
}

install_command() {
  preflight
  prompt_install_config
  manager_validate_urls
  probe_validate_config
  probe_select_image_source

  if [[ "$DRY_RUN" == "true" ]]; then
    show_dry_run_plan
    return 0
  fi

  probe_prepare_image
  manager_health
  manager_login_endpoint_check
  if ! manager_container_connectivity; then
    die "A probe container cannot reach $PLATFORM_URL. Check host-gateway/DNS and the platform URL."
  fi

  EXISTING_ACTION=
  probe_existing_install_action
  case "${EXISTING_ACTION:-}" in
    restart)
      probe_restart
      probe_status
      return 0
      ;;
    cancel) die "Installation cancelled." ;;
  esac

  auth_prepare_pat
  save_state
  probe_collect_identity
  probe_prepare_state_volume
  license_prepare
  license_store_in_volume

  if [[ "${EXISTING_ACTION:-}" == "reregister" ]]; then
    probe_clear_identity
    probe_remove_container
  elif [[ "${EXISTING_ACTION:-}" == "recreate" ]]; then
    probe_remove_container
  fi

  probe_run_container true
  if ! verify_registration; then
    probe_abort_bootstrap
    die "Probe startup could not be verified."
  fi
  probe_seal_registration
  verify_registration
  save_state

  PAT_TOKEN=
  PROBE_LICENSE=
  log_ok "Probe bootstrap completed."
  log_info "Dashboard: Scanner page → probe '$PROBE_NAME' should show ONLINE."
}

register_command() {
  preflight
  manager_validate_urls
  probe_validate_config
  docker image inspect "$PROBE_IMAGE" >/dev/null 2>&1 ||
    die "Probe image '$PROBE_IMAGE' is unavailable."
  probe_container_exists || die "Probe container '$PROBE_CONTAINER' is not installed."
  auth_prepare_pat
  save_state
  probe_collect_identity
  probe_prepare_state_volume
  license_prepare
  license_store_in_volume
  probe_clear_identity
  probe_remove_container
  probe_run_container true
  if ! verify_registration; then
    probe_abort_bootstrap
    die "Probe re-registration could not be verified."
  fi
  probe_seal_registration
  verify_registration
  save_state
  PAT_TOKEN=
  PROBE_LICENSE=
  log_ok "Probe re-registration completed."
}

status_command() {
  probe_status
  PAT_TOKEN=${PAT_TOKEN:-${VEDHA_PAT:-${PROBE_PAT:-}}}
  if [[ -n "$PAT_TOKEN" ]]; then
    auth_validate_pat
    if verify_fetch_agent; then
      IFS='|' read -r id online status age heartbeat <<< "$VERIFY_AGENT_RESULT"
      if [[ "$online" == "true" ]]; then
        printf 'Agent ID:  %s\nManager:   online (heartbeat %ss ago)\n' "$id" "$age"
      else
        printf 'Agent ID:  %s\nManager:   %s (heartbeat %ss ago)\n' "$id" "$status" "$age"
      fi
    else
      log_warn "Manager registration was not found or its heartbeat is stale."
    fi
  else
    log_info "Set VEDHA_PAT to include manager-side registration verification."
  fi
}

dispatch() {
  case "$COMMAND" in
    install) install_command ;;
    status) status_command ;;
    logs) probe_sanitized_logs 100 ;;
    restart) probe_restart; probe_status ;;
    register) register_command ;;
    uninstall) probe_uninstall ;;
    doctor) doctor_command ;;
    *) die "Unsupported command: $COMMAND" ;;
  esac
}

main() {
  install_cleanup_traps
  parse_args "$@"
  initialize_config
  if [[ -z "$COMMAND" ]]; then
    is_interactive || {
      usage >&2
      die "A command is required in non-interactive mode."
    }
    interactive_menu
  fi
  dispatch
}

main "$@"
