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

# ─────────────────────────────────────────────────────────────────────────────
# ONE installer, two modes:
#
#   LOCAL  (default for a bare argument) — run the probe on THIS machine with
#          Python. For dev / testing. Uses the PAT saved in probe.env.
#              ./install.sh <manager-ip-or-url> [--enroll]
#
#   DOCKER (production) — hardened container, zero-touch device enrollment.
#              sudo sh install.sh --docker --manager https://manager.example.com [--enroll-token vet_…]
#
# A bare ip/url ⇒ LOCAL; the --manager flag (or --docker) ⇒ DOCKER.
# ─────────────────────────────────────────────────────────────────────────────
say() { printf '%s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

_MODE=""
for _a in "$@"; do
  case "$_a" in --docker) _MODE=docker ;; --local) _MODE=local ;; esac
done
if [ -z "$_MODE" ]; then
  case "${1:-}" in ""|--*) _MODE=docker ;; *) _MODE=local ;; esac
fi

if [ "$_MODE" = "local" ]; then
  # ==== LOCAL MODE (Python-direct; folds the former run-probe.sh) ====
  cd "$(dirname "$0")"
  _MANAGER=""; _ENROLL=false; _TOKEN=""
  for _a in "$@"; do
    case "$_a" in
      --enroll) _ENROLL=true ;;
      --*) : ;;
      *)
        if [ -z "$_MANAGER" ]; then _MANAGER="$_a"
        elif [ -z "$_TOKEN" ]; then _TOKEN="$_a"
        fi
        ;;
    esac
  done
  if [ -z "$_MANAGER" ]; then
    printf 'usage: %s <manager-ip-or-url> [--enroll | <enroll-token>]   (LOCAL)\n' "$0"
    printf '   or: %s --docker --manager <url> [...]    (DOCKER)\n' "$0"
    exit 2
  fi
  # Saved config (PLATFORM_URL default, name, tuning, and any saved credential).
  # In --enroll we deliberately SKIP probe.env so nothing saved is loaded → the
  # probe does a fresh device enrollment (its keypair is its id; the Manager
  # issues the token). The CLI arg overrides the manager URL either way.
  if [ "$_ENROLL" != "true" ] && [ -f probe.env ]; then
    set -a; . ./probe.env; set +a
  fi
  case "$_MANAGER" in
    http://*|https://*) PLATFORM_URL="$_MANAGER" ;;
    *)                  PLATFORM_URL="http://${_MANAGER}:18080" ;;
  esac
  export PLATFORM_URL
  if [ "$_ENROLL" = "true" ]; then
    printf '• zero-touch enrollment: the probe will connect via device enrollment\n'
  elif [ -n "$_TOKEN" ]; then
    # Pre-authorized, site-bound enrollment token (auto-approve).
    export PROBE_ENROLL_TOKEN="$_TOKEN"
  fi
  # Local scan CEILING (safety net; the Manager still governs per-job scope).
  if [ -z "${PROBE_NETWORK_SEGMENTS:-}" ]; then
    # Primary source IPv4 via the DEFAULT ROUTE (works on any interface, not just
    # en0): Linux `ip route get`, then BSD/macOS `route`→interface→ipconfig, then
    # the old en0/hostname fallbacks. IPv6 is skipped since the /24 ceiling is IPv4.
    _IP="$(ip -4 route get 1.1.1.1 2>/dev/null | sed -n 's/.*src \([0-9.]\{1,\}\).*/\1/p' | head -1 || true)"
    if [ -z "${_IP:-}" ]; then
      _if="$(route -n get default 2>/dev/null | awk '/interface:/{print $2; exit}')"
      [ -n "${_if:-}" ] && _IP="$(ipconfig getifaddr "$_if" 2>/dev/null || true)"
    fi
    [ -n "${_IP:-}" ] || _IP="$(ipconfig getifaddr en0 2>/dev/null || { hostname -I 2>/dev/null | awk '{print $1}'; } || true)"
    case "${_IP:-}" in
      *:*|"") : ;;                       # IPv6 or empty → no auto scan-ceiling
      *.*.*.*)
        PROBE_NETWORK_SEGMENTS="${_IP%.*}.0/24"; export PROBE_NETWORK_SEGMENTS
        printf '• auto scan-ceiling: %s (override with PROBE_NETWORK_SEGMENTS)\n' "$PROBE_NETWORK_SEGMENTS" ;;
    esac
  fi
  export PROBE_NAME="${PROBE_NAME:-$(hostname)-probe}"
  export STATE_FILE="${STATE_FILE:-$HOME/vedha-agent/state.json}"
  export RESULT_SPOOL_DIR="${RESULT_SPOOL_DIR:-$HOME/vedha-agent/spool}"
  mkdir -p "$(dirname "$STATE_FILE")" "$RESULT_SPOOL_DIR"
  # Preflight: LOCAL mode runs the probe directly with Python 3.8+.
  have python3 || {
    printf 'ERROR: python3 not found. LOCAL mode needs Python 3.8+ (plus the\n'
    printf '       python3-venv package on Debian/Ubuntu). Or use DOCKER mode:\n'
    printf '         sudo sh install.sh --docker --manager <url>\n'
    exit 1
  }
  python3 -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 8) else 1)' || {
    printf 'ERROR: Python 3.8+ required (found %s). Install a newer python3.\n' \
      "$(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])' 2>/dev/null || echo unknown)"
    exit 1
  }
  # Runnable interpreter: (re)create the venv and (re)install deps when the venv is
  # absent/partial OR requirements-runtime.txt changed. The stamp avoids reinstalling
  # on every launch while still healing a half-built venv or a newly-added dependency.
  _PY=".venv/bin/python"
  _STAMP=".venv/.reqs-stamp"
  _REQS="$(cksum requirements-runtime.txt 2>/dev/null || echo none)"
  if [ ! -x "$_PY" ] || [ "$(cat "$_STAMP" 2>/dev/null || true)" != "$_REQS" ]; then
    printf '• setting up .venv + runtime deps…\n'
    [ -x "$_PY" ] || python3 -m venv .venv || {
      printf 'ERROR: virtualenv creation failed. On Debian/Ubuntu install the venv\n'
      printf '       module first: sudo apt-get install -y python3-venv\n'
      exit 1
    }
    ./.venv/bin/pip install -q --upgrade pip
    ./.venv/bin/pip install -q -r requirements-runtime.txt || {
      printf 'ERROR: failed to install runtime deps from requirements-runtime.txt.\n'
      exit 1
    }
    printf '%s' "$_REQS" > "$_STAMP"
  fi
  printf '▶ probe → %s   name=%s  scope-ceiling=%s\n' \
    "$PLATFORM_URL" "$PROBE_NAME" "${PROBE_NETWORK_SEGMENTS:-<unset>}"

  # ── Self-heal supervisor (LOCAL mode) ───────────────────────────────────────
  # The probe uses exit codes to ask its supervisor to restart it:
  #   4 = it wiped an ORPHANED identity (its device key is still registered on a
  #       manager whose credential was reset — e.g. a redeploy — so it can neither
  #       refresh nor re-enroll) and needs a restart to enroll with a FRESH key.
  #   2 = the manager was unreachable/unavailable past the probe's own retry budget
  #       (a redeploy window can outlast it); a backed-off restart usually recovers.
  # A container's restart policy does exactly this. LOCAL mode has no supervisor,
  # so a routine manager redeploy looked like a permanently broken probe until the
  # operator happened to re-run install.sh. Do the bounded restart here instead.
  _SELFHEAL_MAX="${PROBE_SELFHEAL_MAX:-6}"
  _heal=0
  while :; do
    set +e
    "$_PY" -m agent.agent
    _rc=$?
    set -e
    case "$_rc" in
      4)
        _heal=$((_heal + 1))
        if [ "$_heal" -ge "$_SELFHEAL_MAX" ]; then
          printf '✗ Re-enrollment did not converge after %d fresh-key attempts. The\n' "$_heal" >&2
          printf '  manager keeps rejecting enrollment — remove the stale probe in Fleet\n' >&2
          printf '  and check the manager, then re-run.\n' >&2
          exit 4
        fi
        printf '↻ Orphaned credential cleared — re-enrolling with a fresh identity (%d/%d)…\n' \
          "$_heal" "$_SELFHEAL_MAX"
        ;;
      2)
        _heal=$((_heal + 1))
        if [ "$_heal" -ge "$_SELFHEAL_MAX" ]; then
          printf '✗ Manager stayed unreachable across %d attempts — giving up. Check the\n' "$_heal" >&2
          printf '  manager is up and PLATFORM_URL/network are correct, then re-run.\n' >&2
          exit 2
        fi
        _sleep=$(( _heal * 5 )); [ "$_sleep" -gt 30 ] && _sleep=30
        printf '↻ Manager unavailable — retrying in %ss (%d/%d)…\n' "$_sleep" "$_heal" "$_SELFHEAL_MAX"
        sleep "$_sleep"
        ;;
      *)
        # 0 (clean), 1 (needs a human: bad config/revoked), 3 (awaiting approval),
        # 130 (Ctrl-C), etc. — surface as-is; the probe already explained why.
        exit "$_rc"
        ;;
    esac
  done
