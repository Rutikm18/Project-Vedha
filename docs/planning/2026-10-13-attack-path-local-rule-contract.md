# R01: exact binding contract for one local consequence

Date: 2026-10-13. Status: implemented experimental contract/evaluator, not an activated production rule. Branch: `codex/attack-path-rule-contract`, starting at the locally available `origin/main` revision `64051cd`. This is the first implementation increment from the expert review. No database migration, route, scanner, graph-store replacement or theme change is included.

## Outcome and claim boundary

Given normalized, authorized evidence and assertions for one selected engagement, evaluate one selected local prerequisite bundle and return exactly **data-read capability for the observed operation on the bound datastore listener**. Require both current reachability from the declared external unauthenticated actor and explicit unauthenticated application-data-read support for that same listener/context.

The caller cannot provide an effect, goal-wide feasibility verdict or arbitrary rule version. The code derives a fixed effect from the rule. It does not infer host execution, host/domain administration, all-record access, data writing, lateral movement, compromise probability or an observed attack chain.

An unsuccessful bundle raises a structured binding error; it does not mean the goal is blocked or the organization is safe. R02 will define proof versus goal status and compute completeness before an API can expose those conclusions.

## Grounded predicate signatures

| Predicate / relation | Typed arguments | Meaning and required joins |
| --- | --- | --- |
| `service_reachable_from_declared_entry` | actor UUID, service UUID, context reference, service instance reference, TCP protocol, integer port, scope, evidence IDs | Evidence concerns the declared actor/vantage and exact listener under the declared unauthenticated scenario. A subnet tag or host-level open-port summary is insufficient. |
| `unauthenticated_datastore_data_read_supported` | Same argument types, plus cited read evidence with an operation reference | The operation returns application data without authentication; metadata, handshake, version and auth-disabled configuration alone do not establish it. |
| Service ownership | service UUID → asset UUID; instance reference, protocol, port and scope | Both assertions refer to this service instance. A reused IP/port or replacement listener cannot compose merely because a display label matches. |
| Finding applicability | finding UUID → asset UUID + service UUID + read evidence IDs | The finding concerns the same service/asset and cites the actual read-support record. Lifecycle is open or accepted; remediation/false-positive adjudication withdraws eligibility. |
| Rule effect | actor, scenario, asset, service instance, observed operation | Only `datastore_data_read`, `service_data_read_only`, `observed_operation_only`; no caller-supplied privilege. |

For one bound actor E, service S, asset H and scenario C, the rule requires:

```text
reachable(E, S, C, instance, tcp, port)
AND unauthenticated_application_read(E, S, C, instance, tcp, port, operation)
AND service_owned_by(S, H)
AND finding_applies_to(F, H, S, read_evidence)
AND each selected record matches the declared tenant and engagement
AND each selected supporting observation is valid at the assessment time
=> datastore_data_read(E, S, H, C, operation)
```

Predicate labels alone are never enough: entity identity, instance, principal/scenario, listener and scope must agree. Exact nominal entity kinds are enforced by the input model. Referenced records and evidence links must exist; duplicate identities or references cannot inflate support. Proof references are sorted canonically so input order does not alter the result.

## Source readiness: checked fields versus missing facts

This is source-schema inspection, not a census of production payloads or an assertion that the following data is already collected.

| Required fact | Current source observation | Integration requirement |
| --- | --- | --- |
| Service UUID, asset, port and protocol | `app/models/service.py` persists these and uniquely constrains asset/port/protocol | Reuse service identity; capture an instance/revision binding before treating reassigned listeners as continuous. |
| Finding asset and engagement | `app/models/finding.py` persists them | Finding has no dedicated `service_id` column in this baseline; normalize an explicit applicability binding from cited facts before activating the rule. Do not guess from the finding title. |
| Declared entry/vantage and scenario | Coarse `Service.exposure` exists | It does not supply the exact entry principal/vantage, context, listener and time required here. A source adapter must retain those fields. |
| Unauthenticated application-data read | `probe/scanner/unauth_access.py` classifies some metadata/handshake responses as unauthenticated access | Do not directly promote that boolean to this rule's application-data-read assertion. Some underlying responses establish a narrower metadata capability. |
| Explicit observed operation | Existing Redis INFO and Memcached version requests are visible in `probe/scanner/service_banner.py` | Those requests do not demonstrate reading stored application records. Missing read evidence yields no supported data-read proof. No new scan or data-read operation is executed by this increment. |
| Time, raw lineage and permitted scope | Raw/finding evidence infrastructure exists, with uneven field availability documented in earlier research | Later normalization must resolve raw records, verify classification and determine observation validity; this evaluator only checks the normalized contract. |

