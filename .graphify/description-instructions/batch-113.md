# Node Description Batch 114 of 336

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

- "tests_test_main_scripts_completeness_test_duplicate_port_is_detected": "test_duplicate_port_is_detected()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L39 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_full_scan_is_complete": "test_full_scan_is_complete()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L24 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_missing_port_is_detected": "test_missing_port_is_detected()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L32 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_skip_plus_duplicate_is_not_falsely_complete": "test_skip_plus_duplicate_is_not_falsely_complete()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L46 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_completeness_test_summary_exposes_missing_and_duplicates": "test_summary_exposes_missing_and_duplicates()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L55 | neighbors=[test_main_scripts_completeness.py, _metrics(), _rec()]
- "tests_test_main_scripts_correlation_test_cleartext_cluster_fires_on_two_cleartext_services": "test_cleartext_cluster_fires_on_two_cleartext_services()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L67 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_correlation_does_not_cross_hosts": "test_correlation_does_not_cross_hosts()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L83 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_legacy_windows_surface_smbv1_plus_rdp": "test_legacy_windows_surface_smbv1_plus_rdp()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L49 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_no_legacy_surface_with_only_smbv1": "test_no_legacy_surface_with_only_smbv1()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L60 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_no_relay_finding_when_signing_required": "test_no_relay_finding_when_signing_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L42 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_correlation_test_ntlm_relay_is_high_when_smbv1_also_enabled": "test_ntlm_relay_is_high_when_smbv1_also_enabled()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L34 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_ntlm_relay_is_medium_when_only_signing_not_required": "test_ntlm_relay_is_medium_when_only_signing_not_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L26 | neighbors=[test_main_scripts_correlation.py, _get(), _run()]
- "tests_test_main_scripts_correlation_test_single_cleartext_service_does_not_cluster": "test_single_cleartext_service_does_not_cluster()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L77 | neighbors=[test_main_scripts_correlation.py, _ids(), _run()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_every_port_scanned_exactly_once": ".test_every_port_scanned_exactly_once()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L82 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_local_resource_error_marks_scan_degraded": ".test_local_resource_error_marks_scan_degraded()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L150 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_metrics_counts_every_state": ".test_metrics_counts_every_state()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L136 | neighbors=[TestWorkerPoolAndMetrics, _mk_scanner(), _summary()]
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_open_only_output_still_keeps_full_metrics": ".test_open_only_output_still_keeps_full_metrics()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L165 | neighbors=[TestWorkerPoolAndMetrics, _scope(), _summary()]
- "tests_test_main_scripts_findings_test_all_security_headers_present_no_finding": "test_all_security_headers_present_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L272 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_closed_port_no_finding": "test_closed_port_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L192 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_ntp_monlist_and_dns_open_recursion": "test_ntp_monlist_and_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L150 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_open_filtered_never_raises_exposure": "test_open_filtered_never_raises_exposure()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L185 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_hardened_host_no_finding": "test_smb_hardened_host_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L117 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_signing_not_required_is_medium": "test_smb_signing_not_required_is_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L110 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmp_amplification": "test_snmp_amplification()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L137 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmpv3_only_no_finding": "test_snmpv3_only_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L143 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
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
