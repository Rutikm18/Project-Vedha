#!/usr/bin/env sh
# Vedha probe installer — one command, no human credential on the client.
#
#   Supported flow (Fleet → Add agent prints this with your token filled in):
#     curl --proto '=https' --tlsv1.2 -fsSL https://api.example.com/agent/install.sh \
#       | sudo sh -s -- --manager https://api.example.com --token vet_...
#
#   Inspect-first:
#     curl --proto '=https' --tlsv1.2 -fsSL -o vedha-install.sh https://api.example.com/agent/install.sh
#     less vedha-install.sh
#     sudo sh vedha-install.sh --manager https://api.example.com --token vet_...
#
#   The agent image comes from YOUR manager, never a public registry: the
#   installer downloads the signed release manifest, verifies its Ed25519
#   signature with the key embedded below, downloads the image for this CPU with
#   the token, and refuses to load it unless its SHA-256 matches the manifest.
set -eu

# ── Native cross-OS brain path (Phase 7) ─────────────────────────────────────
# `install.sh <doctor|config|self-scan|connect> [--strict|--insecure] ...`
# Ensures Python 3.8+ (+ the venv module) per OS, then hands off to the ONE brain
# CLI (agent.setup). Strict security is optional in this initial phase: pass
# --strict for fail-closed verification, or --insecure (default) to skip it.
# The legacy LOCAL/DOCKER modes below are unchanged for backward compatibility.
case "${1:-}" in
  doctor|config|self-scan|connect|--strict|--insecure)
    cd "$(dirname "$0")"
    if ! command -v python3 >/dev/null 2>&1; then
      if   command -v apt-get >/dev/null 2>&1; then sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
      elif command -v dnf     >/dev/null 2>&1; then sudo dnf install -y python3 python3-pip
      elif command -v pacman  >/dev/null 2>&1; then sudo pacman -S --noconfirm python python-pip
      elif command -v brew    >/dev/null 2>&1; then brew install python
      else echo "Install Python 3.8+ (and the venv module), then re-run." >&2; exit 1; fi
    fi
    python3 -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3, 8) else 1)' \
      || { echo "Python 3.8+ required." >&2; exit 1; }
    python3 -c 'import venv' 2>/dev/null \
      || { command -v apt-get >/dev/null 2>&1 && sudo apt-get install -y python3-venv; }
    exec python3 -m agent.setup "$@"
    ;;
esac

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
# Set by scripts/agent_release.py when this file is packaged into a signed agent
# release; empty in the repository copy (development installs skip the check).
VEDHA_RELEASE_SPKI=""
VEDHA_RELEASE_VERSION=""
# Matches scripts/agent_release.py key_id(): SHA-256 of the raw Ed25519 key, 16 hex.
release_key_id() {
  printf '%s' "$VEDHA_RELEASE_SPKI" | { base64 -d 2>/dev/null || openssl base64 -d -A; } \
    | tail -c 32 | { sha256sum 2>/dev/null || shasum -a 256; } | cut -c1-16
}

_IMAGE_EXPLICIT="${PROBE_IMAGE:+yes}"
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
PROBE_PROXY="${PROBE_PROXY:-}"
PROBE_NO_PROXY="${PROBE_NO_PROXY:-}"
PROBE_CA_BUNDLE_FILE="${PROBE_CA_BUNDLE_FILE:-}"
# A signed release (key embedded above) always requires a verified signature;
# only a development installer from the repository runs without one.
if [ -n "$VEDHA_RELEASE_SPKI" ]; then PROBE_REQUIRE_SIGNATURE=true; fi
PROBE_REQUIRE_SIGNATURE="${PROBE_REQUIRE_SIGNATURE:-false}"
PROBE_TOKEN_FILE=""

