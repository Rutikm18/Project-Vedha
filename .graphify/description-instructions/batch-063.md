# Node Description Batch 64 of 332

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
- "tests_test_portal_remediation_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L22 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_remediation_testportalremediation": "TestPortalRemediation" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L44 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_posture_confidence_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L26 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L19 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_testendtoend": "TestEndToEnd" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L93 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_rules_testhardenedgroundtruth": "TestHardenedGroundTruth" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L50 | neighbors=[test_posture_rules.py, ._host(), .test_hardened_smb_and_rdp_raise_no_mis…, .test_no_critical_or_high_findings(), .test_rdp_exposed_is_low_because_nla_re…]
- "tests_test_posture_rules_testriskmodel": "TestRiskModel" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L132 | neighbors=[test_posture_rules.py, .test_auth_enforced_deescalates(), .test_internet_facing_unauth_escalates(), .test_priority_buckets(), .test_suspected_scores_below_confirmed()]
- "tests_test_posture_trace_testabsentversusclean": "TestAbsentVersusClean" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L36 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…]
- "tests_test_posture_trace_testabsentversusclean_test_missing_input_invariant_across_all_rules": ".test_missing_input_invariant_across_all_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L62 | neighbors=[I10 structurally: for EVERY rule with a…, TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L276 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L390 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L405 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L853 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L884 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_probe_simple_approve_testnextprobename": "TestNextProbeName" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L20 | neighbors=[test_probe_simple_approve.py, .test_first_is_01(), .test_ignores_non_matching_and_non_nume…, .test_increments_past_highest_with_gaps…, .test_legacy_probe_names_still_advance_…]
- "tests_test_project_time_testrendering": "TestRendering" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L23 | neighbors=[test_project_time.py, .test_default_is_ist(), .test_same_instant_as_utc(), .test_still_orders_against_utc_rows(), .test_timestamp_carries_an_offset()]
- "tests_test_project_timezone_testprojecttimezone": "TestProjectTimezone" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L26 | neighbors=[test_project_timezone.py, .test_aware_timestamps_still_compare_ag…, .test_default_is_ist(), .test_timestamp_is_iso_with_offset_not_…, .test_timestamp_is_the_same_instant_as_…]
- "tests_test_reference_testshape": "TestShape" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L27 | neighbors=[test_reference.py, .test_an_unknown_prefix_is_refused(), .test_naive_created_at_is_treated_as_ut…, .test_reads_as_prefix_date_code(), .test_uses_the_rows_own_date_not_today()]
- "tests_test_remediation_kb_testclassify": "TestClassify" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L16 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic()]
- "tests_test_remediation_routes_one_result": "_one_result()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L53 | neighbors=[test_remediation_routes.py, A result whose .one() yields the RETURN…, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, A result whose .one() yields the RETURN…]
- "tests_test_remediation_routes_testgenerateremediation": "TestGenerateRemediation" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L145 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404()]
- "tests_test_remediation_routes_testgenerateremediation_test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed": ".test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L166 | neighbors=[TestGenerateRemediation, _FakeDB, _finding(), _operator(), _scalar_result()]

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
