#!/usr/bin/env bash
# =============================================================================
# Vedha — Production AWS Installer  (v2)
#
# Security model:
#   - Sparse+partial clone: only manager/ and deploy/ land on this host.
#     The probe source, probe Dockerfile, and any other top-level dirs are
#     NEVER downloaded to the EC2 box — even if someone compromises the host,
#     they cannot read probe/detection-engine source from disk.
#   - .env written atomically (tmp → mv) — never world-readable even for a ms.
#   - API and frontend ports bound to 127.0.0.1 — Caddy bypass impossible from
#     the internet even if the SG is misconfigured.
#   - Deployment lock prevents concurrent installs (concurrent `git pull + up`
#     can produce mixed-version containers).
#
# Usage:
#   A) From inside an existing checkout (no clone needed):
#        sudo bash deploy/aws/install.sh
#
#   B) From EC2 user-data / bootstrap (sparse clones only manager/ + deploy/):
#        #!/usr/bin/env bash
#        export REPO_URL=https://github.com/<org>/vedha.git
#        export DOMAIN=vedha.example.com
#        export OPENAI_API_KEY=$(aws ssm get-parameter --name /vedha/OPENAI_API_KEY \
#          --with-decryption --query Parameter.Value --output text)
#        curl -fsSL "https://raw.githubusercontent.com/<org>/vedha/main/deploy/aws/install.sh" | bash
#
# Environment variables (all optional except where noted):
#   DOMAIN             e.g. vedha.example.com  → UI at app.$DOMAIN, API at api.$DOMAIN
#   REPO_URL           git URL (required if not already in a checkout)
#   APP_DIR            install location (default /opt/vedha)
#   ADMIN_EMAIL        seeded admin email (default admin@vedha.io)
#   ACME_EMAIL         Let's Encrypt contact (default = ADMIN_EMAIL)
#   LLM_PROVIDER       openai|anthropic|openrouter|ollama  (auto-detected from keys)
#   OPENAI_API_KEY / ANTHROPIC_API_KEY / OPENROUTER_API_KEY
#   ENABLE_GRAPH=1     also start Neo4j attack-path graph
#   API_WORKERS        override auto-sizing
#   SKIP_VERIFY=1      skip post-deploy smoke tests (not recommended)
#   SSM_PREFIX         SSM path prefix for secrets (default /vedha)
#   SSM_REQUIRED=1     require core secrets to resolve from SSM
#   RELEASE_REF        immutable Git tag/commit to deploy (required by default)
#   RELEASE_SHA        optional expected full/prefix commit SHA
#   REQUIRE_SIGNED_RELEASE=1  verify the tag/commit with the host Git trust store
#   ALLOW_UNPINNED_RELEASE=1  lab-only escape hatch
# =============================================================================
set -Eeuo pipefail

# ── Constants ─────────────────────────────────────────────────────────────────
readonly LOCK_FILE="/var/lock/vedha-install.lock"
readonly MIN_DISK_GB=10
readonly MIN_RAM_GB=3
readonly DEPLOY_TIMEOUT=300   # seconds to wait for healthy stack

APP_DIR="${APP_DIR:-/opt/vedha}"
DOMAIN="${DOMAIN:-}"
REPO_URL="${REPO_URL:-}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@vedha.io}"
ACME_EMAIL="${ACME_EMAIL:-$ADMIN_EMAIL}"
ENABLE_GRAPH="${ENABLE_GRAPH:-0}"
SKIP_VERIFY="${SKIP_VERIFY:-0}"
SSM_PREFIX="${SSM_PREFIX:-/vedha}"
SSM_REQUIRED="${SSM_REQUIRED:-0}"
RELEASE_REF="${RELEASE_REF:-}"
RELEASE_SHA="${RELEASE_SHA:-}"
REQUIRE_SIGNED_RELEASE="${REQUIRE_SIGNED_RELEASE:-1}"
ALLOW_UNPINNED_RELEASE="${ALLOW_UNPINNED_RELEASE:-0}"
ALLOW_SKIP_VERIFY="${ALLOW_SKIP_VERIFY:-0}"