usage() {
  say "Usage: $0 --manager https://api.example.com --token vet_... [options]"
  say "  --token, --enroll-token  Install token from Fleet → Add agent: downloads the agent and"
  say "                           enrols it with no approval step (single use, expires)."
  say "  --token-file FILE        Read the install token from FILE instead (keeps it out of shell"
  say "                           history and the process list)."
  say "  --name NAME              Agent host name shown in Fleet (default: this hostname)."
  say "  --proxy URL              Outbound HTTP(S) proxy, e.g. http://proxy.corp:3128 — used by"
  say "                           this installer and by the agent."
  say "  --no-proxy LIST          Hosts that bypass the proxy (comma-separated)."
  say "  --ca-bundle FILE         Extra CA certificates (PEM) for a TLS-inspecting proxy."
  say "  --require-signature      Fail if the release signature cannot be checked (always on for a"
  say "                           signed release)."
  say "  --insecure               Allow an http:// manager (testing only; production requires https)."
  say "  --uninstall              Remove the agent container (PROBE_PURGE=true also deletes its identity)."
  say "Only the Manager endpoint is deployment-specific; scope comes from the token or Fleet."
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --manager)
      [ "$#" -ge 2 ] || { say "ERROR: --manager requires a value."; usage; exit 2; }
      PLATFORM_URL=$2
      shift 2
      ;;
    --enroll-token|--token)
      [ "$#" -ge 2 ] || { say "ERROR: $1 requires a value."; usage; exit 2; }
      PROBE_ENROLL_TOKEN=$2
      shift 2
      ;;
    --token-file)
      [ "$#" -ge 2 ] || { say "ERROR: --token-file requires a file."; usage; exit 2; }
      PROBE_TOKEN_FILE=$2
      shift 2
      ;;
    --name)
      [ "$#" -ge 2 ] || { say "ERROR: --name requires a value."; usage; exit 2; }
      PROBE_NAME=$2
      shift 2
      ;;
    --proxy)
      [ "$#" -ge 2 ] || { say "ERROR: --proxy requires a value."; usage; exit 2; }
      PROBE_PROXY=$2
      shift 2
      ;;
    --no-proxy)
      [ "$#" -ge 2 ] || { say "ERROR: --no-proxy requires a value."; usage; exit 2; }
      PROBE_NO_PROXY=$2
      shift 2
      ;;
    --ca-bundle)
      [ "$#" -ge 2 ] || { say "ERROR: --ca-bundle requires a file."; usage; exit 2; }
      PROBE_CA_BUNDLE_FILE=$2
      shift 2
      ;;
    --require-signature)
      PROBE_REQUIRE_SIGNATURE=true
      shift
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

if [ -n "$PROBE_TOKEN_FILE" ]; then
  [ -r "$PROBE_TOKEN_FILE" ] || { say "ERROR: --token-file '$PROBE_TOKEN_FILE' is not readable."; exit 2; }
  PROBE_ENROLL_TOKEN="$(tr -d ' \t\r\n' < "$PROBE_TOKEN_FILE")"
  [ -n "$PROBE_ENROLL_TOKEN" ] || { say "ERROR: --token-file '$PROBE_TOKEN_FILE' is empty."; exit 2; }
fi

PLATFORM_URL="${PLATFORM_URL:-}"
PROBE_NAME="${PROBE_NAME:-$(hostname)}"
PROBE_LOCATION="${PROBE_LOCATION:-}"
PROBE_NETWORK_SEGMENTS="${PROBE_NETWORK_SEGMENTS:-}"

[ -n "$PLATFORM_URL" ] || { say "ERROR: --manager is required."; usage; exit 2; }
PLATFORM_URL="${PLATFORM_URL%/}"

