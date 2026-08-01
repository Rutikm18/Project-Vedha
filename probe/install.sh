#!/usr/bin/env sh
# Vedha probe installer — one command, no source tree on the client.
#
#   Fastest (one line, set vars):
#     curl -fsSL https://YOUR_HOST/install.sh | \
#       PLATFORM_URL=https://manager.example.com \
#       OPERATOR_TOKEN=vpat_xxx \
#       PROBE_NETWORK_SEGMENTS=10.20.0.0/16 sh
#
#   Lab/offline image install:
#     curl -fsSL http://MAC_IP:8000/install.sh | \
#       PLATFORM_URL=http://MAC_IP:18080 \
#       OPERATOR_TOKEN=vpat_xxx \
#       PROBE_IMAGE=vedha-probe:local-amd64 \
#       PROBE_IMAGE_TAR_URL=http://MAC_IP:8000/vedha-probe-local-amd64.tar \
#       PROBE_NETWORK_SEGMENTS=MAC_IP/32 \
#       LICENSE_ENFORCED=false sh
#
#   Inspect-first (recommended for security teams):
#     curl -fsSL https://YOUR_HOST/install.sh -o install.sh
#     less install.sh           # read it
#     sh install.sh             # interactive — it asks for what it needs
#
#   Get this machine's Host ID (to request a license), no install:
#     sh install.sh hostid
set -eu

IMAGE="${PROBE_IMAGE:-vedha-probe:local}"       # local tag or registry path
NAME="${PROBE_CONTAINER:-vedha-probe}"
STATE_VOL="${PROBE_STATE_VOLUME:-vedha-probe-state}"
VERIFY_TLS="${VERIFY_TLS:-true}"
LICENSE_ENFORCED="${LICENSE_ENFORCED:-true}"
PROBE_MAX_TARGETS="${PROBE_MAX_TARGETS:-4096}"
PROBE_MAX_JOB_SECONDS="${PROBE_MAX_JOB_SECONDS:-7200}"
PROBE_REGISTRATION_TIMEOUT="${PROBE_REGISTRATION_TIMEOUT:-60}"

