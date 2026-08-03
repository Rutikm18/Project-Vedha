# Deploying Vedha on AWS

> **Architecture principle:** Only `manager/` and `deploy/` land on the AWS host.
> The probe source, detection engine source, and all other top-level directories
> are **never downloaded** to the EC2 box — sparse+partial clone enforces this at
> the git level, not just at the firewall level.

---

## Architecture overview

```
GitHub (private)                      AWS EC2 host
─────────────────                     ────────────────────────────────────────
manager/             ── sparse clone → /opt/vedha/manager/   ✓ present
  backend/                            /opt/vedha/deploy/     ✓ present
  frontend/
  detection_engine/   baked into      probe/                 ✗ NEVER cloned
deploy/               Docker image    docs/                  ✗ NEVER cloned
probe/               ✗ excluded      scripts/               ✗ NEVER cloned
docs/                ✗ excluded
```

```
Internet
   │
   ▼ 443/80
┌─────────────┐
│   Caddy     │  ← TLS termination, HSTS, security headers
└──────┬──────┘
       │ internal compose network only
  ┌────┴────┐      ┌────────┐      ┌────────────────┐
  │frontend │      │  api   │ ─── │    postgres    │
  │(Next.js)│      │(FastAPI│      │    redis       │
  └─────────┘      └────────┘      └────────────────┘
                        │                  ▲
                   ┌────┴────┐             │
                   │ worker  │─────────────┘
                   └─────────┘
  (No probe service — probe deploys on the target network, dials out to api.)
```

---

## Security model: sparse + partial clone

| What | Status on EC2 |
|------|--------------|
| `manager/backend` (FastAPI app) | ✓ Present — needed to build image |
| `manager/detection_engine` | ✓ Baked INTO image at build time, then source is gone |
| `manager/frontend` (Next.js) | ✓ Present — needed to build image |
| `probe/` (probe source) | **✗ Never downloaded** |
| `docs/` | **✗ Never downloaded** |

After `docker compose build`, even `manager/` source is only on disk — the
running container has the compiled artifact. For maximum security, add a post-build
cleanup step (see Day-2 ops).

---

## Root Cause Analysis — Production Findings

### CRITICAL-01: Full repo clone exposes probe source on EC2

**Root cause:** `git clone --depth 1` downloads all tracked files.
`probe/` contains scanner logic and network discovery code that should never
touch a server the customer doesn't own.

**Fix:** Sparse + partial clone (implemented in `deploy/aws/install.sh`):

```bash
git clone --filter=blob:none --no-checkout --depth 1 "$REPO_URL" "$APP_DIR"
cd "$APP_DIR"
git sparse-checkout init --cone
git sparse-checkout set manager deploy
git checkout
```

**Verification:** `ls /opt/vedha/` should show only `manager/` and `deploy/`.

---

### CRITICAL-02: Weak default JWT_SECRET in compose file

**Root cause:** The `x-backend-env` anchor has
`JWT_SECRET: ${JWT_SECRET:-change-me-at-least-32-chars-long!!}`. If `.env` is
missing or `JWT_SECRET` is unset, Compose silently substitutes the weak
default. Every deployment using the default shares the same signing key.

**Impact:** An attacker who knows the default can forge valid JWT tokens,
gaining admin access to any deployment that didn't rotate the secret.

**Fix (implemented):** `manager/docker-compose.yml` uses `:?` syntax — compose
will refuse to start with an error if the variable is empty:

```yaml
JWT_SECRET: ${JWT_SECRET:?JWT_SECRET must be set — run deploy/aws/install.sh}
```

**Verification:**
```bash
JWT_SECRET= docker compose -f manager/docker-compose.yml config 2>&1 | grep -i "required"
```

---

### CRITICAL-03: AUTH_COOKIE_SECURE defaults to false

**Root cause:** The root compose defaulted `AUTH_COOKIE_SECURE: ${AUTH_COOKIE_SECURE:-false}`.
If the installer forgot to set it, session cookies are sent without the `Secure`
flag, allowing theft over HTTP connections or by JavaScript.

**Fix (implemented):** `manager/docker-compose.yml` defaults to `true`. The
installer explicitly sets it to `true` in `.env`.

---

### HIGH-01: API and frontend ports bound to 0.0.0.0

**Root cause:** `"${API_PORT:-18080}:8000"` binds to all interfaces. Anyone
who can reach the EC2 host on port 18080 bypasses Caddy entirely — no TLS,
no security headers, no rate limiting.

