#!/usr/bin/env bash
# Shared logging, validation, state, prompts, and cleanup.
set -Eeuo pipefail

VEDHA_SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
VEDHA_ROOT="$(CDPATH= cd -- "$VEDHA_SCRIPT_DIR/.." && pwd)"
VEDHA_STATE_DIR=${VEDHA_STATE_DIR:-"$VEDHA_SCRIPT_DIR/state"}
VEDHA_STATE_FILE=${VEDHA_STATE_FILE:-"$VEDHA_STATE_DIR/probe.env"}

declare -a VEDHA_TEMP_FILES=()
VEDHA_TEMP_REGISTRY=

log_info() { printf '[INFO] %s\n' "$*"; }
log_ok() { printf '[OK] %s\n' "$*"; }
log_warn() { printf '[WARN] %s\n' "$*" >&2; }
log_error() { printf '[ERROR] %s\n' "$*" >&2; }
die() { log_error "$*"; return 1; }

cleanup_temp_files() {
  local path
  for path in "${VEDHA_TEMP_FILES[@]:-}"; do
    [[ -n "$path" ]] && rm -f -- "$path"
  done
  if [[ -n "${VEDHA_TEMP_REGISTRY:-}" && -f "$VEDHA_TEMP_REGISTRY" ]]; then
    while IFS= read -r path || [[ -n "$path" ]]; do
      [[ -n "$path" ]] && rm -f -- "$path"
    done < "$VEDHA_TEMP_REGISTRY"
    rm -f -- "$VEDHA_TEMP_REGISTRY"
  fi
  VEDHA_TEMP_FILES=()
}

on_error() {
  local exit_code=$?
  log_error "Command failed near line ${BASH_LINENO[0]:-unknown} (exit $exit_code)."
  return "$exit_code"
}

on_signal() {
  log_warn "Interrupted; cleaning up protected temporary files."
  cleanup_temp_files
  exit 130
}

install_cleanup_traps() {
  VEDHA_TEMP_REGISTRY="$(mktemp "${TMPDIR:-/tmp}/vedha-probe-registry.XXXXXX")"
  chmod 600 "$VEDHA_TEMP_REGISTRY"
  trap on_error ERR
  trap cleanup_temp_files EXIT
  trap on_signal INT TERM
}

secure_temp_file() {
  local path
  path="$(mktemp "${TMPDIR:-/tmp}/vedha-probe.XXXXXX")"
  chmod 600 "$path"
  VEDHA_TEMP_FILES+=("$path")
  [[ -n "${VEDHA_TEMP_REGISTRY:-}" ]] && printf '%s\n' "$path" >> "$VEDHA_TEMP_REGISTRY"
  printf '%s\n' "$path"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "Required command '$1' was not found."
}

is_interactive() {
  [[ "${NON_INTERACTIVE:-false}" != "true" && -t 0 && -t 1 ]]
}

prompt_value() {
  local variable=$1 label=$2 default_value=${3:-} answer
  [[ -n "${!variable:-}" ]] && return 0
  if ! is_interactive; then
    [[ -n "$default_value" ]] && printf -v "$variable" '%s' "$default_value"
    return 0
  fi
  if [[ -n "$default_value" ]]; then
    read -r -p "$label [$default_value]: " answer
    printf -v "$variable" '%s' "${answer:-$default_value}"
  else
    read -r -p "$label: " answer
    printf -v "$variable" '%s' "$answer"
  fi
}

prompt_secret() {
  local variable=$1 label=$2 answer
  [[ -n "${!variable:-}" ]] && return 0
  if ! is_interactive; then
    return 1
  fi
  read -r -s -p "$label: " answer
  printf '\n' >&2
  printf -v "$variable" '%s' "$answer"
}

confirm_action() {
  local prompt=$1 default=${2:-no} answer
  [[ "${FORCE:-false}" == "true" ]] && return 0
  if ! is_interactive; then
    return 1
  fi
  if [[ "$default" == "yes" ]]; then
    read -r -p "$prompt [Y/n]: " answer
    [[ -z "$answer" || "$answer" =~ ^[Yy]([Ee][Ss])?$ ]]
  else
    read -r -p "$prompt [y/N]: " answer
    [[ "$answer" =~ ^[Yy]([Ee][Ss])?$ ]]
  fi
}

