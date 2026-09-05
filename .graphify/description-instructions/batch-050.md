# Node Description Batch 51 of 336

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
- "tests_test_portal_remediation_db_scalar": "_db_scalar()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L32 | neighbors=[test_portal_remediation.py, Each db.execute(...) → result whose .sc…, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_scope_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L30 | neighbors=[test_portal_scope.py, .test_bound_client_returns_engagement(), .test_applies_engagement_filter_for_bou…, .test_matching_request_ok(), .test_mismatched_request_is_403_idor_de…, .test_no_request_returns_bound()]
- "tests_test_portal_scope_testportaltokenisconfinedtoportalroutes": "TestPortalTokenIsConfinedToPortalRoutes" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L107 | neighbors=[test_portal_scope.py, `jwt.py` states the portal audience exi…, .test_auth_routes_are_allowed(), .test_operator_routes_are_rejected(), .test_portal_routes_are_allowed(), .test_prefix_lookalikes_do_not_slip_thr…]
- "tests_test_portal_scope_testrefreshpreservesaudienceandscope": "TestRefreshPreservesAudienceAndScope" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L140 | neighbors=[test_portal_scope.py, `/auth/refresh` must re-mint the SAME c…, ._db_returning(), .test_client_refresh_keeps_portal_aud_a…, .test_operator_refresh_keeps_manager_au…, .test_unbound_client_cannot_refresh_int…]
- "tests_test_posture_confidence_testassessor": "TestAssessor" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L38 | neighbors=[test_posture_confidence.py, .test_deception_penalty(), .test_final_is_clamped_and_recorded(), .test_lone_chain_member_gets_no_floor(), .test_unreachable_downgrades_and_is_rec…, .test_validated_base_higher_than_unvali…]
- "tests_test_posture_rules_testhardenedgroundtruth_host": "._host()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L51 | neighbors=[TestHardenedGroundTruth, _asset(), _fact(), .test_hardened_smb_and_rdp_raise_no_mis…, .test_no_critical_or_high_findings(), .test_rdp_exposed_is_low_because_nla_re…]
- "tests_test_probe_core_testclamp": "TestClamp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L867 | neighbors=[test_probe_core.py, .test_bad_value_uses_default(), .test_clamped_high(), .test_clamped_low(), .test_in_range(), .test_none_uses_default()]
- "tests_test_probe_core_testengagementmodes": "TestEngagementModes" | kind=code-symbol | source=probe/tests/test_probe_core.py:L444 | neighbors=[test_probe_core.py, .test_assessment(), .test_re_scan(), .test_service_specific_invalid_raises(), .test_service_specific_valid(), .test_triage()]
- "tests_test_probe_manifest": "test_probe_manifest.py" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _manifest(), test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…, test_probe_manifest.py — the `agent.age…]
- "tests_test_probe_next_features_cache_with": "_cache_with()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L103 | neighbors=[test_probe_next_features.py, test_device_inventory_post_stage_classi…, test_device_inventory_skips_hosts_witho…, test_exposure_matrix_flags_internet_rea…, test_exposure_matrix_internal_only_from…, test_no_post_stage_for_ordinary_scan_ty…]
- "tests_test_probe_simple_approve": "test_probe_simple_approve.py" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, eff17d6 feat(probe): one-click approve …, _db_names(), TestNextProbeName, TestSimpleApproveInput, test_probe_simple_approve.py — one-clic…]
- "tests_test_probe_simple_approve_db_names": "_db_names()" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L11 | neighbors=[test_probe_simple_approve.py, db.execute(...).scalars().all() → the g…, .test_first_is_01(), .test_ignores_non_matching_and_non_nume…, .test_increments_past_highest_with_gaps…, .test_legacy_probe_names_still_advance_…]
- "tests_test_project_timezone": "test_project_timezone.py" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, TestFileStamps, TestOverrideAndFallback, TestProjectTimezone, TestScanResultUsesProjectTime, Project timestamps render in IST, and s…]
- "tests_test_project_timezone_testfilestamps": "TestFileStamps" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L49 | neighbors=[test_project_timezone.py, .test_custom_format_is_honoured(), .test_file_stamp_has_no_z_suffix(), .test_file_stamp_is_filename_safe(), .test_file_stamp_is_local_wall_clock(), .test_file_stamp_sorts_chronologically()]
- "tests_test_reference_at": "_at()" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L23 | neighbors=[test_reference.py, .test_reads_as_prefix_date_code(), .test_uses_the_rows_own_date_not_today(), .test_the_same_row_always_gets_the_same…, .test_typed_back_lowercase_still_resolv…, .test_a_reference_is_distinguishable_fr…]
- "tests_test_remediation_kb": "test_remediation_kb.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L1 | neighbors=[fd5dc96 feat(remediation): AI + determi…, _f(), TestClassify, TestRecipeForFinding, TestRecipeShape, test_remediation_kb.py — the pure deter…]
- "tests_test_remediation_kb_testrecipeforfinding": "TestRecipeForFinding" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L59 | neighbors=[test_remediation_kb.py, .test_missing_os_defaults_to_generic(), .test_network_os_falls_back_to_generic_…, .test_returns_kb_source_and_category(), .test_steps_are_numbered_and_os_filtere…, .test_unknown_finding_yields_generic_pl…]
- "tests_test_remediation_routes_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L31 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cached_ai_on_hit(), .test_kb_on_cache_miss()]
- "tests_test_remediation_routes_scalar_result": "_scalar_result()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L47 | neighbors=[test_remediation_routes.py, .execute(), .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-050.json

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
