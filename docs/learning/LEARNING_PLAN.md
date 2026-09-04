# Vedha — 6-Week "Build It Without AI" Learning Plan

> Goal: understand every core concept in this project and be able to **build the technical
> parts unaided**. Method: **build a parallel mini-clone ("MiniVedha") from zero**, one
> vertical slice per week, then diff your build against the real Vedha module.

## Your profile (drives this plan)

| | |
|---|---|
| **Baseline** | Strong on security; weak on **backend / async Python** → we front-load that. |
| **Time** | Intensive, ~20+ hrs/week, **6 weeks** (~120–140 hrs total). |
| **Method** | Build a parallel **mini-clone from zero**, then compare to real code. |
| **Depth focus** | Probe/scanning · Backend + distributed systems · Offensive security + AI/ML. **Code & engineering over security theory** (you already know the security). |
| **Lighter** | Detection engine = solid but not deep. Frontend = optional stretch. |

**How to read a week:** each week has `Concepts & drills` (learn the gap) → `BUILD` (the
MiniVedha slice you write from a blank file) → `Compare to Vedha` (the real files to study
*after* you build) → `Resources` → `✅ Done gate` (checkboxes) → `🚫 No-AI gate` (prove you
internalized it). Check the boxes as you go.

---

## The north star: what "MiniVedha" is by end of Week 6

A working, dial-out-only **probe** that async-scans an authorized CIDR and ships **raw facts**
(never CVEs) to a **manager** (FastAPI + Postgres) over HTTP/WebSocket with durable
at-least-once delivery; the manager runs a **detection pipeline** (facts → CVE findings, ranked
by CVSS/KEV/EPSS), an **AI report + ML prioritizer**, an **attack-path graph**, and a
**safety-gated exploit orchestrator** — all runnable via `docker-compose up`. It mirrors the
real Vedha two-deployable design (thin probe / fat manager, vuln DB only on the manager).

---

## Global setup (do this before Week 1)

- Build MiniVedha in a **sibling repo** so you never touch Vedha's code:
  `mkdir ~/minivedha && cd ~/minivedha && git init` — commit at every ✅ Done gate.
- Tools: Python 3.10+, Docker + docker-compose, Postgres (via Docker), `nmap`/`masscan`
  (optional), an Anthropic API key for Week 5 (you already have one in `.env`).
- Keep Vedha open in a second window for the `Compare to Vedha` step. **Read Vedha's code
  only after you've attempted the build** — comparing beats copying.
- Read once, now, for the mental model: `ARCHITECTURE.md`, `README.md`.

---

## Concept inventory (the full map — tracks 0–7)

You'll touch all of these; the plan orders them weak-skill-first.

- **T0 Foundations:** async Python (`asyncio`, bounded concurrency, timeouts, cancellation),
  stdlib `socket`/`ssl`/`struct`, `ipaddress`/CIDR, JWT, bcrypt, Docker/compose, Makefile.
- **T1 Probe:** TCP/UDP scanning, banner grabbing, the 13 protocol scanners, host discovery,
  IT/IoT/OT profiles, `ScopeGuard`, workflow engine (bounded fan-out, failure isolation,
  gates, routing, caching), `ScanResult` schema, agent transport, durable result spool.
- **T2 Backend:** FastAPI, Pydantic v2, async SQLAlchemy 2.0 + asyncpg + Postgres, Alembic,
  multi-tenancy, JWT/PAT auth, Redis queue, rate limiting.
- **T3 Detection:** ingest→Asset, CPE normalization, dpkg-accurate version-range matching
  (epoch/backport), pinned vuln DB, CVSS/KEV/EPSS enrichment, correlate/dedup/suppress,
  verifier (confidence, anti-FP), N-run consistency (Wilson CI).
- **T4 Distributed systems:** register/heartbeat/poll/atomic-claim/submit lifecycle,
  HTTP + WebSocket transport, outbox pattern, reaper/reconciliation, idempotency, dual scope
  enforcement.
- **T5 Offensive modules:** AD (LDAP enum, Kerberoast, AS-REP, ADCS, NTLM relay, BloodHound),
  exploit orchestration (Metasploit RPC, Nuclei, safety gating), attack-path graph
  (NetworkX/Neo4j).
