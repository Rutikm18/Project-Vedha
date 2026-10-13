# Durable finding-readiness snapshot increment

This increment adds real scoped finding assessment transport behind `ATTACK_ASSESSMENTS_ENABLED=false` by default. It uses the platform's PostgreSQL/outbox infrastructure and never returns static graph-store data.

## What is implemented

- Migration 0063 (after integrating current main through 0062) adds tenant/engagement-bound snapshot storage, monotonic request sequence and state/result constraints. A composite foreign key prevents a tenant from owning another tenant's engagement snapshot. The table matches main's dormant tenant RLS policy.
- Database triggers prevent changing the snapshot ID, source cut, input body, model versions, request sequence or creation time. Completed results are immutable. Queued/failed computation can retry without replacing its inputs.
- Capture uses a short Repeatable Read transaction. Scoped findings, assets and services are materialized into a bounded immutable input document. Ingest/capture time is not used as missing security-observation time.
- Input bounds: 1,000 findings, 2,000 assets, 5,000 services; individual finding evidence over 64 KiB is explicitly limited. The aggregate document cannot exceed 2 MiB. Omitted findings retain a total denominator and truncated qualifier; an oversized aggregate is rejected without destroying old results.
- Snapshot and outbox event are persisted in the same caller transaction. The worker reads only the stored input, verifies its content hash, computes readiness and atomically publishes one completed result. A locked row makes repeated delivery idempotent.
- Ordinary reads do not queue computation or delete results. Latest-request state and last-completed result are selected together. A late old worker cannot replace a newer completed snapshot because current-result ordering uses the monotonic request sequence.
- API access uses the operator matrix from R04 and tenant-scoped engagement lookup. Portal/client/PAT access is excluded. Normal responses and access-denied/disabled responses are marked no-store.

## API contract

| Method and path under `/engagements/{engagement_id}/attack-assessments` | Meaning |
| --- | --- |
| POST base | Capture current scoped input and enqueue a durable job; returns 202 with snapshot metadata. No caller-supplied assertion/effect is accepted. |
| GET base | Latest request and last completed snapshot, including a failed/queued refresh separate from historical results. |
| GET `/{snapshot_id}?page=1&page_size=20` | Bounded assessed-finding list, source denominator, computation and coverage qualifiers. |
| GET `/{snapshot_id}/findings/{finding_id}` | One finding's recorded prerequisites, missing evidence and next action. Unknown/not-assessed IDs return 404. |

## Evidence boundary

This transport is a **readiness assessment**, not activation of the experimental data-read rule. It maps explicit scoped service references, recognizes candidate datastore families from explicit service data, and keeps unmapped findings visible. Titles, CVSS, confirmation status, accepted risk, an open port or an unauthenticated banner cannot generate a positive proof.

Every currently transported consequence remains incomplete or not evaluated until raw facts have the source-backed observation/scenario/instance bindings required by the normalized rule. The independently tested local proof engine and typed simulation are not exposed as caller-authoritative API input. No compromise probability, observed chain or safety claim is manufactured to fill a telemetry gap.

The stored raw finding evidence is bounded and used internally for normalization; it is not returned wholesale by these API endpoints. Foreign/unresolved asset/service IDs are not presented as bound entities. A known service name is only rule-family candidacy, not finding applicability or successful data access.

## Validation

An isolated local PostgreSQL 17 container was used, bound to `127.0.0.1:25432`. All existing migrations plus 0055 upgraded successfully; 0055 downgrade/re-upgrade passed. Integration tests verify immutable inputs/completed output, scope FK, result publication constraints, older-worker ordering, snapshot/outbox persistence, real handler duplicate delivery, readonly GET, access policy, preserved old results and a concurrent source update between capture queries.

The test database is explicitly opt-in through `ATTACK_PATH_TEST_DATABASE_URL`; integration fixtures refuse URLs outside the dedicated local database/port. Core runtime and test dependencies are installed into a temporary directory with the repository's pinned versions. No production database is used.

Still pending: analyst UI/BFF integration, live payload and independent analyst validation, approved raw-observation adapters, rule activation/withdrawal workflow, post-change verification and release pilot. Existing legacy graph endpoints continue to be separate heuristic infrastructure until the later transport cleanup; these new endpoints do not adopt their path scores or movement claims.
