#!/usr/bin/env sh
# Mint a probe-scoped Vedha Personal Access Token (vpat_...) via the manager API.
# There is NO PAT UI in the dashboard — this is the supported one-command path
# when an operator needs to copy a token for another client.
#
#   make probe-pat
#   scripts/issue_pat.sh --url https://vedha.example.com --email admin@you.com --days 90
#
# Password source (first that is set): ADMIN_PASSWORD, SEED_ADMIN_PASSWORD,
# SEED_ADMIN_PASSWORD in ./.env, else an interactive prompt. The password is sent
# on stdin (never on the command line / process list).
set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
envval() { [ -f "$ENV_FILE" ] && grep -E "^$1=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- || true; }

NAME=""; DAYS="365"; URL=""; EMAIL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --url)   URL="$2";   shift 2 ;;
    --email) EMAIL="$2"; shift 2 ;;
    --name)  NAME="$2";  shift 2 ;;
    --days)  DAYS="$2";  shift 2 ;;
    -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

command -v curl    >/dev/null 2>&1 || { echo "curl is required."    >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required." >&2; exit 1; }

# Resolve manager URL: --url > PLATFORM_URL/BASE > http://localhost:<API_PORT>
[ -n "$URL" ] || URL="${PLATFORM_URL:-${BASE:-}}"
if [ -z "$URL" ]; then port="$(envval API_PORT)"; URL="http://localhost:${port:-18080}"; fi
URL="${URL%/}"

# Resolve admin email
[ -n "$EMAIL" ] || EMAIL="${ADMIN_EMAIL:-${SEED_ADMIN_EMAIL:-}}"
[ -n "$EMAIL" ] || EMAIL="$(envval SEED_ADMIN_EMAIL)"
[ -n "$EMAIL" ] || EMAIL="admin@vedha.io"

# Resolve admin password (prompt as a last resort)
PASSWORD="${ADMIN_PASSWORD:-${SEED_ADMIN_PASSWORD:-}}"
[ -n "$PASSWORD" ] || PASSWORD="$(envval SEED_ADMIN_PASSWORD)"
if [ -z "$PASSWORD" ]; then
  if [ -t 0 ]; then
    printf 'Admin password for %s: ' "$EMAIL" >&2
    stty -echo 2>/dev/null || true; read PASSWORD; stty echo 2>/dev/null || true
    printf '\n' >&2
  else
    echo "No password: set ADMIN_PASSWORD or SEED_ADMIN_PASSWORD (or add it to .env)." >&2
    exit 1
  fi
fi

[ -n "$NAME" ] || NAME="probe-$(hostname 2>/dev/null || echo host)"

tmp="$(mktemp)"
curl_config="$(mktemp)"
chmod 600 "$tmp" "$curl_config"
trap 'rm -f "$tmp" "$curl_config"' EXIT

# 1) Login → JWT (password passed on stdin, not argv)
body="$(EMAIL="$EMAIL" PASSWORD="$PASSWORD" python3 -c 'import json,os;print(json.dumps({"email":os.environ["EMAIL"],"password":os.environ["PASSWORD"]}))')"
code="$(printf '%s' "$body" | curl -sS -o "$tmp" -w '%{http_code}' \
  -X POST "$URL/auth/login" -H 'Content-Type: application/json' -d @- || echo 000)"
if [ "$code" != "200" ]; then
  echo "Login failed (HTTP $code) at $URL — check the email/password and that the manager is up." >&2
  [ "$code" = "000" ] && echo "  (could not reach $URL — is PLATFORM_URL/API_PORT right?)" >&2
  exit 1
fi
JWT="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get("access_token",""))' "$tmp")"
[ -n "$JWT" ] || { echo "Login returned no access_token." >&2; exit 1; }

# 2) Create the PAT — default scopes ARE the 5 probe scopes, so we only send name+expiry
patbody="$(python3 -c 'import json,sys;print(json.dumps({"name":sys.argv[1],"expires_in_days":int(sys.argv[2])}))' "$NAME" "$DAYS")"
{
  printf 'silent\nshow-error\n'
  printf 'header = "Authorization: Bearer %s"\n' "$JWT"
  printf 'header = "Content-Type: application/json"\n'
} > "$curl_config"
code="$(curl --config "$curl_config" -o "$tmp" -w '%{http_code}' \
  -X POST "$URL/auth/personal-access-tokens" -d "$patbody" || echo 000)"
if [ "$code" != "201" ]; then
  echo "PAT creation failed (HTTP $code):" >&2; cat "$tmp" >&2; echo >&2; exit 1
fi
TOKEN="$(python3  -c 'import json,sys;print(json.load(open(sys.argv[1])).get("token",""))' "$tmp")"
SCOPES="$(python3 -c 'import json,sys;print(", ".join(json.load(open(sys.argv[1])).get("scopes",[])))' "$tmp")"
EXP="$(python3    -c 'import json,sys;print(json.load(open(sys.argv[1])).get("expires_at") or "no expiry")' "$tmp")"
[ -n "$TOKEN" ] || { echo "No token in response." >&2; exit 1; }

echo ""
echo "Probe PAT created for $EMAIL @ $URL"
echo "  name:    $NAME"
echo "  scopes:  $SCOPES"
echo "  expires: $EXP"
echo ""
echo "  $TOKEN"
echo ""
echo "Shown once — copy it now and inject it through your secret manager."