The selected class is a narrow **candidate** until the actual-payload inventory and R06 readiness gate confirm sufficient data. The provided example is synthetic and all raw/operation references use `fixture:` prefixes. It is not evidence of a live environment or a successful read.

## Implementation and error behavior

- [Pure evaluator](../../manager/backend/app/graph/local_rule.py) uses existing Pydantic models without transport/persistence dependencies. Input/output objects are frozen and reject extra fields. TCP is the only supported transport in this version.
- [Synthetic grounded input](2026-10-13-attack-path-local-rule.example.json) demonstrates the exact two predicates, service ownership, scoped records and explicit read operation.
- [Regression tests](../../manager/backend/tests/test_local_attack_path_rule.py) exercise positive/accepted exposure, every AND prerequisite, binding mismatches, metadata confusion, scope, lifecycle, time/reference errors, duplicate identities and order invariance.

Evidence intervals are timezone-aware and half-open: `observed_at <= as_of < valid_until`. An interval ending before or at its observation is structurally invalid. `valid_until` must eventually come from an approved source-specific freshness policy; the example's 30-minute window is synthetic and is not such a policy.

Errors expose stable reason codes such as `scope_mismatch`, `assertion_entity_mismatch`, `listener_mismatch`, `scenario_mismatch`, `evidence_binding_mismatch`, `evidence_kind_mismatch`, `finding_read_evidence_mismatch`, `premise_not_supported` and `evidence_not_current`. A future API must authorize before returning details; these internal errors are not permission checks.

## Verification and remaining work

The focused test run can isolate this pure module from unrelated global backend fixtures:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=manager/backend python3 -m pytest manager/backend/tests/test_local_attack_path_rule.py -q --noconftest -p no:cacheprovider
python3 -m ruff check manager/backend/app/graph/local_rule.py manager/backend/tests/test_local_attack_path_rule.py --no-cache
```

The default interpreter initially lacked `structlog` and had Pydantic 2.9.2. This was resolved without changing global packages: pinned Pydantic 2.10.3 and structlog 24.4.0 were installed into `/private/tmp/vedha-local-rule-deps`. The 65 local cases also passed with that pinned library version and the normal backend shared fixtures:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/private/tmp/vedha-local-rule-deps:manager/backend python3 -m pytest manager/backend/tests/test_local_attack_path_rule.py -q -p no:cacheprovider
```

This is not a complete backend integration run. The test runner is the locally available pytest 9.0.2; the complete pinned CI/runtime matrix remains unverified.

Recorded result: **65 focused cases passed**. Lint passed. Formatting, JSON parsing and document links were checked. Cases are developer-authored synthetic regressions, not an independently labeled holdout or a measurement of field accuracy.

The combined normal-fixture run with the existing `test_attack_path_correlation.py` suite passed **79 cases** (65 new local-rule cases and 14 existing correlation cases).

This increment does not repair the old research checker or activate its schema. It implements a separate narrower typed contract; the earlier ten counterexamples remain a useful diagnostic of that old fixture. Several have direct regression counterparts here, while caller summary labels/selected steps are excluded entirely from this input.

Still required: independently reviewed real payloads; raw evidence classification; source namespaces/instance capture; coherent input manifests and known-at history; authorization and rule activation governance; goal/alternative status; bounded inference and durable snapshots; API and analyst workflow. Do not mark T05/T06/T14 as production-complete from this unit suite.

Next increment: **R02 — an executable proof/goal/completeness decision table**, including one blocked route with another supported alternative and a truncated search with no observed support.
