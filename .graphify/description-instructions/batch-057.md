# Node Description Batch 58 of 104

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

- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_format": ".test_generate_dns_callback_token_format()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L290 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_unique": ".test_generate_dns_callback_token_unique()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L298 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_safety_meterpreter_raises": ".test_validate_safety_meterpreter_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L275 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_get_job_status_running": ".test_get_job_status_running()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L218 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_kill_job": ".test_kill_job()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L227 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_list_modules_exploit": ".test_list_modules_exploit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L198 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_error_raises": ".test_run_module_error_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L212 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_returns_job_id": ".test_run_module_returns_job_id()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L204 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_integration_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_integration.py:L41 | neighbors=[test_integration.py, Return a minimal valid scan result (no …]
- "tests_test_integration_testfulljoblifecycle_test_complete_flow_with_encrypted_scope": ".test_complete_flow_with_encrypted_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L314 | neighbors=[Simulate the full probe lifecycle from …, TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_ot_passive_profile": ".test_job_ot_passive_profile()" | kind=code-symbol | source=probe/tests/test_integration.py:L408 | neighbors=[OT passive profile resolves correctly., TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_rejected_all_targets_out_of_scope": ".test_job_rejected_all_targets_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L382 | neighbors=[All targets outside scope → job is reje…, TestFullJobLifecycle]
- "tests_test_integration_testidentityandencryption_test_different_key_cannot_decrypt": ".test_different_key_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_integration.py:L91 | neighbors=[A different probe cannot decrypt scope …, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_full_identity_lifecycle": ".test_full_identity_lifecycle()" | kind=code-symbol | source=probe/tests/test_integration.py:L67 | neighbors=[Generate identity → encrypt scope → dec…, TestIdentityAndEncryption]
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
- "tests_test_probe_core_testassetmergepassivecollect": "TestAssetMergePassiveCollect" | kind=code-symbol | source=probe/tests/test_probe_core.py:L557 | neighbors=[test_probe_core.py, .test_passive_facts_appended()]
- "tests_test_probe_core_testassetmergeservicebanner": "TestAssetMergeServiceBanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L508 | neighbors=[test_probe_core.py, .test_banner_stored()]
- "tests_test_probe_core_testassetmergesmbscan": "TestAssetMergeSmbScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L533 | neighbors=[test_probe_core.py, .test_smb_state_host_level()]
- "tests_test_probe_core_testassetmergetlsscan": "TestAssetMergeTlsScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L517 | neighbors=[test_probe_core.py, .test_tls_facts_stored()]
- "tests_test_probe_core_testassetmergeunknownscanner": "TestAssetMergeUnknownScanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L566 | neighbors=[test_probe_core.py, .test_unknown_scanner_ignored()]
- "tests_test_probe_core_testassetmergewebscan": "TestAssetMergeWebScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L525 | neighbors=[test_probe_core.py, .test_web_facts_stored()]
- "tests_test_probe_core_testassetneedsrechecklive_test_never_seen": ".test_never_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L450 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_recently_seen": ".test_recently_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L454 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_stale": ".test_stale()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L458 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L471 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_only_open": ".test_only_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L464 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testcacheentry": "TestCacheEntry" | kind=code-symbol | source=probe/tests/test_probe_core.py:L618 | neighbors=[test_probe_core.py, .test_roundtrip()]
- "tests_test_probe_core_testcacheentry_test_roundtrip": ".test_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L619 | neighbors=[TestCacheEntry, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_error_overrides": ".test_error_overrides()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L609 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_host_discovery_uncertain": ".test_host_discovery_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L605 | neighbors=[TestClassifyCertainty, _scan_result()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-057.json

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
