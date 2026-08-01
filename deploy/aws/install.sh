#!/usr/bin/env bash
# ============================================================================
# Vedha — single-file AWS installer.
#
# ONE script. It generates .env, Caddyfile and the compose override itself, so
# there is nothing else to copy. Idempotent: safe to re-run (it never rotates
# the Postgres password once the data volume exists, and reconciles the stack).
#
# Two ways to run — pick one:
#
#   A) In-repo (recommended, zero copy):
#        git clone <repo> /opt/vedha && cd /opt/vedha
#        sudo DOMAIN=vedha.example.com OPENAI_API_KEY=sk-... bash deploy/aws/install.sh
#
#   B) EC2 user-data (fully unattended, nothing to copy — paste as user-data):
#        #!/usr/bin/env bash
#        export REPO_URL=https://github.com/<org>/vedha.git
#        export DOMAIN=vedha.example.com
#        export OPENAI_API_KEY=sk-...
#        curl -fsSL "$REPO_URL/raw/main/deploy/aws/install.sh" | bash   # or embed the file
#
# Config (all optional except where noted) — pass as environment variables:
#   DOMAIN            e.g. vedha.example.com  -> UI at app.$DOMAIN, API at api.$DOMAIN
#                     (omit to fall back to the instance public IP + self-signed TLS)
#   REPO_URL          git URL to clone when not already inside a checkout
#   APP_DIR           install location (default /opt/vedha)
#   ADMIN_EMAIL       seeded admin email (default admin@vedha.io)
#   ACME_EMAIL        Let's Encrypt contact (default = ADMIN_EMAIL)
#   LLM_PROVIDER      openai|anthropic|openrouter|ollama (auto-detected from keys)
#   OPENAI_API_KEY / ANTHROPIC_API_KEY / OPENROUTER_API_KEY
#   ENABLE_GRAPH=1    also start Neo4j attack-path graph
#   API_WORKERS       override auto-sizing
# ============================================================================
set -Eeuo pipefail

APP_DIR="${APP_DIR:-/opt/vedha}"
DOMAIN="${DOMAIN:-}"
REPO_URL="${REPO_URL:-}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@vedha.io}"
ACME_EMAIL="${ACME_EMAIL:-$ADMIN_EMAIL}"
ENABLE_GRAPH="${ENABLE_GRAPH:-0}"
COMPOSE_PROFILES_ARGS=(--profile ui)
[ "$ENABLE_GRAPH" = "1" ] && COMPOSE_PROFILES_ARGS+=(--profile graph)

log()  { printf '\033[1;36m[vedha]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[vedha] WARN:\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m[vedha] FATAL:\033[0m %s\n' "$*" >&2; exit 1; }
trap 'die "failed at line $LINENO. See output above."' ERR

# ── 0. Preconditions ────────────────────────────────────────────────────────
[ "$(id -u)" -eq 0 ] || exec sudo -E bash "$0" "$@"   # re-exec as root, keep env
command -v openssl >/dev/null || die "openssl is required"

ARCH="$(uname -m)"; case "$ARCH" in
  x86_64)  COMPOSE_ARCH=x86_64 ;;
  aarch64|arm64) COMPOSE_ARCH=aarch64 ;;
  *) die "unsupported architecture: $ARCH" ;;
esac

# ── 1. Package manager + base packages ──────────────────────────────────────
if   command -v dnf >/dev/null; then PKG="dnf -y"
elif command -v yum >/dev/null; then PKG="yum -y"
elif command -v apt-get >/dev/null; then PKG="apt-get -y"; export DEBIAN_FRONTEND=noninteractive; apt-get update -y
else die "no supported package manager (dnf/yum/apt-get)"; fi
$PKG install git curl ca-certificates >/dev/null 2>&1 || $PKG install git curl >/dev/null

# ── 2. Docker + Compose plugin ──────────────────────────────────────────────
if ! command -v docker >/dev/null; then
  log "installing Docker..."
  if command -v apt-get >/dev/null; then
    $PKG install docker.io >/dev/null
  else
    $PKG install docker >/dev/null
  fi
fi
systemctl enable --now docker >/dev/null 2>&1 || service docker start || true
docker info >/dev/null 2>&1 || die "Docker daemon is not running"

if ! docker compose version >/dev/null 2>&1; then
  log "installing Docker Compose plugin..."
  CLI_DIR=/usr/local/lib/docker/cli-plugins; mkdir -p "$CLI_DIR"
  curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${COMPOSE_ARCH}" \
    -o "$CLI_DIR/docker-compose"
  chmod +x "$CLI_DIR/docker-compose"
