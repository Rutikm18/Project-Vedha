#!/usr/bin/env bash
# gen-env.sh — auto-generate .env with real random secrets.
#
# Safe to re-run: skips fields that already have a non-empty value so an
# existing .env is never overwritten with new secrets (which would break a
# running Postgres volume).
#
# Usage:
#   bash scripts/gen-env.sh           # writes .env in repo root
#   ENV_FILE=/opt/vedha/.env bash scripts/gen-env.sh

set -euo pipefail

ENV_FILE="${ENV_FILE:-$(dirname "$(cd "$(dirname "$0")" && pwd)")/.env}"
EXAMPLE="$(dirname "$(cd "$(dirname "$0")" && pwd)")/.env.docker.example"

gen() { openssl rand -base64 48 | tr -d '\n/+='; }
gen32() { openssl rand -base64 32 | tr -d '\n'; }
gen_pw() { printf '%s%s' "$(openssl rand -base64 18 | tr -d '\n/+=')" "Aa1!"; }

# Bootstrap from example if .env does not exist yet
if [ ! -f "$ENV_FILE" ]; then
  if [ -f "$EXAMPLE" ]; then
    cp "$EXAMPLE" "$ENV_FILE"
    echo "[gen-env] created $ENV_FILE from example"
  else
    touch "$ENV_FILE"
    echo "[gen-env] created empty $ENV_FILE (example not found)"
  fi
fi

# Helper: set KEY=VALUE only when the key is missing or still has a placeholder
set_if_missing() {
  local key="$1" value="$2"
  local current
  current="$(grep -m1 "^${key}=" "$ENV_FILE" 2>/dev/null | cut -d= -f2- || true)"
  # Treat empty, "secret", "change-me*", "ChangeMe*" as placeholders
  if [ -z "$current" ] || echo "$current" | grep -qiE '^(secret|change.me|changeme)'; then
    if grep -q "^${key}=" "$ENV_FILE" 2>/dev/null; then
      # Replace existing placeholder line
      sed -i "s|^${key}=.*|${key}=${value}|" "$ENV_FILE"
    else
      # Append new key
      echo "${key}=${value}" >> "$ENV_FILE"
    fi
    echo "[gen-env] generated $key"
  else
    echo "[gen-env] keeping existing $key"
  fi
}

set_if_missing JWT_SECRET              "$(gen)"
set_if_missing POSTGRES_PASSWORD       "$(gen)"
set_if_missing SEED_ADMIN_PASSWORD     "$(gen_pw)"
set_if_missing PROBE_POLICY_SIGNING_KEY "$(gen32)"

echo ""
echo "[gen-env] .env is ready → $ENV_FILE"
echo "[gen-env] Admin login: $(grep -m1 '^SEED_ADMIN_EMAIL=' "$ENV_FILE" | cut -d= -f2-)"
echo "[gen-env] Admin password stored in .env (SEED_ADMIN_PASSWORD)"
