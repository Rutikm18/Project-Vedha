# Node Description Batch 39 of 186

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

- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_hardening_testsmbparsing": "TestSmbParsing" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L131 | neighbors=[test_main_scripts_hardening.py, .test_error_response_not_trusted(), .test_negotiate_request_excludes_smb311…, .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L358 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_os_fingerprint_testicmpbuilders": "TestIcmpBuilders" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L36 | neighbors=[test_os_fingerprint.py, .test_address_mask_request_type(), .test_echo_payload_preserved(), .test_echo_request_type_and_checksum(), .test_timestamp_request_type()]
- "tests_test_os_fingerprint_testicmpparse": "TestIcmpParse" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L61 | neighbors=[test_os_fingerprint.py, ._ip_icmp(), .test_parse_extracts_ttl_and_type(), .test_parse_raw_icmp_without_ip_header(), .test_parse_rejects_short()]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_perf_optimization_write_snapshot": "_write_snapshot()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L103 | neighbors=[test_perf_optimization.py, test_clear_caches_forces_reload(), test_load_snapshot_memoized_returns_sam…, test_load_snapshot_reloads_after_file_c…, test_load_snapshot_runs_dpkg_guard_once…]
- "tests_test_pipeline_mock_vuln_db": "_mock_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L40 | neighbors=[test_pipeline.py, _openssh_vuln_db(), .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty(), .test_injected_dbs_used_no_file_io()]
- "tests_test_pipeline_testrunpipelineemptyinput_test_no_paths_returns_empty": ".test_no_paths_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L123 | neighbors=[Passing an empty path list must return …, TestRunPipelineEmptyInput, _empty_epss(), _empty_kev(), _mock_vuln_db()]
- "tests_test_pipeline_testrunpipelineexposure_test_exposure_internet_facing_propagates": ".test_exposure_internet_facing_propagates()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L204 | neighbors=[TestRunPipelineExposure, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_pipeline_testrunpipelinereturnvalue_test_returns_tuple_of_findings_and_ingest_result": ".test_returns_tuple_of_findings_and_ingest_result()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L263 | neighbors=[TestRunPipelineReturnValue, _empty_epss(), _empty_kev(), _openssh_vuln_db(), _ssh_inventory_jsonl()]
- "tests_test_probe_core_testenginesummary": "TestEngineSummary" | kind=code-symbol | source=probe/tests/test_probe_core.py:L604 | neighbors=[test_probe_core.py, .test_affirmative_fact_creates_one_dedu…, .test_negative_or_ambiguous_facts_do_no…, .test_open_port_count_deduplicates_conf…, .test_open_port_count_excludes_host_liv…]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L276 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L390 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L405 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L816 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L847 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_router_db": "test_router_db.py" | kind=code-symbol | source=probe/tests/test_router_db.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, test_mysql_greeting_on_odd_port(), test_plain_http_is_not_db(), test_redis_noauth_signature(), router.py]
- "tests_test_runtime_topology": "test_runtime_topology.py" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, main.py, test_manager_does_not_mount_a_static_da…, test_manager_root_is_service_metadata(), Product-boundary tests for the single-d…]
- "tests_test_scan_funnel_testrouteports": "TestRoutePorts" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L98 | neighbors=[test_scan_funnel.py, .test_intersection_only(), .test_no_match_returns_empty(), .test_port_in_multiple_routes(), .test_sorted_output()]
- "tests_test_service_match_testhttpmatch": "TestHttpMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L35 | neighbors=[test_service_match.py, .test_apache_version(), .test_iis_version(), .test_nginx_version(), .test_nginx_without_version()]
- "tests_test_syn_scanner_testpacketroundtrip": "TestPacketRoundTrip" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L71 | neighbors=[test_syn_scanner.py, .test_ip_checksum_valid_in_full_packet(), .test_parse_rejects_short_packet(), .test_syn_flag_is_set(), .test_syn_packet_parses_back_to_fields()]
- "tests_test_syn_scanner_testsyncookie": "TestSynCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L50 | neighbors=[test_syn_scanner.py, .test_cookie_is_32_bit(), .test_cookie_is_deterministic(), .test_cookie_varies_with_key(), .test_cookie_varies_with_port()]
- "tests_test_syn_scanner_testverifyreplycookie": "TestVerifyReplyCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L112 | neighbors=[test_syn_scanner.py, ._make_synack_reply(), .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_tls_fingerprint_testclienthello": "TestClientHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L22 | neighbors=[test_tls_fingerprint.py, .test_contains_client_hello_handshake_t…, .test_contains_sni_hostname(), .test_declared_lengths_are_consistent(), .test_is_tls_handshake_record()]
- "tests_test_tls_fingerprint_testparseserverhello": "TestParseServerHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L58 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_returns_none_on_alert(), .test_returns_none_on_short(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_posture_modern": "_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L68 | neighbors=[test_tls_posture.py, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_tls11(), .test_grade_f_tls10()]
- "tests_test_transport_testdeviceenrollment": "TestDeviceEnrollment" | kind=code-symbol | source=probe/tests/test_transport.py:L171 | neighbors=[test_transport.py, .test_activation_persists_recoverable_d…, .test_create_enrollment_request_forward…, .test_device_refresh_signs_unique_nonce…, .test_legacy_token_is_not_forced_throug…]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=probe/tests/test_transport.py:L507 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_web_methods": "test_web_methods.py" | kind=code-symbol | source=probe/tests/test_web_methods.py:L1 | neighbors=[bce780a feat(probe): enumerate HTTP met…, web_scanner.py, test_dangerous_methods_flagged(), test_no_allow_header(), test_safe_methods_only()]
- "tools_installer_getinstalledrecord": "getInstalledRecord()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L63 | neighbors=[installer.ts, readInstalled(), installAll(), installTool(), tools.ts]
- "tools_installer_ismanaged": "isManaged()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L56 | neighbors=[tools.ts, tool-runners.ts, installer.ts, installTool(), managedPath()]
- "tools_installer_readinstalled": "readInstalled()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L33 | neighbors=[installer.ts, getInstalledRecord(), installTool(), listStatus(), removeTool()]
- "tools_installer_removetool": "removeTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L243 | neighbors=[tools.ts, installer.ts, managedPath(), readInstalled(), writeInstalled()]
- "ui_output_rule": "rule()" | kind=code-symbol | source=manager/frontend/cli/ui/output.ts:L50 | neighbors=[output.ts, findingDetail(), ln(), scanHeader(), summary()]
- "versions_0002_services_agents": "0002_services_agents.py" | kind=code-symbol | source=manager/backend/alembic/versions/0002_services_agents.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add services and agents tables  Revisio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0003_vuln_scan_fields": "0003_vuln_scan_fields.py" | kind=code-symbol | source=manager/backend/alembic/versions/0003_vuln_scan_fields.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, downgrade(), upgrade(), Add enrichment fields index + webhook c…, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
