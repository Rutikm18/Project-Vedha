# Node Description Batch 113 of 119

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

- "tests_test_use_cases_test_iot_survey_collects_banners": "test_iot_survey_collects_banners()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L36 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_udp_claims_amplification": "test_udp_claims_amplification()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L27 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L23 | neighbors=[test_use_cases.py]
- "tests_test_version_compare_rationale_1": "Cross-validates the pure-Python Debian version comparator against the real `dpkg" | kind=entity | source=manager/detection_engine/tests/test_version_compare.py:L1 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_dpkg_compare_public_api": "test_dpkg_compare_public_api()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L65 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_pure_python_matches_known_pairs": "test_pure_python_matches_known_pairs()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L45 | neighbors=[test_version_compare.py]
- "tests_test_version_compare_test_pure_python_matches_real_dpkg_binary": "test_pure_python_matches_real_dpkg_binary()" | kind=code-symbol | source=manager/detection_engine/tests/test_version_compare.py:L52 | neighbors=[test_version_compare.py]
- "tests_test_vuln_enrichment_test_dedup_hash_case_insensitive_cve": "test_dedup_hash_case_insensitive_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L242 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_dedup_hash_different_inputs": "test_dedup_hash_different_inputs()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L248 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_dedup_hash_stable": "test_dedup_hash_stable()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L236 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_epss_empty": "test_fetch_epss_empty()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L114 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_mitre_known_cve": "test_fetch_mitre_known_cve()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L148 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_fetch_nvd_not_found": "test_fetch_nvd_not_found()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L82 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_kev_bonus_increases_score": "test_kev_bonus_increases_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L186 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_max_risk_score": "test_max_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L164 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_risk_score_bounds": "test_risk_score_bounds()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L193 | neighbors=[test_vuln_enrichment.py]
- "tests_test_vuln_enrichment_test_zero_risk_score": "test_zero_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_vuln_enrichment.py:L175 | neighbors=[test_vuln_enrichment.py]
- "tests_test_web_methods_test_dangerous_methods_flagged": "test_dangerous_methods_flagged()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L4 | neighbors=[test_web_methods.py]
- "tests_test_web_methods_test_no_allow_header": "test_no_allow_header()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L17 | neighbors=[test_web_methods.py]
- "tests_test_web_methods_test_safe_methods_only": "test_safe_methods_only()" | kind=code-symbol | source=probe/tests/test_web_methods.py:L12 | neighbors=[test_web_methods.py]
- "tests_test_workflow_execution_concurrencyscanner_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L49 | neighbors=[_ConcurrencyScanner]
- "tests_test_workflow_execution_concurrencyscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L53 | neighbors=[_ConcurrencyScanner]
- "tests_test_workflow_execution_explodingscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L32 | neighbors=[_ExplodingScanner]
- "tests_test_workflow_execution_test_agent_scan_types_have_distinct_stage_ceilings": "test_agent_scan_types_have_distinct_stage_ceilings()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L419 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_database_gate_uses_scanner_port_catalog": "test_database_gate_uses_scanner_port_catalog()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L132 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_empty_authoritative_scope_never_falls_back_to_job_targets": "test_empty_authoritative_scope_never_falls_back_to_job_targets()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L519 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_applies_configured_target_ceiling": "test_engine_applies_configured_target_ceiling()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L446 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_deadline_fails_when_no_evidence_exists": "test_engine_deadline_fails_when_no_evidence_exists()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L467 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_deadline_preserves_verified_partial_evidence": "test_engine_deadline_preserves_verified_partial_evidence()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L486 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_enforces_local_scope_after_engagement_scope": "test_engine_enforces_local_scope_after_engagement_scope()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L455 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_exposes_component_manifest_and_run_states": "test_engine_exposes_component_manifest_and_run_states()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L530 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_fails_when_every_observation_is_an_error": "test_engine_fails_when_every_observation_is_an_error()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L566 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_rejects_non_string_targets": "test_engine_rejects_non_string_targets()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L431 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_engine_rejects_oversized_cidr_instead_of_false_success": "test_engine_rejects_oversized_cidr_instead_of_false_success()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L438 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_error_result_does_not_mutate_asset_state": "test_error_result_does_not_mutate_asset_state()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L87 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_execution_trace_reports_partial_component": "test_execution_trace_reports_partial_component()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L99 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_explicit_empty_port_catalog_never_falls_back_to_top_ports": "test_explicit_empty_port_catalog_never_falls_back_to_top_ports()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L143 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_filtered_jobs_use_only_requested_tcp_catalogs": "test_filtered_jobs_use_only_requested_tcp_catalogs()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L136 | neighbors=[test_workflow_execution.py]
- "tests_test_workflow_execution_test_manifest_does_not_claim_external_engine_executed": "test_manifest_does_not_claim_external_engine_executed()" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L119 | neighbors=[test_workflow_execution.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-112.json

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