- **T6 AI/ML:** LLM reporting (Anthropic SDK), hallucination guardrails, ML risk scoring
  (scikit-learn/XGBoost/SHAP), the "AI never emits a CVE" pattern.
- **T7 Infra/ops:** multi-service Docker images, compose, Makefile, TLS/reverse proxy,
  Postgres volumes/backups, secrets, structlog observability.

---

# Week 1 — Async Python + the socket-level probe core

**Theme:** kill the async/backend gap first, on ground you find intuitive (scanning).

**Concepts & drills**
- `asyncio` event loop; `async def`/`await`; `asyncio.gather`; **bounded concurrency** with
  `asyncio.Semaphore`; `asyncio.wait_for` timeouts; task cancellation. Drill: sweep 1000 ports
  concurrently but never more than N sockets open at once.
- stdlib `socket` (TCP connect, `settimeout`), `ssl` (wrap a socket, read a cert),
  `ipaddress` (CIDR membership → the basis of scope).
- Dataclasses for a typed `ScanResult` (scanner, target, port, proto, status, data, evidence,
  timestamp).

**BUILD — `miniprobe` v0**
- Async TCP connect scanner + banner grab over a `ScopeGuard` that refuses any target outside
  an allowlist **before** the socket opens.
- One protocol scanner (TLS: connect, grab cert + accepted versions).
- Emit `ScanResult` dicts as JSONL. CLI: `miniprobe scan 127.0.0.1/32 --scope 127.0.0.0/8`.

**Compare to Vedha** — `probe/scanner/scanner_base.py` (ScanResult, BaseScanner, ScopeGuard),
`port_scanner.py`, `service_banner.py`, `tls_scanner.py`, `host_discovery.py`.

**Resources** — Python `asyncio` docs (Coroutines & Tasks); Python `socket` HOWTO; Beej's Guide
to Network Programming (concepts only); Python `ssl` module docs.

**✅ Done gate**
- [ ] Concurrent scan of a /28 completes with a hard concurrency cap and per-socket timeout.
- [ ] Out-of-scope target is refused before any packet leaves.
- [ ] Output is valid `ScanResult` JSONL with a TLS cert captured.

**🚫 No-AI gate** — from a blank file, rewrite the semaphore-bounded scanner + ScopeGuard in
under 40 min without references.

---

# Week 2 — Workflow engine, more scanners, durable spool

**Theme:** turn a pile of scanners into a **bounded, fail-isolated pipeline** — the core probe
engineering pattern.

**Concepts & drills**
- Per-target sequencing; **bounded host fan-out**; **per-target failure isolation** (one
  scanner/host crashing must not sink the run); structured telemetry (`scanner_runs`:
  completed/cached/skipped/degraded/failed; `issues` with stable error codes + retryable).
- Dynamic **routing/gates** (only run the TLS scanner if 443 is open); result **caching**.
- IT/IoT/OT **profiles** (port sets + rate/passivity). OT = structurally passive-only.
- **Atomic file spool**: write to `tmp` + `os.replace` (atomic rename) so a crash never leaves
  a half-written fact file. This is the foundation for Week 4 durable delivery.

**BUILD — `miniprobe` v1**
- Workflow engine that runs N scanners per target, isolates failures, caps host fan-out, and
  produces `scanner_runs` + `issues` telemetry alongside `facts`.
- Add 2 more scanners (SMB or SNMP, and a web method/`OPTIONS` scanner).
- Add profiles (`it`/`iot`/`ot`) that change port sets and disable active scans for `ot`.
- Write facts to an atomic on-disk **spool** dir.

**Compare to Vedha** — `probe/workflow/workflow_engine.py`, `execution.py`, `gates.py`,
`router.py`, `modes.py`, `cache.py`; `probe/agent/result_spool.py`; `probe/scanner/smb_scanner.py`,
`snmp_scanner.py`, `web_scanner.py`.

**Resources** — `asyncio` exceptions/cancellation; `os.replace` atomicity notes; a short read
on "crash-only / atomic write" file patterns.

**✅ Done gate**
- [ ] Killing one scanner mid-run yields a `degraded` run, not a crash; other facts survive.
- [ ] `ot` profile emits zero active-scan packets.
- [ ] Facts land in the spool via atomic rename (verify: no partial files after a kill -9).

