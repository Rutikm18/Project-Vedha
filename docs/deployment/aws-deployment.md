# Deploying Vedha on AWS

> **Goal:** stand up a production Vedha instance on AWS in ~20 minutes, with one
> bootstrap script, automatic HTTPS, and as few manual steps as possible.
>
> **Model:** single EC2 host running the existing `docker compose` stack behind
> [Caddy](https://caddyserver.com) (automatic Let's Encrypt TLS). This is the
> same self-host pattern shipped by Supabase, Plausible, n8n, and PostHog: one
> VM to start, a documented path to managed services (RDS / ElastiCache / ECS)
> when you outgrow it.

---

## 1. What actually runs

Vedha is already a self-contained Compose stack (`docker-compose.yml`). You do
**not** rearchitect anything to deploy it.

| Service | Profile | Port (container) | Exposed to internet? |
|---------|---------|------------------|----------------------|
| `api` (FastAPI) | default | 8000 | via Caddy → `api.<domain>` |
| `worker` | default | — | no |
| `postgres` | default | 5432 | **no** (compose network only) |
| `redis` | default | 6379 | **no** |
| `migrate` (one-shot: alembic + seed admin) | default | — | no |
| `frontend` (Next.js BFF) | `ui` | 3000 | via Caddy → `app.<domain>` |
| `neo4j` (attack-path graph) | `graph` | 7474/7687 | **no** (optional) |
| `ollama` (local LLM) | `local-ai` | 11434 | no — **skip on AWS**, use a cloud LLM |
| `probe` | `probe` | — | **dials out only**, no inbound |

**Key facts that shape the deployment:**

- The **frontend is a BFF** — the browser only ever talks to the frontend; the
  frontend reaches the API over the internal Compose network
  (`BACKEND_INTERNAL_URL=http://api:8000`). No CORS in the browser path.
- **Operators** use `https://app.<domain>` (the UI).
- **Probes and CLI/curl clients** use `https://api.<domain>` (the REST API).
  This replaces the raw `:18080` you used locally — in production the API is
  served over 443 by Caddy.
- **Postgres/Redis are never published to the host** — they stay on the Compose
  network. Do not open 5432/6379 in the security group.
- The **probe never needs an inbound port**; it registers outbound to
  `api.<domain>`. So the only inbound ports you open are 443, 80 (ACME), 22.

---

## 2. Cost & sizing

Pick the instance by which profiles you enable. Use a **cloud LLM**
(OpenAI/Anthropic/OpenRouter) on AWS — running Ollama locally needs a large or
GPU instance and defeats "simple."

| Profile set | Instance | vCPU / RAM | EBS | ~US-east cost/mo |
|-------------|----------|-----------|-----|------------------|
| Core + UI, cloud LLM | `t3.large` | 2 / 8 GB | 40 GB gp3 | ~$60 + LLM usage |
| + attack-path graph (`graph`) | `t3.xlarge` | 4 / 16 GB | 60 GB gp3 | ~$120 |
| Local LLM (`local-ai`) | `g5.xlarge` (GPU) | 4 / 16 GB + A10G | 100 GB | ~$700 — avoid unless required |

Set `API_WORKERS=2` on a `t3.large` (4 uvicorn workers can thrash 8 GB when
Postgres + Redis share the box).

---

## 3. Prerequisites (one-time)

1. **AWS account** + the [AWS CLI](https://docs.aws.amazon.com/cli/) configured
   (`aws configure`).
2. A **domain** you control (e.g. `vedha.example.com`) with DNS you can edit.
   Route 53 is easiest but any registrar works.
3. An **EC2 key pair** for SSH:
   ```bash
   aws ec2 create-key-pair --key-name vedha --query 'KeyMaterial' \
     --output text > ~/.ssh/vedha.pem && chmod 400 ~/.ssh/vedha.pem
   ```
4. Decide your **cloud LLM** and have its API key ready (see
   [`.env.docker.example`](../../.env.docker.example) for `LLM_PROVIDER`).

---

## 4. Store secrets first (SSM Parameter Store)

Never bake secrets into the AMI, user-data, or git. Put them in SSM once; the
bootstrap script pulls them at boot. `SecureString` params are KMS-encrypted and
free at this scale.

```bash
gen() { openssl rand -base64 48 | tr -d '\n'; }

aws ssm put-parameter --name /vedha/JWT_SECRET        --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/POSTGRES_PASSWORD --type SecureString --value "$(gen)"
aws ssm put-parameter --name /vedha/SEED_ADMIN_PASSWORD --type SecureString --value 'ChangeMe-Strong-1!'
aws ssm put-parameter --name /vedha/OPENAI_API_KEY    --type SecureString --value 'sk-...'   # your provider key
aws ssm put-parameter --name /vedha/DOMAIN            --type String       --value 'vedha.example.com'
aws ssm put-parameter --name /vedha/ADMIN_EMAIL       --type String       --value 'admin@vedha.io'
```

> Give the EC2 instance an **IAM role** with `ssm:GetParameter*` and
> `kms:Decrypt` on `arn:aws:ssm:*:*:parameter/vedha/*` (created in step 5).

---

## 5. Provision the instance (one script)

All of the provisioning — Docker, Compose, secrets, `.env`, Caddy, and launch —
is done by a **single, self-contained, idempotent installer** that lives in the
repo: [`deploy/aws/install.sh`](../../deploy/aws/install.sh). It generates every
auxiliary file itself (nothing else to copy), auto-sizes workers to the box,
never rotates the Postgres password once the data volume exists, and is safe to
re-run for upgrades.

**Manual (SSH in, zero files to copy beyond the repo):**

```bash
git clone --depth 1 https://github.com/<your-org>/vedha.git /opt/vedha
cd /opt/vedha
sudo DOMAIN=vedha.example.com OPENAI_API_KEY=sk-... bash deploy/aws/install.sh
```

**Fully unattended (EC2 user-data — nothing to copy at all):** paste this as the
instance's user-data; it runs on first boot and the instance comes up deployed.

```bash
#!/usr/bin/env bash
export REPO_URL=https://github.com/<your-org>/vedha.git
export DOMAIN=vedha.example.com
# Prefer SSM over inline secrets in real deployments (see step 4):
export OPENAI_API_KEY=$(aws ssm get-parameter --name /vedha/OPENAI_API_KEY --with-decryption --query Parameter.Value --output text)
curl -fsSL "https://raw.githubusercontent.com/<your-org>/vedha/main/deploy/aws/install.sh" | bash
```

The script accepts everything via env vars (`DOMAIN`, `REPO_URL`, `ADMIN_EMAIL`,
`LLM_PROVIDER`, the provider keys, `ENABLE_GRAPH=1`, `API_WORKERS`). Omit
`DOMAIN` and it falls back to the instance's public IP with self-signed TLS
(UI on `:443`, API on `:8443`) so you can smoke-test before DNS is ready.

Launch the instance (replace the SG/subnet/role from step 6):

```bash
aws ec2 run-instances \
  --image-id resolve:ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --instance-type t3.large \
  --key-name vedha \
  --security-group-ids sg-xxxxxxxx \
  --iam-instance-profile Name=vedha-ssm-role \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":40,"VolumeType":"gp3"}}]' \
  --user-data file://user-data.sh \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=vedha-prod}]'
```

---

## 6. Networking (security group, Elastic IP, DNS)

**Security group** — open only what's needed:

| Port | Source | Why |
|------|--------|-----|
| 22 (SSH) | your admin IP `/32` only | maintenance |
| 80 (HTTP) | `0.0.0.0/0` | Let's Encrypt ACME challenge + HTTP→HTTPS redirect |
| 443 (HTTPS) | operator IPs (or `0.0.0.0/0`) | UI + API |

Do **not** open 5432, 6379, 3000, 8000, or 18080. Caddy reaches `frontend:3000`
and `api:8000` over the internal Compose network, so even though the base compose
still binds those ports on the host, the security group is what keeps them off
the internet. (For defense-in-depth you can bind them to `127.0.0.1` in the base
compose, but the SG is the real control.)

**Elastic IP + DNS** — allocate a static IP and point both subdomains at it:

```bash
aws ec2 allocate-address --domain vpc
aws ec2 associate-address --instance-id i-xxxx --allocation-id eipalloc-xxxx
```

Create two DNS `A` records → the Elastic IP:

```
app.vedha.example.com  →  <elastic-ip>
api.vedha.example.com  →  <elastic-ip>
```

Once DNS resolves, Caddy fetches TLS certs automatically on first request.

---

## 7. First-run verification

```bash
# Health (should be 200)
curl -sS https://api.vedha.example.com/health -w '\nHTTP=%{http_code}\n'

# Log in with the seeded admin (email/password from SSM)
curl -sS -X POST https://api.vedha.example.com/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@vedha.io","password":"<SEED_ADMIN_PASSWORD>"}'
```

Then open `https://app.vedha.example.com` in a browser.

> The `migrate` service runs Alembic + seeds the admin **once**, then exits;
> `api` only starts after it succeeds. If `api` never becomes healthy, check
> `docker compose logs migrate`.

---

## 8. Connect a probe (field VA)

A probe is any host on the target network. It dials **out** to
`api.vedha.example.com` — no inbound ports on the probe, nothing to open in the
target's firewall for *inbound*. On the probe host:

```bash
export PLATFORM_URL=https://api.vedha.example.com
export OPERATOR_EMAIL=admin@vedha.io
export OPERATOR_PASSWORD=<seed-admin-password>
export PROBE_NETWORK_SEGMENTS=10.0.0.0/24   # the scope it may scan
docker compose --profile probe up -d probe
```

See [`../../PROBE_RUNBOOK.md`](../../PROBE_RUNBOOK.md) for probe registration and
PAT details.

---

## 9. Day-2 operations

**Redeploy after a code change** — just re-run the installer. It's idempotent:
pulls latest, preserves `.env`/secrets, and reconciles the stack.

```bash
cd /opt/vedha && sudo bash deploy/aws/install.sh
```

**Backups** — two layers:

1. **EBS snapshots** (whole-disk, automated) via a Data Lifecycle Manager policy
   on the instance's volume — set daily, 7-day retention.
2. **Logical Postgres dump** to S3 (point-in-time restore of just the DB):
   ```bash
   # /etc/cron.daily/vedha-pgdump
   docker compose exec -T postgres pg_dump -U vapt vapt_db | gzip \
     | aws s3 cp - s3://vedha-backups/pg/$(date +\%F).sql.gz
   ```

**Logs & health:**

```bash
docker compose ps                    # service health
docker compose logs -f api worker    # app logs
```

For real observability, ship container logs to CloudWatch with the
`awslogs` Docker log driver, and point an ALB/Route53 health check at
`https://api.<domain>/health`.

**Updates to secrets** — change the SSM param, then re-render `.env` (re-run the
`.env` block of the bootstrap, or edit in place) and `docker compose up -d`.

---

## 10. Hardening checklist

- [ ] `JWT_SECRET`, `POSTGRES_PASSWORD`, `SEED_ADMIN_PASSWORD` are strong and
      sourced from SSM (never in git — the repo's `.env` is git-ignored).
- [ ] `AUTH_COOKIE_SECURE=true` (set by bootstrap; required behind HTTPS).
- [ ] `APP_ENV=production`, `LOG_LEVEL=INFO`.
- [ ] Security group: SSH restricted to your `/32`; 5432/6379 never exposed.
- [ ] `CORS_ORIGINS` set to exactly `https://app.<domain>`.
- [ ] Rotate the seeded admin password after first login.
- [ ] EBS snapshot + pg_dump backups scheduled.
- [ ] IMDSv2 enforced on the instance (`--metadata-options HttpTokens=required`).

---

## 11. When to move off a single box

A single `t3.large` comfortably runs a small team. Scale when Postgres CPU or
disk I/O becomes the bottleneck, or you need HA:

| Concern | Managed replacement |
|---------|---------------------|
| Postgres durability / HA | **RDS for PostgreSQL** — set `DATABASE_URL`, drop the `postgres` service |
| Redis durability | **ElastiCache for Redis** — set `REDIS_URL`, drop the `redis` service |
| API horizontal scale | Move `api`/`worker`/`frontend` to **ECS Fargate** behind an **ALB**; keep the same images |
| Zero-downtime deploys | ECS rolling deploys + ALB health checks on `/health` |
| Secrets at scale | **Secrets Manager** (rotation) instead of SSM SecureString |

The images and env contract are identical — only the orchestration changes. Do
this migration incrementally: RDS first (biggest durability win), then
ElastiCache, then Fargate only if you actually need multi-node.

---

## 12. Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `curl https://api…/health` empty / connection refused | DNS not resolving to the Elastic IP yet, or SG missing 443. |
| Browser cert warning | Caddy couldn't complete ACME — port 80 must be open to `0.0.0.0/0`, and both A records must resolve. Check `docker compose logs caddy`. |
| Login works via API but UI 401s | `AUTH_COOKIE_SECURE` must be `true` behind HTTPS; `CORS_ORIGINS` must match the UI origin. |
| `api` never healthy | `docker compose logs migrate` — Alembic or seed failed (usually a bad `DATABASE_URL`/password). |
| LLM features return 429 | Cloud LLM account has no billing/quota — see [`.env.docker.example`](../../.env.docker.example) note on `OPENAI_API_KEY`. |
| Probe won't register | `PLATFORM_URL` must be the **HTTPS `api.` subdomain**, not `:18080`; `PROBE_NETWORK_SEGMENTS` must be non-empty. |

---

_Last updated: 2026-08-01. Deployment model: single EC2 + Compose + Caddy.
Owner: platform. See [`../README.md`](../README.md) for the docs map._