if [ "${PROBE_INSTALL_DRY_RUN:-false}" = "true" ]; then
  say "Dry-run preview (no Docker or connectivity checks were run)."
  if [ -n "$_IMAGE_EXPLICIT" ] || [ -n "${PROBE_IMAGE_TAR_URL:-}" ]; then
    say "Image: $IMAGE"
  elif [ -n "$PROBE_ENROLL_TOKEN" ]; then
    say "Image: signed agent release from $PLATFORM_URL/agent (verified before loading)"
    [ -n "$VEDHA_RELEASE_SPKI" ] && say "Release signing key: $(release_key_id) (signature required)"
  else
    say "Image: $IMAGE if present locally, else the signed release from the manager (needs --token)"
  fi
  [ -n "$PROBE_PROXY" ] && say "Proxy: $PROBE_PROXY (installer and agent)"
  [ -n "$PROBE_CA_BUNDLE_FILE" ] && say "Extra CA bundle: $PROBE_CA_BUNDLE_FILE"
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

# The container restarts with Docker (--restart unless-stopped), but only if
# Docker itself starts at boot — not the default on every distribution.
if have systemctl && [ "$(systemctl is-enabled docker 2>/dev/null || true)" = "disabled" ]; then
  if systemctl enable docker >/dev/null 2>&1; then
    say "Enabled Docker at boot so the agent comes back after a reboot."
  else
    say "WARNING: Docker does not start at boot. Run 'systemctl enable docker', or the agent stays"
    say "  offline after this host reboots."
  fi
fi

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

# ── Download from the manager's signed release (the production path) ─────────
case "$(uname -m 2>/dev/null || echo unknown)" in
  x86_64|amd64) HOST_ARCH=amd64 ;;
  aarch64|arm64) HOST_ARCH=arm64 ;;
  *) HOST_ARCH="$(uname -m 2>/dev/null || echo unknown)" ;;
esac

# Outbound proxy / private CA for this installer's own downloads. `sudo` drops the
# caller's proxy variables, which is why they are flags; the same values are
# written into the agent's config below so it uses them too.
if [ -n "$PROBE_PROXY" ]; then
  export HTTPS_PROXY="$PROBE_PROXY" HTTP_PROXY="$PROBE_PROXY" https_proxy="$PROBE_PROXY" http_proxy="$PROBE_PROXY"
fi
if [ -n "$PROBE_NO_PROXY" ]; then
  export NO_PROXY="$PROBE_NO_PROXY" no_proxy="$PROBE_NO_PROXY"
fi
CURL_CA=""
if [ -n "$PROBE_CA_BUNDLE_FILE" ]; then
  [ -r "$PROBE_CA_BUNDLE_FILE" ] || { say "ERROR: --ca-bundle file '$PROBE_CA_BUNDLE_FILE' is not readable."; exit 2; }
  grep -q 'BEGIN CERTIFICATE' "$PROBE_CA_BUNDLE_FILE" || { say "ERROR: --ca-bundle must be a PEM file with at least one CERTIFICATE."; exit 2; }
  CURL_CA="$PROBE_CA_BUNDLE_FILE"
fi

# GET $1 into $2 (optionally with the header file $3); prints the HTTP status.
http_get() {
  set -- "$1" "$2" "${3:-}"
  if [ -n "$3" ]; then
    curl -sSL --connect-timeout 10 --retry 3 --retry-delay 2 ${CURL_CA:+--cacert "$CURL_CA"} \
      -H "@$3" -o "$2" -w '%{http_code}' "$1" 2>"$STAGE_DIR/curl.err" || true
  else
    curl -sSL --connect-timeout 10 --retry 3 --retry-delay 2 ${CURL_CA:+--cacert "$CURL_CA"} \
      -o "$2" -w '%{http_code}' "$1" 2>"$STAGE_DIR/curl.err" || true
  fi
}