**🚫 No-AI gate** — explain aloud why `os.replace` is atomic but `open(...).write()` isn't, and
where that matters for at-least-once delivery.

---

# Week 3 — The Manager backend (FastAPI + async SQLAlchemy + Postgres)  ← biggest week

**Theme:** your weakest area, most hours. Build the fat manager: API + real database + auth +
multi-tenancy.

**Concepts & drills**
- FastAPI: routers, path/query/body params, **Pydantic v2** request/response schemas,
  **dependency injection** (`Depends`), OpenAPI at `/docs`.
- **Async SQLAlchemy 2.0** + `asyncpg`: async engine/session, declarative models, `select()`,
  relationships; **Alembic** migration to create the schema.
- Auth: password login → **JWT** (PyJWT), bcrypt hashing (passlib), then **PAT** (hashed token,
  scoped). **Multi-tenancy**: every query filtered by `tenant_id` (the isolation boundary).
- Rate limiting basics.

**BUILD — `minimanager` v0**
- FastAPI app + Postgres (Docker). Models: `tenant`, `user`, `agent`, `engagement`
  (`scope_cidrs`), `scan_job`, `finding`. Alembic migration to create them.
- Endpoints: `POST /auth/login` (→ JWT), `POST /engagements`, `POST /agents/jobs` (enqueue,
  refuse targets outside `scope_cidrs`), `GET /findings?engagement_id=`.
- All reads/writes tenant-scoped; PAT accepted as an alternative to JWT.

**Compare to Vedha** — `manager/backend/app/main.py`, `config.py`, `database.py`,
`dependencies.py`; `routers/engagements.py`, `routers/agents.py`, `routers/findings.py`;
`models/` (engagement, scan_job, finding, tenant, user, personal_access_token); `app/auth/`.

**Resources** — FastAPI official tutorial (esp. Dependencies + Security); SQLAlchemy 2.0 async
ORM docs; Alembic tutorial; PyJWT + passlib[bcrypt] docs. (Use context7 for current API syntax.)

**✅ Done gate**
- [ ] Login returns a JWT; a protected route rejects a missing/invalid token.
- [ ] Creating a job with an out-of-scope target is refused by the API (server-side).
- [ ] Two tenants cannot see each other's engagements/findings.
- [ ] Alembic `upgrade head` builds the schema from empty.

**🚫 No-AI gate** — from scratch, wire a new tenant-scoped `GET /assets` endpoint (model → schema
→ router → dependency) in one sitting without copying an existing one.

---

# Week 4 — Distributed systems: transport, dispatch, durable delivery, reliability

**Theme:** the heart of what you asked for. Wire probe ↔ manager with the reliability patterns
that make it production-grade.

**Concepts & drills**
- Agent lifecycle: **register → heartbeat → poll → atomic claim → scan → submit**. Why
  **atomic claim** (two probes must never run the same job): `SELECT ... FOR UPDATE SKIP LOCKED`
  or a compare-and-set status update.
- HTTP polling first, then **WebSocket** job offers (execute only after the claim is confirmed).
- **At-least-once + idempotency**: probe spools before sending, retries on failure, manager
  **acks**, probe deletes only after ack; manager **dedups** on resubmit (idempotency key).
- **Outbox pattern**: manager writes side-effects to an `outbox` table in the same txn, a worker
  drains it — so an event is never lost between DB commit and downstream action.
- **Reaper/reconciliation**: a worker that re-queues jobs stuck `claimed` past a deadline.
- **Dual scope enforcement**: manager refuses to dispatch out-of-scope **and** probe refuses to
  scan out-of-scope — defense in depth.

**BUILD — connect `miniprobe` ↔ `minimanager`**
- Probe: register, heartbeat, poll `GET /agents/{id}/jobs`, run workflow, submit result to
  `POST /agents/{id}/jobs/{job_id}/result`; spool + retry + delete-on-ack.
- Manager: Redis (or Postgres) job queue, atomic claim, `outbox` table + drain worker, a reaper
  that re-queues stale jobs, idempotent result ingest.
- Prove end-to-end: enqueue → probe scans → facts persisted; kill the probe mid-submit and show
  the fact still arrives exactly once on restart.

