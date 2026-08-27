# Node Description Batch 24 of 92

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

- "scanner_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=scanner/os_fingerprint.py:L270 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…]
- "scanner_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=scanner/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…]
- "scanner_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=scanner/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "scanner_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=scanner/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "scanner_passive_collector_device_hint": "_device_hint()" | kind=code-symbol | source=scanner/passive_collector.py:L90 | neighbors=[passive_collector.py, _printable_strings(), .run(), Best-effort device label from an announ…]
- "scanner_passive_collector_passivecollector_select": "._select()" | kind=code-symbol | source=scanner/passive_collector.py:L331 | neighbors=[PassiveCollector, .run(), _is_readable(), Await readability on any listener witho…]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/port_scanner.py:L404 | neighbors=[PortScanner, ScanMetrics, .summary(), Bounded worker-pool scan of every reque…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=scanner/rdp_scanner.py:L83 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), One synchronous RDP handshake. Best-eff…]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=scanner/scanner_base.py:L756 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=scanner/scanner_base.py:L247 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=scanner/scanner_base.py:L340 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_service_banner_match_service": "match_service()" | kind=code-symbol | source=scanner/service_banner.py:L91 | neighbors=[service_banner.py, _dec(), Soft-match collected bytes to {service,…, ._grab()]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=scanner/service_banner.py:L173 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=scanner/service_enum.py:L465 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target()]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=scanner/syn_scanner.py:L118 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=scanner/syn_scanner.py:L151 | neighbors=[syn_scanner.py, _parse_mss(), Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking()]
- "scanner_syn_scanner_syn_cookie": "syn_cookie()" | kind=code-symbol | source=scanner/syn_scanner.py:L190 | neighbors=[syn_scanner.py, Keyed 32-bit ISN for (dst_ip, dst_port,…, ._syn_scan_blocking(), verify_reply_cookie()]
- "scanner_syn_scanner_verify_reply_cookie": "verify_reply_cookie()" | kind=code-symbol | source=scanner/syn_scanner.py:L197 | neighbors=[syn_scanner.py, A genuine reply to our SYN acknowledges…, ._syn_scan_blocking(), syn_cookie()]
- "scanner_tls_scanner_sni": "_sni()" | kind=code-symbol | source=scanner/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "scanner_tls_scanner_try_version": "_try_version()" | kind=code-symbol | source=scanner/tls_scanner.py:L155 | neighbors=[tls_scanner.py, Attempt a handshake forcing one protoco…, _scan_tls_sync(), _sni()]
- "scanner_unauth_access": "unauth_access.py" | kind=code-symbol | source=scanner/unauth_access.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _as_text(), classify_unauth_access(), is_rce_capable()]
- "scanner_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=scanner/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "tests_test_adaptive_rate_testudpscanneradaptive": "TestUdpScannerAdaptive" | kind=code-symbol | source=tests/test_adaptive_rate.py:L185 | neighbors=[test_adaptive_rate.py, .test_adaptive_scanner_creates_controll…, .test_adaptive_scanner_detects_open_on_…, .test_non_adaptive_scanner_has_no_contr…]
- "tests_test_adaptive_rate_testwindowgating": "TestWindowGating" | kind=code-symbol | source=tests/test_adaptive_rate.py:L79 | neighbors=[test_adaptive_rate.py, .test_acquire_blocks_when_window_full(), .test_release_unblocks_waiter(), .test_report_loss_shrinks_and_releases()]
- "tests_test_agent_identity_cached_transport": "_cached_transport()" | kind=code-symbol | source=tests/test_agent_identity.py:L11 | neighbors=[test_agent_identity.py, test_cached_identity_refreshes_current_…, test_cached_identity_retries_transient_…, test_rejected_cached_token_falls_back_t…]
- "tests_test_db_scanner_fakereader": "FakeReader" | kind=code-symbol | source=tests/test_db_scanner.py:L17 | neighbors=[test_db_scanner.py, .__init__(), .read(), _probe()]
- "tests_test_db_scanner_fakewriter": "FakeWriter" | kind=code-symbol | source=tests/test_db_scanner.py:L25 | neighbors=[test_db_scanner.py, .drain(), .write(), _probe()]
- "tests_test_db_unauth": "test_db_unauth.py" | kind=code-symbol | source=tests/test_db_unauth.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, db_scanner.py, test_redis_authenticated(), test_redis_unauthenticated()]
- "tests_test_integration_teststartupgauntlet": "TestStartupGauntlet" | kind=code-symbol | source=tests/test_integration.py:L431 | neighbors=[test_integration.py, Phase 5: startup gauntlet checks., .test_gauntlet_hw_bind_blocks(), .test_gauntlet_skips_in_dev_mode()]
- "tests_test_integration_testtaskrunnerwithencryptedscope": "TestTaskRunnerWithEncryptedScope" | kind=code-symbol | source=tests/test_integration.py:L100 | neighbors=[test_integration.py, Phase 4 + Phase 1: TaskRunner receives …, .test_decrypts_encrypted_scope_from_job…, .test_falls_back_when_decryption_fails()]
- "tests_test_integration_testtransportwithidentity": "TestTransportWithIdentity" | kind=code-symbol | source=tests/test_integration.py:L238 | neighbors=[test_integration.py, Phase 4 + Phase 1: Transport sends publ…, .test_register_sends_public_key(), .test_register_without_public_key()]
- "tests_test_main_scripts_coverage_scope": "_scope()" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L23 | neighbors=[test_main_scripts_coverage.py, _mk_scanner(), .test_default_ports_are_nmap_top100_not…, .test_open_only_output_still_keeps_full…]
- "tests_test_main_scripts_coverage_testdefaultsandadaptivetimeout": "TestDefaultsAndAdaptiveTimeout" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L186 | neighbors=[test_main_scripts_coverage.py, .test_adaptive_estimator_is_shared_and_…, .test_default_ports_are_nmap_top100_not…, .test_fixed_timeout_flag_disables_the_e…]
- "tests_test_main_scripts_datastore_probe_svc": "_svc()" | kind=code-symbol | source=tests/test_main_scripts_datastore_probe.py:L15 | neighbors=[test_main_scripts_datastore_probe.py, test_elasticsearch_and_couchdb_win_over…, test_memcached_version_and_stat_identif…, test_redis_info_and_noauth_identify_as_…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-023.json

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
