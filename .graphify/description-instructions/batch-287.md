# Node Description Batch 288 of 330

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

- "tests_test_nessus_scanner_test_authenticate_api_key": "test_authenticate_api_key()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L37 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_critical": "test_map_finding_critical()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L129 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_info_severity": "test_map_finding_info_severity()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L163 | neighbors=[test_nessus_scanner.py]
- "tests_test_nessus_scanner_test_map_finding_no_cvss": "test_map_finding_no_cvss()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L170 | neighbors=[test_nessus_scanner.py]
- "tests_test_network_va_accuracy_listener_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L29 | neighbors=[_Listener]
- "tests_test_network_va_accuracy_listener_serve": "._serve()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L57 | neighbors=[_Listener]
- "tests_test_network_va_accuracy_rationale_1": "test_network_va_accuracy.py — end-to-end accuracy of the network_va use case.  E" | kind=entity | source=probe/tests/test_network_va_accuracy.py:L1 | neighbors=[test_network_va_accuracy.py]
- "tests_test_network_va_accuracy_rationale_120": "The regression this guards: these ports were outside the 40-port catalog,     so" | kind=entity | source=probe/tests/test_network_va_accuracy.py:L120 | neighbors=[test_every_planted_risk_port_is_found()]
- "tests_test_network_va_accuracy_rationale_141": "Positive protocol evidence turns the botnet-C2 port guess into an     observatio" | kind=entity | source=probe/tests/test_network_va_accuracy.py:L141 | neighbors=[test_irc_is_identified_by_protocol_not_…]
- "tests_test_network_va_accuracy_rationale_157": "4444 says nothing. The scanner must record that, not invent a service." | kind=entity | source=probe/tests/test_network_va_accuracy.py:L157 | neighbors=[test_silent_port_reports_no_banner_hone…]
- "tests_test_network_va_accuracy_rationale_169": "Every deep branch that ran must have produced facts or have had a port to     ju" | kind=entity | source=probe/tests/test_network_va_accuracy.py:L169 | neighbors=[test_no_branch_runs_without_evidence()]
- "tests_test_network_va_accuracy_rationale_181": "service_banner now proves non-TLS by attempting a handshake, so silent     binar" | kind=entity | source=probe/tests/test_network_va_accuracy.py:L181 | neighbors=[test_tls_branch_is_not_routed_by_silenc…]
- "tests_test_network_va_accuracy_rationale_189": "network_va composes device classification and the exposure matrix." | kind=entity | source=probe/tests/test_network_va_accuracy.py:L189 | neighbors=[test_post_stages_ran()]
- "tests_test_network_va_accuracy_rationale_27": "A real TCP listener that optionally speaks first." | kind=entity | source=probe/tests/test_network_va_accuracy.py:L27 | neighbors=[_Listener]
- "tests_test_network_va_accuracy_rationale_79": "One real network_va against loopback with risk-catalog services listening." | kind=entity | source=probe/tests/test_network_va_accuracy.py:L79 | neighbors=[va_scan()]
- "tests_test_network_va_accuracy_test_etcd_is_identified_and_cpe_mapped": "test_etcd_is_identified_and_cpe_mapped()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L148 | neighbors=[test_network_va_accuracy.py]
- "tests_test_network_va_accuracy_test_named_risk_port_in_catalog": "test_named_risk_port_in_catalog()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L201 | neighbors=[test_network_va_accuracy.py]
- "tests_test_network_va_accuracy_test_risk_ports_are_in_the_it_catalog": "test_risk_ports_are_in_the_it_catalog()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L196 | neighbors=[test_network_va_accuracy.py]
- "tests_test_network_va_accuracy_test_scan_completed_without_errors": "test_scan_completed_without_errors()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L126 | neighbors=[test_network_va_accuracy.py]
- "tests_test_network_va_accuracy_test_shell_prompt_is_identified_as_a_shell": "test_shell_prompt_is_identified_as_a_shell()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L134 | neighbors=[test_network_va_accuracy.py]
- "tests_test_new_scanners_delta_engine": "delta_engine()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L326 | neighbors=[test_new_scanners.py]
- "tests_test_new_scanners_rationale_1": "test_new_scanners.py — unit tests for the five new/enhanced scanner modules.  Te" | kind=entity | source=probe/tests/test_new_scanners.py:L1 | neighbors=[test_new_scanners.py]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_missing_file": ".test_load_jsonl_missing_file()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L408 | neighbors=[TestDeltaEngine]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_header": ".test_coap_get_wellknown_header()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L281 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_get_wellknown_path": ".test_coap_get_wellknown_path()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L287 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_205": ".test_coap_response_parse_205()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L293 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_404": ".test_coap_response_parse_404()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L300 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_coap_response_parse_short": ".test_coap_response_parse_short()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L306 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_clean_session_flag": ".test_mqtt_connect_clean_session_flag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L275 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_connect_packet_structure": ".test_mqtt_connect_packet_structure()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L265 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_mqtt_remaining_length_encoding": ".test_mqtt_remaining_length_encoding()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L258 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testiotscanner_test_ssdp_header_parsing_location": ".test_ssdp_header_parsing_location()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L248 | neighbors=[TestIoTScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_empty": ".test_adb_checksum_empty()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L586 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_checksum_known_value": ".test_adb_checksum_known_value()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L590 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_checksum_matches": ".test_adb_cnxn_checksum_matches()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L532 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_command_field": ".test_adb_cnxn_command_field()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L520 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_adb_cnxn_magic_invariant": ".test_adb_cnxn_magic_invariant()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L526 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_contains_service_labels": ".test_mdns_query_contains_service_labels()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L574 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_googlecast": ".test_mdns_query_googlecast()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L581 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_mdns_query_one_question": ".test_mdns_query_one_question()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L569 | neighbors=[TestMobileScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-287.json

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
