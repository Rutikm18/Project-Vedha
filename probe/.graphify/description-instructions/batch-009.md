# Node Description Batch 10 of 92

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "main_scripts_syn_scanner_rationale_180": "SYN/ACK -> open, RST -> closed, anything else -> None (indeterminate)." | kind=entity | source=main_scripts/syn_scanner.py:L180 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_191": "Keyed 32-bit ISN for (dst_ip, dst_port, src_port). Reply.ack == cookie+1." | kind=entity | source=main_scripts/syn_scanner.py:L191 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_198": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=main_scripts/syn_scanner.py:L198 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_211": "True only when a real SYN scan can work: Linux (BSD/macOS raw sockets can't" | kind=entity | source=main_scripts/syn_scanner.py:L211 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_syn_scanner_rationale_232": "Outbound-interface IP for reaching dst_ip (no packets sent — UDP connect)." | kind=entity | source=main_scripts/syn_scanner.py:L232 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_246": "SYN scan on privileged Linux; transparent connect-scan fallback elsewhere." | kind=entity | source=main_scripts/syn_scanner.py:L246 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_418": "Turn resolved port states + harvested intel into ScanResults. Pure —         no" | kind=entity | source=main_scripts/syn_scanner.py:L418 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=en
- "main_scripts_syn_scanner_rationale_82": "Build a 20-byte IPv4 header with a valid checksum.      NOTE (BSD caveat): on ma" | kind=entity | source=main_scripts/syn_scanner.py:L82 | neighbors=[AdaptiveTimeout, PortScanner, BaseScanner, ResultWriter, ScanResult, ScopeGuard] | lang=pt
- "main_scripts_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=main_scripts/tls_fingerprint.py:L86 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()] | lang=en
- "scanner_delta_scanner_deltaengine_load_jsonl": ".load_jsonl()" | kind=code-symbol | source=scanner/delta_scanner.py:L160 | neighbors=[DeltaEngine, _extract_service(), _extract_version(), ScanRecord, _stable_host_id(), main()] | lang=en
- "scanner_findings_by_target": "_by_target()" | kind=code-symbol | source=scanner/findings.py:L1006 | neighbors=[findings.py, _corr_anon_data_exposure(), _corr_cleartext_cluster(), _corr_legacy_windows(), _corr_mgmt_plane_exposed(), _corr_ntlm_relay()] | lang=en
- "scanner_ja4s_ja4s_from_parsed": "ja4s_from_parsed()" | kind=code-symbol | source=scanner/ja4s.py:L99 | neighbors=[ja4s.py, compute_ja4s(), _ext_types(), ja4s_from_fields(), _selected_alpn(), ja4s_from_serverhello()] | lang=en
- "scanner_ja4x": "ja4x.py" | kind=code-symbol | source=scanner/ja4x.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _hash_oids(), ja4x_from_cert(), ja4x_from_der(), ja4x_from_oid_lists(), match_suspicious()] | lang=en
- "scanner_mass_scan_run_mass_scan": "run_mass_scan()" | kind=code-symbol | source=scanner/mass_scan.py:L237 | neighbors=[mass_scan.py, target_specs: raw CIDRs/ranges/hosts (N…, _ConnectSweep, _have_masscan(), _masscan_excludes(), _masscan_records_to_results()] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner": "MCPAIScanner" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L199 | neighbors=[mcp_ai_scanner.py, BaseScanner, ._fetch(), .__init__(), ._probe_port(), ._result()] | lang=en
- "scanner_mcp_ai_scanner_mcpaiscanner_probe_port": "._probe_port()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L237 | neighbors=[MCPAIScanner, _auth_shaped_json_body(), _known_false_positive(), _mcp_oauth_signal(), ._fetch(), ._result()] | lang=en
- "scanner_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=scanner/os_fingerprint.py:L286 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), ._icmp_timestamp(), .__init__(), .scan_target()] | lang=en
- "scanner_passive_collector_passivecollector_run": ".run()" | kind=code-symbol | source=scanner/passive_collector.py:L222 | neighbors=[PassiveCollector, _coverage(), _device_hint(), _listener_error_code(), _open_listener(), ._select()] | lang=en
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=scanner/port_scanner.py:L256 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._scan_port()] | lang=en
- "scanner_run_all": "run_all.py" | kind=code-symbol | source=scanner/run_all.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, _log(), main(), _open_tcp_ports(), _ports_arg(), _read_jsonl()] | lang=en
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=scanner/scanner_base.py:L864 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()] | lang=en
- "scanner_scanner_base_udpprobeprotocol": "_UDPProbeProtocol" | kind=code-symbol | source=scanner/scanner_base.py:L564 | neighbors=[scanner_base.py, async_udp_probe(), One-shot datagram protocol backing `asy…, .connection_lost(), .datagram_received(), .error_received()] | lang=en
- "scanner_service_enum_serviceenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/service_enum.py:L529 | neighbors=[ServiceEnumScanner, classify_roles(), Enrichment, guess_os(), resolve_hostnames(), ._probe_port()] | lang=en
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L86 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()] | lang=en
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=scanner/windows_collector.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…] | lang=en
- "tests_test_host_discovery_mobile": "test_host_discovery_mobile.py" | kind=code-symbol | source=tests/test_host_discovery_mobile.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, host_discovery.py, TestDeviceHint, TestLocallyAdministered, TestNormalizeMac, TestVendorLookup] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac": "TestNormalizeMac" | kind=code-symbol | source=tests/test_host_discovery_mobile.py:L9 | neighbors=[test_host_discovery_mobile.py, .test_extracts_from_arp_line(), .test_lowercases(), .test_rejects_broadcast(), .test_rejects_garbage(), .test_rejects_multicast()] | lang=en
- "tests_test_installer_contract": "test_installer_contract.py" | kind=code-symbol | source=tests/test_installer_contract.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, _dry_run(), test_installer_accepts_enroll_token_and…, test_installer_rejects_missing_or_unkno…, test_installer_requires_only_manager_en…, test_installer_source_has_no_human_or_j…] | lang=en
- "tests_test_main_scripts_completeness_rec": "_rec()" | kind=code-symbol | source=tests/test_main_scripts_completeness.py:L20 | neighbors=[test_main_scripts_completeness.py, test_duplicate_port_is_detected(), test_fallback_count_based_when_no_reque…, test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely…] | lang=en
- "tests_test_main_scripts_coverage_testprofiles": "TestProfiles" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L41 | neighbors=[test_main_scripts_coverage.py, .test_custom_dedups_and_requires_ports(), .test_full_is_entire_tcp_space(), .test_quick_is_small_and_contains_smb(), .test_top1000_covers_windows_ground_tru…, .test_top100_is_100_unique()] | lang=en
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics": "TestWorkerPoolAndMetrics" | kind=code-symbol | source=tests/test_main_scripts_coverage.py:L81 | neighbors=[test_main_scripts_coverage.py, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state()] | lang=en
- "tests_test_main_scripts_rdp_cc": "_cc()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L15 | neighbors=[test_main_scripts_rdp.py, A TPKT + X.224 Connection Confirm, opti…, test_cc_without_negotiation_is_standard…, test_negotiation_failure(), test_nla_when_hybrid_selected(), test_standard_rdp_security_no_nla()] | lang=en
- "tests_test_os_fingerprint_testacceptechoreply": "TestAcceptEchoReply" | kind=code-symbol | source=tests/test_os_fingerprint.py:L169 | neighbors=[test_os_fingerprint.py, ._reply(), .test_accepts_echo_reply_from_target(), .test_accepts_when_source_unknown(), .test_rejects_non_echo_type(), .test_rejects_none_parsed()] | lang=en
- "tests_test_probe_core_testclassifycertainty": "TestClassifyCertainty" | kind=code-symbol | source=tests/test_probe_core.py:L706 | neighbors=[test_probe_core.py, .test_error_overrides(), .test_host_discovery_uncertain(), .test_service_banner_deterministic(), .test_tcp_port_scan_deterministic(), .test_udp_port_scan_uncertain()] | lang=en
- "tests_test_scope_validator": "test_scope_validator.py" | kind=code-symbol | source=tests/test_scope_validator.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, scope_validator.py, TestFetchEngagementScope, TestMergeExclusions, TestTargetsInExcludes, TestValidateTargetsInScope] | lang=en
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=tests/test_scope_validator.py:L144 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()] | lang=en
- "tests_test_tls_fingerprint_testdigest": "TestDigest" | kind=code-symbol | source=tests/test_tls_fingerprint.py:L83 | neighbors=[test_tls_fingerprint.py, .test_cipher_code_known_and_unknown(), .test_digest_differs_with_cipher(), .test_digest_is_62_chars(), .test_digest_is_deterministic(), .test_version_code()] | lang=en
- "tests_test_tls_integration_tlsserver": "_TLSServer" | kind=code-symbol | source=tests/test_tls_integration.py:L50 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade(), .__enter__(), .__exit__(), .__init__()] | lang=en
- "tests_test_transport_testdeviceenrollment": "TestDeviceEnrollment" | kind=code-symbol | source=tests/test_transport.py:L171 | neighbors=[test_transport.py, .test_activation_persists_recoverable_d…, .test_create_enrollment_request_409_rai…, .test_create_enrollment_request_409_wit…, .test_create_enrollment_request_forward…, .test_device_refresh_signs_unique_nonce…] | lang=en
- "tests_test_udp_amplifiers": "test_udp_amplifiers.py" | kind=code-symbol | source=tests/test_udp_amplifiers.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…, udp_scanner.py, test_dns_open_recursion(), test_memcached_exposed(), test_ntp_monlist_absent(), test_ntp_monlist_enabled()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-009.json

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