fi

# ==== DOCKER MODE (production; hardened container) — original installer below ====
IMAGE="${PROBE_IMAGE:-vedha-agent:local}"       # local tag or registry path
NAME="${PROBE_CONTAINER:-vedha-agent}"
STATE_VOL="${PROBE_STATE_VOLUME:-vedha-agent-state}"
VERIFY_TLS="${VERIFY_TLS:-true}"
LICENSE_ENFORCED="${LICENSE_ENFORCED:-false}"
PROBE_MAX_TARGETS="${PROBE_MAX_TARGETS:-4096}"
PROBE_MAX_JOB_SECONDS="${PROBE_MAX_JOB_SECONDS:-7200}"
PROBE_REGISTRATION_TIMEOUT="${PROBE_REGISTRATION_TIMEOUT:-60}"
PROBE_ENROLL_TOKEN="${PROBE_ENROLL_TOKEN:-}"
PROBE_ALLOW_INSECURE="${PROBE_ALLOW_INSECURE:-false}"

usage() {
  say "Usage: $0 --manager https://manager.example.com [--enroll-token vet_...] [--insecure]"
  say "  --enroll-token  Pre-authorized, Site-bound token → probe auto-enrolls (no user_code step)."
  say "  --insecure      Allow an http:// manager (testing only; production requires https)."
  say "  --uninstall     Remove the probe container (PROBE_PURGE=true also deletes its identity/license volume)."
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
    --docker|--local)
      shift
      ;;
    --uninstall)
      have docker || { say "Docker not found."; exit 1; }
      docker rm -f "$NAME" >/dev/null 2>&1 && say "Removed probe container '$NAME'." \
        || say "No probe container '$NAME' to remove."
      if [ "${PROBE_PURGE:-false}" = "true" ]; then
        docker volume rm "$STATE_VOL" >/dev/null 2>&1 \
          && say "Purged state volume '$STATE_VOL' — identity & license removed." || true
      fi
      exit 0
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
docker info >/dev/null 2>&1 || { say "Docker is installed but its daemon isn't reachable. Start Docker (open Docker Desktop, or 'sudo systemctl start docker') and retry."; exit 1; }

