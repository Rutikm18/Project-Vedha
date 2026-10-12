# Sequential attack-path delivery checkpoints

Working branch: `codex/attack-path-rule-contract`. Scope: first local, single-engagement delivery. Later organization grouping, AD/cloud rule families and incremental optimization remain independently gated extensions, not prerequisites for this release.

## Completed engineering outputs

| Correction | Output | Remaining integration/validation boundary |
| --- | --- | --- |
| R01 | Typed local bindings and fixed effect; 65 regression cases | No activation until actual evidence and rule governance permit it. |
| R02 | Executable proof/goal/completeness decision table | API must derive these states from trusted computation. |
| R03 | Immutable cut contract, canonical content identity, source/known-at checks | Database capture and completed-batch verification must supply the cut. |
| R04 | Operator role/scope policy, excluding portal/PAT projections | Endpoints, jobs and exports must enforce fresh access checks. |
| R05 | Adversarial regressions and a developer-authored independent-expression finite oracle covering 256 worlds | This is not an independently labeled human holdout; analyst review remains open. |
| R06 | Repository-source/fixture field census and explicit data-read readiness decision | Live engagement availability and analyst pilot remain external dependencies. |
| R07 | Bounded local alternatives, semantic proof identity, separate display/compute limits | Generic capability-transfer DAG is a later same-engagement breadth gate. |
| R08 | Typed authentication counterfactual preserving surviving alternatives and raw inputs | Rule withdrawal and fresh post-change verification remain integration tasks. |

## R06 field census and go/no-go

Seven committed accuracy-corpus files were inspected. Two have `nmap` provenance (2,145 facts total); five are labeled `self_regression` (17 facts). Do not combine those provenance classes into a real-world accuracy claim.

The Nmap fixtures contain target/port/status/scanner/data but no explicit observation timestamp, collector version, entry/vantage/context, service instance or application-data-read field. The self-regression set has timestamps on 17 records and protocol on eight, but also lacks explicit application-data-read and scenario/instance fields. These figures describe the checked fixture fields, not production telemetry completeness.

The first data-read rule has **no-go for real supported-path activation from this corpus**. Metadata/handshake responses and unauthenticated-service booleans cannot fill the missing proof. This does not prevent building the incomplete-result workflow, source-normalization/storage, safe snapshots, APIs and local test harness. It does prevent labeling a synthetic path as a validated organizational consequence.

The current backend `Finding` has engagement and asset fields, but no dedicated service binding; `Service` provides asset/port/protocol/exposure. `ScanResult` preserves raw records, checksum and ingest timestamps, not guaranteed per-observation scenario/time fields. New adapters must use explicit source bindings, rather than titles/IP-only matching or substituting ingest time for collection time.

## Verification checkpoint

R01–R04 combined with the existing correlation suite: 139 cases passed. R05/R07/R08 bring the combined count to 154, including one oracle test checking 256 finite worlds. Those worlds are not 256 independently observed environments. Tests use pinned core runtime dependencies installed in a temporary directory; the global environment is unchanged.

No release task is marked production-complete from these counts alone. The next slices are scoped durable snapshot storage and acquisition, asynchronous computation, real transport and the evidence-first analyst interface. Keep failures, missing data and old results visible; preserve branding/themes and existing findings.

## Durable storage/transport checkpoint

[Snapshot implementation](2026-10-13-attack-path-snapshot-implementation.md) covers immutable scoped PostgreSQL storage, coherent capture, transactional outbox, idempotent worker, atomic publication and real readiness endpoints behind a disabled-by-default flag. Migration upgrade, downgrade and re-upgrade passed in an isolated PostgreSQL database. Nine integration cases passed, including source updates between queries and the actual outbox handler's duplicate delivery. Six additional readiness cases ensure metadata never grants application-data read and unmapped findings stay visible.

The wider non-integration backend suite passed **2,422 cases**, with four skipped and 13 integration cases deselected. One pre-existing agent-expiry test used a stale hardcoded future date; its date reference was corrected without changing agent behavior. The nine new PostgreSQL/API cases were run separately and passed. The analyst interface is in progress. This checkpoint does not close supported-path activation, real-data/analyst gates or the full first-release definition of done.
