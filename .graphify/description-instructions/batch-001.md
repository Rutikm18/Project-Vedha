# Node Description Batch 2 of 92

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

- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=agent/task_runner.py:L39 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=scanner/udp_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, _dns_probe(), _ike_probe(), interpret_dns_recursion()]
- "tests_test_probe_next_features": "test_probe_next_features.py" | kind=code-symbol | source=tests/test_probe_next_features.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, engine.py, use_cases.py, scanner_base.py, _cache_with(), test_device_inventory_post_stage_classi…]
- "agent_transport_devicealreadyenrollederror": "DeviceAlreadyEnrolledError" | kind=code-symbol | source=agent/transport.py:L53 | neighbors=[Load or atomically create the probe's E…, Request UI approval, poll, prove key po…, One-line, transparent summary of what a…, Return (agent_id, token, fresh, identit…, Map a low-level connection exception to…, GET /health. Returns (ok, human-detail)…]
- "tests_test_probe_core_scan_result": "_scan_result()" | kind=code-symbol | source=tests/test_probe_core.py:L61 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory(), .test_alive_sets_timestamp(), .test_responding_ports(), .test_passive_facts_appended()]
- "main_scripts_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=main_scripts/port_scanner.py:L256 | neighbors=[port_scanner.py, BaseScanner, AdaptiveTimeout, ._attempt(), ._build(), .__init__()]
- "main_scripts_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=main_scripts/udp_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _dns_probe(), _ike_probe(), interpret_dns_recursion(), interpret_ike()]
- "main_scripts_findings_scanner": "_scanner()" | kind=code-symbol | source=main_scripts/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()]
- "scanner_findings_scanner": "_scanner()" | kind=code-symbol | source=scanner/findings.py:L110 | neighbors=[findings.py, build_service_index(), _rule_cleartext_and_exposure(), _rule_dns(), _rule_ftp(), _rule_ipmi()]
- "tests_test_result_spool_testresultspool": "TestResultSpool" | kind=code-symbol | source=tests/test_result_spool.py:L18 | neighbors=[test_result_spool.py, .test_byte_high_water_mark_pauses_new_w…, .test_custom_retry_config(), .test_exists(), .test_file_high_water_mark_pauses_new_w…, .test_flush_quarantines_permanent_rejec…]
- "main_scripts_findings_data": "_data()" | kind=code-symbol | source=main_scripts/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=main_scripts/scan_funnel.py:L109 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, DBScanner, HostDiscoveryScanner, MCPAIScanner]
- "main_scripts_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=main_scripts/scanner_base.py:L401 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "scanner_findings_data": "_data()" | kind=code-symbol | source=scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_dns(), _rule_ftp(), _rule_ipmi(), _rule_ldap()]
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=scanner/snmp_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c()]
- "main_scripts_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=main_scripts/iot_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner]
- "main_scripts_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp()]
- "main_scripts_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=main_scripts/scan_funnel.py:L83 | neighbors=[scan_funnel.py, DBScanner, HostDiscoveryScanner, MCPAIScanner, ResultWriter, ScanResult]
- "scanner_iot_scanner": "iot_scanner.py" | kind=code-symbol | source=scanner/iot_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, _coap_get_wellknown_core(), _decode_mdns_name(), _fetch_upnp_root_desc(), IoTScanner]
- "scanner_os_fingerprint": "os_fingerprint.py" | kind=code-symbol | source=scanner/os_fingerprint.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, accept_echo_reply(), build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp()]
- "tests_test_new_scanners_testudpprobeconstruction": "TestUDPProbeConstruction" | kind=code-symbol | source=tests/test_new_scanners.py:L121 | neighbors=[test_new_scanners.py, .test_ike_probe_header_fields(), .test_ike_probe_init_spi_not_zero(), .test_ike_probe_length_field_matches_ac…, .test_ike_probe_resp_spi_zero(), .test_interpret_ike_short_data()]
- "main_scripts_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=main_scripts/scanner_base.py:L365 | neighbors=[VA scanner module — pure collection/sca…, _ConnectSweep, MasscanRun, mass_scan.py — fast large-scale TCP por…, Parse masscan -oJ output robustly: hand…, target_specs: raw CIDRs/ranges/hosts (N…]
- "main_scripts_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _ber_len(), _ber_parse(), _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_host_discovery": "host_discovery.py" | kind=code-symbol | source=scanner/host_discovery.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, device_hint(), fuse_liveness(), HostDiscoveryScanner]
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=tests/test_cli.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, FakeClient, test_cmd_daemon_run_overrides_stale_env…, test_cmd_doctor_fails_when_no_agent_unl…, test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…]
- "tests_test_use_cases": "test_use_cases.py" | kind=code-symbol | source=tests/test_use_cases.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, use_cases.py, test_codes_are_unique_and_stable(), test_descriptions_do_not_overclaim(), test_every_code_maps_to_a_real_use_case…]
- "main_scripts_service_enum": "service_enum.py" | kind=code-symbol | source=main_scripts/service_enum.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology()]
- "main_scripts_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest()]
- "scanner_service_enum": "service_enum.py" | kind=code-symbol | source=scanner/service_enum.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, classify_roles(), _dns_read_name(), Enrichment, guess_os(), local_topology()]
- "scanner_tls_fingerprint": "tls_fingerprint.py" | kind=code-symbol | source=scanner/tls_fingerprint.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, build_client_hello(), cipher_code(), _ext(), fingerprint_host(), jarm_style_digest()]
- "tests_test_syn_scanner": "test_syn_scanner.py" | kind=code-symbol | source=tests/test_syn_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, scanner_base.py, _synack_with_options(), TestAdaptiveTimeoutToggle, TestBuildResultsEnrichment]
- "workflow_workflow_engine_run_engagement": "run_engagement()" | kind=code-symbol | source=workflow/workflow_engine.py:L269 | neighbors=[workflow_engine.py, Runs gates 0/2-6 (in order) across `tar…, _finalize_trace(), _gather_per_host(), _port_candidates(), _record()]
- "agent_local_run": "local_run.py" | kind=code-symbol | source=agent/local_run.py:L1 | neighbors=[agent.py, _clean(), _main(), _parse_args(), _port_label(), _ports_from_env()]
- "tests_test_async_udp": "test_async_udp.py" | kind=code-symbol | source=tests/test_async_udp.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, scanner_base.py, _EchoProtocol, _SinkProtocol, _start_server(), test_datagram_received_resolves_future_…]
- "tests_test_main_scripts_findings_ids": "_ids()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L19 | neighbors=[test_main_scripts_findings.py, test_accepts_scanresult_objects_not_jus…, test_all_security_headers_present_no_fi…, test_closed_port_no_finding(), test_ntp_monlist_and_dns_open_recursion…, test_open_filtered_never_raises_exposur…]
- "tests_test_new_scanners_testsnmpberutilities": "TestSNMPBerUtilities" | kind=code-symbol | source=tests/test_new_scanners.py:L24 | neighbors=[test_new_scanners.py, .test_ber_len_long_form_one_byte(), .test_ber_len_long_form_two_bytes(), .test_ber_len_short_form(), .test_ber_parse_empty(), .test_ber_parse_two_tlvs()]
- "workflow_modes": "modes.py" | kind=code-symbol | source=workflow/modes.py:L1 | neighbors=[engine.py, local_run.py, ae7a30b feat: add Posture & Patch-Compa…, test_probe_core.py, test_workflow_execution.py, assessment()]
- "main_scripts_host_discovery": "host_discovery.py" | kind=code-symbol | source=main_scripts/host_discovery.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, device_hint(), fuse_liveness(), HostDiscoveryScanner, is_locally_administered()]
- "scanner_db_scanner": "db_scanner.py" | kind=code-symbol | source=scanner/db_scanner.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, DBScanner, interpret_redis_info(), main(), _probe_mongodb(), _probe_mssql()]
- "scanner_syn_scanner": "syn_scanner.py" | kind=code-symbol | source=scanner/syn_scanner.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, a548359 feat(auto-enrollment): implemen…, build_ip_header(), build_syn_packet(), build_tcp_syn(), classify()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-001.json

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
