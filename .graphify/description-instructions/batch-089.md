# Node Description Batch 90 of 104

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
- "tests_test_cli_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_cli.py:L153 | neighbors=[FakeClient]
- "tests_test_cli_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_cli.py:L157 | neighbors=[FakeClient]
- "tests_test_cli_test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity": "test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity()" | kind=code-symbol | source=probe/tests/test_cli.py:L318 | neighbors=[test_cli.py]
- "tests_test_cli_test_cmd_doctor_fails_when_no_agent_unless_allowed": "test_cmd_doctor_fails_when_no_agent_unless_allowed()" | kind=code-symbol | source=probe/tests/test_cli.py:L248 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_malformed_json": "test_config_store_rejects_malformed_json()" | kind=code-symbol | source=probe/tests/test_cli.py:L31 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_non_object_profiles": "test_config_store_rejects_non_object_profiles()" | kind=code-symbol | source=probe/tests/test_cli.py:L38 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_writes_private_file": "test_config_store_writes_private_file()" | kind=code-symbol | source=probe/tests/test_cli.py:L13 | neighbors=[test_cli.py]
- "tests_test_cli_test_normalize_manager_url_trims_and_validates": "test_normalize_manager_url_trims_and_validates()" | kind=code-symbol | source=probe/tests/test_cli.py:L72 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_rejects_missing_equals": "test_parse_param_pairs_rejects_missing_equals()" | kind=code-symbol | source=probe/tests/test_cli.py:L59 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_supports_json_values": "test_parse_param_pairs_supports_json_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L45 | neighbors=[test_cli.py]
- "tests_test_cli_test_parser_accepts_json_after_concrete_commands": "test_parser_accepts_json_after_concrete_commands()" | kind=code-symbol | source=probe/tests/test_cli.py:L80 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_env_overrides_config": "test_resolve_profile_env_overrides_config()" | kind=code-symbol | source=probe/tests/test_cli.py:L106 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_reports_missing_manager_or_token": "test_resolve_profile_reports_missing_manager_or_token()" | kind=code-symbol | source=probe/tests/test_cli.py:L134 | neighbors=[test_cli.py]
- "tests_test_cli_test_split_values_accepts_repeated_and_csv_values": "test_split_values_accepts_repeated_and_csv_values()" | kind=code-symbol | source=probe/tests/test_cli.py:L64 | neighbors=[test_cli.py]
- "tests_test_db_scanner_fakereader_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L18 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakereader_read": ".read()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L21 | neighbors=[FakeReader]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-089.json

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
