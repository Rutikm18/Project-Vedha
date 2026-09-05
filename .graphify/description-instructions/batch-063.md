# Node Description Batch 64 of 336

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

- "tests_test_integrations_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L17 | neighbors=[test_integrations.py, .test_list_masks_secret(), .test_create_encrypts_secret_and_masks_…, .test_rejects_unknown_kind(), .test_update_without_secret_keeps_exist…]
- "tests_test_ipmi_scanner_testwireformat": "TestWireFormat" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L23 | neighbors=[test_ipmi_scanner.py, .test_open_session_request_offers_ciphe…, .test_parse_nonzero_status_is_safe(), .test_parse_rejects_non_response(), .test_parse_status_zero_is_cipher_zero()]
- "tests_test_ipv6_discovery": "test_ipv6_discovery.py" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, ipv6_discovery.py, TestDiscoverFiltering, TestParsers, test_ipv6_discovery.py — FIX 3: IPv6 ne…]
- "tests_test_ipv6_wiring_run": "_run()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L96 | neighbors=[test_ipv6_wiring.py, test_discovery_failure_does_not_abort_t…, test_in_scope_neighbour_is_added_and_sc…, test_out_of_scope_neighbour_is_reported…, test_the_fact_records_both_sides()]
- "tests_test_job_attempt_service": "test_job_attempt_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_attempt_service.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_claim_creates_immutable_attempt_wi…, test_current_fence_renews_attempt_and_l…, test_lost_claim_does_not_create_attempt…, test_stale_fence_cannot_renew_attempt()]
- "tests_test_job_cancel_test_terminal_jobs_cannot_be_cancelled": "test_terminal_jobs_cannot_be_cancelled()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L156 | neighbors=[test_job_cancel.py, _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_testqueuelimit": "TestQueueLimit" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L182 | neighbors=[test_job_cancel.py, .test_fourth_queued_job_is_refused(), .test_limit_is_three(), .test_pending_count_helper_counts(), .test_third_queued_job_is_still_accepte…]
- "tests_test_job_cancel_testqueuelimit_test_fourth_queued_job_is_refused": ".test_fourth_queued_job_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L192 | neighbors=[TestQueueLimit, _count(), _db(), _one(), _user()]
- "tests_test_loaders_testloadkeverrors": "TestLoadKevErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L124 | neighbors=[test_loaders.py, .setup_method(), .test_malformed_kev_json_raises(), .test_missing_kev_file_raises(), .test_valid_kev_loads()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]
- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_rdp_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L137 | neighbors=[test_main_scripts_rdp.py, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…, test_confirmed_rdp_without_nla_is_high_…, test_nla_required_rdp_is_low_severity_n…]
- "tests_test_msrpc_scanner_testdynamicports": "TestDynamicPorts" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L27 | neighbors=[test_msrpc_scanner.py, EPM bindings carry the dynamic RPC port…, .test_extract_tcp_and_dynamic(), .test_out_of_range_port_dropped(), .test_summarize_surfaces_dynamic_ports()]
- "tests_test_msrpc_scanner_testmsrpcscanner": "TestMSRPCScanner" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L56 | neighbors=[test_msrpc_scanner.py, ._sc(), .test_impacket_missing_is_error(), .test_no_msrpc_filtered(), .test_open()]
- "tests_test_network_va_accuracy_va_scan": "va_scan()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L78 | neighbors=[test_network_va_accuracy.py, One real network_va against loopback wi…, _Listener, .start(), .stop()]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L361 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_nfs_scanner_mount_export_reply": "_mount_export_reply()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L30 | neighbors=[test_nfs_scanner.py, _xstr(), .test_main_scripts(), .test_mount_export_parse_and_world_flag…, .test_rpc_reply_header_stripping()]
- "tests_test_online_testclionlineflag": "TestCliOnlineFlag" | kind=code-symbol | source=probe/tests/test_online.py:L180 | neighbors=[test_online.py, ._db(), ._facts(), .test_no_online_flag_skips_enrichment(), .test_online_flag_invokes_enrichment()]
- "tests_test_online_testlookupnvd": "TestLookupNvd" | kind=code-symbol | source=probe/tests/test_online.py:L77 | neighbors=[test_online.py, .test_empty_result_is_none(), .test_garbage_json_is_fail_open(), .test_network_error_is_fail_open(), .test_parses_score_severity_refs()]
- "tests_test_online_testlookupvulners": "TestLookupVulners" | kind=code-symbol | source=probe/tests/test_online.py:L100 | neighbors=[test_online.py, .test_error_is_none(), .test_exploit_present_is_true(), .test_no_exploit_is_false(), .test_no_key_returns_none()]
- "tests_test_os_fingerprint_testacceptechoreply_reply": "._reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L170 | neighbors=[TestAcceptEchoReply, .test_accepts_echo_reply_from_target(), .test_accepts_when_source_unknown(), .test_rejects_non_echo_type(), .test_rejects_reply_from_a_different_ho…]
- "tests_test_os_fingerprint_testicmpbuilders": "TestIcmpBuilders" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L37 | neighbors=[test_os_fingerprint.py, .test_address_mask_request_type(), .test_echo_payload_preserved(), .test_echo_request_type_and_checksum(), .test_timestamp_request_type()]
- "tests_test_os_fingerprint_testicmpparse": "TestIcmpParse" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L62 | neighbors=[test_os_fingerprint.py, ._ip_icmp(), .test_parse_extracts_ttl_and_type(), .test_parse_raw_icmp_without_ip_header(), .test_parse_rejects_short()]
- "tests_test_os_fingerprint_testicmptimestamps": "TestIcmpTimestamps" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L95 | neighbors=[test_os_fingerprint.py, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit(), .test_parse_rejects_short_body(), ._ts_reply()]
- "tests_test_os_fingerprint_testsmbbuildenrichment": "TestSmbBuildEnrichment" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L328 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_build_lifts_ttl_only_guess_to_aut…, .test_no_smb_leaves_ttl_only_result_unt…, .test_smb_build_can_be_disabled()]
- "tests_test_os_stage_wiring_testgate": "TestGate" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L36 | neighbors=[test_os_stage_wiring.py, .test_alive_host_is_eligible(), .test_dead_host_is_not(), .test_no_open_ports_still_eligible(), .test_passive_profile_never_probes()]
- "tests_test_os_stage_wiring_testplan": "TestPlan" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L52 | neighbors=[test_os_stage_wiring.py, .test_full_assessment_includes_it(), .test_not_planned_for_a_udp_only_job(), .test_not_planned_for_liveness_only(), .test_os_stage_planned_from_the_port_st…]
- "tests_test_os_stage_wiring_wire": "_wire()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L115 | neighbors=[test_os_stage_wiring.py, test_cached_os_fact_is_reused_not_repro…, test_os_stage_runs_for_a_port_stage_job…, test_rescan_mode_reprobes_a_stale_os_fa…, test_stack_hints_from_syn_scan_reach_th…]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_perf_optimization_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L103 | neighbors=[test_perf_optimization.py, test_clear_caches_forces_reload(), test_load_snapshot_memoized_returns_sam…, test_load_snapshot_reloads_after_file_c…, test_load_snapshot_runs_dpkg_guard_once…]
- "tests_test_pipeline_testrunpipelineexposure_test_exposure_internet_facing_propagates": ".test_exposure_internet_facing_propagates()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L248 | neighbors=[TestRunPipelineExposure, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinereturnvalue_test_returns_tuple_of_findings_and_ingest_result": ".test_returns_tuple_of_findings_and_ingest_result()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L307 | neighbors=[TestRunPipelineReturnValue, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_portal_assistant_test_model_failure_surfaces_its_status_not_a_500": "test_model_failure_surfaces_its_status_not_a_500()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L221 | neighbors=[test_portal_assistant.py, _ask(), _client(), _db(), _engagement()]
- "tests_test_portal_read_db_first": "_db_first()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L152 | neighbors=[test_portal_read.py, Each db.execute(...) → result whose .sc…, .test_creates_pending_request_and_audit…, .test_duplicate_pending_is_conflict(), .test_operator_cannot_create()]
- "tests_test_portal_read_db_scalar": "_db_scalar()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L47 | neighbors=[test_portal_read.py, .test_single_finding_404_when_out_of_sc…, .test_engagement_summary(), .test_download_returns_content_for_appr…, .test_unapproved_or_missing_report_is_4…]
- "tests_test_portal_read_testcreatescanrequest_test_creates_pending_request_with_targets_and_intensity": ".test_creates_pending_request_with_targets_and_intensity()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L243 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_whole_scope_when_no_targets": ".test_whole_scope_when_no_targets()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L258 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_for_create(), _engagement()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-063.json

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
