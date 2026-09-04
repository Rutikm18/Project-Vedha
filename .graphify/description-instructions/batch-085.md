# Node Description Batch 86 of 330

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

- "tests_test_ssh_scanner_testparsekexinit": "TestParseKexinit" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L69 | neighbors=[test_ssh_scanner.py, .test_empty_language_list(), .test_handles_payload_without_leading_t…, .test_parses_all_name_lists()]
- "tests_test_ssh_scanner_testsshfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L194 | neighbors=[TestSSHFindings, .test_clean_server_raises_nothing(), .test_terrapin_raises_finding(), .test_weak_algorithms_raise_finding()]
- "tests_test_ssh_scanner_testsshscanner": "TestSSHScanner" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L164 | neighbors=[test_ssh_scanner.py, ._scanner(), .test_no_response_is_filtered(), .test_weak_server_reports_open_with_fai…]
- "tests_test_ssh_scanner_testvendoreddb": "TestVendoredDB" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L219 | neighbors=[test_ssh_scanner.py, .test_full_db_is_large_not_a_subset(), .test_gss_wildcard_match(), .test_lookup_exact_and_unknown()]
- "tests_test_stage2_reconcile_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L44 | neighbors=[test_stage2_reconcile.py, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…]
- "tests_test_syn_scanner_synack_with_options": "_synack_with_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L326 | neighbors=[test_syn_scanner.py, A SYN/ACK carrying an MSS option (data …, .test_window_ttl_mss_surfaced(), A SYN/ACK carrying an MSS option (data …]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L27 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L94 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynretransmit_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L209 | neighbors=[TestSynRetransmit, .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L157 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L110 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_tls_legacy_versions_test_legacy_version_is_detected_not_masked_by_client_policy": "test_legacy_version_is_detected_not_masked_by_client_policy()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L113 | neighbors=[test_tls_legacy_versions.py, _LegacyTLSServer, _self_signed(), _server_supports()]
- "tests_test_tls_legacy_versions_test_untested_versions_are_surfaced_in_the_fact": "test_untested_versions_are_surfaced_in_the_fact()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L144 | neighbors=[test_tls_legacy_versions.py, When the probe genuinely cannot test a …, _LegacyTLSServer, _self_signed()]
- "tests_test_tls_port_coverage_testsinglesourceoftruth": "TestSingleSourceOfTruth" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L31 | neighbors=[test_tls_port_coverage.py, .test_branch_port_table_reuses_it_too(), .test_branch_spec_matches_the_gate(), .test_gates_reuses_the_same_object()]
- "tests_test_tls_port_coverage_testwidenedcoverage": "TestWidenedCoverage" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L44 | neighbors=[test_tls_port_coverage.py, .test_classic_implicit_tls_still_covere…, .test_management_and_api_surfaces_now_c…, .test_the_set_actually_grew()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L339 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L501 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L372 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L294 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_va_campaign_detect_stage": "_detect_stage()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L242 | neighbors=[test_va_campaign.py, _scope(), test_detect_stage_skipped_when_nothing_…, test_detect_stage_turns_facts_into_weak…]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=probe/tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=probe/tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=probe/tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=probe/tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=probe/tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_verification_llm": "test_verification_llm.py" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L1 | neighbors=[de2d1c9 feat(verification): optional fa…, test_llm_can_flag_false_positive_and_lo…, test_llm_error_falls_back_to_determinis…, test_no_llm_matches_deterministic()]
- "tests_test_vnc_scanner_testvncfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L53 | neighbors=[TestVNCFindings, .test_no_auth_is_critical(), .test_strong_auth_silent(), .test_weak_only_is_medium()]
- "tests_test_vnc_scanner_testvncscanner": "TestVNCScanner" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L33 | neighbors=[test_vnc_scanner.py, ._sc(), .test_no_auth_open(), .test_no_vnc_filtered()]
- "tests_test_weakness_map_testclicorrelatemerges": "TestCliCorrelateMerges" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L180 | neighbors=[test_weakness_map.py, ._disk_db(), .test_correlate_includes_weakness_findi…, .test_no_weakness_map_flag_disables_it()]
- "tests_test_weakness_map_testfindingview": "TestFindingView" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L56 | neighbors=[test_weakness_map.py, .test_non_finding_ignored(), .test_raw_shape(), .test_wrapped_shape()]
- "tests_test_wire_identity_testmoduleconstantsunbranded": "TestModuleConstantsUnbranded" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L80 | neighbors=[test_wire_identity.py, Import-time probe constants built from …, .test_iot_rtsp_options(), .test_service_banner_http_probe()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L75 | neighbors=[issue_license.py, issue(), keygen(), pubkey()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0015_finding_risk_score_scale": "0015_finding_risk_score_scale.py" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, downgrade(), upgrade(), Allow the documented 0-1000 finding ris…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-085.json

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
