# Node Description Batch 113 of 227

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

- "tests_test_manager_ai_test_status_fails_safe_without_cloud_key": "test_status_fails_safe_without_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L283 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manual_reopen": "test_manual_reopen.py" | kind=code-symbol | source=manager/backend/tests/test_manual_reopen.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, test_manual_reopen_restores_open_and_au…]
- "tests_test_nessus_scanner_test_create_scan": "test_create_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L48 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_create_scan_with_credentials": "test_create_scan_with_credentials()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L65 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_launch_scan": "test_launch_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L85 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_completed": "test_poll_status_completed()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L114 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_running": "test_poll_status_running()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L99 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_invalid_json": ".test_load_jsonl_skips_invalid_json()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L499 | neighbors=[TestDeltaEngine, _make_scan_record()]
- "tests_test_nuclei_background_fakesession_begin_nested": ".begin_nested()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L43 | neighbors=[_FakeSession, _NestedTransaction]
- "tests_test_nuclei_background_fakesession_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L40 | neighbors=[_FakeSession, _ScalarResult]
- "tests_test_nuclei_background_sessionfactory_call": ".__call__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L71 | neighbors=[_SessionFactory, _FakeSession]
- "tests_test_nuclei_background_test_fatal_nuclei_error_marks_background_job_failed": "test_fatal_nuclei_error_marks_background_job_failed()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L76 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_background_test_partial_nuclei_run_preserves_findings_and_diagnostics": "test_partial_nuclei_run_preserves_findings_and_diagnostics()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L117 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_scanner_test_nonzero_exit_without_findings_raises_with_stderr": "test_nonzero_exit_without_findings_raises_with_stderr()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L108 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_nuclei_scanner_test_template_initialization_failure_cannot_be_clean_zero": "test_template_initialization_failure_cannot_be_clean_zero()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L177 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_os_fingerprint_testacceptechoreply_test_accepts_echo_reply_from_target": ".test_accepts_echo_reply_from_target()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L173 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_accepts_when_source_unknown": ".test_accepts_when_source_unknown()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L186 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_non_echo_type": ".test_rejects_non_echo_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L180 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_reply_from_a_different_host": ".test_rejects_reply_from_a_different_host()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L176 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testicmpparse_ip_icmp": "._ip_icmp()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L63 | neighbors=[TestIcmpParse, .test_parse_extracts_ttl_and_type()]
- "tests_test_os_fingerprint_testicmpparse_test_parse_extracts_ttl_and_type": ".test_parse_extracts_ttl_and_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L72 | neighbors=[TestIcmpParse, ._ip_icmp()]
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_datagram_delivery_has_no_ttl": ".test_parse_datagram_delivery_has_no_ttl()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L113 | neighbors=[TestIcmpTimestamps, ._ts_reply()]
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_extracts_ttl_and_transmit": ".test_parse_extracts_ttl_and_transmit()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L107 | neighbors=[TestIcmpTimestamps, ._ts_reply()]
- "tests_test_os_fingerprint_testtimestampfallback_test_both_filtered_reports_no_reply": ".test_both_filtered_reports_no_reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L158 | neighbors=[TestTimestampFallback, ._scanner()]
- "tests_test_os_fingerprint_testtimestampfallback_test_timestamp_reply_when_echo_is_filtered": ".test_timestamp_reply_when_echo_is_filtered()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L144 | neighbors=[TestTimestampFallback, ._scanner()]
- "tests_test_outbox_reclaim_test_boundary_at_exactly_the_lease_is_reclaimed": "test_boundary_at_exactly_the_lease_is_reclaimed()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L41 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_outbox_reclaim_test_expired_processing_lock_is_reclaimed": "test_expired_processing_lock_is_reclaimed()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L35 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_outbox_reclaim_test_fresh_processing_lock_is_not_reclaimed": "test_fresh_processing_lock_is_not_reclaimed()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L29 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_outbox_reclaim_test_missing_locked_at_is_not_reclaimed": "test_missing_locked_at_is_not_reclaimed()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L55 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_outbox_reclaim_test_pending_and_done_rows_are_never_reclaimed": "test_pending_and_done_rows_are_never_reclaimed()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L47 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_outbox_reclaim_test_reclaim_handles_none_rowcount_from_driver": "test_reclaim_handles_none_rowcount_from_driver()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L136 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_reclaim_is_noop_when_nothing_is_stranded": "test_reclaim_is_noop_when_nothing_is_stranded()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L127 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_reclaim_runs_both_sweeps_commits_and_sums_rowcounts": "test_reclaim_runs_both_sweeps_commits_and_sums_rowcounts()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L115 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_stale_cutoff_is_now_minus_lease": "test_stale_cutoff_is_now_minus_lease()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L60 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_passive_collector_socket_close": ".close()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L31 | neighbors=[_Socket, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_passive_collector_test_collector_raises_when_no_listener_binds": "test_collector_raises_when_no_listener_binds()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L165 | neighbors=[test_passive_collector.py, _Writer]
- "tests_test_perf_optimization_clean_guard_cache": "clean_guard_cache()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L49 | neighbors=[test_perf_optimization.py, Isolate the guard's in-memory + on-disk…]
- "tests_test_perf_optimization_test_clear_caches_forces_reload": "test_clear_caches_forces_reload()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L133 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_perf_optimization_test_dpkg_compare_does_not_call_the_binary": "test_dpkg_compare_does_not_call_the_binary()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L26 | neighbors=[test_perf_optimization.py, dpkg_compare must use the pure-Python c…]
- "tests_test_perf_optimization_test_guard_is_noop_without_dpkg": "test_guard_is_noop_without_dpkg()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L57 | neighbors=[test_perf_optimization.py, No dpkg binary → nothing to cross-check…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-112.json

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
