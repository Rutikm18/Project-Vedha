# Deployment architecture review

3 October 2026 · read-only review of how the manager is deployed today, with each gap ranked by risk and backed by evidence from the repository. Nothing was changed on any server. Items marked **verified** were reproduced in this session; the rest are read from code and config.

## How it is deployed today

```
Internet ──► EC2 (one host, one AZ, public IP without an Elastic IP)
              └─ Docker Compose project "vedha"
                   Caddy (80/443, Let's Encrypt) ─► frontend (Next.js BFF :3000)
                                                  └► api (FastAPI/uvicorn :8000, also published on :18080)
                   worker (outbox + detection)   postgres 16 (volume)   redis 7 (volume, AOF)
Customer networks ──► probes / agents ──HTTPS/WSS──► api.<domain>
```

Images are built on the production host from a git checkout. Secrets live in `.env` on the host (or SSM on the `install.sh` path). There are three ways to bring this up, and they do not produce the same result:

| Path | Entry point | Ingress | `APP_ENV` | API port | Used by |
|---|---|---|---|---|---|
| A | `deploy/aws/install.sh` (`/opt/vedha`) | Caddy overlay `deploy/aws/` | forced `production` | 127.0.0.1 | the deployment guide |
| B | `make full`, then `make tls` (`/opt/Project-Vedha`) | Caddy overlay `deploy/tls/` | whatever `gen-env.sh` wrote first (usually `development`) | 127.0.0.1 after `make tls` | **production today**, per STATUS and the runbook commands |
| C | `make full` / `make aws-up` without TLS | `edge` profile, plain HTTP :80 | `development` | `0.0.0.0:18080` | testing |

## Findings

### P0: fix before the redeploy

**1. HTTPS via `make tls` can leave production in development mode, which publishes the admin password.**
- On a fresh `.env` with no TLS, `scripts/gen-env.sh` (lines 138–149) sets `APP_ENV=development`, `DEV_LOGIN_HINT=1` and `PROBE_AUTO_ENROLL=true`.
- `scripts/enable-tls.sh` then turns on Secure cookies and localhost binding, but never sets `APP_ENV` or `DEV_LOGIN_HINT`.
- Afterwards, `gen-env.sh` takes its first branch when `TLS_DOMAIN` is set and leaves both alone.
- In development mode:
  - `/api/auth/dev-hint` returns the seeded admin email and password to anyone. The login page shows them in a "TESTING" box.
  - `/docs`, `/redoc` and `/openapi.json` are public.
  - Fatal startup checks only log instead of stopping the server.
  - Unsigned agent releases are accepted (`agent_distribution.py:48`).
  - The probe site-policy key falls back to one derived from `JWT_SECRET`.
  - Logs are DEBUG level in console format.
- Check the server now:
  - `curl -s -o /dev/null -w '%{http_code}\n' https://<app-domain>/api/auth/dev-hint` must print 404.
  - `grep -E '^(APP_ENV|DEV_LOGIN_HINT|PROBE_AUTO_ENROLL)=' .env`
- **Fix:** `enable-tls.sh` sets `APP_ENV=production`, `DEV_LOGIN_HINT=0`, `PROBE_AUTO_ENROLL=false` (backed up, so rollback still works). `gen-env.sh` treats `TLS_DOMAIN` as production. The API refuses to start when a public TLS domain is configured with `APP_ENV` other than `production`. If the hint was ever served, rotate the admin password.

**2. The API believes the client address that any caller sends (verified).**
- `manager/docker-compose.yml` runs uvicorn with `--proxy-headers --forwarded-allow-ips "*"`.
- Reproduced with uvicorn 0.32.1: a direct request carrying `X-Forwarded-For: 10.1.2.3` is seen by the app as coming from `10.1.2.3`.
- Wherever port 18080 is reachable (path C publishes it on `0.0.0.0`; a security-group rule or a mistake does the rest), an attacker can:
  - start a fresh rate-limit bucket per request, which defeats the login and MFA throttles;
  - pick an address on the sign-in allowlist;
  - pass the private-range check for automatic probe enrolment;
  - write false addresses into the audit log.
