# Attack-path failure coverage and release gates

Scope: the experimental single-engagement readiness workflow and its pure local rule contract. The existing platform's broader legacy graph remains a separate modeled heuristic. Passing local tests does not validate that graph, a collector adapter or organizational consequences.

Evidence keys below refer to `manager/backend/tests/`: **Rule** = `test_local_attack_path_rule.py`; **Alternatives** = `test_local_attack_path_assessment.py`; **Manifest** = `test_attack_path_input_manifest.py`; **State** = `test_attack_path_assessment_state.py`; **API** = `test_attack_assessment_api.py`; **Storage** = `test_attack_assessment_storage.py`; **Comparison** = `test_attack_snapshot_comparison.py`; **Legacy** = `test_legacy_attack_path_transport.py`. Frontend checks refer to `manager/frontend/tests` and the recorded local browser inspection.

“Excluded” means the new workflow cannot emit the relevant conclusion; it is not a test of an unimplemented feature. “Open” remains a release gate. The failure identifiers retain the research register's numbering.

| Failure | Current evidence or boundary | Status |
| --- | --- | --- |
| F01 Wrong listener/version | Rule checks listener identity/instance/port; no version-dependent exploit rule activated | Local regression; version exploit excluded |
| F02 Reused-IP merge | Rule rejects asset/service mismatch; readiness uses explicit scoped IDs | Local regression; live identity census open |
| F03 CVSS as probability | New readiness output has no success probability or ranking score | Excluded by output contract |
| F04 Reachability as control | Both reachability and explicit application-read observations required | Local regression |
| F05 Exposure as initial compromise | Fixed external unauthenticated entry; no host foothold effect | Local regression |
| F06 Missing AND condition | Each premise removed/unknown/false/conflicted in Rule | Local regression |
| F07 Mixed principals | Subject/context mismatches rejected; no identity-transfer rule | Local regression; transfer excluded |
| F08 Local to domain privilege | Fixed service-data-read-only effect; caller effects rejected | Local regression |
| F09 Account name as credentials | No credential adapter/control edge in new engine | Excluded |
| F10 Exclusive scenarios combined | Alternatives rejects incompatible actor/scenario/asset/as-of | Local regression |
| F11 Missing control as disabled | Unknown premise cannot support rule | Local regression |
| F12 Dependency as movement | No business-dependency transfer rule | Excluded |
| F13 Ingest time as freshness | Manifest rejects unknown/later source revisions; readiness names absent observation time | Local regression; raw adapter open |
| F14 Non-overlapping validity | Every premise's evidence interval must contain as-of | Local regression |
| F15 Capability retention | No temporal planning semantics | Excluded |
| F16 Duplicate corroboration | Duplicate IDs/references rejected; alternatives deduplicates canonical inputs/proofs | Local regression |
| F17 Conflict overwritten | Conflicted premise cannot support positive rule | Local regression; source adjudication open |
| F18 Accepted risk treated fixed | Rule allows accepted finding while technical premises remain | Local regression |
| F19 Withdrawal leaves current support | Remediated/FP input rejected by Rule; frozen history retained | Local regression; verified live withdrawal open |
| F20 One support removes all | Authentication simulation preserves independent listener alternative | Local regression |
| F21 Rule change rewrites history | Storage immutability; digest/version metadata; reassessment qualifier; Comparison flags model change | Regression |
| F22 Partial collection as all-clear | State decision table; partial/not-normalized coverage and zero proofs never imply safety | Regression |
| F23 LLM FP as false fact | No generated-text adjudication input to inference | Excluded; human review open |
| F24 Attempt as effect | Metadata rejected; explicit read-operation reference required; no observed-chain claim | Local regression |
| F25 Demo output in engagement | Real BFF routes, status propagation, synthetic browser→API→worker→DB check | Integration; real-data pilot open |
| F26 Schema-valid invalid semantics | Rule checks scope/bindings/types/references beyond JSON parsing | Local regression; import adapter open |
| F27 Cache/scope join | Composite FK; tenant/engagement lookup; fresh operator access; no-store scoped UI keys | Integration |
| F28 GET erases other goals | Legacy GET rejects refresh; explicit targeted POST preserves unrelated rows | Integration |
| F29 Old job becomes latest | Storage/API select monotonic request sequence, separate latest request/last completion | Integration |
| F30 Retry duplicates | Duplicate worker delivery and concurrent idempotency keys | Integration |
| F31 Stale Neo4j projection | New readiness derives only from sealed PostgreSQL input | Excluded from new workflow |
| F32 Enumeration exhausts memory | 10,000 input cap, 1,000 default applications, 20 displayed; measured local allocations | Local budget; composed graph stress open |
| F33 Limit becomes no path | Alternatives reports truncation independently of supported proofs; State preserves indeterminate | Local regression |
| F34 Representations disagree | Typed local proof round-trip; UI consumes API record; no map/export in readiness | Regression; map/export excluded |
| F35 Partial publication | Transactional snapshot/outbox; completed-result constraint; immutable results; failed refresh keeps prior completion | Integration |
| F36 Source deletion retracts others | Alternatives preserves distinct support; no multi-source normalization/withdrawal adapter | Partial; live source withdrawal open |
| F37 Top-K as universal cut | Display limit independent of compute; no universal chokepoint claim in readiness | Local regression; cut optimization excluded |
| F38 Impossible action | Typed authentication action is simulation only; no operational feasibility/approval integration | Open operational action gate |
| F39 Simulation as verified fix | Simulated-only contract; Comparison always inconclusive for readiness/remediation | Regression |
| F40 Hops inflate ranking | New readiness has no hop/CVSS priority formula | Excluded |
| F41 Canvas hides missing premise | Text-first prerequisite list includes service instance, entry, read and validity gaps | Browser inspection; analyst task study open |
| F42 Color/hover alone | Explicit text, keyboard tab navigation, mobile/no-overflow, light/dark inspection | Browser inspection; broader assistive-tech review open |
| F43 Counts imply completeness | Captured total denominator, assessed count, partial coverage, truncation qualifiers | Integration |
| F44 No owner or verification | Explicit unassigned owner and fresh same-context verification requirement | UI inspection; owner handoff pilot open |
| F45 Invented generated explanation | Deterministic rule/readiness text; no LLM explanation channel | Excluded |
| F46 Content changes authorization | Source text never selects policy, rule activation or code; titles not used for applicability | Structural boundary; collector injection review open |
| F47 Restricted disclosure/reassurance | Portal/PAT denied; live demotion/disable/tenant disable; scoped IDs and finding lookup | Integration; export excluded |
| F48 Feedback changes global rule | No feedback-to-rule activation path; experimental rule stays unactivated | Excluded; governance review open |

