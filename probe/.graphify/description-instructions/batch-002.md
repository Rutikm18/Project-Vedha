# Node Description Batch 3 of 92

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

- "tests_test_integration": "test_integration.py" | kind=code-symbol | source=tests/test_integration.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, result_spool.py, scope_crypt.py, scope_validator.py, task_runner.py, transport.py]
- "tests_test_scan_funnel_make_funnel": "_make_funnel()" | kind=code-symbol | source=tests/test_scan_funnel.py:L64 | neighbors=[test_scan_funnel.py, FakeDiscovery, FakePortScanner, _scope(), Build a funnel with fakes; return (funn…, .test_db_scanner_invoked_with_db_port()]
- "agent_cli_managerclient_request": ".request()" | kind=code-symbol | source=agent/cli.py:L125 | neighbors=[cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create(), cmd_engagements_list()]
- "agent_transport": "transport.py" | kind=code-symbol | source=agent/transport.py:L1 | neighbors=[agent.py, _atomic_write_private_state(), DeviceAlreadyEnrolledError, _enrollment_conflict_detail(), _strip_nul(), _sync_directory()]
- "main_scripts_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=main_scripts/port_scanner.py:L156 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, AdaptiveTimeout, .classified(), .complete()]
- "main_scripts_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=main_scripts/syn_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, build_ip_header(), build_syn_packet(), build_tcp_syn(), classify()]
- "scanner_tls_scanner": "tls_scanner.py" | kind=code-symbol | source=scanner/tls_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, classify_cipher(), _get_cert_der(), grade_tls_posture(), main()]
- "tests_test_transport": "test_transport.py" | kind=code-symbol | source=tests/test_transport.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, ae7a30b feat: add Posture & Patch-Compa…, transport.py, TestDeviceEnrollment, TestFetchScope, TestHeartbeat]
- "agent_agent_main": "main()" | kind=code-symbol | source=agent/agent.py:L205 | neighbors=[agent.py, _bounded_env_int(), _classify_connection_error(), _dbg(), _is_local_manager_url(), _load_env()]
- "agent_agent_say": "say()" | kind=code-symbol | source=agent/agent.py:L76 | neighbors=[agent.py, _check_anti_debug(), _enroll_device(), _flush_spool_over_http(), _load_or_create_identity(), main()]
- "agent_engine_run_scan": "run_scan()" | kind=code-symbol | source=agent/engine.py:L534 | neighbors=[engine.py, Execute a scan and return the enriched …, _build_run_stats(), _derive_post_stage(), _error_result(), _facts_from_cache()]
- "main_scripts_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=main_scripts/scan_funnel.py:L93 | neighbors=[scan_funnel.py, DBScanner, HostDiscoveryScanner, MCPAIScanner, .scan_target(), ResultWriter]
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, BaseScanner, ResultWriter, ScanResult]
- "scanner_mass_scan": "mass_scan.py" | kind=code-symbol | source=scanner/mass_scan.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "tests_test_main_scripts_correlation": "test_main_scripts_correlation.py" | kind=code-symbol | source=tests/test_main_scripts_correlation.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _get(), _ids(), _run(), test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts()]
- "tests_test_main_scripts_rdp": "test_main_scripts_rdp.py" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _cc(), _run(), test_cc_without_negotiation_is_standard…, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…]
- "tests_test_main_scripts_unauth": "test_main_scripts_unauth.py" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, unauth_access.py, _run(), test_couchdb_and_memcached_and_mongodb(), test_elasticsearch_unauth_vs_secured(), test_non_datastore_service_is_unknown()]
- "tests_test_new_scanners_testmobilescanner": "TestMobileScanner" | kind=code-symbol | source=tests/test_new_scanners.py:L518 | neighbors=[test_new_scanners.py, .test_adb_checksum_empty(), .test_adb_checksum_known_value(), .test_adb_cnxn_checksum_matches(), .test_adb_cnxn_command_field(), .test_adb_cnxn_magic_invariant()]
- "tests_test_os_fingerprint": "test_os_fingerprint.py" | kind=code-symbol | source=tests/test_os_fingerprint.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, scanner_base.py, TestAcceptEchoReply, TestFingerprintOs, TestIcmpBuilders]
- "tests_test_validation": "test_validation.py" | kind=code-symbol | source=tests/test_validation.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, validation.py, FakeClient, _preflight_responses(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=agent/use_cases.py:L1 | neighbors=[agent.py, task_runner.py, _as_int(), normalize_intensity(), resolve(), use_case_for_code()]
- "main_scripts_findings_main": "_main()" | kind=code-symbol | source=main_scripts/findings.py:L1211 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…]
- "main_scripts_mass_scan": "mass_scan.py" | kind=code-symbol | source=main_scripts/mass_scan.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _ConnectSweep, _have_masscan(), main(), _masscan_excludes(), _masscan_records_to_results()]
- "main_scripts_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=main_scripts/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "scanner_findings_main": "_main()" | kind=code-symbol | source=scanner/findings.py:L1211 | neighbors=[findings.py, .to_dict(), load_facts_jsonl(), run_findings(), summarize(), CLI: derive findings from one or more s…]
- "scanner_passive_collector": "passive_collector.py" | kind=code-symbol | source=scanner/passive_collector.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, _coverage(), _device_hint(), _is_readable(), _listener_error_code(), main()]
- "scanner_port_scanner": "port_scanner.py" | kind=code-symbol | source=scanner/port_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, _family_of(), main(), PortScanner]
- "scanner_udp_scanner_udpscanner_probe": "._probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L312 | neighbors=[UDPScanner, interpret_dns_recursion(), interpret_ike(), interpret_ipmi(), interpret_mdns(), interpret_memcached_stats()]
- "tests_test_e2e_engagement_to_findings": "test_e2e_engagement_to_findings.py" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, task_runner.py, _accept_loop(), _manager(), _plant(), test_correlated_findings_cite_their_bas…]
- "tests_test_external_engine_wrappers": "test_external_engine_wrappers.py" | kind=code-symbol | source=tests/test_external_engine_wrappers.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, mass_scan.py, nmap_wrapper.py, scanner_base.py, test_masscan_nonzero_with_valid_output_…, test_masscan_range_must_be_fully_in_sco…]
- "tests_test_main_scripts_accuracy": "test_main_scripts_accuracy.py" | kind=code-symbol | source=tests/test_main_scripts_accuracy.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, test_by_rule_breakdown(), test_clean_host_has_zero_false_positive…, test_corpus_flags_a_missed_expected_fin…, test_corpus_matches_real_engine_output(), test_corpus_scores_port_states_when_gro…]
- "tests_test_main_scripts_ja4x": "test_main_scripts_ja4x.py" | kind=code-symbol | source=tests/test_main_scripts_ja4x.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _fake_cert(), test_empty_list_hashes_to_sentinel(), test_ja4x_format_is_three_12hex_fields(), test_ja4x_from_cert_handles_garbage(), test_ja4x_from_cert_matches_pure_core()]
- "tests_test_probe_core_testscopeguard": "TestScopeGuard" | kind=code-symbol | source=tests/test_probe_core.py:L79 | neighbors=[test_probe_core.py, .test_assert_in_scope_passes(), .test_assert_in_scope_raises(), .test_excludes_larger_subnet(), .test_excludes_override_allowlist(), .test_filter_yields_only_in_scope()]
- "tests_test_scan_funnel": "test_scan_funnel.py" | kind=code-symbol | source=tests/test_scan_funnel.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scan_funnel.py, scanner_base.py, FakeDiscovery, FakePortScanner, _make_funnel()]
- "workflow_gates": "gates.py" | kind=code-symbol | source=workflow/gates.py:L1 | neighbors=[local_run.py, ae7a30b feat: add Posture & Patch-Compa…, test_port_catalog.py, test_probe_core.py, test_workflow_execution.py, db_scanner.py]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=workflow/workflow_engine.py:L178 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "agent_cli_cmd_validate": "cmd_validate()" | kind=code-symbol | source=agent/cli.py:L573 | neighbors=[cli.py, CliError, _fetch_all_findings(), _manager_is_local(), ManagerClient, .request()]
- "agent_cli_output": "output()" | kind=code-symbol | source=agent/cli.py:L177 | neighbors=[cli.py, cmd_agents_list(), cmd_auth_login(), cmd_auth_status(), cmd_doctor(), cmd_engagements_create()]
- "main_scripts_db_scanner": "db_scanner.py" | kind=code-symbol | source=main_scripts/db_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, DBScanner, interpret_redis_info(), main(), _probe_mongodb(), _probe_mssql()]
- "main_scripts_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-002.json

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
