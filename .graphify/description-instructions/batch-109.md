# Node Description Batch 110 of 134

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

- "tests_test_ad_assessment_testbloodhoundcollector_test_query_da_paths_without_driver": ".test_query_da_paths_without_driver()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L376 | neighbors=[TestBloodHoundCollector]
- "tests_test_ad_assessment_testbuildadfinding_test_attack_narrative_carried_in_evidence": ".test_attack_narrative_carried_in_evidence()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L84 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_invalid_severity_falls_back_to_info": ".test_invalid_severity_falls_back_to_info()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L76 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testbuildadfinding_test_required_fields_present": ".test_required_fields_present()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L60 | neighbors=[TestBuildADFinding]
- "tests_test_ad_assessment_testkerberoastchecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L170 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_finding_critical_when_privileged": ".test_finding_critical_when_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L189 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_finding_high_when_not_privileged": ".test_finding_high_when_not_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L197 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_no_finding_when_empty": ".test_no_finding_when_empty()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L202 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testkerberoastchecker_test_request_tgs_without_impacket_returns_none": ".test_request_tgs_without_impacket_returns_none()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L205 | neighbors=[TestKerberoastChecker]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_domain_to_base_dn": ".test_domain_to_base_dn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L99 | neighbors=[TestLDAPEnumeratorParsing]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_search_without_connection_raises": ".test_search_without_connection_raises()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L158 | neighbors=[TestLDAPEnumeratorParsing]
- "tests_test_ad_assessment_testntlmrelaychecker_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L249 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_for_ldap_signing_only": ".test_finding_for_ldap_signing_only()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L265 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_finding_includes_ntlmrelayx_command": ".test_finding_includes_ntlmrelayx_command()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L258 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_no_finding_when_all_secure": ".test_no_finding_when_all_secure()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L270 | neighbors=[TestNTLMRelayChecker]
- "tests_test_ad_assessment_testntlmrelaychecker_test_smb_signing_without_impacket_marks_unreachable": ".test_smb_signing_without_impacket_marks_unreachable()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L252 | neighbors=[TestNTLMRelayChecker]
- "tests_test_agent_auth_boundary_test_admin_enrollment_approval_is_not_public": "test_admin_enrollment_approval_is_not_public()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L94 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_legacy_agent_jwt_allows_only_workload_operations": "test_legacy_agent_jwt_allows_only_workload_operations()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L23 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_legacy_agent_jwt_rejects_human_and_wrong_method_operations": "test_legacy_agent_jwt_rejects_human_and_wrong_method_operations()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L43 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_only_device_side_enrollment_posts_are_public": "test_only_device_side_enrollment_posts_are_public()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L89 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_accepts_bearer_header": ".test_accepts_bearer_header()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L18 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_rejects_query_string_credentials": ".test_rejects_query_string_credentials()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L26 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testjobsecretboundary_test_allows_non_secret_scan_tuning": ".test_allows_non_secret_scan_tuning()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L79 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testjobsecretboundary_test_detects_persisted_secret_material": ".test_detects_persisted_secret_material()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L74 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_displaced_socket_cannot_unregister_reconnect": ".test_displaced_socket_cannot_unregister_reconnect()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L106 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_first_online_push_cannot_cross_tenants": ".test_first_online_push_cannot_cross_tenants()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L160 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_online_heartbeat_clears_finished_job": ".test_online_heartbeat_clears_finished_job()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L93 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_only_returns_online_agents_in_requested_tenant": ".test_only_returns_online_agents_in_requested_tenant()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L133 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testusecasecatalogparity_test_manager_and_probe_route_use_cases_identically": ".test_manager_and_probe_route_use_cases_identically()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L37 | neighbors=[TestUseCaseCatalogParity]
- "tests_test_agent_identity_test_generated_scope_identity_preserves_agent_credentials": "test_generated_scope_identity_preserves_agent_credentials()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L19 | neighbors=[test_agent_identity.py]
- "tests_test_agents_rationale_641": "Re-registering the same-named probe must reuse the row, not create a dup." | kind=entity | source=manager/backend/tests/test_agents.py:L641 | neighbors=[.test_reuses_existing_probe_by_name()]
- "tests_test_agents_rationale_676": "Agent token must outlive the 15-min access default so it doesn't churn." | kind=entity | source=manager/backend/tests/test_agents.py:L676 | neighbors=[.test_agent_token_is_long_lived()]
- "tests_test_agents_rationale_694": "Discovery results → assets/services promotion (makes the Attack Surface populate" | kind=entity | source=manager/backend/tests/test_agents.py:L694 | neighbors=[TestPromoteAssets]
- "tests_test_agents_rationale_722": "A single web scan can emit multiple facts for the same host:port." | kind=entity | source=manager/backend/tests/test_agents.py:L722 | neighbors=[.test_dedupes_duplicate_services_in_sam…]
- "tests_test_agents_testaccesstokenexpiry_test_custom_expiry_overrides_default": ".test_custom_expiry_overrides_default()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L761 | neighbors=[TestAccessTokenExpiry]
- "tests_test_agents_testagentexecutabletypes_test_network_types_included": ".test_network_types_included()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L30 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentexecutabletypes_test_server_side_types_excluded": ".test_server_side_types_excluded()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L35 | neighbors=[TestAgentExecutableTypes]
- "tests_test_agents_testagentjobcompatibility_test_agent_network_segments_are_normalized_and_validated": ".test_agent_network_segments_are_normalized_and_validated()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L513 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_must_cover_entire_scope": ".test_declared_segment_must_cover_entire_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L413 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_declared_segment_rejects_missing_or_invalid_scope": ".test_declared_segment_rejects_missing_or_invalid_scope()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L423 | neighbors=[TestAgentJobCompatibility]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