## Measured local budgets

Reproduce from `manager/backend` with the project's Python dependencies: `PYTHONPATH=. python scripts/benchmark_attack_readiness.py`. For capture measurements, set `ATTACK_PATH_TEST_DATABASE_URL` to the isolated localhost database on port 25432 named `attack_path_test`; the script refuses any other database and deletes only its own synthetic tenant.

Three samples on macOS arm64, Python 3.13.7, PostgreSQL 17. `tracemalloc` reports Python allocations during evaluation, excluding prebuilt inputs; it is **not process RSS**, database memory, network latency or concurrent-production capacity.

| Synthetic workload | Median | Peak measured Python allocations | Outcome |
| --- | --- | --- | --- |
| 10 distinct local bundles | 0.0054 s | 79,416 bytes | Complete, 10 proofs |
| 100 distinct bundles | 0.0502 s | 699,471 bytes | Complete, 20 displayed |
| 1,000 distinct bundles | 0.5164 s | 6,690,029 bytes | Complete, 20 displayed |
| 10,000 distinct bundles, default application cap | 0.5085 s | 6,730,156 bytes | Truncated, 1,000 supported proofs retained |
| 10,000 references to one immutable bundle | 0.0089 s | 93,062 bytes | Complete, one proof |
| Capture 1,000 database findings | 0.1600 s | 5,852,762 bytes | Sealed scoped input |
| Readiness for those 1,000 findings | 0.0288 s | 1,872,412 bytes | Zero supported proofs; missing observations visible |

Repeated-object serialization initially took 6.0689 seconds; per-evaluation identity caching removed that work without changing semantic deduplication. Distinct equivalent objects still require canonicalization. The synthetic positive bundles reuse fixture observations and do not represent independent real-world evidence.

Limits remain 1,000 captured findings, 2,000 assets, 5,000 services, 64 KiB per finding evidence and 2 MiB aggregate input. Larger evidence becomes an explicit missing-input condition; aggregate overrun refuses capture and preserves previous completion. Broader concurrency, database sizing, cancellation/timeouts and composed graph stress remain release work.

## Required external gates

Still required before supported organizational path activation: authorized sanitized observation-rich engagement data; reviewed bindings and collector lineage; independently annotated positive/incomplete/blocked cases and held-out examples; operational authentication-action constraints; analyst and owner shadow pilot. The feature remains disabled by default with a per-engagement allowlist. Snapshot comparison records changes, **never verified remediation** from this adapter.
