# Node Description Batch 154 of 186

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

- "tests_test_ai_normalizer_testainormalizercache_test_get_returns_none_on_miss": ".test_get_returns_none_on_miss()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L124 | neighbors=[TestAINormalizerCache]
- "tests_test_ai_normalizer_testainormalizercache_test_key_is_content_hash_not_plaintext": ".test_key_is_content_hash_not_plaintext()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L141 | neighbors=[TestAINormalizerCache]
- "tests_test_ai_normalizer_testainormalizercache_test_put_and_get_roundtrip": ".test_put_and_get_roundtrip()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L128 | neighbors=[TestAINormalizerCache]
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_empty_for_unknown_text": ".test_returns_empty_for_unknown_text()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L114 | neighbors=[TestFakeAIClient]
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_registered_response": ".test_returns_registered_response()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L110 | neighbors=[TestFakeAIClient]
- "tests_test_async_udp_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L24 | neighbors=[_EchoProtocol]
- "tests_test_async_udp_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L27 | neighbors=[_EchoProtocol]
- "tests_test_async_udp_rationale_1": "test_async_udp.py — tests for the true-async UDP probe helper in scanner_base." | kind=entity | source=probe/tests/test_async_udp.py:L1 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_sinkprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L32 | neighbors=[_SinkProtocol]
- "tests_test_async_udp_start_server": "_start_server()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L36 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_datagram_received_resolves_future_with_bytes": "test_datagram_received_resolves_future_with_bytes()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L77 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_error_received_connection_refused_maps_to_closed": "test_error_received_connection_refused_maps_to_closed()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L86 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_concurrency_all_complete": "test_probe_concurrency_all_complete()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L106 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_no_reply_returns_none_on_timeout": "test_probe_no_reply_returns_none_on_timeout()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L67 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_open_returns_exact_payload": "test_probe_open_returns_exact_payload()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L56 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_open_returns_reply_bytes": "test_probe_open_returns_reply_bytes()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L46 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_unbound_loopback_port_is_not_open": "test_probe_unbound_loopback_port_is_not_open()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L95 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_probe_unresolvable_host_returns_none": "test_probe_unresolvable_host_returns_none()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L126 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_maps_closed_sentinel_to_closed_status": "test_udp_scanner_maps_closed_sentinel_to_closed_status()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L138 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_probe_filtered_on_timeout": "test_udp_scanner_probe_filtered_on_timeout()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L183 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_probe_open_filtered_on_timeout": "test_udp_scanner_probe_open_filtered_on_timeout()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L183 | neighbors=[test_async_udp.py]
- "tests_test_async_udp_test_udp_scanner_probe_open_status_via_event_loop": "test_udp_scanner_probe_open_status_via_event_loop()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L160 | neighbors=[test_async_udp.py]
- "tests_test_attack_paths_built_graph": "built_graph()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L39 | neighbors=[test_attack_paths.py]
- "tests_test_attack_paths_demo": "demo()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L34 | neighbors=[test_attack_paths.py]
- "tests_test_attack_paths_testgraphbuilder_test_asset_node_attributes": ".test_asset_node_attributes()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L59 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_connects_to_and_same_segment_edges": ".test_connects_to_and_same_segment_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L77 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_credential_reuse_edges": ".test_credential_reuse_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L82 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_complexity_falls_back_to_severity": ".test_exploit_complexity_falls_back_to_severity()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L102 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_complexity_from_vector": ".test_exploit_complexity_from_vector()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L95 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_exploit_edges_only_for_exploitable": ".test_exploit_edges_only_for_exploitable()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L70 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_has_service_and_has_finding_edges": ".test_has_service_and_has_finding_edges()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L65 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_is_internet_exposed": ".test_is_internet_exposed()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L87 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphbuilder_test_nodes_and_edges_created": ".test_nodes_and_edges_created()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L54 | neighbors=[TestGraphBuilder]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_highlights_top_path": ".test_d3_highlights_top_path()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L202 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_marks_compromised": ".test_d3_marks_compromised()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L197 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_d3_shape": ".test_d3_shape()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L187 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testgraphvisualizer_test_layout_is_deterministic": ".test_layout_is_deterministic()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L210 | neighbors=[TestGraphVisualizer]
- "tests_test_attack_paths_testneo4jclient_test_run_without_connection_returns_empty": ".test_run_without_connection_returns_empty()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L222 | neighbors=[TestNeo4jClient]
- "tests_test_attack_paths_testneo4jclient_test_run_write_noop_without_connection": ".test_run_write_noop_without_connection()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L226 | neighbors=[TestNeo4jClient]
- "tests_test_attack_paths_testneo4jclient_test_sync_to_neo4j_noop_without_client": ".test_sync_to_neo4j_noop_without_client()" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L230 | neighbors=[TestNeo4jClient]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-153.json

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
