#!/usr/bin/env sh
# Vedha doctor — catch the common dev/deploy footguns before `make up`.
#   make doctor
set -u

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
ENV_FILE="$ROOT/.env"
ok=0; warn=0; fail=0
pass() { printf '  \033[32m\xE2\x9C\x93\033[0m %s\n' "$1"; ok=$((ok+1)); }
note() { printf '  \033[33m\xE2\x9A\xA0\033[0m %s\n' "$1"; warn=$((warn+1)); }
bad()  { printf '  \033[31m\xE2\x9C\x97\033[0m %s\n' "$1"; fail=$((fail+1)); }
envval() { [ -f "$ENV_FILE" ] && grep -E "^$1=" "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2- || true; }
port_busy() {
  if   command -v lsof >/dev/null 2>&1; then lsof -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
  elif command -v nc   >/dev/null 2>&1; then nc -z localhost "$1" >/dev/null 2>&1
  else return 2; fi
}

echo "Vedha doctor — preflight checks"
echo ""

# Docker
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then pass "Docker installed and daemon running"
  else bad "Docker installed but the daemon isn't running — start Docker Desktop/Engine"; fi
else
  bad "Docker not found — https://docs.docker.com/engine/install/"
fi

# python3 — used by `make probe-pat` and the runbook curl snippets
if command -v python3 >/dev/null 2>&1; then pass "python3 available"
else note "python3 not found — needed for 'make probe-pat' and runbook JSON parsing"; fi

# .env
if [ -f "$ENV_FILE" ]; then pass ".env present"
else note ".env missing — run: cp .env.docker.example .env  (the make targets also auto-copy it)"; fi

# Ports
for pair in "API_PORT 18080" "FRONTEND_PORT 3000"; do
  key=${pair%% *}; def=${pair##* }
  p="$(envval "$key")"; p="${p:-$def}"
  port_busy "$p"; r=$?
  if   [ "$r" = "0" ]; then note "Port $p ($key) is already in use — change $key in .env or free it"
  elif [ "$r" = "2" ]; then :
  else pass "Port $p ($key) is free"; fi
done

# Insecure defaults — only a real problem for exposed/production stacks
appenv="$(envval APP_ENV)"; appenv="${appenv:-production}"
jwt="$(envval JWT_SECRET)"
pw="$(envval SEED_ADMIN_PASSWORD)"
case "$jwt" in ""|change-me*) jwt_default=1 ;; *) jwt_default=0 ;; esac
if [ "${#jwt}" -lt 32 ] 2>/dev/null; then jwt_short=1; else jwt_short=0; fi
if [ "$appenv" = "production" ]; then
  if [ "$jwt_default" = "1" ] || [ "$jwt_short" = "1" ]; then
    note "APP_ENV=production but JWT_SECRET is default/short — set a 32+ char secret (openssl rand -base64 48)"
  else
    pass "JWT_SECRET is set to a non-default value"
  fi
  case "$pw" in
    ""|ChangeMe123!) note "APP_ENV=production but SEED_ADMIN_PASSWORD is the default — change it before exposing the manager" ;;
    *) pass "SEED_ADMIN_PASSWORD changed from the default" ;;
  esac
else
  pass "APP_ENV=$appenv (dev — default secrets tolerated)"
fi

echo ""
printf 'Result: %d ok, %d warning(s), %d blocker(s)\n' "$ok" "$warn" "$fail"
[ "$fail" = "0" ] || { echo "Fix the blocker(s) above, then re-run: make doctor"; exit 1; }