# ── Logging ───────────────────────────────────────────────────────────────────
DEPLOY_LOG="${APP_DIR}/deploy.log"
_ts()  { date '+%Y-%m-%dT%H:%M:%S%z'; }
log()  { printf '\033[1;36m[vedha %s]\033[0m %s\n' "$(_ts)" "$*" | tee -a "${DEPLOY_LOG:-/dev/null}"; }
warn() { printf '\033[1;33m[vedha %s] WARN:\033[0m %s\n' "$(_ts)" "$*" >&2 | tee -a "${DEPLOY_LOG:-/dev/null}"; }
die()  { printf '\033[1;31m[vedha %s] FATAL:\033[0m %s\n' "$(_ts)" "$*" >&2; exit 1; }
step() { printf '\n\033[1;35m━━━ %s ━━━\033[0m\n' "$*"; }

trap 'die "Install failed at line $LINENO. Check ${DEPLOY_LOG:-/dev/null} for details."' ERR

# ── 0. Root + lock ────────────────────────────────────────────────────────────
[ "$(id -u)" -eq 0 ] || exec sudo -E bash "$0" "$@"

# Deployment lock — prevents concurrent installs (git pull + docker up race).
# Uses file descriptor locking so the lock is released automatically on exit.
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
  die "Another install is already running (lock: $LOCK_FILE). Wait for it to finish."
fi

mkdir -p "$APP_DIR"
touch "$DEPLOY_LOG"
chmod 600 "$DEPLOY_LOG"

log "=== Vedha install started (pid $$) ==="

# ── 1. Architecture check ─────────────────────────────────────────────────────
step "Checking host architecture"
ARCH="$(uname -m)"; case "$ARCH" in
  x86_64)  COMPOSE_ARCH=x86_64 ;;
  aarch64|arm64) COMPOSE_ARCH=aarch64 ;;
  *) die "unsupported architecture: $ARCH" ;;
esac
log "architecture: $ARCH"

# ── 2. Pre-flight checks ──────────────────────────────────────────────────────
step "Pre-flight system checks"

# Disk space
AVAIL_GB=$(( $(df --output=avail / | tail -1) / 1024 / 1024 ))
if [ "$AVAIL_GB" -lt "$MIN_DISK_GB" ]; then
  die "insufficient disk space: ${AVAIL_GB}GB available, ${MIN_DISK_GB}GB required. Docker build will fail."
fi
log "disk: ${AVAIL_GB}GB available ✓"

# RAM
MEM_GB=$(( $(grep MemTotal /proc/meminfo | awk '{print $2}') / 1024 / 1024 ))
if [ "$MEM_GB" -lt "$MIN_RAM_GB" ]; then
  warn "only ${MEM_GB}GB RAM — Vedha needs ≥4GB; performance may be degraded."
fi
log "RAM: ${MEM_GB}GB ✓"

# Port conflicts — Caddy needs 80+443 free. A rerun may find Vedha's own
# Compose-managed Caddy listening; that is safe because Compose recreates it.
port_owned_by_vedha_caddy() {
  command -v docker >/dev/null 2>&1 || return 1
  docker ps \
    --filter "publish=$1" \
    --filter "label=com.docker.compose.project=vedha" \
    --filter "label=com.docker.compose.service=caddy" \
    --format '{{.ID}}' 2>/dev/null | grep -q .
}
for PORT in 80 443; do
  if ss -tlnp 2>/dev/null | grep -q ":${PORT} " || \
     netstat -tlnp 2>/dev/null | grep -q ":${PORT} "; then
    if port_owned_by_vedha_caddy "$PORT"; then
      log "port ${PORT} is owned by the existing Vedha Caddy container ✓"
    else
      die "port ${PORT} is already in use by a non-Vedha process/container. Stop it before deploying."
    fi
  fi
done
log "ports 80/443 available ✓"

# CPU sizing
CPUS=$(nproc)
if [ -z "${API_WORKERS:-}" ]; then
  # Cap at 4 uvicorn workers — more thrashes RAM on shared box
  API_WORKERS=$(( CPUS < 2 ? 1 : (CPUS > 4 ? 4 : CPUS) ))
fi
log "cpu: ${CPUS} cores → API_WORKERS=${API_WORKERS}"

# ── 3. Package dependencies ───────────────────────────────────────────────────
step "Installing system dependencies"
command -v openssl >/dev/null || die "openssl is required"

