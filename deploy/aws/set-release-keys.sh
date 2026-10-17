#!/usr/bin/env bash
#
# set-release-keys.sh — turn on a published signed agent release (run AFTER B2).
#
# publish-release.ps1 (B2) builds, signs and UPLOADS the release to this server and
# prints two PUBLIC verification keys. This script does the rest in one go:
#   1. writes those two public keys into the manager's .env (idempotent),
#   2. recreates the API so it serves the signed release (the exact compose stack
#      install.sh uses — no full rebuild),
#   3. verifies the manager now serves the Windows package.
#
# The PRIVATE keys never touch the server; only the public halves live here.
#
# Usage (on the manager server, from the app dir, with the two keys from B2):
#
#   sudo ./deploy/aws/set-release-keys.sh \
#       --ed25519 '<AGENT_RELEASE_PUBLIC_KEY value>' \
#       --p256    '<AGENT_RELEASE_P256_PUBLIC_KEY value>'
#
# Options:
#   --app-dir DIR   manager app dir            (default: /opt/vedha, or $APP_DIR)
#   --facade URL    facade to verify through   (default: MANAGER_PUBLIC_URL from .env)
#
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/vedha}"
FACADE="${FACADE:-}"
ED=""
P256=""

while [ $# -gt 0 ]; do
  case "$1" in
    --ed25519) ED="${2:-}"; shift 2 ;;
    --p256)    P256="${2:-}"; shift 2 ;;
    --app-dir) APP_DIR="${2:-}"; shift 2 ;;
    --facade)  FACADE="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

ENV_FILE="$APP_DIR/.env"
[ -f "$ENV_FILE" ] || { echo "error: $ENV_FILE not found — is --app-dir correct?" >&2; exit 2; }

# A public key here is base64 (Ed25519 raw, or P-256 DER SPKI). Reject junk early.
is_b64() { printf '%s' "$1" | grep -Eq '^[A-Za-z0-9+/=]{20,}$'; }
[ -n "$ED" ]   || { echo "error: --ed25519 is required (the AGENT_RELEASE_PUBLIC_KEY value from B2)" >&2; exit 2; }
[ -n "$P256" ] || { echo "error: --p256 is required (the AGENT_RELEASE_P256_PUBLIC_KEY value from B2)" >&2; exit 2; }
is_b64 "$ED"   || { echo "error: --ed25519 does not look like a base64 public key: '$ED'" >&2; exit 2; }
is_b64 "$P256" || { echo "error: --p256 does not look like a base64 public key: '$P256'" >&2; exit 2; }

if [ -z "$FACADE" ]; then
  FACADE="$(grep -E '^MANAGER_PUBLIC_URL=' "$ENV_FILE" | head -1 | cut -d= -f2- || true)"
fi

cd "$APP_DIR"

# 1) write the keys into .env — strip any old copies, append fresh, keep a private backup.
umask 077
cp -p "$ENV_FILE" "$ENV_FILE.bak.$(date +%Y%m%d%H%M%S)"
grep -v -E '^(AGENT_RELEASE_PUBLIC_KEY|AGENT_RELEASE_P256_PUBLIC_KEY|AGENT_RELEASE_REQUIRE_SIGNATURE)=' "$ENV_FILE" > "$ENV_FILE.new"
{
  echo "AGENT_RELEASE_PUBLIC_KEY=$ED"
  echo "AGENT_RELEASE_P256_PUBLIC_KEY=$P256"
  echo "AGENT_RELEASE_REQUIRE_SIGNATURE=true"
} >> "$ENV_FILE.new"
cat "$ENV_FILE.new" > "$ENV_FILE"      # rewrite in place so owner/permissions are kept
rm -f "$ENV_FILE.new"
echo "[set-release-keys] release keys written to $ENV_FILE (dated backup kept)"

# 2) recreate the API with the new environment — the same compose stack install.sh uses.
COMPOSE=(docker compose
  --env-file "$APP_DIR/.env"
  -f "$APP_DIR/manager/docker-compose.yml"
  -f "$APP_DIR/deploy/aws/docker-compose.prod.yml"
)
"${COMPOSE[@]}" up -d --no-build api
echo "[set-release-keys] API recreated with the release keys"

# 3) verify the manager now serves the Windows package.
echo "[set-release-keys] verifying the Windows manifest (up to ~40s)..."
check_url="http://127.0.0.1:8000/agent/manifest.json"
[ -n "$FACADE" ] && check_url="${FACADE%/}/agent/manifest.json"
ok=0
for _ in $(seq 1 12); do
  if curl -fsS "$check_url" 2>/dev/null | grep -qi 'windows'; then ok=1; break; fi
  sleep 3
done

if [ "$ok" = 1 ]; then
  echo "[set-release-keys] OK — the manager serves the Windows package."
  echo ""
  echo "DONE. For each client machine: console -> Fleet -> Add agent -> Windows ->"
  echo "Generate, then send the client the one line. No Windows build per client."
else
  echo "[set-release-keys] WARNING: no Windows package is being served yet." >&2
  echo "  - is the release uploaded?   ls -1 $APP_DIR/manager/agent-releases" >&2
  echo "  - what does the API say?      ${COMPOSE[*]} logs --tail 50 api" >&2
  echo "  - did B2 finish the upload without error?" >&2
  exit 1
fi
