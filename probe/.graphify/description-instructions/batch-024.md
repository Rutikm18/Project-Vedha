# Node Description Batch 25 of 92

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

- "tests_test_main_scripts_hardening_make_smb2_error": "make_smb2_error()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L122 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), STATUS_INVALID_PARAMETER error response…, .test_error_response_not_trusted()]
- "tests_test_main_scripts_hardening_make_smb2_success": "make_smb2_success()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L113 | neighbors=[test_main_scripts_hardening.py, _smb2_header(), .test_success_response_signing_and_dial…, .test_success_signing_supported_not_req…]
- "tests_test_main_scripts_hardening_smb2_header": "_smb2_header()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L100 | neighbors=[test_main_scripts_hardening.py, make_smb2_error(), make_smb2_success(), A 64-byte SMB2 header. Caller prepends …]
- "tests_test_main_scripts_hardening_testudpstatemodel": "TestUdpStateModel" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L42 | neighbors=[test_main_scripts_hardening.py, ._scanner(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_scanner": "._scanner()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L43 | neighbors=[TestUdpStateModel, _scope(), .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_rdp_run": "_run()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L64 | neighbors=[test_main_scripts_rdp.py, test_confirmed_rdp_wins_dedup_over_port…, test_confirmed_rdp_with_nla_has_no_nla_…, test_confirmed_rdp_without_nla_is_high_…]
- "tests_test_main_scripts_unauth_run": "_run()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L51 | neighbors=[test_main_scripts_unauth.py, test_protected_redis_raises_no_unauth_f…, test_unauth_elasticsearch_is_high(), test_unauth_redis_is_critical_and_rce_f…]
- "tests_test_nmap_xml_safety_testnmapentityguard": "TestNmapEntityGuard" | kind=code-symbol | source=tests/test_nmap_xml_safety.py:L27 | neighbors=[test_nmap_xml_safety.py, .test_entity_declaration_is_refused(), .test_entity_guard_is_case_insensitive(), .test_legitimate_doctype_output_still_p…]
- "tests_test_os_fingerprint_testtimestampfallback": "TestTimestampFallback" | kind=code-symbol | source=tests/test_os_fingerprint.py:L138 | neighbors=[test_os_fingerprint.py, ._scanner(), .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=tests/test_probe_core.py:L227 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_probe_manifest_manifest": "_manifest()" | kind=code-symbol | source=tests/test_probe_manifest.py:L20 | neighbors=[test_probe_manifest.py, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…]
- "tests_test_resolve": "test_resolve.py" | kind=code-symbol | source=tests/test_resolve.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, _infos(), TestResolveFamily, test_resolve.py — resolve() address-fam…]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=tests/test_scan_funnel.py:L22 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=tests/test_scan_funnel.py:L34 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=tests/test_scan_funnel.py:L60 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=tests/test_scan_funnel.py:L190 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]
- "tests_test_syn_scanner_testchecksum": "TestChecksum" | kind=code-symbol | source=tests/test_syn_scanner.py:L27 | neighbors=[test_syn_scanner.py, .test_checksum_handles_odd_length(), .test_checksum_of_valid_ip_header_is_ze…, .test_tcp_checksum_verifies_to_zero()]
- "tests_test_syn_scanner_testclassify": "TestClassify" | kind=code-symbol | source=tests/test_syn_scanner.py:L94 | neighbors=[test_syn_scanner.py, .test_other_flags_are_none(), .test_rst_is_closed(), .test_syn_ack_is_open()]
- "tests_test_syn_scanner_testsynretransmit_patch": "._patch()" | kind=code-symbol | source=tests/test_syn_scanner.py:L209 | neighbors=[TestSynRetransmit, .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…]
- "tests_test_syn_scanner_testsynscannerfallback": "TestSynScannerFallback" | kind=code-symbol | source=tests/test_syn_scanner.py:L157 | neighbors=[test_syn_scanner.py, .test_fallback_detects_open_port_on_loo…, .test_fallback_labels_scanner_name(), .test_forced_fallback_builds_connect_sc…]
- "tests_test_syn_scanner_testverifyreplycookie_make_synack_reply": "._make_synack_reply()" | kind=code-symbol | source=tests/test_syn_scanner.py:L110 | neighbors=[TestVerifyReplyCookie, .test_reply_from_other_host_fails(), .test_valid_cookie_verifies(), .test_wrong_ack_fails()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=tests/test_transport.py:L339 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=tests/test_transport.py:L501 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=tests/test_transport.py:L372 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=tests/test_transport.py:L294 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-024.json

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