if   command -v dnf >/dev/null;     then PKG="dnf -y"
elif command -v yum >/dev/null;     then PKG="yum -y"
elif command -v apt-get >/dev/null; then PKG="apt-get -y"; export DEBIAN_FRONTEND=noninteractive; apt-get update -qq
else die "no supported package manager (dnf/yum/apt-get)"; fi

$PKG install git curl ca-certificates iproute2 jq >/dev/null 2>&1 || \
  $PKG install git curl >/dev/null 2>&1 || true
command -v jq >/dev/null 2>&1 || die "jq is required for secret-safe deployment verification"
log "dependencies installed ✓"

# ── 4. Docker Engine ──────────────────────────────────────────────────────────
step "Docker Engine"
if ! command -v docker >/dev/null; then
  log "installing Docker..."
  if command -v apt-get >/dev/null; then
    $PKG install docker.io >/dev/null
  else
    $PKG install docker >/dev/null
  fi
fi
systemctl enable --now docker >/dev/null 2>&1 || service docker start >/dev/null 2>&1 || true
docker info >/dev/null 2>&1 || die "Docker daemon is not running after install attempt."
log "docker $(docker --version | awk '{print $3}' | tr -d ',') ✓"

# Docker Compose plugin
if ! docker compose version >/dev/null 2>&1; then
  log "installing Docker Compose plugin..."
  CLI_DIR=/usr/local/lib/docker/cli-plugins
  mkdir -p "$CLI_DIR"
  curl -fsSL \
    "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-${COMPOSE_ARCH}" \
    -o "$CLI_DIR/docker-compose"
  chmod +x "$CLI_DIR/docker-compose"
fi
docker compose version >/dev/null 2>&1 || die "docker compose unavailable after install."
log "docker compose $(docker compose version --short) ✓"

# ── 5. Locate or sparse-clone the repo ───────────────────────────────────────
step "Repository (sparse clone — manager + deploy only)"

# Detect if we're already inside a Vedha checkout
find_repo_root() {
  local d="$PWD"
  while [ "$d" != / ]; do
    [ -f "$d/manager/docker-compose.yml" ] && { echo "$d"; return 0; }
    d="$(dirname "$d")"
  done
  return 1
}

if SRC="$(find_repo_root)"; then
  log "using existing checkout at $SRC"
  APP_DIR="$SRC"

elif [ -d "$APP_DIR/.git" ]; then
  # Existing install — update only the sparse slices we care about.
  log "updating existing install at $APP_DIR..."
  git -C "$APP_DIR" fetch --depth 1 origin 2>&1 | tee -a "$DEPLOY_LOG" || warn "git fetch failed — deploying from current disk state"
  git -C "$APP_DIR" sparse-checkout reapply 2>/dev/null || true
  git -C "$APP_DIR" checkout 2>&1 | tee -a "$DEPLOY_LOG" || warn "git checkout failed — using existing files"

elif [ -n "$REPO_URL" ]; then
  # Fresh install — SPARSE + PARTIAL clone: only manager/ and deploy/ land on disk.
  # probe/, docs/, etc. are never fetched. Even if the EC2 box is compromised the
  # attacker cannot read probe source — it was never downloaded.
  log "sparse-cloning $REPO_URL → $APP_DIR (manager/ + deploy/ only)..."
  git clone \
    --filter=blob:none \
    --no-checkout \
    --depth 1 \
    "$REPO_URL" \
    "$APP_DIR" \
    2>&1 | tee -a "$DEPLOY_LOG"

  cd "$APP_DIR"
  git sparse-checkout init --cone
  # Cone mode: list directory names to include. Everything else is excluded.
  git sparse-checkout set manager deploy
  git checkout 2>&1 | tee -a "$DEPLOY_LOG"
  log "sparse clone complete. Directories present:"
  ls -1 "$APP_DIR"

else
  die "Not inside a Vedha checkout and REPO_URL is not set.\nEither: cd into your checkout and re-run, or set REPO_URL."
fi

cd "$APP_DIR"

[ -f manager/docker-compose.yml ]   || die "manager/docker-compose.yml not found — is the sparse checkout correct?"
[ -f .env.docker.example ] 2>/dev/null || [ -f manager/.env.docker.example ] 2>/dev/null || \
  warn ".env.docker.example not found — will generate .env from scratch"

