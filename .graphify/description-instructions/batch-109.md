# Node Description Batch 110 of 332

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
- "tests_test_ai_normalizer_testproposecandidates_test_source_confidence_propagated_from_fact": ".test_source_confidence_propagated_from_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L218 | neighbors=[source_confidence on the resulting CPEC…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_none_when_absent": ".test_version_none_when_absent()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L242 | neighbors=[A candidate without a version key produ…, TestProposeCandidates, _fact()]
- "tests_test_ai_normalizer_testproposecandidates_test_version_propagated_when_present": ".test_version_propagated_when_present()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L230 | neighbors=[When the AI response includes a version…, TestProposeCandidates, _fact()]
- "tests_test_async_udp_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=probe/tests/test_async_udp.py:L23 | neighbors=[test_async_udp.py, .connection_made(), .datagram_received()]
- "tests_test_attack_path_correlation_test_cleartext_cluster_needs_two": "test_cleartext_cluster_needs_two()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L82 | neighbors=[test_attack_path_correlation.py, _get(), _ids()]
- "tests_test_auth_login_testauthenticatedisableduser_test_raises_disabled_user": ".test_raises_disabled_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L111 | neighbors=[TestAuthenticateDisabledUser, _make_db(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword": "TestAuthenticateExpiredPassword" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L135 | neighbors=[test_auth_login.py, .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testauthenticatesuccess": "TestAuthenticateSuccess" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L193 | neighbors=[test_auth_login.py, .test_null_password_expires_at_never_ex…, .test_returns_user_on_valid_credentials…]
- "tests_test_branch_registry_fake": "_fake()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L89 | neighbors=[test_branch_registry.py, test_host_level_branch_is_cached_under_…, test_service_specific_plan_matches_what…]
- "tests_test_branch_registry_test_db_branch_splits_known_and_router_discovered_ports": "test_db_branch_splits_known_and_router_discovered_ports()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L184 | neighbors=[test_branch_registry.py, The database branch is the one spec tha…, _asset_with()]
- "tests_test_branch_registry_test_host_level_branch_is_cached_under_a_null_port": "test_host_level_branch_is_cached_under_a_null_port()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L157 | neighbors=[test_branch_registry.py, smb's fact describes the host, so it mu…, _fake()]
- "tests_test_branch_registry_test_service_specific_plan_matches_what_the_engine_runs": "test_service_specific_plan_matches_what_the_engine_runs()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L111 | neighbors=[test_branch_registry.py, Before the registry, these five planned…, _fake()]
- "tests_test_branch_registry_test_snmp_scanner_is_constructed_without_a_ports_kwarg": "test_snmp_scanner_is_constructed_without_a_ports_kwarg()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L204 | neighbors=[test_branch_registry.py, SNMPScanner's signature has no `ports`;…, _asset_with()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_does_not_hijack_a_campaign_that_produced_results": ".test_does_not_hijack_a_campaign_that_produced_results()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L49 | neighbors=[The normal path must be untouched: a co…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_partial_cancel_with_one_success_still_aggregates": ".test_partial_cancel_with_one_success_still_aggregates()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L66 | neighbors=[One good job is enough to expect a dete…, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_running_job_still_wins": ".test_running_job_still_wins()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L56 | neighbors=[Precedence: work in flight is reported …, TestTerminalWithoutResults, _status()]
- "tests_test_campaign_progress_test_pipeline_advances_through_every_phase": "test_pipeline_advances_through_every_phase()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L154 | neighbors=[test_campaign_progress.py, _run_scenario(), _user()]
- "tests_test_campaign_progress_test_unknown_worker_liveness_falls_back_to_patience": "test_unknown_worker_liveness_falls_back_to_patience()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L353 | neighbors=[test_campaign_progress.py, No heartbeat table (migration not yet r…, _running_run()]
- "tests_test_customer_access_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L48 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_creates_a_scoped_client_login()]
- "tests_test_customer_access_testassignagent": "TestAssignAgent" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L206 | neighbors=[test_customer_access.py, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()]
- "tests_test_customer_access_testassignagent_test_assigns_agent_to_engagement": ".test_assigns_agent_to_engagement()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L207 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testassignagent_test_unknown_agent_is_404": ".test_unknown_agent_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L218 | neighbors=[TestAssignAgent, _mock_db(), _operator()]
- "tests_test_customer_access_testprovisionclientuser_test_duplicate_is_conflict": ".test_duplicate_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L114 | neighbors=[TestProvisionClientUser, _mock_db(), _operator()]
- "tests_test_customer_reveal_test_reveal_missing_user_is_404": "test_reveal_missing_user_is_404()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L48 | neighbors=[test_customer_reveal.py, _db(), _operator()]
- "tests_test_customer_reveal_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L30 | neighbors=[test_customer_reveal.py, test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]

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
