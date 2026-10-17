#!/usr/bin/env bash
#
# set-public-url.sh — set the address agents and install commands use (MANAGER_PUBLIC_URL).
#
# Fleet -> Add agent only shows Windows install commands when MANAGER_PUBLIC_URL is an
# https:// address: the Windows installer refuses plain http (the install token and
# everything the agent sends must be encrypted). If the page says "This manager address
# cannot be embedded safely in a Windows command", MANAGER_PUBLIC_URL is http://<ip> —
# usually because scripts/gen-env.sh (make full / make aws-up) replaced the facade
# address with the server's IP. This script puts the right address back in one go:
#   1. writes MANAGER_PUBLIC_URL into the manager's .env (dated backup kept),
#   2. recreates the API so it picks the value up (no rebuild),
#   3. checks that the address answers over https and serves the agent manifest.
#
# Usage (on the manager server, with the facade address set up by install.sh):
#
#   sudo ./deploy/aws/set-public-url.sh --url https://get.vedhasec.com
#
# Options:
#   --url URL       the https:// address agents dial (required). Use the get.<domain>
#                   facade install.sh created, or https://api.<domain>. A bare IP only
#                   works if its certificate is trusted by Windows (a self-signed
#                   "tls internal" certificate is not).
#   --app-dir DIR   manager app dir (default: /opt/vedha, or $APP_DIR)
#   --no-verify     skip step 3
#
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/vedha}"
URL=""
VERIFY=1

while [ $# -gt 0 ]; do
  case "$1" in
    --url)       URL="${2:-}"; shift 2 ;;
    --app-dir)   APP_DIR="${2:-}"; shift 2 ;;
    --no-verify) VERIFY=0; shift ;;
    -h|--help)   sed -n '2,27p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

URL="${URL%/}"
[ -n "$URL" ] || { echo "error: --url is required, for example --url https://get.vedhasec.com" >&2; exit 2; }
# Same shape the Windows command builder accepts: https, a host name or IP, optional port.
printf '%s' "$URL" | grep -Eq '^https://[A-Za-z0-9.-]+(:[0-9]{1,5})?$' || {
  echo "error: --url must look like https://host or https://host:port (got '$URL')." >&2
  echo "       http:// cannot work: the Windows agent only talks to an https:// manager." >&2
  exit 2
}

ENV_FILE="$APP_DIR/.env"
[ -f "$ENV_FILE" ] || { echo "error: $ENV_FILE not found — is --app-dir correct?" >&2; exit 2; }
cd "$APP_DIR"

old="$(grep -E '^MANAGER_PUBLIC_URL=' "$ENV_FILE" | head -1 | cut -d= -f2- || true)"

# 1) write it — strip old copies, append fresh, rewrite in place so owner/permissions stay.
umask 077
cp -p "$ENV_FILE" "$ENV_FILE.bak.$(date +%Y%m%d%H%M%S)"
grep -v -E '^MANAGER_PUBLIC_URL=' "$ENV_FILE" > "$ENV_FILE.new" || true
echo "MANAGER_PUBLIC_URL=$URL" >> "$ENV_FILE.new"
cat "$ENV_FILE.new" > "$ENV_FILE"
rm -f "$ENV_FILE.new"
echo "[set-public-url] MANAGER_PUBLIC_URL: ${old:-<unset>} -> $URL (dated backup of .env kept)"

# 2) recreate the API with the same compose stack the deploy used (mirrors the Makefile).
COMPOSE=(docker compose --env-file "$ENV_FILE" -f "$APP_DIR/manager/docker-compose.yml")
if [ -f "$APP_DIR/deploy/tls/docker-compose.tls.yml" ]; then
  COMPOSE+=(-f "$APP_DIR/deploy/tls/docker-compose.tls.yml")
elif [ -f "$APP_DIR/deploy/aws/docker-compose.prod.yml" ]; then
  COMPOSE+=(-f "$APP_DIR/deploy/aws/docker-compose.prod.yml")
fi
"${COMPOSE[@]}" up -d --no-build api
echo "[set-public-url] API recreated"

[ "$VERIFY" = 1 ] || { echo "[set-public-url] done (not verified)."; exit 0; }

# 3) the address must answer over https with a certificate this server trusts, and serve
#    the agent manifest. The facade 503s for ~15s after an API recreate, so retry.
echo "[set-public-url] checking $URL/agent/manifest.json (up to ~60s)..."
ok=0
err=""
for _ in $(seq 1 20); do
  if err="$(curl -fsS --proto '=https' --tlsv1.2 -o /dev/null "$URL/agent/manifest.json" 2>&1)"; then ok=1; break; fi
  sleep 3
done

if [ "$ok" = 1 ]; then
  echo "[set-public-url] OK — $URL serves the agent manifest over https."
  echo ""
  echo "DONE. Reload Fleet -> Add agent: the Windows commands are offered again."
else
  echo "[set-public-url] WARNING: $URL/agent/manifest.json did not answer over https: $err" >&2
  echo "  - does DNS for the host point at this server?   getent hosts ${URL#https://}" >&2
  echo "  - is Caddy serving it? (restart after a Caddyfile change)  ${COMPOSE[*]} logs --tail 50 caddy" >&2
  echo "  - a self-signed / 'tls internal' certificate fails here and on Windows too: use a real domain." >&2
  exit 1
fi
