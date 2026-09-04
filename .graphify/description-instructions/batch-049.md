# Node Description Batch 50 of 330

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

- "tests_test_engine_bridge_ingest_health": "test_engine_bridge_ingest_health.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, test_census_survives_an_engine_that_ret…, test_healthy_facts_ingest_completely_an…, test_partial_drift_still_detects_but_re…, test_total_shape_drift_is_reported_not_…, test_engine_bridge_ingest_health.py — a…]
- "tests_test_exploit_engine_testmetasploitrpcclient_make_client": "._make_client()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L183 | neighbors=[TestMetasploitRPCClient, .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit(), .test_run_module_error_raises(), .test_run_module_returns_job_id()]
- "tests_test_finding_events_testmerge": "TestMerge" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L92 | neighbors=[test_finding_events.py, ._stored(), ._synth(), .test_labels_attached(), .test_sorted_oldest_first(), .test_stored_supersedes_synthesized_sam…]
- "tests_test_finding_section_testfindingsection_sum": "._sum()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L48 | neighbors=[TestFindingSection, .test_backward_compatible_keys_kept(), .test_clean_host_shows_no_findings_hone…, .test_each_finding_tagged_with_verified…, .test_findings_are_ranked_worst_first(), .test_vulnerable_host_shows_ranked_vuln…]
- "tests_test_finding_section_testscannerregistry": "TestScannerRegistry" | kind=code-symbol | source=probe/tests/test_finding_section.py:L17 | neighbors=[test_finding_section.py, .test_registry_aligns_with_manager_vali…, .test_unknown_scanner_is_not_trusted(), .test_unvalidated_scanners_are_not_veri…, .test_user_validated_scanners_are_verif…, .test_verification_report_shape()]
- "tests_test_host_discovery_mobile_testdevicehint": "TestDeviceHint" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L52 | neighbors=[test_host_discovery_mobile.py, .test_iphone_lockdownd_port(), .test_mobile_vendor(), .test_no_signal(), .test_plain_vendor_passthrough(), .test_randomized_mac_is_mobile()]
- "tests_test_host_health_testverdict": "TestVerdict" | kind=code-symbol | source=probe/tests/test_host_health.py:L83 | neighbors=[test_host_health.py, .test_a_broken_liveness_probe_never_abo…, .test_firewalled_host_that_still_answer…, .test_flaky_host_can_be_suspected_again…, .test_host_that_stopped_answering_is_of…, .test_no_recheck_is_spent_below_thresho…]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py, 2885afa Add comprehensive probe testing…]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=probe/tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=probe/tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_integrations": "test_integrations.py" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, _db(), _operator(), TestListIntegrations, TestPutIntegration, test_integrations.py — operator notific…]
- "tests_test_ipv6_discovery_testdiscoverfiltering_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L39 | neighbors=[TestDiscoverFiltering, .test_dedups(), .test_excludes_own_addresses(), .test_keeps_usable_drops_dead_states(), .test_link_local_can_be_excluded(), .test_never_raises_on_empty()]
- "tests_test_ipv6_wiring_wire": "_wire()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L73 | neighbors=[test_ipv6_wiring.py, test_disabled_by_default(), test_discovery_failure_does_not_abort_t…, test_in_scope_neighbour_is_added_and_sc…, test_out_of_scope_neighbour_is_reported…, test_the_fact_records_both_sides()]
- "tests_test_job_cancel_probe": "test_job_cancel_probe.py" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, transport.py, TestHeartbeatOutcomes, TestPollingNoiseIsSuppressed, transport(), Probe-side operator job control + polli…]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_configure": "._configure()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L77 | neighbors=[TestPollingNoiseIsSuppressed, .test_per_request_info_lines_are_suppre…, .test_probe_debug_restores_full_tracing…, .test_probe_own_narration_is_unaffected…, .test_transport_errors_still_surface(), .test_transport_loggers_are_quiet_by_de…]
- "tests_test_job_cancel_test_missing_attempt_row_does_not_break_cancel": "test_missing_attempt_row_does_not_break_cancel()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L143 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_open_attempt_is_closed_as_cancelled": "test_open_attempt_is_closed_as_cancelled()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L128 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_pending_job_is_cancelled_and_freed": "test_pending_job_is_cancelled_and_freed()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L78 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_running_job_bumps_the_fence_to_abort_the_probe": "test_running_job_bumps_the_fence_to_abort_the_probe()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L102 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_running_job_releases_the_agent_for_the_next_queued_job": "test_running_job_releases_the_agent_for_the_next_queued_job()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L115 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_testqueuelimit_test_third_queued_job_is_still_accepted": ".test_third_queued_job_is_still_accepted()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L207 | neighbors=[Two queued jobs must leave room for a t…, TestQueueLimit, _count(), _db(), _one(), _user()]
- "tests_test_loaders_testloadepsserrors": "TestLoadEpssErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L150 | neighbors=[test_loaders.py, .setup_method(), .test_epss_get_returns_none_for_unknown…, .test_malformed_epss_json_raises(), .test_missing_epss_file_raises(), .test_valid_epss_loads()]
- "tests_test_main_scripts_completeness_metrics": "_metrics()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L15 | neighbors=[test_main_scripts_completeness.py, test_duplicate_port_is_detected(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely…, test_summary_exposes_missing_and_duplic…]
- "tests_test_main_scripts_hardening_testsmbparsing": "TestSmbParsing" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L131 | neighbors=[test_main_scripts_hardening.py, .test_error_response_not_trusted(), .test_negotiate_request_offers_smb311_w…, .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…, .test_negotiate_request_excludes_smb311…]
- "tests_test_main_scripts_vantage": "test_main_scripts_vantage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, vantage_matrix.py, _r(), TestReconcileVantages, test_main_scripts_vantage.py — multi-va…]
- "tests_test_nessus_scanner_mock_response": "_mock_response()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L25 | neighbors=[test_nessus_scanner.py, test_create_scan(), test_create_scan_with_credentials(), test_launch_scan(), test_poll_status_completed(), test_poll_status_running()]
- "tests_test_new_scanners_teststablehostid": "TestStableHostId" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L331 | neighbors=[test_new_scanners.py, .test_hostname_second_priority(), .test_ip_fallback(), .test_mac_normalises_dashes(), .test_mac_takes_priority(), .test_zero_mac_skipped()]
- "tests_test_nfs_scanner_testxdrparsers": "TestXdrParsers" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L51 | neighbors=[test_nfs_scanner.py, .test_mount_export_parse_and_world_flag…, .test_parser_is_bounded(), .test_portmap_dump_parse(), .test_rpc_reply_header_stripping(), .test_world_readable_logic()]
- "tests_test_nmap_wrapper": "test_nmap_wrapper.py" | kind=code-symbol | source=probe/tests/test_nmap_wrapper.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, nmap_wrapper.py, test_filtered_ports_not_emitted_as_open…, test_open_ports_are_emitted(), test_port_scan_profiles_carry_pn(), test_nmap_wrapper.py — the "nmap return…]
- "tests_test_os_fusion_os": "_os()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L12 | neighbors=[test_os_fusion.py, test_build_only_is_strong_but_not_certa…, test_build_smb2_hostname_is_high_confid…, test_no_os_signal_yields_no_finding(), test_smb2_plus_p0f_stack_is_medium(), test_ttl_only_stays_a_hint()]
- "tests_test_os_stage_wiring_testassetmerge": "TestAssetMerge" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L77 | neighbors=[test_os_stage_wiring.py, .test_closed_port_contributes_no_hints(), .test_connect_scan_without_stack_signal…, .test_os_fact_is_cacheable_as_determini…, .test_os_fact_stored_and_ntlm_name_beco…, .test_syn_stack_hints_harvested_from_op…]
- "tests_test_passive_collector_writer": "_Writer" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L15 | neighbors=[test_passive_collector.py, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…, test_subset_listener_failure_reports_de…, .__init__(), .write()]
- "tests_test_pipeline_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L40 | neighbors=[test_pipeline.py, _openssh_upstream_vuln_db(), _openssh_vuln_db(), .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty(), .test_injected_dbs_used_no_file_io()]
- "tests_test_pipeline_testrunpipelineemptyinput_test_no_paths_returns_empty": ".test_no_paths_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L140 | neighbors=[Passing an empty path list must return …, TestRunPipelineEmptyInput, _empty_epss(), _empty_kev(), _mock_vuln_db(), Passing an empty path list must return …]
- "tests_test_pipeline_testrunpipelinevulnmatching_test_full_detection_exposes_authoritative_suppression_audit": ".test_full_detection_exposes_authoritative_suppression_audit()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L215 | neighbors=[TestRunPipelineVulnMatching, _banner_jsonl(), _empty_epss(), _empty_kev(), _openssh_upstream_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_portal_assistant_test_reply_is_timestamped_and_attributed": "test_reply_is_timestamped_and_attributed()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L232 | neighbors=[test_portal_assistant.py, _ask(), _client(), _db(), _engagement(), _llm()]
- "tests_test_portal_assistant_test_the_exchange_is_audited": "test_the_exchange_is_audited()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L241 | neighbors=[test_portal_assistant.py, _ask(), _client(), _db(), _engagement(), _llm()]
- "tests_test_portal_assistant_test_uses_the_security_restricted_task": "test_uses_the_security_restricted_task()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L167 | neighbors=[test_portal_assistant.py, _ask(), _client(), _db(), _engagement(), _llm()]
- "tests_test_portal_metrics": "test_portal_metrics.py" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _f(), TestOpenClosed, TestSeverityBreakdown, TestStatusTimeline, test_portal_metrics.py — pure dashboard…]
- "tests_test_portal_metrics_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L14 | neighbors=[test_portal_metrics.py, .test_counts_by_status_and_resolved_at(), .test_open_only_excludes_closed(), .test_unknown_severity_falls_into_info(), .test_activity_outside_window_is_ignore…, .test_buckets_opened_and_closed()]

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
