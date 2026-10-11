# Failure areas and improvement areas — a system-designer review

Date: 2026-10-11 · Scope: `main` after the deep-scan (PR #15) + attack-path + hardening
merge (commit `a4cfc1d7`). This is a **follow-on** to
[`2026-10-09-system-design-review.md`](2026-10-09-system-design-review.md); it does not repeat
that review's F1–F9 / E1–E6. It does two things: (A) check which of those findings still hold
against current code, and (B) record the new failure and improvement areas this session's work
(the 65,535-port deep scan, the attack-path engine, the direct-to-`main` merge) created or exposed.

Method is unchanged: every finding cites the file it lives in; nothing is inferred from a plan.

---

## A. Status of the 2026-10-09 findings

| # | 2026-10-09 finding | Status today | Evidence |
|---|---|---|---|
| F1 | Tenant isolation is a convention, no Postgres RLS — **Critical** | **Still open, and larger.** Hand-written `tenant_id ==` filters have grown 108 → **117** across the backend; no `ROW LEVEL SECURITY` / `SET LOCAL app.tenant_id` anywhere. The attack-path endpoints added new tenant-scoped surface, each relying on a hand filter. | `grep 'tenant_id ==' manager/backend/app` = 117; no RLS in `alembic/` |
| F2 | Redis down → 500 that looks like a bug — High | **Partly fixed** (503 + `Retry-After`, fix #10). Open: Redis volume/AOF, readiness reports Redis. | `app/main.py` |
| F3 | One Postgres, no backups/PITR — High | **Open.** No backup service or replica in compose. | — |
| F4 | Safety net (reaper) shares a loop with the drainer — Medium | **Open.** | `workers/outbox.py` |
| F5 | A scanner that fails silently reports a clean network — High | **Open, and now the bigger risk** given deep scan: see NF1. Agent still swallows scanner errors instead of emitting coverage records. | — |
| F8 | No trace ID across agent → worker → detection → notify — Medium | **Open.** 0 OpenTelemetry refs. | — |
| E1 | Red CI can merge to `main` (no required checks) — High | **Open, and demonstrated this session:** a hand-resolved 6-conflict merge was fast-forwarded to `main` with GitHub Actions unable to run any job. See NF4. | this session's push |
| E4 | Files too large to change safely — Medium | **Open, and worse.** `findings/workspace.tsx` 4,509 → **4,572**; `agents.py` 1,836 → **1,874**; `report_document.py` 2,219 → **2,409**; `agent.py` 2,196 → **2,535**. None were split. | `wc -l` |

The rest of §4–§6 (F6, F7, F9, E2, E3, E5, E6) are unchanged from 2026-10-09; they were not touched
by this session's work.

One prior concern is now settled in the **good** direction, worth recording so nobody "fixes" it:
**Neo4j is correctly optional.** The attack-path engine builds and analyses the graph in memory;
Neo4j is an advisory mirror whose driver errors are swallowed on purpose
(`app/graph/neo4j_client.py:149`, `# noqa: BLE001 — the mirror is advisory`). Neo4j being down
does not fail a request. Keep it that way.

---

## B. New failure areas (this session's work)

### NF1 · Deep scan trades refusal for a 24-hour single job and silent truncation — High (operational)

The 65,535-port sweep removed Deep Port Sweep's old 3-host cap. The cap is now **0 (no cap) by
default**, and the runtime ceiling grows with the scope up to `MAX_FULL_SCAN_SECONDS` =
**24 h** (env-cappable to 7 days) (`probe/agent/engine.py:81,193,286`). This is the right call for
small scopes, but at scale it has two edges:

- **One job can own a probe for 24 h.** A Deep Port Sweep over a /24 (254 hosts × 65,535 ports ≈
  16.6 M probes) no longer gets refused — it runs until it covers the space or hits the ceiling.
  There is no obvious `max_concurrent_jobs` bound in the agent, so a single deep sweep can
  monopolise a small customer probe and starve every other engagement's scans behind it
  (head-of-line blocking — the same class of problem F4 describes on the manager).
- **Coverage truncates silently-ish.** When the ceiling is hit, the sweep stops and reports
  `filtered_unverified`. That is honest, but "Deep scan: all 65,535 ports" in the UI and "best
  effort up to 24 h on a large scope" are not the same promise, and only the probe summary carries
  the caveat today.

**Do:** (1) bound probe-side job concurrency explicitly and queue the rest, so a deep sweep cannot
starve other work; (2) surface the ceiling/coverage outcome to the operator *before* launch
("this scope will take ≈ N h; it may not finish") and in the engagement, not only in the probe
summary; (3) keep a hard upper scope guard (hosts × ports) that warns rather than refuses.

### NF2 · "All 65,535 ports" performs very differently on an unprivileged Windows agent — Medium

Wide sweeps switch to the stateless **SYN** scanner above 4,096 ports (`engine.py:_SYN_PORT_THRESHOLD`).
SYN needs root; the default scanner is unprivileged ("no raw packets, no SYN/stealth — that needs
root", `scanner/port_scanner.py:5`). On a customer **Windows** agent, which is the common case and
is not root, a full-port audit falls back to a **connect scan of 65,535 sockets per host**. PR #15's
`SIO_TCP_INITIAL_RTO` fix makes each closed port fast on Windows, but it is version-gated and
fail-safe, and STATUS still records the **Windows effect as "not yet measured."** So the headline
capability is proven on a rooted Linux probe and unproven where most agents actually run.

**Do:** measure a 65,535-port connect audit on a real Windows agent (closed-port latency with and
without the RTO opt-out) before the deep-scan capability is presented as production-ready; make the
scanner report which method it actually used so the coverage record is truthful.

### NF3 · A zero-route engagement rebuilds the whole analyzer on every attack-path read — Medium

The write-on-GET bug was fixed (a never-computed engagement computes once). But when a computed
engagement has **zero routes**, every `GET …/attack-paths` still rebuilds the analyzer and
re-runs `diagnose(...)` to produce `why_empty` (`app/routers/attack_paths.py:255-258`). That is
O(assets + findings) graph construction on every page load / poll of an engagement that, by
definition, has nothing to show — a read-amplification and latency cost that scales with the
engagements most likely to be opened repeatedly (the "why is this empty?" ones).

**Do:** store the `why_empty` diagnostics in the `AttackPathAnalysis` row at recompute time and
serve them O(1); only rebuild on explicit `refresh=true`.

### NF4 · Production `main` has no CI gate — High (process)

E1 is not theoretical any more. This session fast-forwarded a hand-resolved 6-conflict merge of a
reworked probe subsystem straight to `main`, and GitHub Actions could not run a single job to
confirm it. Local suites were run and are green, but "the author ran the tests on their branch" is
exactly the gap branch protection exists to close. Every future merge to `main` has the same
exposure.

**Do:** enable branch protection on `main` with the `backend-ci`, `agent-ci`,
`scanner-accuracy` and `frontend-ci` suites as **required** checks, and require a PR (no direct
push) for `main`. Until then, treat any direct-to-`main` change as unverified by CI and say so in
the change log (as this session did).

### NF5 · Attack-path total count loads every row to count it — Low (efficiency)

`total` is computed as `len((await db.execute(select(AttackPath.id).where(...))).all())`
(`app/routers/attack_paths.py:241-243`) — it pulls every path id into Python to take a length,
on every paged read. Fine at a handful of paths, wasteful as route counts grow.

**Do:** `select(func.count())…`.

---

## C. Improvement areas (architecture-level)

These are not bugs; they are where the design will bend next.

1. **Make coverage a first-class result, end to end (closes F5 and underwrites NF1/NF2).** The
   detection engine already emits BLIND/NO_EVIDENCE verdicts and an ingest census. The agent does
   not: it still has ~70 `except: pass` scanner blocks, so a scanner that errored and a port that
   is genuinely closed look identical in the output. For a VA product that is a false negative wearing
   a clean result. Turn every swallowed scanner error, and every ceiling-truncated sweep, into a
   coverage record that reaches the report. This is the single highest-leverage reliability change.

2. **Probe job scheduling.** Give the agent an explicit concurrency bound and a queue with fairness,
   so one long deep sweep cannot starve other engagements (NF1). Report queue depth and the
   running job's ETA.

3. **Trace IDs across the hops (F8).** Bind a job/trace id into `structlog` at agent → API →
   outbox → detection → notification now; it is cheap and it is what will answer "why is this
   finding missing?" without grepping six logs by timestamp. The attack-path engine adds a hop
   (recompute), which makes this more valuable than it was.

4. **Precompute attack-path results on ingest, not on read.** Today a route set and its `why_empty`
   are produced lazily on GET (NF3). Moving recompute to the detection/outbox path (it already runs
   per-engagement work there) makes reads O(1) and removes the write-on-read class of bug entirely.

5. **Split the god-files before the next parallel change (E4).** `findings/workspace.tsx` (4,572),
   `agent.py` (2,535), `report_document.py` (2,409), `agents.py` (1,874). The merge this session
   had to hand-resolve was painful precisely in the biggest files; the duplicate-branch bug git's
   clean auto-merge produced in `branches.py` is the same cost in miniature. Splitting by concern
   (panel / service / scanner family) pays for itself at the next merge.

6. **Defense-in-depth on tenancy (F1).** The attack-path work added more tenant-scoped endpoints,
   each guarded by one hand-written filter. Postgres RLS (`SET LOCAL app.tenant_id` per request
   txn + a policy per tenant-owned table) turns the 118th forgotten filter from a cross-tenant data
   leak into a query that returns nothing. This is the one Critical item; it should not keep
   growing while it waits.

---

## D. Suggested order

| When | Items |
|---|---|
| **Now** | NF4 branch protection on `main` (required checks + no direct push) · F1 RLS spike (the surface is still growing) · NF2 measure the Windows 65k connect audit before calling deep scan production-ready |
| **Next** | NF1 probe job concurrency + pre-launch ETA · C1 agent coverage records (also closes F5) · NF3 store `why_empty` / precompute on ingest (C4) |
| **Later** | C3 trace IDs · C5 split the god-files · NF5 count query · the remaining 2026-10-09 items (F3 backups, F4 reaper split, F6 small-host defaults) |

---

## E. Implemented 2026-10-11 (same session)

| Item | What shipped | Proof |
|---|---|---|
| **NF3** | A zero-route `GET …/attack-paths` now serves the diagnostics the last recompute already stored (`AttackPathAnalysis.analysis`) and only rebuilds the analyzer on `refresh=true` or when a pre-NF3 row stored none. No more O(assets+findings) rebuild on every poll. | `test_attack_paths_list_readonly` asserts a zero-route read neither recomputes nor rebuilds; 335 attack-path tests pass |
| **NF5** | `total` is `select(func.count())` instead of `len(select(id).all())`. | same suite |
| **F1** | Postgres RLS as defense-in-depth, **shipped dormant** (migration 0062 + `app/db_rls.py` + `get_db` GUC wiring, behind `DB_RLS_ENABLED`, off by default). Permissive when the GUC is unset, so workers/migrations are untouched; the request path sets the GUC so a forgotten `tenant_id` filter returns nothing. | live non-superuser Postgres proof (GUC=A → only A's rows unfiltered; cross-tenant write blocked; unset → all) + Postgres-gated `test_tenant_rls_postgres`; full backend **3,144 passed** with the flag off |
| **NF1 / C1** | Found **already implemented** by PR #15 + the M/A waves: the probe refuses `cannot_finish` jobs, runs `tight` ones as partials, emits a feasibility estimate + check + `not_scanned`/`filtered_unverified`; the manager ingests these as four distinct port-states (`port_coverage.py`) and exposes them. No redundant code added. Residual: a pre-launch ETA in the operator Scanner UI, and the scanner-internal `except: pass` sites (F5) — left as recorded work, not safely changeable without running real scans here. | — |

**Not codeable from here:** NF4 (branch protection on `main`) is a GitHub repo setting — enable required checks (`backend-ci`, `agent-ci`, `scanner-accuracy`, `frontend-ci`) and "require a PR" on `main`. NF2 (measure the Windows 65k connect audit) needs a real Windows agent.

**To enable F1 RLS in production:** run migration 0062, set `DB_RLS_ENABLED=true`, and ensure the app connects as a **non-superuser** Postgres role (superusers bypass RLS). Confirm first that no request-path endpoint reads across tenants on the protected tables (none does today). Extend `RLS_TENANT_TABLES` to cover findings/assets later (they need a subquery policy through `engagement_id`).