# One field of the image entry for an architecture in the signed manifest. The
# release tool writes JSON with sorted keys and fixed indentation, and the
# values are re-validated below, so a minimal awk reader is enough (no jq).
manifest_image_field() {
  awk -v arch="$2" -v key="$3" '
    /"arch":/ { inblock = (index($0, "\"arch\": \"" arch "\"") > 0) }
    inblock && index($0, "\"" key "\":") {
      line = $0; sub(/^[^:]*: */, "", line); gsub(/[",]/, "", line); print line; exit
    }
    /^ *}/ { inblock = 0 }
  ' "$1"
}

verify_manifest_signature() {
  if [ -z "$VEDHA_RELEASE_SPKI" ]; then
    if [ "$PROBE_REQUIRE_SIGNATURE" = "true" ]; then
      say "ERROR: this installer has no release key embedded. Download it from your manager"
      say "  (Fleet → Add agent) instead of using a copy from the source repository."
      exit 1
    fi
    say "NOTE: development installer (no release key embedded) — skipping the signature check."
    return 0
  fi
  tr -d '\n\r ' < "$STAGE_DIR/manifest.json.sig" > "$STAGE_DIR/manifest.sig.b64"
  _verified=""
  _ossl="$(openssl version 2>/dev/null || true)"
  case "$_ossl" in
    "OpenSSL 3."*|"OpenSSL 4."*)
      printf -- '-----BEGIN PUBLIC KEY-----\n%s\n-----END PUBLIC KEY-----\n' "$VEDHA_RELEASE_SPKI" > "$STAGE_DIR/release.pub"
      if openssl base64 -d -A -in "$STAGE_DIR/manifest.sig.b64" -out "$STAGE_DIR/manifest.sig.bin" 2>/dev/null \
        && openssl pkeyutl -verify -pubin -inkey "$STAGE_DIR/release.pub" -rawin \
             -in "$STAGE_DIR/manifest.json" -sigfile "$STAGE_DIR/manifest.sig.bin" >/dev/null 2>&1; then
        _verified=openssl
      else
        _verified=bad
      fi
      ;;
  esac
  # Older OpenSSL (RHEL 8, Ubuntu 20.04, Amazon Linux 2) cannot do Ed25519;
  # Python's cryptography package can, when it is installed.
  if [ -z "$_verified" ] && have python3 && python3 -c 'import cryptography' >/dev/null 2>&1; then
    if python3 - "$VEDHA_RELEASE_SPKI" "$STAGE_DIR/manifest.json" "$STAGE_DIR/manifest.sig.b64" <<'PYEOF'
import base64, sys
from cryptography.hazmat.primitives.serialization import load_der_public_key
spki, manifest, sig = sys.argv[1:4]
key = load_der_public_key(base64.b64decode(spki))
key.verify(base64.b64decode(open(sig).read().strip()), open(manifest, "rb").read())
PYEOF
    then _verified=python
    else _verified=bad
    fi
  fi
  if [ "$_verified" = "bad" ]; then
    say "ERROR: the agent release signature does NOT verify. Refusing to install."
    say "  The release on $PLATFORM_URL was not signed by the key this installer trusts."
    say "  Tell your Vedha contact; do not work around this."
    exit 1
  fi
  if [ -z "$_verified" ]; then
    if [ "$PROBE_REQUIRE_SIGNATURE" = "true" ]; then
      say "ERROR: this host cannot check the release signature: it needs OpenSSL 3 (found:"
      say "  ${_ossl:-none}) or python3 with the 'cryptography' package."
      say "  Use a supported host (Ubuntu 22.04+, Debian 12, RHEL 9, Amazon Linux 2023), or install"
      say "  python3-cryptography, then run the installer again."
      exit 1
    fi
    say "WARNING: OpenSSL 3 not found (${_ossl:-none}); the release signature can't be checked on"
    say "  this host. The image is still checked against the manifest's SHA-256 over HTTPS."
    return 0
  fi
  say "Release signature verified (signing key $(release_key_id))."
}

