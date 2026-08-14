# Node Description Batch 69 of 186

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

- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L893 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_reaper_objects": "_objects()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L8 | neighbors=[test_reaper.py, test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_resolution_apply_test_covered_clean_medium_finding_is_auto_resolved": "test_covered_clean_medium_finding_is_auto_resolved()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L34 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_db_version_change_blocks_resolution": "test_db_version_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L63 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_uncovered_finding_is_left_open": "test_uncovered_finding_is_left_open()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L50 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…, ResultSpool with tiny retry delay for f…]
- "tests_test_scan_funnel_recordingdeep": "RecordingDeep" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L47 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target()]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_seed_admin_testdriftdetection": "TestDriftDetection" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L308 | neighbors=[test_seed_admin.py, .test_warns_on_multiple_admins(), .test_warns_on_stale_admin_emails()]
- "tests_test_seed_admin_testpasswordrotation": "TestPasswordRotation" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L189 | neighbors=[test_seed_admin.py, .test_rotation_raises_on_hash_verify_fa…, .test_rotation_updates_hash_and_verifie…]
- "tests_test_service_match_testnomatch": "TestNoMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L87 | neighbors=[test_service_match.py, .test_empty_returns_none(), .test_unrecognized_returns_none()]
- "tests_test_service_match_testprobeladder": "TestProbeLadder" | kind=code-symbol | source=probe/tests/test_service_match.py:L95 | neighbors=[test_service_match.py, .test_ladder_has_http_and_generic(), .test_ladder_starts_with_null_probe()]
- "tests_test_smb_scanner_smb2_error_response": "_smb2_error_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L14 | neighbors=[test_smb_scanner.py, An SMB2 ERROR response (e.g. STATUS_INV…, test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_test_error_response_not_parsed_as_signing": "test_error_response_not_parsed_as_signing()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L50 | neighbors=[test_smb_scanner.py, The confirmed bug: an SMB2 error respon…, _smb2_error_response()]
- "tests_test_smb_scanner_test_signing_supported_field_present": "test_signing_supported_field_present()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L71 | neighbors=[test_smb_scanner.py, Step 13: expose signing_supported (prot…, _smb2_negotiate_response()]
- "tests_test_task_runner_testrunnerscantypes": "TestRunnerScanTypes" | kind=code-symbol | source=probe/tests/test_task_runner.py:L447 | neighbors=[test_task_runner.py, .test_ot_passive_profile(), .test_web_triage_scan_type()]
- "tests_test_task_runner_testrunnerscopevalidation_test_rejects_out_of_scope_target": ".test_rejects_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L205 | neighbors=[When scope is fetched and targets are o…, TestRunnerScopeValidation, When scope is fetched and targets are o…]
- "tests_test_task_runner_testrunnerscopevalidation_test_scope_fallback_when_fetch_fails": ".test_scope_fallback_when_fetch_fails()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L318 | neighbors=[When scope fetch fails, manager-embedde…, TestRunnerScopeValidation, When scope fetch fails, manager-embedde…]
- "tests_test_task_runner_testrunnersubmission": "TestRunnerSubmission" | kind=code-symbol | source=probe/tests/test_task_runner.py:L389 | neighbors=[test_task_runner.py, .test_calls_submit_with_result(), .test_uses_spool_when_available()]
- "tests_test_task_runner_testrunnersubmission_test_calls_submit_with_result": ".test_calls_submit_with_result()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L390 | neighbors=[Verify the submit callback is called wi…, TestRunnerSubmission, Verify the submit callback is called wi…]
- "tests_test_task_runner_testrunnersubmission_test_uses_spool_when_available": ".test_uses_spool_when_available()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L415 | neighbors=[When spool_submit is provided, it's use…, TestRunnerSubmission, When spool_submit is provided, it's use…]
- "tests_test_tls_fingerprint_synthetic_server_hello": "_synthetic_server_hello()" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L45 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_integration_self_signed": "_self_signed()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L29 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_integration_test_tls_fingerprint_is_nonzero_and_stable": "test_tls_fingerprint_is_nonzero_and_stable()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L111 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_tls_integration_test_tls_scanner_reports_posture_grade": "test_tls_scanner_reports_posture_grade()" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L87 | neighbors=[test_tls_integration.py, _self_signed(), _TLSServer]
- "tests_test_transport_testfetchscope": "TestFetchScope" | kind=code-symbol | source=probe/tests/test_transport.py:L382 | neighbors=[test_transport.py, .test_http_error_returns_none(), .test_returns_scope()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-068.json

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
