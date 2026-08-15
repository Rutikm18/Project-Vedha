#!/usr/bin/env bash
# gen-env.sh — auto-generate .env for the no-TLS AWS testing path (make aws-up).
#
# Design goals:
#   1. Idempotent secrets — never rotate an existing secret. Rotating
#      POSTGRES_PASSWORD against a live pgdata volume = permanent auth failure,
#      which is the classic "API dies after first call" trap.
#   2. Fail-safe config — guarantee APP_ENV / AUTH_COOKIE_SECURE are a consistent
#      pair so the API startup diagnostic never aborts the uvicorn workers
#      (production + insecure-cookie is a FATAL startup check).
#   3. Zero friction — auto-detect the EC2 public IP via IMDSv2 (works even when
#      IMDSv1 is disabled) for MANAGER_PUBLIC_URL + CORS_ORIGINS.
#   4. Injection-safe writes — no `sed` interpolation of secret values.
#
# Production deploys do NOT use this script — they go through
# deploy/aws/install.sh (TLS via Caddy, SSM secrets, APP_ENV=production).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$ROOT/.env}"
EXAMPLE="$ROOT/.env.docker.example"

command -v openssl >/dev/null 2>&1 || { echo "[gen-env] FATAL: openssl is required" >&2; exit 1; }

gen()    { openssl rand -base64 48 | tr -d '\n/+='; }   # ~64 url-safe chars
gen32()  { openssl rand -base64 32 | tr -d '\n/+='; }
gen_pw() { printf '%s%s' "$(openssl rand -base64 18 | tr -d '\n/+=')" "Aa1!"; }
# The Site-policy signing key MUST stay VALID standard base64 of exactly 32 bytes
# (app _policy() does base64.b64decode(validate=True) → Ed25519 seed). Stripping
# /+=/padding like gen32 does would corrupt it → 503 on every enrollment activate.
gen_b64_32() { openssl rand -base64 32 | tr -d '\n'; }
# True iff $1 is valid base64 decoding to exactly 32 bytes.
valid_b64_32() {
  n=$(printf '%s' "$1" | openssl base64 -d -A 2>/dev/null | wc -c | tr -d ' ')
  [ "$n" = "32" ]
}

# ── Bootstrap .env from the example on first run ──────────────────────────────
env_existed=1
[ -f "$ENV_FILE" ] || env_existed=0
if [ "$env_existed" -eq 0 ]; then
  if [ -f "$EXAMPLE" ]; then
    cp "$EXAMPLE" "$ENV_FILE"
    echo "[gen-env] created $ENV_FILE from example"
  else
    : > "$ENV_FILE"
    echo "[gen-env] created empty $ENV_FILE (example not found)"
  fi
fi
chmod 600 "$ENV_FILE" 2>/dev/null || true

# ── Read/write helpers (no sed → no metacharacter injection from values) ──────
get() { grep -m1 "^$1=" "$ENV_FILE" 2>/dev/null | cut -d= -f2- || true; }

# Set KEY=VALUE, replacing in place (preserves line order); appends if absent.
set_kv() {
  local key="$1" val="$2" tmp found=0
  [ "$(get "$key")" = "$val" ] && return 0
  tmp="$(mktemp)"
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      "${key}="*) printf '%s=%s\n' "$key" "$val" >> "$tmp"; found=1 ;;
      *)          printf '%s\n' "$line" >> "$tmp" ;;
    esac
  done < "$ENV_FILE"
  [ "$found" -eq 1 ] || printf '%s=%s\n' "$key" "$val" >> "$tmp"
  cat "$tmp" > "$ENV_FILE"
  rm -f "$tmp"
}

# Generate a secret ONLY when missing or still a placeholder — never rotate.
set_secret() {
  local key="$1" val="$2" cur
  cur="$(get "$key")"
  if [ -z "$cur" ] || printf '%s' "$cur" | grep -qiE '^(secret|change.?me|changeme|your-secret)'; then
    set_kv "$key" "$val"
    echo "[gen-env] generated $key"
  else
    echo "[gen-env] keeping existing $key"
  fi
}

# ── Secrets ───────────────────────────────────────────────────────────────────
set_secret JWT_SECRET               "$(gen)"
set_secret POSTGRES_PASSWORD        "$(gen)"
set_secret SEED_ADMIN_PASSWORD      "$(gen_pw)"
# Regenerate the policy key if absent OR if a legacy/invalid value is present
# (older gen-env stripped /+= → not valid base64 → 503 on enrollment activate).
if ! valid_b64_32 "$(get PROBE_POLICY_SIGNING_KEY)"; then
  set_kv PROBE_POLICY_SIGNING_KEY "$(gen_b64_32)"
  echo "[gen-env] PROBE_POLICY_SIGNING_KEY (re)generated as valid base64-32"
fi

# ── AI pipeline: default to Claude Sonnet ─────────────────────────────────────
# The manager's LLM pipeline (security briefs / advisor / AI reports) runs on
# Anthropic Claude Sonnet by default. LLM_PROVIDER/LLM_MODEL are set ONLY WHEN
# ABSENT, so an operator who chose Ollama (local dev) or OpenAI keeps their pick.
# Pinning the provider matters: auto-detect prefers OpenAI over Anthropic, so
# without this a deployment with both keys would not use Sonnet.
# The API key is a real secret YOU provide — gen-env never generates or guesses it.
[ -z "$(get LLM_PROVIDER)" ] && { set_kv LLM_PROVIDER anthropic; echo "[gen-env] LLM_PROVIDER=anthropic (Claude Sonnet pipeline)"; }
[ -z "$(get LLM_MODEL)" ]    && set_kv LLM_MODEL claude-sonnet-4-6
if [ -z "$(get ANTHROPIC_API_KEY)" ]; then
  echo "[gen-env] NOTE: add ANTHROPIC_API_KEY=<your key> to .env to enable the Claude Sonnet AI pipeline (the AI panel reports 'not configured' until you do)."
