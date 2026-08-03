#!/usr/bin/env bash
# =============================================================================
# Vedha — Deployment Verification Framework
#
# Validates every layer of the deployed stack and produces a pass/fail report.
# Designed to run after install.sh or independently for ongoing ops verification.
#
# Usage:
#   bash deploy/aws/verify.sh                         # full verification
#   bash deploy/aws/verify.sh --mode smoke            # fast subset (post-deploy)
#   bash deploy/aws/verify.sh --mode full             # exhaustive (pre-release)
#   bash deploy/aws/verify.sh --api-url https://api.example.com --mode full
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed (see report)
# =============================================================================
set -Eeuo pipefail

# ── Args ──────────────────────────────────────────────────────────────────────
APP_DIR="${APP_DIR:-/opt/vedha}"
API_URL="${API_URL:-http://localhost:18080}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@vedha.io}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-}"
MODE="${MODE:-full}"   # smoke | full

while [[ $# -gt 0 ]]; do
  case "$1" in
    --api-url)       API_URL="$2";       shift 2 ;;
    --admin-email)   ADMIN_EMAIL="$2";   shift 2 ;;
    --admin-password)
      echo "--admin-password is unsafe because process arguments are observable; use --admin-password-file or APP_DIR/.env" >&2
      exit 1 ;;
    --admin-password-file)
      ADMIN_PASSWORD="$(<"$2")"; shift 2 ;;
    --mode)          MODE="$2";          shift 2 ;;
    --full)          MODE="full";        shift ;;
    --app-dir)       APP_DIR="$2";       shift 2 ;;
    *) echo "unknown arg: $1"; exit 1 ;;
  esac
done

case "$MODE" in
  smoke|full) ;;
  *) echo "invalid --mode: $MODE (expected smoke or full)" >&2; exit 1 ;;
esac

# If password not passed, read from .env
if [ -z "$ADMIN_PASSWORD" ] && [ -f "$APP_DIR/.env" ]; then
  ADMIN_PASSWORD=$(grep -m1 '^SEED_ADMIN_PASSWORD=' "$APP_DIR/.env" | cut -d= -f2- || true)
fi

COMPOSE_CMD=(docker compose --env-file "$APP_DIR/.env"
  -f "$APP_DIR/manager/docker-compose.yml"
  -f "$APP_DIR/deploy/aws/docker-compose.prod.yml")

# ── Reporting ─────────────────────────────────────────────────────────────────
PASS=0; FAIL=0; WARN=0; SKIP=0
_ts()  { date '+%H:%M:%S'; }
ok()   { printf '\033[0;32m  ✓ [%s] %s\033[0m\n' "$(_ts)" "$*"; PASS=$(( PASS + 1 )); }
fail() { printf '\033[0;31m  ✗ [%s] %s\033[0m\n' "$(_ts)" "$*" >&2; FAIL=$(( FAIL + 1 )); }
warn() { printf '\033[0;33m  ⚠ [%s] %s\033[0m\n' "$(_ts)" "$*"; WARN=$(( WARN + 1 )); }
skip() { printf '\033[0;34m  ↷ [%s] SKIP: %s\033[0m\n' "$(_ts)" "$*"; SKIP=$(( SKIP + 1 )); }
section() { printf '\n\033[1;37m── %s ──────────────────────────────────\033[0m\n' "$*"; }

# ── Helper: HTTP check ────────────────────────────────────────────────────────
http_check() {
  local label="$1" url="$2" expected_status="${3:-200}"
  local status
  status=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" 2>/dev/null || echo "000")
  if [ "$status" = "$expected_status" ]; then
    ok "$label → HTTP $status"
    return 0
  else
    fail "$label → expected HTTP $expected_status, got $status (url: $url)"
    return 1
  fi
}

# ── 1. Docker Engine ──────────────────────────────────────────────────────────
section "Docker Engine"

if docker info >/dev/null 2>&1; then
  ok "Docker daemon running"
  DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "unknown")
  ok "Docker version: $DOCKER_VERSION"
else
  fail "Docker daemon not running"
fi

if docker compose version >/dev/null 2>&1; then
  ok "Docker Compose plugin available"
