# Node Description Batch 324 of 380

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_finding_grouping_testgroupkey_test_key_is_short_and_stable": ".test_key_is_short_and_stable()" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L56 | neighbors=[TestGroupKey]
- "tests_test_finding_grouping_testgroupkey_test_missing_evidence_is_survivable": ".test_missing_evidence_is_survivable()" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L53 | neighbors=[TestGroupKey]
- "tests_test_finding_metrics_rationale_1": "Mobilization metrics: MTTR and ownership distribution.  \"No trend metrics — noth" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L1 | neighbors=[test_finding_metrics.py]
- "tests_test_finding_metrics_rationale_122": "A large unassigned pile is itself the thing a manager needs to see —         it" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L122 | neighbors=[.test_unassigned_is_a_first_class_bucke…]
- "tests_test_finding_metrics_rationale_44": "An engagement with nothing closed yet must render, not 500." | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L44 | neighbors=[.test_empty_is_zero_not_a_crash()]
- "tests_test_finding_metrics_rationale_49": "Clamping to zero would quietly pull the mean down and make         remediation l" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L49 | neighbors=[.test_negative_durations_are_dropped_no…]
- "tests_test_finding_metrics_rationale_56": "A finding closed before first_seen was recorded has no measurable         durati" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L56 | neighbors=[.test_none_values_are_dropped()]
- "tests_test_finding_metrics_rationale_66": "Resolved in the same instant is legitimate (a duplicate closed at         creati" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L66 | neighbors=[.test_zero_duration_is_counted()]
- "tests_test_finding_metrics_rationale_87": "The REAL CurrentUser — a SimpleNamespace stand-in once let an endpoint     ship" | kind=entity | source=manager/backend/tests/test_finding_metrics.py:L87 | neighbors=[_user()]
- "tests_test_finding_metrics_testcomputemttr_test_all_dirty_is_zero_count": ".test_all_dirty_is_zero_count()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L61 | neighbors=[TestComputeMttr]
- "tests_test_finding_out_computed_rationale_1": "FindingOut computes the explainable risk_rank at serialization (P4 Task 5 wiring" | kind=entity | source=manager/backend/tests/test_finding_out_computed.py:L1 | neighbors=[test_finding_out_computed.py]
- "tests_test_finding_out_enrichment_phase3_rationale_1": "Phase 3: FindingOut exposes report enrichment (detection_method, verification re" | kind=entity | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L1 | neighbors=[test_finding_out_enrichment_phase3.py]
- "tests_test_finding_owner_schema_rationale_1": "Finding ownership + explicit close time.  The mobilization gap: SLA windows exis" | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L1 | neighbors=[test_finding_owner_schema.py]
- "tests_test_finding_owner_schema_rationale_30": "Unassigned is the normal state — most findings never get an owner." | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L30 | neighbors=[.test_assigned_to_is_nullable()]
- "tests_test_finding_owner_schema_rationale_34": "Null means still open; it is the presence of a value that means closed." | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L34 | neighbors=[.test_resolved_at_is_nullable()]
- "tests_test_finding_owner_schema_rationale_38": "What is on my plate' is a per-owner query and must not table-scan." | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L38 | neighbors=[.test_assigned_to_is_indexed()]
- "tests_test_finding_owner_schema_rationale_44": "Naive timestamps would make MTTR wrong by the UTC offset." | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L44 | neighbors=[.test_resolved_at_is_timezone_aware()]
- "tests_test_finding_owner_schema_rationale_49": "Guards the assumption the metrics service is built on — if these ever go     awa" | kind=entity | source=manager/backend/tests/test_finding_owner_schema.py:L49 | neighbors=[TestMttrInputsAlreadyExist]
- "tests_test_finding_owner_schema_testmttrinputsalreadyexist_test_first_seen_exists": ".test_first_seen_exists()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L52 | neighbors=[TestMttrInputsAlreadyExist]
- "tests_test_finding_owner_schema_testmttrinputsalreadyexist_test_last_seen_exists": ".test_last_seen_exists()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L55 | neighbors=[TestMttrInputsAlreadyExist]
- "tests_test_finding_owner_schema_testownershipcolumns_test_assigned_to_exists": ".test_assigned_to_exists()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L23 | neighbors=[TestOwnershipColumns]
- "tests_test_finding_owner_schema_testownershipcolumns_test_resolved_at_exists": ".test_resolved_at_exists()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L26 | neighbors=[TestOwnershipColumns]
- "tests_test_finding_priority_rationale_1": "finding_priority — the 'critical always on top' ordering contract.  The product" | kind=entity | source=manager/backend/tests/test_finding_priority.py:L1 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_critical_outranks_high_regardless_of_risk": "test_critical_outranks_high_regardless_of_risk()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L39 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_none_risk_is_treated_as_zero_not_a_crash": "test_none_risk_is_treated_as_zero_not_a_crash()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L48 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_severity_order_case_has_a_branch_for_every_tier": "test_severity_order_case_has_a_branch_for_every_tier()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L66 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_severity_rank_accepts_plain_and_mixed_case_strings": "test_severity_rank_accepts_plain_and_mixed_case_strings()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L29 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_severity_rank_orders_all_five_tiers": "test_severity_rank_orders_all_five_tiers()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L19 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_severity_rank_unknown_or_none_sorts_last": "test_severity_rank_unknown_or_none_sorts_last()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L34 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_sorting_a_mixed_list_puts_criticals_first_then_risk": "test_sorting_a_mixed_list_puts_criticals_first_then_risk()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L52 | neighbors=[test_finding_priority.py]
- "tests_test_finding_priority_test_within_a_tier_higher_risk_wins": "test_within_a_tier_higher_risk_wins()" | kind=code-symbol | source=manager/backend/tests/test_finding_priority.py:L44 | neighbors=[test_finding_priority.py]
- "tests_test_finding_resolution_schema_test_finding_has_resolution_lifecycle_columns": "test_finding_has_resolution_lifecycle_columns()" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L6 | neighbors=[test_finding_resolution_schema.py]
- "tests_test_finding_risk_rank_api_test_finding_schema_exposes_risk_rank": "test_finding_schema_exposes_risk_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L6 | neighbors=[test_finding_risk_rank_api.py]
- "tests_test_finding_schema_test_finding_patch_accepts_documented_maximum_risk_score": "test_finding_patch_accepts_documented_maximum_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L9 | neighbors=[test_finding_schema.py]
- "tests_test_finding_schema_test_finding_patch_rejects_risk_score_above_scale": "test_finding_patch_rejects_risk_score_above_scale()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L15 | neighbors=[test_finding_schema.py]
- "tests_test_finding_schema_test_finding_summary_exposes_full_open_severity_breakdown": "test_finding_summary_exposes_full_open_severity_breakdown()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L20 | neighbors=[test_finding_schema.py]
- "tests_test_finding_section_rationale_1": "test_finding_section.py — the scanner-module trust view + the finding section." | kind=entity | source=probe/tests/test_finding_section.py:L1 | neighbors=[test_finding_section.py]
- "tests_test_finding_section_testscannerregistry_test_registry_aligns_with_manager_validated_set": ".test_registry_aligns_with_manager_validated_set()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L38 | neighbors=[TestScannerRegistry]
- "tests_test_finding_section_testscannerregistry_test_unknown_scanner_is_not_trusted": ".test_unknown_scanner_is_not_trusted()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L28 | neighbors=[TestScannerRegistry]
- "tests_test_finding_section_testscannerregistry_test_unvalidated_scanners_are_not_verified": ".test_unvalidated_scanners_are_not_verified()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L24 | neighbors=[TestScannerRegistry]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-323.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