load_image_from_manager() {
  say "Fetching the agent release from $PLATFORM_URL ..."
  _code="$(http_get "$PLATFORM_URL/agent/manifest.json" "$STAGE_DIR/manifest.json")"
  case "$_code" in
    200) ;;
    503) say "ERROR: the manager has no agent release to hand out yet. Ask your Vedha administrator"
         say "  to publish one (scripts/agent_release.py), then run this command again."; exit 1 ;;
    000) say "ERROR: could not reach $PLATFORM_URL ($(tr -d '\n' < "$STAGE_DIR/curl.err" | cut -c1-160))."
         say "  Check outbound HTTPS (443) to the manager, DNS, and any proxy (--proxy URL)."
         say "  A TLS-inspecting proxy needs --ca-bundle FILE, or an inspection exemption for the manager."
         exit 1 ;;
    *)   say "ERROR: manifest download failed (HTTP $_code)."; exit 1 ;;
  esac
  if [ -n "$VEDHA_RELEASE_SPKI" ]; then
    _code="$(http_get "$PLATFORM_URL/agent/manifest.json.sig" "$STAGE_DIR/manifest.json.sig")"
    [ "$_code" = "200" ] || { say "ERROR: the release signature is missing on the manager (HTTP $_code). Refusing to install."; exit 1; }
  fi
  verify_manifest_signature

  _ver="$(awk -F'"' '/^  "version":/ {print $4; exit}' "$STAGE_DIR/manifest.json")"
  IMG_FILE="$(manifest_image_field "$STAGE_DIR/manifest.json" "$HOST_ARCH" file)"
  IMG_SHA="$(manifest_image_field "$STAGE_DIR/manifest.json" "$HOST_ARCH" sha256)"
  IMG_TAG="$(manifest_image_field "$STAGE_DIR/manifest.json" "$HOST_ARCH" tag)"
  if [ -z "$IMG_FILE" ]; then
    say "ERROR: agent release ${_ver:-?} has no image for this CPU ($HOST_ARCH)."
    exit 1
  fi
  case "$IMG_FILE" in .*|*[!A-Za-z0-9._-]*) say "ERROR: malformed manifest (file name)."; exit 1 ;; esac
  case "$IMG_TAG" in ""|*[!a-z0-9._/:-]*) say "ERROR: malformed manifest (image tag)."; exit 1 ;; esac
  case "$IMG_SHA" in *[!0-9a-f]*) IMG_SHA="" ;; esac
  [ "${#IMG_SHA}" -eq 64 ] || { say "ERROR: malformed manifest (checksum)."; exit 1; }
  if [ -n "$VEDHA_RELEASE_VERSION" ] && [ "$VEDHA_RELEASE_VERSION" != "$_ver" ]; then
    say "NOTE: installer is from release $VEDHA_RELEASE_VERSION; the manager now serves $_ver."
  fi

  if [ -z "$PROBE_ENROLL_TOKEN" ]; then
    say "ERROR: downloading the agent needs an install token. In Fleet → Add agent, copy the"
    say "  command — it includes --token vet_... — and run that instead."
    exit 2
  fi
  # The token goes in a private header file, not on the command line (ps).
  ( umask 077; printf 'Authorization: Bearer %s\n' "$PROBE_ENROLL_TOKEN" > "$STAGE_DIR/auth.hdr" )
  say "Downloading agent ${_ver:-} for $HOST_ARCH ..."
  _code="$(http_get "$PLATFORM_URL/agent/image/$HOST_ARCH" "$STAGE_DIR/$IMG_FILE" "$STAGE_DIR/auth.hdr")"
  rm -f "$STAGE_DIR/auth.hdr"
  case "$_code" in
    200) ;;
    401) say "ERROR: the install token was refused — it is expired, revoked or already used."
         say "  Create a new install command in Fleet → Add agent."; exit 1 ;;
    429) say "ERROR: too many downloads from this address; wait a minute and retry."; exit 1 ;;
    *)   say "ERROR: agent download failed (HTTP $_code)."; exit 1 ;;
  esac
  _got="$( { sha256sum "$STAGE_DIR/$IMG_FILE" 2>/dev/null || shasum -a 256 "$STAGE_DIR/$IMG_FILE" 2>/dev/null; } | awk '{print $1}')"
  if [ "$_got" != "$IMG_SHA" ]; then
    say "ERROR: the downloaded agent does not match the release checksum. Refusing to load it."
    say "  expected $IMG_SHA"
    say "  got      ${_got:-none}"
    exit 1
  fi
  say "Checksum verified. Loading the agent image ..."
  docker load -i "$STAGE_DIR/$IMG_FILE" >/dev/null
  rm -f "$STAGE_DIR/$IMG_FILE"
  IMAGE="$IMG_TAG"
}

