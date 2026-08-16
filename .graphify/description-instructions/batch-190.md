# Node Description Batch 191 of 209

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_probe_next_features_test_light_and_deep_change_port_breadth": "test_light_and_deep_change_port_breadth()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L37 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_scan_types_still_enforce_scope": "test_new_scan_types_still_enforce_scope()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L169 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_use_cases_are_rejected_if_not_in_library": "test_new_use_cases_are_rejected_if_not_in_library()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L183 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_new_use_cases_present_and_capable": "test_new_use_cases_present_and_capable()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L58 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_none_intensity_defaults_to_standard": "test_none_intensity_defaults_to_standard()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L42 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_params_intensity_overrides_and_is_applied": "test_params_intensity_overrides_and_is_applied()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L84 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_scan_method_selection_rule": "test_scan_method_selection_rule()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L191 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_standard_intensity_is_a_noop_baseline": "test_standard_intensity_is_a_noop_baseline()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L29 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_syn_scan_method_routes_through_syn_scanner": "test_syn_scan_method_routes_through_syn_scanner()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L206 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_unknown_intensity_raises": "test_unknown_intensity_raises()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L46 | neighbors=[test_probe_next_features.py]
- "tests_test_probe_next_features_test_unsupported_intensity_is_rejected_before_scanning": "test_unsupported_intensity_is_rejected_before_scanning()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L93 | neighbors=[test_probe_next_features.py]
- "tests_test_resolution_coverage_test_coverage_counts_only_completed_scanner_observations": "test_coverage_counts_only_completed_scanner_observations()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L12 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_coverage_test_coverage_empty_when_no_scanner_runs": "test_coverage_empty_when_no_scanner_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L27 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_coverage_test_host_of_strips_single_port": "test_host_of_strips_single_port()" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L6 | neighbors=[test_resolution_coverage.py]
- "tests_test_resolution_decision_test_db_change_blocks_resolution": "test_db_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L22 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_high_needs_two_covered_clean_runs": "test_high_needs_two_covered_clean_runs()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L36 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_medium_resolves_on_first_covered_clean_run": "test_medium_resolves_on_first_covered_clean_run()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L29 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_not_covered_is_skipped_and_counter_untouched": "test_not_covered_is_skipped_and_counter_untouched()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L15 | neighbors=[test_resolution_decision.py]
- "tests_test_resolution_decision_test_threshold_is_stricter_for_critical_and_high": "test_threshold_is_stricter_for_critical_and_high()" | kind=code-symbol | source=manager/backend/tests/test_resolution_decision.py:L7 | neighbors=[test_resolution_decision.py]
- "tests_test_result_spool_rationale_1": "Tests for agent/result_spool.py" | kind=entity | source=probe/tests/test_result_spool.py:L1 | neighbors=[test_result_spool.py]
- "tests_test_result_spool_rationale_13": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L13 | neighbors=[spool()]
- "tests_test_result_spool_rationale_14": "ResultSpool with tiny retry delay for fast tests." | kind=entity | source=probe/tests/test_result_spool.py:L14 | neighbors=[spool()]
- "tests_test_result_spool_testresultspool_test_byte_high_water_mark_pauses_new_work_without_eviction": ".test_byte_high_water_mark_pauses_new_work_without_eviction()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L194 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_custom_retry_config": ".test_custom_retry_config()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L179 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_exists": ".test_exists()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L64 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_file_high_water_mark_pauses_new_work": ".test_file_high_water_mark_pauses_new_work()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L183 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_quarantines_permanent_rejection": ".test_flush_quarantines_permanent_rejection()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L166 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_empty": ".test_flush_spool_empty()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L135 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_partial": ".test_flush_spool_partial()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L154 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_flush_spool_with_pending": ".test_flush_spool_with_pending()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L139 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_corrupt": ".test_load_corrupt()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L57 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_load_missing": ".test_load_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L53 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_max_retries_uses_class_default": ".test_max_retries_uses_class_default()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L175 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_permanent_rejection_is_quarantined_without_retry": ".test_permanent_rejection_is_quarantined_without_retry()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L121 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_rejects_job_id_path_traversal": ".test_rejects_job_id_path_traversal()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L37 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_rejects_non_positive_capacity": ".test_rejects_non_positive_capacity()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L210 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove": ".test_remove()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L70 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_remove_missing": ".test_remove_missing()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L76 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_and_load": ".test_save_and_load()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L19 | neighbors=[TestResultSpool]
- "tests_test_result_spool_testresultspool_test_save_is_atomic_no_temp_leftover": ".test_save_is_atomic_no_temp_leftover()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L26 | neighbors=[TestResultSpool]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-190.json

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
