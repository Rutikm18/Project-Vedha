# Node Description Batch 152 of 186

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

- "tests_test_adaptive_rate_testwindowgating_test_acquire_blocks_when_window_full": ".test_acquire_blocks_when_window_full()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L80 | neighbors=[TestWindowGating]
- "tests_test_adaptive_rate_testwindowgating_test_release_unblocks_waiter": ".test_release_unblocks_waiter()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L92 | neighbors=[TestWindowGating]
- "tests_test_adaptive_rate_testwindowgating_test_report_loss_shrinks_and_releases": ".test_report_loss_shrinks_and_releases()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L108 | neighbors=[TestWindowGating]
- "tests_test_adaptive_rate_testwindowstatemachine_test_congestion_avoidance_grows_sublinearly": ".test_congestion_avoidance_grows_sublinearly()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L39 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_initial_window": ".test_initial_window()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L28 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_loss_halves_window": ".test_loss_halves_window()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L45 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_loss_sets_ssthresh_to_half": ".test_loss_sets_ssthresh_to_half()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L50 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_recovery_after_loss_enters_congestion_avoidance": ".test_recovery_after_loss_enters_congestion_avoidance()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L69 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_slow_start_grows_by_one_per_success": ".test_slow_start_grows_by_one_per_success()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L32 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_window_never_above_max": ".test_window_never_above_max()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L62 | neighbors=[TestWindowStateMachine]
- "tests_test_adaptive_rate_testwindowstatemachine_test_window_never_below_min": ".test_window_never_below_min()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L55 | neighbors=[TestWindowStateMachine]
- "tests_test_agent_auth_boundary_test_admin_enrollment_approval_is_not_public": "test_admin_enrollment_approval_is_not_public()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L94 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_legacy_agent_jwt_allows_only_workload_operations": "test_legacy_agent_jwt_allows_only_workload_operations()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L23 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_legacy_agent_jwt_rejects_human_and_wrong_method_operations": "test_legacy_agent_jwt_rejects_human_and_wrong_method_operations()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L43 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_auth_boundary_test_only_device_side_enrollment_posts_are_public": "test_only_device_side_enrollment_posts_are_public()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L89 | neighbors=[test_agent_auth_boundary.py]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_accepts_bearer_header": ".test_accepts_bearer_header()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L18 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testagentwebsocketauthentication_test_rejects_query_string_credentials": ".test_rejects_query_string_credentials()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L26 | neighbors=[TestAgentWebSocketAuthentication]
- "tests_test_agent_dispatch_testjobsecretboundary_test_allows_non_secret_scan_tuning": ".test_allows_non_secret_scan_tuning()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L84 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testjobsecretboundary_test_detects_persisted_secret_material": ".test_detects_persisted_secret_material()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L79 | neighbors=[TestJobSecretBoundary]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_displaced_socket_cannot_unregister_reconnect": ".test_displaced_socket_cannot_unregister_reconnect()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L111 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_first_online_push_cannot_cross_tenants": ".test_first_online_push_cannot_cross_tenants()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L165 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_online_heartbeat_clears_finished_job": ".test_online_heartbeat_clears_finished_job()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L98 | neighbors=[TestTenantWebSocketSelection]
- "tests_test_agent_dispatch_testtenantwebsocketselection_test_only_returns_online_agents_in_requested_tenant": ".test_only_returns_online_agents_in_requested_tenant()" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L138 | neighbors=[TestTenantWebSocketSelection]
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
- "tests_test_agents_testagentjobcompatibility_test_empty_capabilities_receive_no_jobs": ".test_empty_capabilities_receive_no_jobs()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L433 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_empty_segments_are_fail_closed": ".test_empty_segments_are_fail_closed()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L430 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_explicit_out_of_scope_target_is_never_dispatched": ".test_explicit_out_of_scope_target_is_never_dispatched()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L460 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_hostname_and_explicit_empty_targets_are_not_routable": ".test_hostname_and_explicit_empty_targets_are_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L503 | neighbors=[TestAgentJobCompatibility]
- "tests_test_agents_testagentjobcompatibility_test_missing_authoritative_scope_never_uses_job_targets_as_authority": ".test_missing_authoritative_scope_never_uses_job_targets_as_authority()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L467 | neighbors=[TestAgentJobCompatibility]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-151.json

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