**Compare to Vedha** — `probe/agent/agent.py`, `transport.py`, `task_runner.py`,
`result_spool.py`; `manager/backend/app/routers/agents.py`, `routers/agent_ws.py`,
`workers/outbox.py`, `workers/reaper.py`, `models/outbox.py`, `models/scan_job.py`.

**Resources** — microservices.io **Transactional Outbox**; "at-least-once vs exactly-once" +
idempotency (DDIA ch. 8–9 concepts); Postgres `SKIP LOCKED` docs; `websockets` library docs.

**✅ Done gate**
- [ ] Two probes racing for one job: exactly one runs it (atomic claim proven).
- [ ] Probe killed mid-submit → fact arrives **exactly once** after restart (idempotent ingest).
- [ ] A job artificially stuck `claimed` gets re-queued by the reaper.
- [ ] Out-of-scope target is refused at **both** manager and probe.

**🚫 No-AI gate** — whiteboard the full "enqueue → claim → scan → submit → ack → detect" sequence
and name the failure each reliability mechanism (spool, ack, outbox, reaper, idempotency key)
prevents.

---

# Week 5 — Detection engine + AI/ML prioritization

**Theme:** facts → real findings, then the AI/ML layer. Detection is lighter depth; spend the
saved time on the ML engineering.

**Concepts & drills**
- Pipeline: ingest facts → **Asset**; **CPE normalization** (product/version → CPE 2.3);
  **version-range matching** — the hard part: **dpkg-accurate compare** with epoch (`1:2.3`) and
  **backport** traps (`2.3-1ubuntu0.1`). Pinned **vuln DB** snapshot (small JSON is fine).
- Enrichment: **CVSS** (base score/vector), **KEV** (CISA actively-exploited flag), **EPSS**
  (exploitation probability). Correlate: dedup, suppress, composite.
- **Verifier**: attach a calibrated `confidence` + `evidence_reason`; it only ever *lowers*
  certainty (anti-false-positive). Optional: N-run consistency with **Wilson CI**.
- **AI/ML**: LLM report via **Anthropic SDK** with a **hallucination guardrail** — the AI writes
  prose but **never invents a CVE**; every CVE it mentions must exist in the findings. ML
  **prioritizer**: start with a transparent weighted score (CVSS×KEV×EPSS×asset-criticality),
  then upgrade to a scikit-learn/XGBoost model with **SHAP** to explain rankings.

**BUILD — `minimanager` detection + AI**
- Detection module: facts → CPEs → range-match against a small pinned DB → enrich (mock or real
  CVSS/KEV/EPSS lookups) → dedup → verify → persist `findings`.
- LLM report endpoint that summarizes findings with the "no invented CVE" guard enforced in code.
- Prioritizer that ranks findings; print SHAP/weight contributions per finding.

**Compare to Vedha** — `manager/detection_engine/pipeline.py`, `ingest.py`, `cpe_normalizer.py`,
`version_compare.py`, `matcher.py`, `enrichment.py`, `verifier.py`, `correlate.py`,
`consistency.py`, `vuln_db.py`; `manager/backend/app/ai/llm_report.py`, `hallucination.py`,
`prioritizer.py`.

**Resources** — NVD CPE 2.3 spec; FIRST **CVSS** spec; CISA **KEV** catalog; FIRST **EPSS**;
Debian **dpkg version comparison** algorithm; Anthropic SDK docs (use context7); SHAP docs.

**✅ Done gate**
- [ ] `2.3-1ubuntu0.1` vs `2.3-1` and an epoch case both compare correctly (write the tests).
- [ ] A fact matches a pinned CVE and persists a finding with CVSS/KEV/EPSS + confidence.
- [ ] The LLM report is **rejected/regenerated** if it names a CVE not in the findings set.
- [ ] Prioritizer explains *why* the top finding ranks first.

**🚫 No-AI gate** — implement dpkg version compare from the spec, from scratch, passing your own
epoch + backport test cases.

---

# Week 6 — Offensive modules, attack graph + production packaging

**Theme:** you know the attacks — build them as **software** (orchestration, safety gating, graph
algorithms), then ship the whole stack.

**Concepts & drills**
- **Attack-path graph:** model assets + findings as a graph in **NetworkX**; nodes = hosts/creds,
  edges = "can reach / can exploit"; compute **attack chains / shortest path** to a crown-jewel
  target. (Neo4j optional — the concept is graph modeling + traversal.)
