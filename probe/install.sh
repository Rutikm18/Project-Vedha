#!/usr/bin/env sh
# Vedha probe installer — one command, no human credential on the client.
#
#   Supported enrollment flow:
#     curl --proto '=https' --tlsv1.2 -fsS https://downloads.example/probe/install.sh \
#       | sudo sh -s -- --manager https://manager.example.com
#
#   Inspect-first:
#     curl -fsSL https://YOUR_HOST/install.sh -o install.sh
#     less install.sh
#     sudo sh install.sh --manager https://manager.example.com
set -eu

IMAGE="${PROBE_IMAGE:-vedha-probe:local}"       # local tag or registry path
NAME="${PROBE_CONTAINER:-vedha-probe}"
STATE_VOL="${PROBE_STATE_VOLUME:-vedha-probe-state}"
VERIFY_TLS="${VERIFY_TLS:-true}"
LICENSE_ENFORCED="${LICENSE_ENFORCED:-false}"
PROBE_MAX_TARGETS="${PROBE_MAX_TARGETS:-4096}"
PROBE_MAX_JOB_SECONDS="${PROBE_MAX_JOB_SECONDS:-7200}"
PROBE_REGISTRATION_TIMEOUT="${PROBE_REGISTRATION_TIMEOUT:-60}"
PROBE_ENROLL_TOKEN="${PROBE_ENROLL_TOKEN:-}"
PROBE_ALLOW_INSECURE="${PROBE_ALLOW_INSECURE:-false}"

say() { printf '%s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

usage() {
  say "Usage: $0 --manager https://manager.example.com [--enroll-token vet_...] [--insecure]"
  say "  --enroll-token  Pre-authorized, Site-bound token → probe auto-enrolls (no user_code step)."
  say "  --insecure      Allow an http:// manager (testing only; production requires https)."
  say "Only the Manager endpoint is deployment-specific; Site policy comes from the token or Fleet UI."
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --manager)
      [ "$#" -ge 2 ] || { say "ERROR: --manager requires a value."; usage; exit 2; }
      PLATFORM_URL=$2
      shift 2
      ;;
    --enroll-token)
      [ "$#" -ge 2 ] || { say "ERROR: --enroll-token requires a value."; usage; exit 2; }
      PROBE_ENROLL_TOKEN=$2
      shift 2
      ;;
    --insecure)
      PROBE_ALLOW_INSECURE=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      say "ERROR: unknown argument: $1"
      usage
      exit 2
      ;;
  esac
done

PLATFORM_URL="${PLATFORM_URL:-}"
PROBE_NAME="${PROBE_NAME:-$(hostname)}"
PROBE_LOCATION="${PROBE_LOCATION:-}"
PROBE_NETWORK_SEGMENTS="${PROBE_NETWORK_SEGMENTS:-}"

[ -n "$PLATFORM_URL" ] || { say "ERROR: --manager is required."; usage; exit 2; }
PLATFORM_URL="${PLATFORM_URL%/}"

if [ "${PROBE_INSTALL_DRY_RUN:-false}" = "true" ]; then
  say "Dry-run preview (no Docker or connectivity checks were run)."
  say "Image: $IMAGE"
  say "Container: $NAME"
  say "Manager: $PLATFORM_URL"
  if [ -n "$PROBE_ENROLL_TOKEN" ]; then
    say "Identity: device-generated key; auto-enroll via pre-authorized token (${PROBE_ENROLL_TOKEN%%_*}_…)"
  else
    say "Identity: device-generated key; Fleet UI approval required"
  fi
  say "Scope and safety budgets: Manager-owned Site policy"
  [ "$PROBE_ALLOW_INSECURE" = "true" ] && say "TLS: insecure http manager permitted (testing mode)"
  exit 0
fi

# --- preflight ----------------------------------------------------------------
have docker || { say "Docker is required. Install Docker Desktop/Engine first: https://docs.docker.com/engine/install/"; exit 1; }

LOCK_DIR="${TMPDIR:-/tmp}/vedha-probe-install.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  say "ERROR: another Vedha probe install is running (lock: $LOCK_DIR)."
  exit 75
fi
STAGE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/vedha-probe-install.XXXXXX")"
cleanup_install() {
  rm -rf "$STAGE_DIR"
  rmdir "$LOCK_DIR" 2>/dev/null || true
}
trap cleanup_install EXIT HUP INT TERM

load_image_from_url() {
  url="$1"
  tmp="$STAGE_DIR/probe-image.tar"
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
if [ -z "${PROBE_HW_ID:-}" ]; then
  PROBE_HW_ID="$(docker run --rm --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
    --hostname "$NAME" --mac-address "$PROBE_MAC_ADDRESS" \
    --entrypoint python "$IMAGE" -c \
    'from agent.hw_bind import get_hw_id; print(get_hw_id())')"
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

