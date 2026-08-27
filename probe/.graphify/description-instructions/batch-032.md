# Node Description Batch 33 of 92

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

- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=scanner/syn_scanner.py:L125 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…]
- "scanner_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=scanner/syn_scanner.py:L209 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__()]
- "scanner_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=scanner/syn_scanner.py:L415 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking()]
- "scanner_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/syn_scanner.py:L284 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…]
- "scanner_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=scanner/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=scanner/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=scanner/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=scanner/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe()]
- "scanner_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=scanner/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe()]
- "scanner_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=scanner/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe()]
- "scanner_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=scanner/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe()]
- "scanner_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=scanner/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe()]
- "scanner_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "scanner_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L290 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe()]
- "scanner_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=scanner/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "scanner_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=scanner/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=scanner/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…]
- "tests_test_adaptive_rate_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=tests/test_adaptive_rate.py:L177 | neighbors=[test_adaptive_rate.py, .connection_made(), .datagram_received()]
- "tests_test_async_udp_echoprotocol": "_EchoProtocol" | kind=code-symbol | source=tests/test_async_udp.py:L23 | neighbors=[test_async_udp.py, .connection_made(), .datagram_received()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_identified": ".test_mysqlx_identified()" | kind=code-symbol | source=tests/test_db_scanner.py:L54 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_not_misread_as_oracle": ".test_mysqlx_not_misread_as_oracle()" | kind=code-symbol | source=tests/test_db_scanner.py:L59 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_reply_not_misread_as_mysqlx": ".test_oracle_reply_not_misread_as_mysqlx()" | kind=code-symbol | source=tests/test_db_scanner.py:L70 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_still_identified": ".test_oracle_still_identified()" | kind=code-symbol | source=tests/test_db_scanner.py:L64 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_tns_packet": "_tns_packet()" | kind=code-symbol | source=tests/test_db_scanner.py:L44 | neighbors=[test_db_scanner.py, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_db_scanner_xproto_frame": "_xproto_frame()" | kind=code-symbol | source=tests/test_db_scanner.py:L39 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_e2e_engagement_to_findings_test_real_scan_of_open_datastore_yields_manager_finding": "test_real_scan_of_open_datastore_yields_manager_finding()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L109 | neighbors=[test_e2e_engagement_to_findings.py, _manager(), _plant()]
- "tests_test_host_discovery_mobile_testlocallyadministered": "TestLocallyAdministered" | kind=code-symbol | source=tests/test_host_discovery_mobile.py:L32 | neighbors=[test_host_discovery_mobile.py, .test_globally_unique_macs(), .test_randomized_phone_macs()]
- "tests_test_host_discovery_mobile_testvendorlookup": "TestVendorLookup" | kind=code-symbol | source=tests/test_host_discovery_mobile.py:L44 | neighbors=[test_host_discovery_mobile.py, .test_known_oui(), .test_unknown_oui()]
- "tests_test_hw_bind_testgethwid": "TestGetHwId" | kind=code-symbol | source=tests/test_hw_bind.py:L11 | neighbors=[test_hw_bind.py, .test_deterministic_within_session(), .test_returns_32_hex_chars()]
- "tests_test_installer_contract_dry_run": "_dry_run()" | kind=code-symbol | source=tests/test_installer_contract.py:L55 | neighbors=[test_installer_contract.py, test_installer_accepts_enroll_token_and…, test_installer_without_token_still_show…]
- "tests_test_main_scripts_completeness_test_duplicate_port_is_detected": "test_duplicate_port_is_detected()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L39 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_full_scan_is_complete": "test_full_scan_is_complete()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L24 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_missing_port_is_detected": "test_missing_port_is_detected()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L32 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-032.json

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