LOCK_DIR="${TMPDIR:-/tmp}/vedha-agent-install.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  # Reclaim a lock left by a crashed run (SIGKILL bypasses the cleanup trap).
  if find "$LOCK_DIR" -maxdepth 0 -mmin +10 2>/dev/null | grep -q .; then
    say "Reclaiming a stale install lock (>10 min old)."
    rmdir "$LOCK_DIR" 2>/dev/null || true
    mkdir "$LOCK_DIR" 2>/dev/null || { say "ERROR: could not acquire install lock."; exit 75; }
  else
    say "ERROR: another Vedha probe install is running (lock: $LOCK_DIR)."
    exit 75
  fi
fi
STAGE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/vedha-agent-install.XXXXXX")"
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
  # Supply-chain: verify the tar before loading it, when a hash is pinned.
  if [ -n "${PROBE_IMAGE_SHA256:-}" ]; then
    say "Verifying image tar checksum ..."
    got="$( { sha256sum "$tmp" 2>/dev/null || shasum -a 256 "$tmp" 2>/dev/null; } | awk '{print $1}')"
    if [ "$got" != "$PROBE_IMAGE_SHA256" ]; then
      say "ERROR: image tar checksum mismatch (expected $PROBE_IMAGE_SHA256, got ${got:-none}). Refusing to load."
      exit 1
    fi
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
      say "Could not pull $IMAGE."
      case "$IMAGE" in
        *:local) say "  '$IMAGE' is a LOCAL tag — it can't come from a registry. Build it"
                 say "  (make probe-build) or host a tar and set PROBE_IMAGE_TAR_URL." ;;
        *)       say "  Set PROBE_IMAGE_TAR_URL for a local tar, set PROBE_IMAGE to a"
                 say "  registry tag, or check your registry login." ;;
      esac
      exit 1
    }
  fi