mask_secret() {
  local value=${1:-} visible=${2:-12}
  if [[ -z "$value" ]]; then
    printf '<not set>'
  elif (( ${#value} <= visible )); then
    printf '%s...' "${value:0:4}"
  else
    printf '%s...' "${value:0:visible}"
  fi
}

validate_url() {
  [[ "$1" =~ ^https?://[^[:space:]/]+(:[0-9]+)?(/.*)?$ ]]
}

is_loopback_url() {
  [[ "$1" =~ ^http://(localhost|127\.0\.0\.1|\[::1\])(:[0-9]+)?(/.*)?$ ]]
}

is_local_platform_url() {
  [[ "$1" =~ ^http://(localhost|127\.0\.0\.1|host\.docker\.internal|api)(:[0-9]+)?(/.*)?$ ]]
}

validate_positive_int() {
  [[ "$1" =~ ^[0-9]+$ ]] && (( 10#$1 > 0 ))
}

normalize_cidr_csv() {
  python3 - "$1" <<'PY'
import ipaddress
import sys

raw = sys.argv[1]
parts = raw.split(",")
if not raw.strip() or any(not part.strip() for part in parts):
    raise SystemExit(1)

networks = []
for part in parts:
    try:
        network = str(ipaddress.ip_network(part.strip(), strict=False))
    except ValueError:
        raise SystemExit(1)
    if network not in networks:
        networks.append(network)

print(",".join(networks))
PY
}

validate_container_name() {
  [[ "$1" =~ ^[A-Za-z0-9][A-Za-z0-9_.-]*$ ]]
}

validate_image_name() {
  [[ "$1" =~ ^[A-Za-z0-9][A-Za-z0-9._/:@-]*$ ]]
}

validate_host_id() {
  [[ "$1" =~ ^[a-f0-9]{24}$ ]]
}

validate_hw_id() {
  [[ "$1" =~ ^[a-f0-9]{32}$ ]]
}

sanitize_single_line() {
  printf '%s' "$1" | tr '\r\n' '  ' | cut -c1-300
}

state_assign() {
  local key=$1 value=$2
  case "$key" in
    MANAGER_API_URL|PLATFORM_URL|PROBE_IMAGE|PROBE_CONTAINER|PROBE_HOST_ID|\
    PROBE_HW_ID|PROBE_MAC_ADDRESS|PROBE_NAME|PROBE_LOCATION|PROBE_NETWORK_SEGMENTS|\
    PROBE_MAX_TARGETS|PROBE_MAX_JOB_SECONDS|PROBE_STATE_VOLUME|PROBE_AGENT_ID|\
    PROBE_LICENSE_PUBKEY|PAT_ID|PAT_PREFIX|CUSTOMER_NAME|LICENSE_DAYS|LICENSE_ENFORCED)
      if [[ -z "${!key:-}" ]]; then
        printf -v "$key" '%s' "$value"
      fi
      ;;
  esac
  return 0
}

load_state() {
  local line key value
  [[ -f "$VEDHA_STATE_FILE" ]] || return 0
  while IFS= read -r line || [[ -n "$line" ]]; do
    [[ -z "$line" || "$line" == \#* || "$line" != *=* ]] && continue
    key=${line%%=*}
    value=${line#*=}
    state_assign "$key" "$value"
  done < "$VEDHA_STATE_FILE"
}

state_value_safe() {
  [[ "$1" != *$'\n'* && "$1" != *$'\r'* ]]
}

save_state() {
  [[ "${DRY_RUN:-false}" == "true" ]] && return 0
  local tmp key value
  mkdir -p "$VEDHA_STATE_DIR"
  chmod 700 "$VEDHA_STATE_DIR"
  tmp="$(secure_temp_file)"
  {
    printf '# Non-sensitive Vedha probe bootstrap state. Do not add secrets.\n'
    for key in \
      MANAGER_API_URL PLATFORM_URL PROBE_IMAGE PROBE_CONTAINER PROBE_HOST_ID \
      PROBE_HW_ID PROBE_MAC_ADDRESS PROBE_NAME PROBE_LOCATION \
      PROBE_NETWORK_SEGMENTS PROBE_MAX_TARGETS PROBE_MAX_JOB_SECONDS \
      PROBE_STATE_VOLUME PAT_ID PAT_PREFIX PROBE_AGENT_ID PROBE_LICENSE_PUBKEY \
      CUSTOMER_NAME LICENSE_DAYS LICENSE_ENFORCED; do
      value=${!key:-}
      state_value_safe "$value" || die "State value for $key contains a newline."
      printf '%s=%s\n' "$key" "$value"
    done
  } > "$tmp"
  chmod 600 "$tmp"
  mv -f "$tmp" "$VEDHA_STATE_FILE"
  chmod 600 "$VEDHA_STATE_FILE"
}

python_json_field() {
  local file=$1 expression=$2
  python3 - "$file" "$expression" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    data = json.load(handle)

value = data
for part in sys.argv[2].split("."):
    if not part:
        continue
    if isinstance(value, dict):
        value = value.get(part)
    else:
        value = None
        break

if value is None:
    print("")
elif isinstance(value, (dict, list)):
    print(json.dumps(value, separators=(",", ":")))
else:
    print(value)
PY
}

api_error_summary() {
  local file=$1
  python3 - "$file" <<'PY'
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as handle:
        body = json.load(handle)
    detail = body.get("detail") or body.get("error") or body.get("message")
    if isinstance(detail, list):
        detail = "; ".join(str(x.get("msg", x)) if isinstance(x, dict) else str(x) for x in detail[:3])
    print(str(detail or "request failed")[:300].replace("\n", " "))
except Exception:
    print("request failed with a non-JSON response")
PY
}

run_or_plan() {
  if [[ "${DRY_RUN:-false}" == "true" ]]; then
    log_info "DRY-RUN: $*"
    return 0
  fi
  "$@"
}