else
  fail "Docker Compose plugin not available"
fi

# ── 2. Repository structure ───────────────────────────────────────────────────
section "Repository (sparse clone integrity)"

EXPECTED_DIRS=("manager/backend" "manager/frontend" "manager/detection_engine" "deploy/aws")
for d in "${EXPECTED_DIRS[@]}"; do
  if [ -d "$APP_DIR/$d" ]; then
    ok "dir $d present"
  else
    fail "dir $d missing — sparse checkout may be broken"
  fi
done

# Verify probe source is NOT present (data security check)
if [ -d "$APP_DIR/probe" ]; then
  warn "probe/ directory present on this host — sparse clone may not be active. Run: git sparse-checkout set manager deploy"
else
  ok "probe/ not present on this host (data security ✓)"
fi

# ── 3. Environment configuration ─────────────────────────────────────────────
section "Environment Configuration"

ENV_FILE="$APP_DIR/.env"
if [ -f "$ENV_FILE" ]; then
  ok ".env exists"

  ENV_PERMS=$(stat -c '%a' "$ENV_FILE" 2>/dev/null || stat -f '%A' "$ENV_FILE" 2>/dev/null || echo "unknown")
  if [ "$ENV_PERMS" = "600" ]; then
    ok ".env permissions: 600 ✓"
  else
    fail ".env permissions: $ENV_PERMS (should be 600 — chmod 600 $ENV_FILE)"
  fi

  # Check for dangerous default values
  if grep -q 'JWT_SECRET=change-me' "$ENV_FILE" 2>/dev/null; then
    fail "JWT_SECRET is still the default weak value — regenerate immediately"
  else
    JWT_LEN=$(grep -m1 '^JWT_SECRET=' "$ENV_FILE" | cut -d= -f2- | wc -c | tr -d ' ')
    if [ "${JWT_LEN:-0}" -ge 32 ]; then
      ok "JWT_SECRET set and length ≥32 chars"
    else
      fail "JWT_SECRET too short (${JWT_LEN} chars, need ≥32)"
    fi
  fi

  if grep -q 'POSTGRES_PASSWORD=secret$' "$ENV_FILE" 2>/dev/null; then
    fail "POSTGRES_PASSWORD is still the default 'secret' — regenerate"
  else
    ok "POSTGRES_PASSWORD not default"
  fi

  if grep -q 'SEED_ADMIN_PASSWORD=ChangeMe123!$' "$ENV_FILE" 2>/dev/null; then
    warn "SEED_ADMIN_PASSWORD is still the example value — rotate immediately"
  else
    ok "SEED_ADMIN_PASSWORD not default"
  fi

  if grep -m1 '^AUTH_COOKIE_SECURE=' "$ENV_FILE" | grep -q 'true'; then
    ok "AUTH_COOKIE_SECURE=true"
  else
    fail "AUTH_COOKIE_SECURE is not true — session cookies will not be Secure-flagged"
  fi

  CORS=$(grep -m1 '^CORS_ORIGINS=' "$ENV_FILE" | cut -d= -f2- || true)
  if echo "$CORS" | grep -qE 'localhost|127\.0\.0\.1'; then
    warn "CORS_ORIGINS contains localhost — should be production domain only in prod"
  else
    ok "CORS_ORIGINS: $CORS"
  fi

else
  fail ".env not found at $ENV_FILE"
fi

# ── 4. Containers ─────────────────────────────────────────────────────────────
section "Container Status"

REQUIRED_SERVICES=(postgres redis api worker caddy)
OPTIONAL_SERVICES=(frontend neo4j ollama)

for svc in "${REQUIRED_SERVICES[@]}"; do
  STATUS=$("${COMPOSE_CMD[@]}" ps --status running --format '{{.Service}}' 2>/dev/null | grep -x "$svc" || true)
  if [ -n "$STATUS" ]; then
    ok "container $svc: running"
  else
    # Check if it exited intentionally (migrate is a one-shot)
    EXIT_STATUS=$("${COMPOSE_CMD[@]}" ps --format '{{.Service}} {{.State}}' 2>/dev/null | grep "^$svc " | awk '{print $2}' || true)
    fail "container $svc: not running (state: ${EXIT_STATUS:-unknown})"
  fi
