# Node Description Batch 70 of 92

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

- "tests_test_async_udp_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=tests/test_async_udp.py:L24 | neighbors=[_EchoProtocol]
- "tests_test_async_udp_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=tests/test_async_udp.py:L27 | neighbors=[_EchoProtocol]
- "tests_test_async_udp_rationale_1": "test_async_udp.py — tests for the true-async UDP probe helper in scanner_base." | kind=entity | source=tests/test_async_udp.py:L1 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_sinkprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=tests/test_async_udp.py:L32 | neighbors=[_SinkProtocol]
- "tests_test_async_udp_start_server": "_start_server()" | kind=code-symbol | source=tests/test_async_udp.py:L36 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_datagram_received_resolves_future_with_bytes": "test_datagram_received_resolves_future_with_bytes()" | kind=code-symbol | source=tests/test_async_udp.py:L77 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_error_received_connection_refused_maps_to_closed": "test_error_received_connection_refused_maps_to_closed()" | kind=code-symbol | source=tests/test_async_udp.py:L86 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_concurrency_all_complete": "test_probe_concurrency_all_complete()" | kind=code-symbol | source=tests/test_async_udp.py:L106 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_no_reply_returns_none_on_timeout": "test_probe_no_reply_returns_none_on_timeout()" | kind=code-symbol | source=tests/test_async_udp.py:L67 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_open_returns_exact_payload": "test_probe_open_returns_exact_payload()" | kind=code-symbol | source=tests/test_async_udp.py:L56 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_open_returns_reply_bytes": "test_probe_open_returns_reply_bytes()" | kind=code-symbol | source=tests/test_async_udp.py:L46 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_unbound_loopback_port_is_not_open": "test_probe_unbound_loopback_port_is_not_open()" | kind=code-symbol | source=tests/test_async_udp.py:L95 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_unresolvable_host_returns_none": "test_probe_unresolvable_host_returns_none()" | kind=code-symbol | source=tests/test_async_udp.py:L126 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_maps_closed_sentinel_to_closed_status": "test_udp_scanner_maps_closed_sentinel_to_closed_status()" | kind=code-symbol | source=tests/test_async_udp.py:L138 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_probe_open_filtered_on_timeout": "test_udp_scanner_probe_open_filtered_on_timeout()" | kind=code-symbol | source=tests/test_async_udp.py:L183 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_probe_open_status_via_event_loop": "test_udp_scanner_probe_open_status_via_event_loop()" | kind=code-symbol | source=tests/test_async_udp.py:L160 | neighbors=[test_async_udp.py]
- "tests_test_cli_fakeclient_init": ".__init__()" | kind=code-symbol | source=tests/test_cli.py:L153 | neighbors=[FakeClient]
- "tests_test_cli_fakeclient_request": ".request()" | kind=code-symbol | source=tests/test_cli.py:L157 | neighbors=[FakeClient]
- "tests_test_cli_test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity": "test_cmd_daemon_run_overrides_stale_env_and_sets_probe_identity()" | kind=code-symbol | source=tests/test_cli.py:L318 | neighbors=[test_cli.py]
- "tests_test_cli_test_cmd_doctor_fails_when_no_agent_unless_allowed": "test_cmd_doctor_fails_when_no_agent_unless_allowed()" | kind=code-symbol | source=tests/test_cli.py:L248 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_malformed_json": "test_config_store_rejects_malformed_json()" | kind=code-symbol | source=tests/test_cli.py:L31 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_rejects_non_object_profiles": "test_config_store_rejects_non_object_profiles()" | kind=code-symbol | source=tests/test_cli.py:L38 | neighbors=[test_cli.py]
- "tests_test_cli_test_config_store_writes_private_file": "test_config_store_writes_private_file()" | kind=code-symbol | source=tests/test_cli.py:L13 | neighbors=[test_cli.py]
- "tests_test_cli_test_normalize_manager_url_trims_and_validates": "test_normalize_manager_url_trims_and_validates()" | kind=code-symbol | source=tests/test_cli.py:L72 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_rejects_missing_equals": "test_parse_param_pairs_rejects_missing_equals()" | kind=code-symbol | source=tests/test_cli.py:L59 | neighbors=[test_cli.py]
- "tests_test_cli_test_parse_param_pairs_supports_json_values": "test_parse_param_pairs_supports_json_values()" | kind=code-symbol | source=tests/test_cli.py:L45 | neighbors=[test_cli.py]
- "tests_test_cli_test_parser_accepts_json_after_concrete_commands": "test_parser_accepts_json_after_concrete_commands()" | kind=code-symbol | source=tests/test_cli.py:L80 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_env_overrides_config": "test_resolve_profile_env_overrides_config()" | kind=code-symbol | source=tests/test_cli.py:L106 | neighbors=[test_cli.py]
- "tests_test_cli_test_resolve_profile_reports_missing_manager_or_token": "test_resolve_profile_reports_missing_manager_or_token()" | kind=code-symbol | source=tests/test_cli.py:L134 | neighbors=[test_cli.py]
- "tests_test_cli_test_split_values_accepts_repeated_and_csv_values": "test_split_values_accepts_repeated_and_csv_values()" | kind=code-symbol | source=tests/test_cli.py:L64 | neighbors=[test_cli.py]
- "tests_test_db_scanner_fakereader_init": ".__init__()" | kind=code-symbol | source=tests/test_db_scanner.py:L18 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakereader_read": ".read()" | kind=code-symbol | source=tests/test_db_scanner.py:L21 | neighbors=[FakeReader]
- "tests_test_db_scanner_fakewriter_drain": ".drain()" | kind=code-symbol | source=tests/test_db_scanner.py:L29 | neighbors=[FakeWriter]
- "tests_test_db_scanner_fakewriter_write": ".write()" | kind=code-symbol | source=tests/test_db_scanner.py:L26 | neighbors=[FakeWriter]
- "tests_test_db_scanner_rationale_1": "Regression tests for db_scanner fingerprint matchers.  Focus: MySQL X Protocol (" | kind=entity | source=tests/test_db_scanner.py:L1 | neighbors=[test_db_scanner.py]
- "tests_test_db_unauth_test_redis_authenticated": "test_redis_authenticated()" | kind=code-symbol | source=tests/test_db_unauth.py:L11 | neighbors=[test_db_unauth.py]
- "tests_test_db_unauth_test_redis_unauthenticated": "test_redis_unauthenticated()" | kind=code-symbol | source=tests/test_db_unauth.py:L4 | neighbors=[test_db_unauth.py]
- "tests_test_device_identity_test_device_identity_rejects_invalid_private_key_encoding": "test_device_identity_rejects_invalid_private_key_encoding()" | kind=code-symbol | source=tests/test_device_identity.py:L36 | neighbors=[test_device_identity.py]
- "tests_test_device_identity_test_device_identity_round_trip_and_signature_proof": "test_device_identity_round_trip_and_signature_proof()" | kind=code-symbol | source=tests/test_device_identity.py:L21 | neighbors=[test_device_identity.py]
- "tests_test_device_identity_test_site_policy_signature_and_tofu_pin_are_enforced": "test_site_policy_signature_and_tofu_pin_are_enforced()" | kind=code-symbol | source=tests/test_device_identity.py:L41 | neighbors=[test_device_identity.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-069.json

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
