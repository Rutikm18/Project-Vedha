# Node Description Batch 268 of 332

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

- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_closed": ".test_returns_immediately_on_closed()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L133 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_reply": ".test_returns_immediately_on_reply()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L120 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_creates_controller": ".test_adaptive_scanner_creates_controller()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L186 | neighbors=[TestUdpScannerAdaptive]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_detects_open_on_loopback": ".test_adaptive_scanner_detects_open_on_loopback()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L198 | neighbors=[TestUdpScannerAdaptive]
- "tests_test_adaptive_rate_testudpscanneradaptive_test_non_adaptive_scanner_has_no_controller": ".test_non_adaptive_scanner_has_no_controller()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L192 | neighbors=[TestUdpScannerAdaptive]
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
- "tests_test_agent_identity_test_generated_scope_identity_preserves_agent_credentials": "test_generated_scope_identity_preserves_agent_credentials()" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L23 | neighbors=[test_agent_identity.py]
- "tests_test_agent_policy_rationale_1": "test_agent_policy.py — the pure deterministic agent policy engine." | kind=entity | source=manager/backend/tests/test_agent_policy.py:L1 | neighbors=[test_agent_policy.py]
- "tests_test_agent_policy_testclassifyaction_test_known_actions_map_to_expected_tier": ".test_known_actions_map_to_expected_tier()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L23 | neighbors=[TestClassifyAction]
- "tests_test_agent_policy_testclassifyaction_test_unknown_action_fails_closed_to_highest_tier": ".test_unknown_action_fails_closed_to_highest_tier()" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L26 | neighbors=[TestClassifyAction]
- "tests_test_agent_read_tools_fakesession_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L39 | neighbors=[_FakeSession]
- "tests_test_agent_read_tools_fakesession_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L35 | neighbors=[_FakeSession]
- "tests_test_agent_read_tools_rationale_1": "Regression tests for AgentDecisionEngine._list_assets service batching.  The rea" | kind=entity | source=manager/backend/tests/test_agent_read_tools.py:L1 | neighbors=[test_agent_read_tools.py]
- "tests_test_agent_read_tools_rationale_20": "Mimics the subset of a SQLAlchemy Result the read tools use." | kind=entity | source=manager/backend/tests/test_agent_read_tools.py:L20 | neighbors=[_Result]
- "tests_test_agent_read_tools_rationale_33": "Returns queued results in call order and counts execute() calls." | kind=entity | source=manager/backend/tests/test_agent_read_tools.py:L33 | neighbors=[_FakeSession]
- "tests_test_agent_read_tools_result_all": ".all()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L28 | neighbors=[_Result]
- "tests_test_agent_read_tools_result_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L22 | neighbors=[_Result]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-267.json

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