fi
docker compose version >/dev/null 2>&1 || die "docker compose still unavailable"

# ── 3. Locate or fetch the repo ─────────────────────────────────────────────
find_repo_root() { local d="$PWD"; while [ "$d" != / ]; do
  [ -f "$d/docker-compose.yml" ] && [ -f "$d/.env.docker.example" ] && { echo "$d"; return 0; }
  d="$(dirname "$d")"; done; return 1; }

if SRC="$(find_repo_root)"; then
  log "using existing checkout at $SRC"
  [ "$SRC" != "$APP_DIR" ] && APP_DIR="$SRC"
elif [ -d "$APP_DIR/.git" ]; then
  log "updating existing install at $APP_DIR"; git -C "$APP_DIR" pull --ff-only || warn "git pull skipped"
elif [ -n "$REPO_URL" ]; then
  log "cloning $REPO_URL -> $APP_DIR"; git clone --depth 1 "$REPO_URL" "$APP_DIR"
else
  die "not inside a Vedha checkout and REPO_URL is unset. Clone the repo first or set REPO_URL."
fi
cd "$APP_DIR"
[ -f docker-compose.yml ] || die "docker-compose.yml not found in $APP_DIR"

# ── 4. Resource sizing ──────────────────────────────────────────────────────
MEM_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024 ))
CPUS=$(nproc)
[ "$MEM_GB" -lt 3 ] && warn "only ${MEM_GB}GB RAM — Vedha wants >=4GB; consider t3.large."
if [ -z "${API_WORKERS:-}" ]; then
  API_WORKERS=$(( CPUS < 2 ? 1 : (CPUS > 4 ? 4 : CPUS) ))   # cap at 4, min 1
fi

# ── 5. Secrets — generate once, PRESERVE across re-runs ─────────────────────
# The Postgres password is special: once the pgdata volume is initialized, the
# stored password is fixed. If we ever change it the API can't authenticate to
# its own DB. Rule: if the volume already exists, KEEP whatever .env has (even a
# weak default — it must match the volume). Only when there is no volume yet is
# it safe to mint a fresh strong one.
gen_secret() { openssl rand -base64 48 | tr -d '\n/+='; }
env_get() { [ -f .env ] && sed -n "s/^$1=//p" .env | tail -1 || true; }
volume_exists() { docker volume ls -q 2>/dev/null | grep -qx "$1"; }

JWT_SECRET="$(env_get JWT_SECRET)"; [ -n "$JWT_SECRET" ] || JWT_SECRET="$(gen_secret)"
SEED_ADMIN_PASSWORD="$(env_get SEED_ADMIN_PASSWORD)"; [ -n "$SEED_ADMIN_PASSWORD" ] || SEED_ADMIN_PASSWORD="$(openssl rand -base64 18 | tr -d '\n/+=')Aa1!"

PG_CUR="$(env_get POSTGRES_PASSWORD)"
if volume_exists vedha_pgdata; then
  [ -n "$PG_CUR" ] || die "pgdata volume exists but POSTGRES_PASSWORD is missing from .env — cannot recover the DB password. Restore .env or remove the volume to reinitialize."
  POSTGRES_PASSWORD="$PG_CUR"; log "preserving existing Postgres password (data volume present)."
elif [ -n "$PG_CUR" ] && [ "$PG_CUR" != "secret" ]; then
  POSTGRES_PASSWORD="$PG_CUR"                    # already strong, no volume yet
else
  POSTGRES_PASSWORD="$(gen_secret)"              # fresh install → strong password
fi

# ── 6. LLM provider resolution ──────────────────────────────────────────────
if [ -z "${LLM_PROVIDER:-}" ]; then
  if   [ -n "${OPENAI_API_KEY:-}" ];     then LLM_PROVIDER=openai
  elif [ -n "${ANTHROPIC_API_KEY:-}" ];  then LLM_PROVIDER=anthropic
  elif [ -n "${OPENROUTER_API_KEY:-}" ]; then LLM_PROVIDER=openrouter
  else LLM_PROVIDER=ollama; warn "no LLM key provided — AI features will be inert until you set one."; fi
fi

