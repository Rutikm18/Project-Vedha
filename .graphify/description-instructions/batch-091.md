# Node Description Batch 92 of 104

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

- "tests_test_detection_core_testmakefindingid_test_length_16": ".test_length_16()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L109 | neighbors=[TestMakeFindingId]
- "tests_test_detection_core_testproductfromcpe_test_extracts_product": ".test_extracts_product()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L553 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testproductfromcpe_test_short_cpe_returns_cpe": ".test_short_cpe_returns_cpe()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L556 | neighbors=[TestProductFromCpe]
- "tests_test_detection_core_testversioninranges_test_empty_ranges": ".test_empty_ranges()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L373 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_ignores_unknown_type": ".test_ignores_unknown_type()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L351 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_introduced_fixed": ".test_introduced_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L313 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_last_affected": ".test_last_affected()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L335 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_no_match_returns_false_none": ".test_no_match_returns_false_none()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L365 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_regression_sequence": ".test_regression_sequence()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L378 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_semver_type_included": ".test_semver_type_included()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L358 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_unbounded_introduced": ".test_unbounded_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L343 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_at_fixed": ".test_version_at_fixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L328 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testversioninranges_test_version_before_introduced": ".test_version_before_introduced()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L321 | neighbors=[TestVersionInRanges]
- "tests_test_detection_core_testvulndb_test_content_hash_deterministic": ".test_content_hash_deterministic()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L898 | neighbors=[TestVulnDB]
- "tests_test_detection_core_testwilsonci_test_all_appearances": ".test_all_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1017 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_perfect_appearance": ".test_perfect_appearance()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1009 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_zero_appearances": ".test_zero_appearances()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1013 | neighbors=[TestWilsonCi]
- "tests_test_detection_core_testwilsonci_test_zero_n": ".test_zero_n()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L1021 | neighbors=[TestWilsonCi]
- "tests_test_detection_validation_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L312 | neighbors=[test_detection_validation.py]
- "tests_test_detection_validation_testdetectioncorrelator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L51 | neighbors=[TestDetectionCorrelator]
- "tests_test_detection_validation_testdetectioncorrelator_test_coverage_empty": ".test_coverage_empty()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L121 | neighbors=[TestDetectionCorrelator]
- "tests_test_detection_validation_testdetectioncorrelator_test_naive_timestamp_does_not_crash": ".test_naive_timestamp_does_not_crash()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L98 | neighbors=[TestDetectionCorrelator]
- "tests_test_detection_validation_testedrparsing_test_crowdstrike_parse": ".test_crowdstrike_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L243 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_defender_parse_and_host_filter": ".test_defender_parse_and_host_filter()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L257 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L285 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testedrparsing_test_sentinelone_parse": ".test_sentinelone_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L273 | neighbors=[TestEDRParsing]
- "tests_test_detection_validation_testsiemparsing_test_elastic_parse": ".test_elastic_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L216 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_factory": ".test_factory()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L231 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_sentinel_parse": ".test_sentinel_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L205 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_splunk_parse": ".test_splunk_parse()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L188 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsiemparsing_test_splunk_spl_includes_host_and_time": ".test_splunk_spl_includes_host_and_time()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L200 | neighbors=[TestSIEMParsing]
- "tests_test_detection_validation_testsigmarulegenerator_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L148 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_evidence_customises_rule": ".test_evidence_customises_rule()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L169 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_known_technique_template": ".test_known_technique_template()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L151 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_output_is_valid_yaml_and_stable_id": ".test_output_is_valid_yaml_and_stable_id()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L176 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_subtechnique_falls_back_to_parent": ".test_subtechnique_falls_back_to_parent()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L158 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsigmarulegenerator_test_unknown_technique_uses_generic": ".test_unknown_technique_uses_generic()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L164 | neighbors=[TestSigmaRuleGenerator]
- "tests_test_detection_validation_testsplunkintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L299 | neighbors=[TestSplunkIntegration]
- "tests_test_detection_validation_testsplunkintegration_test_live_query": ".test_live_query()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L306 | neighbors=[TestSplunkIntegration]
- "tests_test_engagement_lists_rationale_1": "Unit tests for the dashboard list endpoints (jobs + assets)." | kind=entity | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[test_engagement_lists.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-091.json

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
