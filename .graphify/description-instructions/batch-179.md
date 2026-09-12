# Node Description Batch 180 of 380

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
- "tests_test_perf_optimization_test_guard_reports_divergence_and_warns": "test_guard_reports_divergence_and_warns()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L75 | neighbors=[test_perf_optimization.py, When the binary disagrees with pure-Pyt…]
- "tests_test_perf_optimization_test_load_snapshot_memoized_returns_same_instance": "test_load_snapshot_memoized_returns_same_instance()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L114 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_perf_optimization_test_load_snapshot_reloads_after_file_change": "test_load_snapshot_reloads_after_file_change()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L121 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_perf_optimization_test_load_snapshot_runs_dpkg_guard_once_keyed_by_content_hash": "test_load_snapshot_runs_dpkg_guard_once_keyed_by_content_hash()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L154 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_pipeline_concurrency_test_detection_locks_the_engagement_before_reading_anything": "test_detection_locks_the_engagement_before_reading_anything()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L30 | neighbors=[test_pipeline_concurrency.py, The lock must be taken BEFORE the first…]
- "tests_test_pipeline_concurrency_test_different_engagements_generally_do_not_contend": "test_different_engagements_generally_do_not_contend()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L70 | neighbors=[test_pipeline_concurrency.py, Collisions are harmless (two unrelated …]
- "tests_test_pipeline_concurrency_test_the_key_fits_a_postgres_bigint": "test_the_key_fits_a_postgres_bigint()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L82 | neighbors=[test_pipeline_concurrency.py, pg_advisory_xact_lock takes a signed bi…]
- "tests_test_pipeline_concurrency_test_the_lock_is_transaction_scoped_not_session_scoped": "test_the_lock_is_transaction_scoped_not_session_scoped()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L44 | neighbors=[test_pipeline_concurrency.py, pg_advisory_lock (session) would leak o…]
- "tests_test_pipeline_concurrency_test_the_same_engagement_always_maps_to_the_same_key": "test_the_same_engagement_always_maps_to_the_same_key()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L57 | neighbors=[test_pipeline_concurrency.py, Two concurrent handlers must contend, s…]
- "tests_test_pipeline_empty_jsonl": "_empty_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L119 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings()]
- "tests_test_pipeline_testrunpipelinereturnvalue": "TestRunPipelineReturnValue" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L306 | neighbors=[test_pipeline.py, .test_returns_tuple_of_findings_and_ing…]
- "tests_test_portal_assistant_test_a_non_client_user_is_refused": "test_a_non_client_user_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L158 | neighbors=[test_portal_assistant.py, _ask()]
- "tests_test_portal_assistant_test_request_body_cannot_carry_context": "test_request_body_cannot_carry_context()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L113 | neighbors=[test_portal_assistant.py, The schema has no context field, so a c…]
- "tests_test_portal_finding_actions_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L43 | neighbors=[test_portal_finding_actions.py, test_customer_transition_mutates_shared…]
- "tests_test_portal_finding_actions_test_customer_cannot_mutate_a_finding_outside_bound_engagement": "test_customer_cannot_mutate_a_finding_outside_bound_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L100 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_portal_assets_use_session_engagement": "test_portal_assets_use_session_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L184 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_portal_engagement_update_pins_session_identity": "test_portal_engagement_update_pins_session_identity()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L160 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_portal_enrollment_binds_device_to_session_engagement_scope": "test_portal_enrollment_binds_device_to_session_engagement_scope()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L256 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_portal_probe_history_is_filtered_by_engagement": "test_portal_probe_history_is_filtered_by_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L235 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_portal_scan_launch_pins_session_engagement_and_assigned_probe": "test_portal_scan_launch_pins_session_engagement_and_assigned_probe()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L202 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_workspace_engagement_uses_session_binding": "test_workspace_engagement_uses_session_binding()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L142 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_finding_actions_test_workspace_queries_pin_engagement_and_forward_agent_filter": "test_workspace_queries_pin_engagement_and_forward_agent_filter()" | kind=code-symbol | source=manager/backend/tests/test_portal_finding_actions.py:L118 | neighbors=[test_portal_finding_actions.py, _client()]
- "tests_test_portal_metrics_testopenclosed": "TestOpenClosed" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L34 | neighbors=[test_portal_metrics.py, .test_counts_by_status_and_resolved_at()]
- "tests_test_portal_metrics_testopenclosed_test_counts_by_status_and_resolved_at": ".test_counts_by_status_and_resolved_at()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L35 | neighbors=[TestOpenClosed, _f()]
- "tests_test_portal_metrics_testseveritybreakdown_test_open_only_excludes_closed": ".test_open_only_excludes_closed()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L24 | neighbors=[TestSeverityBreakdown, _f()]
- "tests_test_portal_metrics_testseveritybreakdown_test_unknown_severity_falls_into_info": ".test_unknown_severity_falls_into_info()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L30 | neighbors=[TestSeverityBreakdown, _f()]
- "tests_test_portal_metrics_teststatustimeline_test_activity_outside_window_is_ignored": ".test_activity_outside_window_is_ignored()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L60 | neighbors=[TestStatusTimeline, _f()]
- "tests_test_portal_metrics_teststatustimeline_test_buckets_opened_and_closed": ".test_buckets_opened_and_closed()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L49 | neighbors=[TestStatusTimeline, _f()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-179.json

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