done

# migrate is a one-shot — should be exited with code 0, not running
MIGRATE_STATE=$("${COMPOSE_CMD[@]}" ps --format '{{.Service}} {{.ExitCode}}' 2>/dev/null | grep '^migrate ' | awk '{print $2}' || true)
if [ "${MIGRATE_STATE:-}" = "0" ]; then
  ok "container migrate: completed successfully (exit 0)"
elif [ -z "${MIGRATE_STATE:-}" ]; then
  warn "container migrate: state unknown (may not have run yet)"
else
  fail "container migrate: exited with code ${MIGRATE_STATE} — check logs: docker compose logs migrate"
fi

for svc in "${OPTIONAL_SERVICES[@]}"; do
  STATUS=$("${COMPOSE_CMD[@]}" ps --status running --format '{{.Service}}' 2>/dev/null | grep -x "$svc" || true)
  if [ -n "$STATUS" ]; then
    ok "container $svc: running"
  else
    skip "container $svc: not running (optional profile)"
  fi
done

# Orphan container check
ORPHANS=$("${COMPOSE_CMD[@]}" ps --format '{{.Service}}' 2>/dev/null | sort > /tmp/v_running.txt
  printf '%s\n' postgres redis api worker migrate caddy frontend neo4j ollama ollama-model-init | sort > /tmp/v_expected.txt
  comm -23 /tmp/v_running.txt /tmp/v_expected.txt || true)
if [ -n "$ORPHANS" ]; then
  warn "Potential orphan containers: $ORPHANS"
else
  ok "no orphan containers"
fi

# ── 5. Volumes ────────────────────────────────────────────────────────────────
section "Volumes"

for vol in vedha_pgdata vedha_redisdata; do
  if docker volume inspect "$vol" >/dev/null 2>&1; then
    ok "volume $vol exists"
  else
    warn "volume $vol not found — first-run or data loss?"
  fi
done

# ── 6. Network ────────────────────────────────────────────────────────────────
section "Network"

if docker network inspect vedha_default >/dev/null 2>&1; then
  ok "compose network vedha_default exists"
else
  fail "compose network vedha_default not found"
fi

# API port must be 127.0.0.1-bound, not 0.0.0.0 (Caddy bypass risk)
if docker inspect vedha-api-1 >/dev/null 2>&1; then
  BINDING=$(docker inspect vedha-api-1 --format '{{range .NetworkSettings.Ports}}{{range .}}{{.HostIp}}{{end}}{{end}}' 2>/dev/null || true)
  if echo "$BINDING" | grep -q '^0\.0\.0\.0$'; then
    fail "API port is bound to 0.0.0.0 — clients can bypass Caddy on port 18080. Fix: bind to 127.0.0.1 in manager/docker-compose.yml"
  else
    ok "API port bound to 127.0.0.1 (Caddy bypass blocked)"
  fi
fi

# ── 7. API health endpoint ────────────────────────────────────────────────────
section "API Endpoints"

http_check "API /health" "${API_URL}/health" "200" || true

# API docs (should be disabled in production)
DOCS_STATUS=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "${API_URL}/docs" 2>/dev/null || echo "000")
if [ "$DOCS_STATUS" = "404" ] || [ "$DOCS_STATUS" = "403" ]; then
  ok "API /docs disabled in production (HTTP $DOCS_STATUS)"
elif [ "$DOCS_STATUS" = "200" ]; then
  warn "API /docs accessible — consider disabling in production (APP_ENV=production should suppress this)"
fi

# ── 8. Authentication ─────────────────────────────────────────────────────────
section "Authentication"

