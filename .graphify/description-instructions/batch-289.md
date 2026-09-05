# Node Description Batch 290 of 336

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

- "tests_test_job_result_service_test_out_of_scope_result_is_rejected_before_database_mutation": "test_out_of_scope_result_is_rejected_before_database_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L98 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_result_scope_accepts_authorized_targets_and_control_records": "test_result_scope_accepts_authorized_targets_and_control_records()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L13 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_result_scope_fails_closed": "test_result_scope_fails_closed()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L36 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_stale_attempt_gets_terminal_receipt_without_mutation": "test_stale_attempt_gets_terminal_receipt_without_mutation()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L136 | neighbors=[test_job_result_service.py]
- "tests_test_job_result_service_test_terminal_result_retry_is_idempotent": "test_terminal_result_retry_is_idempotent()" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L51 | neighbors=[test_job_result_service.py]
- "tests_test_loaders_rationale_1": "Tests for loader error paths in vuln_db.py and enrichment_db.py.  These are the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L1 | neighbors=[test_loaders.py]
- "tests_test_loaders_rationale_102": "The FileNotFoundError message should mention re-syncing, so         operators kn" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L102 | neighbors=[.test_error_message_mentions_re_sync()]
- "tests_test_loaders_rationale_108": "The ValueError for a hash mismatch must include truncated hashes         in the" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L108 | neighbors=[.test_hash_mismatch_message_truncates_h…]
- "tests_test_loaders_rationale_60": "A path that doesn't exist must raise FileNotFoundError with a         helpful me" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L60 | neighbors=[.test_missing_file_raises_file_not_foun…]
- "tests_test_loaders_rationale_66": "A snapshot whose records don't match the stored content_hash must         raise" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L66 | neighbors=[.test_content_hash_mismatch_raises_valu…]
- "tests_test_loaders_rationale_78": "Completely broken JSON must propagate as an exception — never         silently y" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L78 | neighbors=[.test_malformed_json_raises()]
- "tests_test_loaders_rationale_86": "A JSON file that is valid JSON but missing the 'records' key         must raise" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L86 | neighbors=[.test_missing_required_key_raises()]
- "tests_test_loaders_rationale_94": "A well-formed snapshot must load without error and return a VulnDB         that" | kind=entity | source=manager/detection_engine/tests/test_loaders.py:L94 | neighbors=[.test_valid_snapshot_loads_cleanly()]
- "tests_test_loaders_testloadepsserrors_setup_method": ".setup_method()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L151 | neighbors=[TestLoadEpssErrors]
- "tests_test_loaders_testloadepsserrors_test_malformed_epss_json_raises": ".test_malformed_epss_json_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L158 | neighbors=[TestLoadEpssErrors]
- "tests_test_loaders_testloadepsserrors_test_missing_epss_file_raises": ".test_missing_epss_file_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L154 | neighbors=[TestLoadEpssErrors]
- "tests_test_loaders_testloadkeverrors_setup_method": ".setup_method()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L125 | neighbors=[TestLoadKevErrors]
- "tests_test_loaders_testloadkeverrors_test_malformed_kev_json_raises": ".test_malformed_kev_json_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L132 | neighbors=[TestLoadKevErrors]
- "tests_test_loaders_testloadkeverrors_test_missing_kev_file_raises": ".test_missing_kev_file_raises()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L128 | neighbors=[TestLoadKevErrors]
- "tests_test_loaders_testloadsnapshoterrors_setup_method": ".setup_method()" | kind=code-symbol | source=manager/detection_engine/tests/test_loaders.py:L56 | neighbors=[TestLoadSnapshotErrors]
- "tests_test_main_scripts_accuracy_rationale_1": "test_main_scripts_accuracy.py — Epic 6: the ground-truth accuracy harness.  Scor" | kind=entity | source=probe/tests/test_main_scripts_accuracy.py:L1 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_by_rule_breakdown": "test_by_rule_breakdown()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L37 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_clean_host_has_zero_false_positives": "test_clean_host_has_zero_false_positives()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L103 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_corpus_flags_a_missed_expected_finding": "test_corpus_flags_a_missed_expected_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L91 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_corpus_matches_real_engine_output": "test_corpus_matches_real_engine_output()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L73 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_corpus_scores_port_states_when_ground_truth_given": "test_corpus_scores_port_states_when_ground_truth_given()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L119 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_empty_expected_and_produced_is_perfect": "test_empty_expected_and_produced_is_perfect()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L45 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_false_negative_lowers_recall": "test_false_negative_lowers_recall()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L30 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_false_positive_lowers_precision": "test_false_positive_lowers_precision()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L22 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_open_precision_recall_and_accuracy": "test_open_precision_recall_and_accuracy()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L51 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_perfect_findings_score": "test_perfect_findings_score()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L15 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_accuracy_test_unscanned_open_port_is_false_negative": "test_unscanned_open_port_is_false_negative()" | kind=code-symbol | source=probe/tests/test_main_scripts_accuracy.py:L65 | neighbors=[test_main_scripts_accuracy.py]
- "tests_test_main_scripts_adaptive_timeout_rationale_1": "test_main_scripts_adaptive_timeout.py — Phase 7: per-host adaptive probe timeout" | kind=entity | source=probe/tests/test_main_scripts_adaptive_timeout.py:L1 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_estimate_converges_on_stable_rtt": "test_estimate_converges_on_stable_rtt()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L44 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_fast_lan_gets_short_timeout_slow_wan_gets_long": "test_fast_lan_gets_short_timeout_slow_wan_gets_long()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L25 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_first_sample_sets_srtt_and_timeout": "test_first_sample_sets_srtt_and_timeout()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L18 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_invalid_band_rejected": "test_invalid_band_rejected()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L67 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_narrows_then_widens_after_outlier": "test_narrows_then_widens_after_outlier()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L50 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_no_samples_returns_base": "test_no_samples_returns_base()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L14 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_observe_ignores_bad_samples": "test_observe_ignores_bad_samples()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L38 | neighbors=[test_main_scripts_adaptive_timeout.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-289.json

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