# ── 7. TLS mode: real domain (Let's Encrypt) vs public IP (self-signed) ─────
imds() { local t; t=$(curl -s -m 2 -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 60" 2>/dev/null || true)
  curl -s -m 2 -H "X-aws-ec2-metadata-token: $t" "http://169.254.169.254/latest/meta-data/$1" 2>/dev/null || true; }

if [ -n "$DOMAIN" ]; then
  UI_HOST="app.$DOMAIN"; API_HOST="api.$DOMAIN"; COOKIE_SECURE=true
  UI_URL="https://$UI_HOST"; API_URL="https://$API_HOST"
  cat > Caddyfile <<EOF
{
    email $ACME_EMAIL
}
$UI_HOST {
    reverse_proxy frontend:3000
}
$API_HOST {
    reverse_proxy api:8000
}
EOF
else
  PUBIP="$(imds public-ipv4)"; [ -n "$PUBIP" ] || PUBIP="$(curl -fsSL https://checkip.amazonaws.com 2>/dev/null | tr -d '\n')"
  [ -n "$PUBIP" ] || die "DOMAIN not set and could not detect a public IP."
  warn "no DOMAIN set — serving self-signed TLS on $PUBIP (UI :443, API :8443). Browsers/probes will warn on the cert. Set DOMAIN for real HTTPS."
  UI_HOST="$PUBIP"; API_HOST="$PUBIP:8443"; COOKIE_SECURE=true
  UI_URL="https://$PUBIP"; API_URL="https://$PUBIP:8443"
  cat > Caddyfile <<EOF
https://$PUBIP {
    tls internal
    reverse_proxy frontend:3000
}
https://$PUBIP:8443 {
    tls internal
    reverse_proxy api:8000
}
EOF
fi

# ── 8. Render .env (idempotent) ─────────────────────────────────────────────
[ -f .env ] || cp .env.docker.example .env
# Strip any previous "AWS installer" block, then re-append a fresh one.
sed -i '/# >>> vedha-aws-installer >>>/,/# <<< vedha-aws-installer <<</d' .env
cat >> .env <<EOF
# >>> vedha-aws-installer >>>  (managed block — edit values in SSM/here, then re-run)
APP_ENV=production
LOG_LEVEL=INFO
API_WORKERS=$API_WORKERS
AUTH_COOKIE_SECURE=$COOKIE_SECURE
JWT_SECRET=$JWT_SECRET
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
SEED_ADMIN_EMAIL=$ADMIN_EMAIL
SEED_ADMIN_PASSWORD=$SEED_ADMIN_PASSWORD
LLM_PROVIDER=$LLM_PROVIDER
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-}
CORS_ORIGINS=$UI_URL
NEO4J_ENABLED=$([ "$ENABLE_GRAPH" = "1" ] && echo true || echo false)
# <<< vedha-aws-installer <<<
EOF
chmod 600 .env

# ── 9. Compose override: add Caddy in front ─────────────────────────────────
cat > docker-compose.prod.yml <<'EOF'
services:
  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "8443:8443"   # only used in IP/self-signed mode; harmless otherwise
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - frontend
      - api
volumes:
  caddy_data:
  caddy_config:
EOF

# ── 10. Launch ──────────────────────────────────────────────────────────────
log "building & starting stack (workers=$API_WORKERS, provider=$LLM_PROVIDER)..."
docker compose -f docker-compose.yml -f docker-compose.prod.yml \
  "${COMPOSE_PROFILES_ARGS[@]}" up -d --build

# ── 11. Wait for health ─────────────────────────────────────────────────────
log "waiting for API health (up to 180s)..."
ok=0
for _ in $(seq 1 60); do
  if docker compose exec -T api curl -fsS http://localhost:8000/health >/dev/null 2>&1; then ok=1; break; fi
  sleep 3
done
if [ "$ok" != 1 ]; then
  warn "API did not report healthy in time. Recent logs:"
  docker compose logs --tail=40 migrate api || true
  die "startup incomplete — investigate with: docker compose logs -f api"
fi

# ── 12. Summary ─────────────────────────────────────────────────────────────
printf '\n\033[1;32m[vedha] Deployment complete.\033[0m\n'
cat <<EOF

  Dashboard (UI) : $UI_URL
  API (probes)   : $API_URL
  Admin login    : $ADMIN_EMAIL
  Admin password : $SEED_ADMIN_PASSWORD   (rotate after first login)

Next:
  • Open $UI_HOST in Route53/DNS and the security group (allow 80,443$([ -z "$DOMAIN" ] && echo ",8443") inbound; 22 from your IP only).
  • Point a probe at it:   PLATFORM_URL=$API_URL docker compose --profile probe up -d probe
  • Redeploy after code changes:  cd $APP_DIR && git pull && sudo bash deploy/aws/install.sh
  • Secrets live in $APP_DIR/.env (chmod 600). This script never rotates them on re-run.
EOF