# Resolve one immutable source revision. Deploying a moving branch means two
# hosts given the same command can build different artifacts.
if [ -z "$RELEASE_REF" ] && [ "$ALLOW_UNPINNED_RELEASE" != "1" ]; then
  die "RELEASE_REF is required (signed tag or commit SHA). Set ALLOW_UNPINNED_RELEASE=1 only for a disposable lab."
fi
if [ -n "$RELEASE_REF" ]; then
  git -C "$APP_DIR" diff --quiet && git -C "$APP_DIR" diff --cached --quiet || \
    die "tracked working-tree changes exist; refusing to overwrite them during a release checkout"
  git -C "$APP_DIR" fetch --depth 1 origin "$RELEASE_REF" 2>&1 | tee -a "$DEPLOY_LOG"
  RESOLVED_RELEASE="$(git -C "$APP_DIR" rev-parse 'FETCH_HEAD^{commit}')"
  if [ -n "$RELEASE_SHA" ]; then
    case "$RESOLVED_RELEASE" in
      "$RELEASE_SHA"*) ;;
      *) die "RELEASE_REF resolved to $RESOLVED_RELEASE, not expected RELEASE_SHA=$RELEASE_SHA" ;;
    esac
  fi
  if [ "$REQUIRE_SIGNED_RELEASE" = "1" ]; then
    if [ "$(git -C "$APP_DIR" cat-file -t "$RELEASE_REF" 2>/dev/null || true)" = "tag" ]; then
      git -C "$APP_DIR" verify-tag "$RELEASE_REF" >/dev/null 2>&1 || \
        die "release tag signature verification failed for $RELEASE_REF"
    else
      git -C "$APP_DIR" verify-commit "$RESOLVED_RELEASE" >/dev/null 2>&1 || \
        die "release commit signature verification failed for $RESOLVED_RELEASE"
    fi
  fi
  git -C "$APP_DIR" checkout --detach "$RESOLVED_RELEASE" 2>&1 | tee -a "$DEPLOY_LOG"
  git -C "$APP_DIR" sparse-checkout reapply 2>/dev/null || true
else
  RESOLVED_RELEASE="$(git -C "$APP_DIR" rev-parse HEAD)"
  warn "deploying unpinned revision $RESOLVED_RELEASE (lab override enabled)"
fi
RELEASE_ID="$(printf '%s' "$RESOLVED_RELEASE" | cut -c1-12)"
log "release: $RESOLVED_RELEASE ✓"

# ── 6. Pull secrets from SSM (optional — if AWS CLI + IAM role available) ────
step "Secrets resolution"

ssm_get() {
  aws ssm get-parameter \
    --name "${SSM_PREFIX}/$1" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text 2>/dev/null || true
}

# Do not require ssm:DescribeParameters: a least-privilege instance role only
# needs GetParameter on the configured path.
ssm_available() { command -v aws >/dev/null; }

if ssm_available; then
  log "SSM available — pulling secrets from ${SSM_PREFIX}/..."
  _ssm_jwt="$(ssm_get JWT_SECRET)"
  _ssm_probe_policy="$(ssm_get PROBE_POLICY_SIGNING_KEY)"
  _ssm_pg="$(ssm_get POSTGRES_PASSWORD)"
  _ssm_admin_pw="$(ssm_get SEED_ADMIN_PASSWORD)"
  _ssm_openai="$(ssm_get OPENAI_API_KEY)"
  _ssm_anthropic="$(ssm_get ANTHROPIC_API_KEY)"
  _ssm_domain="$(ssm_get DOMAIN)"
  [ -n "$_ssm_jwt" ]      && JWT_SECRET="$_ssm_jwt"
  [ -n "$_ssm_probe_policy" ] && PROBE_POLICY_SIGNING_KEY="$_ssm_probe_policy"
  [ -n "$_ssm_pg" ]       && POSTGRES_PASSWORD_SSM="$_ssm_pg"
  [ -n "$_ssm_admin_pw" ] && SEED_ADMIN_PASSWORD_SSM="$_ssm_admin_pw"
  [ -n "$_ssm_openai" ]   && OPENAI_API_KEY="${OPENAI_API_KEY:-$_ssm_openai}"
  [ -n "$_ssm_anthropic" ]&& ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-$_ssm_anthropic}"
  [ -n "$_ssm_domain" ]   && DOMAIN="${DOMAIN:-$_ssm_domain}"
  log "SSM pull complete ✓"