- **Exploit orchestration + safety:** the important pattern is the **safety gate** — an
  approval/allowlist layer that blocks any exploit that isn't explicitly authorized (dry-run by
  default, human approval required, scope re-checked). Wrap a **Metasploit RPC**/**Nuclei** client
  interface; you can mock the actual calls — the engineering is the gating and orchestration.
- **AD orchestration (engineering focus):** build the orchestrator + module interface for LDAP
  enum + one roast (Kerberoast/AS-REP) as pluggable steps feeding findings; mock the network
  calls since you know the protocol semantics.
- **Production packaging:** Dockerfile for probe and manager, `docker-compose.yml` (postgres +
  redis + api + probe), a `Makefile` (`up`/`down`/`ps`/`logs`), TLS-in-front note, Postgres volume.

**BUILD — finish MiniVedha**
- Attack graph built from your findings; render/print the top attack path.
- Exploit orchestrator with a working **safety gate** that refuses unapproved/out-of-scope runs.
- AD orchestrator skeleton with 2 pluggable modules producing findings.
- `docker-compose up` brings up the whole MiniVedha stack; `make up`/`make ps` work.

**Compare to Vedha** — `manager/backend/app/graph/builder.py`, `analyzer.py`, `neo4j_client.py`;
`app/exploit/orchestrator.py`, `safety.py`, `msf_client.py`, `nuclei_exploit.py`;
`app/ad/orchestrator.py`, `ldap_enum.py`, `kerberoast.py`, `asreproast.py`; root
`docker-compose.yml`, `Makefile`.

**Resources** — NetworkX tutorial (shortest paths, DiGraph); Metasploit RPC (msgrpc) docs; Nuclei
docs; BloodHound attack-path concepts (you know these — skim); docker-compose + multi-stage
Dockerfile docs.

**✅ Done gate**
- [ ] Attack graph computes a multi-hop path from a foothold to a target asset.
- [ ] Safety gate blocks an exploit that lacks approval or is out-of-scope; allows an approved one.
- [ ] `docker-compose up` runs probe + manager + postgres; an end-to-end scan produces findings
      in the DB through the containers.

**🚫 No-AI gate** — design and defend the safety-gate state machine (states, transitions, who can
approve, what's re-checked) on a whiteboard without notes.

---

## Optional stretch (only if ahead) — Frontend dashboard

A single Next.js page that lists findings (Priority Queue) via a **BFF proxy** to your manager,
with JWT in an httpOnly cookie and one Recharts chart. Compare to `manager/frontend/app/`,
`middleware.ts`, `lib/`, and the findings pages. Deprioritized on purpose — it's not on your
critical path to "build the tech unaided."

---

## Mastery rubric — how you'll know you can build it without AI

For each track, you can build unaided when you can, **from a blank file, no references, no AI**:

- **Probe:** write a bounded async scanner + ScopeGuard, and explain failure-isolation telemetry.
- **Backend:** stand up a tenant-scoped FastAPI + async-SQLAlchemy endpoint with JWT/PAT auth.
- **Distributed systems:** implement atomic job claim + idempotent at-least-once ingest, and name
  which failure each of spool/ack/outbox/reaper/idempotency prevents.
- **Detection:** implement dpkg version compare and range-match a fact to a CVE with enrichment.
- **AI/ML:** enforce the "no invented CVE" guardrail in code and explain a prioritizer's ranking.
- **Offensive/graph:** compute an attack path and design an exploit safety gate.

Each week's **🚫 No-AI gate** is the checkpoint. Don't advance until you pass it.

---

## Progress tracker

- [ ] Week 1 — Async + socket probe core
- [ ] Week 2 — Workflow engine + spool
- [ ] Week 3 — FastAPI + async SQLAlchemy + auth
- [ ] Week 4 — Transport + durable delivery + reliability
- [ ] Week 5 — Detection engine + AI/ML
- [ ] Week 6 — Offensive modules + graph + packaging
- [ ] Stretch — Frontend dashboard

_Log daily wins/blockers in your `minivedha` repo commits. Add hard-won concepts to Vedha's
`learning.md` (the append-only notes file) as you go._
