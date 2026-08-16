# Node Description Batch 42 of 209

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

- "tests_test_agents_testregisteragent": "TestRegisterAgent" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L637 | neighbors=[test_agents.py, .test_agent_token_is_long_lived(), .test_creates_when_none_exists(), .test_reuses_existing_probe_by_name(), ScanJobType]
- "tests_test_agents_testregisteragent_test_agent_token_is_long_lived": ".test_agent_token_is_long_lived()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L675 | neighbors=[Agent token must outlive the 15-min acc…, TestRegisterAgent, _user(), Agent token must outlive the 15-min acc…, Agent token must outlive the 15-min acc…]
- "tests_test_agents_testregisteragent_test_reuses_existing_probe_by_name": ".test_reuses_existing_probe_by_name()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L640 | neighbors=[Re-registering the same-named probe mus…, TestRegisterAgent, _user(), Re-registering the same-named probe mus…, Re-registering the same-named probe mus…]
- "tests_test_ai_engine_resp": "_resp()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L165 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard()]
- "tests_test_ai_engine_testllmreportgenerator_test_technical_finding_runs_guard": ".test_technical_finding_runs_guard()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L205 | neighbors=[TestLLMReportGenerator, _asset(), _finding(), _mock_db(), _resp()]
- "tests_test_ai_normalizer_testainormalizercache": "TestAINormalizerCache" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L123 | neighbors=[test_ai_normalizer.py, .test_cache_persists_across_instances(), .test_get_returns_none_on_miss(), .test_key_is_content_hash_not_plaintext…, .test_put_and_get_roundtrip()]
- "tests_test_attack_path_correlation_ids": "_ids()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L15 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_correlation_is_host_scoped(), test_exposed_db_without_unauth_does_not…, test_no_relay_when_signing_required()]
- "tests_test_customer_access_pending_request": "_pending_request()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L142 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_reject_records_reason()]
- "tests_test_customer_access_testapprovescanrequest_test_approve_dispatches_job_and_links_it": ".test_approve_dispatches_job_and_links_it()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L151 | neighbors=[TestApproveScanRequest, _added(), _mock_db(), _operator(), _pending_request()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L787 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L809 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L801 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L825 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L817 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_device_identity": "test_device_identity.py" | kind=code-symbol | source=probe/tests/test_device_identity.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, device_identity.py, test_device_identity_rejects_invalid_pr…, test_device_identity_round_trip_and_sig…, test_site_policy_signature_and_tofu_pin…]
- "tests_test_e2e_engagement_to_findings_manager": "_manager()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L51 | neighbors=[test_e2e_engagement_to_findings.py, Return (http_get, submit_result, captur…, test_engagement_dispatch_reaches_probe_…, test_out_of_scope_target_is_refused_end…, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_vulnerable_host_facts": "_vulnerable_host_facts()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L137 | neighbors=[test_e2e_engagement_to_findings.py, Exactly what the probe's smb/port scann…, test_correlated_findings_cite_their_bas…, test_manager_correlation_finds_all_thre…, test_ntlm_relay_is_high_when_smbv1_pres…]
- "tests_test_engagement_validation": "test_engagement_validation.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_create_normalizes_name_scopes_and_…, test_create_rejects_invalid_scope_entri…, test_create_rejects_reversed_date_range…, test_update_rejects_blank_name_invalid_…]
- "tests_test_finding_out_computed_base": "_base()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L11 | neighbors=[test_finding_out_computed.py, test_confirmed_exploited_outranks_contr…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_job_attempt_service": "test_job_attempt_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_claim_creates_immutable_attempt_wi…, test_current_fence_renews_attempt_and_l…, test_lost_claim_does_not_create_attempt…, test_stale_fence_cannot_renew_attempt()]
- "tests_test_loaders_testloadkeverrors": "TestLoadKevErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L124 | neighbors=[test_loaders.py, .setup_method(), .test_malformed_kev_json_raises(), .test_missing_kev_file_raises(), .test_valid_kev_loads()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]
- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_hardening_testsmbparsing": "TestSmbParsing" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L131 | neighbors=[test_main_scripts_hardening.py, .test_error_response_not_trusted(), .test_negotiate_request_excludes_smb311…, .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L358 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_os_fingerprint_testicmpbuilders": "TestIcmpBuilders" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L36 | neighbors=[test_os_fingerprint.py, .test_address_mask_request_type(), .test_echo_payload_preserved(), .test_echo_request_type_and_checksum(), .test_timestamp_request_type()]
- "tests_test_os_fingerprint_testicmpparse": "TestIcmpParse" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L61 | neighbors=[test_os_fingerprint.py, ._ip_icmp(), .test_parse_extracts_ttl_and_type(), .test_parse_raw_icmp_without_ip_header(), .test_parse_rejects_short()]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_perf_optimization_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L103 | neighbors=[test_perf_optimization.py, test_clear_caches_forces_reload(), test_load_snapshot_memoized_returns_sam…, test_load_snapshot_reloads_after_file_c…, test_load_snapshot_runs_dpkg_guard_once…]
- "tests_test_pipeline_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L40 | neighbors=[test_pipeline.py, _openssh_vuln_db(), .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty(), .test_injected_dbs_used_no_file_io()]
- "tests_test_pipeline_testrunpipelineemptyinput_test_no_paths_returns_empty": ".test_no_paths_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L123 | neighbors=[Passing an empty path list must return …, TestRunPipelineEmptyInput, _empty_epss(), _empty_kev(), _mock_vuln_db()]
- "tests_test_pipeline_testrunpipelineexposure_test_exposure_internet_facing_propagates": ".test_exposure_internet_facing_propagates()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L204 | neighbors=[TestRunPipelineExposure, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinereturnvalue_test_returns_tuple_of_findings_and_ingest_result": ".test_returns_tuple_of_findings_and_ingest_result()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L263 | neighbors=[TestRunPipelineReturnValue, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
