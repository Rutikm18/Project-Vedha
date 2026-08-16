# Node Description Batch 105 of 209

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

- "tests_test_main_scripts_unauth_test_unauth_elasticsearch_is_high": "test_unauth_elasticsearch_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L63 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_unauth_test_unauth_redis_is_critical_and_rce_flagged": "test_unauth_redis_is_critical_and_rce_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L55 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_ambiguous_when_only_open_filtered": ".test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L44 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_auto_detects_external_by_name": ".test_auto_detects_external_by_name()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L63 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_explicit_external_vantage_by_name_override": ".test_explicit_external_vantage_by_name_override()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L56 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_external_exposure_is_flagged": ".test_external_exposure_is_flagged()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L17 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_internal_only_not_called_external": ".test_internal_only_not_called_external()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L26 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_not_exposed_everywhere": ".test_not_exposed_everywhere()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L39 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_vantages_are_not_collapsed": ".test_vantages_are_not_collapsed()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L49 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_manager_ai_test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter": "test_default_auto_detect_prefers_openai_then_anthropic_then_openrouter()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L247 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_auto_detects_the_configured_cloud_provider": "test_default_auto_detects_the_configured_cloud_provider()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L240 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_default_runtime_fails_closed_without_any_cloud_key": "test_default_runtime_fails_closed_without_any_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L254 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_fallback_never_includes_local_ollama": "test_fallback_never_includes_local_ollama()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L271 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_generate_fails_closed_when_no_cloud_provider_configured": "test_generate_fails_closed_when_no_cloud_provider_configured()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L262 | neighbors=[test_manager_ai.py, _cloud()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
