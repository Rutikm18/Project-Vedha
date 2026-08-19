# Node Description Batch 199 of 227

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

- "tests_test_main_scripts_ja4s_test_ja4s_from_fields_shape_and_parts": "test_ja4s_from_fields_shape_and_parts()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L31 | neighbors=[test_main_scripts_ja4s.py]
- "tests_test_main_scripts_ja4s_test_suspicious_ja4s_finding_fires_only_on_match": "test_suspicious_ja4s_finding_fires_only_on_match()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L78 | neighbors=[test_main_scripts_ja4s.py]
- "tests_test_main_scripts_ja4s_test_version_and_alpn_encodings": "test_version_and_alpn_encodings()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L40 | neighbors=[test_main_scripts_ja4s.py]
- "tests_test_main_scripts_ja4x_rationale_1": "test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa" | kind=entity | source=probe/tests/test_main_scripts_ja4x.py:L1 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_empty_list_hashes_to_sentinel": "test_empty_list_hashes_to_sentinel()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L38 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_ja4x_format_is_three_12hex_fields": "test_ja4x_format_is_three_12hex_fields()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L30 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_ja4x_from_cert_handles_garbage": "test_ja4x_from_cert_handles_garbage()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L65 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_ja4x_is_deterministic_and_order_sensitive": "test_ja4x_is_deterministic_and_order_sensitive()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L43 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_match_suspicious_registry": "test_match_suspicious_registry()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L94 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_oid_to_hex_known_values": "test_oid_to_hex_known_values()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L21 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_real_self_signed_cert_round_trip": "test_real_self_signed_cert_round_trip()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L72 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_self_signed_finding_carries_ja4x_for_correlation": "test_self_signed_finding_carries_ja4x_for_correlation()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L123 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_ja4x_test_suspicious_fingerprint_finding_fires_only_on_match": "test_suspicious_fingerprint_finding_fires_only_on_match()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L104 | neighbors=[test_main_scripts_ja4x.py]
- "tests_test_main_scripts_rdp_rationale_1": "test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec" | kind=entity | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[test_main_scripts_rdp.py]
- "tests_test_main_scripts_rdp_rationale_16": "A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU." | kind=entity | source=probe/tests/test_main_scripts_rdp.py:L16 | neighbors=[_cc()]
- "tests_test_main_scripts_rdp_test_connection_request_is_valid_tpkt_and_requests_protocols": "test_connection_request_is_valid_tpkt_and_requests_protocols()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L23 | neighbors=[test_main_scripts_rdp.py]
- "tests_test_main_scripts_rdp_test_non_rdp_data_is_none": "test_non_rdp_data_is_none()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L58 | neighbors=[test_main_scripts_rdp.py]
- "tests_test_main_scripts_statemodel_rationale_1": "test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model" | kind=entity | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_backward_compatible_old_style_construction_still_works": "test_backward_compatible_old_style_construction_still_works()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L57 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_canonical_states_are_the_six_documented_states": "test_canonical_states_are_the_six_documented_states()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L16 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_explicit_first_class_value_wins_over_data": "test_explicit_first_class_value_wins_over_data()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L41 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_semantics_in_data_are_promoted_to_first_class_non_destructively": "test_semantics_in_data_are_promoted_to_first_class_non_destructively()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L30 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_state_and_reason_are_separate_first_class_fields": "test_state_and_reason_are_separate_first_class_fields()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L23 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_to_json_exposes_promoted_fields_and_round_trips": "test_to_json_exposes_promoted_fields_and_round_trips()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L47 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_unauth_rationale_1": "test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive" | kind=entity | source=probe/tests/test_main_scripts_unauth.py:L1 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_couchdb_and_memcached_and_mongodb": "test_couchdb_and_memcached_and_mongodb()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L33 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_elasticsearch_unauth_vs_secured": "test_elasticsearch_unauth_vs_secured()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L26 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_non_datastore_service_is_unknown": "test_non_datastore_service_is_unknown()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L39 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_rce_capability_flag": "test_rce_capability_flag()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L45 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_noauth_is_protected": "test_redis_noauth_is_protected()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L17 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_silent_is_unknown": "test_redis_silent_is_unknown()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L21 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_unauth_info_leak_is_true": "test_redis_unauth_info_leak_is_true()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L12 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_vantage_rationale_1": "test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ \"Multi-vantag" | kind=entity | source=probe/tests/test_main_scripts_vantage.py:L1 | neighbors=[test_main_scripts_vantage.py]
- "tests_test_manager_ai_rationale_233": "Settings with provider unset and all cloud keys pinned, so .env cannot     leak" | kind=entity | source=manager/backend/tests/test_manager_ai.py:L233 | neighbors=[_cloud()]
- "tests_test_manager_ai_test_ai_request_rejects_unsafe_model_and_oversized_context": "test_ai_request_rejects_unsafe_model_and_oversized_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L214 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_ollama_generation_owns_security_prompt_and_context": "test_manager_ollama_generation_owns_security_prompt_and_context()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L13 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_generation_is_server_side": "test_manager_openai_generation_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L82 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openai_rejects_unconfigured_and_unenabled_model": "test_manager_openai_rejects_unconfigured_and_unenabled_model()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L114 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_openrouter_free_selection_is_server_side": "test_manager_openrouter_free_selection_is_server_side()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L51 | neighbors=[test_manager_ai.py]
- "tests_test_manager_ai_test_manager_rejects_cloud_model_not_enabled_by_deployment": "test_manager_rejects_cloud_model_not_enabled_by_deployment()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L150 | neighbors=[test_manager_ai.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-198.json

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
