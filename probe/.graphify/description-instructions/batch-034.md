# Node Description Batch 35 of 92

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

- "tests_test_new_scanners_testdeltaengine_test_summary_counts": ".test_summary_counts()" | kind=code-symbol | source=tests/test_new_scanners.py:L485 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_nmap_xml_safety": "test_nmap_xml_safety.py" | kind=code-symbol | source=tests/test_nmap_xml_safety.py:L1 | neighbors=[56508b2 Add unit tests for XML parsing,…, TestNmapEntityGuard, test_nmap_xml_safety.py — nmap XML pars…]
- "tests_test_os_fingerprint_testicmpcapability": "TestIcmpCapability" | kind=code-symbol | source=tests/test_os_fingerprint.py:L270 | neighbors=[test_os_fingerprint.py, .test_available_when_socket_ok(), .test_unavailable_when_socket_raises()]
- "tests_test_os_fingerprint_testicmptimestamps_ts_reply": "._ts_reply()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L96 | neighbors=[TestIcmpTimestamps, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit()]
- "tests_test_os_fingerprint_testinetchecksum": "TestInetChecksum" | kind=code-symbol | source=tests/test_os_fingerprint.py:L24 | neighbors=[test_os_fingerprint.py, .test_checksum_handles_odd_length(), .test_checksum_verifies_to_zero()]
- "tests_test_os_fingerprint_testremoteclock": "TestRemoteClock" | kind=code-symbol | source=tests/test_os_fingerprint.py:L123 | neighbors=[test_os_fingerprint.py, .test_high_bit_marks_nonstandard_clock(), .test_standard_value_decodes_to_wall_cl…]
- "tests_test_os_fingerprint_testtimestampfallback_scanner": "._scanner()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L139 | neighbors=[TestTimestampFallback, .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_port_catalog": "test_port_catalog.py" | kind=code-symbol | source=tests/test_port_catalog.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, test_modern_infra_ports_present(), gates.py]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=tests/test_probe_core.py:L893 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_scan_funnel_recordingdeep": "RecordingDeep" | kind=code-symbol | source=tests/test_scan_funnel.py:L47 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target()]
- "tests_test_scanner_parity_py_files": "_py_files()" | kind=code-symbol | source=tests/test_scanner_parity.py:L25 | neighbors=[test_scanner_parity.py, test_no_extra_scanner_files(), test_scanner_is_superset_of_no_missing_…]
- "tests_test_scanner_parity_test_no_extra_scanner_files": "test_no_extra_scanner_files()" | kind=code-symbol | source=tests/test_scanner_parity.py:L38 | neighbors=[test_scanner_parity.py, scanner/ must not carry modules that ma…, _py_files()]
- "tests_test_scanner_parity_test_scanner_is_superset_of_no_missing_files": "test_scanner_is_superset_of_no_missing_files()" | kind=code-symbol | source=tests/test_scanner_parity.py:L29 | neighbors=[test_scanner_parity.py, Every scanner module authored in main_s…, _py_files()]
- "tests_test_scope_crypt_testkeygeneration": "TestKeyGeneration" | kind=code-symbol | source=tests/test_scope_crypt.py:L15 | neighbors=[test_scope_crypt.py, .test_generates_32_byte_keys(), .test_generates_different_keys_each_cal…]
- "tests_test_service_match_testnomatch": "TestNoMatch" | kind=code-symbol | source=tests/test_service_match.py:L87 | neighbors=[test_service_match.py, .test_empty_returns_none(), .test_unrecognized_returns_none()]
- "tests_test_service_match_testprobeladder": "TestProbeLadder" | kind=code-symbol | source=tests/test_service_match.py:L95 | neighbors=[test_service_match.py, .test_ladder_has_http_and_generic(), .test_ladder_starts_with_null_probe()]
- "tests_test_smb_scanner_smb2_error_response": "_smb2_error_response()" | kind=code-symbol | source=tests/test_smb_scanner.py:L14 | neighbors=[test_smb_scanner.py, An SMB2 ERROR response (e.g. STATUS_INV…, test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_test_error_response_not_parsed_as_signing": "test_error_response_not_parsed_as_signing()" | kind=code-symbol | source=tests/test_smb_scanner.py:L50 | neighbors=[test_smb_scanner.py, The confirmed bug: an SMB2 error respon…, _smb2_error_response()]
- "tests_test_smb_scanner_test_signing_supported_field_present": "test_signing_supported_field_present()" | kind=code-symbol | source=tests/test_smb_scanner.py:L71 | neighbors=[test_smb_scanner.py, Step 13: expose signing_supported (prot…, _smb2_negotiate_response()]
- "tests_test_syn_scanner_synack_with_options": "_synack_with_options()" | kind=code-symbol | source=tests/test_syn_scanner.py:L325 | neighbors=[test_syn_scanner.py, A SYN/ACK carrying an MSS option (data …, .test_window_ttl_mss_surfaced()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle": "TestAdaptiveTimeoutToggle" | kind=code-symbol | source=tests/test_syn_scanner.py:L381 | neighbors=[test_syn_scanner.py, .test_adaptive_on_by_default(), .test_can_disable()]
- "tests_test_syn_scanner_testparsepacketsignals": "TestParsePacketSignals" | kind=code-symbol | source=tests/test_syn_scanner.py:L335 | neighbors=[test_syn_scanner.py, .test_no_options_gives_none_mss(), .test_window_ttl_mss_surfaced()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-034.json

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
