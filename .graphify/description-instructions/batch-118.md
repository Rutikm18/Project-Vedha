# Node Description Batch 119 of 144

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

- "tests_test_agents_rationale_722": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L722 | neighbors=[.test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testaccesstokenexpiry_test_custom_expiry_overrides_default": ".test_custom_expiry_overrides_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L761 | neighbors=[TestAccessTokenExpiry]
- "tests_test_agents_testagentexecutabletypes_test_network_types_included": ".test_network_types_included()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L30 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentexecutabletypes_test_server_side_types_excluded": ".test_server_side_types_excluded()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L35 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentjobcompatibility_test_agent_network_segments_are_normalized_and_validated": ".test_agent_network_segments_are_normalized_and_validated()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L513 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_must_cover_entire_scope": ".test_declared_segment_must_cover_entire_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L413 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_rejects_missing_or_invalid_scope": ".test_declared_segment_rejects_missing_or_invalid_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L423 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_empty_capabilities_receive_no_jobs": ".test_empty_capabilities_receive_no_jobs()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L433 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_empty_segments_are_fail_closed": ".test_empty_segments_are_fail_closed()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L430 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_explicit_out_of_scope_target_is_never_dispatched": ".test_explicit_out_of_scope_target_is_never_dispatched()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L460 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_hostname_and_explicit_empty_targets_are_not_routable": ".test_hostname_and_explicit_empty_targets_are_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L503 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_missing_authoritative_scope_never_uses_job_targets_as_authority": ".test_missing_authoritative_scope_never_uses_job_targets_as_authority()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L467 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_requested_ip_range_uses_only_its_covered_networks": ".test_requested_ip_range_uses_only_its_covered_networks()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L492 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_requested_subset_routes_to_a_subset_probe": ".test_requested_subset_routes_to_a_subset_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L442 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_use_case_resolves_to_required_capability": ".test_use_case_resolves_to_required_capability()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L407 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentregistrationrefresh_test_agent_can_refresh_only_its_own_routing_metadata": ".test_agent_can_refresh_only_its_own_routing_metadata()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L233 | neighbors=[TestAgentRegistrationRefresh]
- "tests_test_agents_testagentregistrationrefresh_test_agent_cannot_refresh_another_identity": ".test_agent_cannot_refresh_another_identity()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L269 | neighbors=[TestAgentRegistrationRefresh]
- "tests_test_agents_testgetagentjobs_test_404_when_agent_unknown": ".test_404_when_agent_unknown()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L397 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_jobs_include_params": ".test_jobs_include_params()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L293 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_skips_job_outside_declared_network_segments": ".test_skips_job_outside_declared_network_segments()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L367 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_skips_job_when_capability_is_missing": ".test_skips_job_when_capability_is_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L337 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testheartbeat_test_online_heartbeat_clears_completed_job": ".test_online_heartbeat_clears_completed_job()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L577 | neighbors=[TestHeartbeat]
- "tests_test_agents_testlegacybootstrap_test_shared_secret_bootstrap_is_disabled_by_default": ".test_shared_secret_bootstrap_is_disabled_by_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L613 | neighbors=[TestLegacyBootstrap]
- "tests_test_agents_testpromoteassets_test_creates_asset_and_services_with_cpe": ".test_creates_asset_and_services_with_cpe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L697 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_empty_result_is_noop": ".test_empty_result_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L754 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_skips_host_without_ip": ".test_skips_host_without_ip()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L747 | neighbors=[TestPromoteAssets]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-118.json

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
