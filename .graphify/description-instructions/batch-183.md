# Node Description Batch 184 of 209

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_missing_file": ".test_load_jsonl_missing_file()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L405 | neighbors=[TestDeltaEngine]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_header": ".test_coap_get_wellknown_header()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L278 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_path": ".test_coap_get_wellknown_path()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L284 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_205": ".test_coap_response_parse_205()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L290 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_404": ".test_coap_response_parse_404()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L297 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_short": ".test_coap_response_parse_short()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L303 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_clean_session_flag": ".test_mqtt_connect_clean_session_flag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L272 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_packet_structure": ".test_mqtt_connect_packet_structure()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L265 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_remaining_length_encoding": ".test_mqtt_remaining_length_encoding()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L258 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_ssdp_header_parsing_location": ".test_ssdp_header_parsing_location()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L248 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_empty": ".test_adb_checksum_empty()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L583 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_known_value": ".test_adb_checksum_known_value()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L587 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_checksum_matches": ".test_adb_cnxn_checksum_matches()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L529 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_command_field": ".test_adb_cnxn_command_field()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L517 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_magic_invariant": ".test_adb_cnxn_magic_invariant()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L523 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_contains_service_labels": ".test_mdns_query_contains_service_labels()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L571 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_googlecast": ".test_mdns_query_googlecast()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L578 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_one_question": ".test_mdns_query_one_question()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L566 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_transaction_id_zero": ".test_mdns_query_transaction_id_zero()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L561 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_auth": ".test_parse_adb_header_auth()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L545 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_cnxn": ".test_parse_adb_header_cnxn()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L536 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_invalid_magic": ".test_parse_adb_header_invalid_magic()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L552 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_too_short": ".test_parse_adb_header_too_short()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L557 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_long_form_one_byte": ".test_ber_len_long_form_one_byte()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L47 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_long_form_two_bytes": ".test_ber_len_long_form_two_bytes()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L52 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_short_form": ".test_ber_len_short_form()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L41 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_parse_empty": ".test_ber_parse_empty()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L65 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_parse_two_tlvs": ".test_ber_parse_two_tlvs()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L57 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_counter32": ".test_decode_value_counter32()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L74 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_end_of_mib_view": ".test_decode_value_end_of_mib_view()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L82 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_ip_address": ".test_decode_value_ip_address()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L69 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_octet_string": ".test_decode_value_octet_string()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L88 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_timeticks": ".test_decode_value_timeticks()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L78 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_encode_sysdescr_oid": ".test_encode_sysdescr_oid()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L30 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_get_pdu_outer_tag": ".test_get_pdu_outer_tag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L92 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getbulk_pdu_tag_and_version": ".test_getbulk_pdu_tag_and_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L103 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getnext_pdu_tag": ".test_getnext_pdu_tag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L98 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_in_subtree": ".test_oid_in_subtree()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L109 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_roundtrip_sysdescr": ".test_oid_roundtrip_sysdescr()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L35 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_teststablehostid_test_hostname_second_priority": ".test_hostname_second_priority()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L340 | neighbors=[TestStableHostId]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-183.json

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