segments, max_targets, max_seconds, registration_timeout, mac, hwid, name, url, licensing, pubkey, allow_insecure = sys.argv[1:]
networks = []
if segments.strip():
    parts = segments.split(",")
    if any(not part.strip() for part in parts):
        raise SystemExit("invalid empty CIDR entry")
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
if not re.fullmatch(r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", mac):
    raise SystemExit("PROBE_MAC_ADDRESS must be a colon-separated MAC address")
if int(mac[:2], 16) & 1:
    raise SystemExit("PROBE_MAC_ADDRESS must be unicast")
if not re.fullmatch(r"[0-9a-f]{32}", hwid):
    raise SystemExit("PROBE_HW_ID must be a 32-character lowercase hex fingerprint")
if not 1 <= len(name) <= 255 or "\n" in name or "\r" in name:
    raise SystemExit("PROBE_NAME must be a single line of 1..255 characters")
parsed = urlparse(url)
if parsed.scheme not in {"http", "https"} or not parsed.hostname:
    raise SystemExit("PLATFORM_URL must be an http(s) URL with a host")
local_hosts = {"localhost", "127.0.0.1", "::1", "host.docker.internal", "api"}
if parsed.scheme != "https" and parsed.hostname not in local_hosts and allow_insecure != "true":
    raise SystemExit("production manager URLs must use https (pass --insecure for a testing http manager)")
if licensing == "true" and not re.fullmatch(r"[0-9a-fA-F]{64}", pubkey):
    raise SystemExit("PROBE_LICENSE_PUBKEY must be a 64-character hex Ed25519 public key")
print(",".join(networks))
print(targets)
print(seconds)
print(timeout)
' "$PROBE_NETWORK_SEGMENTS" "$PROBE_MAX_TARGETS" "$PROBE_MAX_JOB_SECONDS" \
  "$PROBE_REGISTRATION_TIMEOUT" "$PROBE_MAC_ADDRESS" "$PROBE_HW_ID" \
  "$PROBE_NAME" "$PLATFORM_URL" "$LICENSE_ENFORCED" "${PROBE_LICENSE_PUBKEY:-}" \
  "$PROBE_ALLOW_INSECURE" \
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

# --- preflight: reach the Manager before creating local runtime state ---------
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
fi

# --- run ----------------------------------------------------------------------
# The env file contains configuration only. Enrollment and refresh secrets are
# created inside the probe and persist solely in its private state volume.
for config_value in \
  "$PLATFORM_URL" "$VERIFY_TLS" "$PROBE_NAME" "${PROBE_LOCATION:-}" \
  "$PROBE_NETWORK_SEGMENTS" "$PROBE_MAX_TARGETS" "$PROBE_MAX_JOB_SECONDS" \
  "$PROBE_REGISTRATION_TIMEOUT" "$PROBE_HW_ID" "${PROBE_LICENSE_PUBKEY:-}" \
  "${PROBE_ENROLL_TOKEN:-}"
do
  if printf '%s' "$config_value" | LC_ALL=C grep -q '[[:cntrl:]]'; then
    say "Probe configuration values must be single-line text."
    exit 1
  fi
done

ENV_FILE="$(mktemp "${TMPDIR:-/tmp}/vedha-probe-env.XXXXXX")"
chmod 600 "$ENV_FILE"
cleanup_all() {
  rm -f "$ENV_FILE"
  cleanup_install
}
trap cleanup_all EXIT HUP INT TERM

write_env_file() {
  {
    printf 'PLATFORM_URL=%s\n' "$PLATFORM_URL"
    printf 'VERIFY_TLS=%s\n' "$VERIFY_TLS"
    printf 'PROBE_NAME=%s\n' "$PROBE_NAME"
    printf 'PROBE_LOCATION=%s\n' "${PROBE_LOCATION:-}"
    printf 'PROBE_NETWORK_SEGMENTS=%s\n' "$PROBE_NETWORK_SEGMENTS"
    printf 'PROBE_MAX_TARGETS=%s\n' "$PROBE_MAX_TARGETS"
    printf 'PROBE_MAX_JOB_SECONDS=%s\n' "$PROBE_MAX_JOB_SECONDS"
    printf 'HW_BIND_FINGERPRINT=%s\n' "$PROBE_HW_ID"
    if [ -n "$PROBE_ENROLL_TOKEN" ]; then
      # Pre-authorized, Site-bound enrollment token. Consumed once on first boot
      # to auto-approve; the durable identity is the device key + refresh secret.
      printf 'PROBE_ENROLL_TOKEN=%s\n' "$PROBE_ENROLL_TOKEN"
    fi
    printf 'LICENSE_ENFORCED=%s\n' "$LICENSE_ENFORCED"
    if [ "$LICENSE_ENFORCED" = "true" ]; then
      printf 'PROBE_LICENSE_FILE=/var/lib/vedha-probe/license.token\n'
      printf 'PROBE_LICENSE_PUBKEY=%s\n' "$PROBE_LICENSE_PUBKEY"
    fi
  } > "$ENV_FILE"
  chmod 600 "$ENV_FILE"
}

run_probe_container() {
  write_env_file
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

say "Starting probe '$PROBE_NAME' -> $PLATFORM_URL ..."
if docker container inspect "$NAME" >/dev/null 2>&1; then
  existing_manager="$(docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$NAME" \
    | sed -n 's/^PLATFORM_URL=//p' | sed -n '1p')"
  if [ "$existing_manager" != "$PLATFORM_URL" ]; then
    say "ERROR: existing container '$NAME' belongs to Manager '$existing_manager'."
    say "Refusing to move an enrolled identity implicitly; revoke/re-enroll explicitly."
    exit 78
  fi
  docker start "$NAME" >/dev/null
  say "Existing probe installation preserved and started."
else
  run_probe_container
  say "Probe container started. It is creating a device identity and enrollment request."
fi

sleep 2
if [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)" != "true" ]; then
  say "ERROR: probe exited during startup."
  docker logs --tail 50 "$NAME" 2>&1 || true
  exit 1
fi

say ""
say "OK: probe '$PROBE_NAME' is installed with no PAT or human credential."
say "Approve the displayed code in Manager Fleet → Add Probe."
docker logs --tail 20 "$NAME" 2>&1 || true
say ""
say "Logs:    docker logs -f $NAME"
say "Stop:    docker rm -f $NAME"
