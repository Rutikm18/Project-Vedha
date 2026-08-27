# Node Description Batch 48 of 236

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

- "tests_test_job_attempt_service": "test_job_attempt_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_claim_creates_immutable_attempt_wi…, test_current_fence_renews_attempt_and_l…, test_lost_claim_does_not_create_attempt…, test_stale_fence_cannot_renew_attempt()]
- "tests_test_loaders_testloadkeverrors": "TestLoadKevErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L124 | neighbors=[test_loaders.py, .setup_method(), .test_malformed_kev_json_raises(), .test_missing_kev_file_raises(), .test_valid_kev_loads()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]
- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_hardening_testsmbparsing": "TestSmbParsing" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L131 | neighbors=[test_main_scripts_hardening.py, .test_error_response_not_trusted(), .test_negotiate_request_excludes_smb311…, .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L361 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_os_fingerprint_testacceptechoreply_reply": "._reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L170 | neighbors=[TestAcceptEchoReply, .test_accepts_echo_reply_from_target(), .test_accepts_when_source_unknown(), .test_rejects_non_echo_type(), .test_rejects_reply_from_a_different_ho…]
- "tests_test_os_fingerprint_testicmpbuilders": "TestIcmpBuilders" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L37 | neighbors=[test_os_fingerprint.py, .test_address_mask_request_type(), .test_echo_payload_preserved(), .test_echo_request_type_and_checksum(), .test_timestamp_request_type()]
- "tests_test_os_fingerprint_testicmpparse": "TestIcmpParse" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L62 | neighbors=[test_os_fingerprint.py, ._ip_icmp(), .test_parse_extracts_ttl_and_type(), .test_parse_raw_icmp_without_ip_header(), .test_parse_rejects_short()]
- "tests_test_os_fingerprint_testicmptimestamps": "TestIcmpTimestamps" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L95 | neighbors=[test_os_fingerprint.py, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit(), .test_parse_rejects_short_body(), ._ts_reply()]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_perf_optimization_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L103 | neighbors=[test_perf_optimization.py, test_clear_caches_forces_reload(), test_load_snapshot_memoized_returns_sam…, test_load_snapshot_reloads_after_file_c…, test_load_snapshot_runs_dpkg_guard_once…]
- "tests_test_pipeline_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L40 | neighbors=[test_pipeline.py, _openssh_vuln_db(), .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty(), .test_injected_dbs_used_no_file_io()]
- "tests_test_pipeline_testrunpipelineemptyinput_test_no_paths_returns_empty": ".test_no_paths_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L123 | neighbors=[Passing an empty path list must return …, TestRunPipelineEmptyInput, _empty_epss(), _empty_kev(), _mock_vuln_db()]
- "tests_test_pipeline_testrunpipelineexposure_test_exposure_internet_facing_propagates": ".test_exposure_internet_facing_propagates()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L204 | neighbors=[TestRunPipelineExposure, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinereturnvalue_test_returns_tuple_of_findings_and_ingest_result": ".test_returns_tuple_of_findings_and_ingest_result()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L263 | neighbors=[TestRunPipelineReturnValue, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_portal_read_db_first": "_db_first()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L152 | neighbors=[test_portal_read.py, Each db.execute(...) → result whose .sc…, .test_creates_pending_request_and_audit…, .test_duplicate_pending_is_conflict(), .test_operator_cannot_create()]
- "tests_test_portal_read_db_scalar": "_db_scalar()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L47 | neighbors=[test_portal_read.py, .test_single_finding_404_when_out_of_sc…, .test_engagement_summary(), .test_download_returns_content_for_appr…, .test_unapproved_or_missing_report_is_4…]
- "tests_test_portal_read_testcreatescanrequest_test_creates_pending_request_with_targets_and_intensity": ".test_creates_pending_request_with_targets_and_intensity()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L243 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_whole_scope_when_no_targets": ".test_whole_scope_when_no_targets()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L258 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_for_create(), _engagement()]
- "tests_test_portal_remediation_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L22 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_remediation_testportalremediation": "TestPortalRemediation" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L44 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_probe_core_testenginesummary": "TestEngineSummary" | kind=code-symbol | source=probe/tests/test_probe_core.py:L604 | neighbors=[test_probe_core.py, .test_affirmative_fact_creates_one_dedu…, .test_negative_or_ambiguous_facts_do_no…, .test_open_port_count_deduplicates_conf…, .test_open_port_count_excludes_host_liv…]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L276 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L390 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L405 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L816 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L847 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_probe_simple_approve": "test_probe_simple_approve.py" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L1 | neighbors=[eff17d6 feat(probe): one-click approve …, _db_names(), TestNextProbeName, TestSimpleApproveInput, test_probe_simple_approve.py — one-clic…]
- "tests_test_probe_simple_approve_db_names": "_db_names()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L11 | neighbors=[test_probe_simple_approve.py, db.execute(...).scalars().all() → the g…, .test_first_is_01(), .test_ignores_non_matching_and_non_nume…, .test_increments_past_highest_with_gaps…]
- "tests_test_remediation_kb_testclassify": "TestClassify" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L16 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic()]
- "tests_test_remediation_routes_testgenerateremediation": "TestGenerateRemediation" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L138 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404()]
- "tests_test_remediation_routes_testgenerateremediation_test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed": ".test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L159 | neighbors=[TestGenerateRemediation, _FakeDB, _finding(), _operator(), _scalar_result()]
- "tests_test_remediation_upsert_integration": "test_remediation_upsert_integration.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, _run(), _stmt(), test_upsert_resets_gate_and_is_race_saf…, test_remediation_upsert_integration.py …]
- "tests_test_resolve_infos": "_infos()" | kind=code-symbol | source=probe/tests/test_resolve.py:L11 | neighbors=[test_resolve.py, Fake getaddrinfo results: (family, sock…, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…]
- "tests_test_resolve_testresolvefamily": "TestResolveFamily" | kind=code-symbol | source=probe/tests/test_resolve.py:L20 | neighbors=[test_resolve.py, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…, .test_unresolvable_raises()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
