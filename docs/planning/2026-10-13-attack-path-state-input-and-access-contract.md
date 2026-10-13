# R02–R04: assessment states, sealed inputs and disclosure

These implemented foundations extend the experimental local binding contract. They are internal functions, not client-authoritative verdicts, authenticated endpoints or an activation of inference in production.

## R02: the proposition behind each status

| Selected proofs | Computation / collection | Goal conclusion |
| --- | --- | --- |
| At least one current validated supported derivation | Any computation completion, any collection completeness | Supported within the declared model, with incomplete qualifiers retained. |
| One blocked route; another supported route | Complete or incomplete search | Supported; the blocked route cannot suppress the alternative. |
| No supported derivation; search truncated or failed | Any collection | Indeterminate. |
| No supported derivation; missing, restricted or unsupported collection | Complete computation | Indeterminate. |
| No supported derivation; unresolved, conflicted, stale or unevaluated route | Complete computation and collection | Indeterminate. |
| No supported derivation | Complete derivation and complete declared collection, no unresolved routes | Not derived in the declared model. This is not a claim of organizational safety. |
| Query never evaluated | No evaluated proofs | Not evaluated. |

The query identity must include tenant/engagement, scenario, goal, input cut and rule artifact. Top-K explanations, pagination and hidden map elements cannot establish computation completeness. The internal summarizer receives outcomes from trusted evaluation; future APIs must not accept these summary states from callers.

## R03: input history and identity

`InputCut` preserves effective assessment time, known-at cutoff, capture time, normalization version, rule artifact digest and one immutable source revision/completed batch reference per evidence record. `seal_input` rejects foreign scope, missing/duplicate revision bindings, mixed revisions within one source, future observations and evidence ingested after the knowledge cutoff.

Semantic identity uses a canonical SHA-256 representation of the normalized inputs and manifest, excluding capture wall time. Order of assertions/evidence/revision lists and equivalent timezone representations cannot change identity. Rule, normalization, source and knowledge revisions can change it. The sealed object retains the original capture time for audit.

**Capture boundary:** the function validates a supplied cut, not the underlying transaction or external collector. It does not prove a batch completed merely because a string names it. The database adapter must verify completed batches and materialize all eligible inputs in a short Repeatable Read transaction before background computation. Stable database reads do not establish simultaneity of independently observed real-world facts. Raw assertion classification, validity policy and coherent acquisition remain separate integration requirements.

Late evidence can create a new retrospective reconstruction with a later known-at cutoff; it cannot mutate an old immutable input or silently claim the earlier system knew it. New input hashes alone are not proof of a remediation outcome.

## R04: initial operator disclosure policy

| Principal | Read assessment/evidence | Request computation/comparison |
| --- | --- | --- |
| Admin, manager, analyst, tester; matching tenant | Allowed | Allowed |
| Auditor; matching tenant | Allowed | Denied |
| Portal/client, unknown role or engagement-limited principal | Denied | Denied |
| Personal access token | Denied pending an explicit feature scope design | Denied |
| Foreign tenant | Denied | Denied |

This first release uses no redacted graph or hidden-evidence summary. An unapproved principal receives an authorization failure before evidence, counts, goal labels or inference are fetched. Denial is not a negative security fact. Allowed roles receive the complete authorized operator scope; if a later adapter introduces per-record restrictions, it must either decline that scope or mark its collection incomplete, never silently erase premises.

Each endpoint/job/export must recheck fresh authentication and the independently tenant-scoped engagement. The helper checks authorization policy only; it does not load or refresh users itself. Responses should use `Cache-Control: no-store`. Worker computation scope is separate from whoever is allowed to view its output. Portal entitlements and customer access remain outside this operator-only feature.

## Acceptance evidence

Executable cases include a surviving alternative, truncated positive proof, missing/denied collection, contradictory labels, late/mixed revisions, replay/order/timezone invariance, role downgrade and foreign-tenant rejection. These are developer-authored contract regressions. Independent analyst labels, real-payload field census, transaction/race tests and live revocation tests remain required for the later delivery gates.

Implementation: `app/graph/assessment_state.py`, `input_manifest.py`, `access_policy.py`, with corresponding `tests/test_attack_path_*` suites. No existing graph/API behavior was replaced by these foundations.