fi
# Insurance: the graph-profile neo4j service uses ${NEO4J_PASSWORD:?...}, which
# Compose interpolates even when the profile is inactive. Guarantee a value so a
# blanked var can't break `make aws-up`.
[ -n "$(get NEO4J_PASSWORD)" ] || set_kv NEO4J_PASSWORD "$(gen32)"

# ── Idempotency guard: fresh .env + existing DB volume = auth mismatch ────────
if [ "$env_existed" -eq 0 ] \
   && command -v docker >/dev/null 2>&1 \
   && docker volume ls -q 2>/dev/null | grep -qx vedha_pgdata; then
  echo "[gen-env] ================================ WARNING ================================" >&2
  echo "[gen-env] vedha_pgdata volume exists but .env was just regenerated with a NEW" >&2
  echo "[gen-env] POSTGRES_PASSWORD. Postgres will reject the new password → migrate fails." >&2
  echo "[gen-env] Fix: restore your previous .env, OR wipe the DB (DATA LOSS):" >&2
  echo "[gen-env]   docker volume rm vedha_pgdata" >&2
  echo "[gen-env] =========================================================================" >&2
fi

# ── Consistent config pair (prevents the FATAL production+insecure-cookie combo)
# Respect a deliberate, valid production setup; otherwise force the testing pair.
if [ "$(get APP_ENV)" = "production" ] && [ "$(get AUTH_COOKIE_SECURE)" = "true" ]; then
  set_kv DEV_LOGIN_HINT 0
  echo "[gen-env] keeping production config (AUTH_COOKIE_SECURE=true); login autofill OFF"
else
  set_kv APP_ENV development
  set_kv AUTH_COOKIE_SECURE false
  # Testing convenience: autofill the login form with the seeded admin creds.
  set_kv DEV_LOGIN_HINT 1
  echo "[gen-env] APP_ENV=development, AUTH_COOKIE_SECURE=false, login autofill ON (testing path)"
fi

# Trust-on-first-use probe enrollment: in the single-owner testing deploy, a probe
# that runs `install.sh <manager-ip>` auto-connects (device key → Manager-issued
# token) with no PAT and no approval. Off in production unless deliberately set.
if [ "$(get APP_ENV)" != "production" ]; then
  [ -n "$(get PROBE_AUTO_ENROLL)" ] || set_kv PROBE_AUTO_ENROLL true
  echo "[gen-env] PROBE_AUTO_ENROLL=$(get PROBE_AUTO_ENROLL) (probes auto-connect with just the manager IP)"
fi

# ── Public IP detection via IMDSv2 (falls back to IMDSv1-style, then external) ─
detect_public_ip() {
  local token ip=""
  token="$(curl -fsS -m 3 -X PUT 'http://169.254.169.254/latest/api/token' \
    -H 'X-aws-ec2-metadata-token-ttl-seconds: 120' 2>/dev/null || true)"
  if [ -n "$token" ]; then
    ip="$(curl -fsS -m 3 -H "X-aws-ec2-metadata-token: $token" \
      'http://169.254.169.254/latest/meta-data/public-ipv4' 2>/dev/null || true)"
  fi
  [ -n "$ip" ] || ip="$(curl -fsS -m 3 https://checkip.amazonaws.com 2>/dev/null | tr -d '\n' || true)"
  # Validate it looks like an IPv4 before trusting it.
  printf '%s' "$ip" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$' && printf '%s' "$ip" || printf ''
}

PUBIP="$(detect_public_ip)"
if [ -n "$PUBIP" ]; then
  APORT="$(get API_PORT)";      APORT="${APORT:-18080}"
  FPORT="$(get FRONTEND_PORT)"; FPORT="${FPORT:-3000}"
  EPORT="$(get EDGE_HTTP_PORT)"; EPORT="${EPORT:-80}"
  # The edge ingress (Caddy on port 80) is the canonical external endpoint for the
  # API / probe plane — probes dial it and /health is reachable through the one
  # SG rule most hosts already have open. Advertise that as MANAGER_PUBLIC_URL.
  if [ "$EPORT" = "80" ]; then EDGE_URL="http://${PUBIP}"; else EDGE_URL="http://${PUBIP}:${EPORT}"; fi
  set_kv MANAGER_PUBLIC_URL "$EDGE_URL"
  # Allow the dashboard origins (frontend port) AND the edge origin for browser calls.
  set_kv CORS_ORIGINS "http://${PUBIP}:${FPORT},${EDGE_URL},http://localhost:${FPORT}"
  echo "[gen-env] public IP ${PUBIP} → MANAGER_PUBLIC_URL=${EDGE_URL} (edge :${EPORT}) + CORS_ORIGINS set"
else
  echo "[gen-env] public IP not detected — leaving MANAGER_PUBLIC_URL/CORS_ORIGINS as-is"
fi

chmod 600 "$ENV_FILE" 2>/dev/null || true

echo ""
echo "[gen-env] .env ready → $ENV_FILE"
echo "[gen-env] Admin login : $(get SEED_ADMIN_EMAIL)"
echo "[gen-env] Admin password is in .env (grep SEED_ADMIN_PASSWORD .env)"
