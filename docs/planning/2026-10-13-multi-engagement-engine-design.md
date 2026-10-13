# Multi-engagement environment investigation

The user authorized selecting several engagements and investigating how findings across systems contribute to attack paths. This expands the earlier single-engagement scope. Preserve the existing theme and scope-authorized source records.

## Implementation checkpoints

| Slice | Deliverable | Acceptance | State |
| --- | --- | --- | --- |
| 1 | Primary repository/paper research and conservative rule semantics | Directed evidence-backed transitions; no same-IP, shared-subnet or same-CVE shortcut | Complete; primary-source research saved |
| 2 | Bounded pure cross-assessment rule engine | AND prerequisites, source capability, target identity, validity, context and explicit environment bridge tested | Complete for two narrow data-read rule families; synthetic contract tests |
| 3 | Immutable selected-engagement capture and durable worker | One repeatable-read cut, scoped members, bounded input/output, retry/idempotency and failed refresh preservation | Complete; migration 0064 upgrade/rollback/re-upgrade verified |
| 4 | Authorized options/create/latest/detail API and real BFF | Foreign, unallowlisted and revoked principals rejected; inherited operator policy excludes portal/PAT; no caller-supplied evidence/effects | Complete; exact selection restores last completed result without queuing a job |
| 5 | Global selection → system/finding chart → chain inspector | Selected scope visible, source engagement on each finding, keyboard/mobile interactions, no invented bridge | Complete; existing branding/theme retained |
| 6 | Regressions and local preview | Positive synthetic formal cases and truthful missing-evidence source cases; no organizational accuracy claim | Complete for local engineering checks; organizational validation remains gated |

An engagement selection is an analysis scope, not proof that all selected records are the same customer/environment. The present schema has no authoritative customer/environment membership shared by engagements. The first engine retains qualified engagement+asset identities and uses only reviewed explicit environment bridges for cross-assessment capability transfer. Names, private IPs, agent identity and display environment tags cannot create those bridges.

Existing finding/service rows supply candidates and recorded bindings, not normalized execution/credential-transfer observations. Runtime capture therefore reports missing reachability/effect/bridge evidence. The pure engine's supported synthetic test cases do not activate an invented collector adapter.

Normalized transfer contract: same tenant and explicitly selected engagements; exact source/target service-instance and principal/context bindings; active or accepted enabling finding; source capability already derived; approved fixed action; explicit scoped raw-observation lineage, collector/version/checksum; all evidence current at the selected as-of. Evidence for one operation does not establish an observed end-to-end compromise chain.

Capture limits apply across the whole selection, not per engagement. Keep ordinary GET read-only. Preserve immutable snapshots and show unsupported families and truncation separately from path count. UI charts distinguish recorded finding-on-system relationships, missing prerequisites and supported modeled transitions. Never call a disconnected result safe.

## Verification and remaining gates

18 engine/API tests pass, including all required evidence, source capability, stale/conflicted facts, service identity, cycles, budgets, live revocation, cross-scope denials, retry/idempotency, immutable storage and failed-request history. The collectable backend regression suite passes 3,463 tests with nine skips. Two unchanged main-branch test modules still fail collection because they import removed `SyntheticFinding` and `auto_crown_jewel_ids` APIs; this count explicitly excludes `test_capability_map.py` and `test_crown_jewels.py`. After adding the explicit readiness-version pin, the 18 affected tests passed again.

730 frontend tests pass, alongside full type checking, changed-module lint and production build. The synthetic local browser exercised selection of two engagements, real BFF/API/outbox/worker computation, finding-specific source links and condition inspection. Desktop and 320px light/dark views were checked; the grouped correction adds saved-result restoration and reliable inspector navigation when stacked. The final confirmation restores the ordinary viewport and leaves the global dashboard open.

This delivery does **not** activate real cross-system attack discovery. Required next gates are an authoritative customer/environment and entity-equivalence adapter, directed reachability plus exact service-instance observations, reviewed access-transfer and application-read evidence, and independent real-data/analyst validation. The runtime engine receives no normalized transitions until these adapters are implemented and verified. Selection alone cannot establish shared organizational membership. The supported pure-engine cases remain synthetic developer tests; AD/cloud/execution effects are outside these two read-only rule families.