**Fix (implemented):** Both files now bind to `127.0.0.1`:

```yaml
ports:
  - "127.0.0.1:${API_PORT:-18080}:8000"
```

**Verification:**
```bash
docker inspect vedha-api-1 --format '{{range .NetworkSettings.Ports}}{{range .}}{{.HostIp}}{{end}}{{end}}'
# should print: 127.0.0.1
```

---

### HIGH-02: Neo4j ports published to host

**Root cause:** Neo4j ports 7474 (HTTP) and 7687 (Bolt) were published to
`0.0.0.0`, exposing the graph DB to anyone who can reach the host. Neo4j's
default auth is weak.

**Fix (implemented):**
- Root compose: bound to `127.0.0.1` for local dev
- `manager/docker-compose.yml`: ports completely commented out (access via
  `docker compose exec neo4j cypher-shell`)

---

### HIGH-03: No pre-flight disk and port conflict checks

**Root cause:** `docker build` silently fails midway through if disk runs out
(leaves half-built layers consuming more space). Port 80/443 conflicts make
Caddy silently fail to start — the stack appears deployed but ACME never runs.

**Fix (implemented):** `install.sh` now checks:
- ≥10 GB free disk before build
- Ports 80 and 443 unoccupied before starting

---

### HIGH-04: .env written world-readable during install

**Root cause:** The original script ran `cat >> .env` then `chmod 600 .env`.
Between the write and the chmod, the file with plaintext secrets is
world-readable (default umask is 022).

**Fix (implemented):** Atomic write pattern — `chmod 600` the temp file BEFORE
writing any secret content, then `mv` atomically:

```bash
ENV_TMP="$(mktemp "$APP_DIR/.env.XXXXXX")"
chmod 600 "$ENV_TMP"          # lock BEFORE writing secrets
cat >> "$ENV_TMP" <<...       # write secrets to the already-locked file
mv "$ENV_TMP" "$APP_DIR/.env" # atomic rename — always 600
```

---

### MEDIUM-01: No deployment lock — concurrent installs corrupt state

**Root cause:** If two operators SSH in simultaneously and both run `install.sh`,
`git pull` + `docker compose up --build` run concurrently — one may build from
a partially-pulled tree and one may overwrite the other's `.env`.

**Fix (implemented):** `flock` on a lock file:

```bash
exec 200>/var/lock/vedha-install.lock
flock -n 200 || die "Another install is already running."
```

---

### MEDIUM-02: Redis has no persistence (data loss on restart)

**Root cause:** The original Redis service had no `command:` override — it used
the default Redis config with no persistence. The outbox worker queue was in
memory only. A Redis restart (OOM kill, EC2 reboot) drops all pending jobs.

**Fix (implemented):** `manager/docker-compose.yml` enables AOF persistence:

```yaml
command: >
  redis-server
  --appendonly yes
  --appendfsync everysec
```

---

### MEDIUM-03: No worker health check

**Root cause:** The original `worker` service had no `healthcheck:`. A crashed
worker produces no container restart signal — `docker compose ps` shows it
running even when it's deadlocked or stuck in a crash loop.

**Fix (implemented):** Basic healthcheck added. For production add a proper
worker liveness HTTP endpoint or heartbeat file check.

---

### LOW-01: Docker build context too broad

**Root cause:** `COPY . .` in the backend Dockerfile copies `.pytest_cache/`,
`.ruff_cache/`, test fixtures, and local `.env` files into the image if present.
Bloats image size and risks leaking local secrets into the image layer.

**Recommended fix:** Add to `manager/backend/.dockerignore`:

```
.env
.env.*
!.env.example
.pytest_cache/
.ruff_cache/
__pycache__/
*.pyc
tests/
.venv/
node_modules/
*.md
```

---

## 1. Prerequisites

1. AWS account + CLI (`aws configure`)
2. Domain you control (Route53 easiest)
3. EC2 key pair:
   ```bash
   aws ec2 create-key-pair --key-name vedha --query 'KeyMaterial' \
     --output text > ~/.ssh/vedha.pem && chmod 400 ~/.ssh/vedha.pem
   ```
4. Cloud LLM API key (OpenAI / Anthropic / OpenRouter)

---

## 2. Sizing

| Profile | Instance | vCPU / RAM | EBS | ~Cost/mo |
|---------|----------|-----------|-----|----------|
| Core + UI, cloud LLM | `t3.large` | 2 / 8 GB | 40 GB gp3 | ~$60 |
| + attack-path graph | `t3.xlarge` | 4 / 16 GB | 60 GB gp3 | ~$120 |