if [ -n "$ADMIN_PASSWORD" ]; then
  if ! command -v jq >/dev/null 2>&1; then
    fail "admin login: jq is required to encode credentials safely"
    LOGIN_PAYLOAD=""
  else
    LOGIN_PAYLOAD=$(jq -n \
      --arg email "$ADMIN_EMAIL" \
      --arg password "$ADMIN_PASSWORD" \
      '{email:$email,password:$password}')
  fi
  if [ -z "$LOGIN_PAYLOAD" ]; then
    LOGIN_RESPONSE=$'\n000'
  else
  LOGIN_RESPONSE=$(curl -s -w '\n%{http_code}' --max-time 10 \
    -X POST "${API_URL}/auth/login" \
    -H "Content-Type: application/json" \
    --data-binary @- \
    <<<"$LOGIN_PAYLOAD" \
    2>/dev/null || echo -e "\n000")
  fi
  LOGIN_STATUS=$(echo "$LOGIN_RESPONSE" | tail -1)
  LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | head -1)

  if [ "$LOGIN_STATUS" = "200" ]; then
    ok "admin login: HTTP 200 ✓"
    # Extract token for further tests
    JWT_TOKEN=$(echo "$LOGIN_BODY" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4 || true)
    if [ -n "$JWT_TOKEN" ]; then
      ok "JWT token returned ✓"
    else
      warn "No access_token in login response — check auth response format"
    fi
  elif [ "$LOGIN_STATUS" = "401" ]; then
    fail "admin login failed (HTTP 401) — password may have changed or seed failed"
  elif [ "$LOGIN_STATUS" = "000" ]; then
    fail "admin login: connection refused — API may not be running"
  else
    fail "admin login: unexpected HTTP $LOGIN_STATUS"
  fi
else
  skip "Authentication test (no admin password available)"
fi

# ── 9. Database ────────────────────────────────────────────────────────────────
section "Database (PostgreSQL)"

if "${COMPOSE_CMD[@]}" exec -T postgres pg_isready -U vapt -d vapt_db >/dev/null 2>&1; then
  ok "postgres pg_isready ✓"
else
  fail "postgres not ready"
fi

# Check migration ran successfully
TABLE_COUNT=$("${COMPOSE_CMD[@]}" exec -T postgres \
  psql -U vapt -d vapt_db -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" \
  2>/dev/null | tr -d ' \n' || echo "0")
if [ "${TABLE_COUNT:-0}" -gt "0" ]; then
  ok "postgres: $TABLE_COUNT tables in public schema (migrations ran)"
else
  fail "postgres: no tables in public schema — migration may have failed"
fi

# ── 10. Redis ─────────────────────────────────────────────────────────────────
section "Redis"

if "${COMPOSE_CMD[@]}" exec -T redis redis-cli ping 2>/dev/null | grep -q PONG; then
  ok "redis PING → PONG ✓"
else
  fail "redis PING failed"
fi

# Check persistence mode
REDIS_PERSIST=$("${COMPOSE_CMD[@]}" exec -T redis redis-cli config get appendonly 2>/dev/null | tail -1 || true)
if [ "${REDIS_PERSIST:-}" = "yes" ]; then
  ok "redis persistence: AOF enabled ✓"
else
  warn "redis persistence: AOF not enabled — job queue lost on restart"
fi

# ── 11. TLS / Caddy ───────────────────────────────────────────────────────────
section "Reverse Proxy (Caddy)"

if "${COMPOSE_CMD[@]}" ps --format '{{.Service}}' | grep -q '^caddy$'; then
  ok "caddy container running"

  # Caddy config validation inside the container
  if "${COMPOSE_CMD[@]}" exec -T caddy caddy validate --config /etc/caddy/Caddyfile >/dev/null 2>&1; then
    ok "Caddyfile syntax valid ✓"
  else
    fail "Caddyfile syntax invalid — caddy may have started with old config"
  fi
else
  fail "caddy container not running"
fi

# ── 12. Security headers ──────────────────────────────────────────────────────
section "Security Headers"

if [ -n "${DOMAIN:-}" ] || echo "$API_URL" | grep -q 'https://'; then
  HEADERS=$(curl -s -I --max-time 10 "$API_URL/health" 2>/dev/null || true)
  for HEADER in "Strict-Transport-Security" "X-Content-Type-Options" "X-Frame-Options"; do
    if echo "$HEADERS" | grep -qi "$HEADER"; then
      ok "header $HEADER present ✓"
    else
      warn "header $HEADER missing — add to Caddyfile"
    fi
  done
  # Ensure Server header is stripped
  if echo "$HEADERS" | grep -qi '^Server:'; then
    warn "Server header exposed — add 'header -Server' to Caddyfile"
  else
    ok "Server header stripped ✓"
  fi
else
  skip "Security header checks (not HTTPS — set DOMAIN for production)"
fi

# ── 13. Disk space (post-deploy) ─────────────────────────────────────────────
section "Disk Space"
USED_PCT=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "${USED_PCT:-0}" -gt 85 ]; then
  fail "Disk usage at ${USED_PCT}% — below 15% free. Clean up with: docker system prune -f"
