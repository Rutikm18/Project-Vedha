# Node Description Batch 83 of 336

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

- "tests_test_ipmi_scanner_testipmifindings": "TestIPMIFindings" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L62 | neighbors=[test_ipmi_scanner.py, ._fact(), .test_cipher_zero_is_critical(), .test_reachable_bmc_is_low()]
- "tests_test_ipmi_scanner_testipmiscanner": "TestIPMIScanner" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L44 | neighbors=[test_ipmi_scanner.py, ._sc(), .test_cipher_zero_open(), .test_no_ipmi_filtered()]
- "tests_test_ipv6_discovery_testparsers": "TestParsers" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L13 | neighbors=[test_ipv6_discovery.py, .test_ignores_non_ipv6_lines(), .test_parse_ip_neigh_linux(), .test_parse_ndp_macos()]
- "tests_test_ipv6_wiring_test_out_of_scope_neighbour_is_reported_but_never_probed": "test_out_of_scope_neighbour_is_reported_but_never_probed()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L110 | neighbors=[test_ipv6_wiring.py, The core restraint: discovery must not …, _run(), _wire()]
- "tests_test_job_cancel_test_job_outside_the_tenant_is_not_found": "test_job_outside_the_tenant_is_not_found()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L166 | neighbors=[test_job_cancel.py, _db(), _one(), _user()]
- "tests_test_loaders_valid_snapshot": "_valid_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L28 | neighbors=[test_loaders.py, .test_content_hash_mismatch_raises_valu…, .test_hash_mismatch_message_truncates_h…, _write_snapshot()]
- "tests_test_main_scripts_coverage_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L23 | neighbors=[test_main_scripts_coverage.py, _mk_scanner(), .test_default_ports_are_nmap_top100_not…, .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout": "TestDefaultsAndAdaptiveTimeout" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L186 | neighbors=[test_main_scripts_coverage.py, .test_adaptive_estimator_is_shared_and_…, .test_default_ports_are_nmap_top100_not…, .test_fixed_timeout_flag_disables_the_e…]
- "tests_test_main_scripts_datastore_probe_svc": "_svc()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L15 | neighbors=[test_main_scripts_datastore_probe.py, test_elasticsearch_and_couchdb_win_over…, test_memcached_version_and_stat_identif…, test_redis_info_and_noauth_identify_as_…]
- "tests_test_main_scripts_hardening_make_smb2_error": "make_smb2_error()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L122 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), STATUS_INVALID_PARAMETER error response…, .test_error_response_not_trusted()]
- "tests_test_main_scripts_hardening_make_smb2_success": "make_smb2_success()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L113 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_main_scripts_hardening_smb2_header": "_smb2_header()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L100 | neighbors=[test_main_scripts_hardening.py, make_smb2_error(), make_smb2_success(), A 64-byte SMB2 header. Caller prepends …]
- "tests_test_main_scripts_hardening_testudpstatemodel": "TestUdpStateModel" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L42 | neighbors=[test_main_scripts_hardening.py, ._scanner(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L43 | neighbors=[TestUdpStateModel, _scope(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_unauth_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L51 | neighbors=[test_main_scripts_unauth.py, test_protected_redis_raises_no_unauth_f…, test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_f…]
- "tests_test_msrpc_scanner_testmsrpcfindings": "TestMSRPCFindings" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L81 | neighbors=[test_msrpc_scanner.py, ._fact(), .test_endpoints_low(), .test_zero_endpoints_silent()]
- "tests_test_msrpc_scanner_testmsrpcscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L57 | neighbors=[TestMSRPCScanner, .test_impacket_missing_is_error(), .test_no_msrpc_filtered(), .test_open()]
- "tests_test_nessus_scanner_rationale_1": "Unit tests for NessusScanner — all HTTP calls mocked." | kind=entity | source=manager/backend/tests/test_nessus_scanner.py:L1 | neighbors=[test_nessus_scanner.py, FindingSeverity, FindingStatus, NessusScanner]
- "tests_test_nfs_scanner_testnfsfindings": "TestNFSFindings" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L117 | neighbors=[test_nfs_scanner.py, ._fact(), .test_restricted_exports_no_high_findin…, .test_world_readable_and_portmapper()]
- "tests_test_nfs_scanner_testnfsscanner": "TestNFSScanner" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L94 | neighbors=[test_nfs_scanner.py, ._sc(), .test_no_rpc_is_filtered(), .test_world_readable_export_open()]
- "tests_test_nmap_xml_safety_testnmapentityguard": "TestNmapEntityGuard" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L27 | neighbors=[test_nmap_xml_safety.py, .test_entity_declaration_is_refused(), .test_entity_guard_is_case_insensitive(), .test_legitimate_doctype_output_still_p…]
- "tests_test_notifications": "test_notifications.py" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, TestDeliver, TestNotifyTenant, test_notifications.py — integration del…]
- "tests_test_notifications_testdeliver": "TestDeliver" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L13 | neighbors=[test_notifications.py, .test_dispatches_to_the_kind(), .test_sender_error_is_swallowed(), .test_unknown_kind_returns_false()]
- "tests_test_nuclei_scanner_finding_line": "_finding_line()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L12 | neighbors=[test_nuclei_scanner.py, test_nonzero_exit_retains_and_marks_par…, test_run_scan_streams_jsonl_and_separat…, test_timeout_retains_findings_emitted_b…]
- "tests_test_online_get_raising": "_get_raising()" | kind=code-symbol | source=probe/tests/test_online.py:L58 | neighbors=[test_online.py, .test_fail_open_leaves_offline_result_u…, .test_network_error_is_fail_open(), .test_error_is_none()]
- "tests_test_online_nvd_bytes": "_nvd_bytes()" | kind=code-symbol | source=probe/tests/test_online.py:L25 | neighbors=[test_online.py, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…, .test_parses_score_severity_refs()]
- "tests_test_online_testenrichfindings_test_gap_fill_sets_cvss_and_recomputes_risk": ".test_gap_fill_sets_cvss_and_recomputes_risk()" | kind=code-symbol | source=probe/tests/test_online.py:L118 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]
- "tests_test_online_testenrichfindings_test_online_all_cross_checks_and_annotates_mismatch": ".test_online_all_cross_checks_and_annotates_mismatch()" | kind=code-symbol | source=probe/tests/test_online.py:L139 | neighbors=[TestEnrichFindings, _finding(), _get_returning(), _nvd_bytes()]
- "tests_test_os_fingerprint_testtimestampfallback": "TestTimestampFallback" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L138 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_outbox_reclaim_mock_session": "_mock_session()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L104 | neighbors=[test_outbox_reclaim.py, test_reclaim_handles_none_rowcount_from…, test_reclaim_is_noop_when_nothing_is_st…, test_reclaim_runs_both_sweeps_commits_a…]
- "tests_test_outbox_reclaim_sql": "_sql()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L20 | neighbors=[test_outbox_reclaim.py, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_requeue_stmt_makes_retryable_stran…]
- "tests_test_pipeline_concurrency_db_with": "_db_with()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L100 | neighbors=[test_pipeline_concurrency.py, test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_pipeline_concurrency_event": "_event()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L93 | neighbors=[test_pipeline_concurrency.py, test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_pipeline_concurrency_test_a_first_delivery_still_runs_detection": "test_a_first_delivery_still_runs_detection()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L128 | neighbors=[test_pipeline_concurrency.py, The guard must not swallow real work., _db_with(), _event()]
- "tests_test_pipeline_concurrency_test_a_missing_submission_is_not_an_error": "test_a_missing_submission_is_not_an_error()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L147 | neighbors=[test_pipeline_concurrency.py, Pre-existing behaviour: a vanished scan…, _db_with(), _event()]
- "tests_test_pipeline_openssh_upstream_vuln_db": "_openssh_upstream_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L73 | neighbors=[test_pipeline.py, _mock_vuln_db(), Upstream boundary for a banner-vs-inven…, .test_full_detection_exposes_authoritat…]
- "tests_test_pipeline_testrunpipelineaiassist": "TestRunPipelineAiAssist" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L323 | neighbors=[test_pipeline.py, .test_ab_evaluate_no_precision_regressi…, .test_ab_evaluate_returns_expected_keys…, .test_ai_assist_off_by_default()]
- "tests_test_portal_assistant_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L44 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_only_the_whitelisted_finding_field…]
- "tests_test_portal_metrics_testseveritybreakdown": "TestSeverityBreakdown" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L19 | neighbors=[test_portal_metrics.py, .test_all_buckets_present_zero_filled(), .test_open_only_excludes_closed(), .test_unknown_severity_falls_into_info()]
- "tests_test_portal_metrics_teststatustimeline": "TestStatusTimeline" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L41 | neighbors=[test_portal_metrics.py, .test_activity_outside_window_is_ignore…, .test_buckets_opened_and_closed(), .test_emits_continuous_zero_filled_mont…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
