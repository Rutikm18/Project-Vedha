# Node Description Batch 112 of 134

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
- "tests_test_auth_login_rationale_1": "Tests for authentication login flow.  Covers:   - login success   - user_not_fou" | kind=entity | source=manager/backend/tests/test_auth_login.py:L1 | neighbors=[test_auth_login.py]
- "tests_test_auth_login_rationale_224": "Ensure every exception class has the expected reason_code attribute.     These c" | kind=entity | source=manager/backend/tests/test_auth_login.py:L224 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_rationale_70": "AsyncSession mock that returns user on first execute, tenant on second." | kind=entity | source=manager/backend/tests/test_auth_login.py:L70 | neighbors=[_make_db()]
- "tests_test_auth_login_testauthenticatedatabasefailure_test_raises_database_failure_on_sqlalchemy_error": ".test_raises_database_failure_on_sqlalchemy_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L183 | neighbors=[TestAuthenticateDatabaseFailure]
- "tests_test_auth_login_testreasoncodes_test_bcrypt_failure_code": ".test_bcrypt_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L242 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_database_failure_code": ".test_database_failure_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L245 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_disabled_tenant_code": ".test_disabled_tenant_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L236 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_disabled_user_code": ".test_disabled_user_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L233 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_expired_password_code": ".test_expired_password_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L239 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_password_mismatch_code": ".test_password_mismatch_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L230 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_testreasoncodes_test_user_not_found_code": ".test_user_not_found_code()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L227 | neighbors=[TestReasonCodes]
- "tests_test_auth_login_teststartupdiagnostics_test_bcrypt_round_trip_passes": ".test_bcrypt_round_trip_passes()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L277 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_fatal_in_production": ".test_cookie_config_fatal_in_production()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L283 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_cookie_config_ok_in_development": ".test_cookie_config_ok_in_development()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L293 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_database_check_returns_fatal_on_connection_error": ".test_database_check_returns_fatal_on_connection_error()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L303 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_known_weak_is_fatal": ".test_jwt_secret_known_weak_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L261 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_strong_is_ok": ".test_jwt_secret_strong_is_ok()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L269 | neighbors=[TestStartupDiagnostics]
- "tests_test_auth_login_teststartupdiagnostics_test_jwt_secret_too_short_is_fatal": ".test_jwt_secret_too_short_is_fatal()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L253 | neighbors=[TestStartupDiagnostics]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-111.json

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
