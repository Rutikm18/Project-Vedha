#!/usr/bin/env bash
# JWT login and least-privilege PAT lifecycle.
set -Eeuo pipefail

PAT_SCOPES_JSON='["probe:read","probe:write","probe:register","engagement:read","engagement:write"]'

auth_curl() {
  local method=$1 url=$2 token=$3 response=$4 body_file=${5:-}
  local config
  config="$(secure_temp_file)"
  {
    printf 'silent\nshow-error\nconnect-timeout = 5\nmax-time = 20\n'
    printf 'header = "Authorization: Bearer %s"\n' "$token"
    printf 'header = "Content-Type: application/json"\n'
  } > "$config"
  if [[ -n "$body_file" ]]; then
    HTTP_CODE="$(curl --config "$config" -o "$response" -w '%{http_code}' \
      -X "$method" --data-binary "@$body_file" "$url" 2>/dev/null || printf '000')"
  else
    HTTP_CODE="$(curl --config "$config" -o "$response" -w '%{http_code}' \
      -X "$method" "$url" 2>/dev/null || printf '000')"
  fi
}

env_file_value() {
  local key=$1
  [[ -f "$VEDHA_ROOT/.env" ]] || return 0
  python3 - "$VEDHA_ROOT/.env" "$key" <<'PY'
import sys

path, wanted = sys.argv[1:]
with open(path, encoding="utf-8") as handle:
    for raw in handle:
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == wanted:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1]
            print(value)
            break
PY
}

auth_resolve_admin_credentials() {
  ADMIN_EMAIL=${ADMIN_EMAIL:-${SEED_ADMIN_EMAIL:-}}
  [[ -n "$ADMIN_EMAIL" ]] || ADMIN_EMAIL="$(env_file_value SEED_ADMIN_EMAIL)"
  ADMIN_EMAIL=${ADMIN_EMAIL:-admin@vedha.io}

  ADMIN_PASSWORD=${VEDHA_ADMIN_PASSWORD:-${ADMIN_PASSWORD:-${SEED_ADMIN_PASSWORD:-}}}
  [[ -n "${ADMIN_PASSWORD:-}" ]] || ADMIN_PASSWORD="$(env_file_value SEED_ADMIN_PASSWORD)"
  if [[ -z "${ADMIN_PASSWORD:-}" ]]; then
    prompt_secret ADMIN_PASSWORD "Admin password for $ADMIN_EMAIL" ||
      die "Admin password is required via secure prompt or VEDHA_ADMIN_PASSWORD."
  fi
}

auth_login() {
  local request response code
  auth_resolve_admin_credentials
  request="$(secure_temp_file)"
  response="$(secure_temp_file)"
  EMAIL="$ADMIN_EMAIL" PASSWORD="$ADMIN_PASSWORD" python3 - "$request" <<'PY'
import json
import os
import sys

with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump({"email": os.environ["EMAIL"], "password": os.environ["PASSWORD"]}, handle)
PY
  code="$(curl -sS --connect-timeout 5 --max-time 20 -o "$response" -w '%{http_code}' \
    -X POST -H 'Content-Type: application/json' --data-binary "@$request" \
    "$MANAGER_API_URL/auth/login" 2>/dev/null || printf '000')"
  ADMIN_PASSWORD=
  if [[ "$code" != "200" ]]; then
    die "Manager login failed (HTTP $code): $(api_error_summary "$response")"
  fi
  ACCESS_TOKEN="$(python_json_field "$response" access_token)"
  [[ -n "$ACCESS_TOKEN" ]] || die "Login response did not contain an access token."
  log_ok "Authenticated to the manager as $ADMIN_EMAIL."
}

auth_validate_pat() {
  local response
  response="$(secure_temp_file)"
  auth_curl GET "$MANAGER_API_URL/auth/me" "$PAT_TOKEN" "$response"
  if [[ "$HTTP_CODE" != "200" ]]; then
    die "PAT was rejected (HTTP $HTTP_CODE): $(api_error_summary "$response")"
  fi
  local auth_type
  auth_type="$(python_json_field "$response" auth_type)"
  [[ "$auth_type" == "pat" ]] || die "The supplied credential is not a personal access token."
  if ! python3 - "$response" "$PAT_SCOPES_JSON" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    actual = set(json.load(handle).get("scopes") or [])
required = set(json.loads(sys.argv[2]))
missing = sorted(required - actual)
if missing:
    print(", ".join(missing))
    raise SystemExit(1)
PY
  then
    die "PAT is valid but does not have every required probe CLI scope."
  fi
  PAT_ID="$(python_json_field "$response" pat_id)"
  PAT_PREFIX="$(mask_secret "$PAT_TOKEN" 16)"
  log_ok "PAT accepted: $(mask_secret "$PAT_TOKEN" 16)"
}