else
  [ "$SSM_REQUIRED" != "1" ] || die "SSM_REQUIRED=1 but the AWS CLI is unavailable"
  log "SSM not available — using env vars / generating secrets locally"
fi

if [ "$SSM_REQUIRED" = "1" ]; then
  [ -n "${_ssm_jwt:-}" ] || die "required SSM parameter ${SSM_PREFIX}/JWT_SECRET is unavailable"
  [ -n "${_ssm_probe_policy:-}" ] || die "required SSM parameter ${SSM_PREFIX}/PROBE_POLICY_SIGNING_KEY is unavailable"
  [ -n "${_ssm_pg:-}" ] || die "required SSM parameter ${SSM_PREFIX}/POSTGRES_PASSWORD is unavailable"
  [ -n "${_ssm_admin_pw:-}" ] || die "required SSM parameter ${SSM_PREFIX}/SEED_ADMIN_PASSWORD is unavailable"
fi

# ── 7. Generate / preserve secrets ───────────────────────────────────────────
gen_secret() { openssl rand -base64 48 | tr -d '\n/+='; }
env_get()    { [ -f .env ] && grep -m1 "^$1=" .env | cut -d= -f2- || true; }
volume_exists() { docker volume ls -q 2>/dev/null | grep -qx "$1"; }

# JWT secret: generate once, preserve forever
JWT_SECRET="${JWT_SECRET:-$(env_get JWT_SECRET)}"
[ -n "$JWT_SECRET" ] || JWT_SECRET="$(gen_secret)"

# Site-policy signing seed: preserve independently from JWT rotation.
PROBE_POLICY_SIGNING_KEY="${PROBE_POLICY_SIGNING_KEY:-$(env_get PROBE_POLICY_SIGNING_KEY)}"
[ -n "$PROBE_POLICY_SIGNING_KEY" ] || \
  PROBE_POLICY_SIGNING_KEY="$(openssl rand -base64 32 | tr -d '\n')"

# Admin password: preserve across re-runs unless SSM has an override
SEED_ADMIN_PASSWORD="${SEED_ADMIN_PASSWORD_SSM:-$(env_get SEED_ADMIN_PASSWORD)}"
[ -n "$SEED_ADMIN_PASSWORD" ] || SEED_ADMIN_PASSWORD="$(openssl rand -base64 18 | tr -d '\n/+=')Aa1!"

# Postgres password: CRITICAL — never rotate once the data volume exists.
# Changing it without recreating the volume = permanent authentication failure.
PG_ENV="${POSTGRES_PASSWORD_SSM:-$(env_get POSTGRES_PASSWORD)}"
if volume_exists vedha_pgdata; then
  if [ -z "$PG_ENV" ]; then
    die "pgdata volume exists but POSTGRES_PASSWORD is missing.\nRestore your .env or remove the volume: docker volume rm vedha_pgdata (DATA LOSS)."
  fi
  POSTGRES_PASSWORD="$PG_ENV"
  log "preserving existing Postgres password (data volume present) ✓"
elif [ -n "$PG_ENV" ] && [ "$PG_ENV" != "secret" ]; then
  POSTGRES_PASSWORD="$PG_ENV"
else
  POSTGRES_PASSWORD="$(gen_secret)"
  log "generated new Postgres password ✓"
fi