say() { printf '%s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

if [ "${PROBE_INSTALL_DRY_RUN:-false}" = "true" ]; then
  say "Dry run OK."
  say "Image: $IMAGE"
  say "Container: $NAME"
  say "Manager: ${PLATFORM_URL:-<not set>}"
  exit 0
fi

# --- preflight ----------------------------------------------------------------
have docker || { say "Docker is required. Install Docker Desktop/Engine first: https://docs.docker.com/engine/install/"; exit 1; }

load_image_from_url() {
  url="$1"
  tmp="${TMPDIR:-/tmp}/vedha-probe-image.tar"
  say "Downloading probe image from $url ..."
  if have curl; then
    curl -fL "$url" -o "$tmp"
  elif have wget; then
    wget -O "$tmp" "$url"
  else
    say "curl or wget is required to download PROBE_IMAGE_TAR_URL."
    exit 1
  fi
  say "Loading Docker image ..."
  docker load -i "$tmp" >/dev/null
  rm -f "$tmp"
}

# Image source precedence:
#   1. already-loaded local image,
#   2. PROBE_IMAGE_TAR_URL hosted by the manager/operator machine,
#   3. registry pull via docker pull.
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  if [ -n "${PROBE_IMAGE_TAR_URL:-}" ]; then
    load_image_from_url "$PROBE_IMAGE_TAR_URL"
  else
    say "Pulling $IMAGE ..."
    docker pull "$IMAGE" || {
      say "Could not pull $IMAGE. Set PROBE_IMAGE_TAR_URL for a local tar download, or check registry login."
      exit 1
    }
  fi
fi

docker image inspect "$IMAGE" >/dev/null 2>&1 || {
  say "Image '$IMAGE' is still not available after load/pull."
  say "If you loaded a tar, set PROBE_IMAGE to the tag inside the tar, for example vedha-probe:local."
  exit 1
}

# Keep the host-bound license identity stable when the bootstrap container is
# recreated without its PAT. A locally administered MAC derived from the
# container name is deterministic and does not collide with vendor OUIs.
if [ -z "${PROBE_MAC_ADDRESS:-}" ]; then
  PROBE_MAC_ADDRESS="$(docker run --rm --network none --read-only \
    --cap-drop ALL --security-opt no-new-privileges:true --user 10001:10001 \
    --entrypoint python "$IMAGE" -c \
    'import hashlib,sys; d=hashlib.sha256(sys.argv[1].encode()).digest(); print("02:42:%02x:%02x:%02x:%02x" % tuple(d[:4]))' \
    "$NAME")"
fi

# Images before the non-root hardening ran as root and may have left the named
# state volume unreadable to UID 10001. Test access first and migrate only when
# needed, preserving every identity, license, and spooled-result file.
state_volume_writable() {
  docker run --rm \
    --network none \
    --read-only \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --user 10001:10001 \
    -v "$STATE_VOL:/state" \
    --entrypoint python \
    "$IMAGE" -c \
    'import os; p="/state/.vedha-write-test"; fd=os.open(p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600); os.close(fd); os.remove(p)' \
    >/dev/null 2>&1
}

prepare_state_volume() {
  docker volume create "$STATE_VOL" >/dev/null
  state_volume_writable && return 0
  say "Migrating probe state volume ownership to runtime UID 10001 ..."
  docker run --rm \
    --network none \
    --read-only \
    --cap-drop ALL \
    --cap-add CHOWN \
    --cap-add DAC_OVERRIDE \
    --cap-add DAC_READ_SEARCH \
    --security-opt no-new-privileges:true \
    --user 0:0 \
    -v "$STATE_VOL:/state" \
    --entrypoint chown \
    "$IMAGE" -R 10001:10001 /state >/dev/null && state_volume_writable
}

prepare_state_volume || {
  say "Could not prepare the private probe state volume '$STATE_VOL'."
  exit 1
}

# --- hostid shortcut ----------------------------------------------------------
if [ "${1:-}" = "hostid" ]; then
  exec docker run --rm \
    --read-only --cap-drop ALL --security-opt no-new-privileges:true \
    --pids-limit 64 --user 10001:10001 \
    --hostname "$NAME" --mac-address "$PROBE_MAC_ADDRESS" \
    -v "$STATE_VOL:/var/lib/vedha-probe" \
    --entrypoint python "$IMAGE" -c \
    'from agent.license import host_fingerprint; print(host_fingerprint())'
fi

# --- gather config (env if provided, else prompt when interactive) ------------
ask() {  # ask VAR "Prompt" [default]
  eval "cur=\${$1:-}"; [ -n "${cur:-}" ] && return 0
  if [ -t 0 ]; then
    printf '%s%s: ' "$2" "$( [ -n "${3:-}" ] && printf ' [%s]' "$3" )"
    read ans || ans=""
    eval "$1=\${ans:-${3:-}}"
  else
    eval "$1=\${3:-}"
  fi
}

OPERATOR_TOKEN="${OPERATOR_TOKEN:-${PROBE_PAT:-${VEDHA_PAT:-}}}"

ask PLATFORM_URL    "Manager URL (https://...)"
ask OPERATOR_TOKEN  "Personal Access Token (vpat_...)"
ask PROBE_NAME      "Probe name" "$(hostname)"
ask PROBE_LOCATION  "Probe location" ""
ask PROBE_NETWORK_SEGMENTS "Reachable network segment(s), comma-separated" ""
ask PROBE_LICENSE   "Deployment license (blank if licensing is disabled)" ""
ask PROBE_LICENSE_PUBKEY "Vendor Ed25519 public key (hex)" ""

[ -n "${PLATFORM_URL:-}" ] || { say "PLATFORM_URL is required."; exit 1; }
[ -n "${PROBE_NETWORK_SEGMENTS:-}" ] || {
  say "PROBE_NETWORK_SEGMENTS is required and must contain authorized reachable CIDRs."
  say "An empty value is fail-closed; the probe will not start or scan."
  exit 1
}
[ -n "${OPERATOR_TOKEN:-}" ] || {
  say "OPERATOR_TOKEN/PROBE_PAT is required. Mint a scoped PAT with: make probe-pat"
  exit 1
}

case "$VERIFY_TLS" in true|false) : ;; *) say "VERIFY_TLS must be true or false."; exit 1 ;; esac
case "$LICENSE_ENFORCED" in true|false) : ;; *) say "LICENSE_ENFORCED must be true or false."; exit 1 ;; esac

