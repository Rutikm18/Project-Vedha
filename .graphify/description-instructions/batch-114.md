# Node Description Batch 115 of 336

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
- "tests_test_os_fingerprint_testinetchecksum": "TestInetChecksum" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L24 | neighbors=[test_os_fingerprint.py, .test_checksum_handles_odd_length(), .test_checksum_verifies_to_zero()]
- "tests_test_os_fingerprint_testremoteclock": "TestRemoteClock" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L123 | neighbors=[test_os_fingerprint.py, .test_high_bit_marks_nonstandard_clock(), .test_standard_value_decodes_to_wall_cl…]
- "tests_test_os_fingerprint_testtimestampfallback_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L139 | neighbors=[TestTimestampFallback, .test_both_filtered_reports_no_reply(), .test_timestamp_reply_when_echo_is_filt…]
- "tests_test_outbox_reclaim_test_dead_letter_and_requeue_are_mutually_exclusive": "test_dead_letter_and_requeue_are_mutually_exclusive()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L92 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_dead_letter_stmt_targets_exhausted_stranded_rows": "test_dead_letter_stmt_targets_exhausted_stranded_rows()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L68 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_outbox_reclaim_test_requeue_stmt_makes_retryable_stranded_rows_due_now": "test_requeue_stmt_makes_retryable_stranded_rows_due_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L81 | neighbors=[test_outbox_reclaim.py, _now(), _sql()]
- "tests_test_passive_collector_test_ot_udp_backend_never_joins_or_transmits": "test_ot_udp_backend_never_joins_or_transmits()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L74 | neighbors=[test_passive_collector.py, .close(), _Writer]
- "tests_test_passive_collector_test_subset_listener_failure_reports_degraded_coverage": "test_subset_listener_failure_reports_degraded_coverage()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L35 | neighbors=[test_passive_collector.py, _Socket, _Writer]
- "tests_test_pipeline_banner_jsonl": "_banner_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L105 | neighbors=[test_pipeline.py, .test_banner_finding_is_suspected_not_c…, .test_full_detection_exposes_authoritat…]
- "tests_test_pipeline_concurrency_test_a_redelivered_submission_is_not_detected_twice": "test_a_redelivered_submission_is_not_detected_twice()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L111 | neighbors=[test_pipeline_concurrency.py, _db_with(), _event()]
- "tests_test_pipeline_testrunpipelinededup": "TestRunPipelineDedup" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L276 | neighbors=[test_pipeline.py, .test_findings_deduped_within_same_host…, .test_two_identical_hosts_each_get_thei…]
- "tests_test_pipeline_testrunpipelineemptyinput": "TestRunPipelineEmptyInput" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L129 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings(), .test_no_paths_returns_empty()]
- "tests_test_pipeline_testrunpipelineexposure": "TestRunPipelineExposure" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L247 | neighbors=[test_pipeline.py, .test_exposure_internet_facing_propagat…, .test_no_exposure_fields_are_none()]
- "tests_test_port_catalog": "test_port_catalog.py" | kind=code-symbol | source=probe/tests/test_port_catalog.py:L1 | neighbors=[cdee859 feat(probe): add container/clou…, test_modern_infra_ports_present(), gates.py]
- "tests_test_portal_read_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L180 | neighbors=[test_portal_read.py, .test_aggregates_posture_counts_and_que…, .test_returns_severity_and_timeline()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-114.json

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
