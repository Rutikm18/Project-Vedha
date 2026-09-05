# Node Description Batch 110 of 336

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

- "tests_test_accuracy_gate_testprovenance_test_gate_counts_the_two_kinds_separately": ".test_gate_counts_the_two_kinds_separately()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L136 | neighbors=[TestProvenance, _port_fact(), _write()]
- "tests_test_accuracy_gate_testshippedcorpora_test_regression_only_directory_still_warns": ".test_regression_only_directory_still_warns()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L81 | neighbors=[TestShippedCorpora, _port_fact(), _write()]
- "tests_test_accuracy_gate_testthresholds_test_matching_port_state_scores_perfectly": ".test_matching_port_state_scores_perfectly()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L197 | neighbors=[TestThresholds, _port_fact(), _write()]
- "tests_test_accuracy_gate_testthresholds_test_thresholds_are_overridable": ".test_thresholds_are_overridable()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L186 | neighbors=[TestThresholds, _port_fact(), _write()]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_groups_marks_privileged": ".test_get_groups_marks_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L150 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_disabled_account": ".test_get_users_disabled_account()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L123 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_parses_uac_and_spn": ".test_get_users_parses_uac_and_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L103 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_adaptive_rate_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L177 | neighbors=[test_adaptive_rate.py, .connection_made(), .datagram_received()]
- "tests_test_agent_auth_boundary_boundary_test_client": "_boundary_test_client()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L47 | neighbors=[test_agent_auth_boundary.py, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…]
- "tests_test_agent_policy_testclassifyaction": "TestClassifyAction" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L9 | neighbors=[test_agent_policy.py, .test_known_actions_map_to_expected_tie…, .test_unknown_action_fails_closed_to_hi…]
- "tests_test_agent_read_tools_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L44 | neighbors=[test_agent_read_tools.py, test_list_assets_batches_services_no_n_…, test_list_assets_caps_services_at_30()]
- "tests_test_agent_read_tools_svc": "_svc()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L52 | neighbors=[test_agent_read_tools.py, test_list_assets_batches_services_no_n_…, test_list_assets_caps_services_at_30()]
- "tests_test_agent_read_tools_test_list_assets_empty_skips_service_query": "test_list_assets_empty_skips_service_query()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L92 | neighbors=[test_agent_read_tools.py, _FakeSession, _Result]
- "tests_test_agents_testaccesstokenexpiry": "TestAccessTokenExpiry" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L797 | neighbors=[test_agents.py, .test_custom_expiry_overrides_default(), ScanJobType]
- "tests_test_agents_testenqueueagentjob_test_404_when_engagement_missing": ".test_404_when_engagement_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L59 | neighbors=[TestEnqueueAgentJob, _redis(), _user()]
- "tests_test_agents_testenqueueagentjob_test_materializes_direct_job_capability_for_probe": ".test_materializes_direct_job_capability_for_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L99 | neighbors=[TestEnqueueAgentJob, _redis(), _user()]
- "tests_test_agents_testenqueueagentjob_test_rejects_server_side_type": ".test_rejects_server_side_type()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L52 | neighbors=[TestEnqueueAgentJob, _redis(), _user()]
- "tests_test_agents_testenqueueagentjob_test_scope_fields_cannot_override_engagement_scope": ".test_scope_fields_cannot_override_engagement_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L128 | neighbors=[TestEnqueueAgentJob, _redis(), _user()]
- "tests_test_agents_testenqueueagentjob_test_success_creates_pending_job": ".test_success_creates_pending_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L68 | neighbors=[TestEnqueueAgentJob, _redis(), _user()]
- "tests_test_agents_testotprofilegate_test_allows_passive_discovery_on_ot_engagement": ".test_allows_passive_discovery_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L205 | neighbors=[TestOTProfileGate, _redis(), _user()]
- "tests_test_agents_testotprofilegate_test_blocks_active_scan_type_on_ot_engagement": ".test_blocks_active_scan_type_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L173 | neighbors=[TestOTProfileGate, _redis(), _user()]
- "tests_test_agents_testotprofilegate_test_blocks_explicit_active_scan_type_override_on_ot_engagement": ".test_blocks_explicit_active_scan_type_override_on_ot_engagement()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L188 | neighbors=[TestOTProfileGate, _redis(), _user()]
- "tests_test_agents_testotprofilegate_test_it_and_iot_profiles_unaffected": ".test_it_and_iot_profiles_unaffected()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L221 | neighbors=[TestOTProfileGate, _redis(), _user()]
- "tests_test_ai_engine_testllmreportgenerator_test_complete_retries_then_succeeds": ".test_complete_retries_then_succeeds()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L226 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_detection_rule_explanation": ".test_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L243 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_executive_summary_persists_pending": ".test_executive_summary_persists_pending()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L180 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_unavailable_without_client": ".test_unavailable_without_client()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L217 | neighbors=[TestLLMReportGenerator, _finding(), _mock_db()]
- "tests_test_ai_engine_testvulnprioritizer_test_explain_prediction_fallback_shape": ".test_explain_prediction_fallback_shape()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L78 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_extract_features_order_and_values": ".test_extract_features_order_and_values()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L55 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_higher_cvss_scores_higher": ".test_higher_cvss_scores_higher()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L73 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_predict_priority_uses_fallback_when_untrained": ".test_predict_priority_uses_fallback_when_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L67 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_normalizer_testextractrawtext_test_ssh_inventory_returns_none": ".test_ssh_inventory_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L95 | neighbors=[ssh_inventory facts have no banner-styl…, TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testfakeaiclient": "TestFakeAIClient" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L109 | neighbors=[test_ai_normalizer.py, .test_returns_empty_for_unknown_text(), .test_returns_registered_response()]
- "tests_test_ai_normalizer_testproposecandidates_test_ai_assisted_flag_set_on_candidates": ".test_ai_assisted_flag_set_on_candidates()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L205 | neighbors=[Every candidate produced by propose_can…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_cache_hit_bypasses_client": ".test_cache_hit_bypasses_client()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L167 | neighbors=[When the cache already has an answer, t…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_client_failure_returns_empty": ".test_client_failure_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L154 | neighbors=[Any exception from the AI client yields…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_malformed_response_missing_product_skipped": ".test_malformed_response_missing_product_skipped()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L184 | neighbors=[A candidate dict without a 'product' ke…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_malformed_response_not_a_list_returns_empty": ".test_malformed_response_not_a_list_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L193 | neighbors=[If the client returns something that is…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_result_is_cached_after_first_call": ".test_result_is_cached_after_first_call()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L252 | neighbors=[The result of a first successful client…, TestProposeCandidates, _fact()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
