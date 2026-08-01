# Node Description Batch 98 of 119

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

- "tests_test_ad_assessment_testldapenumeratorparsing_test_search_without_connection_raises": ".test_search_without_connection_raises()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L158 | neighbors=[TestLDAPEnumeratorParsing]
- "tests_test_ad_assessment_testntlmrelaychecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L249 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_for_ldap_signing_only": ".test_finding_for_ldap_signing_only()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L265 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_includes_ntlmrelayx_command": ".test_finding_includes_ntlmrelayx_command()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L258 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_no_finding_when_all_secure": ".test_no_finding_when_all_secure()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L270 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_smb_signing_without_impacket_marks_unreachable": ".test_smb_signing_without_impacket_marks_unreachable()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L252 | neighbors=[TestNTLMRelayChecker]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_accepts_bearer_header": ".test_accepts_bearer_header()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L18 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_rejects_query_string_credentials": ".test_rejects_query_string_credentials()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L26 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testjobsecretboundary_test_allows_non_secret_scan_tuning": ".test_allows_non_secret_scan_tuning()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L79 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testjobsecretboundary_test_detects_persisted_secret_material": ".test_detects_persisted_secret_material()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L74 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_displaced_socket_cannot_unregister_reconnect": ".test_displaced_socket_cannot_unregister_reconnect()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L93 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_first_online_push_cannot_cross_tenants": ".test_first_online_push_cannot_cross_tenants()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L147 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_only_returns_online_agents_in_requested_tenant": ".test_only_returns_online_agents_in_requested_tenant()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L120 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testusecasecatalogparity_test_manager_and_probe_route_use_cases_identically": ".test_manager_and_probe_route_use_cases_identically()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L37 | neighbors=[TestUseCaseCatalogParity]
- "tests_test_agent_identity_test_generated_scope_identity_preserves_agent_credentials": "test_generated_scope_identity_preserves_agent_credentials()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L19 | neighbors=[test_agent_identity.py]
- "tests_test_agents_testaccesstokenexpiry_test_custom_expiry_overrides_default": ".test_custom_expiry_overrides_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L650 | neighbors=[TestAccessTokenExpiry]
- "tests_test_agents_testagentexecutabletypes_test_network_types_included": ".test_network_types_included()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L30 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentexecutabletypes_test_server_side_types_excluded": ".test_server_side_types_excluded()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L35 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentjobcompatibility_test_agent_network_segments_are_normalized_and_validated": ".test_agent_network_segments_are_normalized_and_validated()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L465 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_must_cover_entire_scope": ".test_declared_segment_must_cover_entire_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L385 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_rejects_missing_or_invalid_scope": ".test_declared_segment_rejects_missing_or_invalid_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L395 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_empty_capabilities_receive_no_jobs": ".test_empty_capabilities_receive_no_jobs()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L405 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_empty_segments_are_fail_closed": ".test_empty_segments_are_fail_closed()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L402 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_explicit_out_of_scope_target_is_never_dispatched": ".test_explicit_out_of_scope_target_is_never_dispatched()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L432 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_hostname_and_explicit_empty_targets_are_not_routable": ".test_hostname_and_explicit_empty_targets_are_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L455 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_requested_ip_range_uses_only_its_covered_networks": ".test_requested_ip_range_uses_only_its_covered_networks()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L444 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_requested_subset_routes_to_a_subset_probe": ".test_requested_subset_routes_to_a_subset_probe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L414 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_use_case_resolves_to_required_capability": ".test_use_case_resolves_to_required_capability()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L379 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentregistrationrefresh_test_agent_can_refresh_only_its_own_routing_metadata": ".test_agent_can_refresh_only_its_own_routing_metadata()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L211 | neighbors=[TestAgentRegistrationRefresh]
- "tests_test_agents_testagentregistrationrefresh_test_agent_cannot_refresh_another_identity": ".test_agent_cannot_refresh_another_identity()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L247 | neighbors=[TestAgentRegistrationRefresh]
- "tests_test_agents_testgetagentjobs_test_404_when_agent_unknown": ".test_404_when_agent_unknown()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L369 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_jobs_include_params": ".test_jobs_include_params()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L271 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_skips_job_outside_declared_network_segments": ".test_skips_job_outside_declared_network_segments()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L339 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testgetagentjobs_test_skips_job_when_capability_is_missing": ".test_skips_job_when_capability_is_missing()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L309 | neighbors=[TestGetAgentJobs]
- "tests_test_agents_testpromoteassets_test_creates_asset_and_services_with_cpe": ".test_creates_asset_and_services_with_cpe()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L586 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_empty_result_is_noop": ".test_empty_result_is_noop()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L643 | neighbors=[TestPromoteAssets]
- "tests_test_agents_testpromoteassets_test_skips_host_without_ip": ".test_skips_host_without_ip()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L636 | neighbors=[TestPromoteAssets]
- "tests_test_ai_engine_testhallucinationguard_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L106 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_cve_all_known_valid": ".test_cve_all_known_valid()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L117 | neighbors=[TestHallucinationGuard]
- "tests_test_ai_engine_testhallucinationguard_test_cve_invention_flagged": ".test_cve_invention_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L109 | neighbors=[TestHallucinationGuard]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-097.json

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
