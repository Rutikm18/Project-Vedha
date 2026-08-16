# Node Description Batch 103 of 209

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

- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]
- "tests_test_finding_verification_api": "test_finding_verification_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L1 | neighbors=[72f68af feat(verification): expose veri…, test_finding_schema_exposes_verificatio…]
- "tests_test_finding_verification_schema": "test_finding_verification_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, test_finding_has_verification_columns()]
- "tests_test_installer_contract_test_installer_accepts_enroll_token_and_insecure_for_http_manager": "test_installer_accepts_enroll_token_and_insecure_for_http_manager()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L62 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_installer_contract_test_installer_without_token_still_shows_manual_approval": "test_installer_without_token_still_shows_manual_approval()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L76 | neighbors=[test_installer_contract.py, _dry_run()]
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
- "tests_test_loaders_testloadepsserrors_test_epss_get_returns_none_for_unknown_cve": ".test_epss_get_returns_none_for_unknown_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L172 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadepsserrors_test_valid_epss_loads": ".test_valid_epss_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L164 | neighbors=[TestLoadEpssErrors, _valid_epss()]
- "tests_test_loaders_testloadkeverrors_test_valid_kev_loads": ".test_valid_kev_loads()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L138 | neighbors=[TestLoadKevErrors, _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors_test_error_message_mentions_re_sync": ".test_error_message_mentions_re_sync()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L101 | neighbors=[The FileNotFoundError message should me…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_malformed_json_raises": ".test_malformed_json_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L77 | neighbors=[Completely broken JSON must propagate a…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_file_raises_file_not_found": ".test_missing_file_raises_file_not_found()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L59 | neighbors=[A path that doesn't exist must raise Fi…, TestLoadSnapshotErrors]
- "tests_test_loaders_testloadsnapshoterrors_test_missing_required_key_raises": ".test_missing_required_key_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L85 | neighbors=[A JSON file that is valid JSON but miss…, TestLoadSnapshotErrors]
- "tests_test_loaders_valid_kev": "_valid_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L42 | neighbors=[test_loaders.py, .test_valid_kev_loads()]
- "tests_test_main_scripts_completeness_test_fallback_count_based_when_no_requested_set": "test_fallback_count_based_when_no_requested_set()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L64 | neighbors=[test_main_scripts_completeness.py, _rec()]
- "tests_test_main_scripts_correlation_test_correlations_are_evidence_backed": "test_correlations_are_evidence_backed()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L91 | neighbors=[test_main_scripts_correlation.py, _run()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts": ".test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L195 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_default_ports_are_nmap_top100_not_the_35_port_set": ".test_default_ports_are_nmap_top100_not_the_35_port_set()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L187 | neighbors=[TestDefaultsAndAdaptiveTimeout, _scope()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_fixed_timeout_flag_disables_the_estimator": ".test_fixed_timeout_flag_disables_the_estimator()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L214 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_all_65535_ports_scheduled_exactly_once": ".test_all_65535_ports_scheduled_exactly_once()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L103 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_concurrency_is_bounded_by_the_pool": ".test_concurrency_is_bounded_by_the_pool()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L117 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_datastore_probe_test_elasticsearch_and_couchdb_win_over_generic_http": "test_elasticsearch_and_couchdb_win_over_generic_http()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L31 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_memcached_version_and_stat_identify_as_memcached": "test_memcached_version_and_stat_identify_as_memcached()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L26 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_redis_info_and_noauth_identify_as_redis": "test_redis_info_and_noauth_identify_as_redis()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L21 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_device_testclassifyfromresults": "TestClassifyFromResults" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L71 | neighbors=[test_main_scripts_device.py, .test_extracts_signals_from_scan_result…]
- "tests_test_main_scripts_errno_test_definitive_states": "test_definitive_states()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L21 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_describe_os_error_is_fully_debuggable": "test_describe_os_error_is_fully_debuggable()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L49 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_scanner_side_errors_are_error_not_filtered": "test_scanner_side_errors_are_error_not_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L28 | neighbors=[test_main_scripts_errno.py, _oserr()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-102.json

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