# Image source precedence:
#   1. PROBE_IMAGE (explicit) — already loaded, PROBE_IMAGE_TAR_URL, or a registry pull,
#   2. PROBE_IMAGE_TAR_URL hosted by the operator,
#   3. the manager's signed release — the default whenever an install token is given,
#   4. a locally built vedha-agent:local (development, no token).
if [ -z "$_IMAGE_EXPLICIT" ] && [ -z "${PROBE_IMAGE_TAR_URL:-}" ]; then
  if [ -n "$PROBE_ENROLL_TOKEN" ] || ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
    load_image_from_manager
  fi
fi

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

# Host binding is a LICENSING control: it only exists for the licensed agent
# (LICENSE_ENFORCED=true). It pins a deterministic container MAC and records the
# hardware id derived from it. The standard agent skips it entirely — on hosts
# where --mac-address is rejected or silently ignored (rootless Docker, Podman,
# a Docker CLI older than its daemon) every container gets a random MAC, the id
# changes, and the agent would refuse to start.
if [ "$LICENSE_ENFORCED" = "true" ]; then
  # A locally administered MAC derived from the container name is deterministic
  # and does not collide with vendor OUIs.
  if [ -z "${PROBE_MAC_ADDRESS:-}" ]; then
    PROBE_MAC_ADDRESS="$(docker run --rm --network none --read-only \
      --cap-drop ALL --security-opt no-new-privileges:true --user 10001:10001 \
      --entrypoint python "$IMAGE" -c \
      'import hashlib,sys; d=hashlib.sha256(sys.argv[1].encode()).digest(); print("02:42:%02x:%02x:%02x:%02x" % tuple(d[:4]))' \
      "$NAME")"
  fi
  if [ -z "${PROBE_HW_ID:-}" ]; then
    # Prints the hardware id only when the requested MAC really took effect.
    PROBE_HW_ID="$(docker run --rm --read-only --cap-drop ALL \
      --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
      --hostname "$NAME" --mac-address "$PROBE_MAC_ADDRESS" \
      --entrypoint python "$IMAGE" -c \
      'import sys, uuid
from agent.hw_bind import get_hw_id
want = int(sys.argv[1].replace(":", ""), 16)
raise SystemExit(print(get_hw_id()) if uuid.getnode() == want else 3)' \
      "$PROBE_MAC_ADDRESS" 2>/dev/null || true)"
    if [ -z "$PROBE_HW_ID" ]; then
      say "ERROR: this Docker cannot pin the container MAC address that the licensed agent's"
      say "  host binding needs (rootless Docker, Podman, Docker Desktop, or a Docker CLI older"
      say "  than its daemon). Use a rootful Docker Engine with matching client and daemon, or"
      say "  set PROBE_MAC_ADDRESS + PROBE_HW_ID explicitly."
      exit 1
    fi
  fi
else
  PROBE_MAC_ADDRESS=""
  PROBE_HW_ID=""
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
if licensing == "true" or mac or hwid:
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

