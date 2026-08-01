# Node Description Batch 112 of 119

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
Write every description in Portuguese (pt). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_transport_testheartbeat_test_heartbeat_sends_current_job": ".test_heartbeat_sends_current_job()" | kind=code-symbol | source=probe/tests/test_transport.py:L235 | neighbors=[TestHeartbeat]
- "tests_test_transport_testheartbeat_test_successful_heartbeat": ".test_successful_heartbeat()" | kind=code-symbol | source=probe/tests/test_transport.py:L217 | neighbors=[TestHeartbeat]
- "tests_test_transport_testhttpget_test_exception_returns_none": ".test_exception_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L384 | neighbors=[TestHttpGet]
- "tests_test_transport_testhttpget_test_non_200_returns_none": ".test_non_200_returns_none()" | kind=code-symbol | source=probe/tests/test_transport.py:L375 | neighbors=[TestHttpGet]
- "tests_test_transport_testhttpget_test_successful_get": ".test_successful_get()" | kind=code-symbol | source=probe/tests/test_transport.py:L365 | neighbors=[TestHttpGet]
- "tests_test_transport_testidentity_test_agent_state_updates_preserve_scope_identity": ".test_agent_state_updates_preserve_scope_identity()" | kind=code-symbol | source=probe/tests/test_transport.py:L70 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_auth_header": ".test_auth_header()" | kind=code-symbol | source=probe/tests/test_transport.py:L38 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_failed_atomic_replace_preserves_previous_state": ".test_failed_atomic_replace_preserves_previous_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L107 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_is_authenticated_false_initially": ".test_is_authenticated_false_initially()" | kind=code-symbol | source=probe/tests/test_transport.py:L30 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_is_authenticated_true_with_creds": ".test_is_authenticated_true_with_creds()" | kind=code-symbol | source=probe/tests/test_transport.py:L34 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_loads_cached_agent_identity_from_state": ".test_loads_cached_agent_identity_from_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L57 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_private_state_uses_restrictive_modes_and_fsync": ".test_private_state_uses_restrictive_modes_and_fsync()" | kind=code-symbol | source=probe/tests/test_transport.py:L94 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_save_and_clear_state": ".test_save_and_clear_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L42 | neighbors=[TestIdentity]
- "tests_test_transport_testpolljobs_test_poll_401_raises": ".test_poll_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L259 | neighbors=[TestPollJobs]
- "tests_test_transport_testpolljobs_test_poll_uses_limit_param": ".test_poll_uses_limit_param()" | kind=code-symbol | source=probe/tests/test_transport.py:L268 | neighbors=[TestPollJobs]
- "tests_test_transport_testpolljobs_test_returns_jobs": ".test_returns_jobs()" | kind=code-symbol | source=probe/tests/test_transport.py:L248 | neighbors=[TestPollJobs]
- "tests_test_transport_testrefreshregistration_test_cached_agent_refreshes_capabilities": ".test_cached_agent_refreshes_capabilities()" | kind=code-symbol | source=probe/tests/test_transport.py:L173 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testrefreshregistration_test_old_manager_returns_compatibility_signal": ".test_old_manager_returns_compatibility_signal()" | kind=code-symbol | source=probe/tests/test_transport.py:L193 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testrefreshregistration_test_rejected_cached_identity_raises": ".test_rejected_cached_identity_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L204 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testregister_test_registration_401_raises": ".test_registration_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L154 | neighbors=[TestRegister]
- "tests_test_transport_testregister_test_registration_sends_public_key": ".test_registration_sends_public_key()" | kind=code-symbol | source=probe/tests/test_transport.py:L161 | neighbors=[TestRegister]
- "tests_test_transport_testregister_test_successful_registration": ".test_successful_registration()" | kind=code-symbol | source=probe/tests/test_transport.py:L130 | neighbors=[TestRegister]
- "tests_test_transport_testsubmitresult_test_2xx_variants_return_true": ".test_2xx_variants_return_true()" | kind=code-symbol | source=probe/tests/test_transport.py:L337 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_client_errors_return_false_no_data_loss": ".test_client_errors_return_false_no_data_loss()" | kind=code-symbol | source=probe/tests/test_transport.py:L327 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_large_payload_is_gzipped": ".test_large_payload_is_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L344 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_network_error_returns_false": ".test_network_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L319 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_server_error_returns_false": ".test_server_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L310 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_small_payload_not_gzipped": ".test_small_payload_not_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L355 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_successful_submit": ".test_successful_submit()" | kind=code-symbol | source=probe/tests/test_transport.py:L301 | neighbors=[TestSubmitResult]
- "tests_test_transport_testwebsocket_test_is_ws_connected_false_by_default": ".test_is_ws_connected_false_by_default()" | kind=code-symbol | source=probe/tests/test_transport.py:L394 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_requires_token": ".test_ws_requires_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L412 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_http": ".test_ws_url_http()" | kind=code-symbol | source=probe/tests/test_transport.py:L398 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_https": ".test_ws_url_https()" | kind=code-symbol | source=probe/tests/test_transport.py:L405 | neighbors=[TestWebSocket]
- "tests_test_udp_amplifiers_test_dns_open_recursion": "test_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L18 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_memcached_exposed": "test_memcached_exposed()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L26 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_ntp_monlist_absent": "test_ntp_monlist_absent()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L13 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_ntp_monlist_enabled": "test_ntp_monlist_enabled()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L8 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_probe_builders_are_bytes": "test_probe_builders_are_bytes()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L31 | neighbors=[test_udp_amplifiers.py]
- "tests_test_use_cases_rationale_1": "Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only" | kind=entity | source=probe/tests/test_use_cases.py:L1 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_descriptions_do_not_overclaim": "test_descriptions_do_not_overclaim()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L16 | neighbors=[test_use_cases.py]

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
