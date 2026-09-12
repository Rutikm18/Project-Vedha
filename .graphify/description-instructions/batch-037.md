# Node Description Batch 38 of 380

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

- "tests_test_db_posture_rules": "test_db_posture_rules.py" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, _captured(), _fact(), _fire(), TestCleartextTransport, TestContract]
- "tests_test_db_posture_rules_testunauthenticatedaccess": "TestUnauthenticatedAccess" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L56 | neighbors=[test_db_posture_rules.py, .test_fires_on_real_open_mongodb(), .test_fires_on_real_open_redis(), .test_requires_the_db_marker(), .test_severity_is_critical(), .test_silent_on_ismaster_only_shape()]
- "tests_test_db_tds_prelogin": "test_db_tds_prelogin.py" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, db_scanner.py, _prelogin_response(), TestEncryptionPosture, TestPositiveEvidenceOnly, TestRequestIsWellFormed]
- "tests_test_default_cred_rule": "test_default_cred_rule.py" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L1 | neighbors=[831bdef feat(detection): default-creden…, _fact(), _rule(), TestCatalog, TestRuleFires, TestRuleMetadata]
- "tests_test_detection_core_mock_kev_db": "_mock_kev_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L92 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_device_profile": "test_device_profile.py" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_ambiguous_keeps_asset_type_none_bu…, test_device_profiles_extracts_role_deta…, test_every_device_type_maps_to_the_righ…, test_malformed_entries_are_skipped(), test_non_device_inventory_result_yields…]
- "tests_test_dns_scanner": "test_dns_scanner.py" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, TestAxfrBounded, TestDeriveZones, TestDNSFindings, TestDNSScanner]
- "tests_test_eol_detection_rule": "_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L70 | neighbors=[test_eol_detection.py, .test_declares_its_required_input(), .test_fires_on_past_eol_os(), .test_is_high_severity_with_attack_surf…, .test_reads_os_fingerprint_facts(), .test_rule_is_registered()]
- "tests_test_eol_detection_testcataloglookup": "TestCatalogLookup" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L20 | neighbors=[test_eol_detection.py, .test_days_past_eol_is_positive_for_lon…, .test_longest_match_wins(), .test_match_is_case_insensitive(), .test_missing_os_release_returns_none(), .test_supported_os_returns_none()]
- "tests_test_eol_detection_testeolrule": "TestEolRule" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L74 | neighbors=[test_eol_detection.py, .test_declares_its_required_input(), .test_fires_on_past_eol_os(), .test_is_high_severity_with_attack_surf…, .test_reads_os_fingerprint_facts(), .test_rule_is_registered()]
- "tests_test_exit_state": "test_exit_state.py" | kind=code-symbol | source=probe/tests/test_exit_state.py:L1 | neighbors=[42b9cf2 Phase 3: exit-state protocol + …, test_class_for_code_roundtrip(), test_json_roundtrip(), test_parse_stderr_line_ignores_noise(), test_reason_maps_to_class_and_code(), test_stderr_line_emit_and_parse()]
- "tests_test_exploit_engine_testexploitorchestrator_make_orchestrator": "._make_orchestrator()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L246 | neighbors=[TestExploitOrchestrator, .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_exploitability_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L33 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_no_databases_is_a_no_op(), .test_reason_is_recorded_in_notes()]
- "tests_test_exploitability_testtiers": "TestTiers" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L73 | neighbors=[test_exploitability.py, .test_elevated_epss_band(), .test_epss_max_takes_the_worst_linked_c…, .test_high_epss_without_kev_is_likely(), .test_kev_listed_is_actively_exploited(), .test_kev_outranks_epss()]
- "tests_test_exposed_services_testporthypothesiscontradiction": "TestPortHypothesisContradiction" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L188 | neighbors=[test_exposed_services.py, A catalog entry is a guess about what a…, .test_airplay_suppresses_the_cassandra_…, .test_airplay_suppresses_the_docker_reg…, .test_an_unrelated_product_does_not_sup…, .test_backdoor_evidence_is_never_suppre…]
- "tests_test_finding_compliance_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_finding_compliance.py:L14 | neighbors=[test_finding_compliance.py, test_default_creds_maps_to_hipaa_authen…, test_default_creds_maps_to_pci_default_…, test_each_ref_has_controls_and_a_ration…, test_every_finding_maps_to_all_five_fra…, test_generic_and_empty_findings_still_m…]
- "tests_test_finding_metrics_pair": "_pair()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L28 | neighbors=[test_finding_metrics.py, .test_days_is_hours_over_24(), .test_mean_of_two(), .test_negative_durations_are_dropped_no…, .test_none_values_are_dropped(), .test_single_finding()]
- "tests_test_host_health_testsilencedetection": "TestSilenceDetection" | kind=code-symbol | source=probe/tests/test_host_health.py:L36 | neighbors=[test_host_health.py, .test_any_contact_beats_many_failures(), .test_filtered_is_silence_but_only_susp…, .test_no_results_is_not_silence(), .test_open_and_observed_are_contact(), .test_rst_is_contact_not_silence()]
- "tests_test_installer_contract": "test_installer_contract.py" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, _dry_run(), test_installer_accepts_enroll_token_and…, test_installer_rejects_missing_or_unkno…, test_installer_requires_only_manager_en…]
- "tests_test_intensity_budget_testtuningtranslation": "TestTuningTranslation" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L48 | neighbors=[test_intensity_budget.py, A preset value that never reaches run_e…, .test_deep_preset_reaches_the_tuning_di…, .test_operator_override_is_honoured(), .test_override_can_bound_an_otherwise_u…, .test_override_is_clamped_to_a_safe_env…]
- "tests_test_ipmi_scanner": "test_ipmi_scanner.py" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, _resp(), TestIPMIFindings, TestIPMIScanner, TestParity]
- "tests_test_job_cancel_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L45 | neighbors=[test_job_cancel.py, test_cancel_records_who_did_it(), test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…, test_pending_job_is_cancelled_and_freed…, test_running_job_bumps_the_fence_to_abo…]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed": "TestPollingNoiseIsSuppressed" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L73 | neighbors=[test_job_cancel_probe.py, The probe polls forever; routine transp…, ._configure(), .test_per_request_info_lines_are_suppre…, .test_probe_debug_restores_full_tracing…, .test_probe_own_narration_is_unaffected…]
- "tests_test_main_scripts_vantage_r": "_r()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L12 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_main_scripts_vantage_testreconcilevantages": "TestReconcileVantages" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L16 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_network_va_accuracy_listener": "_Listener" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L26 | neighbors=[test_network_va_accuracy.py, .__init__(), ._loop(), ._serve(), .start(), .stop()]
- "tests_test_nuclei_background_sessionfactory": "_SessionFactory" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L59 | neighbors=[test_nuclei_background.py, .__call__(), .__init__(), test_fatal_nuclei_error_marks_backgroun…, test_partial_nuclei_run_preserves_findi…, ScanJobStatus]
- "tests_test_online_finding": "_finding()" | kind=code-symbol | source=probe/tests/test_online.py:L64 | neighbors=[test_online.py, A CVEFinding as the offline pass would …, .test_caches_per_cve_id(), .test_fail_open_leaves_offline_result_u…, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…]
- "tests_test_os_fingerprint_testprovenance": "TestProvenance" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L369 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_datagram_echo_without_ttl_does_no…, .test_icmp_unavailable_tcp_hints_is_met…, .test_icmp_unavailable_with_tcp_ttl_is_…, .test_no_icmp_but_tcp_ttl_hint_is_metho…]
- "tests_test_os_fusion": "test_os_fusion.py" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, _os(), test_build_only_is_strong_but_not_certa…, test_build_smb2_hostname_is_high_confid…, test_no_os_signal_yields_no_finding(), test_smb2_plus_p0f_stack_is_medium()]
- "tests_test_port_scan_budget": "test_port_scan_budget.py" | kind=code-symbol | source=probe/tests/test_port_scan_budget.py:L1 | neighbors=[09c6c0a feat(probe): per-host wall-cloc…, port_scanner.py, scanner_base.py, _sc(), _summary(), TestBudgetStops]
- "tests_test_port_scan_host_isolation": "test_port_scan_host_isolation.py" | kind=code-symbol | source=probe/tests/test_port_scan_host_isolation.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, port_scanner.py, scanner_base.py, _congestion(), _run_both_hosts_concurrently(), _scanner()]
- "tests_test_port_scan_result_retention_live_probe": "_live_probe()" | kind=code-symbol | source=probe/tests/test_port_scan_result_retention.py:L42 | neighbors=[test_port_scan_result_retention.py, Returns (attempt_fn, live_at_end) where…, .test_every_port_is_classified_exactly_…, .test_only_open_ports_and_the_summary_a…, .test_report_closed_still_emits_every_p…, .test_state_tallies_match_the_probes()]
- "tests_test_portal_assistant_llm": "_llm()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L86 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_only_the_whitelisted_finding_field…, test_reply_is_timestamped_and_attribute…]
- "tests_test_portal_assistant_test_only_the_whitelisted_finding_fields_reach_the_model": "test_only_the_whitelisted_finding_fields_reach_the_model()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L119 | neighbors=[test_portal_assistant.py, Internal triage/evidence fields must ne…, _ask(), _client(), _db(), _engagement()]
- "tests_test_portal_read_db_for_create": "_db_for_create()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L216 | neighbors=[test_portal_read.py, Mock the create_scan_request db flow: e…, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()]
- "tests_test_posture_confidence": "test_posture_confidence.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, _asset(), _by_rule(), _fact(), TestAssessor, TestChains]
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=probe/tests/test_probe_core.py:L898 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()]
- "tests_test_remediation_generator_testparsejsonresponse": "TestParseJsonResponse" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L32 | neighbors=[test_remediation_generator.py, .test_empty_returns_empty(), .test_junk_returns_empty(), .test_non_object_json_returns_empty(), .test_plain_object(), .test_recovers_from_preamble()]
- "tests_test_remediation_routes_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L27 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404(), .test_cached_ai_on_hit()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
