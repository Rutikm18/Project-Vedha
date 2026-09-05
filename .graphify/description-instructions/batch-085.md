# Node Description Batch 86 of 336

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

- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L36 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L192 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testrpcreconcile": "TestRpcReconcile" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L266 | neighbors=[test_scan_funnel.py, ._funnel(), .test_advertised_ports_are_scanned_and_…, .test_no_dynamic_ports_no_reconcile_sta…]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_silent": "._silent()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L145 | neighbors=[TestConnectCongestionWindow, .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_scan_completes_every_port_under_t…]
- "tests_test_scanner_congestion_testharvesttcpstack_test_never_synthesizes_an_initial_tcp_window": ".test_never_synthesizes_an_initial_tcp_window()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L263 | neighbors=[THE accuracy guarantee for #6b.        …, TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_disabled_reprobe_leaves_false_filtered_in_place": ".test_disabled_reprobe_leaves_false_filtered_in_place()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L396 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_genuinely_filtered_ports_stay_filtered": ".test_genuinely_filtered_ports_stay_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L368 | neighbors=[TestReprobeCleanupPass, _scanner(), ._silent_attempt(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_recovers_ports_the_fast_sweep_called_filtered": ".test_recovers_ports_the_fast_sweep_called_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L355 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_service_posture_rules_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L28 | neighbors=[test_service_posture_rules.py, _fire(), test_experimental_scanner_findings_are_…, .test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_test_smb_null_session_is_silent_on_the_live_host": "test_smb_null_session_is_silent_on_the_live_host()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L98 | neighbors=[test_service_posture_rules.py, The live host REFUSED the null bind (ST…, _corpus(), _fire()]
- "tests_test_service_posture_rules_test_ssh_rules_against_live_capture": "test_ssh_rules_against_live_capture()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L72 | neighbors=[test_service_posture_rules.py, The live Windows host offers OpenSSH 9.…, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnonla_test_fires_from_the_second_probe_when_the_first_failed": ".test_fires_from_the_second_probe_when_the_first_failed()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L167 | neighbors=[The live-host case: negotiation returne…, TestRdpNoNla, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnotls": "TestRdpNoTls" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L198 | neighbors=[test_service_posture_rules.py, .test_fires_on_ssl_not_allowed(), .test_ignores_uninterpreted_failure_cod…, .test_silent_when_negotiation_succeeded…]
- "tests_test_sla_policy_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L32 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_custom_when_row_present": ".test_get_custom_when_row_present()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L58 | neighbors=[TestSlaPolicyRoutes, _db(), _operator(), _row()]
- "tests_test_smb_ldap_scanners_testldaptimeouttypes": "TestLDAPTimeoutTypes" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L135 | neighbors=[test_smb_ldap_scanners.py, ldap3 packs receive_timeout into a stru…, .test_receive_timeout_is_an_int(), .test_sub_second_timeout_does_not_floor…]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing": "TestNtlmFingerprintFraming" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L79 | neighbors=[test_smb_ntlm_build.py, Regression: _recv_smb_frame STRIPS the …, .test_end_to_end_framing_extracts_build…, .test_ntlm_os_build_shared_function()]
- "tests_test_smb_ntlm_build_testtype1andspnego": "TestType1AndSpnego" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L143 | neighbors=[test_smb_ntlm_build.py, .test_session_setup_packet_shape(), .test_spnego_wraps_and_contains_type1(), .test_type1_sets_negotiate_version()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_smtp_scanner_testsmtpfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L51 | neighbors=[TestSMTPFindings, .test_expn_alone_triggers_enum(), .test_hardened_is_silent(), .test_user_enum_and_no_starttls()]
- "tests_test_smtp_scanner_testsmtpscanner": "TestSMTPScanner" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L31 | neighbors=[test_smtp_scanner.py, ._sc(), .test_no_smtp_filtered(), .test_open()]
- "tests_test_ssh_scanner_testnofalsepositives": "TestNoFalsePositives" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L271 | neighbors=[test_ssh_scanner.py, ._eval(), .test_ed25519_hostkey_is_clean(), .test_rsa_sha2_hostkeys_are_not_failure…]
- "tests_test_ssh_scanner_testparsebanner": "TestParseBanner" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L51 | neighbors=[test_ssh_scanner.py, .test_dropbear_no_comments_from_bytes(), .test_openssh_with_comments(), .test_rejects_non_ssh()]
- "tests_test_ssh_scanner_testparsekexinit": "TestParseKexinit" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L69 | neighbors=[test_ssh_scanner.py, .test_empty_language_list(), .test_handles_payload_without_leading_t…, .test_parses_all_name_lists()]
- "tests_test_ssh_scanner_testsshfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L194 | neighbors=[TestSSHFindings, .test_clean_server_raises_nothing(), .test_terrapin_raises_finding(), .test_weak_algorithms_raise_finding()]
- "tests_test_ssh_scanner_testsshscanner": "TestSSHScanner" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L164 | neighbors=[test_ssh_scanner.py, ._scanner(), .test_no_response_is_filtered(), .test_weak_server_reports_open_with_fai…]
- "tests_test_ssh_scanner_testvendoreddb": "TestVendoredDB" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L219 | neighbors=[test_ssh_scanner.py, .test_full_db_is_large_not_a_subset(), .test_gss_wildcard_match(), .test_lookup_exact_and_unknown()]
- "tests_test_stage2_reconcile_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L44 | neighbors=[test_stage2_reconcile.py, test_fresh_heartbeat_reports_worker_ali…, test_multi_agent_all_covered_is_complet…, test_multi_agent_latest_done_but_earlie…]
- "tests_test_syn_scanner_synack_with_options": "_synack_with_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L326 | neighbors=[test_syn_scanner.py, A SYN/ACK carrying an MSS option (data …, .test_window_ttl_mss_surfaced(), A SYN/ACK carrying an MSS option (data …]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L27 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L94 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynretransmit_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L209 | neighbors=[TestSynRetransmit, .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L157 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L110 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-085.json

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
