# Node Description Batch 265 of 330

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

- "tests_test_accuracy_gate_testshippedcorpora_test_every_shipped_corpus_declares_provenance": ".test_every_shipped_corpus_declares_provenance()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L48 | neighbors=[TestShippedCorpora]
- "tests_test_accuracy_gate_testshippedcorpora_test_report_marks_regression_corpora_as_not_accuracy_evidence": ".test_report_marks_regression_corpora_as_not_accuracy_evidence()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L53 | neighbors=[TestShippedCorpora]
- "tests_test_accuracy_gate_testshippedcorpora_test_unlabeled_findings_dimension_is_marked_in_the_report": ".test_unlabeled_findings_dimension_is_marked_in_the_report()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L77 | neighbors=[TestShippedCorpora]
- "tests_test_accuracy_gate_testthresholds_test_clean_result_produces_no_violations": ".test_clean_result_produces_no_violations()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L178 | neighbors=[TestThresholds]
- "tests_test_accuracy_gate_testthresholds_test_false_positive_finding_trips_precision": ".test_false_positive_finding_trips_precision()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L165 | neighbors=[TestThresholds]
- "tests_test_accuracy_gate_testthresholds_test_missed_open_port_trips_open_recall": ".test_missed_open_port_trips_open_recall()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L157 | neighbors=[TestThresholds]
- "tests_test_accuracy_gate_testthresholds_test_phantom_open_port_trips_open_precision": ".test_phantom_open_port_trips_open_precision()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L149 | neighbors=[TestThresholds]
- "tests_test_accuracy_gate_testthresholds_test_unlabeled_dimension_is_skipped_not_scored_as_perfect": ".test_unlabeled_dimension_is_skipped_not_scored_as_perfect()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L172 | neighbors=[TestThresholds]
- "tests_test_active_validation_interpret_test_confirmed_upgrades_and_sets_exploit_validated": "test_confirmed_upgrades_and_sets_exploit_validated()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L6 | neighbors=[test_active_validation_interpret.py]
- "tests_test_active_validation_interpret_test_contradicted_marks_false_positive": "test_contradicted_marks_false_positive()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L13 | neighbors=[test_active_validation_interpret.py]
- "tests_test_active_validation_interpret_test_inconclusive_keeps_state_unchanged": "test_inconclusive_keeps_state_unchanged()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L20 | neighbors=[test_active_validation_interpret.py]
- "tests_test_active_validation_interpret_test_missing_or_garbage_result_is_inconclusive": "test_missing_or_garbage_result_is_inconclusive()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_interpret.py:L27 | neighbors=[test_active_validation_interpret.py]
- "tests_test_ad_assessment_fakeattr_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L32 | neighbors=[_FakeAttr]
- "tests_test_ad_assessment_fakeentry_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L37 | neighbors=[_FakeEntry]
- "tests_test_ad_assessment_testadcschecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L280 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_negative_when_manager_approval": ".test_esc1_negative_when_manager_approval()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L292 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_negative_without_low_priv_enrollment": ".test_esc1_negative_without_low_priv_enrollment()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L299 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc1_positive": ".test_esc1_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L283 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc4_negative_when_deny_ace": ".test_esc4_negative_when_deny_ace()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L313 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc4_positive": ".test_esc4_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L306 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_negative_no_web_enrollment": ".test_esc8_negative_no_web_enrollment()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L332 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_negative_with_epa_and_https": ".test_esc8_negative_with_epa_and_https()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L326 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_esc8_positive": ".test_esc8_positive()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L320 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testadcschecker_test_generate_findings_produces_esc1_and_esc8": ".test_generate_findings_produces_esc1_and_esc8()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L335 | neighbors=[TestADCSChecker]
- "tests_test_ad_assessment_testasreproastchecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L217 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_finding_shape": ".test_finding_shape()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L229 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_get_no_preauth_accounts": ".test_get_no_preauth_accounts()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L220 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_no_finding_when_empty": ".test_no_finding_when_empty()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L235 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testasreproastchecker_test_request_asrep_without_impacket": ".test_request_asrep_without_impacket()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L238 | neighbors=[TestASREPRoastChecker]
- "tests_test_ad_assessment_testbloodhoundcollector_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L358 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_da_path_finding_critical_when_short": ".test_da_path_finding_critical_when_short()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L361 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_da_path_finding_high_when_long": ".test_da_path_finding_high_when_long()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L368 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_import_without_neo4j": ".test_import_without_neo4j()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L379 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_no_finding_without_paths": ".test_no_finding_without_paths()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L373 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbloodhoundcollector_test_query_da_paths_without_driver": ".test_query_da_paths_without_driver()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L376 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbuildadfinding_test_attack_narrative_carried_in_evidence": ".test_attack_narrative_carried_in_evidence()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L84 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_invalid_severity_falls_back_to_info": ".test_invalid_severity_falls_back_to_info()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L76 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_required_fields_present": ".test_required_fields_present()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L60 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testkerberoastchecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L170 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_finding_critical_when_privileged": ".test_finding_critical_when_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L189 | neighbors=[TestKerberoastChecker]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-264.json

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
