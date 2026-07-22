# Node Description Batch 71 of 76

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

- "tests_test_attack_paths_testneo4jclient_test_run_write_noop_without_connection": ".test_run_write_noop_without_connection()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L226 | neighbors=[TestNeo4jClient]
- "tests_test_attack_paths_testneo4jclient_test_sync_to_neo4j_noop_without_client": ".test_sync_to_neo4j_noop_without_client()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L230 | neighbors=[TestNeo4jClient]
- "tests_test_attack_paths_testpathanalyzer_test_blast_radius_unknown_asset": ".test_blast_radius_unknown_asset()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L170 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_chokepoints_empty_without_paths": ".test_chokepoints_empty_without_paths()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L159 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_cypher_constants_present": ".test_cypher_constants_present()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L175 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_find_blast_radius": ".test_find_blast_radius()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L163 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_find_paths_to_target": ".test_find_paths_to_target()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L114 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_identify_chokepoints": ".test_identify_chokepoints()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L150 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_no_paths_for_unknown_target": ".test_no_paths_for_unknown_target()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L129 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_paths_sorted_by_risk_desc": ".test_paths_sorted_by_risk_desc()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L123 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_clamped_0_100": ".test_score_path_clamped_0_100()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L145 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_credential_reuse_bonus": ".test_score_path_credential_reuse_bonus()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L139 | neighbors=[TestPathAnalyzer]
- "tests_test_attack_paths_testpathanalyzer_test_score_path_rewards_cvss_penalises_hops": ".test_score_path_rewards_cvss_penalises_hops()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L133 | neighbors=[TestPathAnalyzer]
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
- "tests_test_exploit_engine_testmetasploitintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L434 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_connect_and_list_modules": ".test_connect_and_list_modules()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L441 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_run_safe_scanner_smb": ".test_run_safe_scanner_smb()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L450 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_call_without_connect_raises": ".test_call_without_connect_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L233 | neighbors=[TestMetasploitRPCClient]
- "tests_test_exploit_engine_testnucleiexploitrunner_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L351 | neighbors=[TestNucleiExploitRunner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-070.json

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
