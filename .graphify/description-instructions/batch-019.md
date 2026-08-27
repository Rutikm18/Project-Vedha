# Node Description Batch 20 of 92

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

- "tests_test_main_scripts_coverage_summary": "_summary()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L35 | neighbors=[test_main_scripts_coverage.py, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state(), .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_errno_oserr": "_oserr()" | kind=code-symbol | source=tests/test_main_scripts_errno.py:L17 | neighbors=[test_main_scripts_errno.py, test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_scanner_side_errors_are_error_not_…, test_unknown_errno_is_self_identifying_…]
- "tests_test_main_scripts_hardening_testosconfidence": "TestOsConfidence" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L73 | neighbors=[test_main_scripts_hardening.py, .test_linux_ttl_only_capped(), .test_no_signal_is_unknown(), .test_ttl_only_is_not_absolute(), .test_two_signals_beat_one()]
- "tests_test_main_scripts_hardening_testsmbparsing": "TestSmbParsing" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L131 | neighbors=[test_main_scripts_hardening.py, .test_error_response_not_trusted(), .test_negotiate_request_excludes_smb311…, .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_new_scanners_testversionchange": "TestVersionChange" | kind=code-symbol | source=tests/test_new_scanners.py:L361 | neighbors=[test_new_scanners.py, .test_different_versions(), .test_empty_old_version(), .test_same_version(), .test_whitespace_normalised()]
- "tests_test_os_fingerprint_testacceptechoreply_reply": "._reply()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L170 | neighbors=[TestAcceptEchoReply, .test_accepts_echo_reply_from_target(), .test_accepts_when_source_unknown(), .test_rejects_non_echo_type(), .test_rejects_reply_from_a_different_ho…]
- "tests_test_os_fingerprint_testicmpbuilders": "TestIcmpBuilders" | kind=code-symbol | source=tests/test_os_fingerprint.py:L37 | neighbors=[test_os_fingerprint.py, .test_address_mask_request_type(), .test_echo_payload_preserved(), .test_echo_request_type_and_checksum(), .test_timestamp_request_type()]
- "tests_test_os_fingerprint_testicmpparse": "TestIcmpParse" | kind=code-symbol | source=tests/test_os_fingerprint.py:L62 | neighbors=[test_os_fingerprint.py, ._ip_icmp(), .test_parse_extracts_ttl_and_type(), .test_parse_raw_icmp_without_ip_header(), .test_parse_rejects_short()]
- "tests_test_os_fingerprint_testicmptimestamps": "TestIcmpTimestamps" | kind=code-symbol | source=tests/test_os_fingerprint.py:L95 | neighbors=[test_os_fingerprint.py, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit(), .test_parse_rejects_short_body(), ._ts_reply()]
- "tests_test_passive_collector_socket": "_Socket" | kind=code-symbol | source=tests/test_passive_collector.py:L23 | neighbors=[test_passive_collector.py, .close(), .fileno(), .__init__(), test_subset_listener_failure_reports_de…]
- "tests_test_probe_core_testenginesummary": "TestEngineSummary" | kind=code-symbol | source=tests/test_probe_core.py:L604 | neighbors=[test_probe_core.py, .test_affirmative_fact_creates_one_dedu…, .test_negative_or_ambiguous_facts_do_no…, .test_open_port_count_deduplicates_conf…, .test_open_port_count_excludes_host_liv…]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=tests/test_probe_core.py:L276 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=tests/test_probe_core.py:L390 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=tests/test_probe_core.py:L405 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=tests/test_probe_core.py:L816 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=tests/test_probe_core.py:L847 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_resolve_infos": "_infos()" | kind=code-symbol | source=tests/test_resolve.py:L11 | neighbors=[test_resolve.py, Fake getaddrinfo results: (family, sock…, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…]
- "tests_test_resolve_testresolvefamily": "TestResolveFamily" | kind=code-symbol | source=tests/test_resolve.py:L20 | neighbors=[test_resolve.py, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…, .test_unresolvable_raises()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=tests/test_result_spool.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, result_spool.py, spool(), TestResultSpool, Tests for agent/result_spool.py]
- "tests_test_router_db": "test_router_db.py" | kind=code-symbol | source=tests/test_router_db.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, test_mysql_greeting_on_odd_port(), test_plain_http_is_not_db(), test_redis_noauth_signature(), router.py]
- "tests_test_scan_funnel_testrouteports": "TestRoutePorts" | kind=code-symbol | source=tests/test_scan_funnel.py:L98 | neighbors=[test_scan_funnel.py, .test_intersection_only(), .test_no_match_returns_empty(), .test_port_in_multiple_routes(), .test_sorted_output()]
- "tests_test_scope_crypt": "test_scope_crypt.py" | kind=code-symbol | source=tests/test_scope_crypt.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, scope_crypt.py, TestEncryptDecryptRoundtrip, TestKeyGeneration, Tests for agent/scope_crypt.py]
- "tests_test_service_match_testhttpmatch": "TestHttpMatch" | kind=code-symbol | source=tests/test_service_match.py:L35 | neighbors=[test_service_match.py, .test_apache_version(), .test_iis_version(), .test_nginx_version(), .test_nginx_without_version()]
- "tests_test_syn_scanner_testbuildresultsenrichment_scanner": "._scanner()" | kind=code-symbol | source=tests/test_syn_scanner.py:L349 | neighbors=[TestBuildResultsEnrichment, .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_windows_ttl_maps_to_windows()]
- "tests_test_syn_scanner_testpacketroundtrip": "TestPacketRoundTrip" | kind=code-symbol | source=tests/test_syn_scanner.py:L68 | neighbors=[test_syn_scanner.py, .test_ip_checksum_valid_in_full_packet(), .test_parse_rejects_short_packet(), .test_syn_flag_is_set(), .test_syn_packet_parses_back_to_fields()]
- "tests_test_syn_scanner_testsyncookie": "TestSynCookie" | kind=code-symbol | source=tests/test_syn_scanner.py:L47 | neighbors=[test_syn_scanner.py, .test_cookie_is_32_bit(), .test_cookie_is_deterministic(), .test_cookie_varies_with_key(), .test_cookie_varies_with_port()]
- "tests_test_syn_scanner_testverifyreplycookie": "TestVerifyReplyCookie" | kind=code-symbol | source=tests/test_syn_scanner.py:L109 | neighbors=[test_syn_scanner.py, ._make_synack_reply(), .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_tarpit_testportscannertarpitflag": "TestPortScannerTarpitFlag" | kind=code-symbol | source=tests/test_tarpit.py:L42 | neighbors=[test_tarpit.py, ._scanner(), ._summary(), .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tls_fingerprint_testclienthello": "TestClientHello" | kind=code-symbol | source=tests/test_tls_fingerprint.py:L22 | neighbors=[test_tls_fingerprint.py, .test_contains_client_hello_handshake_t…, .test_contains_sni_hostname(), .test_declared_lengths_are_consistent(), .test_is_tls_handshake_record()]
- "tests_test_tls_fingerprint_testparseserverhello": "TestParseServerHello" | kind=code-symbol | source=tests/test_tls_fingerprint.py:L58 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_returns_none_on_alert(), .test_returns_none_on_short(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_posture_modern": "_modern()" | kind=code-symbol | source=tests/test_tls_posture.py:L68 | neighbors=[test_tls_posture.py, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_tls11(), .test_grade_f_tls10()]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=tests/test_transport.py:L530 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_web_methods": "test_web_methods.py" | kind=code-symbol | source=tests/test_web_methods.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, web_scanner.py, test_dangerous_methods_flagged(), test_no_allow_header(), test_safe_methods_only()]
- "tests_test_wire_identity_testjittereddelay": "TestJitteredDelay" | kind=code-symbol | source=tests/test_wire_identity.py:L57 | neighbors=[test_wire_identity.py, Evasion: blur a fixed scan cadence with…, .test_never_negative_even_at_full_jitte…, .test_stays_within_jitter_band(), .test_zero_or_negative_base_is_zero()]
- "workflow_report": "report.py" | kind=code-symbol | source=workflow/report.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, asset_to_dict(), diff_assets(), engagement_summary(), report.py — JSON-safe Asset serializati…]
- "agent_agent_check_anti_debug": "_check_anti_debug()" | kind=code-symbol | source=agent/agent.py:L927 | neighbors=[agent.py, say(), Detect common debugging/tracing tools. …, _startup_gauntlet()]
- "agent_agent_load_or_create_identity": "_load_or_create_identity()" | kind=code-symbol | source=agent/agent.py:L975 | neighbors=[agent.py, say(), _obtain_identity(), Load the probe's X25519 identity from p…]
- "agent_agent_manager_reachable": "_manager_reachable()" | kind=code-symbol | source=agent/agent.py:L156 | neighbors=[agent.py, _classify_connection_error(), GET /health. Returns (ok, human-detail)…, _wait_for_manager()]
- "agent_agent_result_summary": "_result_summary()" | kind=code-symbol | source=agent/agent.py:L106 | neighbors=[agent.py, main(), One-line, transparent summary of what a…, _ws_run_job()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-019.json

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
