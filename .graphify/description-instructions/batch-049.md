# Node Description Batch 50 of 186

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

- "tests_test_resolution_apply_db_returning": "_db_returning()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L26 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port()]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L22 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L34 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L60 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L190 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L141 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L30 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L97 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L160 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L113 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L316 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L478 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L349 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L271 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=probe/tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=probe/tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=probe/tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=probe/tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=probe/tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_verification_llm": "test_verification_llm.py" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L1 | neighbors=[de2d1c9 feat(verification): optional fa…, test_llm_can_flag_false_positive_and_lo…, test_llm_error_falls_back_to_determinis…, test_no_llm_matches_deterministic()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0015_finding_risk_score_scale": "0015_finding_risk_score_scale.py" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, downgrade(), upgrade(), Allow the documented 0-1000 finding ris…]
- "versions_0016_user_tenant_is_active": "0016_user_tenant_is_active.py" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, downgrade(), upgrade(), Add is_active to users and tenants; add…]
- "versions_0017_scan_job_attempts": "0017_scan_job_attempts.py" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add fenced execution attempts for agent…]
- "versions_0018_probe_enrollment": "0018_probe_enrollment.py" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add Manager-approved device-key probe e…]
- "versions_0020_finding_resolution_lifecycle": "0020_finding_resolution_lifecycle.py" | kind=code-symbol | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, downgrade(), upgrade(), Finding resolution lifecycle: coverage-…]
- "versions_0021_finding_verification": "0021_finding_verification.py" | kind=code-symbol | source=manager/backend/alembic/versions/0021_finding_verification.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, downgrade(), upgrade(), Finding verification verdict columns (P…]
- "versions_0022_validation_requests": "0022_validation_requests.py" | kind=code-symbol | source=manager/backend/alembic/versions/0022_validation_requests.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, downgrade(), upgrade(), Approval-gated safe active-validation r…]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-049.json

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
