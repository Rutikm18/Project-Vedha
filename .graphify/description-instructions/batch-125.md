# Node Description Batch 126 of 380

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

- "tests_test_engagement_lists_test_list_jobs_returns_results": "test_list_jobs_returns_results()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L22 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L13 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_eol_detection_testeolrule_test_declares_its_required_input": ".test_declares_its_required_input()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L96 | neighbors=[The `requires` contract makes a missing…, TestEolRule, _rule()]
- "tests_test_eol_detection_testeolrule_test_fires_on_past_eol_os": ".test_fires_on_past_eol_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L80 | neighbors=[TestEolRule, _fact(), _rule()]
- "tests_test_eol_detection_testeolrule_test_silent_on_supported_os": ".test_silent_on_supported_os()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L88 | neighbors=[TestEolRule, _fact(), _rule()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_by_cve": ".test_select_exploit_by_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L256 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_fallback_no_cve": ".test_select_exploit_fallback_no_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L269 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_log4shell": ".test_select_exploit_log4shell()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L263 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_scope_out_of_range": ".test_validate_scope_out_of_range()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L284 | neighbors=[TestExploitOrchestrator, _engagement(), ._make_orchestrator()]
- "tests_test_exploitability_testneverclaimsthecveispresent_test_refs_carry_the_relation_and_kev_status": ".test_refs_carry_the_relation_and_kev_status()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L54 | neighbors=[TestNeverClaimsTheCveIsPresent, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_elevated_epss_band": ".test_elevated_epss_band()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L84 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_epss_max_takes_the_worst_linked_cve": ".test_epss_max_takes_the_worst_linked_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L102 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_high_epss_without_kev_is_likely": ".test_high_epss_without_kev_is_likely()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L79 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_kev_listed_is_actively_exploited": ".test_kev_listed_is_actively_exploited()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L74 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_kev_outranks_epss": ".test_kev_outranks_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L92 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_low_epss_is_unknown": ".test_low_epss_is_unknown()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L88 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_rule_with_no_linkage": ".test_rule_with_no_linkage()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L97 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exposed_services_test_exposed_findings_flow_through_detect_posture": "test_exposed_findings_flow_through_detect_posture()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L124 | neighbors=[test_exposed_services.py, _asset(), _fact()]
- "tests_test_exposed_services_testdetect_test_dedicated_ports_not_double_reported": ".test_dedicated_ports_not_double_reported()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L97 | neighbors=[TestDetect, _asset(), _fact()]
- "tests_test_exposed_services_testdetect_test_udp_ports_ignored": ".test_udp_ports_ignored()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L104 | neighbors=[TestDetect, _asset(), _fact()]
- "tests_test_fact_contract_test_corpus_survives_ingestion": "test_corpus_survives_ingestion()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L65 | neighbors=[test_fact_contract.py, The gate the name-level check above can…, _ingest_corpus()]
- "tests_test_finding_ai_test_llm_error_fails_closed_to_none": "test_llm_error_fails_closed_to_none()" | kind=code-symbol | source=manager/backend/tests/test_finding_ai.py:L47 | neighbors=[test_finding_ai.py, _f(), _run()]
- "tests_test_finding_ai_test_none_llm_is_a_no_op": "test_none_llm_is_a_no_op()" | kind=code-symbol | source=manager/backend/tests/test_finding_ai.py:L81 | neighbors=[test_finding_ai.py, _f(), _run()]
- "tests_test_finding_events_testmerge_stored": "._stored()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L98 | neighbors=[TestMerge, .test_sorted_oldest_first(), .test_stored_supersedes_synthesized_sam…]
- "tests_test_finding_events_testmerge_test_stored_supersedes_synthesized_same_type": ".test_stored_supersedes_synthesized_same_type()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L103 | neighbors=[TestMerge, ._stored(), ._synth()]
- "tests_test_finding_events_testpatchaudits": "TestPatchAudits" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L158 | neighbors=[test_finding_events.py, .test_manual_remediation_sets_close_met…, .test_status_change_records_event()]
- "tests_test_finding_events_testsynthesize_test_manual_remediation_event": ".test_manual_remediation_event()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L73 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_no_reobserved_when_last_seen_equals_genesis": ".test_no_reobserved_when_last_seen_equals_genesis()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L63 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_reobserved_when_last_seen_advances": ".test_reobserved_when_last_seen_advances()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L59 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_terminal_confirmed_state_emitted": ".test_terminal_confirmed_state_emitted()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L84 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_events_testsynthesize_test_terminal_false_positive_state_emitted": ".test_terminal_false_positive_state_emitted()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L87 | neighbors=[TestSynthesize, _finding(), _types()]
- "tests_test_finding_grouping": "test_finding_grouping.py" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L1 | neighbors=[6136a6e feat(detection): stable group_k…, TestGroupKey, Stable grouping keys for fleet-scale fi…]
- "tests_test_finding_metrics_testcomputemttr_test_negative_durations_are_dropped_not_clamped": ".test_negative_durations_are_dropped_not_clamped()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L48 | neighbors=[Clamping to zero would quietly pull the…, TestComputeMttr, _pair()]
- "tests_test_finding_metrics_testcomputemttr_test_none_values_are_dropped": ".test_none_values_are_dropped()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L55 | neighbors=[A finding closed before first_seen was …, TestComputeMttr, _pair()]
- "tests_test_finding_metrics_testcomputemttr_test_zero_duration_is_counted": ".test_zero_duration_is_counted()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L65 | neighbors=[Resolved in the same instant is legitim…, TestComputeMttr, _pair()]
- "tests_test_finding_metrics_testmetricsendpoint_test_shape_is_stable_when_empty": ".test_shape_is_stable_when_empty()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L103 | neighbors=[TestMetricsEndpoint, _db(), _user()]
- "tests_test_finding_reopen_endpoint_db_with": "_db_with()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L15 | neighbors=[test_finding_reopen_endpoint.py, test_reopen_non_remediated_is_conflict(), test_reopen_remediated_finding_sets_ope…]
- "tests_test_fleet_jobs_test_filter_by_probe_and_engagement_run_without_error": "test_filter_by_probe_and_engagement_run_without_error()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L54 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]
- "tests_test_fleet_jobs_test_lists_jobs_with_probe_and_engagement_names": "test_lists_jobs_with_probe_and_engagement_names()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L22 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]
- "tests_test_fleet_jobs_test_running_filter_is_accepted": "test_running_filter_is_accepted()" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L46 | neighbors=[test_fleet_jobs.py, _scalars(), _user()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-125.json

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