Do **not** run Ollama on AWS — it requires a GPU instance and costs ~$700/mo.
Use OpenAI / Anthropic / OpenRouter instead.

---

## 3. Store secrets in SSM (do this first)

```bash
gen() { openssl rand -base64 48 | tr -d '\n'; }

aws ssm put-parameter --name /vedha/JWT_SECRET          --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/POSTGRES_PASSWORD   --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/SEED_ADMIN_PASSWORD --type SecureString --value "$(gen)Aa1!"
aws ssm put-parameter --name /vedha/OPENAI_API_KEY      --type SecureString --value "sk-..."
aws ssm put-parameter --name /vedha/DOMAIN              --type String       --value "vedha.example.com"
aws ssm put-parameter --name /vedha/ADMIN_EMAIL         --type String       --value "admin@example.com"
```

Give the EC2 instance an IAM role with:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["ssm:GetParameter", "ssm:GetParameters", "ssm:GetParametersByPath"],
    "Resource": "arn:aws:ssm:*:*:parameter/vedha/*"
  }, {
    "Effect": "Allow",
    "Action": "kms:Decrypt",
    "Resource": "*"
  }]
}
```

---

## 4. Deploy (EC2 user-data — fully unattended)

```bash
#!/usr/bin/env bash
export REPO_URL=https://github.com/<org>/vedha.git
export DOMAIN=vedha.example.com
# SSM secrets pulled automatically by install.sh when IAM role is attached
bash <(curl -fsSL "https://raw.githubusercontent.com/<org>/vedha/main/deploy/aws/install.sh")
```

**Or manually (SSH in):**

```bash
# Sparse clone — probe source never touches this host
git clone --filter=blob:none --no-checkout --depth 1 \
  https://github.com/<org>/vedha.git /opt/vedha
cd /opt/vedha
git sparse-checkout init --cone
git sparse-checkout set manager deploy
git checkout

sudo DOMAIN=vedha.example.com bash deploy/aws/install.sh
```

---

## 5. Networking

**Security group — open only:**

| Port | Source | Why |
|------|--------|-----|
| 22 (SSH) | your admin IP `/32` | maintenance only |
| 80 (HTTP) | `0.0.0.0/0` | ACME challenge + HTTPS redirect |
| 443 (HTTPS) | `0.0.0.0/0` (or operator IPs) | UI + API |

**Never open:** 5432, 6379, 3000, 8000, 18080, 7474, 7687

**Elastic IP + DNS:**

```bash
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-xxxx --allocation-id eipalloc-xxxx
```

Create DNS A records → Elastic IP:
```
app.vedha.example.com  →  <elastic-ip>
api.vedha.example.com  →  <elastic-ip>
```

---

## 6. Verification (run after every deploy)

```bash
# Full post-deploy verification
bash /opt/vedha/deploy/aws/verify.sh --mode full

# Quick smoke test
bash /opt/vedha/deploy/aws/verify.sh --mode smoke \
  --admin-email admin@vedha.io

# Manual health check
curl -sS https://api.vedha.example.com/health -w '\nHTTP=%{http_code}\n'
```

---

## 7. Startup validator (application-level)

The FastAPI app runs `scripts/startup_validator.py` at boot. It validates:

- All required env vars are set
- JWT_SECRET is ≥32 chars and not a known-weak value
- AUTH_COOKIE_SECURE=true in production
- CORS_ORIGINS doesn't include localhost in production
- DATABASE_URL uses asyncpg driver
- detection_engine directory is present in the image
- Database is reachable
- Redis is reachable

**To run manually:**

```bash
docker compose exec api python scripts/startup_validator.py
```

---

## 8. Connect a probe

The probe deploys on the **target network** and dials **out** to the API. No
inbound port needed on the probe host. On the probe host:

```bash
# Clone ONLY the probe slice (mirror of how manager-only is cloned for AWS)
git clone --filter=blob:none --no-checkout --depth 1 \
  https://github.com/<org>/vedha.git /opt/vedha-probe
cd /opt/vedha-probe
git sparse-checkout init --cone
git sparse-checkout set probe
git checkout

