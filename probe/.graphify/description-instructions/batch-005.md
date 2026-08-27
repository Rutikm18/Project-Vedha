# Node Description Batch 6 of 92

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

- "tests_test_main_scripts_ja4s": "test_main_scripts_ja4s.py" | kind=code-symbol | source=tests/test_main_scripts_ja4s.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _ext(), _serverhello(), test_empty_extensions_sentinel(), test_extension_hash_is_order_sensitive(), test_ja4s_from_bad_serverhello_is_none()]
- "tests_test_os_fingerprint_testfingerprintos": "TestFingerprintOs" | kind=code-symbol | source=tests/test_os_fingerprint.py:L224 | neighbors=[test_os_fingerprint.py, .test_mss_flags_jumbo_even_without_os_s…, .test_mss_flags_tunnel_or_vpn(), .test_mss_is_path_intel_not_an_os_signa…, .test_mss_yields_ethernet_mtu(), .test_network_device_from_ttl_255()]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=tests/test_passive_collector.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=tests/test_probe_core.py:L745 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_scan_funnel_testscanfunnel": "TestScanFunnel" | kind=code-symbol | source=tests/test_scan_funnel.py:L119 | neighbors=[test_scan_funnel.py, .test_db_scanner_invoked_with_db_port(), .test_db_scanner_not_invoked_without_db…, .test_dead_host_forced_runs_full(), .test_dead_host_skips_port_scan(), .test_deep_scanner_receives_only_open_p…]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "agent_agent_obtain_identity": "_obtain_identity()" | kind=code-symbol | source=agent/agent.py:L1226 | neighbors=[agent.py, main(), _bounded_env_int(), _classify_connection_error(), _dbg(), _enroll_device()]
- "agent_agent_run_ws_push_loop": "_run_ws_push_loop()" | kind=code-symbol | source=agent/agent.py:L549 | neighbors=[agent.py, main(), Persistent WebSocket push loop.      Re…, _flush_spool_over_http(), say(), _ws_heartbeat_sender()]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_license": "license.py" | kind=code-symbol | source=agent/license.py:L1 | neighbors=[agent.py, _b64d(), check_license(), gauntlet(), host_fingerprint(), LicenseError]
- "agent_transport_transport_update_state": ".update_state()" | kind=code-symbol | source=agent/transport.py:L217 | neighbors=[Merge and atomically persist private st…, Transport, .activate_enrollment(), .clear_state(), .refresh_device_access(), .refresh_registration()]
- "agent_validation": "validation.py" | kind=code-symbol | source=agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "main_scripts_accuracy": "accuracy.py" | kind=code-symbol | source=main_scripts/accuracy.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "main_scripts_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=main_scripts/findings.py:L1195 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…]
- "main_scripts_nmap_wrapper": "nmap_wrapper.py" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _have_nmap(), main(), NmapExecutionError, _parse_nmap_xml()]
- "main_scripts_port_scanner": "port_scanner.py" | kind=code-symbol | source=main_scripts/port_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _family_of(), main(), PortScanner, resolve_profile()]
- "main_scripts_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=main_scripts/run_all.py:L55 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…, Run one scanner module as a subprocess,…]
- "main_scripts_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=main_scripts/scan_funnel.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]
- "main_scripts_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=main_scripts/service_banner.py:L123 | neighbors=[service_banner.py, BaseScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard]
- "scanner_accuracy": "accuracy.py" | kind=code-symbol | source=scanner/accuracy.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "scanner_findings_load_facts_jsonl": "load_facts_jsonl()" | kind=code-symbol | source=scanner/findings.py:L1195 | neighbors=[findings.py, _main(), Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…, Read a scanner's JSONL output into fact…]
- "scanner_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=scanner/port_scanner.py:L156 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()]
- "scanner_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=scanner/run_all.py:L55 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…, Run one scanner module as a subprocess,…]
- "scanner_scanner_base_scopeguard": "ScopeGuard" | kind=code-symbol | source=scanner/scanner_base.py:L251 | neighbors=[scanner_base.py, Loads an allowlist of CIDRs / IPs / hos…, .assert_in_scope(), .excludes(), .filter(), .from_file()]
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=scanner/service_banner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, _dec(), main(), match_service()]
- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=scanner/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "scanner_web_scanner": "web_scanner.py" | kind=code-symbol | source=scanner/web_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, ae7a30b feat: add Posture & Patch-Compa…, _fetch(), main(), _NoRedirect, parse_allow_header()]
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=tests/test_agent_identity.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, agent.py, engine.py, transport.py, _cached_transport()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=tests/test_db_scanner.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_http_lease": "test_http_lease.py" | kind=code-symbol | source=tests/test_http_lease.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, ae7a30b feat: add Posture & Patch-Compa…, agent.py, engine.py, transport.py, test_engine_cancellation_stops_async_sc…]
- "tests_test_main_scripts_adaptive_timeout": "test_main_scripts_adaptive_timeout.py" | kind=code-symbol | source=tests/test_main_scripts_adaptive_timeout.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, adaptive_timeout.py, test_estimate_converges_on_stable_rtt(), test_fast_lan_gets_short_timeout_slow_w…, test_first_sample_sets_srtt_and_timeout…, test_invalid_band_rejected()]
- "tests_test_main_scripts_correlation_run": "_run()" | kind=code-symbol | source=tests/test_main_scripts_correlation.py:L13 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_…, test_no_legacy_surface_with_only_smbv1()]
- "tests_test_main_scripts_device_testclassifydevice": "TestClassifyDevice" | kind=code-symbol | source=tests/test_main_scripts_device.py:L17 | neighbors=[test_main_scripts_device.py, .test_domain_controller(), .test_iot_camera(), .test_network_device_router(), .test_printer(), .test_service_product_reinforces_server…]
- "tests_test_main_scripts_errno": "test_main_scripts_errno.py" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _oserr(), test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_dns_failure_is_error_not_filtered(), test_errno_none_falls_back_to_os_error()]
- "tests_test_new_scanners_make_scan_record": "_make_scan_record()" | kind=code-symbol | source=tests/test_new_scanners.py:L315 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_new_scanners_testiotscanner": "TestIoTScanner" | kind=code-symbol | source=tests/test_new_scanners.py:L246 | neighbors=[test_new_scanners.py, .test_coap_get_wellknown_header(), .test_coap_get_wellknown_path(), .test_coap_response_parse_205(), .test_coap_response_parse_404(), .test_coap_response_parse_short()]
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-005.json

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
