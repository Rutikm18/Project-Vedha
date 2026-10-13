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

Local inference/capture measurements, the [48-case failure audit](2026-10-13-attack-path-failure-coverage.md), and scoped snapshot comparison are now implemented. Comparison explicitly refuses incomplete/reversed/cross-scope records and never awards remediation credit for deleted findings, lifecycle edits or changed model versions. Source evidence inspection remains through the original scoped finding; readiness does not expose invented observation references. A stronger raw-observation adapter must be grounded in actual payloads, not invented fields.

External gates still open: an authorized real engagement/test backend, independently reviewed expected consequences/holdouts, a supported observation-rich local case and analyst/owner shadow pilot. A concise request for engagement ID/test address is pending with the user. The repository corpus cannot fill the missing application-read/scenario/instance observations. **Do not mark positive-path activation, raw observation inference, multi-host composition or the release pilot Done from this checkpoint.** Later grouped/AD/cloud extensions remain out of the local-first release scope.

## Local continuation resources

All resources below belong to this task, not production: PostgreSQL container `vedha-attack-path-tests` on localhost 25432; Redis container `vedha-attack-path-redis-tests` on localhost 25379. The synthetic API/filtered worker were stopped for the integration migration rebuild; earlier browser screenshots are historical synthetic verification. Temporary pinned Python dependencies are `/private/tmp/vedha-local-rule-deps`. Test-only seed/session/filtered-worker/browser scripts live under `/private/tmp/vedha-attack-path-*`; do not print the private synthetic session token. Stop only verified task resources when finished. The original checkout remains separate and its unrelated changes are preserved.

## Integration retry checkpoint

Integrated current `origin/main` at `8f9575c2` instead of publishing against the old `64051cd` base. Main introduced legacy attack-path analysis/history, stable route IDs, workspace component moves and migrations through 0062. The merged implementation preserves those changes, migrates this feature at **0063**, and applies main's dormant tenant RLS policy to the new snapshot table without modifying the historical migration's table list. Manual legacy refresh now uses POST through the browser API and BFF; GET cannot write on the first read or refresh. Target refresh preserves other targets and engagement-wide history.

Post-merge frontend: **723 tests passed**, production build, regenerated full type check and changed-module lint passed. Migration chain upgraded from empty and 0063 downgraded/re-upgraded. Backend full collection exposes two unchanged main-branch test modules importing removed `SyntheticFinding`/`auto_crown_jewel_ids` APIs (`test_capability_map.py`, `test_crown_jewels.py`); those are a disclosed baseline gate, not silently counted as passes. The feature/affected-route integration run passed **105 tests**. With those two baseline collection failures explicitly excluded, the wider suite passed **3,444 tests**, nine skipped and 51 warnings. This is not an unqualified full-suite pass. Changed comparison/benchmark modules passed current main's Ruff rules.

## Backlog disposition

“Local contract” means synthetic pure engine behavior is tested; it does not mean production observation inference is activated. Later transfer/map/grouping gates remain separate from the local readiness PR.

| Tasks | Delivered | Still required |
| --- | --- | --- |
| T01 | Single-engagement experimental scope and exclusions | Scope governance review |
| T02 | Repository source/fixture census | Representative sanitized live payloads |
| T03 | Datastore data-read candidate with explicit no-go | Observation-rich supported class approval |
| T04–T05 | Typed entry/goal/privilege/status contracts | Independent contract approval |
| T06 | Synthetic golden/adversarial cases and finite developer oracle | Independent labels and held-out real examples |
| T07–T09 | Scoped immutable readiness storage, explicit ID binding, input manifest | Persisted normalized observation/assertion lineage and collector adapter |
| T10 | Local lifecycle eligibility | Verified source adjudication/withdrawal integration |
| T11–T12 | Missing reachability/read coverage retained | Authorized real reachability normalization and completed-batch manifest |
| T13–T15 | Fixed versioned experimental local rule and AND checks | Reviewed activation and production adapter |
| T16–T17a | Local alternatives, conflict/freshness checks | Live observation validation |
| T17b–T18 | Incompatible scenarios rejected | Capability-transfer composition deferred to breadth gate |
| T19a–T20a | Canonical local proof and measured bounded compute/display | Production cancellation/concurrency capacity |
| T19b–T20b | No composed output claimed | Composed proof/frontier/cycle stress gate |
| T21–T24 | Sealed RR capture, durable outbox, retries, atomic history, stale failure preservation | Operational deployment review |
| T25 | Immutable history and local withdrawal regressions | Live source removal/alternate-source recomputation |
| T26–T29 | Live-role scoped endpoints, real BFF, no demo fallback | Restricted export design remains excluded |
| T30–T33 | Finding link, text prerequisites, gaps, scoped detail lookup | Supported proof/raw observation workflow after adapter activation |
| T34/T35b | Map omitted from text-first local release | Optional equivalent map breadth gate |
| T35a | Responsive text UI, keyboard navigation, light/dark and adverse states | Broader assistive-tech and analyst task study |
| T36–T38 | Typed authentication counterfactual, surviving alternatives, simulated-only outputs | Operational feasibility/owner constraints and real evidence |
| T39–T40 | Visible owner/unassigned state, verification requirements, honest snapshot comparison | Actual owner handoff and fresh comparable verification |
| T41 | 48-case coverage audit plus regression suite | Independent holdouts and baseline suite repair |
| T42 | Reproducible local inference/capture measurements | Production concurrency, cancellation and composed stress |
| T43 | Disabled flag plus explicit engagement allowlist | Analyst/owner shadow pilot |
| T44 | Local migration rollback and enablement boundaries | Reviewed release/rollback rehearsal with real data |
| X01–X08 | No organization/AD/cloud/incremental claims | Independent later extension gates |
