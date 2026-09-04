# Learning Notes

Use this file to add core technical concepts that need to be learned.
Keep each note direct, practical, append-only, and detailed only where useful.

## Writing Rules

- Add only core technical concepts: software engineering, architecture, security, backend, frontend, databases, infrastructure, algorithms, protocols, testing, or production operations.
- Do not add meta workflow notes such as Codex usage, prompt setup, file maintenance, or command mechanics unless explicitly requested as a technical topic.
- Think like an expert software engineer before writing: capture the real concept, the practical problem, and the correct usage.
- Keep each field short but useful. Prefer one or two focused sentences over vague one-liners or long explanations.

## Format

```md
## Concept Headline

**What:** Clear meaning of the concept.

**Problem:** The practical issue, risk, or confusion it solves.

**Solution:** The core idea or pattern that fixes the problem.

**When Use:** Where this concept should be applied.

**Why Use:** Why it matters in real engineering work.
```

## Notes

Add new concepts below this line. Do not delete previous notes.

---

## Append-Only Learning Notes

**What:** A notes file where new concepts are added without removing old ones.

**Problem:** Important learning points can be lost if old notes are overwritten.

**Solution:** Always append each new concept below the existing notes.

**When Use:** Use when building a personal learning history.

**Why Use:** It keeps all previous learning available for review.

## AGENTS.md Project Guidance

**What:** A repo instruction file that tells Codex how to behave in this project.

**Problem:** Repeating the same workflow rules in every prompt is slow and error-prone.

**Solution:** Store durable project rules in `AGENTS.md`.

**When Use:** Use for project-specific habits, formats, checks, and workflows.

**Why Use:** Codex reads it automatically and follows consistent rules.

## Codex Custom Prompt

**What:** A Markdown prompt saved in `~/.codex/prompts` for reuse.

**Problem:** Common tasks need the same instructions again and again.

**Solution:** Save the task as a reusable prompt file.

**When Use:** Use for repeated workflows like adding learning notes.

**Why Use:** It turns repeated instructions into a quick command.

## Slash Command Prompt

**What:** A command-style shortcut that invokes a saved Codex prompt.

**Problem:** Typing full instructions each time wastes time.

**Solution:** Use `/prompts:learning` with the concept name.

**When Use:** Use when adding a new concept to `learning.md`.

**Why Use:** It makes the learning workflow fast and consistent.

## Prompt Arguments

**What:** Extra text passed into a custom prompt.

**Problem:** A reusable prompt still needs the specific topic each time.

**Solution:** Pass the concept after the command, such as `/prompts:learning JWT`.

**When Use:** Use when the same prompt needs different input.

**Why Use:** It keeps the command reusable while changing only the topic.

## DB Connection Pool Recycling

**What:** Closing and reopening pooled DB connections after a max age (`pool_recycle`).

**Problem:** Cloud networks (AWS NAT/LB) silently drop idle TCP connections after ~350s; the next query on a dead connection throws `OperationalError`.

**Solution:** Set `pool_recycle` below the network idle timeout (e.g. 280s) so the pool refreshes connections before they go stale; add `pool_pre_ping` as a safety net.

**When Use:** Any long-lived service holding a DB connection pool behind cloud networking.

**Why Use:** Prevents random request failures minutes after traffic goes quiet.

## Connection Pool Sizing Per Worker

**What:** Each process (uvicorn worker) owns its own pool, so total DB connections = workers × (pool_size + max_overflow).

**Problem:** `pool_size=10, max_overflow=20` × 3 processes = 90 connections, near Postgres' default `max_connections=100` → exhaustion under load.

**Solution:** Keep per-process pools small (e.g. 5+5) and multiply by worker count to stay well under the DB limit.

**When Use:** Sizing any multi-process app against a shared database.

**Why Use:** Connection exhaustion looks like random hangs and 500s that are hard to trace.

## Fail-Fast Startup Diagnostics

**What:** Running dependency/config checks during app startup and aborting before accepting traffic.

**Problem:** A misconfig (e.g. insecure cookie in production) or a missing dependency lets the app serve broken responses, or crash-loops mysteriously.

**Solution:** Validate on boot; make checks fatal only when truly unrecoverable, and retry transient ones (DB not ready yet) before declaring failure.

**When Use:** Production services with hard config/dependency invariants.

**Why Use:** Turns silent runtime breakage into a clear, early, logged failure — but over-strict fatals cause crash loops, so retry transients.

## Decompression Bomb Guard

**What:** Size ceilings on both compressed input and decompressed output before inflating a request body.

**Problem:** A tiny gzip payload can expand to gigabytes, OOM-killing the process (a decompression bomb).

