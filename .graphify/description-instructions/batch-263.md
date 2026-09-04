# Node Description Batch 264 of 330

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

- "supporting_research_evidence_store_rationale_382": "Audit-grade: what did the evidence support on a specific date?" | kind=entity | source=Supporting_research/evidence_store.py:L382 | neighbors=[time_travel()]
- "supporting_research_evidence_store_rationale_391": "(observed_at, answer) transitions -- the real remediation-verification signal." | kind=entity | source=Supporting_research/evidence_store.py:L391 | neighbors=[exposure_timeline()]
- "supporting_research_evidence_store_rule": "Rule" | kind=code-symbol | source=Supporting_research/evidence_store.py:L271 | neighbors=[evidence_store.py]
- "supporting_research_evidence_store_unionfind_init": ".__init__()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L147 | neighbors=[_UnionFind]
- "supporting_research_evidence_store_utcnow": "utcnow()" | kind=code-symbol | source=Supporting_research/evidence_store.py:L81 | neighbors=[evidence_store.py]
- "supporting_research_test_evidence_store_rationale_1": "Tests for the evidence store, and a demo that puts numbers on the strategic clai" | kind=entity | source=Supporting_research/test_evidence_store.py:L1 | neighbors=[test_evidence_store.py]
- "supporting_research_test_evidence_store_rationale_105": "Not merely coarse -- wrong. It splits one machine and merges two." | kind=entity | source=Supporting_research/test_evidence_store.py:L105 | neighbors=[.test_ip_identity_is_wrong_in_both_dire…]
- "supporting_research_test_evidence_store_rationale_146": "No rescan. The whole point." | kind=entity | source=Supporting_research/test_evidence_store.py:L146 | neighbors=[.test_a_brand_new_rule_answers_against_…]
- "supporting_research_test_evidence_store_rationale_169": "Regression guard. An OR over history means a patched host stays vulnerable" | kind=entity | source=Supporting_research/test_evidence_store.py:L169 | neighbors=[.test_current_state_comes_from_latest_e…]
- "supporting_research_test_evidence_store_rationale_195": "Drifted payload: the probe ran, the field moved." | kind=entity | source=Supporting_research/test_evidence_store.py:L195 | neighbors=[.test_collected_but_unusable_evidence_i…]
- "supporting_research_test_evidence_store_rationale_73": "30 days of history. HOST_A is patched on day 10." | kind=entity | source=Supporting_research/test_evidence_store.py:L73 | neighbors=[build_fleet()]
- "supporting_research_test_evidence_store_testidentity_test_fingerprint_identity_finds_exactly_three_machines": ".test_fingerprint_identity_finds_exactly_three_machines()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L100 | neighbors=[TestIdentity]
- "supporting_research_test_evidence_store_testidentity_test_observations_without_any_fingerprint_fall_back_to_hostname": ".test_observations_without_any_fingerprint_fall_back_to_hostname()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L127 | neighbors=[TestIdentity]
- "supporting_research_test_evidence_store_testretroactivedetection_test_cannot_answer_is_reported_rather_than_assumed_clean": ".test_cannot_answer_is_reported_rather_than_assumed_clean()" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L178 | neighbors=[TestRetroactiveDetection]
- "test_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/integrations/test/route.ts:L9 | neighbors=[route.ts]
- "tests_assistant_test_cansubmit": "canSubmit()" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L108 | neighbors=[assistant.test.ts]
- "tests_assistant_test_sendbtnlabel": "sendBtnLabel()" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L112 | neighbors=[assistant.test.ts]
- "tests_assistant_test_textareaplaceholder": "textareaPlaceholder()" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L116 | neighbors=[assistant.test.ts]
- "tests_campaign_store_test_makesnapshot": "makeSnapshot()" | kind=code-symbol | source=manager/frontend/tests/campaign-store.test.ts:L18 | neighbors=[campaign-store.test.ts]
- "tests_campaign_store_test_tmp_dir": "TMP_DIR" | kind=code-symbol | source=manager/frontend/tests/campaign-store.test.ts:L8 | neighbors=[campaign-store.test.ts]
- "tests_conftest_pytest_configure": "pytest_configure()" | kind=code-symbol | source=probe/tests/conftest.py:L25 | neighbors=[conftest.py]
- "tests_conftest_rationale_11": "Keep the local result archive out of the checkout.      TaskRunner writes every" | kind=entity | source=probe/tests/conftest.py:L11 | neighbors=[_isolate_result_archive()]
- "tests_findings_detail_layout_test_findingspage": "findingsPage" | kind=code-symbol | source=manager/frontend/tests/findings-detail-layout.test.ts:L5 | neighbors=[findings-detail-layout.test.ts]
- "tests_findings_store_test_makefinding": "makeFinding()" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L25 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_dir": "TMP_DIR" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L8 | neighbors=[findings-store.test.ts]
- "tests_findings_store_test_tmp_file": "TMP_FILE" | kind=code-symbol | source=manager/frontend/tests/findings-store.test.ts:L9 | neighbors=[findings-store.test.ts]
- "tests_parsers_test_naabu_line": "NAABU_LINE" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L81 | neighbors=[parsers.test.ts]
- "tests_parsers_test_nuclei_valid": "NUCLEI_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L56 | neighbors=[parsers.test.ts]
- "tests_parsers_test_testssl_valid": "TESTSSL_VALID" | kind=code-symbol | source=manager/frontend/tests/parsers.test.ts:L73 | neighbors=[parsers.test.ts]
- "tests_test_accuracy_gate_rationale_1": "test_accuracy_gate.py — the accuracy MERGE GATE (roadmap #4 / Tier 1.3).  `accur" | kind=entity | source=probe/tests/test_accuracy_gate.py:L1 | neighbors=[test_accuracy_gate.py]
- "tests_test_accuracy_gate_rationale_44": "CI's actual assertion: the engine still matches every labeled corpus." | kind=entity | source=probe/tests/test_accuracy_gate.py:L44 | neighbors=[.test_gate_passes_on_the_committed_corp…]
- "tests_test_accuracy_gate_rationale_58": "Without one of these the gate proves only non-drift, never accuracy." | kind=entity | source=probe/tests/test_accuracy_gate.py:L58 | neighbors=[.test_an_independently_labeled_corpus_i…]
- "tests_test_accuracy_gate_rationale_64": "Locks in the measured results: every port state agrees with nmap on         both" | kind=entity | source=probe/tests/test_accuracy_gate.py:L64 | neighbors=[.test_every_independent_corpus_scores_p…]
- "tests_test_accuracy_gate_testcli_test_cli_exits_two_on_a_corpus_error": ".test_cli_exits_two_on_a_corpus_error()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L209 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcli_test_cli_exits_zero_on_passing_corpora": ".test_cli_exits_zero_on_passing_corpora()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L206 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcli_test_cli_json_mode_is_machine_readable": ".test_cli_json_mode_is_machine_readable()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L212 | neighbors=[TestCli]
- "tests_test_accuracy_gate_testcorpusvalidation_test_malformed_json_is_a_gate_error_not_a_crash": ".test_malformed_json_is_a_gate_error_not_a_crash()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L113 | neighbors=[TestCorpusValidation]
- "tests_test_accuracy_gate_testcorpusvalidation_test_missing_directory_is_rejected": ".test_missing_directory_is_rejected()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L118 | neighbors=[TestCorpusValidation]
- "tests_test_accuracy_gate_testprovenance_test_nmap_labels_count_as_accuracy_evidence": ".test_nmap_labels_count_as_accuracy_evidence()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L130 | neighbors=[TestProvenance]
- "tests_test_accuracy_gate_testprovenance_test_self_regression_labels_do_not": ".test_self_regression_labels_do_not()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L133 | neighbors=[TestProvenance]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-263.json

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