# Validate secret strength
[ ${#JWT_SECRET} -ge 32 ]         || die "JWT_SECRET too short (< 32 chars)"
[ ${#POSTGRES_PASSWORD} -ge 16 ]  || die "POSTGRES_PASSWORD too short (< 16 chars)"

# ── 8. LLM provider resolution ────────────────────────────────────────────────
step "LLM provider"
if [ -z "${LLM_PROVIDER:-}" ]; then
  if   [ -n "${OPENAI_API_KEY:-}" ];     then LLM_PROVIDER=openai
  elif [ -n "${ANTHROPIC_API_KEY:-}" ];  then LLM_PROVIDER=anthropic
  elif [ -n "${OPENROUTER_API_KEY:-}" ]; then LLM_PROVIDER=openrouter
  else LLM_PROVIDER=ollama; warn "no LLM API key — AI features inert until you set OPENAI_API_KEY / ANTHROPIC_API_KEY in SSM or .env"; fi
fi
log "LLM provider: $LLM_PROVIDER ✓"

# ── 9. TLS / Caddy configuration ─────────────────────────────────────────────
step "TLS & domain"

# Fetch public IP via IMDSv2 (EC2 only)
imds() {
  local token
  token=$(curl -s -m 3 -X PUT "http://169.254.169.254/latest/api/token" \
    -H "X-aws-ec2-metadata-token-ttl-seconds: 60" 2>/dev/null || true)
  curl -s -m 3 -H "X-aws-ec2-metadata-token: $token" \
    "http://169.254.169.254/latest/meta-data/$1" 2>/dev/null || true
}

CADDY_DIR="$APP_DIR/deploy/aws"

if [ -n "$DOMAIN" ]; then
  UI_HOST="app.$DOMAIN"
  API_HOST="api.$DOMAIN"
  COOKIE_SECURE=true
  UI_URL="https://$UI_HOST"
  API_URL="https://$API_HOST"

  # Validate DNS resolves before writing Caddyfile (Caddy will fail ACME if not)
  if command -v dig >/dev/null; then
    for HOST in "$UI_HOST" "$API_HOST"; do
      if ! dig +short "$HOST" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$'; then
        warn "DNS: $HOST does not resolve yet. Caddy ACME will fail until DNS propagates."
      else
        log "DNS: $HOST resolves ✓"
      fi
    done
  fi

  cat > "$CADDY_DIR/Caddyfile" <<EOF
{
    email $ACME_EMAIL
    # Disable admin API endpoint (not needed, reduces attack surface)
    admin off
}

$UI_HOST {
    encode gzip
    reverse_proxy frontend:3000 {
        header_up X-Real-IP {remote_host}
        health_path /
        health_interval 30s
    }
    # Security headers
    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server
    }
}

$API_HOST {
    encode gzip
    reverse_proxy api:8000 {
        header_up X-Real-IP {remote_host}
        health_path /health
        health_interval 15s
    }
    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        -Server
    }
}
EOF

else
  # No domain — self-signed for smoke testing only. NOT for production.
  PUBIP="$(imds public-ipv4)"
  [ -n "$PUBIP" ] || PUBIP="$(curl -fsSL https://checkip.amazonaws.com 2>/dev/null | tr -d '\n')" || true
  [ -n "$PUBIP" ] || die "DOMAIN not set and could not detect public IP. Set DOMAIN=your.domain.com."
  warn "No DOMAIN set — self-signed TLS on $PUBIP. Browsers will warn. Set DOMAIN for production."
  UI_HOST="$PUBIP"
  API_HOST="${PUBIP}:8443"
  COOKIE_SECURE=true
  UI_URL="https://$PUBIP"
  API_URL="https://${PUBIP}:8443"

  cat > "$CADDY_DIR/Caddyfile" <<EOF
{
    admin off
}

https://$PUBIP {
    tls internal
    encode gzip
    reverse_proxy frontend:3000
}

https://$PUBIP:8443 {
    tls internal
    encode gzip
    reverse_proxy api:8000
}
EOF
fi
log "Caddyfile written to $CADDY_DIR/Caddyfile ✓"

