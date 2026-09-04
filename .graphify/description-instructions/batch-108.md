# Node Description Batch 109 of 330

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

- "services_validation_ingest_apply_validation_outcome": "apply_validation_outcome()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L32 | neighbors=[validation_ingest.py, ingest_validation_result(), Apply a validation verdict to a finding…]
- "services_validation_ingest_looks_like_validation_result": "looks_like_validation_result()" | kind=code-symbol | source=manager/backend/app/services/validation_ingest.py:L44 | neighbors=[validation_ingest.py, ingest_validation_result(), Cheap gate so normal scan submissions n…]
- "supporting_research_evidence_store_assetverdict": "AssetVerdict" | kind=code-symbol | source=Supporting_research/evidence_store.py:L287 | neighbors=[evidence_store.py, retroactive_detect(), time_travel()]
- "supporting_research_evidence_store_exposure_timeline": "exposure_timeline()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L388 | neighbors=[evidence_store.py, get_path(), (observed_at, answer) transitions -- th…]
- "supporting_research_evidence_store_get_path": "get_path()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L99 | neighbors=[evidence_store.py, exposure_timeline(), _identity_keys()]
- "supporting_research_evidence_store_identity_keys": "_identity_keys()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L163 | neighbors=[evidence_store.py, get_path(), resolve_identity()]
- "supporting_research_evidence_store_iso": "_iso()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L85 | neighbors=[evidence_store.py, record_observation(), retroactive_detect()]
- "supporting_research_evidence_store_unionfind_find": ".find()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L150 | neighbors=[resolve_identity(), _UnionFind, .union()]
- "supporting_research_evidence_store_unionfind_union": ".union()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L157 | neighbors=[resolve_identity(), _UnionFind, .find()]
- "supporting_research_test_evidence_store_demo": "demo()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L222 | neighbors=[test_evidence_store.py, build_fleet(), openssh_below()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_a_brand_new_rule_answers_against_stored_evidence": ".test_a_brand_new_rule_answers_against_stored_evidence()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L145 | neighbors=[No rescan. The whole point., TestRetroactiveDetection, openssh_below()]
- "supporting_research_test_evidence_store_testretroactivedetection_test_current_state_comes_from_latest_evidence_not_a_union_over_history": ".test_current_state_comes_from_latest_evidence_not_a_union_over_history()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L168 | neighbors=[Regression guard. An OR over history me…, TestRetroactiveDetection, openssh_below()]
- "tests_test_accuracy_gate_testcorpusvalidation_test_ground_truth_states_alone_is_a_valid_corpus": ".test_ground_truth_states_alone_is_a_valid_corpus()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L122 | neighbors=[TestCorpusValidation, _port_fact(), _write()]
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
- "tests_test_agents_testaccesstokenexpiry": "TestAccessTokenExpiry" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L767 | neighbors=[test_agents.py, .test_custom_expiry_overrides_default(), ScanJobType]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-108.json

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