# Validate and canonicalize all execution-boundary fields with the same Python
# standard library used by the probe. The helper has no network and no writable
# filesystem, so invalid configuration fails before any scan-capable process runs.
validated_config="$(docker run --rm \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
  --entrypoint python "$IMAGE" -c '
import ipaddress, re, sys
from urllib.parse import urlparse

segments, max_targets, max_seconds, registration_timeout, name, url, licensing, pubkey = sys.argv[1:]
parts = segments.split(",")
if not segments.strip() or any(not part.strip() for part in parts):
    raise SystemExit("invalid empty CIDR entry")
networks = []
for part in parts:
    network = str(ipaddress.ip_network(part.strip(), strict=False))
    if network not in networks:
        networks.append(network)
targets = int(max_targets)
seconds = int(max_seconds)
timeout = int(registration_timeout)
if not 1 <= targets <= 200000:
    raise SystemExit("PROBE_MAX_TARGETS must be 1..200000")
if not 1 <= seconds <= 86400:
    raise SystemExit("PROBE_MAX_JOB_SECONDS must be 1..86400")
if not 1 <= timeout <= 600:
    raise SystemExit("PROBE_REGISTRATION_TIMEOUT must be 1..600")
if not 1 <= len(name) <= 255 or "\n" in name or "\r" in name:
    raise SystemExit("PROBE_NAME must be a single line of 1..255 characters")
parsed = urlparse(url)
if parsed.scheme not in {"http", "https"} or not parsed.hostname:
    raise SystemExit("PLATFORM_URL must be an http(s) URL with a host")
local_hosts = {"localhost", "127.0.0.1", "::1", "host.docker.internal", "api"}
if parsed.scheme != "https" and parsed.hostname not in local_hosts and licensing == "true":
    raise SystemExit("production manager URLs must use https")
if licensing == "true" and not re.fullmatch(r"[0-9a-fA-F]{64}", pubkey):
    raise SystemExit("PROBE_LICENSE_PUBKEY must be a 64-character hex Ed25519 public key")
print(",".join(networks))
print(targets)
print(seconds)
print(timeout)
' "$PROBE_NETWORK_SEGMENTS" "$PROBE_MAX_TARGETS" "$PROBE_MAX_JOB_SECONDS" \
  "$PROBE_REGISTRATION_TIMEOUT" "$PROBE_NAME" "$PLATFORM_URL" \
  "$LICENSE_ENFORCED" "${PROBE_LICENSE_PUBKEY:-}" \
  2>&1)" || {
    say "Invalid probe configuration: $validated_config"
    exit 1
  }
PROBE_NETWORK_SEGMENTS="$(printf '%s\n' "$validated_config" | sed -n '1p')"
PROBE_MAX_TARGETS="$(printf '%s\n' "$validated_config" | sed -n '2p')"
PROBE_MAX_JOB_SECONDS="$(printf '%s\n' "$validated_config" | sed -n '3p')"
PROBE_REGISTRATION_TIMEOUT="$(printf '%s\n' "$validated_config" | sed -n '4p')"

store_license() {
  [ "$LICENSE_ENFORCED" = "true" ] || return 0
  if [ -n "${PROBE_LICENSE:-}" ]; then
    if ! printf '%s' "$PROBE_LICENSE" | docker run --rm -i \
      --network none --read-only --cap-drop ALL \
      --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
      -v "$STATE_VOL:/state" --entrypoint python "$IMAGE" -c \
      'import os,sys; os.umask(0o077); open("/state/license.token","w",encoding="utf-8").write(sys.stdin.read())'
    then
      say "Could not store the license in the private probe state volume."
      exit 1
    fi
    return 0
  fi
  docker run --rm --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
    -v "$STATE_VOL:/state:ro" --entrypoint python "$IMAGE" -c \
    'from pathlib import Path; raise SystemExit(0 if Path("/state/license.token").is_file() else 1)' \
    >/dev/null 2>&1 || {
      say "PROBE_LICENSE is required because no stored license exists."
      exit 1
    }
}

