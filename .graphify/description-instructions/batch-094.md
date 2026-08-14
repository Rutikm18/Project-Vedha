# Node Description Batch 95 of 186

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

- "tests_test_nuclei_background_fakesession_begin_nested": ".begin_nested()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L43 | neighbors=[_FakeSession, _NestedTransaction]
- "tests_test_nuclei_background_fakesession_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L40 | neighbors=[_FakeSession, _ScalarResult]
- "tests_test_nuclei_background_sessionfactory_call": ".__call__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L71 | neighbors=[_SessionFactory, _FakeSession]
- "tests_test_nuclei_background_test_fatal_nuclei_error_marks_background_job_failed": "test_fatal_nuclei_error_marks_background_job_failed()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L76 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_background_test_partial_nuclei_run_preserves_findings_and_diagnostics": "test_partial_nuclei_run_preserves_findings_and_diagnostics()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L117 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_scanner_test_nonzero_exit_without_findings_raises_with_stderr": "test_nonzero_exit_without_findings_raises_with_stderr()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L108 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_nuclei_scanner_test_template_initialization_failure_cannot_be_clean_zero": "test_template_initialization_failure_cannot_be_clean_zero()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L177 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_os_fingerprint_testicmpparse_ip_icmp": "._ip_icmp()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L62 | neighbors=[TestIcmpParse, .test_parse_extracts_ttl_and_type()]
- "tests_test_os_fingerprint_testicmpparse_test_parse_extracts_ttl_and_type": ".test_parse_extracts_ttl_and_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L71 | neighbors=[TestIcmpParse, ._ip_icmp()]
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
- "tests_test_pipeline_banner_jsonl": "_banner_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L88 | neighbors=[test_pipeline.py, .test_banner_finding_is_suspected_not_c…]
- "tests_test_pipeline_empty_jsonl": "_empty_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L102 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings()]
- "tests_test_pipeline_testrunpipelinereturnvalue": "TestRunPipelineReturnValue" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L262 | neighbors=[test_pipeline.py, .test_returns_tuple_of_findings_and_ing…]
- "tests_test_posture_test_build_posture_buckets_resolved_new_persisting": "test_build_posture_buckets_resolved_new_persisting()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L89 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_build_posture_single_run_has_no_prev": "test_build_posture_single_run_has_no_prev()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L76 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_compute_scores_uses_risk_epss_exploit_and_asset_criticality": "test_compute_scores_uses_risk_epss_exploit_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L53 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_finding_views_handles_null_asset_and_scores": "test_finding_views_handles_null_asset_and_scores()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L128 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_test_finding_views_maps_columns_and_asset_criticality": "test_finding_views_maps_columns_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L114 | neighbors=[test_posture.py, _Row]
- "tests_test_probe_core_testassetmergepassivecollect": "TestAssetMergePassiveCollect" | kind=code-symbol | source=probe/tests/test_probe_core.py:L583 | neighbors=[test_probe_core.py, .test_passive_facts_appended()]
- "tests_test_probe_core_testassetmergeservicebanner": "TestAssetMergeServiceBanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L534 | neighbors=[test_probe_core.py, .test_banner_stored()]
- "tests_test_probe_core_testassetmergesmbscan": "TestAssetMergeSmbScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L559 | neighbors=[test_probe_core.py, .test_smb_state_host_level()]
- "tests_test_probe_core_testassetmergetlsscan": "TestAssetMergeTlsScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L543 | neighbors=[test_probe_core.py, .test_tls_facts_stored()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-094.json

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