export PLATFORM_URL=https://api.vedha.example.com
export OPERATOR_EMAIL=admin@vedha.io
export OPERATOR_PASSWORD=<password>
export PROBE_NETWORK_SEGMENTS=10.0.0.0/24
docker compose --profile probe up -d probe
```

---

## 9. Day-2 operations

**Redeploy after a code change:**

```bash
cd /opt/vedha
git fetch --depth 1 origin
git checkout          # sparse-checkout reapply is automatic
sudo bash deploy/aws/install.sh
```

**Logs:**

```bash
docker compose --project-directory /opt/vedha \
  -f /opt/vedha/manager/docker-compose.yml logs -f api worker
```

**Backups:**

```bash
# Logical DB dump to S3
docker compose exec -T postgres pg_dump -U vapt vapt_db | gzip \
  | aws s3 cp - s3://vedha-backups/pg/$(date +%F).sql.gz
```

Schedule via `/etc/cron.daily/vedha-pgdump`.

**Source cleanup (optional hardening):** After a successful deploy you can
remove the source tree — the images are already built and running:

```bash
# Optionally rm -rf /opt/vedha/manager after build (containers are already running)
# Re-run install.sh will re-clone next time
```

---

## 10. Production Readiness Checklist

Run before every production deployment:

```
□  SSM secrets set for JWT_SECRET, POSTGRES_PASSWORD, SEED_ADMIN_PASSWORD, OPENAI_API_KEY
□  EC2 IAM role has ssm:GetParameter* + kms:Decrypt on /vedha/*
□  Security group: only 80, 443, 22 (your /32) open — 18080/3000/5432/6379/7474/7687 CLOSED
□  Elastic IP allocated and associated with instance
□  DNS A records for app.<domain> and api.<domain> pointing to Elastic IP
□  IMDSv2 enforced: aws ec2 modify-instance-metadata-options --http-tokens required
□  EBS encrypted (--encrypted flag on volume)
□  EBS snapshot lifecycle policy configured (daily, 7-day retention)
□  pg_dump cron job to S3 configured

After deploy:
□  bash /opt/vedha/deploy/aws/verify.sh --mode full → all checks pass
□  Admin password rotated (first login → change password)
□  docker exec vedha-api-1 python scripts/startup_validator.py → no errors
□  ls /opt/vedha/ confirms probe/ is NOT present
□  docker inspect vedha-api-1 confirms 127.0.0.1 binding (not 0.0.0.0)
□  curl https://api.<domain>/health → HTTP 200
□  Curl response has Strict-Transport-Security header
□  Log in via https://app.<domain> — session works
```

---

## 11. Error catalog

| Symptom | Root cause | Detection | Fix |
|---------|-----------|-----------|-----|
| `JWT_SECRET must be set` on compose up | `:?` guard triggered | compose error | Set JWT_SECRET in SSM or .env |
| API never healthy (180s timeout) | Migration failed | `docker compose logs migrate` | Check Alembic + DB connectivity |
| Browser cert warning | Caddy ACME failed | `docker compose logs caddy` | Ensure port 80 open + DNS resolves |
| Login returns 401 | Seed failed or wrong password | `docker compose logs migrate` | Check seed_admin.py logs |
| `port already in use` | Something using 80/443 | `ss -tlnp \| grep :80` | Stop conflicting service first |
| Worker silently dead | Crash loop | `docker compose ps` + `logs worker` | Check worker logs; verify Redis reachable |
| pgdata volume exists but password missing | .env deleted after first run | `docker volume ls` | Restore .env or full redeploy (data loss) |
| Probe can't register | Wrong PLATFORM_URL | Probe logs | Must be `https://api.<domain>`, not `:18080` |
| CORS 403 on API | CORS_ORIGINS mismatch | Browser devtools | Set CORS_ORIGINS=https://app.<domain> |
| 18080 accessible from internet | SG misconfigured | `curl http://<ip>:18080/health` | Add SG inbound deny rule; now also bound to 127.0.0.1 |

---

## 12. Scale path

| Bottleneck | Replacement |
|-----------|-------------|
| Postgres CPU / disk | **RDS for PostgreSQL** — set `DATABASE_URL`, remove postgres service |
| Redis data loss | **ElastiCache** — set `REDIS_URL`, remove redis service |
| API horizontal scale | **ECS Fargate** behind **ALB** — same images, no code change |
| Secrets rotation | **Secrets Manager** (auto-rotation) instead of SSM SecureString |

_Last updated: 2026-08-02. Architecture: sparse-clone single EC2 + Compose + Caddy._
_Owner: platform. See [`../README.md`](../README.md) for the docs map._
