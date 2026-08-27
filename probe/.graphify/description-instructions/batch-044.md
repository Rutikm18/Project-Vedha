# Node Description Batch 45 of 92

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

- "tests_test_installer_contract_test_installer_without_token_still_shows_manual_approval": "test_installer_without_token_still_shows_manual_approval()" | kind=code-symbol | source=tests/test_installer_contract.py:L76 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_integration_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=tests/test_integration.py:L41 | neighbors=[test_integration.py, Return a minimal valid scan result (no …]
- "tests_test_integration_testfulljoblifecycle_test_complete_flow_with_encrypted_scope": ".test_complete_flow_with_encrypted_scope()" | kind=code-symbol | source=tests/test_integration.py:L314 | neighbors=[Simulate the full probe lifecycle from …, TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_ot_passive_profile": ".test_job_ot_passive_profile()" | kind=code-symbol | source=tests/test_integration.py:L408 | neighbors=[OT passive profile resolves correctly., TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_rejected_all_targets_out_of_scope": ".test_job_rejected_all_targets_out_of_scope()" | kind=code-symbol | source=tests/test_integration.py:L382 | neighbors=[All targets outside scope → job is reje…, TestFullJobLifecycle]
- "tests_test_integration_testidentityandencryption_test_different_key_cannot_decrypt": ".test_different_key_cannot_decrypt()" | kind=code-symbol | source=tests/test_integration.py:L91 | neighbors=[A different probe cannot decrypt scope …, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_full_identity_lifecycle": ".test_full_identity_lifecycle()" | kind=code-symbol | source=tests/test_integration.py:L67 | neighbors=[Generate identity → encrypt scope → dec…, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_scope_encryption_roundtrip": ".test_scope_encryption_roundtrip()" | kind=code-symbol | source=tests/test_integration.py:L78 | neighbors=[Manager encrypts → probe decrypts., TestIdentityAndEncryption]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_hw_bind_blocks": ".test_gauntlet_hw_bind_blocks()" | kind=code-symbol | source=tests/test_integration.py:L442 | neighbors=[Wrong HW fingerprint blocks startup., TestStartupGauntlet]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_skips_in_dev_mode": ".test_gauntlet_skips_in_dev_mode()" | kind=code-symbol | source=tests/test_integration.py:L434 | neighbors=[With LICENSE_ENFORCED=false, gauntlet r…, TestStartupGauntlet]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_decrypts_encrypted_scope_from_job": ".test_decrypts_encrypted_scope_from_job()" | kind=code-symbol | source=tests/test_integration.py:L103 | neighbors=[Job carries encrypted_scope → TaskRunne…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_falls_back_when_decryption_fails": ".test_falls_back_when_decryption_fails()" | kind=code-symbol | source=tests/test_integration.py:L135 | neighbors=[Wrong key → decryption fails → graceful…, TestTaskRunnerWithEncryptedScope]
- "tests_test_integration_testtransportwithidentity_test_register_without_public_key": ".test_register_without_public_key()" | kind=code-symbol | source=tests/test_integration.py:L259 | neighbors=[Backward compat: registration without p…, TestTransportWithIdentity]
- "tests_test_main_scripts_completeness_test_fallback_count_based_when_no_requested_set": "test_fallback_count_based_when_no_requested_set()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L64 | neighbors=[test_main_scripts_completeness.py, _rec()]
- "tests_test_main_scripts_correlation_test_correlations_are_evidence_backed": "test_correlations_are_evidence_backed()" | kind=code-symbol | source=tests/test_main_scripts_correlation.py:L91 | neighbors=[test_main_scripts_correlation.py, _run()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts": ".test_adaptive_estimator_is_shared_and_adapts_down_from_fast_rtts()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L195 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_default_ports_are_nmap_top100_not_the_35_port_set": ".test_default_ports_are_nmap_top100_not_the_35_port_set()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L187 | neighbors=[TestDefaultsAndAdaptiveTimeout, _scope()]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout_test_fixed_timeout_flag_disables_the_estimator": ".test_fixed_timeout_flag_disables_the_estimator()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L214 | neighbors=[TestDefaultsAndAdaptiveTimeout, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_all_65535_ports_scheduled_exactly_once": ".test_all_65535_ports_scheduled_exactly_once()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L103 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_concurrency_is_bounded_by_the_pool": ".test_concurrency_is_bounded_by_the_pool()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L117 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner()]
- "tests_test_main_scripts_datastore_probe_test_elasticsearch_and_couchdb_win_over_generic_http": "test_elasticsearch_and_couchdb_win_over_generic_http()" | kind=code-symbol | source=tests/test_main_scripts_datastore_probe.py:L31 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_memcached_version_and_stat_identify_as_memcached": "test_memcached_version_and_stat_identify_as_memcached()" | kind=code-symbol | source=tests/test_main_scripts_datastore_probe.py:L26 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_datastore_probe_test_redis_info_and_noauth_identify_as_redis": "test_redis_info_and_noauth_identify_as_redis()" | kind=code-symbol | source=tests/test_main_scripts_datastore_probe.py:L21 | neighbors=[test_main_scripts_datastore_probe.py, _svc()]
- "tests_test_main_scripts_device_testclassifyfromresults": "TestClassifyFromResults" | kind=code-symbol | source=tests/test_main_scripts_device.py:L71 | neighbors=[test_main_scripts_device.py, .test_extracts_signals_from_scan_result…]
- "tests_test_main_scripts_errno_test_definitive_states": "test_definitive_states()" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L21 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_describe_os_error_is_fully_debuggable": "test_describe_os_error_is_fully_debuggable()" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L49 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_scanner_side_errors_are_error_not_filtered": "test_scanner_side_errors_are_error_not_filtered()" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L28 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_errno_test_unknown_errno_is_self_identifying_and_never_filtered": "test_unknown_errno_is_self_identifying_and_never_filtered()" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L36 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_findings_test_accepts_scanresult_objects_not_just_dicts": "test_accepts_scanresult_objects_not_just_dicts()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L322 | neighbors=[test_main_scripts_findings.py, _ids()]
- "tests_test_main_scripts_findings_test_confirmed_and_port_hint_do_not_double_report": "test_confirmed_and_port_hint_do_not_double_report()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L239 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_ftp_cleartext_is_high_confidence": "test_confirmed_ftp_cleartext_is_high_confidence()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L230 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_redis_is_high_confidence_even_on_nonstandard_port": "test_confirmed_redis_is_high_confidence_even_on_nonstandard_port()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L212 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_dangerous_http_methods_medium": "test_dangerous_http_methods_medium()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L250 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_every_finding_is_evidence_backed": "test_every_finding_is_evidence_backed()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L305 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_exposed_redis_is_high_exposure_medium_confidence": "test_exposed_redis_is_high_exposure_medium_confidence()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L173 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_are_deduped_by_rule_target_port": "test_findings_are_deduped_by_rule_target_port()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L285 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_sorted_most_severe_first": "test_findings_sorted_most_severe_first()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L291 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_missing_security_headers_is_low": "test_missing_security_headers_is_low()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L262 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_no_finding_carries_a_cve_id": "test_no_finding_carries_a_cve_id()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L299 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed": "test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L223 | neighbors=[test_main_scripts_findings.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-044.json

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
