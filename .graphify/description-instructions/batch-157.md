# Node Description Batch 158 of 332

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

- "tests_test_os_fusion_test_build_only_is_strong_but_not_certain": "test_build_only_is_strong_but_not_certain()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L29 | neighbors=[test_os_fusion.py, _os()]
- "tests_test_os_fusion_test_build_smb2_hostname_is_high_confidence": "test_build_smb2_hostname_is_high_confidence()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L17 | neighbors=[test_os_fusion.py, _os()]
- "tests_test_os_fusion_test_no_os_signal_yields_no_finding": "test_no_os_signal_yields_no_finding()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L51 | neighbors=[test_os_fusion.py, _os()]
- "tests_test_os_fusion_test_smb2_plus_p0f_stack_is_medium": "test_smb2_plus_p0f_stack_is_medium()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L42 | neighbors=[test_os_fusion.py, _os()]
- "tests_test_os_fusion_test_ttl_only_stays_a_hint": "test_ttl_only_stays_a_hint()" | kind=code-symbol | source=probe/tests/test_os_fusion.py:L35 | neighbors=[test_os_fusion.py, _os()]
- "tests_test_os_stage_wiring_test_cached_os_fact_is_reused_not_reprobed": "test_cached_os_fact_is_reused_not_reprobed()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L223 | neighbors=[test_os_stage_wiring.py, _wire()]
- "tests_test_os_stage_wiring_test_os_stage_runs_for_a_port_stage_job": "test_os_stage_runs_for_a_port_stage_job()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L138 | neighbors=[test_os_stage_wiring.py, _wire()]
- "tests_test_os_stage_wiring_test_rescan_mode_reprobes_a_stale_os_fact": "test_rescan_mode_reprobes_a_stale_os_fact()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L238 | neighbors=[test_os_stage_wiring.py, _wire()]
- "tests_test_os_stage_wiring_test_stack_hints_from_syn_scan_reach_the_os_scanner": "test_stack_hints_from_syn_scan_reach_the_os_scanner()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L157 | neighbors=[test_os_stage_wiring.py, _wire()]
- "tests_test_os_stage_wiring_testassetmerge_test_closed_port_contributes_no_hints": ".test_closed_port_contributes_no_hints()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L93 | neighbors=[TestAssetMerge, _asset()]
- "tests_test_os_stage_wiring_testassetmerge_test_connect_scan_without_stack_signals_leaves_hints_empty": ".test_connect_scan_without_stack_signals_leaves_hints_empty()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L87 | neighbors=[TestAssetMerge, _asset()]
- "tests_test_os_stage_wiring_testassetmerge_test_os_fact_stored_and_ntlm_name_becomes_alias": ".test_os_fact_stored_and_ntlm_name_becomes_alias()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L99 | neighbors=[TestAssetMerge, _asset()]
- "tests_test_os_stage_wiring_testassetmerge_test_syn_stack_hints_harvested_from_open_port": ".test_syn_stack_hints_harvested_from_open_port()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L78 | neighbors=[TestAssetMerge, _asset()]
- "tests_test_os_stage_wiring_testgate_test_alive_host_is_eligible": ".test_alive_host_is_eligible()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L37 | neighbors=[TestGate, _asset()]
- "tests_test_os_stage_wiring_testgate_test_dead_host_is_not": ".test_dead_host_is_not()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L40 | neighbors=[TestGate, _asset()]
- "tests_test_os_stage_wiring_testgate_test_no_open_ports_still_eligible": ".test_no_open_ports_still_eligible()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L47 | neighbors=[TestGate, _asset()]
- "tests_test_os_stage_wiring_testgate_test_passive_profile_never_probes": ".test_passive_profile_never_probes()" | kind=code-symbol | source=probe/tests/test_os_stage_wiring.py:L43 | neighbors=[TestGate, _asset()]
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
- "tests_test_perf_optimization_test_guard_reports_divergence_and_warns": "test_guard_reports_divergence_and_warns()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L75 | neighbors=[test_perf_optimization.py, When the binary disagrees with pure-Pyt…]
- "tests_test_perf_optimization_test_load_snapshot_memoized_returns_same_instance": "test_load_snapshot_memoized_returns_same_instance()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L114 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_perf_optimization_test_load_snapshot_reloads_after_file_change": "test_load_snapshot_reloads_after_file_change()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L121 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_perf_optimization_test_load_snapshot_runs_dpkg_guard_once_keyed_by_content_hash": "test_load_snapshot_runs_dpkg_guard_once_keyed_by_content_hash()" | kind=code-symbol | source=manager/detection_engine/tests/test_perf_optimization.py:L154 | neighbors=[test_perf_optimization.py, _write_snapshot()]
- "tests_test_pipeline_concurrency_test_detection_locks_the_engagement_before_reading_anything": "test_detection_locks_the_engagement_before_reading_anything()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L30 | neighbors=[test_pipeline_concurrency.py, The lock must be taken BEFORE the first…]
- "tests_test_pipeline_concurrency_test_different_engagements_generally_do_not_contend": "test_different_engagements_generally_do_not_contend()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L70 | neighbors=[test_pipeline_concurrency.py, Collisions are harmless (two unrelated …]
- "tests_test_pipeline_concurrency_test_the_key_fits_a_postgres_bigint": "test_the_key_fits_a_postgres_bigint()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L82 | neighbors=[test_pipeline_concurrency.py, pg_advisory_xact_lock takes a signed bi…]
- "tests_test_pipeline_concurrency_test_the_lock_is_transaction_scoped_not_session_scoped": "test_the_lock_is_transaction_scoped_not_session_scoped()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L44 | neighbors=[test_pipeline_concurrency.py, pg_advisory_lock (session) would leak o…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-157.json

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