store_license

# --- preflight: reach the manager + validate the token BEFORE launching -------
# Catches a wrong URL or a bad/expired token now, instead of after the container
# is up and you're tailing docker logs. Bypass with SKIP_PREFLIGHT=true.
if [ "${SKIP_PREFLIGHT:-false}" != "true" ] && have curl; then
  ctls=""; [ "$VERIFY_TLS" = "false" ] && ctls="-k"
  say "Checking manager at $PLATFORM_URL ..."
  if ! curl -fsS --connect-timeout 5 --max-time 15 $ctls \
    "$PLATFORM_URL/health" >/dev/null 2>&1; then
    say "ERROR: manager not reachable at $PLATFORM_URL/health."
    say "  - Is PLATFORM_URL correct and the manager up (https needs a TLS front)?"
    say "  - Bypass with SKIP_PREFLIGHT=true if you know the probe will retry."
    exit 1
  fi
  case "${OPERATOR_TOKEN:-}" in
    vpat_*|"") : ;;   # a PAT, or the email/password fallback path
    *) say "NOTE: token doesn't look like a Vedha PAT (expected 'vpat_...'). Mint one with: make probe-pat" ;;
  esac
  if [ -n "${OPERATOR_TOKEN:-}" ]; then
    if curl -fsS --connect-timeout 5 --max-time 15 $ctls \
      -H "Authorization: Bearer $OPERATOR_TOKEN" \
      "$PLATFORM_URL/auth/me" >/dev/null 2>&1; then
      say "Token accepted by the manager."
    else
      say "ERROR: the manager rejected the token (invalid, expired, revoked, or out of scope)."
      say "  - Mint a fresh probe PAT:  make probe-pat"
      say "    (or POST $PLATFORM_URL/auth/personal-access-tokens — the Swagger form is at /docs)"
      say "  - Bypass with SKIP_PREFLIGHT=true."
      exit 1
    fi
  fi
fi

# --- run ----------------------------------------------------------------------
# Use a protected env file so secrets do not appear in the docker CLI process
# arguments. It exists only long enough to create the bootstrap container.
for config_value in \
  "$PLATFORM_URL" "$VERIFY_TLS" "$PROBE_NAME" "${PROBE_LOCATION:-}" \
  "$PROBE_NETWORK_SEGMENTS" "$PROBE_MAX_TARGETS" "$PROBE_MAX_JOB_SECONDS" \
  "$PROBE_REGISTRATION_TIMEOUT" \
  "$OPERATOR_TOKEN" "${PROBE_LICENSE_PUBKEY:-}"
do
  if printf '%s' "$config_value" | LC_ALL=C grep -q '[[:cntrl:]]'; then
    say "Probe configuration values must be single-line text."
    exit 1
  fi
done

ENV_FILE="$(mktemp "${TMPDIR:-/tmp}/vedha-probe-env.XXXXXX")"
chmod 600 "$ENV_FILE"
cleanup_env_file() { rm -f "$ENV_FILE"; }
trap cleanup_env_file EXIT HUP INT TERM

write_env_file() {
  include_bootstrap="$1"
  {
    printf 'PLATFORM_URL=%s\n' "$PLATFORM_URL"
    printf 'VERIFY_TLS=%s\n' "$VERIFY_TLS"
    printf 'PROBE_NAME=%s\n' "$PROBE_NAME"
    printf 'PROBE_LOCATION=%s\n' "${PROBE_LOCATION:-}"
    printf 'PROBE_NETWORK_SEGMENTS=%s\n' "$PROBE_NETWORK_SEGMENTS"
    printf 'PROBE_MAX_TARGETS=%s\n' "$PROBE_MAX_TARGETS"
    printf 'PROBE_MAX_JOB_SECONDS=%s\n' "$PROBE_MAX_JOB_SECONDS"
    printf 'LICENSE_ENFORCED=%s\n' "$LICENSE_ENFORCED"
    if [ "$LICENSE_ENFORCED" = "true" ]; then
      printf 'PROBE_LICENSE_FILE=/var/lib/vedha-probe/license.token\n'
      printf 'PROBE_LICENSE_PUBKEY=%s\n' "$PROBE_LICENSE_PUBKEY"
    fi
    if [ "$include_bootstrap" = "true" ]; then
      printf 'OPERATOR_TOKEN=%s\n' "$OPERATOR_TOKEN"
    fi
  } > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
}

