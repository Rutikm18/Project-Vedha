# Architecture Review — scalability & system design

A staff-level audit of the platform as built. Grounded in the actual code, not
generic advice. The verdict up front: **the bones are good** — the hard,
get-it-wrong-once decisions (probe/manager split, deterministic offline
detection, stateless JWT, scope dual-enforcement, sealed probe) are already
right. What remains is **operational hardening for scale**, not a rewrite.
Do *not* "rewrite everything" — that destroys a working, tested system. Apply
the prioritized changes below in order.

---

## 1. Current architecture (as built)

```
PROBE (per client, thin)            MANAGER (cloud, multi-tenant)
 scanner_module + agent              FastAPI (async, 4 workers) ── Postgres (pool 10+20)
   scope-checked collection           │   11 routers · 19 models · BFF (Next.js)
   raw facts ──HTTPS out──────────────┤   detection_engine (offline, pinned DB)
                                       │   ad / graph / exploit / ai engines
                                       └── Redis (cache/queue substrate, present)
```

**What's already right (keep):**
- **Thin probe / fat manager** — the crown-jewel logic + vuln DB never leave the cloud.
- **Deterministic, offline detection** — reproducible, auditable, re-runnable; no live-API in the hot path.
- **Stateless auth (JWT)** — the API can scale horizontally with no sticky sessions.
- **Async FastAPI + real connection pooling** (`pool_size=10, max_overflow=20, pool_pre_ping`).
- **BFF pattern** — one backend contract, no CORS sprawl, server-side token.
- **Scope enforced at both ends**; `ot` profile structurally passive.

---

## 2. Scalability findings (prioritized, grounded in the code)

### P1 — do these first (correctness-at-scale)

| # | Finding | Where | Fix |
|---|---|---|---|
| 1 | **Detection runs INLINE in the probe-result endpoint** — `await create_findings_from_facts(...)` blocks the HTTP request while the whole `detection_engine` pipeline runs. A large facts payload stalls the probe's submit and ties up a worker. | `routers/agents.py` submit_job_result | Enqueue detection as a **background job** (Redis queue / `arq`); the endpoint just persists raw facts + returns 202. A worker runs detection and writes findings. Decouples probe throughput from analysis cost. |
| 2 | **BFF N+1** — `/api/engagements` fetches the list, then `Promise.all(ids.map(id ⇒ GET /engagements/{id}))` — one round-trip per engagement just to get counts. 100 engagements = 101 calls. | `app/api/engagements/route.ts` | Add a backend **list endpoint that returns counts** (single SQL with `GROUP BY` / subquery), so the BFF makes **one** call. |
| 3 | **Detection DB ships as a read-only volume mount**, not baked into the image. Fine for dev; in prod the image isn't self-contained and the snapshot can drift. | `docker-compose.yml` api volume | `COPY` `detection_engine` + its pinned snapshot **into** the backend image; version-stamp it. |

### P2 — before real load / many tenants

| # | Finding | Fix |
|---|---|---|
| 4 | **No rate limiting** on `/auth/login` or the API. Brute-force + abuse exposure, and a noisy tenant can starve others. | Add `slowapi` (Redis-backed) — per-IP on auth, per-tenant quotas on heavy endpoints. |
| 5 | **No caching of hot reads** (findings/engagements lists hit Postgres every time). | Cache list/aggregate responses in **Redis** with short TTL + invalidate on write. Redis is already in the stack. |
| 6 | **Poll-based job dispatch** (probe `GET /jobs` every 10s). Fine to hundreds of probes; thousands = constant baseline load + latency floor. | Add **jitter + backoff** now (cheap); move to **push** (SSE/WebSocket or a job-ready webhook) when probe count grows. |
| 7 | **Observability is logs-only** (`structlog`). No metrics/traces to find the bottleneck under load. | Add **Prometheus metrics** (request latency, queue depth, scan duration) + OpenTelemetry traces. |

### P3 — when you actually need the scale

| # | Finding | Fix |
|---|---|---|
| 8 | Single Postgres. | **Read replicas** for the read-heavy dashboard; route reads via replica DSN. Review indexes on `findings(engagement_id, severity, status)` and `scan_jobs(agent_id, status)`. |
| 9 | Per-tenant noisy-neighbor isolation. | Per-tenant rate/quota; consider partitioning `findings`/`scan_results` by `tenant_id` at high row counts. |
| 10 | Large facts payloads in `scan_jobs.result` JSONB. | Move raw facts to an append-only `scan_results` table (or object storage) keyed by job; keep `scan_jobs` lean. Enables re-detection without re-scan. |

---

## 3. Horizontal-scaling readiness (the "top 1%" lens)

The API is **already mostly stateless** (JWT, no in-process session) — so the path to scale is well-paved:

```
            ┌── API replica 1 ─┐
 LB ──┬─────┼── API replica 2 ─┼──► Postgres (primary) ──► read replicas
      │     └── API replica N ─┘            ▲
      │                                     │
      └── workers (detection / ad / ai) ◄── Redis queue ◄── API enqueues
                                            ▲
 probes ──poll/push──────────────────────────┘
```

To get there cleanly, the **one structural change that unlocks the rest** is P1-#1:
**move all heavy work (detection, AD, attack-graph, AI report) off the request path
onto a Redis-backed worker pool.** Everything else (replicas, autoscaling, caching)
becomes straightforward once the API is doing only fast, stateless request/response and
workers absorb the variable-cost analysis.

---

## 4. Functional / code-quality (scalable + proper)

- **Keep detection deterministic & offline** — it's a competitive moat; don't let "enrich live" creep into the hot path.
- **One source of truth per concept** — already enforced (scanner_module is the only scan engine; detection_engine the only detector). Maintain it; reject re-introduced duplicates in review.
- **Idempotency** — finding IDs are deterministic (good); make the result-submit endpoint idempotent on `(job_id)` so a probe retry can't double-write.
- **Backpressure** — bound the worker queue and per-tenant concurrency so one huge engagement can't monopolize workers.
- **Tests** — 222 backend unit tests + the detection precision/recall harness exist; add **load tests** (k6/Locust) targeting the result-submit + findings-list paths, the two that scale with usage.

---

## 5. The 30-day roadmap (do in this order)

1. **P1-#1** workerize detection (Redis queue + worker) — the unlock for everything.
2. **P1-#3** bake detection_engine + snapshot into the backend image.
3. **P1-#2** single-call engagements aggregate endpoint (kill the N+1).
4. **P2-#4** rate limiting on auth + per-tenant.
5. **P2-#5** Redis cache on hot reads.
6. **P2-#7** metrics + traces (so #8–#10 are data-driven, not guessed).
7. Then scale out: API replicas behind an LB, read replica, autoscale workers.

> Principle: **decouple collection (probe) from analysis (workers) from serving (API).**
> Each scales independently. That separation is already 80% built — finishing it is the
> whole game.
