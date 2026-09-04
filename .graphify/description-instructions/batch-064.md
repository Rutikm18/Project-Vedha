# Node Description Batch 65 of 330

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

- "tests_test_run_scoped_fact_scope": "test_run_scoped_fact_scope.py" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _fact(), TestRunScopedFactsAreExempt, TestTheScopeGateStillWorks, Run-scoped facts must not be scope-chec…]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt": "TestRunScopedFactsAreExempt" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L43 | neighbors=[test_run_scoped_fact_scope.py, .test_a_real_result_with_one_run_scoped…, .test_ipv6_discovery_auto_target_is_not…, .test_ipv6_discovery_interface_name_is_…, .test_run_scoped_fact_is_not_collected_…]
- "tests_test_runtime_requirements_coverage": "test_runtime_requirements_coverage.py" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _declared(), test_runtime_image_installs_every_wired…, test_runtime_is_a_subset_of_the_develop…, test_runtime_requirements_coverage.py —…]
- "tests_test_runtime_topology": "test_runtime_topology.py" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, main.py, test_manager_does_not_mount_a_static_da…, test_manager_root_is_service_metadata(), Product-boundary tests for the single-d…]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L24 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel(), ._funnel()]
- "tests_test_scan_funnel_fakemsrpc": "_FakeMSRPC" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L254 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), A deep scanner on 135 that returns EPM-…, ._funnel()]
- "tests_test_scan_funnel_opensetportfactory": "_OpenSetPortFactory" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L232 | neighbors=[test_scan_funnel.py, .__call__(), .__init__(), Port-scanner factory whose scanners rep…, ._funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L62 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner(), ._funnel()]
- "tests_test_scan_funnel_testrouteports": "TestRoutePorts" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L100 | neighbors=[test_scan_funnel.py, .test_intersection_only(), .test_no_match_returns_empty(), .test_port_in_multiple_routes(), .test_sorted_output()]
- "tests_test_scanner_congestion_fake_gai": "_fake_gai()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L287 | neighbors=[test_scanner_congestion.py, .test_deduplicates_repeated_addresses(), .test_family_filter_restricts_results(), .test_returns_every_family_in_order(), .test_v4_is_reachable_even_when_aaaa_so…]
- "tests_test_scanner_congestion_tcp_info_buf": "_tcp_info_buf()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L200 | neighbors=[test_scanner_congestion.py, A synthetic Linux `struct tcp_info`: 8 …, .test_absurd_values_are_rejected(), .test_never_synthesizes_an_initial_tcp_…, .test_tcp_info_yields_wscale_rtt_and_ad…]
- "tests_test_scanner_congestion_testreprobecleanuppass_rate_limited": "._rate_limited()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L341 | neighbors=[Silent for the first `answer_after` pro…, TestReprobeCleanupPass, .test_completeness_holds_after_correcti…, .test_disabled_reprobe_leaves_false_fil…, .test_recovers_ports_the_fast_sweep_cal…]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_completeness_holds_after_correction": ".test_completeness_holds_after_correction()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L383 | neighbors=[Corrected ports must be recorded ONCE, …, TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scanner_congestion_testwaitreadable": "TestWaitReadable" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L106 | neighbors=[test_scanner_congestion.py, .test_returns_false_when_nothing_arrive…, .test_returns_true_as_soon_as_data_is_w…, .test_unselectable_object_degrades_to_a…, .test_zero_timeout_never_blocks()]
- "tests_test_service_banner_ident_testladder": "TestLadder" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L142 | neighbors=[test_service_banner_ident.py, .test_client_first_ports_skip_null_rung…, .test_greet_timeout_tracks_operator_tim…, .test_no_tls_flag_drops_rung(), .test_tls_rung_present_after_http()]
- "tests_test_service_match_testhttpmatch": "TestHttpMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L35 | neighbors=[test_service_match.py, .test_apache_version(), .test_iis_version(), .test_nginx_version(), .test_nginx_without_version()]
- "tests_test_service_posture_rules_test_experimental_scanner_findings_are_suspected_not_confirmed": "test_experimental_scanner_findings_are_suspected_not_confirmed()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L217 | neighbors=[test_service_posture_rules.py, None of the new service scanners is rig…, _asset(), _corpus(), _fact()]
- "tests_test_service_posture_rules_testrdpnonla": "TestRdpNoNla" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L166 | neighbors=[test_service_posture_rules.py, .test_fires_from_the_first_probe_when_i…, .test_fires_from_the_second_probe_when_…, .test_no_longer_reports_schema_drift(), .test_silent_when_nla_is_required()]
- "tests_test_service_posture_rules_testrdpnonla_test_no_longer_reports_schema_drift": ".test_no_longer_reports_schema_drift()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L187 | neighbors=[The regression this fixes: `nla` was de…, TestRdpNoNla, _asset(), _corpus(), _fact()]
- "tests_test_sla_policy_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L36 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_sla_policy_testslapolicyroutes": "TestSlaPolicyRoutes" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L52 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent(), .test_resolve_windows_fallback_and_cust…]
- "tests_test_smb_ldap_scanners_testldapscanner": "TestLDAPScanner" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L103 | neighbors=[test_smb_ldap_scanners.py, ._sc(), .test_anon_refused_is_filtered(), .test_anonymous_bind_open(), .test_no_ldap_is_filtered()]
- "tests_test_smb_ldap_scanners_testridranges": "TestRidRanges" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L28 | neighbors=[test_smb_ldap_scanners.py, .test_is_bounded_no_brute_sweep(), .test_parses_enum4linux_default(), .test_reversed_range_tolerated(), .test_single_and_bad_tokens()]
- "tests_test_smtp_scanner_testsmtpfindings": "TestSMTPFindings" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L50 | neighbors=[test_smtp_scanner.py, ._fact(), .test_expn_alone_triggers_enum(), .test_hardened_is_silent(), .test_user_enum_and_no_starttls()]
- "tests_test_ssh_scanner_testsshfindings": "TestSSHFindings" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L193 | neighbors=[test_ssh_scanner.py, ._fact(), .test_clean_server_raises_nothing(), .test_terrapin_raises_finding(), .test_weak_algorithms_raise_finding()]
- "tests_test_ssh_scanner_testterrapinfidelity": "TestTerrapinFidelity" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L291 | neighbors=[test_ssh_scanner.py, ._ev(), .test_cbc_plus_etm_is_vulnerable_withou…, .test_cbc_without_etm_mac_is_not_terrap…, .test_chacha20_without_openssh_suffix_s…]
- "tests_test_ssh_scanner_testterrapinfidelity_ev": "._ev()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L292 | neighbors=[TestTerrapinFidelity, _kexinit(), .test_cbc_plus_etm_is_vulnerable_withou…, .test_cbc_without_etm_mac_is_not_terrap…, .test_chacha20_without_openssh_suffix_s…]
- "tests_test_stage2_reconcile_test_dead_lettered_facts_event_is_error": "test_dead_lettered_facts_event_is_error()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L150 | neighbors=[test_stage2_reconcile.py, _job(), _rows(), _scalars(), _user()]
- "tests_test_stage2_reconcile_test_stalled_when_queue_overdue": "test_stalled_when_queue_overdue()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L132 | neighbors=[test_stage2_reconcile.py, _job(), _rows(), _scalars(), _user()]
- "tests_test_syn_scanner_testpacketroundtrip": "TestPacketRoundTrip" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L68 | neighbors=[test_syn_scanner.py, .test_ip_checksum_valid_in_full_packet(), .test_parse_rejects_short_packet(), .test_syn_flag_is_set(), .test_syn_packet_parses_back_to_fields()]
- "tests_test_syn_scanner_testsyncookie": "TestSynCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L47 | neighbors=[test_syn_scanner.py, .test_cookie_is_32_bit(), .test_cookie_is_deterministic(), .test_cookie_varies_with_key(), .test_cookie_varies_with_port()]
- "tests_test_syn_scanner_testtcpoptionprofile": "TestTcpOptionProfile" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L403 | neighbors=[test_syn_scanner.py, .test_malformed_options_do_not_raise(), .test_parse_linux_syn_ack_options(), .test_parse_mss_shim_still_works(), .test_parse_windows_syn_ack_options()]
- "tests_test_syn_scanner_testverifyreplycookie": "TestVerifyReplyCookie" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L109 | neighbors=[test_syn_scanner.py, ._make_synack_reply(), .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_tarpit_testportscannertarpitflag": "TestPortScannerTarpitFlag" | kind=code-symbol | source=probe/tests/test_tarpit.py:L42 | neighbors=[test_tarpit.py, ._scanner(), ._summary(), .test_all_open_host_flagged_as_tarpit(), .test_mostly_closed_host_not_flagged()]
- "tests_test_tls_fingerprint_testclienthello": "TestClientHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L22 | neighbors=[test_tls_fingerprint.py, .test_contains_client_hello_handshake_t…, .test_contains_sni_hostname(), .test_declared_lengths_are_consistent(), .test_is_tls_handshake_record()]
- "tests_test_tls_fingerprint_testparseserverhello": "TestParseServerHello" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L58 | neighbors=[test_tls_fingerprint.py, .test_extracts_version_and_cipher(), .test_returns_none_on_alert(), .test_returns_none_on_short(), .test_tls13_version_from_supported_vers…]
- "tests_test_tls_port_coverage_testdeliberateexclusions": "TestDeliberateExclusions" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L66 | neighbors=[test_tls_port_coverage.py, Excluded on purpose — a bare ClientHell…, .test_rdp_is_excluded(), .test_starttls_upgrade_ports_excluded(), .test_winrm_plaintext_listeners_exclude…]
- "tests_test_tls_posture_modern": "_modern()" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L68 | neighbors=[test_tls_posture.py, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_tls11(), .test_grade_f_tls10()]
- "tests_test_transport_testwebsocket": "TestWebSocket" | kind=code-symbol | source=probe/tests/test_transport.py:L530 | neighbors=[test_transport.py, .test_is_ws_connected_false_by_default(), .test_ws_requires_token(), .test_ws_url_http(), .test_ws_url_https()]
- "tests_test_va_campaign_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L22 | neighbors=[test_va_campaign.py, _detect_stage(), _run(), test_catalog_ids_are_unique_and_match_d…, test_detect_stage_turns_facts_into_weak…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-064.json

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