**Solution:** Cap accepted compressed bytes and reject if decompressed size exceeds a limit; return HTTP 413 instead of buffering it all.

**When Use:** Any endpoint that accepts `Content-Encoding: gzip` request bodies.

**Why Use:** Prevents a single crafted request from crashing the server.

## Graceful Shutdown Timeout

**What:** A window (`--timeout-graceful-shutdown`) for in-flight requests to finish after SIGTERM before the process is killed.

**Problem:** On redeploy/restart, Docker sends SIGTERM and in-flight requests are severed instantly, corrupting client state.

**Solution:** Set a graceful timeout in the server and a matching `stop_grace_period` in Compose so the orchestrator waits.

**When Use:** Any redeployable service handling non-trivial request durations.

**Why Use:** Zero-downtime-ish deploys and no truncated writes mid-request.

## Container Memory Limits vs OOM Killer

**What:** Per-container memory caps (`deploy.resources.limits.memory`).

**Problem:** Without limits, one runaway container triggers the host OOM killer, which may kill an unrelated container with no crash signal the orchestrator sees.

**Solution:** Set explicit per-service limits so an over-using container is contained and restarted cleanly; keep the sum under host RAM.

**When Use:** Multi-container hosts (Compose/Kubernetes) on fixed-size machines.

**Why Use:** Makes memory failures local, visible, and auto-recoverable.

## Cache/Store Memory Below Container Limit

**What:** An in-memory store's own max (e.g. Redis `--maxmemory`) must sit under its container memory limit.

**Problem:** If `maxmemory` > container limit, the OOM killer kills the container before the store's own eviction runs → crash loop.

**Solution:** Set the store's max to ~70% of the container limit, leaving headroom for overhead (AOF buffers, copy-on-write).

**When Use:** Running Redis/Memcached/etc. under a container memory cap.

**Why Use:** Lets the store evict gracefully instead of getting hard-killed.

## Compose Interpolates All Services

**What:** Docker Compose v2 resolves variables for every service in the file at parse time — even ones excluded by inactive profiles.

**Problem:** A `${VAR:?error}` in a profiled service (e.g. an optional DB) breaks unrelated `up` commands that never start that service.

**Solution:** Guarantee those vars are always set, or use soft defaults `${VAR:-}` for optional-profile services.

**When Use:** Any Compose file using profiles + required-variable syntax.

**Why Use:** Avoids confusing failures for services you aren't even running.

## Compose Project Dir vs Build Context

**What:** `--project-directory` changes where relative paths (build contexts) resolve, not just where `.env` is read.

**Problem:** Pointing project-dir at the repo root while the compose file lives in a subdir makes `context: ./backend` resolve to the wrong path → "path not found".

**Solution:** Load env with `--env-file` (which doesn't move the base path) and let build contexts resolve relative to the compose file's own directory.

**When Use:** Compose files nested in subdirectories with relative build contexts.

**Why Use:** Keeps builds working without moving files around.

## Idempotent Secret Generation

**What:** A bootstrap script that generates a secret only if absent, never rotating an existing one.

**Problem:** Regenerating `POSTGRES_PASSWORD` while the data volume still holds the old one causes permanent auth failure.

**Solution:** Check for an existing value (and placeholder patterns) first; only fill gaps. Warn if a fresh secret would mismatch an existing stateful volume.

**When Use:** Auto-provisioning `.env`/secrets for stateful services.

**Why Use:** Safe re-runs — the classic cause of "database auth fails after redeploy".

## IMDSv2 Token Flow

**What:** AWS instance metadata v2 requires a short-lived token (PUT) before reading metadata (GET).

**Problem:** Plain `curl http://169.254.169.254/...` (IMDSv1) returns 401 on hardened instances where IMDSv1 is disabled.

**Solution:** First PUT `/latest/api/token` with a TTL header, then send it as `X-aws-ec2-metadata-token` on the GET.

**When Use:** Reading EC2 public IP / role creds from inside an instance.

**Why Use:** Works on security-hardened instances; IMDSv1 is a known SSRF risk.

## Loopback vs All-Interfaces Port Binding

**What:** Publishing a container port on `127.0.0.1` (host-only) vs `0.0.0.0` (all interfaces).

**Problem:** `127.0.0.1:18080` is unreachable from other machines even if the firewall/security-group allows it — traffic hits the NIC, not loopback.

**Solution:** Bind to `0.0.0.0` when you want external access (rely on the security group as the firewall), or keep `127.0.0.1` when a reverse proxy fronts it.

**When Use:** Deciding whether a service is reachable off-box.

**Why Use:** Explains "connection refused from my laptop but works via SSH tunnel".