# ── 10. Generate the Caddy compose overlay ────────────────────────────────────
cat > "$CADDY_DIR/docker-compose.prod.yml" <<EOF
# Auto-generated by install.sh — do not edit by hand.
# Re-run install.sh to regenerate.
services:
  caddy:
    image: caddy:2-alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
      - "8443:8443"
    volumes:
      - ${CADDY_DIR}/Caddyfile:/etc/caddy/Caddyfile:ro
      - caddy_data:/data
      - caddy_config:/config
    healthcheck:
      test: ["CMD", "caddy", "validate", "--config", "/etc/caddy/Caddyfile"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      api:
        condition: service_healthy
    logging:
      driver: json-file
      options: {max-size: "10m", max-file: "3"}
volumes:
  caddy_data:
  caddy_config:
EOF
log "docker-compose.prod.yml written ✓"

# ── 11. Write .env atomically ─────────────────────────────────────────────────
step "Writing .env"

# SECURITY: write to temp file first, then atomic move.
# Direct append to .env leaves it world-readable during the write window.
ENV_TMP="$(mktemp "$APP_DIR/.env.XXXXXX")"
chmod 600 "$ENV_TMP"   # lock permissions BEFORE writing secrets

# Start from example if .env doesn't exist
if [ -f "$APP_DIR/.env" ]; then
  # Preserve user customizations — strip only the installer-managed block
  sed '/# >>> vedha-aws-installer >>>/,/# <<< vedha-aws-installer <<</d' "$APP_DIR/.env" > "$ENV_TMP"
else
  [ -f "$APP_DIR/.env.docker.example" ] && cp "$APP_DIR/.env.docker.example" "$ENV_TMP" || true
fi

# Append the installer-managed block
cat >> "$ENV_TMP" <<ENVEOF

# >>> vedha-aws-installer >>>  (managed by install.sh — re-run to update)
APP_ENV=production
LOG_LEVEL=${LOG_LEVEL:-INFO}
API_WORKERS=$API_WORKERS
API_BIND=127.0.0.1
FRONTEND_BIND=127.0.0.1
AUTH_COOKIE_SECURE=$COOKIE_SECURE
AUTH_COOKIE_SAMESITE=strict
JWT_SECRET=$JWT_SECRET
PROBE_POLICY_SIGNING_KEY=$PROBE_POLICY_SIGNING_KEY
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
SEED_ADMIN_EMAIL=$ADMIN_EMAIL
SEED_ADMIN_PASSWORD=$SEED_ADMIN_PASSWORD
LLM_PROVIDER=$LLM_PROVIDER
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-}
CORS_ORIGINS=$UI_URL
MANAGER_PUBLIC_URL=$API_URL
NEO4J_ENABLED=$([ "$ENABLE_GRAPH" = "1" ] && echo true || echo false)
VEDHA_RELEASE_ID=$RELEASE_ID
VEDHA_BACKEND_IMAGE=vedha-backend:$RELEASE_ID
VEDHA_FRONTEND_IMAGE=vedha-frontend:$RELEASE_ID
# <<< vedha-aws-installer <<<
ENVEOF

# Atomic swap
mv "$ENV_TMP" "$APP_DIR/.env"
chmod 600 "$APP_DIR/.env"
log ".env written (chmod 600) ✓"

# ── 12. Compose profile selection ────────────────────────────────────────────
COMPOSE_PROFILES_ARGS=(--profile ui)
[ "$ENABLE_GRAPH" = "1" ] && COMPOSE_PROFILES_ARGS+=(--profile graph)

# ── 13. Build and launch ──────────────────────────────────────────────────────
step "Building and launching stack"
log "profiles: ${COMPOSE_PROFILES_ARGS[*]}"
log "workers: $API_WORKERS  provider: $LLM_PROVIDER"

RELEASE_STATE="$APP_DIR/.release-current"
PREVIOUS_BACKEND_IMAGE=""
PREVIOUS_FRONTEND_IMAGE=""
if [ -f "$RELEASE_STATE" ]; then
  PREVIOUS_BACKEND_IMAGE="$(grep -m1 '^VEDHA_BACKEND_IMAGE=' "$RELEASE_STATE" | cut -d= -f2- || true)"
  PREVIOUS_FRONTEND_IMAGE="$(grep -m1 '^VEDHA_FRONTEND_IMAGE=' "$RELEASE_STATE" | cut -d= -f2- || true)"
fi
export VEDHA_BACKEND_IMAGE="vedha-backend:$RELEASE_ID"
export VEDHA_FRONTEND_IMAGE="vedha-frontend:$RELEASE_ID"

COMPOSE_CMD=(docker compose
  --env-file "$APP_DIR/.env"
  -f "$APP_DIR/manager/docker-compose.yml"
  -f "$APP_DIR/deploy/aws/docker-compose.prod.yml"
  "${COMPOSE_PROFILES_ARGS[@]}"
)

