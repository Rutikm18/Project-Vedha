# System design — find, verify, decide

Use in Phase 1. The goal is not to list every pattern; it is to pick the
**simplest design that meets the requirements and the security bar**, and to
prove the claims behind that choice.

## Step 1 — Requirements first
Write them down before choosing anything:
- **Functional**: what it must do.
- **Non-functional** (put numbers on them where possible): expected scale
  (tenants, probes, assets, findings/day), latency, availability, data
  retention, consistency needs, offline/air-gapped probe operation, BFSI
  compliance constraints (data residency, audit), cost.
- **Security requirements**: from the Phase 0 threat model.
- **Constraints**: existing stack (FastAPI, async SQLAlchemy + Postgres,
  Redis, Next.js, Python probe, Docker Compose deploys), ADRs in `docs/adr/`,
  team size. Don't introduce a new datastore/broker/service unless the
  requirements can't be met without it.

## Step 2 — Generate 2–3 candidate approaches
Always include "extend what already exists" as one candidate. Typical axes:

| Decision | Options to weigh |
|---|---|
| Sync vs async work | Inline request · background task · worker queue (Redis) · scheduled job |
| Communication | Request/response REST · WebSocket push · polling · event/outbox |
| Data model | New table · column(s) on existing · JSONB · separate store (only with a clear reason) |
| Consistency | Single DB transaction · outbox + idempotent consumer · saga with compensation |
| Multi-tenancy | Row-level `tenant_id` filter (current) · Postgres RLS as defence-in-depth · schema-per-tenant |
| Caching | None · Redis with TTL + tenant-scoped keys · HTTP caching (never for tenant data on shared caches) |
| Probe ↔ manager | Probe-initiated pull (outbound-only from customer network — preferred) · manager push |
| Failure handling | Retry w/ backoff + cap · idempotency keys · dead-letter · circuit breaker |
| AI features | Deterministic core + optional LLM enrichment with fallback (ADR-0004) |

## Step 3 — Score candidates on the same criteria

| Criterion | A | B | C |
|---|---|---|---|
| Meets functional reqs | | | |
| Security (attack surface, tenancy isolation, least privilege) | | | |
| Reliability / failure modes | | | |
| Scalability to stated numbers | | | |
| Operational complexity (new infra? on-prem/air-gapped friendly?) | | | |
| Consistency with existing code & ADRs | | | |
| Effort / reversibility | | | |

Prefer designs that are: **boring, reversible, secure by default, and
consistent with the codebase.** Security beats convenience; simplicity
beats theoretical scalability you don't need yet.

## Step 4 — Verify every claim
For each claim the decision relies on, record how it was verified:
- **Code**: "the rate limiter supports per-tenant keys" → read `app/ratelimit.py`, cite file:line.
- **Framework/library behaviour**: read official docs or installed source
  (`python -c "import x, inspect; print(inspect.getsource(...))"`), or run a
  minimal experiment in the scratchpad.
- **Performance**: a quick benchmark or `EXPLAIN ANALYZE` on realistic row
  counts — not intuition. Check indexes exist for new query patterns (tenant_id first in composite indexes).
- **External facts** (standards, CVEs, versions): cite the authoritative
  source (owasp.org, cwe.mitre.org, nvd.nist.gov, vendor docs). If the network
  blocks it, say the fact is unverified.
Unverified claims must be labelled as assumptions in the plan.

## Step 5 — Record the decision
- Small change: a "Design decision" paragraph in the final report.
- Architectural change (new service/datastore, protocol change, tenancy model,
  auth model, cross-component contract): write `docs/adr/NNNN-<slug>.md` with
  Context · Decision · Alternatives considered · Consequences · Security impact.

## Design principles checklist
- Least privilege (DB roles, service accounts, container caps, API scopes).
- Defence in depth (app-level tenant filter + DB constraints/RLS + tests).
- Secure defaults; explicit opt-in for risky features.
- Separation of concerns: validation → authz → business logic → persistence.
- Idempotent, retry-safe operations for anything crossing a network.
- Backward-compatible API/protocol changes (probes in the field upgrade slowly — version-gate).
- Observability: structured logs, metrics, audit events designed with the feature.
- Data minimisation and retention defined up front.
- Migrations: reversible (`downgrade`), safe on large tables (no long locks), tested.
