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

> **Minimum 4 GB RAM — the free tier (t3.micro, 1 GB) will NOT work.** The Next.js
> production build type-checks in a child process that OOMs below ~4 GB. `install.sh`
> auto-provisions 4 GB swap when RAM < 4 GB, but a 1 GB box still can't finish the
> build (and can't comfortably run the stack). Use **≥ 4 GB** — `t3.medium` (4 GB)
> minimum, `t3.large` (8 GB) recommended. A non-AWS 8 GB VPS (Hetzner / Hostinger /
> DigitalOcean) runs the same `install.sh` and is often far cheaper.

---

## 3. Secrets: `.env` or SSM (SSM is optional)

`install.sh` resolves every secret in this order — **the first value found wins:**

> **exported env var → SSM `$SSM_PREFIX/<NAME>` (default `/vedha`) → existing `.env` → auto-generated**

So the infra secrets are **optional** — if you don't supply them the installer
generates strong values and preserves them across re-runs:

| Secret | If you don't set it |
|--------|---------------------|
| `JWT_SECRET` | auto-generated, then preserved forever |
| `POSTGRES_PASSWORD` | auto-generated (never rotated once the data volume exists) |
| `SEED_ADMIN_PASSWORD` | auto-generated (printed at the end of the install) |
| `PROBE_POLICY_SIGNING_KEY` | auto-generated |

The **only value you must supply for AI features** is at least one cloud LLM key:
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`, or
`OPENROUTER_API_KEY`. Any keys present join the automatic premium-first fallback
chain (`anthropic → openai → gemini → groq → openrouter`); with no key the stack
still runs, AI features just stay inert. Step-by-step key setup, network checks, a live
verification and the symptom → fix table are in [AI on AWS](aws-ai-setup.md).

### Option A — `.env` file (simplest; no AWS IAM needed)

After the clone (§4 step 2), create `/opt/vedha/.env` with just your key(s) plus any
overrides — the installer fills in the rest and keeps your values on re-run:

```bash
sudo tee /opt/vedha/.env >/dev/null <<'EOF'
# at least one AI key (set as many as you like — they form the fallback chain)
ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
# OPENROUTER_API_KEY=sk-or-...

# optional
DOMAIN=vedha.example.com
ADMIN_EMAIL=admin@example.com
# ENABLE_GRAPH=1            # also start the Neo4j attack-path graph
# SEED_ADMIN_PASSWORD=...   # else auto-generated and printed at the end
EOF
sudo chmod 600 /opt/vedha/.env
```

Or skip the file and just `export` the key for one run (see §4 step 3).

### Option B — AWS SSM Parameter Store (optional; best for fleets / no secrets on disk)

If the instance has an IAM role, `install.sh` auto-pulls `$SSM_PREFIX/<NAME>`
(default prefix `/vedha`). Add `SSM_REQUIRED=1` to fail the install if core secrets
are missing.

```bash
# only the AI key is needed; the rest are optional (else auto-generated)
aws ssm put-parameter --name /vedha/ANTHROPIC_API_KEY   --type SecureString --value "sk-ant-..."
aws ssm put-parameter --name /vedha/DOMAIN              --type String       --value "vedha.example.com"
# optional explicit overrides:
gen() { openssl rand -base64 48 | tr -d '\n'; }
aws ssm put-parameter --name /vedha/JWT_SECRET          --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/POSTGRES_PASSWORD   --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/SEED_ADMIN_PASSWORD --type SecureString --value "$(gen)Aa1!"
```

Give the EC2 instance an IAM role with `ssm:GetParameter*` + `kms:Decrypt` on `/vedha/*`:
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

## 4. Install — step by step

> **Repo:** `https://github.com/Rutikm18/Project-Vedha.git`
> `install.sh` deploys an **immutable, pinned release by default** — pass
> `RELEASE_REF=<tag-or-commit>` for production, or `ALLOW_UNPINNED_RELEASE=1` to
> deploy the current branch tip (lab/quick). It refuses to run if the checkout has
> local tracked changes.

**1 — Launch & open ports.** Start the instance (§2), set the security-group
inbound rules for your TLS mode (§5), then SSH in.

**2 — Sparse-clone only `manager/` + `deploy/`** (the probe source never lands here):

```bash
sudo mkdir -p /opt/vedha && sudo chown "$USER" /opt/vedha
git clone --filter=blob:none --no-checkout --depth 1 \
  https://github.com/Rutikm18/Project-Vedha.git /opt/vedha
cd /opt/vedha
git sparse-checkout init --cone
git sparse-checkout set manager deploy
git checkout
```

**3 — Provide your AI key** (§3) — a `.env` file, SSM, or just export it for this run:

```bash
export ANTHROPIC_API_KEY=sk-ant-...        # or OPENAI_API_KEY=sk-...
```

**4 — Run the installer** (`-E` keeps your exported vars under `sudo`):

*Mode A — domain + Let's Encrypt (HTTPS, recommended):*
```bash
sudo -E DOMAIN=vedha.example.com ALLOW_UNPINNED_RELEASE=1 bash deploy/aws/install.sh
# production: swap ALLOW_UNPINNED_RELEASE=1 for RELEASE_REF=<tag-or-commit>
```

*Mode B — bare IP + self-signed (quick, no domain):*
```bash
sudo -E ALLOW_UNPINNED_RELEASE=1 bash deploy/aws/install.sh
#  UI  → https://<public-ip>         (open 443)
#  API → https://<public-ip>:8443    (open 8443)   ← see §5
```

**5 — Verify** and grab the admin password printed at the end of the run:
```bash
bash /opt/vedha/deploy/aws/verify.sh --mode full
```

### Fully unattended (EC2 user-data)

The installer does its own sparse clone when `REPO_URL` is set:

```bash
#!/usr/bin/env bash
export REPO_URL=https://github.com/Rutikm18/Project-Vedha.git
export DOMAIN=vedha.example.com
export ALLOW_UNPINNED_RELEASE=1          # or RELEASE_REF=<tag-or-commit> for prod
# AI key: put it in SSM (/vedha/ANTHROPIC_API_KEY, auto-pulled via IAM role) or export here
curl -fsSL "https://raw.githubusercontent.com/Rutikm18/Project-Vedha/main/deploy/aws/install.sh" | sudo -E bash
```

---

## 5. Networking — ports to open

The host exposes **only Caddy**. Every backend service (FastAPI, Next.js,
PostgreSQL, Redis, Neo4j, Ollama) stays on the internal Docker network or is bound
to `127.0.0.1` — none of them are reachable from the internet directly. **Which
public ports you open depends on how TLS is terminated**, and there are two modes.

### Mode A — domain + Let's Encrypt (`make tls` / `./setup-https.sh`) — recommended

Caddy serves the UI (`app.<domain>`) and the API (`api.<domain>`) **both on 443**,
routed by hostname, and uses **port 80** for the ACME certificate challenge.

| Port | Proto | Source | Why |
|------|-------|--------|-----|
| 22 | TCP | your admin IP `/32` | SSH maintenance only |
| 80 | TCP | `0.0.0.0/0` | Let's Encrypt ACME challenge + HTTP→HTTPS redirect |
| 443 | TCP | `0.0.0.0/0` (or operator IPs) | UI **and** API (split by hostname) |

### Mode B — bare IP + self-signed (`install.sh` default, no domain)

With no domain, Caddy uses `tls internal` (self-signed) and serves the UI on **443**
but the **API on a separate port — 8443** (`API_URL=https://<ip>:8443`). **You must
open 8443**, or the dashboard loads while every API call fails.

| Port | Proto | Source | Why |
|------|-------|--------|-----|
| 22 | TCP | your admin IP `/32` | SSH maintenance only |
| 443 | TCP | `0.0.0.0/0` (or operator IPs) | UI dashboard — `https://<ip>` |
| **8443** | TCP | `0.0.0.0/0` (or operator IPs) | **API — `https://<ip>:8443` — REQUIRED** |
| 80 | TCP | optional | HTTP→HTTPS redirect only (no ACME in self-signed mode) |

### Never expose (internal only — `127.0.0.1` or the compose network)

| Port | Service | | Port | Service |
|------|---------|-|------|---------|
| 8000 | FastAPI (via Caddy only) | | 5432 | PostgreSQL |
| 3000 | Next.js (via Caddy only) | | 6379 | Redis |
| 18080 | API local-tooling bind (`127.0.0.1`) | | 7474 / 7687 | Neo4j HTTP / Bolt |
| 11434 | Ollama (if the `ollama` profile is on) | | | |

### Outbound (egress) the host needs

| Port | Destination | Why |
|------|-------------|-----|
| 443 | `api.anthropic.com` / `api.openai.com` / `generativelanguage.googleapis.com` / `api.groq.com` / `openrouter.ai` (only the providers you configured) | cloud LLM calls |
| 443 | GitHub + container registries | clone/pull during install & redeploy |
| 80 + 443 | `*.letsencrypt.org` | certificate issuance (Mode A only) |
| 53 | DNS resolver | name resolution |

### Probe connectivity (runs on the CLIENT / target network — no inbound)

The probe dials **out** to the manager API and needs **no inbound port**. On the
client network, allow **egress** to the manager host on **443** (Mode A) or **8443**
(Mode B) — the HTTPS API and the WebSocket control channel ride the same port.

**Elastic IP + DNS** (Mode A):

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
  https://github.com/Rutikm18/Project-Vedha.git /opt/vedha-probe
cd /opt/vedha-probe
git sparse-checkout init --cone
git sparse-checkout set probe
git checkout

# Mode A (domain): https://api.<domain>   |   Mode B (bare IP): https://<ip>:8443
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
□  Security group matches §5 for your TLS mode — Mode A (domain): 22/80/443 · Mode B (bare IP): 22/443/8443. Internal ports CLOSED: 8000/3000/18080/5432/6379/7474/7687/11434
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
| `NEO4J_PASSWORD … is missing a value` | Compose interpolates the whole file incl. `neo4j` regardless of active profile | compose error at build | **Auto-fixed** — `install.sh` generates `NEO4J_PASSWORD`; compose defaults it |
| `classic builder doesn't support additional contexts` | Buildx not installed; backend image uses BuildKit additional contexts | build error | **Auto-fixed** — `install.sh` installs `docker-buildx` |
| `JavaScript heap out of memory` at "Running TypeScript" | Box < 4 GB; Node auto-sizes a tiny heap for the Next.js build | build log | **Partly auto** — `install.sh` adds 4 GB swap + raises the Node heap; still needs a **≥ 4 GB box** (see §2) |
| `image "vedha-backend:…" already exists` | `migrate`/`api`/`worker` share one image tag; parallel BuildKit races the containerd store | build error | **Auto-fixed** — `install.sh` builds the backend once (via `api`), then `up --no-build` |
| `openssl` / `make` not found | Package not pre-installed | install error | **Auto-fixed** — `install.sh` installs `make openssl util-linux` in the dependency step |

> The five rows above are now handled automatically by `install.sh` on a fresh box —
> kept here for reference. The only one still needing operator action is the memory
> one: use a **≥ 4 GB** instance (see §2 Sizing).

---

## 12. Scale path

| Bottleneck | Replacement |
|-----------|-------------|
| Postgres CPU / disk | **RDS for PostgreSQL** — set `DATABASE_URL`, remove postgres service |
| Redis data loss | **ElastiCache** — set `REDIS_URL`, remove redis service |
| API horizontal scale | **ECS Fargate** behind **ALB** — same images, no code change |
| Secrets rotation | **Secrets Manager** (auto-rotation) instead of SSM SecureString |

_Last updated: 2026-10-02. Architecture: sparse-clone single EC2 + Compose + Caddy._
_Owner: platform. See [`../README.md`](../README.md) for the docs map._
