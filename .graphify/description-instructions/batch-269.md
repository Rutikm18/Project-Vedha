# Node Description Batch 270 of 332

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

- "tests_test_ai_engine_testhallucinationguard_test_drop_table_flagged": ".test_drop_table_flagged()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L135 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_safe_remediation_passes": ".test_safe_remediation_passes()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L139 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_validate_aggregate_confidence": ".test_validate_aggregate_confidence()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L143 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testhallucinationguard_test_validate_clean_text": ".test_validate_clean_text()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L152 | neighbors=[TestHallucinationGuard] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L49 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_fallback_score_capped": ".test_fallback_score_capped()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L88 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_starts_untrained": ".test_starts_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L52 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_engine_testvulnprioritizer_test_train_without_xgboost_raises": ".test_train_without_xgboost_raises()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L92 | neighbors=[TestVulnPrioritizer] | lang=en
- "tests_test_ai_normalizer_rationale_1": "Tests for ai_normalizer.py — 0% prior coverage.  Covers:   - extract_raw_text: p" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L1 | neighbors=[test_ai_normalizer.py] | lang=en
- "tests_test_ai_normalizer_rationale_155": "Any exception from the AI client yields [] — never raises, never         blocks" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L155 | neighbors=[.test_client_failure_returns_empty()] | lang=en
- "tests_test_ai_normalizer_rationale_168": "When the cache already has an answer, the client must not be called." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L168 | neighbors=[.test_cache_hit_bypasses_client()] | lang=en
- "tests_test_ai_normalizer_rationale_185": "A candidate dict without a 'product' key must be silently skipped." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L185 | neighbors=[.test_malformed_response_missing_produc…] | lang=pt
- "tests_test_ai_normalizer_rationale_194": "If the client returns something that isn't a list, return []." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L194 | neighbors=[.test_malformed_response_not_a_list_ret…] | lang=en
- "tests_test_ai_normalizer_rationale_206": "Every candidate produced by propose_candidates must be tagged         ai_assiste" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L206 | neighbors=[.test_ai_assisted_flag_set_on_candidate…] | lang=en
- "tests_test_ai_normalizer_rationale_219": "source_confidence on the resulting CPECandidate must match the         originati" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L219 | neighbors=[.test_source_confidence_propagated_from…] | lang=en
- "tests_test_ai_normalizer_rationale_231": "When the AI response includes a version, it lands on the candidate." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L231 | neighbors=[.test_version_propagated_when_present()] | lang=en
- "tests_test_ai_normalizer_rationale_243": "A candidate without a version key produces version_raw=None." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L243 | neighbors=[.test_version_none_when_absent()] | lang=pt
- "tests_test_ai_normalizer_rationale_253": "The result of a first successful client call must be stored in the         cache" | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L253 | neighbors=[.test_result_is_cached_after_first_call…] | lang=en
- "tests_test_ai_normalizer_rationale_96": "ssh_inventory facts have no banner-style text for the AI to normalise." | kind=entity | source=manager/detection_engine/tests/test_ai_normalizer.py:L96 | neighbors=[.test_ssh_inventory_returns_none()] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_cache_persists_across_instances": ".test_cache_persists_across_instances()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L134 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_get_returns_none_on_miss": ".test_get_returns_none_on_miss()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L124 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_key_is_content_hash_not_plaintext": ".test_key_is_content_hash_not_plaintext()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L141 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testainormalizercache_test_put_and_get_roundtrip": ".test_put_and_get_roundtrip()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L128 | neighbors=[TestAINormalizerCache] | lang=en
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_empty_for_unknown_text": ".test_returns_empty_for_unknown_text()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L114 | neighbors=[TestFakeAIClient] | lang=en
- "tests_test_ai_normalizer_testfakeaiclient_test_returns_registered_response": ".test_returns_registered_response()" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L110 | neighbors=[TestFakeAIClient] | lang=en
- "tests_test_async_udp_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L24 | neighbors=[_EchoProtocol] | lang=en
- "tests_test_async_udp_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L27 | neighbors=[_EchoProtocol] | lang=en
- "tests_test_async_udp_rationale_1": "test_async_udp.py — tests for the true-async UDP probe helper in scanner_base." | kind=entity | source=probe/tests/test_async_udp.py:L1 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_sinkprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L32 | neighbors=[_SinkProtocol] | lang=en
- "tests_test_async_udp_start_server": "_start_server()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L36 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_datagram_received_resolves_future_with_bytes": "test_datagram_received_resolves_future_with_bytes()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L77 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_error_received_connection_refused_maps_to_closed": "test_error_received_connection_refused_maps_to_closed()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L86 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_concurrency_all_complete": "test_probe_concurrency_all_complete()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L106 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_no_reply_returns_none_on_timeout": "test_probe_no_reply_returns_none_on_timeout()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L67 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_open_returns_exact_payload": "test_probe_open_returns_exact_payload()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L56 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_open_returns_reply_bytes": "test_probe_open_returns_reply_bytes()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L46 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_unbound_loopback_port_is_not_open": "test_probe_unbound_loopback_port_is_not_open()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L95 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_probe_unresolvable_host_returns_none": "test_probe_unresolvable_host_returns_none()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L126 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_udp_scanner_generic_probe_detects_unknown_responder": "test_udp_scanner_generic_probe_detects_unknown_responder()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L183 | neighbors=[test_async_udp.py] | lang=en
- "tests_test_async_udp_test_udp_scanner_generic_probe_unknown_port_silence_is_open_filtered": "test_udp_scanner_generic_probe_unknown_port_silence_is_open_filtered()" | kind=code-symbol | source=probe/tests/test_async_udp.py:L208 | neighbors=[test_async_udp.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-269.json

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
