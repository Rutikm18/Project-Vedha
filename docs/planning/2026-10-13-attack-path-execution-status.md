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

## Interface and transport checkpoint

- Engagement workspace gains an opt-in Attack paths tab and the finding detail gains an opt-in link to its specific assessment. Portal surfaces do not gain operator assessment access.
- New BFF transport forwards authenticated scoped requests, keeps permission denial distinct from session expiration, uses no-store and preserves request idempotency keys. Read-only roles cannot request computation.
- Interface presents prerequisites, missing observations, unassigned ownership and verification requirements. Failed/queued refresh stays separate from the last completed result. Model changes require reassessment; historical results are retained.
- Mobile tab labels do not compress/overlap and the tablist supports arrows/Home/End. The original branding, typography and light/dark tokens remain intact.
- Five legacy graph BFF routes no longer use the static global graph store. Their backend is live-role gated, explicitly marked partial/heuristic/not-observed, and ordinary GET never recomputes. Legacy explicit recomputation is POST `/attack-paths/refresh`; a target-specific refresh preserves other targets.
- Live user/tenant activity and role are checked on assessment/legacy graph endpoints. Pilot enablement additionally requires an explicit engagement UUID allowlist. Flag disable preserves history.
- Snapshot creation supports scoped UUID idempotency keys, including concurrent duplicate requests. Capture streams bounded evidence and refuses a pre-existing non-Repeatable-Read transaction. Rule artifacts are pinned at module load and included in proof identity/history metadata.

Recorded validation: **2,437 backend tests passed, eight skipped**, including the new local PostgreSQL integration tests; **395 frontend tests passed**. Frontend production build, full type check, targeted lint, migration upgrade/downgrade and mechanical UI detector passed. The real local browser → BFF → API → filtered outbox worker → PostgreSQL flow completed with synthetic data. Desktop/320-pixel mobile inspection and its correction/confirmation pass checked non-overlapping labels, arrow-key navigation, no horizontal overflow and dark theme. Synthetic test results do not establish organizational path accuracy or independent analyst outcomes.

## Remaining required work

Engineering continuation: record reproducible local inference/capture budgets; audit the 48-case register against implemented tests; complete snapshot comparison and actionable evidence inspection where the data contract permits it; review the complete diff and prepare the PR. A stronger raw-observation adapter must be grounded in actual payloads, not invented fields.

External gates still open: an authorized real engagement/test backend, independently reviewed expected consequences/holdouts, a supported observation-rich local case and analyst/owner shadow pilot. A concise request for engagement ID/test address is pending with the user. The repository corpus cannot fill the missing application-read/scenario/instance observations. **Do not mark positive-path activation, raw observation inference, multi-host composition or the release pilot Done from this checkpoint.** Later grouped/AD/cloud extensions remain out of the local-first release scope.

## Local continuation resources

All resources below belong to this task, not production: PostgreSQL container `vedha-attack-path-tests` on localhost 25432; Redis container `vedha-attack-path-redis-tests` on localhost 25379; backend on localhost 18081; built frontend on localhost 3114. Temporary pinned Python dependencies are `/private/tmp/vedha-local-rule-deps`. Test-only seed/session/filtered-worker/browser scripts live under `/private/tmp/vedha-attack-path-*`; do not print the private synthetic session token. Stop only these verified resources when finished. The original checkout remains separate and its unrelated changes are preserved.
