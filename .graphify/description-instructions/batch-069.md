# Node Description Batch 70 of 76

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

- "tests_test_ad_assessment_testntlmrelaychecker_test_no_finding_when_all_secure": ".test_no_finding_when_all_secure()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L270 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_smb_signing_without_impacket_marks_unreachable": ".test_smb_signing_without_impacket_marks_unreachable()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L252 | neighbors=[TestNTLMRelayChecker]
- "tests_test_agents_testaccesstokenexpiry_test_custom_expiry_overrides_default": ".test_custom_expiry_overrides_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L327 | neighbors=[TestAccessTokenExpiry]
- "tests_test_agents_testagentexecutabletypes_test_network_types_included": ".test_network_types_included()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L30 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentexecutabletypes_test_server_side_types_excluded": ".test_server_side_types_excluded()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L35 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testgetagentjobs_test_404_when_agent_unknown": ".test_404_when_agent_unknown()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L166 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_jobs_include_params": ".test_jobs_include_params()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L142 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testpromoteassets_test_creates_asset_and_services_with_cpe": ".test_creates_asset_and_services_with_cpe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L263 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_empty_result_is_noop": ".test_empty_result_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L320 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_skips_host_without_ip": ".test_skips_host_without_ip()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L313 | neighbors=[TestPromoteAssets]
- "tests_test_ai_engine_testhallucinationguard_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L106 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_cve_all_known_valid": ".test_cve_all_known_valid()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L117 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_cve_invention_flagged": ".test_cve_invention_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L109 | neighbors=[TestHallucinationGuard]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-069.json

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
