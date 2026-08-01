# Node Description Batch 99 of 119

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

- "tests_test_ai_engine_testhallucinationguard_test_cvss_match_passes": ".test_cvss_match_passes()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L126 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_cvss_mismatch_flagged": ".test_cvss_mismatch_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L121 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_destructive_command_flagged": ".test_destructive_command_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L130 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_drop_table_flagged": ".test_drop_table_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L135 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_safe_remediation_passes": ".test_safe_remediation_passes()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L139 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_validate_aggregate_confidence": ".test_validate_aggregate_confidence()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L143 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_validate_clean_text": ".test_validate_clean_text()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L152 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testvulnprioritizer_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L49 | neighbors=[TestVulnPrioritizer]
- "tests_test_ai_engine_testvulnprioritizer_test_fallback_score_capped": ".test_fallback_score_capped()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L88 | neighbors=[TestVulnPrioritizer]
- "tests_test_ai_engine_testvulnprioritizer_test_starts_untrained": ".test_starts_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L52 | neighbors=[TestVulnPrioritizer]
- "tests_test_ai_engine_testvulnprioritizer_test_train_without_xgboost_raises": ".test_train_without_xgboost_raises()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L92 | neighbors=[TestVulnPrioritizer]
- "tests_test_attack_paths_built_graph": "built_graph()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L39 | neighbors=[test_attack_paths.py]
- "tests_test_attack_paths_demo": "demo()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L34 | neighbors=[test_attack_paths.py]
- "tests_test_attack_paths_testgraphbuilder_test_asset_node_attributes": ".test_asset_node_attributes()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L59 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_connects_to_and_same_segment_edges": ".test_connects_to_and_same_segment_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L77 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_credential_reuse_edges": ".test_credential_reuse_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L82 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_complexity_falls_back_to_severity": ".test_exploit_complexity_falls_back_to_severity()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L102 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_complexity_from_vector": ".test_exploit_complexity_from_vector()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L95 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_edges_only_for_exploitable": ".test_exploit_edges_only_for_exploitable()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L70 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_has_service_and_has_finding_edges": ".test_has_service_and_has_finding_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L65 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_is_internet_exposed": ".test_is_internet_exposed()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L87 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_nodes_and_edges_created": ".test_nodes_and_edges_created()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L54 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_highlights_top_path": ".test_d3_highlights_top_path()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L202 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_marks_compromised": ".test_d3_marks_compromised()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L197 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_shape": ".test_d3_shape()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L187 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_layout_is_deterministic": ".test_layout_is_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L210 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testneo4jclient_test_run_without_connection_returns_empty": ".test_run_without_connection_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L222 | neighbors=[TestNeo4jClient]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-098.json

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
