# Node Description Batch 40 of 332

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_campaign_progress_terminal_testnormalpipelineunaffected": "TestNormalPipelineUnaffected" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L72 | neighbors=[test_campaign_progress_terminal.py, Regression guard: the happy path and it…, .test_complete_campaign(), .test_complete_with_gaps(), .test_defaults_keep_backwards_compatibi…, .test_no_jobs_is_pending()]
- "tests_test_campaign_progress_terminal_testterminalwithoutresults": "TestTerminalWithoutResults" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L38 | neighbors=[test_campaign_progress_terminal.py, .test_a_dead_queue_is_still_reported_as…, .test_all_cancelled_campaign_is_termina…, .test_all_failed_campaign_is_terminal(), .test_does_not_hijack_a_campaign_that_p…, .test_partial_cancel_with_one_success_s…]
- "tests_test_cve_correlation_testcpe": "TestCpe" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L75 | neighbors=[test_cve_correlation.py, .test_datastore_map_entries(), .test_mysql_vs_mariadb_vendor(), .test_no_version_returns_none(), .test_openssh(), .test_unknown_product_returns_none()]
- "tests_test_detection_coverage_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L18 | neighbors=[test_detection_coverage.py, test_aggregating_reason_names_the_outbo…, test_completed_no_blind_is_plain_comple…, test_completed_with_blind_rules_is_comp…, test_explain_all_rules_sorts_gaps_first…, test_explain_no_run_says_never_ran()]
- "tests_test_detection_pipeline_gaps_ctx": "_ctx" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L168 | neighbors=[test_detection_pipeline_gaps.py, .__aenter__(), .__aexit__(), .__init__(), Minimal async-context-manager wrapper a…, test_facts_ready_reads_scanner_runs_fro…]
- "tests_test_detection_pipeline_gaps_fact": "_fact()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L28 | neighbors=[test_detection_pipeline_gaps.py, test_a_non_dict_data_payload_is_quarant…, test_accepted_facts_excludes_what_inges…, test_accepted_facts_falls_back_to_raw_w…, test_facts_ready_reads_scanner_runs_fro…, test_missing_scanner_runs_degrades_to_e…]
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…]
- "tests_test_exposed_services_by_port": "_by_port()" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L29 | neighbors=[test_exposed_services.py, .test_backdoor_4444_is_high_internal(), .test_banner_carried_as_evidence(), .test_internet_facing_escalates_severit…, .test_real_lab_host_produces_expected_f…, .test_detect_uses_service_label_and_fla…]
- "tests_test_exposed_services_testdetect": "TestDetect" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L75 | neighbors=[test_exposed_services.py, .test_backdoor_4444_is_high_internal(), .test_banner_carried_as_evidence(), .test_dedicated_ports_not_double_report…, .test_internet_facing_escalates_severit…, .test_real_lab_host_produces_expected_f…]
- "tests_test_exposed_services_testobservedservicesignals": "TestObservedServiceSignals" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L134 | neighbors=[test_exposed_services.py, .test_basic_auth_over_plaintext_is_clea…, .test_catalog_port_still_wins_its_own_c…, .test_detect_uses_service_label_and_fla…, .test_plain_http_label_on_benign_port_i…, .test_shell_label_is_backdoor_on_any_po…]
- "tests_test_exposure": "test_exposure.py" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_critical_stays_critical(), test_external_escalates_one_rung(), test_non_external_never_escalates(), test_service_exposure_flattens_per_port…, test_service_exposure_ignores_malformed…]
- "tests_test_finding_events_types": "_types()" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L39 | neighbors=[test_finding_events.py, .test_sorted_oldest_first(), .test_manual_remediation_event(), .test_no_reobserved_when_last_seen_equa…, .test_reobserved_when_last_seen_advance…, .test_terminal_confirmed_state_emitted()]
- "tests_test_finding_out_computed_base": "_base()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L11 | neighbors=[test_finding_out_computed.py, test_confirmed_exploited_outranks_contr…, test_detail_asset_context_round_trips_w…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_nested_enrichment_kev_is_part_of_t…]
- "tests_test_finding_reopen_endpoint": "test_finding_reopen_endpoint.py" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L1 | neighbors=[3c277ba feat(lifecycle): add POST /find…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, _db_with(), test_reopen_non_remediated_is_conflict()]
- "tests_test_finding_section_testfindingsection": "TestFindingSection" | kind=code-symbol | source=probe/tests/test_finding_section.py:L47 | neighbors=[test_finding_section.py, ._sum(), .test_backward_compatible_keys_kept(), .test_clean_host_shows_no_findings_hone…, .test_each_finding_tagged_with_verified…, .test_findings_are_ranked_worst_first()]
- "tests_test_fleet_jobs": "test_fleet_jobs.py" | kind=code-symbol | source=manager/backend/tests/test_fleet_jobs.py:L1 | neighbors=[25c014d feat: enhance campaign progress…, _scalars(), test_filter_by_probe_and_engagement_run…, test_lists_jobs_with_probe_and_engageme…, test_running_filter_is_accepted(), _user()]
- "tests_test_ftp_scanner": "test_ftp_scanner.py" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, TestFTPFindings, TestFTPScanner, TestParity, TestPureLogic]
- "tests_test_host_discovery_mobile": "test_host_discovery_mobile.py" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, host_discovery.py, TestDeviceHint, TestLocallyAdministered, TestNormalizeMac, TestVendorLookup]
- "tests_test_host_discovery_mobile_testnormalizemac": "TestNormalizeMac" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L9 | neighbors=[test_host_discovery_mobile.py, .test_extracts_from_arp_line(), .test_lowercases(), .test_rejects_broadcast(), .test_rejects_garbage(), .test_rejects_multicast()]
- "tests_test_host_health_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_host_health.py:L202 | neighbors=[test_host_health.py, The primary detector. Branch-failure ev…, .test_a_broken_probe_never_condemns_a_h…, .test_a_single_miss_is_not_enough(), .test_cancellation_is_clean(), .test_declares_offline_after_consecutiv…]
- "tests_test_ipv6_discovery_testdiscoverfiltering": "TestDiscoverFiltering" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L38 | neighbors=[test_ipv6_discovery.py, ._patch(), .test_dedups(), .test_excludes_own_addresses(), .test_keeps_usable_drops_dead_states(), .test_link_local_can_be_excluded()]
- "tests_test_job_cancel_probe_testheartbeatoutcomes": "TestHeartbeatOutcomes" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L43 | neighbors=[test_job_cancel_probe.py, .test_200_is_ok(), .test_409_is_reported_as_a_revoked_leas…, .test_bool_heartbeat_contract_is_unchan…, .test_network_error_is_a_plain_failure(), .test_other_rejections_are_plain_failur…]
- "tests_test_job_cancel_test_cancel_records_who_did_it": "test_cancel_records_who_did_it()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L90 | neighbors=[test_job_cancel.py, Attribution must come from a field the …, _count(), _db(), _job(), _one()]
- "tests_test_job_result_service": "test_job_result_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_out_of_scope_result_is_rejected_be…, test_result_scope_accepts_authorized_ta…, test_result_scope_fails_closed(), test_stale_attempt_gets_terminal_receip…]
- "tests_test_main_scripts_completeness_rec": "_rec()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L20 | neighbors=[test_main_scripts_completeness.py, test_duplicate_port_is_detected(), test_fallback_count_based_when_no_reque…, test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely…]
- "tests_test_main_scripts_coverage_testprofiles": "TestProfiles" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L41 | neighbors=[test_main_scripts_coverage.py, .test_custom_dedups_and_requires_ports(), .test_full_is_entire_tcp_space(), .test_quick_is_small_and_contains_smb(), .test_top1000_covers_windows_ground_tru…, .test_top100_is_100_unique()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics": "TestWorkerPoolAndMetrics" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L81 | neighbors=[test_main_scripts_coverage.py, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state()]
- "tests_test_main_scripts_device_testworkstationvsserver": "TestWorkstationVsServer" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L93 | neighbors=[test_main_scripts_device.py, FIX 5(b): don't tie an obvious workstat…, .test_baseline_windows_services_are_not…, .test_real_domain_controller_still_serv…, .test_reference_workstation_unauthentic…, .test_reference_workstation_with_domain…]
- "tests_test_main_scripts_device_ties": "test_main_scripts_device_ties.py" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, test_clear_winner_is_not_ambiguous(), test_domain_controller_breaks_the_tie(), test_empty_is_unknown_not_ambiguous(), test_workstation_server_tie_is_ambiguou…]
- "tests_test_nuclei_background": "test_nuclei_background.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L1 | neighbors=[b4b12a9 Rename project and update files, _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_backgroun…]
- "tests_test_nuclei_background_nestedtransaction": "_NestedTransaction" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L22 | neighbors=[test_nuclei_background.py, .begin_nested(), .__aenter__(), .__aexit__(), ScanJobStatus, NucleiRunReport]
- "tests_test_nuclei_background_scalarresult": "_ScalarResult" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L14 | neighbors=[test_nuclei_background.py, .execute(), .__init__(), .scalar_one_or_none(), ScanJobStatus, NucleiRunReport]
- "tests_test_online_testenrichfindings": "TestEnrichFindings" | kind=code-symbol | source=probe/tests/test_online.py:L117 | neighbors=[test_online.py, .test_caches_per_cve_id(), .test_fail_open_leaves_offline_result_u…, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…, .test_only_missing_skips_already_scored…]
- "tests_test_os_fingerprint_testacceptechoreply": "TestAcceptEchoReply" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L169 | neighbors=[test_os_fingerprint.py, ._reply(), .test_accepts_echo_reply_from_target(), .test_accepts_when_source_unknown(), .test_rejects_non_echo_type(), .test_rejects_none_parsed()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ab_evaluate_no_precision_regression_without_ai_gain": ".test_ab_evaluate_no_precision_regression_without_ai_gain()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L347 | neighbors=[When FakeAIClient returns nothing new, …, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ab_evaluate_returns_expected_keys": ".test_ab_evaluate_returns_expected_keys()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L335 | neighbors=[ab_evaluate must return a dict with the…, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelineaiassist_test_ai_assist_off_by_default": ".test_ai_assist_off_by_default()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L324 | neighbors=[With use_ai_assist=False (the default) …, TestRunPipelineAiAssist, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinededup_test_findings_deduped_within_same_host": ".test_findings_deduped_within_same_host()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L290 | neighbors=[The same (asset, CVE) can't appear twic…, TestRunPipelineDedup, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinededup_test_two_identical_hosts_each_get_their_own_finding": ".test_two_identical_hosts_each_get_their_own_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L277 | neighbors=[Different IPs must produce independent …, TestRunPipelineDedup, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-039.json

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
