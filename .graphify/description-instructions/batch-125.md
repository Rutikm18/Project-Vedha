# Node Description Batch 126 of 134

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

- "tests_test_transport_testidentity_test_loads_cached_agent_identity_from_state": ".test_loads_cached_agent_identity_from_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L57 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_private_state_uses_restrictive_modes_and_fsync": ".test_private_state_uses_restrictive_modes_and_fsync()" | kind=code-symbol | source=probe/tests/test_transport.py:L94 | neighbors=[TestIdentity]
- "tests_test_transport_testidentity_test_save_and_clear_state": ".test_save_and_clear_state()" | kind=code-symbol | source=probe/tests/test_transport.py:L42 | neighbors=[TestIdentity]
- "tests_test_transport_testpolljobs_test_poll_401_raises": ".test_poll_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L361 | neighbors=[TestPollJobs]
- "tests_test_transport_testpolljobs_test_poll_uses_limit_param": ".test_poll_uses_limit_param()" | kind=code-symbol | source=probe/tests/test_transport.py:L370 | neighbors=[TestPollJobs]
- "tests_test_transport_testpolljobs_test_returns_jobs": ".test_returns_jobs()" | kind=code-symbol | source=probe/tests/test_transport.py:L350 | neighbors=[TestPollJobs]
- "tests_test_transport_testrefreshregistration_test_cached_agent_refreshes_capabilities": ".test_cached_agent_refreshes_capabilities()" | kind=code-symbol | source=probe/tests/test_transport.py:L273 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testrefreshregistration_test_old_manager_returns_compatibility_signal": ".test_old_manager_returns_compatibility_signal()" | kind=code-symbol | source=probe/tests/test_transport.py:L293 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testrefreshregistration_test_rejected_cached_identity_raises": ".test_rejected_cached_identity_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L304 | neighbors=[TestRefreshRegistration]
- "tests_test_transport_testregister_test_registration_401_raises": ".test_registration_401_raises()" | kind=code-symbol | source=probe/tests/test_transport.py:L154 | neighbors=[TestRegister]
- "tests_test_transport_testregister_test_registration_sends_public_key": ".test_registration_sends_public_key()" | kind=code-symbol | source=probe/tests/test_transport.py:L161 | neighbors=[TestRegister]
- "tests_test_transport_testregister_test_successful_registration": ".test_successful_registration()" | kind=code-symbol | source=probe/tests/test_transport.py:L130 | neighbors=[TestRegister]
- "tests_test_transport_testsubmitresult_test_2xx_variants_return_true": ".test_2xx_variants_return_true()" | kind=code-symbol | source=probe/tests/test_transport.py:L451 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_client_errors_return_false_no_data_loss": ".test_client_errors_return_false_no_data_loss()" | kind=code-symbol | source=probe/tests/test_transport.py:L327 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_large_payload_is_gzipped": ".test_large_payload_is_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L458 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_network_error_returns_false": ".test_network_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L421 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_permanent_client_errors_are_marked_for_quarantine": ".test_permanent_client_errors_are_marked_for_quarantine()" | kind=code-symbol | source=probe/tests/test_transport.py:L439 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_retryable_client_errors_return_false_no_data_loss": ".test_retryable_client_errors_return_false_no_data_loss()" | kind=code-symbol | source=probe/tests/test_transport.py:L429 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_server_error_returns_false": ".test_server_error_returns_false()" | kind=code-symbol | source=probe/tests/test_transport.py:L412 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_small_payload_not_gzipped": ".test_small_payload_not_gzipped()" | kind=code-symbol | source=probe/tests/test_transport.py:L469 | neighbors=[TestSubmitResult]
- "tests_test_transport_testsubmitresult_test_successful_submit": ".test_successful_submit()" | kind=code-symbol | source=probe/tests/test_transport.py:L403 | neighbors=[TestSubmitResult]
- "tests_test_transport_testwebsocket_test_is_ws_connected_false_by_default": ".test_is_ws_connected_false_by_default()" | kind=code-symbol | source=probe/tests/test_transport.py:L508 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_requires_token": ".test_ws_requires_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L526 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_http": ".test_ws_url_http()" | kind=code-symbol | source=probe/tests/test_transport.py:L512 | neighbors=[TestWebSocket]
- "tests_test_transport_testwebsocket_test_ws_url_https": ".test_ws_url_https()" | kind=code-symbol | source=probe/tests/test_transport.py:L519 | neighbors=[TestWebSocket]
- "tests_test_udp_amplifiers_test_dns_open_recursion": "test_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L18 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_memcached_exposed": "test_memcached_exposed()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L26 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_ntp_monlist_absent": "test_ntp_monlist_absent()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L13 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_ntp_monlist_enabled": "test_ntp_monlist_enabled()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L8 | neighbors=[test_udp_amplifiers.py]
- "tests_test_udp_amplifiers_test_probe_builders_are_bytes": "test_probe_builders_are_bytes()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L31 | neighbors=[test_udp_amplifiers.py]
- "tests_test_use_cases_rationale_1": "Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only" | kind=entity | source=probe/tests/test_use_cases.py:L1 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_descriptions_do_not_overclaim": "test_descriptions_do_not_overclaim()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L16 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_iot_survey_collects_banners": "test_iot_survey_collects_banners()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L36 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_udp_claims_amplification": "test_udp_claims_amplification()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L27 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py]
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L23 | neighbors=[test_use_cases.py]
- "tests_test_validation_fakeclient_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_validation.py:L111 | neighbors=[FakeClient]
- "tests_test_validation_fakeclient_request": ".request()" | kind=code-symbol | source=probe/tests/test_validation.py:L115 | neighbors=[FakeClient]
- "tests_test_validation_test_parser_accepts_validate_command": "test_parser_accepts_validate_command()" | kind=code-symbol | source=probe/tests/test_validation.py:L254 | neighbors=[test_validation.py]
- "tests_test_validation_test_resolve_use_cases_deduplicates_combined_suites": "test_resolve_use_cases_deduplicates_combined_suites()" | kind=code-symbol | source=probe/tests/test_validation.py:L19 | neighbors=[test_validation.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-125.json

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