elif [ "${USED_PCT:-0}" -gt 70 ]; then
  warn "Disk usage at ${USED_PCT}% — approaching limit"
else
  ok "Disk usage: ${USED_PCT}% ✓"
fi

# Dangling image check
DANGLING=$(docker images -f dangling=true -q 2>/dev/null | wc -l | tr -d ' ')
if [ "${DANGLING:-0}" -gt 5 ]; then
  warn "$DANGLING dangling images — free space: docker image prune -f"
else
  ok "dangling images: $DANGLING"
fi

# ── 14. Worker (full mode only) ───────────────────────────────────────────────
if [ "$MODE" = "full" ]; then
  section "Worker Queue Health"

  WORKER_STATE=$("${COMPOSE_CMD[@]}" ps --format '{{.Service}} {{.State}}' 2>/dev/null | grep '^worker ' | awk '{print $2}' || true)
  if [ "${WORKER_STATE:-}" = "running" ]; then
    ok "worker: running"
    # Check worker hasn't restarted excessively (>3 restarts = crash loop)
    RESTARTS=$("${COMPOSE_CMD[@]}" ps --format '{{.Service}} {{.Status}}' 2>/dev/null | grep '^worker ' | grep -o 'Restarting ([0-9]*)' | grep -o '[0-9]*' || echo "0")
    if [ "${RESTARTS:-0}" -gt 3 ]; then
      fail "worker has restarted ${RESTARTS} times — crash loop. Check: docker compose logs worker"
    else
      ok "worker restart count: ${RESTARTS:-0}"
    fi
  else
    fail "worker: not running (state: ${WORKER_STATE:-unknown})"
  fi
fi

# ── 15. IMDSv2 (EC2-specific, full mode) ─────────────────────────────────────
if [ "$MODE" = "full" ]; then
  section "EC2 Security"

  # Test that IMDSv2 is enforced (IMDSv1 should return 401)
  IMDSV1_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 2 \
    "http://169.254.169.254/latest/meta-data/" 2>/dev/null || echo "000")
  if [ "$IMDSV1_CODE" = "401" ]; then
    ok "IMDSv2 enforced (IMDSv1 returns 401) ✓"
  elif [ "$IMDSV1_CODE" = "200" ]; then
    fail "IMDSv2 NOT enforced — IMDSv1 responds. Fix: aws ec2 modify-instance-metadata-options --instance-id \$(curl -s http://169.254.169.254/latest/meta-data/instance-id) --http-tokens required"
  elif [ "$IMDSV1_CODE" = "000" ]; then
    skip "IMDSv2 check: not on EC2 or IMDS not reachable"
  fi
fi

# ── Report ─────────────────────────────────────────────────────────────────────
printf '\n\033[1;37m══════════════════════════════════════════\033[0m\n'
printf '  Verification Report  [mode: %s]\n' "$MODE"
printf '\033[1;37m══════════════════════════════════════════\033[0m\n'
printf '  \033[0;32m✓ PASS\033[0m  %d\n' "$PASS"
printf '  \033[0;31m✗ FAIL\033[0m  %d\n' "$FAIL"
printf '  \033[0;33m⚠ WARN\033[0m  %d\n' "$WARN"
printf '  \033[0;34m↷ SKIP\033[0m  %d\n' "$SKIP"
printf '\033[1;37m══════════════════════════════════════════\033[0m\n'

if [ "$FAIL" -gt 0 ]; then
  printf '\n\033[0;31mVerification FAILED (%d failures). Fix the issues above before going live.\033[0m\n\n' "$FAIL"
  exit 1
else
  printf '\n\033[0;32mAll checks passed.\033[0m\n\n'
  exit 0
fi
