# Node Description Batch 173 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_finding_events_testpatchaudits_test_manual_remediation_sets_close_metadata_and_audits_reason": ".test_manual_remediation_sets_close_metadata_and_audits_reason()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L195 | neighbors=[TestPatchAudits, _finding()]
- "tests_test_finding_events_testpatchaudits_test_status_change_records_event": ".test_status_change_records_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L160 | neighbors=[TestPatchAudits, _finding()]
- "tests_test_finding_events_testsynthesize_test_auto_resolution_event": ".test_auto_resolution_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L66 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_detected_actor_falls_back_to_detection_engine": ".test_detected_actor_falls_back_to_detection_engine()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L55 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_detected_actor_labels_network_va_campaign": ".test_detected_actor_labels_network_va_campaign()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L51 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_genesis_detected_from_first_seen": ".test_genesis_detected_from_first_seen()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L45 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testsynthesize_test_reopened_inferred_from_count": ".test_reopened_inferred_from_count()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L78 | neighbors=[TestSynthesize, _finding()]
- "tests_test_finding_events_testtimelineendpoint": "TestTimelineEndpoint" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L137 | neighbors=[test_finding_events.py, .test_returns_synthesized_timeline()]
- "tests_test_finding_events_testtimelineendpoint_test_returns_synthesized_timeline": ".test_returns_synthesized_timeline()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L139 | neighbors=[TestTimelineEndpoint, _finding()]
- "tests_test_finding_grouping_testgroupkey_test_different_rules_do_not_group": ".test_different_rules_do_not_group()" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L30 | neighbors=[Same device, different weakness — must …, TestGroupKey]
- "tests_test_finding_grouping_testgroupkey_test_no_signature_still_groups_by_rule": ".test_no_signature_still_groups_by_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L49 | neighbors=[Coarser, but deterministic — never a cr…, TestGroupKey]
- "tests_test_finding_grouping_testgroupkey_test_product_match_is_case_and_whitespace_insensitive": ".test_product_match_is_case_and_whitespace_insensitive()" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L36 | neighbors=[Vendor strings arrive from banners with…, TestGroupKey]
- "tests_test_finding_metrics_testcomputemttr_test_days_is_hours_over_24": ".test_days_is_hours_over_24()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L71 | neighbors=[TestComputeMttr, _pair()]
- "tests_test_finding_metrics_testcomputemttr_test_empty_is_zero_not_a_crash": ".test_empty_is_zero_not_a_crash()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L43 | neighbors=[An engagement with nothing closed yet m…, TestComputeMttr]
- "tests_test_finding_metrics_testcomputemttr_test_mean_of_two": ".test_mean_of_two()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L33 | neighbors=[TestComputeMttr, _pair()]
- "tests_test_finding_metrics_testcomputemttr_test_single_finding": ".test_single_finding()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L39 | neighbors=[TestComputeMttr, _pair()]
- "tests_test_finding_out_computed_test_confirmed_exploited_outranks_contradicted": "test_confirmed_exploited_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L32 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_detail_asset_context_round_trips_without_changing_list_contract": "test_detail_asset_context_round_trips_without_changing_list_contract()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L55 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_explicit_risk_rank_is_preserved": "test_explicit_risk_rank_is_preserved()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L44 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_lifecycle_fields_round_trip": "test_lifecycle_fields_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L49 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_nested_enrichment_kev_is_part_of_the_rank": "test_nested_enrichment_kev_is_part_of_the_rank()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L38 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_risk_rank_is_computed_not_none": "test_risk_rank_is_computed_not_none()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L26 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_detection_method_from_exploit_validated": "test_detection_method_from_exploit_validated()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L41 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_detection_method_from_verification_state": "test_detection_method_from_verification_state()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L45 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_detection_method_none_when_unproven": "test_detection_method_none_when_unproven()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L49 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_epss_percentile_surfaced_from_evidence": "test_epss_percentile_surfaced_from_evidence()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L53 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_existing_computed_fields_are_unaffected": "test_existing_computed_fields_are_unaffected()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L68 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_internet_reachable_surfaced_from_evidence": "test_internet_reachable_surfaced_from_evidence()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L62 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_kev_added_at_surfaced_from_evidence": "test_kev_added_at_surfaced_from_evidence()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L58 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_verification_block_always_present_with_pass_criterion": "test_verification_block_always_present_with_pass_criterion()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L28 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_out_enrichment_phase3_test_weak_tls_gets_a_specific_retest": "test_weak_tls_gets_a_specific_retest()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L35 | neighbors=[test_finding_out_enrichment_phase3.py, _base()]
- "tests_test_finding_owner_schema_testownershipcolumns_test_assigned_to_is_indexed": ".test_assigned_to_is_indexed()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L37 | neighbors=[What is on my plate' is a per-owner que…, TestOwnershipColumns]
- "tests_test_finding_owner_schema_testownershipcolumns_test_assigned_to_is_nullable": ".test_assigned_to_is_nullable()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L29 | neighbors=[Unassigned is the normal state — most f…, TestOwnershipColumns]
- "tests_test_finding_owner_schema_testownershipcolumns_test_resolved_at_is_nullable": ".test_resolved_at_is_nullable()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L33 | neighbors=[Null means still open; it is the presen…, TestOwnershipColumns]
- "tests_test_finding_owner_schema_testownershipcolumns_test_resolved_at_is_timezone_aware": ".test_resolved_at_is_timezone_aware()" | kind=code-symbol | source=manager/backend/tests/test_finding_owner_schema.py:L43 | neighbors=[Naive timestamps would make MTTR wrong …, TestOwnershipColumns]
- "tests_test_finding_reopen_endpoint_test_reopen_non_remediated_is_conflict": "test_reopen_non_remediated_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L48 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_reopen_endpoint_test_reopen_remediated_finding_sets_open_and_audits": "test_reopen_remediated_finding_sets_open_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L24 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]
- "tests_test_finding_section_testfindingsection_test_backward_compatible_keys_kept": ".test_backward_compatible_keys_kept()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L95 | neighbors=[TestFindingSection, ._sum()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-172.json

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