auth_find_existing_pat() {
  local response
  response="$(secure_temp_file)"
  auth_curl GET "$MANAGER_API_URL/auth/personal-access-tokens" "$ACCESS_TOKEN" "$response"
  [[ "$HTTP_CODE" == "200" ]] || die "Could not list PAT metadata (HTTP $HTTP_CODE): $(api_error_summary "$response")"
  EXISTING_PAT_META="$(python3 - "$response" "${PAT_NAME:-Vedha Probe CLI}" <<'PY'
import datetime as dt
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    rows = json.load(handle)
name = sys.argv[2]
now = dt.datetime.now(dt.timezone.utc)
for row in rows:
    expiry = row.get("expires_at")
    active = not row.get("revoked_at")
    if expiry:
        active = active and dt.datetime.fromisoformat(expiry.replace("Z", "+00:00")) > now
    if active and row.get("name") == name:
        print(f"{row.get('id','')}|{row.get('token_prefix','')}")
        break
PY
)"
}

auth_create_pat() {
  local request response
  request="$(secure_temp_file)"
  response="$(secure_temp_file)"
  PAT_NAME=${PAT_NAME:-Vedha Probe CLI}
  PAT_DAYS=${PAT_DAYS:-90}
  validate_positive_int "$PAT_DAYS" || die "PAT expiry days must be a positive integer."
  (( PAT_DAYS <= 365 )) || die "PAT expiry cannot exceed 365 days."

  NAME="$PAT_NAME" DAYS="$PAT_DAYS" SCOPES="$PAT_SCOPES_JSON" \
    python3 - "$request" <<'PY'
import json
import os
import sys

with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump({
        "name": os.environ["NAME"],
        "scopes": json.loads(os.environ["SCOPES"]),
        "expires_in_days": int(os.environ["DAYS"]),
    }, handle)
PY
  auth_curl POST "$MANAGER_API_URL/auth/personal-access-tokens" \
    "$ACCESS_TOKEN" "$response" "$request"
  if [[ "$HTTP_CODE" != "201" ]]; then
    die "PAT creation failed (HTTP $HTTP_CODE): $(api_error_summary "$response")"
  fi
  PAT_TOKEN="$(python_json_field "$response" token)"
  PAT_ID="$(python_json_field "$response" id)"
  PAT_PREFIX="$(python_json_field "$response" token_prefix)"
  [[ "$PAT_TOKEN" == vpat_* && -n "$PAT_ID" ]] ||
    die "PAT creation response was incomplete."
  log_ok "Created least-privilege PAT $(mask_secret "$PAT_TOKEN" 16) for $PAT_DAYS days."
}

auth_choose_pat_interactive() {
  local choice
  printf '\nPersonal Access Token\n'
  printf '1. Create a new PAT\n'
  printf '2. Enter an existing PAT\n'
  printf '3. Reuse PAT from VEDHA_PAT/PROBE_PAT when available\n'
  read -r -p 'Choice [1]: ' choice
  choice=${choice:-1}
  case "$choice" in
    1) PAT_MODE=create ;;
    2)
      prompt_secret PAT_TOKEN "Existing PAT (vpat_...)" ||
        die "An existing PAT is required."
      PAT_MODE=existing
      ;;
    3)
      PAT_TOKEN=${VEDHA_PAT:-${PROBE_PAT:-}}
      [[ -n "$PAT_TOKEN" ]] || die "VEDHA_PAT or PROBE_PAT is not set."
      PAT_MODE=existing
      ;;
    *) die "Invalid PAT selection." ;;
  esac
}

auth_prepare_pat() {
  PAT_TOKEN=${PAT_TOKEN:-${VEDHA_PAT:-${PROBE_PAT:-}}}
  if [[ -n "$PAT_TOKEN" ]]; then
    auth_validate_pat
    return 0
  fi

  PAT_MODE=${PAT_MODE:-}
  if is_interactive && [[ -z "$PAT_MODE" ]]; then
    auth_choose_pat_interactive
  fi
  PAT_MODE=${PAT_MODE:-create}
  if [[ "$PAT_MODE" == "existing" ]]; then
    [[ -n "$PAT_TOKEN" ]] || prompt_secret PAT_TOKEN "Existing PAT (vpat_...)"
    [[ -n "$PAT_TOKEN" ]] || die "No PAT was provided."
    auth_validate_pat
    return 0
  fi

  auth_login
  auth_find_existing_pat
  if [[ -n "$EXISTING_PAT_META" ]]; then
    PAT_ID=${EXISTING_PAT_META%%|*}
    PAT_PREFIX=${EXISTING_PAT_META#*|}
    if ! is_interactive; then
      die "An active '$PAT_NAME' PAT already exists ($PAT_PREFIX...). Provide it via VEDHA_PAT to avoid a duplicate."
    fi
    log_warn "An active '$PAT_NAME' PAT already exists ($PAT_PREFIX...)."
    if confirm_action "Create another PAT anyway?"; then
      auth_create_pat
    else
      prompt_secret PAT_TOKEN "Enter the existing PAT value" ||
        die "Installation cancelled to avoid creating a duplicate PAT."
      auth_validate_pat
    fi
  else
    auth_create_pat
  fi
  ACCESS_TOKEN=
}
