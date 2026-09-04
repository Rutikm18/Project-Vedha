# Node Description Batch 266 of 330

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
- "tests_test_adaptive_rate_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L178 | neighbors=[_EchoProtocol]
- "tests_test_adaptive_rate_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L181 | neighbors=[_EchoProtocol]
- "tests_test_adaptive_rate_rationale_1": "test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit." | kind=entity | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[test_adaptive_rate.py]
- "tests_test_adaptive_rate_testudpretransmit_test_retries_exhaust_on_silence": ".test_retries_exhaust_on_silence()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L146 | neighbors=[TestUdpRetransmit]
- "tests_test_adaptive_rate_testudpretransmit_test_retry_recovers_dropped_reply": ".test_retry_recovers_dropped_reply()" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L159 | neighbors=[TestUdpRetransmit]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-265.json

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