rollback_previous_release() {
  if [ -n "$PREVIOUS_BACKEND_IMAGE" ] && [ -n "$PREVIOUS_FRONTEND_IMAGE" ]; then
    warn "Attempting application rollback to retained immutable images..."
    export VEDHA_BACKEND_IMAGE="$PREVIOUS_BACKEND_IMAGE"
    export VEDHA_FRONTEND_IMAGE="$PREVIOUS_FRONTEND_IMAGE"
    "${COMPOSE_CMD[@]}" up -d --no-build 2>&1 | tee -a "$DEPLOY_LOG" || true
  else
    warn "No previous immutable release pointer exists; automatic rollback is unavailable."
  fi
}

# Remove orphaned containers from previous deploys (profile changes, service renames)
"${COMPOSE_CMD[@]}" up -d --build --remove-orphans 2>&1 | tee -a "$DEPLOY_LOG"

# ── 14. Wait for API health ───────────────────────────────────────────────────
step "Health check (up to ${DEPLOY_TIMEOUT}s)"
log "waiting for API to become healthy..."

DEADLINE=$(( $(date +%s) + DEPLOY_TIMEOUT ))
HEALTHY=0
while [ "$(date +%s)" -lt "$DEADLINE" ]; do
  if "${COMPOSE_CMD[@]}" exec -T api curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
    HEALTHY=1
    break
  fi
  sleep 5
done

if [ "$HEALTHY" != "1" ]; then
  warn "API did not become healthy within ${DEPLOY_TIMEOUT}s."
  log "Recent logs:"
  "${COMPOSE_CMD[@]}" logs --tail=60 migrate api 2>&1 | tee -a "$DEPLOY_LOG" || true

  rollback_previous_release
  die "Deployment failed. Check $DEPLOY_LOG for details."
fi
log "API healthy ✓"

# ── 15. Post-deploy smoke tests ───────────────────────────────────────────────
if [ "$SKIP_VERIFY" != "1" ]; then
  step "Smoke tests"
  if ! bash "$APP_DIR/deploy/aws/verify.sh" \
    --api-url "$API_URL" \
    --admin-email "$ADMIN_EMAIL" \
    --mode smoke \
    2>&1 | tee -a "$DEPLOY_LOG"; then
    rollback_previous_release
    die "Post-deploy verification failed; release not promoted."
  fi
elif [ "$ALLOW_SKIP_VERIFY" != "1" ]; then
  die "SKIP_VERIFY=1 requires explicit ALLOW_SKIP_VERIFY=1 (lab/emergency use only)"
fi

RELEASE_TMP="$(mktemp "$APP_DIR/.release-current.XXXXXX")"
chmod 600 "$RELEASE_TMP"
cat > "$RELEASE_TMP" <<RELEASEEOF
VEDHA_RELEASE_ID=$RELEASE_ID
VEDHA_RELEASE_SHA=$RESOLVED_RELEASE
VEDHA_BACKEND_IMAGE=vedha-backend:$RELEASE_ID
VEDHA_FRONTEND_IMAGE=vedha-frontend:$RELEASE_ID
RELEASEEOF
mv "$RELEASE_TMP" "$RELEASE_STATE"
chmod 600 "$RELEASE_STATE"
log "promoted immutable release $RELEASE_ID ✓"

# ── 16. Summary ───────────────────────────────────────────────────────────────
printf '\n\033[1;32m[vedha] ✓ Deployment complete.\033[0m\n'
cat <<SUMMARY

  Dashboard  : $UI_URL
  API        : $API_URL
  Admin      : $ADMIN_EMAIL
  Password   : retrieve from SSM or the root-only .env; rotate after first login
  Deploy log : $DEPLOY_LOG

Security checklist:
  □  Rotate admin password immediately after first login
  □  Security group: only 80, 443, 22 (your IP /32) open
  □  Verify CORS_ORIGINS in .env matches exactly: $UI_URL
  □  Enable CloudWatch log driver for persistent log shipping
  □  Schedule daily EBS snapshot + pg_dump to S3

Ops:
  • Status   :  docker compose --project-directory $APP_DIR -f $APP_DIR/manager/docker-compose.yml ps
  • Logs     :  docker compose --project-directory $APP_DIR -f $APP_DIR/manager/docker-compose.yml logs -f api worker
  • Redeploy :  sudo RELEASE_REF=<tag-or-sha> bash $APP_DIR/deploy/aws/install.sh
  • Verify   :  bash $APP_DIR/deploy/aws/verify.sh --mode full

SUMMARY
