# Node Description Batch 284 of 332

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_integration_rationale_315": "Simulate the full probe lifecycle from identity to result submission." | kind=entity | source=probe/tests/test_integration.py:L315 | neighbors=[.test_complete_flow_with_encrypted_scop…] | lang=en
- "tests_test_integration_rationale_383": "All targets outside scope → job is rejected cleanly." | kind=entity | source=probe/tests/test_integration.py:L383 | neighbors=[.test_job_rejected_all_targets_out_of_s…] | lang=en
- "tests_test_integration_rationale_409": "OT passive profile resolves correctly." | kind=entity | source=probe/tests/test_integration.py:L409 | neighbors=[.test_job_ot_passive_profile()] | lang=en
- "tests_test_integration_rationale_42": "Return a minimal valid scan result (no real network I/O)." | kind=entity | source=probe/tests/test_integration.py:L42 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_integration_rationale_432": "Phase 5: startup gauntlet checks." | kind=entity | source=probe/tests/test_integration.py:L432 | neighbors=[TestStartupGauntlet] | lang=en
- "tests_test_integration_rationale_435": "With LICENSE_ENFORCED=false, gauntlet returns None." | kind=entity | source=probe/tests/test_integration.py:L435 | neighbors=[.test_gauntlet_skips_in_dev_mode()] | lang=en
- "tests_test_integration_rationale_443": "Wrong HW fingerprint blocks startup." | kind=entity | source=probe/tests/test_integration.py:L443 | neighbors=[.test_gauntlet_hw_bind_blocks()] | lang=en
- "tests_test_integration_rationale_65": "Phase 4: identity generation + scope encryption roundtrip." | kind=entity | source=probe/tests/test_integration.py:L65 | neighbors=[TestIdentityAndEncryption] | lang=en
- "tests_test_integration_rationale_68": "Generate identity → encrypt scope → decrypt scope." | kind=entity | source=probe/tests/test_integration.py:L68 | neighbors=[.test_full_identity_lifecycle()] | lang=en
- "tests_test_integration_rationale_79": "Manager encrypts → probe decrypts." | kind=entity | source=probe/tests/test_integration.py:L79 | neighbors=[.test_scope_encryption_roundtrip()] | lang=en
- "tests_test_integration_rationale_92": "A different probe cannot decrypt scope meant for another probe." | kind=entity | source=probe/tests/test_integration.py:L92 | neighbors=[.test_different_key_cannot_decrypt()] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_spool_persists_and_flushes": ".test_spool_persists_and_flushes()" | kind=code-symbol | source=probe/tests/test_integration.py:L200 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_exhausts_retries": ".test_submit_exhausts_retries()" | kind=code-symbol | source=probe/tests/test_integration.py:L227 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testresultspoolwithretry_test_submit_retries_on_failure": ".test_submit_retries_on_failure()" | kind=code-symbol | source=probe/tests/test_integration.py:L216 | neighbors=[TestResultSpoolWithRetry] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_accepts_in_scope_rejects_out_of_scope": ".test_accepts_in_scope_rejects_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L168 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_all_excluded_returns_empty": ".test_all_excluded_returns_empty()" | kind=code-symbol | source=probe/tests/test_integration.py:L190 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_excludes_override_scope": ".test_excludes_override_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L174 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testscopevalidationpipeline_test_merge_exclusions_deduplicates": ".test_merge_exclusions_deduplicates()" | kind=code-symbol | source=probe/tests/test_integration.py:L184 | neighbors=[TestScopeValidationPipeline] | lang=en
- "tests_test_integration_testtransportwithidentity_test_register_sends_public_key": ".test_register_sends_public_key()" | kind=code-symbol | source=probe/tests/test_integration.py:L241 | neighbors=[TestTransportWithIdentity] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_heartbeat_message": ".test_heartbeat_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L306 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integrations_rationale_1": "test_integrations.py — operator notification-integration config (item 3)." | kind=entity | source=manager/backend/tests/test_integrations.py:L1 | neighbors=[test_integrations.py] | lang=en
- "tests_test_ipmi_scanner_rationale_1": "test_ipmi_scanner.py — IPMI 2.0 cipher-zero auth-bypass detection.  Byte-exact R" | kind=entity | source=probe/tests/test_ipmi_scanner.py:L1 | neighbors=[test_ipmi_scanner.py] | lang=en
- "tests_test_ipmi_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L77 | neighbors=[TestParity] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_open_session_request_offers_cipher_zero": ".test_open_session_request_offers_cipher_zero()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L24 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_parse_rejects_non_response": ".test_parse_rejects_non_response()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L39 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipv6_discovery_rationale_1": "test_ipv6_discovery.py — FIX 3: IPv6 neighbor discovery (RFC 4861 ND multicast)." | kind=entity | source=probe/tests/test_ipv6_discovery.py:L1 | neighbors=[test_ipv6_discovery.py] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_ignores_non_ipv6_lines": ".test_ignores_non_ipv6_lines()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L33 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ip_neigh_linux": ".test_parse_ip_neigh_linux()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L24 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ndp_macos": ".test_parse_ndp_macos()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L14 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_wiring_rationale_1": "test_ipv6_wiring.py — IPv6 neighbour discovery inside the engagement.  An IPv4 /" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L1 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_rationale_111": "The core restraint: discovery must not widen authorization." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L111 | neighbors=[test_out_of_scope_neighbour_is_reported…] | lang=en
- "tests_test_ipv6_wiring_rationale_137": "Only the scan types that opt in pay for the multicast ping." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L137 | neighbors=[test_disabled_by_default()] | lang=en
- "tests_test_ipv6_wiring_rationale_28": "The neighbour cache is system-wide. Pinging en0 and then harvesting every     in" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L28 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_test_component_is_in_the_catalog": "test_component_is_in_the_catalog()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L160 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_network_va_opts_in": "test_network_va_opts_in()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L172 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_planned_only_when_enabled": "test_planned_only_when_enabled()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L164 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_stub": "._stub()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L42 | neighbors=[TestInterfaceScoping] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-283.json

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
