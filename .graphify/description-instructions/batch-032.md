# Node Description Batch 33 of 380

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

- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L266 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L321 | neighbors=[service_banner.py, BaseScanner, ._connect(), ._grab(), .__init__(), ._ladder_for()]
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L403 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L87 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()]
- "scanner_vnc_scanner": "vnc_scanner.py" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, classify_security_types(), main(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "schemas_finding_findingpatch": "FindingPatch" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L25 | neighbors=[finding.py, BaseModel, .normalize_action_reason(), All fields optional — PATCH semantics., All fields optional — PATCH semantics., All fields optional — PATCH semantics.]
- "scripts_startup_validator_run_all_validators": "run_all_validators()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L396 | neighbors=[startup_validator.py, Run all validators. Use in FastAPI life…, CheckResult, DatabaseConnectivityValidator, RedisConnectivityValidator, ValidationReport]
- "services_agent_policy": "agent_policy.py" | kind=code-symbol | source=manager/backend/app/services/agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, classify_action(), Decision, _deny(), evaluate_action()]
- "services_llm_managerllmservice_fallback_candidates": "._fallback_candidates()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L445 | neighbors=[ManagerLlmService, ._default_runtime(), ._runtime(), Runtime, _usable_key(), .generate_with_fallback()]
- "services_llm_managerllmservice_generate_with_fallback": ".generate_with_fallback()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L467 | neighbors=[ManagerLlmService, AiRuntimeError, ._build_system(), ._dispatch(), ._ensure_installed_ollama_model(), ._fallback_candidates()]
- "services_remediation_kb": "remediation_kb.py" | kind=code-symbol | source=manager/backend/app/services/remediation_kb.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, fd5dc96 feat(remediation): AI + determi…, classify_finding(), _cves(), os_key(), recipe_for_finding()]
- "supporting_research_test_evidence_store": "test_evidence_store.py" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L1 | neighbors=[6bb51ab feat: add detection-explain end…, build_fleet(), demo(), openssh_below(), smb_obs(), ssh_obs()]
- "supporting_research_test_evidence_store_testretroactivedetection": "TestRetroactiveDetection" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L140 | neighbors=[test_evidence_store.py, .setUp(), .test_a_brand_new_rule_answers_against_…, .test_cannot_answer_is_reported_rather_…, .test_collected_but_unusable_evidence_i…, .test_current_state_comes_from_latest_e…]
- "tests_findings_adapters_test": "findings-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-adapters.test.ts:L1 | neighbors=[315cf9c feat(frontend): refine reports …, 42f4e28 feat: enhance security operatio…, 76240ac UI UX Update, 7d8d3f3 merge: resolve conflicts with o…, ce7ab6e Merge origin/main: reconcile fi…, f473173 merge: network VA accuracy, KEV…]
- "tests_test_accuracy_gate": "test_accuracy_gate.py" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _port_fact(), TestCli, TestCorpusValidation, TestProvenance, TestShippedCorpora]
- "tests_test_adaptive_rate_testwindowstatemachine": "TestWindowStateMachine" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L27 | neighbors=[test_adaptive_rate.py, .test_congestion_avoidance_grows_sublin…, .test_initial_window(), .test_loss_halves_window(), .test_loss_sets_ssthresh_to_half(), .test_recovery_after_loss_enters_conges…]
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "tests_test_auth_login_make_user": "_make_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L44 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testreasoncodes": "TestReasonCodes" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L223 | neighbors=[test_auth_login.py, Ensure every exception class has the ex…, .test_bcrypt_failure_code(), .test_database_failure_code(), .test_disabled_tenant_code(), .test_disabled_user_code()]
- "tests_test_campaign_progress_running_run": "_running_run()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L316 | neighbors=[test_campaign_progress.py, _job(), _progress(), _run(), test_a_briefly_running_run_with_a_dead_…, test_a_dead_worker_is_called_out_quickl…]
- "tests_test_dangling_agent_pin_db_heartbeat": "_db_heartbeat()" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L31 | neighbors=[test_dangling_agent_pin.py, A db whose Agent.last_heartbeat lookup …, .test_boundary_is_the_configured_window…, .test_long_dead_agent_releases_its_pin(), .test_malformed_pin_never_strands_a_job…, .test_recently_seen_agent_is_live()]
- "tests_test_db_scanner_probe": "_probe()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L49 | neighbors=[test_db_scanner.py, FakeReader, FakeWriter, _run(), .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_db_tds_prelogin_prelogin_response": "_prelogin_response()" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L24 | neighbors=[test_db_tds_prelogin.py, Build a server PRELOGIN reply the way S…, .test_not_supported_means_no_tls_at_all…, .test_off_still_supports_tls(), .test_required_is_the_hardened_case(), .test_identification_survives_a_missing…]
- "tests_test_detection_core_mock_epss_db": "_mock_epss_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L96 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_engine_bridge_posture": "test_engine_bridge_posture.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_posture.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 26ea68c Add comprehensive tests for OS …, 42f4e28 feat: enhance security operatio…, 6bb51ab feat: add detection-explain end…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…]
- "tests_test_exploitability_testapplytofindings": "TestApplyToFindings" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L110 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_no_databases_is_a_no_op(), .test_priority_bands_match_posture_rule…]
- "tests_test_exposed_services_testclassify": "TestClassify" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L34 | neighbors=[test_exposed_services.py, .test_backdoor_ports(), .test_banner_confirms_backdoor_on_any_p…, .test_benign_port_is_none(), .test_cleartext_telnet_is_high(), .test_container_apis_are_high()]
- "tests_test_finding_ai_llm_returning": "_llm_returning()" | kind=code-symbol | source=manager/backend/tests/test_finding_ai.py:L27 | neighbors=[test_finding_ai.py, test_empty_or_whitespace_values_are_rej…, test_json_wrapped_in_code_fences_is_par…, test_missing_both_keys_fails_closed(), test_non_json_output_fails_closed(), test_overlong_values_are_truncated()]
- "tests_test_finding_grouping_testgroupkey": "TestGroupKey" | kind=code-symbol | source=manager/detection_engine/tests/test_finding_grouping.py:L19 | neighbors=[test_finding_grouping.py, .test_different_products_do_not_group(), .test_different_rules_do_not_group(), .test_falls_back_to_service_when_no_pro…, .test_identical_devices_share_a_key(), .test_key_is_short_and_stable()]
- "tests_test_finding_metrics_testcomputemttr": "TestComputeMttr" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L32 | neighbors=[test_finding_metrics.py, .test_all_dirty_is_zero_count(), .test_days_is_hours_over_24(), .test_empty_is_zero_not_a_crash(), .test_mean_of_two(), .test_negative_durations_are_dropped_no…]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-032.json

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