# A private CA (TLS-inspecting proxy) lives in the agent's own state volume, not
# a host bind mount — no SELinux relabelling, and it moves with the identity.
store_ca_bundle() {
  [ -n "$PROBE_CA_BUNDLE_FILE" ] || return 0
  if ! docker run --rm -i \
    --network none --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --pids-limit 64 --user 10001:10001 \
    -v "$STATE_VOL:/state" --entrypoint python "$IMAGE" -c \
    'import os,sys; os.umask(0o022); open("/state/ca-bundle.pem","w",encoding="utf-8").write(sys.stdin.read())' \
    < "$PROBE_CA_BUNDLE_FILE"
  then
    say "Could not store the CA bundle in the agent's state volume."
    exit 1
  fi
}

store_ca_bundle

# --- preflight: reach the Manager before creating local runtime state ---------
if [ "${SKIP_PREFLIGHT:-false}" != "true" ] && have curl; then
  ctls=""; [ "$VERIFY_TLS" = "false" ] && ctls="-k"
  say "Checking manager at $PLATFORM_URL ..."
  if ! curl -fsS --connect-timeout 5 --max-time 15 $ctls ${CURL_CA:+--cacert "$CURL_CA"} \
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
  "${PROBE_ENROLL_TOKEN:-}" "$PROBE_PROXY" "$PROBE_NO_PROXY"
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
    if [ -n "$PROBE_HW_ID" ]; then
      printf 'HW_BIND_FINGERPRINT=%s\n' "$PROBE_HW_ID"
    fi
    if [ -n "$PROBE_ENROLL_TOKEN" ]; then
      # Pre-authorized, Site-bound enrollment token. Consumed once on first boot
      # to auto-approve; the durable identity is the device key + refresh secret.
      printf 'PROBE_ENROLL_TOKEN=%s\n' "$PROBE_ENROLL_TOKEN"
    fi
    if [ -n "$PROBE_PROXY" ]; then
      # httpx and websockets both honour these; the manager is reached through it.
      printf 'HTTPS_PROXY=%s\nHTTP_PROXY=%s\nhttps_proxy=%s\nhttp_proxy=%s\n' \
        "$PROBE_PROXY" "$PROBE_PROXY" "$PROBE_PROXY" "$PROBE_PROXY"
      # Scan targets are on the LAN: never send them through the proxy.
      _np="localhost,127.0.0.1,::1${PROBE_NO_PROXY:+,$PROBE_NO_PROXY}"
      printf 'NO_PROXY=%s\nno_proxy=%s\n' "$_np" "$_np"
    fi
    if [ -n "$PROBE_CA_BUNDLE_FILE" ]; then
      printf 'PROBE_CA_BUNDLE=/var/lib/vedha-agent/ca-bundle.pem\n'
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
    ${PROBE_MAC_ADDRESS:+--mac-address "$PROBE_MAC_ADDRESS"} --restart unless-stopped \
    --read-only \
    --tmpfs /tmp:size=64m,mode=1777 \
    --cap-drop ALL \
    --security-opt no-new-privileges:true \
    --pids-limit 256 \
    --init \
    --log-driver json-file --log-opt max-size=10m --log-opt max-file=5 \
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
  existing_image="$(docker inspect -f '{{.Config.Image}}' "$NAME" 2>/dev/null || true)"
  if [ "$existing_image" != "$IMAGE" ]; then
    # Upgrade: a new image needs a new container. The identity and enrolment live
    # in the state volume, so the agent keeps its place in Fleet.
    say "Upgrading the agent: $existing_image -> $IMAGE (identity kept)."
    docker rm -f "$NAME" >/dev/null
    run_probe_container
  else
    docker start "$NAME" >/dev/null
    say "Existing probe installation preserved and started."
  fi
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
say "OK: agent '$PROBE_NAME' is installed with no PAT or human credential."
if [ -n "$PROBE_ENROLL_TOKEN" ]; then
  say "It enrols itself with the install token and shows as connected in Fleet within a minute."
else
  say "Approve the code shown below in Fleet (portal: enter it under Add agent)."
fi
docker logs --tail 20 "$NAME" 2>&1 || true
say ""
say "Logs:    docker logs -f $NAME"
say "Stop:    docker rm -f $NAME"