fi

docker image inspect "$IMAGE" >/dev/null 2>&1 || {
  say "Image '$IMAGE' is still not available after load/pull."
  say "If you loaded a tar, set PROBE_IMAGE to the tag inside the tar, for example vedha-agent:local."
  exit 1
}

# Warn on CPU-arch mismatch (e.g. amd64 image on an arm64 host → slow qemu or fail).
_img_arch="$(docker image inspect --format '{{.Architecture}}' "$IMAGE" 2>/dev/null || true)"
_host_arch="$(uname -m 2>/dev/null || echo unknown)"
case "$_host_arch" in aarch64|arm64) _host_arch=arm64 ;; x86_64|amd64) _host_arch=amd64 ;; esac
if [ -n "$_img_arch" ] && [ "$_img_arch" != "$_host_arch" ]; then
  say "WARNING: image arch '$_img_arch' != host arch '$_host_arch' — it may run under"
  say "  emulation (slow) or fail to start. Prefer an image built for $_host_arch."
fi

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
    'from agent.hw_bind import get_hw_id; print(get_hw_id())' 2>/dev/null || true)"
  if [ -z "$PROBE_HW_ID" ]; then
    say "ERROR: could not derive the probe hardware id."
    say "  If your Docker is rootless or Docker Desktop, it may reject --mac-address,"
    say "  which the host-license binding requires. Use a rootful Docker Engine, or set"
    say "  PROBE_MAC_ADDRESS + PROBE_HW_ID explicitly for a MAC-independent enrollment."
    exit 1
  fi
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
# http to a non-local manager is allowed (unencrypted). The warning is emitted on
# the shell side because this block stdout+stderr are captured with 2>&1 as the
# parsed config, so nothing extra may be printed here.
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

# http to a non-local manager is permitted but unencrypted — warn, don't block.
case "$PLATFORM_URL" in
  https://*) ;;
  http://localhost*|http://127.0.0.1*|"http://[::1]"*|http://host.docker.internal*|http://api*|http://api:*) ;;
  http://*) say "WARNING: manager URL uses http, so probe-to-manager traffic is unencrypted. Fine for testing; use https in production." ;;
esac

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
    say "WARNING: manager not reachable at $PLATFORM_URL/health right now."
    say "  - Check PLATFORM_URL, that the manager is up, and the security group/firewall allows this host on that port."
    say "  - Installing anyway; the probe will keep retrying the connection in the background."
    say "  - Set SKIP_PREFLIGHT=true to silence this check entirely."
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

ENV_FILE="$(mktemp "${TMPDIR:-/tmp}/vedha-agent-env.XXXXXX")"
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
      printf 'PROBE_LICENSE_FILE=/var/lib/vedha-agent/license.token\n'
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
    -v "$STATE_VOL:/var/lib/vedha-agent" \
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

# Poll briefly for a running container so a slow first boot isn't a false "exited";
# stop early if it has already exited.
_i=0
while [ "$_i" -lt 15 ]; do
  [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)" = "true" ] && break
  [ "$(docker inspect -f '{{.State.Status}}' "$NAME" 2>/dev/null || true)" = "exited" ] && break
  _i=$((_i + 1)); sleep 1
done
if [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null || true)" != "true" ]; then
  say "ERROR: probe is not running after startup."
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
