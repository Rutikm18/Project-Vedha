# Node Description Batch 61 of 227

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

- "tests_test_remediation_routes_testgetremediation_test_kb_on_cache_miss": ".test_kb_on_cache_miss()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L110 | neighbors=[TestGetRemediation, _db_scalar(), _finding(), _operator()]
- "tests_test_remediation_routes_testupsertstatement_sql": "._sql()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L184 | neighbors=[TestUpsertStatement, .test_refreshes_generated_at_on_conflic…, .test_regeneration_resets_review_gate_n…, .test_targets_the_unique_constraint()]
- "tests_test_resolution_apply_db_returning": "_db_returning()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L26 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port()]
- "tests_test_resolve": "test_resolve.py" | kind=code-symbol | source=probe/tests/test_resolve.py:L1 | neighbors=[dec1e7c fix(scanner): resolve() family …, _infos(), TestResolveFamily, test_resolve.py — resolve() address-fam…]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L22 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L34 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L60 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L190 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_sla_policy_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L32 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_custom_when_row_present": ".test_get_custom_when_row_present()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L58 | neighbors=[TestSlaPolicyRoutes, _db(), _operator(), _row()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L27 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L94 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynretransmit_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L209 | neighbors=[TestSynRetransmit, .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L157 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L110 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L339 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L501 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L372 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L294 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=probe/tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=probe/tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=probe/tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=probe/tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=probe/tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_verification_llm": "test_verification_llm.py" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L1 | neighbors=[de2d1c9 feat(verification): optional fa…, test_llm_can_flag_false_positive_and_lo…, test_llm_error_falls_back_to_determinis…, test_no_llm_matches_deterministic()]
- "tests_test_wire_identity_testmoduleconstantsunbranded": "TestModuleConstantsUnbranded" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L80 | neighbors=[test_wire_identity.py, Import-time probe constants built from …, .test_iot_rtsp_options(), .test_service_banner_http_probe()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L75 | neighbors=[issue_license.py, issue(), keygen(), pubkey()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-060.json

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
