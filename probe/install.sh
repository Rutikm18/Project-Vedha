#!/usr/bin/env sh
# Intrynx probe installer — one command, no source on the client.
#
#   Fastest (one line, set vars):
#     curl -fsSL https://YOUR_HOST/install.sh | \
#       PLATFORM_URL=https://manager.example.com \
#       OPERATOR_EMAIL=you@org.com OPERATOR_PASSWORD=secret sh
#
#   Inspect-first (recommended for security teams):
#     curl -fsSL https://YOUR_HOST/install.sh -o install.sh
#     less install.sh           # read it
#     sh install.sh             # interactive — it asks for what it needs
#
#   Get this machine's Host ID (to request a license), no install:
#     sh install.sh hostid
set -eu

IMAGE="${PROBE_IMAGE:-intrynx-probe:sealed}"      # vendor registry path, e.g. registry.example.com/intrynx-probe:1.0
NAME="${PROBE_CONTAINER:-intrynx-probe}"
STATE_VOL="${PROBE_STATE_VOLUME:-intrynx-probe-state}"

say() { printf '%s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }

# --- preflight ----------------------------------------------------------------
have docker || { say "Docker is required. Install it first: https://docs.docker.com/engine/install/"; exit 1; }

# pull the sealed image (skip if it's a local image already present)
docker image inspect "$IMAGE" >/dev/null 2>&1 || {
  say "Pulling $IMAGE ..."; docker pull "$IMAGE" || { say "Could not pull $IMAGE — check PROBE_IMAGE / registry login."; exit 1; }
}

# --- hostid shortcut ----------------------------------------------------------
if [ "${1:-}" = "hostid" ]; then
  exec docker run --rm -v "$STATE_VOL:/var/lib/adversa-probe" "$IMAGE" hostid
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

ask PLATFORM_URL    "Manager URL (https://...)"
ask OPERATOR_EMAIL  "Operator email (to register)"
ask OPERATOR_PASSWORD "Operator password"
ask PROBE_NAME      "Probe name" "$(hostname)"
ask PROBE_LICENSE   "Deployment license (blank if licensing is disabled)" ""

[ -n "${PLATFORM_URL:-}" ] || { say "PLATFORM_URL is required."; exit 1; }

# --- run ----------------------------------------------------------------------
say "Starting probe '$PROBE_NAME' -> $PLATFORM_URL ..."
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" --restart unless-stopped \
  -e PLATFORM_URL="$PLATFORM_URL" \
  -e OPERATOR_EMAIL="${OPERATOR_EMAIL:-}" \
  -e OPERATOR_PASSWORD="${OPERATOR_PASSWORD:-}" \
  -e PROBE_NAME="$PROBE_NAME" \
  -e PROBE_LICENSE="${PROBE_LICENSE:-}" \
  -e LICENSE_ENFORCED="${LICENSE_ENFORCED:-true}" \
  -v "$STATE_VOL:/var/lib/adversa-probe" \
  "$IMAGE" run >/dev/null

say ""
say "Probe is running.  Logs:    docker logs -f $NAME"
say "                   Host ID: docker run --rm -v $STATE_VOL:/var/lib/adversa-probe $IMAGE hostid"
say "                   Stop:    docker rm -f $NAME"
