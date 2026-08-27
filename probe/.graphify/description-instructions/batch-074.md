# Node Description Batch 75 of 92

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

- "tests_test_main_scripts_rdp_test_non_rdp_data_is_none": "test_non_rdp_data_is_none()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L58 | neighbors=[test_main_scripts_rdp.py]
- "tests_test_main_scripts_statemodel_rationale_1": "test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model" | kind=entity | source=tests/test_main_scripts_statemodel.py:L1 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_backward_compatible_old_style_construction_still_works": "test_backward_compatible_old_style_construction_still_works()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L57 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_canonical_states_are_the_six_documented_states": "test_canonical_states_are_the_six_documented_states()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L16 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_explicit_first_class_value_wins_over_data": "test_explicit_first_class_value_wins_over_data()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L41 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_semantics_in_data_are_promoted_to_first_class_non_destructively": "test_semantics_in_data_are_promoted_to_first_class_non_destructively()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L30 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_state_and_reason_are_separate_first_class_fields": "test_state_and_reason_are_separate_first_class_fields()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L23 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_statemodel_test_to_json_exposes_promoted_fields_and_round_trips": "test_to_json_exposes_promoted_fields_and_round_trips()" | kind=code-symbol | source=tests/test_main_scripts_statemodel.py:L47 | neighbors=[test_main_scripts_statemodel.py]
- "tests_test_main_scripts_unauth_rationale_1": "test_main_scripts_unauth.py — proven unauthenticated datastore access (offensive" | kind=entity | source=tests/test_main_scripts_unauth.py:L1 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_couchdb_and_memcached_and_mongodb": "test_couchdb_and_memcached_and_mongodb()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L33 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_elasticsearch_unauth_vs_secured": "test_elasticsearch_unauth_vs_secured()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L26 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_non_datastore_service_is_unknown": "test_non_datastore_service_is_unknown()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L39 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_rce_capability_flag": "test_rce_capability_flag()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L45 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_noauth_is_protected": "test_redis_noauth_is_protected()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L17 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_silent_is_unknown": "test_redis_silent_is_unknown()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L21 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_unauth_test_redis_unauth_info_leak_is_true": "test_redis_unauth_info_leak_is_true()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L12 | neighbors=[test_main_scripts_unauth.py]
- "tests_test_main_scripts_vantage_rationale_1": "test_main_scripts_vantage.py — multi-vantage reconciliation (P0+++ \"Multi-vantag" | kind=entity | source=tests/test_main_scripts_vantage.py:L1 | neighbors=[test_main_scripts_vantage.py]
- "tests_test_new_scanners_delta_engine": "delta_engine()" | kind=code-symbol | source=tests/test_new_scanners.py:L326 | neighbors=[test_new_scanners.py]
- "tests_test_new_scanners_rationale_1": "test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te" | kind=entity | source=tests/test_new_scanners.py:L1 | neighbors=[test_new_scanners.py]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_missing_file": ".test_load_jsonl_missing_file()" | kind=code-symbol | source=tests/test_new_scanners.py:L408 | neighbors=[TestDeltaEngine]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_header": ".test_coap_get_wellknown_header()" | kind=code-symbol | source=tests/test_new_scanners.py:L281 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_path": ".test_coap_get_wellknown_path()" | kind=code-symbol | source=tests/test_new_scanners.py:L287 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_205": ".test_coap_response_parse_205()" | kind=code-symbol | source=tests/test_new_scanners.py:L293 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_404": ".test_coap_response_parse_404()" | kind=code-symbol | source=tests/test_new_scanners.py:L300 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_short": ".test_coap_response_parse_short()" | kind=code-symbol | source=tests/test_new_scanners.py:L306 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_clean_session_flag": ".test_mqtt_connect_clean_session_flag()" | kind=code-symbol | source=tests/test_new_scanners.py:L275 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_packet_structure": ".test_mqtt_connect_packet_structure()" | kind=code-symbol | source=tests/test_new_scanners.py:L265 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_remaining_length_encoding": ".test_mqtt_remaining_length_encoding()" | kind=code-symbol | source=tests/test_new_scanners.py:L258 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_ssdp_header_parsing_location": ".test_ssdp_header_parsing_location()" | kind=code-symbol | source=tests/test_new_scanners.py:L248 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_empty": ".test_adb_checksum_empty()" | kind=code-symbol | source=tests/test_new_scanners.py:L586 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_known_value": ".test_adb_checksum_known_value()" | kind=code-symbol | source=tests/test_new_scanners.py:L590 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_checksum_matches": ".test_adb_cnxn_checksum_matches()" | kind=code-symbol | source=tests/test_new_scanners.py:L532 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_command_field": ".test_adb_cnxn_command_field()" | kind=code-symbol | source=tests/test_new_scanners.py:L520 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_magic_invariant": ".test_adb_cnxn_magic_invariant()" | kind=code-symbol | source=tests/test_new_scanners.py:L526 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_contains_service_labels": ".test_mdns_query_contains_service_labels()" | kind=code-symbol | source=tests/test_new_scanners.py:L574 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_googlecast": ".test_mdns_query_googlecast()" | kind=code-symbol | source=tests/test_new_scanners.py:L581 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_one_question": ".test_mdns_query_one_question()" | kind=code-symbol | source=tests/test_new_scanners.py:L569 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_transaction_id_zero": ".test_mdns_query_transaction_id_zero()" | kind=code-symbol | source=tests/test_new_scanners.py:L564 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_auth": ".test_parse_adb_header_auth()" | kind=code-symbol | source=tests/test_new_scanners.py:L548 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_cnxn": ".test_parse_adb_header_cnxn()" | kind=code-symbol | source=tests/test_new_scanners.py:L539 | neighbors=[TestMobileScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-074.json

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
