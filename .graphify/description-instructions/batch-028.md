# Node Description Batch 29 of 330

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

- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L321 | neighbors=[service_banner.py, BaseScanner, ._connect(), ._grab(), .__init__(), ._ladder_for()]
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L384 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L87 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()]
- "scanner_vnc_scanner": "vnc_scanner.py" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, classify_security_types(), main(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport]
- "services_agent_policy": "agent_policy.py" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, classify_action(), Decision, _deny(), evaluate_action()]
- "services_remediation_kb": "remediation_kb.py" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, classify_finding(), _cves(), os_key(), recipe_for_finding()]
- "supporting_research_test_evidence_store": "test_evidence_store.py" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, build_fleet(), demo(), openssh_below(), smb_obs(), ssh_obs()]
- "supporting_research_test_evidence_store_testretroactivedetection": "TestRetroactiveDetection" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L140 | neighbors=[test_evidence_store.py, .setUp(), .test_a_brand_new_rule_answers_against_…, .test_cannot_answer_is_reported_rather_…, .test_collected_but_unusable_evidence_i…, .test_current_state_comes_from_latest_e…]
- "tests_test_accuracy_gate": "test_accuracy_gate.py" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _port_fact(), TestCli, TestCorpusValidation, TestProvenance, TestShippedCorpora]
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…]
- "tests_test_agent_read_tools": "test_agent_read_tools.py" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L1 | neighbors=[3ad95f4 feat: Optimize asset service fe…, _asset(), _FakeSession, _Result, _svc(), test_list_assets_batches_services_no_n_…]
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()]
- "tests_test_campaign_progress_running_run": "_running_run()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L316 | neighbors=[test_campaign_progress.py, _job(), _progress(), _run(), test_a_briefly_running_run_with_a_dead_…, test_a_dead_worker_is_called_out_quickl…]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L96 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_engine_bridge_posture": "test_engine_bridge_posture.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 42f4e28 feat: enhance security operatio…, 6bb51ab feat: add detection-explain end…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…]
- "tests_test_exploitability_testapplytofindings": "TestApplyToFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L110 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_no_databases_is_a_no_op(), .test_priority_bands_match_posture_rule…]
- "tests_test_exposed_services_testclassify": "TestClassify" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L34 | neighbors=[test_exposed_services.py, .test_backdoor_ports(), .test_banner_confirms_backdoor_on_any_p…, .test_benign_port_is_none(), .test_cleartext_telnet_is_high(), .test_container_apis_are_high()]
- "tests_test_ipv6_wiring_testinterfacescoping": "TestInterfaceScoping" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L27 | neighbors=[test_ipv6_wiring.py, The neighbour cache is system-wide. Pin…, ._stub(), .test_globals_are_kept_they_are_not_int…, .test_iface_filters_out_other_segments(), .test_iface_keeps_its_own_neighbours()]
- "tests_test_loaders": "test_loaders.py" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, TestLoadEpssErrors, TestLoadKevErrors, TestLoadSnapshotErrors, _valid_epss(), _valid_kev()]
- "tests_test_loaders_testloadsnapshoterrors": "TestLoadSnapshotErrors" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L55 | neighbors=[test_loaders.py, .setup_method(), .test_content_hash_mismatch_raises_valu…, .test_error_message_mentions_re_sync(), .test_hash_mismatch_message_truncates_h…, .test_malformed_json_raises()]
- "tests_test_main_scripts_coverage_mk_scanner": "_mk_scanner()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L27 | neighbors=[test_main_scripts_coverage.py, _scope(), .test_adaptive_estimator_is_shared_and_…, .test_fixed_timeout_flag_disables_the_e…, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…]
- "tests_test_main_scripts_datastore_probe": "test_main_scripts_datastore_probe.py" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, service_banner.py, _svc(), test_elasticsearch_and_couchdb_win_over…, test_ladder_includes_safe_datastore_pro…, test_memcached_probe_response_yields_un…]
- "tests_test_main_scripts_device": "test_main_scripts_device.py" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, device_classifier.py, scanner_base.py, TestClassifyDevice]
- "tests_test_main_scripts_rdp_cc": "_cc()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L17 | neighbors=[test_main_scripts_rdp.py, A TPKT + X.224 Connection Confirm, opti…, test_cc_without_negotiation_is_standard…, test_hybrid_ex_0x08_is_nla_over_tls(), test_negotiation_failure(), test_nla_when_hybrid_selected()]
- "tests_test_main_scripts_statemodel": "test_main_scripts_statemodel.py" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, test_backward_compatible_old_style_cons…, test_canonical_states_are_the_six_docum…, test_explicit_first_class_value_wins_ov…, test_semantics_in_data_are_promoted_to_…]
- "tests_test_manager_ai_cloud": "_cloud()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L298 | neighbors=[test_manager_ai.py, Settings with provider unset and all cl…, test_default_auto_detect_prefers_openai…, test_default_auto_detects_the_configure…, test_default_runtime_fails_closed_witho…, test_fallback_never_includes_local_olla…]
- "tests_test_msrpc_scanner": "test_msrpc_scanner.py" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, scanner_base.py, TestDynamicPorts, TestMSRPCFindings, TestMSRPCScanner]
- "tests_test_new_scanners_testdeltaengine_write_jsonl": "._write_jsonl()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L382 | neighbors=[TestDeltaEngine, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner": "test_nuclei_scanner.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L1 | neighbors=[b4b12a9 Rename project and update files, FakeProcess, _finding_line(), test_missing_binary_is_a_reported_failu…, test_nonzero_exit_retains_and_marks_par…, test_nonzero_exit_without_findings_rais…]
- "tests_test_os_fingerprint_testttlinference": "TestTtlInference" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L192 | neighbors=[test_os_fingerprint.py, .test_hop_estimate(), .test_os_family_linux(), .test_os_family_network(), .test_os_family_unknown_on_none(), .test_os_family_windows()]
- "tests_test_os_stage_wiring_asset": "_asset()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L28 | neighbors=[test_os_stage_wiring.py, .test_closed_port_contributes_no_hints(), .test_connect_scan_without_stack_signal…, .test_os_fact_stored_and_ntlm_name_beco…, .test_syn_stack_hints_harvested_from_op…, .test_alive_host_is_eligible()]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
- "tests_test_portal_assistant_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L39 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…, test_only_the_whitelisted_finding_field…]
- "tests_test_portal_assistant_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L55 | neighbors=[test_portal_assistant.py, test_context_is_built_server_side_from_…, test_focus_finding_in_scope_is_added_to…, test_focus_finding_outside_the_engageme…, test_model_failure_surfaces_its_status_…, test_only_the_whitelisted_finding_field…]
- "tests_test_reference": "test_reference.py" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _at(), test_the_migration_backfill_agrees_with…, TestShape, TestStability, TestStamping]
- "tests_test_rsync_scanner_fakesock": "_FakeSock" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L34 | neighbors=[test_rsync_scanner.py, .__init__(), .recv(), .sendall(), Minimal socket stand-in: replays the da…, .test_echo_stops_at_the_first_line()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
