# Node Description Batch 68 of 186

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

- "tests_test_main_scripts_coverage_testworkerpoolandmetrics_test_open_only_output_still_keeps_full_metrics": ".test_open_only_output_still_keeps_full_metrics()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L165 | neighbors=[TestWorkerPoolAndMetrics, _scope(), _summary()]
- "tests_test_main_scripts_findings_test_all_security_headers_present_no_finding": "test_all_security_headers_present_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L232 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_closed_port_no_finding": "test_closed_port_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L152 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_ntp_monlist_and_dns_open_recursion": "test_ntp_monlist_and_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L110 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_open_filtered_never_raises_exposure": "test_open_filtered_never_raises_exposure()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L145 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_hardened_host_no_finding": "test_smb_hardened_host_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L77 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_smb_signing_not_required_is_medium": "test_smb_signing_not_required_is_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L70 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmp_amplification": "test_snmp_amplification()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L97 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_snmpv3_only_no_finding": "test_snmpv3_only_no_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L103 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_expired_and_self_signed_cert": "test_tls_expired_and_self_signed_cert()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L55 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete": "test_tls_legacy_protocol_is_medium_and_not_double_reported_with_obsolete()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L33 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_tls_modern_only_produces_no_crypto_finding": "test_tls_modern_only_produces_no_crypto_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L41 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_findings_test_udp_no_amplification_when_not_reflecting": "test_udp_no_amplification_when_not_reflecting()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L120 | neighbors=[test_main_scripts_findings.py, _ids(), _run()]
- "tests_test_main_scripts_hardening_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L36 | neighbors=[test_main_scripts_hardening.py, .test_icmp_port_unreachable_is_closed(), .test_silence_is_open_filtered_not_filt…]
- "tests_test_main_scripts_hardening_testudpstatemodel_test_icmp_port_unreachable_is_closed": ".test_icmp_port_unreachable_is_closed()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L60 | neighbors=[TestUdpStateModel, _run(), ._scanner()]
- "tests_test_main_scripts_hardening_testudpstatemodel_test_silence_is_open_filtered_not_filtered": ".test_silence_is_open_filtered_not_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L46 | neighbors=[TestUdpStateModel, _run(), ._scanner()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_new_service": ".test_diff_detects_new_service()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L409 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_service_gone": ".test_diff_detects_service_gone()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L425 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_detects_state_change_to_open": ".test_diff_detects_state_change_to_open()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L441 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_high_severity_port_heuristic": ".test_diff_high_severity_port_heuristic()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L468 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_diff_no_change_produces_no_service_delta": ".test_diff_no_change_produces_no_service_delta()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L454 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_basic": ".test_load_jsonl_basic()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L386 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_error_status": ".test_load_jsonl_skips_error_status()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L394 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_new_scanners_testdeltaengine_test_summary_counts": ".test_summary_counts()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L482 | neighbors=[TestDeltaEngine, _make_scan_record(), ._write_jsonl()]
- "tests_test_nuclei_scanner_test_nonzero_exit_retains_and_marks_partial_findings": "test_nonzero_exit_retains_and_marks_partial_findings()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L128 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_run_scan_streams_jsonl_and_separates_timeouts": "test_run_scan_streams_jsonl_and_separates_timeouts()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L67 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_nuclei_scanner_test_timeout_retains_findings_emitted_before_termination": "test_timeout_retains_findings_emitted_before_termination()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L153 | neighbors=[test_nuclei_scanner.py, FakeProcess, _finding_line()]
- "tests_test_os_fingerprint_testicmpcapability": "TestIcmpCapability" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L157 | neighbors=[test_os_fingerprint.py, .test_available_when_socket_ok(), .test_unavailable_when_socket_raises()]
- "tests_test_os_fingerprint_testinetchecksum": "TestInetChecksum" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L23 | neighbors=[test_os_fingerprint.py, .test_checksum_handles_odd_length(), .test_checksum_verifies_to_zero()]
- "tests_test_outbox_reclaim_test_dead_letter_and_requeue_are_mutually_exclusive": "test_dead_letter_and_requeue_are_mutually_exclusive()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L92 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_dead_letter_stmt_targets_exhausted_stranded_rows": "test_dead_letter_stmt_targets_exhausted_stranded_rows()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L68 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_requeue_stmt_makes_retryable_stranded_rows_due_now": "test_requeue_stmt_makes_retryable_stranded_rows_due_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L81 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_pipeline_testrunpipelinededup": "TestRunPipelineDedup" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L232 | neighbors=[test_pipeline.py, .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_pipeline_testrunpipelineemptyinput": "TestRunPipelineEmptyInput" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L112 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty()]
- "tests_test_pipeline_testrunpipelineexposure": "TestRunPipelineExposure" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L203 | neighbors=[test_pipeline.py, .test_exposure_internet_facing_propagat…, .test_no_exposure_fields_are_none()]
- "tests_test_port_catalog": "test_port_catalog.py" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L1 | neighbors=[cdee859 feat(probe): add container/clou…, test_modern_infra_ports_present(), gates.py]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-067.json

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