- On path B the port is bound to 127.0.0.1, so only Caddy reaches it. That is safe as long as the binding holds.
- MDN: "Any security-related use of X-Forwarded-For … must only use IP addresses added by a trusted proxy." Caddy itself ignores incoming `X-Forwarded-*` by default for this reason (Caddy `reverse_proxy` docs).
- **Fix:**
  1. Give the Compose network a fixed subnet and pass only that subnet (or Caddy's address) to `--forwarded-allow-ips`.
  2. Make 127.0.0.1 the default for `API_BIND` and `FRONTEND_BIND` in the compose file, not only in the scripts.
  3. Drop the 18080 publish entirely when an ingress is present.

**3. No automated backups.**
- Postgres and the Caddy certificates live on one EBS volume in one AZ.
- `install.sh` only prints "Schedule daily EBS snapshot + pg_dump to S3" as a checklist line. No script, timer or AWS Backup plan exists in the repository.
- `.env` now also holds what the stored MFA secrets depend on: `JWT_SECRET` encrypts them (2026-10-03 change), so losing `.env` means everyone sets up two-step sign-in again.
- **Fix:**
  - a nightly `pg_dump` (custom format) to a versioned, encrypted S3 bucket with lifecycle rules;
  - an AWS Backup plan for daily EBS snapshots;
  - a copy of `.env` (or SSM) in a separate place;
  - a quarterly restore drill.
- State an RPO and RTO, for example 24 h and 4 h.

**4. Security state in Redis can be evicted.**
- Redis runs with `--maxmemory 192mb --maxmemory-policy allkeys-lru`. The same instance holds:
  - refresh-token registrations (`rt:*`, one key per token plus a per-user set);
  - login-failure lockout counters and rate-limit windows;
  - the MFA single-use and attempt markers;
  - the AI answer cache with a 7-day TTL (`AI_ANSWER_CACHE_TTL_SECONDS=604800`) and AI cooldowns.
- Under memory pressure, LRU eviction can do any of the following:
  - sign users out (a registered refresh token disappears);
  - reset brute-force lockouts;
  - reopen an MFA challenge within its five minutes.
- Redis docs and common practice: `allkeys-lru` suits a pure cache; data you cannot lose needs `noeviction`.
- **Fix:** run two Redis instances:
  - security and coordination state with `noeviction`, plus an alert on memory;
  - the AI cache with `allkeys-lru`.

  Alternatively, keep the AI cache out of Redis or cap it hard.

### P1: within the next few weeks

**5. Three deploy paths with different security defaults.**
- Paths A, B and C differ in `APP_ENV`, ingress overlay, secret source, release pinning and rollback.
- `make prod-diagnose` checks and "heals" path A's overlay (`deploy/aws/docker-compose.prod.yml`, container `vedha-caddy-1`), while production runs path B (`deploy/tls/`, service `tls`). Running it on production can start a second Caddy that competes for ports 80 and 443.
- **Fix:** pick one production path. Path A has pinned releases, SSM, rollback and forced production mode; give it `make tls`'s DNS and certificate checks. Keep path C clearly labelled as testing, and make `prod-diagnose` detect which path is in use.

**6. Images are built on the production server.**
- Each deploy compiles the backend and the Next.js app on the 4 GB host; the installer adds 4 GB of swap so the build survives.
- Consequences:
  - slow deploys and downtime while containers are recreated;
  - the box holds the build toolchain;
  - nothing scans or signs the images;
  - two servers given the same commit can produce different images.
- Base images use floating tags: `postgres:16-alpine`, `redis:7-alpine`, `caddy:2-alpine`, `ollama/ollama:latest`.
- **Fix:**
  - build both images in GitHub Actions on a tag;
  - scan them (Trivy or Grype), generate an SBOM and sign with cosign;
  - push to ECR;
  - the server only pulls by digest;
  - pin base images by digest, with Dependabot or Renovate to update them.

**7. The backend has no CI.**
- The six workflows cover the frontend, agent, probe sealing, scanner accuracy and secret scanning.
- The roughly 2,400 backend tests and the Alembic migration chain never run on a push or pull request.
- **Fix:** add a `backend-ci` workflow:
  - Postgres and Redis services;
  - `pytest`;
  - `alembic upgrade head`, then a downgrade one step and up again;
  - `ruff`;
  - `pip-audit`.
- Make it a required check alongside `frontend-ci`.

**8. One host, one zone, a public IP that changes.**
- STATUS already notes that the DNS record breaks when the instance restarts (no Elastic IP). Any host or AZ failure is a full outage.
- Every deploy recreates the containers, so users and probe WebSockets see a short outage.
- **Fix, now:** attach an Elastic IP, enable EC2 auto-recovery and add an external uptime check.
- **Fix, later:** move Postgres to RDS Multi-AZ (backups, point-in-time recovery and patching become managed), then run two app instances behind an ALB.

**9. Observability is local-only.**
- Logs use Docker's `json-file` driver; they are deleted when a container is recreated, so a deploy wipes the evidence of what happened before it.
- `/metrics` (Prometheus) is in the auth middleware's public path list and is served through `api.<domain>` to anyone. Nothing scrapes it.
- There is no alerting on errors, outbox backlog, disk, certificate renewal or AI-chain exhaustion.
- **Fix:**
  - ship logs (CloudWatch agent or Loki) with retention;
  - serve `/metrics` only on the internal network (`respond /metrics 403` in Caddy, or a separate port);
  - scrape it and alert on 5xx rate, p95 latency, outbox lag, disk use above 80 %, failed backups and certificate expiry;
  - external uptime checks on `/health` and the login page.

### P2: hardening and hygiene

| # | Gap | Evidence | Improvement |
|---|---|---|---|
| 10 | Plain-HTTP API kept after HTTPS | `enable-tls.sh` defaults to `LEGACY_HTTP=1` (`http://<ip>` proxies to the API) | Move the probes to `https://api.<domain>`, then rerun with `--no-legacy-http`; probe tokens should never cross plain HTTP |
| 11 | One secret does too many jobs | `JWT_SECRET` signs sessions, derives the MFA encryption key and recovery-code key, and is the dev fallback for the site-policy key | Separate `MFA_ENCRYPTION_KEY` with key IDs so each can be rotated on its own; keep all secrets in SSM on every path |
| 12 | Health checks that prove little | The worker check is `kill -0 1`; the frontend check probes `/api/health`, which does not exist, and falls back to the login page | Worker writes a heartbeat (Redis key or table row) checked for freshness; add `/api/health` to the frontend |
| 13 | No edge protection | Rate limits exist only in the app; no WAF or DDoS layer | Cloudflare (proxied, with origin locked to Cloudflare addresses and `trusted_proxies` set) or ALB with AWS WAF; keep WebSocket support for probes |
| 14 | Postgres untuned and capped at 512 MB | Default config, no `pg_stat_statements`, no slow-query log | Tune `shared_buffers` and `work_mem` for the host, enable `pg_stat_statements`, log queries over 500 ms, size the connection pool against `API_WORKERS` × pool size |
| 15 | HSTS `preload` on path A | Caddyfile in `install.sh` | Preload is very hard to undo and covers every subdomain; keep it only once every `*.domain` serves HTTPS |
| 16 | Host patching and access | No unattended upgrades or SSM Session Manager setup; SSH open to "your IP" | Unattended security upgrades, SSM Session Manager instead of open SSH, IMDSv2 required, EBS encryption on |
| 17 | Migrations run on every start | The `migrate` one-shot runs `alembic upgrade head` before the new API, with no pre-migration backup | Take a `pg_dump` before migrating on each deploy; keep migrations expand-then-contract so rollback stays possible |

## What is already good

- **Network and secrets:** Postgres, Redis and Neo4j are never published. Secrets are generated with `openssl rand`, written atomically with mode 600, and the Postgres password is never rotated under an existing volume.
- **Release safety on path A:** pinned and optionally signed releases, a deploy lock, health-gated promotion with automatic rollback to the previous images, and a sparse clone that keeps probe source off the server.
- **Container hardening:** the API runs as a non-root user; containers have memory limits and log rotation; Caddy disables its admin API on path A; the script CSP and security headers are in place.
- **Application-level controls:** the app's own rate limiter only believes `X-Forwarded-For` from private peers. That is the right idea, but uvicorn rewrites the peer first (finding 2).

## Suggested order

1. Check the server for finding 1 today and fix the scripts (finding 1). Lock down the forwarded-header trust (finding 2).
2. Turn on backups and a restore test (finding 3). Split Redis (finding 4). Attach an Elastic IP and an uptime check (finding 8).
3. Pick one deploy path (finding 5). Add backend CI (finding 7).
4. Images built in CI, pulled by digest (finding 6). Log shipping, metrics and alerts (finding 9).
5. P2 items. Then decide on RDS and a second app instance when customer count justifies it.

## Sources

- MDN, *X-Forwarded-For*: security-related use must rely only on addresses added by a trusted proxy.
- Uvicorn discussion #2374: `--forwarded-allow-ips=*` lets any client spoof any address.
- Caddy docs, `reverse_proxy` › Defaults: incoming `X-Forwarded-*` values are ignored unless `trusted_proxies` is set.
- Redis docs, *Key eviction*: `allkeys-lru` for caches; data you cannot lose needs `noeviction`.
