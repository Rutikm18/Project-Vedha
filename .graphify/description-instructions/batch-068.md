# Node Description Batch 69 of 131

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

- "tests_test_integration_testidentityandencryption_test_scope_encryption_roundtrip": ".test_scope_encryption_roundtrip()" | kind=code-symbol | source=probe/tests/test_integration.py:L78 | neighbors=[Manager encrypts → probe decrypts., TestIdentityAndEncryption]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_hw_bind_blocks": ".test_gauntlet_hw_bind_blocks()" | kind=code-symbol | source=probe/tests/test_integration.py:L442 | neighbors=[Wrong HW fingerprint blocks startup., TestStartupGauntlet]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_skips_in_dev_mode": ".test_gauntlet_skips_in_dev_mode()" | kind=code-symbol | source=probe/tests/test_integration.py:L434 | neighbors=[With LICENSE_ENFORCED=false, gauntlet r…, TestStartupGauntlet]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_decrypts_encrypted_scope_from_job": ".test_decrypts_encrypted_scope_from_job()" | kind=code-symbol | source=probe/tests/test_integration.py:L103 | neighbors=[Job carries encrypted_scope → TaskRunne…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_falls_back_when_decryption_fails": ".test_falls_back_when_decryption_fails()" | kind=code-symbol | source=probe/tests/test_integration.py:L135 | neighbors=[Wrong key → decryption fails → graceful…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtransportwithidentity_test_register_without_public_key": ".test_register_without_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L259 | neighbors=[Backward compat: registration without p…, TestTransportWithIdentity]
- "tests_test_nessus_scanner_test_create_scan": "test_create_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L48 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_create_scan_with_credentials": "test_create_scan_with_credentials()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L65 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_launch_scan": "test_launch_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L85 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_completed": "test_poll_status_completed()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L114 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_running": "test_poll_status_running()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L99 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nuclei_background_fakesession_begin_nested": ".begin_nested()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L43 | neighbors=[_FakeSession, _NestedTransaction]
- "tests_test_nuclei_background_fakesession_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L40 | neighbors=[_FakeSession, _ScalarResult]
- "tests_test_nuclei_background_sessionfactory_call": ".__call__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L71 | neighbors=[_SessionFactory, _FakeSession]
- "tests_test_nuclei_background_test_fatal_nuclei_error_marks_background_job_failed": "test_fatal_nuclei_error_marks_background_job_failed()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L76 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_background_test_partial_nuclei_run_preserves_findings_and_diagnostics": "test_partial_nuclei_run_preserves_findings_and_diagnostics()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L117 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_scanner_test_nonzero_exit_without_findings_raises_with_stderr": "test_nonzero_exit_without_findings_raises_with_stderr()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L108 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_nuclei_scanner_test_template_initialization_failure_cannot_be_clean_zero": "test_template_initialization_failure_cannot_be_clean_zero()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L177 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_passive_collector_socket_close": ".close()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L31 | neighbors=[_Socket, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_passive_collector_test_collector_raises_when_no_listener_binds": "test_collector_raises_when_no_listener_binds()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L165 | neighbors=[test_passive_collector.py, _Writer]
- "tests_test_probe_core_testassetmergepassivecollect": "TestAssetMergePassiveCollect" | kind=code-symbol | source=probe/tests/test_probe_core.py:L583 | neighbors=[test_probe_core.py, .test_passive_facts_appended()]
- "tests_test_probe_core_testassetmergeservicebanner": "TestAssetMergeServiceBanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L534 | neighbors=[test_probe_core.py, .test_banner_stored()]
- "tests_test_probe_core_testassetmergesmbscan": "TestAssetMergeSmbScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L559 | neighbors=[test_probe_core.py, .test_smb_state_host_level()]
- "tests_test_probe_core_testassetmergetlsscan": "TestAssetMergeTlsScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L543 | neighbors=[test_probe_core.py, .test_tls_facts_stored()]
- "tests_test_probe_core_testassetmergeunknownscanner": "TestAssetMergeUnknownScanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L592 | neighbors=[test_probe_core.py, .test_unknown_scanner_ignored()]
- "tests_test_probe_core_testassetmergewebscan": "TestAssetMergeWebScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L551 | neighbors=[test_probe_core.py, .test_web_facts_stored()]
- "tests_test_probe_core_testassetneedsrechecklive_test_never_seen": ".test_never_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L476 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_recently_seen": ".test_recently_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L480 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_stale": ".test_stale()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L484 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L497 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_only_open": ".test_only_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L490 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testcacheentry": "TestCacheEntry" | kind=code-symbol | source=probe/tests/test_probe_core.py:L732 | neighbors=[test_probe_core.py, .test_roundtrip()]
- "tests_test_probe_core_testcacheentry_test_roundtrip": ".test_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L733 | neighbors=[TestCacheEntry, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_error_overrides": ".test_error_overrides()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L723 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_host_discovery_uncertain": ".test_host_discovery_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L719 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_service_banner_deterministic": ".test_service_banner_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L715 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_tcp_port_scan_deterministic": ".test_tcp_port_scan_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L707 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_udp_port_scan_uncertain": ".test_udp_port_scan_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L711 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_unknown_scanner_conservative": ".test_unknown_scanner_conservative()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L727 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testgate2_test_never_seen_alive": ".test_never_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L277 | neighbors=[TestGate2, _asset()]

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
