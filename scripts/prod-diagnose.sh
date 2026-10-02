#!/usr/bin/env bash
# prod-diagnose.sh — detect and heal common Vedha production issues.
# Run from the repo root (e.g. cd /opt/vedha && make prod-diagnose).
set -uo pipefail

PROD_OVERLAY="deploy/aws/docker-compose.prod.yml"
CADDYFILE="deploy/aws/Caddyfile"

# ── colours ──────────────────────────────────────────────────────────────────
if [ -t 1 ]; then
  GRN='\033[0;32m'; YLW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
else
  GRN=''; YLW=''; RED=''; NC=''
fi
ok()   { printf "  ${GRN}[OK]${NC}    %s\n" "$*"; }
warn() { printf "  ${YLW}[WARN]${NC}  %s\n" "$*"; }
fail() { printf "  ${RED}[MISS]${NC}  %s\n" "$*"; }
heal() { printf "  ${YLW}[HEAL]${NC}  %s\n" "$*"; }
done_() { printf "  ${GRN}[DONE]${NC}  %s\n" "$*"; }

ISSUES=0

echo ""
echo "=== Vedha Production Diagnostics ==="
echo ""

# ── 1. Container status ───────────────────────────────────────────────────────
echo "--- Container status ---"
for svc in postgres redis api worker frontend caddy; do
  name="vedha-${svc}-1"
  if docker ps --filter "name=${name}" --format "{{.Names}}" 2>/dev/null | grep -qF "${name}"; then
    health=$(docker inspect --format "{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}" "${name}" 2>/dev/null)
    ok "${name}  (${health})"
  else
    fail "${name} not running"
    ISSUES=$((ISSUES + 1))
  fi
done
echo ""

# ── 2. Heal: start Caddy with the prod overlay if it is missing ───────────────
if ! docker ps --filter "name=vedha-caddy-1" --format "{{.Names}}" 2>/dev/null | grep -qF "vedha-caddy-1"; then
  if [ ! -f "${PROD_OVERLAY}" ]; then
    warn "Caddy overlay not found at ${PROD_OVERLAY} — run install.sh first"
  else
    heal "Caddy is missing — starting with prod overlay..."
    docker compose --project-directory . --env-file .env \
      -f manager/docker-compose.yml \
      -f "${PROD_OVERLAY}" up -d caddy
    done_ "Caddy started"
    echo ""
  fi
fi

# ── 3. Caddyfile: remove stale health_path lines ──────────────────────────────
echo "--- Caddyfile check ---"
if [ -f "${CADDYFILE}" ]; then
  if grep -q 'health_path\|health_interval' "${CADDYFILE}" 2>/dev/null; then
    heal "Removing stale health_path / health_interval from ${CADDYFILE}..."
    sed -i '/health_path/d; /health_interval/d' "${CADDYFILE}"
    if docker exec vedha-caddy-1 caddy reload --config /etc/caddy/Caddyfile 2>/dev/null; then
      done_ "Caddy config reloaded"
    else
      warn "Caddy reload failed — try: docker restart vedha-caddy-1"
    fi
  else
    ok "Caddyfile is clean (no health_path)"
  fi
else
  warn "Caddyfile not found at ${CADDYFILE} (overlay not yet generated)"
fi
echo ""

# ── 4. Port 443 reachability ──────────────────────────────────────────────────
echo "--- Connectivity ---"
if command -v curl >/dev/null 2>&1; then
  code=$(curl -sk --max-time 8 https://localhost/ -o /dev/null -w "%{http_code}" 2>/dev/null || true)
  case "${code}" in
    2*|3*) ok "Port 443 reachable (HTTP ${code})" ;;
    000)
      fail "Port 443 not reachable — Caddy may still be starting or DNS not pointed here"
      ISSUES=$((ISSUES + 1))
      ;;
    *)
      warn "Port 443 returned HTTP ${code} — check Caddyfile or upstream health"
      ;;
  esac
else
  warn "curl not installed — cannot probe port 443"
fi
echo ""

# ── 5. Security: frontend should NOT be publicly bound ───────────────────────
echo "--- Security ---"
fe_bind=$(docker port vedha-frontend-1 3000 2>/dev/null | head -1 || true)
if echo "${fe_bind}" | grep -q "0.0.0.0"; then
  warn "Frontend port 3000 is bound to 0.0.0.0 (bypasses TLS — publicly reachable without HTTPS)"
  warn "Fix: restart stack with the prod overlay: docker compose ... -f ${PROD_OVERLAY} up -d"
  ISSUES=$((ISSUES + 1))
elif echo "${fe_bind}" | grep -q "127.0.0.1"; then
  ok "Frontend port 3000 bound to 127.0.0.1 (Caddy-only — correct)"
else
  ok "Frontend port 3000 not externally bound (correct)"
fi
echo ""

# ── 6. Recent migrate errors ──────────────────────────────────────────────────
echo "--- Migration log (last 15 lines) ---"
if docker ps -a --filter "name=vedha-migrate-1" --format "{{.Names}}" 2>/dev/null | grep -qF "vedha-migrate-1"; then
  exit_code=$(docker inspect --format "{{.State.ExitCode}}" vedha-migrate-1 2>/dev/null || echo "?")
  if [ "${exit_code}" != "0" ] && [ "${exit_code}" != "?" ]; then
    warn "migrate container exited with code ${exit_code}:"
    docker logs vedha-migrate-1 --tail 15 2>&1 | sed 's/^/    /'
    ISSUES=$((ISSUES + 1))
  else
    ok "migrate container exited cleanly (code 0)"
  fi
else
  ok "No migrate container present (already cleaned up)"
fi
echo ""

# ── 7. Summary ────────────────────────────────────────────────────────────────
echo "=== Summary ==="
if [ "${ISSUES}" -eq 0 ]; then
  printf "  ${GRN}All checks passed. Stack is healthy.${NC}\n"
else
  printf "  ${RED}${ISSUES} issue(s) found — see [MISS]/[WARN] above.${NC}\n"
  echo ""
  echo "  Useful commands:"
  echo "    docker compose -f manager/docker-compose.yml -f ${PROD_OVERLAY} logs -f caddy"
  echo "    docker logs vedha-migrate-1 --tail 50"
  echo "    docker inspect vedha-api-1 | jq '.[].State.Health'"
fi
echo ""
