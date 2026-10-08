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

# ── 6. Migration version check + heal ────────────────────────────────────────
# Handles three classes of mismatch:
#   A. DB version not in codebase (unmerged branch left a stale version_num)
#      → stamp DB to code head via psql
#   B. DB version < code head but schema already has the columns
#      (sparse-checkout hid migration files; DB was applied from a feature branch)
#      → detected by DuplicateColumnError on upgrade → stamp to code head
#   C. DB version < code head and schema genuinely missing
#      → upgrade runs normally; if it fails for another reason, we warn
echo "--- Migration status ---"
if docker ps --filter "name=vedha-postgres-1" --format "{{.Names}}" 2>/dev/null | grep -qF "vedha-postgres-1"; then
  DB_USER=$(grep -m1 '^POSTGRES_USER=' .env 2>/dev/null | cut -d= -f2- || echo "vapt")
  DB_NAME=$(grep -m1 '^POSTGRES_DB='   .env 2>/dev/null | cut -d= -f2- || echo "vapt_db")

  DB_VER=$(docker exec vedha-postgres-1 \
    psql -U "${DB_USER}" -d "${DB_NAME}" -tAc \
    "SELECT version_num FROM alembic_version LIMIT 1;" 2>/dev/null \
    | tr -d '[:space:]' || echo "")

  CODE_HEAD=$(docker compose --project-directory . --env-file .env \
    -f manager/docker-compose.yml \
    run --rm --no-deps migrate alembic heads 2>/dev/null \
    | grep -Eo '^[0-9a-f]+' | head -1 || echo "")

  if [ -z "${DB_VER}" ]; then
    warn "Could not read alembic_version from DB (table may not exist yet)"
  elif [ -z "${CODE_HEAD}" ]; then
    warn "DB version: ${DB_VER} — could not determine code head (migration files missing?)"
  elif [ "${DB_VER}" = "${CODE_HEAD}" ]; then
    ok "DB migration at code head (${DB_VER})"
  else
    fail "Version mismatch: DB=${DB_VER}  code head=${CODE_HEAD}"

    # Case A: DB version doesn't exist in the codebase at all — just stamp
    if ! docker compose --project-directory . --env-file .env \
        -f manager/docker-compose.yml \
        run --rm --no-deps migrate \
        alembic show "${DB_VER}" >/dev/null 2>&1; then
      heal "DB version '${DB_VER}' not found in codebase — stamping to code head ${CODE_HEAD}..."
      _stamp_result=$(docker exec vedha-postgres-1 \
        psql -U "${DB_USER}" -d "${DB_NAME}" \
        -c "UPDATE alembic_version SET version_num = '${CODE_HEAD}';" 2>&1)
      if echo "${_stamp_result}" | grep -q "UPDATE 1"; then
        done_ "DB stamped to ${CODE_HEAD}"
      else
        warn "psql stamp failed: ${_stamp_result}"
        warn "Manual fix: docker exec vedha-postgres-1 psql -U ${DB_USER} -d ${DB_NAME} -c \"UPDATE alembic_version SET version_num = '${CODE_HEAD}';\""
      fi

    else
      # Case B/C: DB version exists in code but is behind head — try upgrade
      heal "Running alembic upgrade head..."
      UPGRADE_LOG=$(docker compose --project-directory . --env-file .env \
        -f manager/docker-compose.yml \
        run --rm migrate alembic upgrade head 2>&1)
      UPGRADE_EXIT=$?

      if [ "${UPGRADE_EXIT}" -eq 0 ]; then
        done_ "Migrations applied successfully"
      elif echo "${UPGRADE_LOG}" | grep -q "DuplicateColumnError\|already exists\|DuplicateTableError"; then
        # Case B: schema already applied from a feature-branch migration
        heal "Schema already present (DuplicateColumn) — stamping DB to code head ${CODE_HEAD}..."
        _stamp_result=$(docker exec vedha-postgres-1 \
          psql -U "${DB_USER}" -d "${DB_NAME}" \
          -c "UPDATE alembic_version SET version_num = '${CODE_HEAD}';" 2>&1)
        if echo "${_stamp_result}" | grep -q "UPDATE 1"; then
          done_ "DB stamped to ${CODE_HEAD} — schema was already applied by a prior branch"
        else
          warn "psql stamp failed: ${_stamp_result}"
        fi
      else
        # Case C: genuine migration failure
        warn "Migration failed with unexpected error:"
        echo "${UPGRADE_LOG}" | tail -8 | sed 's/^/    /'
        warn "Run manually: docker compose -f manager/docker-compose.yml run --rm migrate alembic upgrade head"
      fi
    fi

    ISSUES=$((ISSUES + 1))
  fi
else
  warn "postgres not running — cannot check migration version"
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
