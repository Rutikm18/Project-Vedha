# Node Description Batch 149 of 336

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

- "tests_test_ai_normalizer_testextractrawtext_test_port_scan_returns_none": ".test_port_scan_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L100 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_falls_back_to_banner": ".test_service_banner_falls_back_to_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L52 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_first_line_takes_priority_over_banner": ".test_service_banner_first_line_takes_priority_over_banner()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L56 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_no_text_returns_none": ".test_service_banner_no_text_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L61 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_service_banner_uses_first_line": ".test_service_banner_uses_first_line()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L48 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_empty_data_returns_none": ".test_web_scan_empty_data_returns_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L81 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_server_and_hints_combined": ".test_web_scan_server_and_hints_combined()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L75 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_server_only": ".test_web_scan_server_only()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L65 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_ai_normalizer_testextractrawtext_test_web_scan_tech_hints_only": ".test_web_scan_tech_hints_only()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L69 | neighbors=[TestExtractRawText, _fact()]
- "tests_test_async_udp_sinkprotocol": "_SinkProtocol" | kind=code-symbol | source=probe/tests/test_async_udp.py:L31 | neighbors=[test_async_udp.py, .datagram_received()]
- "tests_test_attack_path_correlation_test_correlation_is_host_scoped": "test_correlation_is_host_scoped()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L131 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_device_role_from_facts_also_amplifies": "test_device_role_from_facts_also_amplifies()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L62 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_exposed_db_with_unauth_is_critical": "test_exposed_db_with_unauth_is_critical()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L95 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_exposed_db_without_unauth_does_not_fire": "test_exposed_db_without_unauth_does_not_fire()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L106 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_legacy_windows_smbv1_plus_rdp": "test_legacy_windows_smbv1_plus_rdp()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L74 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_no_relay_when_signing_required": "test_no_relay_when_signing_required()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L42 | neighbors=[test_attack_path_correlation.py, _ids()]
- "tests_test_attack_path_correlation_test_ntlm_relay_high_when_smbv1_also_enabled": "test_ntlm_relay_high_when_smbv1_also_enabled()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L34 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_ntlm_relay_medium_when_only_signing_not_required": "test_ntlm_relay_medium_when_only_signing_not_required()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L24 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_ntlm_relay_on_domain_controller_is_critical": "test_ntlm_relay_on_domain_controller_is_critical()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L51 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_snmp_default_community_on_network_device_is_high": "test_snmp_default_community_on_network_device_is_high()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L113 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_attack_path_correlation_test_snmp_default_community_without_network_role_is_medium": "test_snmp_default_community_without_network_role_is_medium()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L122 | neighbors=[test_attack_path_correlation.py, _get()]
- "tests_test_auth_login_testauthenticatebcryptfailure": "TestAuthenticateBcryptFailure" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L162 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…]
- "tests_test_auth_login_testauthenticatedatabasefailure": "TestAuthenticateDatabaseFailure" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L181 | neighbors=[test_auth_login.py, .test_raises_database_failure_on_sqlalc…]
- "tests_test_auth_login_testauthenticatedisabledtenant": "TestAuthenticateDisabledTenant" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L122 | neighbors=[test_auth_login.py, .test_raises_disabled_tenant()]
- "tests_test_auth_login_testauthenticatedisableduser": "TestAuthenticateDisabledUser" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L109 | neighbors=[test_auth_login.py, .test_raises_disabled_user()]
- "tests_test_auth_login_testauthenticatepasswordmismatch": "TestAuthenticatePasswordMismatch" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L95 | neighbors=[test_auth_login.py, .test_raises_password_mismatch()]
- "tests_test_auth_login_testauthenticateusernotfound": "TestAuthenticateUserNotFound" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L84 | neighbors=[test_auth_login.py, .test_raises_user_not_found()]
- "tests_test_auth_login_testauthenticateusernotfound_test_raises_user_not_found": ".test_raises_user_not_found()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L86 | neighbors=[TestAuthenticateUserNotFound, _make_db()]
- "tests_test_branch_registry_test_datagram_branches_need_no_tcp_stage": "test_datagram_branches_need_no_tcp_stage()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L142 | neighbors=[test_branch_registry.py, An SNMP-only job must not fall back to …]
- "tests_test_branch_registry_test_web_branch_passes_observed_tls_ports": "test_web_branch_passes_observed_tls_ports()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L197 | neighbors=[test_branch_registry.py, _asset_with()]
- "tests_test_branch_registry_testregistryconsistency_test_every_branch_is_gateable": ".test_every_branch_is_gateable()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L35 | neighbors=[A spec the profile tables don't know ab…, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_every_component_can_be_merged_into_an_asset": ".test_every_component_can_be_merged_into_an_asset()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L65 | neighbors=[A fact whose scanner name has no merge …, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_every_component_has_a_cache_certainty": ".test_every_component_has_a_cache_certainty()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L71 | neighbors=[An unlisted scanner falls back to 'unce…, TestRegistryConsistency]
- "tests_test_branch_registry_testregistryconsistency_test_port_tables_match_gates": ".test_port_tables_match_gates()" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L40 | neighbors=[gate_5 intersects open ports with its o…, TestRegistryConsistency]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_complete_campaign": ".test_complete_campaign()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L75 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_complete_with_gaps": ".test_complete_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L79 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_defaults_keep_backwards_compatibility": ".test_defaults_keep_backwards_compatibility()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L93 | neighbors=[Callers that don't pass the new inputs …, TestNormalPipelineUnaffected]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_no_jobs_is_pending": ".test_no_jobs_is_pending()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L89 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected_test_uncovered_submission_keeps_it_detecting": ".test_uncovered_submission_keeps_it_detecting()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L84 | neighbors=[TestNormalPipelineUnaffected, _status()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults_test_a_dead_queue_is_still_reported_as_error_first": ".test_a_dead_queue_is_still_reported_as_error_first()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L62 | neighbors=[TestTerminalWithoutResults, _status()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-148.json

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
