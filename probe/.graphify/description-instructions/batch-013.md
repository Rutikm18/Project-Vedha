# Node Description Batch 14 of 92

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

- "scanner_tls_fingerprint_jarm_style_digest": "jarm_style_digest()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L200 | neighbors=[tls_fingerprint.py, fingerprint_host(), cipher_code(), _server_ext_types(), version_code(), JARM-shaped 62-char fuzzy hash: 3 chars…]
- "scanner_tls_fingerprint_one_probe": "_one_probe()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L261 | neighbors=[tls_fingerprint.py, fingerprint_host(), build_client_hello(), parse_server_hello(), _recv_first_record(), Send one crafted ClientHello, read + pa…]
- "scanner_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=scanner/tls_scanner.py:L244 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "scanner_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=scanner/udp_scanner.py:L277 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "scanner_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=scanner/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_host_discovery_mobile_testdevicehint": "TestDeviceHint" | kind=code-symbol | source=tests/test_host_discovery_mobile.py:L52 | neighbors=[test_host_discovery_mobile.py, .test_iphone_lockdownd_port(), .test_mobile_vendor(), .test_no_signal(), .test_plain_vendor_passthrough(), .test_randomized_mac_is_mobile()]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_main_scripts_completeness_metrics": "_metrics()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L15 | neighbors=[test_main_scripts_completeness.py, test_duplicate_port_is_detected(), test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely…, test_summary_exposes_missing_and_duplic…]
- "tests_test_main_scripts_device": "test_main_scripts_device.py" | kind=code-symbol | source=tests/test_main_scripts_device.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, device_classifier.py, scanner_base.py, TestClassifyDevice, TestClassifyFromResults, test_main_scripts_device.py — device-ro…]
- "tests_test_main_scripts_device_ties": "test_main_scripts_device_ties.py" | kind=code-symbol | source=tests/test_main_scripts_device_ties.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, test_clear_winner_is_not_ambiguous(), test_domain_controller_breaks_the_tie(), test_empty_is_unknown_not_ambiguous(), test_workstation_server_tie_is_ambiguou…, test_main_scripts_device_ties.py — Phas…]
- "tests_test_main_scripts_vantage": "test_main_scripts_vantage.py" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, vantage_matrix.py, _r(), TestReconcileVantages, test_main_scripts_vantage.py — multi-va…]
- "tests_test_new_scanners_teststablehostid": "TestStableHostId" | kind=code-symbol | source=tests/test_new_scanners.py:L331 | neighbors=[test_new_scanners.py, .test_hostname_second_priority(), .test_ip_fallback(), .test_mac_normalises_dashes(), .test_mac_takes_priority(), .test_zero_mac_skipped()]
- "tests_test_passive_collector_writer": "_Writer" | kind=code-symbol | source=tests/test_passive_collector.py:L15 | neighbors=[test_passive_collector.py, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…, test_subset_listener_failure_reports_de…, .__init__(), .write()]
- "tests_test_probe_core_testclamp": "TestClamp" | kind=code-symbol | source=tests/test_probe_core.py:L830 | neighbors=[test_probe_core.py, .test_bad_value_uses_default(), .test_clamped_high(), .test_clamped_low(), .test_in_range(), .test_none_uses_default()]
- "tests_test_probe_core_testengagementmodes": "TestEngagementModes" | kind=code-symbol | source=tests/test_probe_core.py:L444 | neighbors=[test_probe_core.py, .test_assessment(), .test_re_scan(), .test_service_specific_invalid_raises(), .test_service_specific_valid(), .test_triage()]
- "tests_test_probe_manifest": "test_probe_manifest.py" | kind=code-symbol | source=tests/test_probe_manifest.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _manifest(), test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…, test_probe_manifest.py — the `agent.age…]
- "tests_test_probe_next_features_cache_with": "_cache_with()" | kind=code-symbol | source=tests/test_probe_next_features.py:L103 | neighbors=[test_probe_next_features.py, test_device_inventory_post_stage_classi…, test_device_inventory_skips_hosts_witho…, test_exposure_matrix_flags_internet_rea…, test_exposure_matrix_internal_only_from…, test_no_post_stage_for_ordinary_scan_ty…]
- "tests_test_scanner_parity": "test_scanner_parity.py" | kind=code-symbol | source=tests/test_scanner_parity.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _py_files(), test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…, test_scanner_module_matches_main_script…, test_scanner_parity.py — the no-drift g…]
- "tests_test_scope_validator_testfetchengagementscope": "TestFetchEngagementScope" | kind=code-symbol | source=tests/test_scope_validator.py:L170 | neighbors=[test_scope_validator.py, .test_http_get_raises(), .test_http_get_returns_incomplete(), .test_http_get_returns_none(), .test_returns_excludes(), .test_returns_scope_from_http_get()]
- "tests_test_service_match_testotherservices": "TestOtherServices" | kind=code-symbol | source=tests/test_service_match.py:L58 | neighbors=[test_service_match.py, .test_mariadb_handshake(), .test_redis_info(), .test_redis_noauth(), .test_smtp_postfix(), .test_vsftpd()]
- "tests_test_syn_scanner_testbuildresultsenrichment": "TestBuildResultsEnrichment" | kind=code-symbol | source=tests/test_syn_scanner.py:L348 | neighbors=[test_syn_scanner.py, ._scanner(), .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_windows_ttl_maps_to_windows()]
- "tests_test_syn_scanner_testoptionparsing": "TestOptionParsing" | kind=code-symbol | source=tests/test_syn_scanner.py:L303 | neighbors=[test_syn_scanner.py, .test_malformed_options_never_raise(), .test_mss_absent_returns_none(), .test_mss_after_nop_padding(), .test_mss_extracted(), .test_mss_skips_other_options()]
- "tests_test_syn_scanner_testsynretransmit": "TestSynRetransmit" | kind=code-symbol | source=tests/test_syn_scanner.py:L204 | neighbors=[test_syn_scanner.py, The raw SYN path resends ONLY still-sil…, ._patch(), .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_tarpit": "test_tarpit.py" | kind=code-symbol | source=tests/test_tarpit.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, port_scanner.py, scanner_base.py, TestAssessTarpit, TestPortScannerTarpitFlag, test_tarpit.py — tarpit / honeypot dete…]
- "tests_test_tarpit_testassesstarpit": "TestAssessTarpit" | kind=code-symbol | source=tests/test_tarpit.py:L17 | neighbors=[test_tarpit.py, .test_boundary_floor_and_ratio_trip_exa…, .test_busy_real_host_is_not_flagged(), .test_nearly_all_open_large_scan_is_fla…, .test_tiny_all_open_scan_is_below_the_f…, .test_zero_attempted_is_safe()]
- "tests_test_tls_fingerprint": "test_tls_fingerprint.py" | kind=code-symbol | source=tests/test_tls_fingerprint.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _synthetic_server_hello(), TestClientHello, TestDigest, TestParseServerHello, test_tls_fingerprint.py — Tier 2.3: act…]
- "tests_test_tls_posture": "test_tls_posture.py" | kind=code-symbol | source=tests/test_tls_posture.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, tls_scanner.py, _modern(), TestClassifyCipher, TestGradeTlsPosture, test_tls_posture.py — Tier 2.4: cipher-…]
- "tests_test_validation_fakeclient": "FakeClient" | kind=code-symbol | source=tests/test_validation.py:L110 | neighbors=[test_validation.py, .__init__(), .request(), test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_wire_identity_testchoosesourceport": "TestChooseSourcePort" | kind=code-symbol | source=tests/test_wire_identity.py:L38 | neighbors=[test_wire_identity.py, Evasion: a fixed source port (e.g. 53/8…, .test_boundary_ports_are_valid(), .test_none_gives_random_ephemeral(), .test_out_of_range_falls_back_to_random…, .test_uses_configured_valid_port()]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=workflow/router.py:L83 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_ssh(), looks_like_tls()]
- "agent_agent_flush_spool_over_http": "_flush_spool_over_http()" | kind=code-symbol | source=agent/agent.py:L867 | neighbors=[agent.py, say(), Retry durable result files using the ac…, _run_ws_push_loop(), _ws_http_poll_fallback()]
- "agent_agent_run_polled_job_with_heartbeats": "_run_polled_job_with_heartbeats()" | kind=code-symbol | source=agent/agent.py:L500 | neighbors=[agent.py, main(), Run an HTTP-claimed job while renewing …, _bounded_env_int(), say()]
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=agent/agent.py:L880 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say()]
- "agent_cli_cmd_auth_status": "cmd_auth_status()" | kind=code-symbol | source=agent/cli.py:L274 | neighbors=[cli.py, client_from_args(), .request(), output(), cmd_whoami()]
- "agent_cli_configstore_load": ".load()" | kind=code-symbol | source=agent/cli.py:L59 | neighbors=[ConfigStore, .get_profile(), CliError, .remove_profile(), .set_profile()]
- "agent_cli_env": "_env()" | kind=code-symbol | source=agent/cli.py:L33 | neighbors=[cli.py, build_parser(), cmd_auth_login(), default_config_path(), resolve_profile()]
- "agent_cli_normalize_manager_url": "normalize_manager_url()" | kind=code-symbol | source=agent/cli.py:L46 | neighbors=[cli.py, cmd_auth_login(), .__init__(), CliError, resolve_profile()]
- "agent_cli_poll_job": "_poll_job()" | kind=code-symbol | source=agent/cli.py:L478 | neighbors=[cli.py, cmd_scan_run(), cmd_validate(), CliError, .request()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-013.json

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
