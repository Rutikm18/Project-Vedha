# Node Description Batch 166 of 186

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

- "tests_test_nuclei_scanner_test_missing_binary_is_a_reported_failure": "test_missing_binary_is_a_reported_failure()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L95 | neighbors=[test_nuclei_scanner.py] | lang=en
- "tests_test_os_fingerprint_rationale_1": "test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +" | kind=entity | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[test_os_fingerprint.py] | lang=pt
- "tests_test_os_fingerprint_testfingerprintos_test_network_device_from_ttl_255": ".test_network_device_from_ttl_255()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L146 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_no_signals_is_unknown": ".test_no_signals_is_unknown()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L141 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_signals_recorded": ".test_signals_recorded()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L149 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_and_window_agree_boosts_confidence": ".test_ttl_and_window_agree_boosts_confidence()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L135 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_linux": ".test_ttl_only_linux()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L127 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_windows": ".test_ttl_only_windows()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L132 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_address_mask_request_type": ".test_address_mask_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L53 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_payload_preserved": ".test_echo_payload_preserved()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L44 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_request_type_and_checksum": ".test_echo_request_type_and_checksum()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L37 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_timestamp_request_type": ".test_timestamp_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L48 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpcapability_test_available_when_socket_ok": ".test_available_when_socket_ok()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L163 | neighbors=[TestIcmpCapability] | lang=en
- "tests_test_os_fingerprint_testicmpcapability_test_unavailable_when_socket_raises": ".test_unavailable_when_socket_raises()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L158 | neighbors=[TestIcmpCapability] | lang=en
- "tests_test_os_fingerprint_testicmpparse_test_parse_raw_icmp_without_ip_header": ".test_parse_raw_icmp_without_ip_header()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L81 | neighbors=[TestIcmpParse] | lang=en
- "tests_test_os_fingerprint_testicmpparse_test_parse_rejects_short": ".test_parse_rejects_short()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L78 | neighbors=[TestIcmpParse] | lang=en
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_handles_odd_length": ".test_checksum_handles_odd_length()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L30 | neighbors=[TestInetChecksum] | lang=en
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_verifies_to_zero": ".test_checksum_verifies_to_zero()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L24 | neighbors=[TestInetChecksum] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_hop_estimate": ".test_hop_estimate()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L107 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_linux": ".test_os_family_linux()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L111 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_network": ".test_os_family_network()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L117 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_unknown_on_none": ".test_os_family_unknown_on_none()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L120 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_os_family_windows": ".test_os_family_windows()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L114 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_128": ".test_round_up_to_128()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L99 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_255": ".test_round_up_to_255()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L103 | neighbors=[TestTtlInference] | lang=en
- "tests_test_os_fingerprint_testttlinference_test_round_up_to_64": ".test_round_up_to_64()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L95 | neighbors=[TestTtlInference] | lang=en
- "tests_test_passive_collector_socket_fileno": ".fileno()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L28 | neighbors=[_Socket] | lang=en
- "tests_test_passive_collector_socket_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L24 | neighbors=[_Socket] | lang=en
- "tests_test_passive_collector_test_zero_listeners_returns_structured_failure": "test_zero_listeners_returns_structured_failure()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L135 | neighbors=[test_passive_collector.py] | lang=en
- "tests_test_passive_collector_writer_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L16 | neighbors=[_Writer] | lang=en
- "tests_test_passive_collector_writer_write": ".write()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L19 | neighbors=[_Writer] | lang=en
- "tests_test_pat_auth_test_new_pat_token_shape_and_hash_stability": "test_new_pat_token_shape_and_hash_stability()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L44 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_rejects_unknown_scope": "test_pat_builder_rejects_unknown_scope()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L88 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_returns_token_once_and_stores_hash_only": "test_pat_builder_returns_token_once_and_stores_hash_only()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L52 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_builder_supports_non_expiring_tokens_only_when_requested": "test_pat_builder_supports_non_expiring_tokens_only_when_requested()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L74 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_scope_allows_probe_cli_paths": "test_pat_scope_allows_probe_cli_paths()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L16 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_pat_scope_matrix_for_api_scopes": "test_pat_scope_matrix_for_api_scopes()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L27 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_pat_auth_test_validate_pat_scopes_dedupes_and_rejects_unknown": "test_validate_pat_scopes_dedupes_and_rejects_unknown()" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L35 | neighbors=[test_pat_auth.py] | lang=en
- "tests_test_perf_optimization_rationale_1": "Tests for the P1+P2 performance optimization of the detection engine.  P1 — vers" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L1 | neighbors=[test_perf_optimization.py] | lang=en
- "tests_test_perf_optimization_rationale_27": "dpkg_compare must use the pure-Python comparator in the hot path.     Shelling o" | kind=entity | source=manager/detection_engine/tests/test_perf_optimization.py:L27 | neighbors=[test_dpkg_compare_does_not_call_the_bin…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-165.json

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
