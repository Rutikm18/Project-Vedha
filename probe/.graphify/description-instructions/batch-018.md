# Node Description Batch 19 of 92

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

- "scanner_host_discovery_hostdiscoveryscanner": "HostDiscoveryScanner" | kind=code-symbol | source=scanner/host_discovery.py:L391 | neighbors=[host_discovery.py, BaseScanner, .__init__(), ._probe(), .scan_target()]
- "scanner_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=scanner/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "scanner_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=scanner/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "scanner_os_fingerprint_fingerprint_os": "fingerprint_os()" | kind=code-symbol | source=scanner/os_fingerprint.py:L178 | neighbors=[os_fingerprint.py, hop_estimate(), infer_initial_ttl(), .scan_target(), Combine available stack signals into a …]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=scanner/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_infer_initial_ttl": "infer_initial_ttl()" | kind=code-symbol | source=scanner/os_fingerprint.py:L152 | neighbors=[os_fingerprint.py, fingerprint_os(), hop_estimate(), os_family_from_ttl(), Round the observed TTL up to the neares…]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=scanner/os_fingerprint.py:L329 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "scanner_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=scanner/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), RuntimeError, .__init__(), All passive sources failed before the l…]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=scanner/port_scanner.py:L324 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…]
- "scanner_scanner_base_async_udp_probe": "async_udp_probe()" | kind=code-symbol | source=scanner/scanner_base.py:L596 | neighbors=[scanner_base.py, .close(), _UDPProbeProtocol, async_udp_probe_retry(), Send one UDP datagram and await the fir…]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=scanner/scanner_base.py:L768 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=scanner/scanner_base.py:L365 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=scanner/scanner_base.py:L200 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json()]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=scanner/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "scanner_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=scanner/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=scanner/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()]
- "scanner_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=scanner/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "scanner_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=scanner/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "scanner_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=scanner/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=scanner/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "scanner_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=scanner/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "scanner_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=scanner/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "scanner_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L62 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "scanner_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…]
- "scanner_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=scanner/tls_fingerprint.py:L282 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=scanner/tls_scanner.py:L272 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=scanner/vantage_matrix.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …]
- "scanner_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=scanner/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "tests_test_adaptive_rate_testudpretransmit": "TestUdpRetransmit" | kind=code-symbol | source=tests/test_adaptive_rate.py:L119 | neighbors=[test_adaptive_rate.py, .test_retries_exhaust_on_silence(), .test_retry_recovers_dropped_reply(), .test_returns_immediately_on_closed(), .test_returns_immediately_on_reply()]
- "tests_test_device_identity": "test_device_identity.py" | kind=code-symbol | source=tests/test_device_identity.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, device_identity.py, test_device_identity_rejects_invalid_pr…, test_device_identity_round_trip_and_sig…, test_site_policy_signature_and_tofu_pin…]
- "tests_test_e2e_engagement_to_findings_manager": "_manager()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L51 | neighbors=[test_e2e_engagement_to_findings.py, Return (http_get, submit_result, captur…, test_engagement_dispatch_reaches_probe_…, test_out_of_scope_target_is_refused_end…, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_vulnerable_host_facts": "_vulnerable_host_facts()" | kind=code-symbol | source=tests/test_e2e_engagement_to_findings.py:L137 | neighbors=[test_e2e_engagement_to_findings.py, Exactly what the probe's smb/port scann…, test_correlated_findings_cite_their_bas…, test_manager_correlation_finds_all_thre…, test_ntlm_relay_is_high_when_smbv1_pres…]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=tests/test_hw_bind.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]
- "tests_test_main_scripts_correlation_get": "_get()" | kind=code-symbol | source=tests/test_main_scripts_correlation.py:L21 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_legacy_windows_surface_smbv1_plus_…, test_ntlm_relay_is_high_when_smbv1_also…, test_ntlm_relay_is_medium_when_only_sig…]
- "tests_test_main_scripts_correlation_ids": "_ids()" | kind=code-symbol | source=tests/test_main_scripts_correlation.py:L17 | neighbors=[test_main_scripts_correlation.py, test_correlation_does_not_cross_hosts(), test_no_legacy_surface_with_only_smbv1(), test_no_relay_finding_when_signing_requ…, test_single_cleartext_service_does_not_…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-018.json

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
