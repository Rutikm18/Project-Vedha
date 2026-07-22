#!/usr/bin/env sh
# Vedha probe installer — one command, no source tree on the client.
#
#   Fastest (one line, set vars):
#     curl -fsSL https://YOUR_HOST/install.sh | \
#       PLATFORM_URL=https://manager.example.com \
#       OPERATOR_TOKEN=vpat_xxx sh
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

# --- hostid shortcut ----------------------------------------------------------
if [ "${1:-}" = "hostid" ]; then
  exec docker run --rm -v "$STATE_VOL:/var/lib/vedha-probe" "$IMAGE" hostid
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

[ -n "${PLATFORM_URL:-}" ] || { say "PLATFORM_URL is required."; exit 1; }
if [ -z "${OPERATOR_TOKEN:-}" ] && [ -z "${OPERATOR_EMAIL:-}" ]; then
  say "OPERATOR_TOKEN/PROBE_PAT is required for production installs."
  say "Development fallback OPERATOR_EMAIL/OPERATOR_PASSWORD is still accepted if explicitly set."
  exit 1
fi

# --- run ----------------------------------------------------------------------
say "Starting probe '$PROBE_NAME' -> $PLATFORM_URL ..."
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --restart unless-stopped \
  -e PLATFORM_URL="$PLATFORM_URL" \
  -e VERIFY_TLS="$VERIFY_TLS" \
  -e OPERATOR_TOKEN="${OPERATOR_TOKEN:-}" \
  -e OPERATOR_EMAIL="${OPERATOR_EMAIL:-}" \
  -e OPERATOR_PASSWORD="${OPERATOR_PASSWORD:-}" \
  -e PROBE_NAME="$PROBE_NAME" \
  -e PROBE_LOCATION="${PROBE_LOCATION:-}" \
  -e PROBE_NETWORK_SEGMENTS="${PROBE_NETWORK_SEGMENTS:-}" \
  -e PROBE_LICENSE="${PROBE_LICENSE:-}" \
  -e LICENSE_ENFORCED="$LICENSE_ENFORCED" \
  -v "$STATE_VOL:/var/lib/vedha-probe" \
  "$IMAGE" >/dev/null

say ""
say "Probe is running.  Logs:    docker logs -f $NAME"
say "                   Host ID: docker run --rm -v $STATE_VOL:/var/lib/vedha-probe $IMAGE hostid"
say "                   Stop:    docker rm -f $NAME"