run_probe_container() {
  include_bootstrap="$1"
  write_env_file "$include_bootstrap"
  docker run -d --name "$NAME" --hostname "$NAME" \
    --mac-address "$PROBE_MAC_ADDRESS" --restart unless-stopped \
    --read-only \
    --tmpfs /tmp:size=64m,mode=1777 \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --pids-limit 256 \
    --init \
    --env-file "$ENV_FILE" \
    -v "$STATE_VOL:/var/lib/vedha-probe" \
    "$IMAGE" >/dev/null
}

manager_probe_online() {
  # The PAT is reintroduced only into a short-lived read-only verifier, never
  # the steady-state probe. Match the persisted agent ID to avoid name races.
  write_env_file true
  if docker run --rm \
    --read-only --cap-drop ALL --security-opt no-new-privileges:true \
    --pids-limit 64 --user 10001:10001 \
    --env-file "$ENV_FILE" \
    -v "$STATE_VOL:/state:ro" \
    --entrypoint python "$IMAGE" -c '
import json, os
import httpx

state = json.load(open("/state/state.json", encoding="utf-8"))
agent_id = str(state.get("agent_id") or "")
verify = os.environ.get("VERIFY_TLS", "true").lower() not in {"false", "0", "no"}
headers = {"Authorization": "Bearer " + os.environ["OPERATOR_TOKEN"]}
with httpx.Client(base_url=os.environ["PLATFORM_URL"], headers=headers,
                  verify=verify, timeout=10.0) as client:
    response = client.get("/agents")
    response.raise_for_status()
    agents = response.json()
match = next((row for row in agents if str(row.get("id")) == agent_id), None)
raise SystemExit(0 if match and match.get("online") else 1)
' >/dev/null 2>&1
  then
    manager_status=0
  else
    manager_status=$?
  fi
  write_env_file false
  return "$manager_status"
}

wait_for_probe() {
  i=0
  while [ "$i" -lt "$PROBE_REGISTRATION_TIMEOUT" ]; do
    logs="$(docker logs "$NAME" 2>&1 || true)"
    case "$logs" in
      *"Registered as"*|*"Resumed as"*|*"Waiting for scan jobs"*|*"Attempting WebSocket push mode"*)
        manager_probe_online && return 0 ;;
    esac
    running="$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)"
    [ "$running" = "true" ] || return 1
    i=$((i + 1))
    sleep 1
  done
  return 1
}

say "Starting probe '$PROBE_NAME' -> $PLATFORM_URL ..."
docker rm -f "$NAME" >/dev/null 2>&1 || true
run_probe_container true

say ""
say "Probe container started — waiting for it to register with the manager ..."
if ! wait_for_probe; then
  say "ERROR: probe bootstrap did not register successfully."
  docker logs --tail 50 "$NAME" 2>&1 || true
  docker rm -f "$NAME" >/dev/null 2>&1 || true
  exit 1
fi

# Registration state now contains the agent-scoped identity. Recreate the
# container immediately so PAT/password/license values cannot remain in Docker
# metadata during normal operation.
say "Registration succeeded; sealing bootstrap credentials ..."
docker rm -f "$NAME" >/dev/null
run_probe_container false
if ! wait_for_probe; then
  say "ERROR: probe could not resume from its persisted agent identity."
  docker logs --tail 50 "$NAME" 2>&1 || true
  exit 1
fi
rm -f "$ENV_FILE"

say ""
say "OK: probe '$PROBE_NAME' is online without bootstrap credentials in its container metadata."
say "    The dashboard Scanner page should now show it ONLINE."
say ""
say "Logs:    docker logs -f $NAME"
say "Host ID: sh install.sh hostid"
say "Stop:    docker rm -f $NAME"
