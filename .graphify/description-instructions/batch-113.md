# Node Description Batch 114 of 332

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

- "tests_test_main_scripts_findings_test_tls_expired_and_self_signed_cert": "test_tls_expired_and_self_signed_cert()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L55 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete": "test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L33 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_modern_only_produces_no_crypto_finding": "test_tls_modern_only_produces_no_crypto_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L41 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_small_ec_key_is_not_treated_as_weak": "test_tls_small_ec_key_is_not_treated_as_weak()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L94 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_strong_rsa_key_is_not_flagged": "test_tls_strong_rsa_key_is_not_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L87 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_strong_signature_hash_is_not_flagged": "test_tls_strong_signature_hash_is_not_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L71 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_udp_no_amplification_when_not_reflecting": "test_udp_no_amplification_when_not_reflecting()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L160 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_hardening_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L36 | neighbors=[test_main_scripts_hardening.py, .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_test_icmp_port_unreachable_is_closed": ".test_icmp_port_unreachable_is_closed()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L60 | neighbors=[TestUdpStateModel, _run(), ._scanner()]
- "tests_test_main_scripts_hardening_testudpstatemodel_test_silence_is_open_filtered_not_filtered": ".test_silence_is_open_filtered_not_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L46 | neighbors=[TestUdpStateModel, _run(), ._scanner()]
- "tests_test_main_scripts_ja4s_serverhello": "_serverhello()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L21 | neighbors=[test_main_scripts_ja4s.py, _ext(), test_ja4s_from_serverhello_tls13()]
- "tests_test_msrpc_scanner_testmsrpcfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L82 | neighbors=[TestMSRPCFindings, .test_endpoints_low(), .test_zero_endpoints_silent()]
- "tests_test_network_va_accuracy_listener_start": ".start()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L35 | neighbors=[_Listener, ._loop(), va_scan()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_new_service": ".test_diff_detects_new_service()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L412 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_service_gone": ".test_diff_detects_service_gone()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L428 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_state_change_to_open": ".test_diff_detects_state_change_to_open()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L444 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_high_severity_port_heuristic": ".test_diff_high_severity_port_heuristic()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L471 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_no_change_produces_no_service_delta": ".test_diff_no_change_produces_no_service_delta()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L457 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_basic": ".test_load_jsonl_basic()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L389 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_error_status": ".test_load_jsonl_skips_error_status()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L397 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_summary_counts": ".test_summary_counts()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L485 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_nfs_scanner_testnfsfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L118 | neighbors=[TestNFSFindings, .test_restricted_exports_no_high_findin…, .test_world_readable_and_portmapper()]
- "tests_test_nfs_scanner_testnfsscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L95 | neighbors=[TestNFSScanner, .test_no_rpc_is_filtered(), .test_world_readable_export_open()]
- "tests_test_nmap_xml_safety": "test_nmap_xml_safety.py" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L1 | neighbors=[37fa611 harden(scanner): XML-entity gua…, TestNmapEntityGuard, test_nmap_xml_safety.py — nmap XML pars…]
- "tests_test_notifications_testnotifytenant": "TestNotifyTenant" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L30 | neighbors=[test_notifications.py, .test_counts_only_successful_channels(), .test_fans_to_enabled_and_decrypts_secr…]
- "tests_test_nuclei_scanner_test_nonzero_exit_retains_and_marks_partial_findings": "test_nonzero_exit_retains_and_marks_partial_findings()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L128 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_run_scan_streams_jsonl_and_separates_timeouts": "test_run_scan_streams_jsonl_and_separates_timeouts()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L67 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_timeout_retains_findings_emitted_before_termination": "test_timeout_retains_findings_emitted_before_termination()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L153 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_online_testclionlineflag_db": "._db()" | kind=code-symbol | source=probe/tests/test_online.py:L189 | neighbors=[TestCliOnlineFlag, .test_no_online_flag_skips_enrichment(), .test_online_flag_invokes_enrichment()]
- "tests_test_online_testclionlineflag_facts": "._facts()" | kind=code-symbol | source=probe/tests/test_online.py:L181 | neighbors=[TestCliOnlineFlag, .test_no_online_flag_skips_enrichment(), .test_online_flag_invokes_enrichment()]
- "tests_test_online_testclionlineflag_test_no_online_flag_skips_enrichment": ".test_no_online_flag_skips_enrichment()" | kind=code-symbol | source=probe/tests/test_online.py:L209 | neighbors=[TestCliOnlineFlag, ._db(), ._facts()]
- "tests_test_online_testclionlineflag_test_online_flag_invokes_enrichment": ".test_online_flag_invokes_enrichment()" | kind=code-symbol | source=probe/tests/test_online.py:L196 | neighbors=[TestCliOnlineFlag, ._db(), ._facts()]
- "tests_test_online_testenrichfindings_test_fail_open_leaves_offline_result_untouched": ".test_fail_open_leaves_offline_result_untouched()" | kind=code-symbol | source=probe/tests/test_online.py:L171 | neighbors=[TestEnrichFindings, _finding(), _get_raising()]
- "tests_test_online_testlookupnvd_test_empty_result_is_none": ".test_empty_result_is_none()" | kind=code-symbol | source=probe/tests/test_online.py:L86 | neighbors=[TestLookupNvd, _get_returning(), _nvd_empty()]
- "tests_test_online_testlookupnvd_test_parses_score_severity_refs": ".test_parses_score_severity_refs()" | kind=code-symbol | source=probe/tests/test_online.py:L78 | neighbors=[TestLookupNvd, _get_returning(), _nvd_bytes()]
- "tests_test_online_testlookupvulners_test_exploit_present_is_true": ".test_exploit_present_is_true()" | kind=code-symbol | source=probe/tests/test_online.py:L104 | neighbors=[TestLookupVulners, _get_returning(), _vulners_bytes()]
- "tests_test_online_testlookupvulners_test_no_exploit_is_false": ".test_no_exploit_is_false()" | kind=code-symbol | source=probe/tests/test_online.py:L108 | neighbors=[TestLookupVulners, _get_returning(), _vulners_bytes()]
- "tests_test_online_vulners_bytes": "_vulners_bytes()" | kind=code-symbol | source=probe/tests/test_online.py:L43 | neighbors=[test_online.py, .test_exploit_present_is_true(), .test_no_exploit_is_false()]
- "tests_test_os_fingerprint_testicmpcapability": "TestIcmpCapability" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L436 | neighbors=[test_os_fingerprint.py, .test_available_when_socket_ok(), .test_unavailable_when_socket_raises()]
- "tests_test_os_fingerprint_testicmptimestamps_ts_reply": "._ts_reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L96 | neighbors=[TestIcmpTimestamps, .test_parse_datagram_delivery_has_no_tt…, .test_parse_extracts_ttl_and_transmit()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-113.json

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
