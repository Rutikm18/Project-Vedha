# Node Description Batch 181 of 209

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
- "tests_test_main_scripts_adaptive_timeout_test_invalid_band_rejected": "test_invalid_band_rejected()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L50 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_no_samples_returns_base": "test_no_samples_returns_base()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L14 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_observe_ignores_bad_samples": "test_observe_ignores_bad_samples()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L38 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_timeout_is_clamped_to_max": "test_timeout_is_clamped_to_max()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L33 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_completeness_rationale_1": "test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian" | kind=entity | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[test_main_scripts_completeness.py]
- "tests_test_main_scripts_correlation_rationale_1": "test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig" | kind=entity | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[test_main_scripts_correlation.py]
- "tests_test_main_scripts_coverage_closed": "_closed()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L76 | neighbors=[test_main_scripts_coverage.py]
- "tests_test_main_scripts_coverage_rationale_1": "test_main_scripts_coverage.py — P0 coverage + self-health capabilities added to" | kind=entity | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[test_main_scripts_coverage.py]
- "tests_test_main_scripts_coverage_testprofiles_test_custom_dedups_and_requires_ports": ".test_custom_dedups_and_requires_ports()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L64 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_full_is_entire_tcp_space": ".test_full_is_entire_tcp_space()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L42 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_quick_is_small_and_contains_smb": ".test_quick_is_small_and_contains_smb()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L54 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_top100_is_100_unique": ".test_top100_is_100_unique()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L49 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_top1000_covers_windows_ground_truth_extras": ".test_top1000_covers_windows_ground_truth_extras()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L58 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_unknown_profile_raises": ".test_unknown_profile_raises()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L69 | neighbors=[TestProfiles]
- "tests_test_main_scripts_datastore_probe_rationale_1": "test_main_scripts_datastore_probe.py — safe read-only datastore probes make the" | kind=entity | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_datastore_probe_test_ladder_includes_safe_datastore_probes": "test_ladder_includes_safe_datastore_probes()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L40 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_datastore_probe_test_memcached_probe_response_yields_unauth_finding": "test_memcached_probe_response_yields_unauth_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L51 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_device_rationale_1": "test_main_scripts_device.py — device-role classification (P0 \"Device classificat" | kind=entity | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[test_main_scripts_device.py]
- "tests_test_main_scripts_device_testclassifydevice_test_domain_controller": ".test_domain_controller()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L25 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_iot_camera": ".test_iot_camera()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L48 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_network_device_router": ".test_network_device_router()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L37 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_printer": ".test_printer()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L31 | neighbors=[TestClassifyDevice]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-180.json

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
