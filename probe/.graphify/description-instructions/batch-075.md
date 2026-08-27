# Node Description Batch 76 of 92

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

- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_invalid_magic": ".test_parse_adb_header_invalid_magic()" | kind=code-symbol | source=tests/test_new_scanners.py:L555 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testmobilescanner_test_parse_adb_header_too_short": ".test_parse_adb_header_too_short()" | kind=code-symbol | source=tests/test_new_scanners.py:L560 | neighbors=[TestMobileScanner]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_long_form_one_byte": ".test_ber_len_long_form_one_byte()" | kind=code-symbol | source=tests/test_new_scanners.py:L47 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_long_form_two_bytes": ".test_ber_len_long_form_two_bytes()" | kind=code-symbol | source=tests/test_new_scanners.py:L52 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_len_short_form": ".test_ber_len_short_form()" | kind=code-symbol | source=tests/test_new_scanners.py:L41 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_parse_empty": ".test_ber_parse_empty()" | kind=code-symbol | source=tests/test_new_scanners.py:L65 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_ber_parse_two_tlvs": ".test_ber_parse_two_tlvs()" | kind=code-symbol | source=tests/test_new_scanners.py:L57 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_counter32": ".test_decode_value_counter32()" | kind=code-symbol | source=tests/test_new_scanners.py:L74 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_end_of_mib_view": ".test_decode_value_end_of_mib_view()" | kind=code-symbol | source=tests/test_new_scanners.py:L82 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_ip_address": ".test_decode_value_ip_address()" | kind=code-symbol | source=tests/test_new_scanners.py:L69 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_octet_string": ".test_decode_value_octet_string()" | kind=code-symbol | source=tests/test_new_scanners.py:L88 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_decode_value_timeticks": ".test_decode_value_timeticks()" | kind=code-symbol | source=tests/test_new_scanners.py:L78 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_encode_sysdescr_oid": ".test_encode_sysdescr_oid()" | kind=code-symbol | source=tests/test_new_scanners.py:L30 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_get_pdu_outer_tag": ".test_get_pdu_outer_tag()" | kind=code-symbol | source=tests/test_new_scanners.py:L92 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getbulk_pdu_tag_and_version": ".test_getbulk_pdu_tag_and_version()" | kind=code-symbol | source=tests/test_new_scanners.py:L103 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getnext_pdu_tag": ".test_getnext_pdu_tag()" | kind=code-symbol | source=tests/test_new_scanners.py:L98 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_in_subtree": ".test_oid_in_subtree()" | kind=code-symbol | source=tests/test_new_scanners.py:L109 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_roundtrip_sysdescr": ".test_oid_roundtrip_sysdescr()" | kind=code-symbol | source=tests/test_new_scanners.py:L35 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_teststablehostid_test_hostname_second_priority": ".test_hostname_second_priority()" | kind=code-symbol | source=tests/test_new_scanners.py:L343 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_ip_fallback": ".test_ip_fallback()" | kind=code-symbol | source=tests/test_new_scanners.py:L348 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_mac_normalises_dashes": ".test_mac_normalises_dashes()" | kind=code-symbol | source=tests/test_new_scanners.py:L338 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_mac_takes_priority": ".test_mac_takes_priority()" | kind=code-symbol | source=tests/test_new_scanners.py:L333 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_zero_mac_skipped": ".test_zero_mac_skipped()" | kind=code-symbol | source=tests/test_new_scanners.py:L353 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_header_fields": ".test_ike_probe_header_fields()" | kind=code-symbol | source=tests/test_new_scanners.py:L129 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_init_spi_not_zero": ".test_ike_probe_init_spi_not_zero()" | kind=code-symbol | source=tests/test_new_scanners.py:L137 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_length_field_matches_actual": ".test_ike_probe_length_field_matches_actual()" | kind=code-symbol | source=tests/test_new_scanners.py:L123 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_resp_spi_zero": ".test_ike_probe_resp_spi_zero()" | kind=code-symbol | source=tests/test_new_scanners.py:L142 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_short_data": ".test_interpret_ike_short_data()" | kind=code-symbol | source=tests/test_new_scanners.py:L162 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_v1": ".test_interpret_ike_v1()" | kind=code-symbol | source=tests/test_new_scanners.py:L155 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_v2": ".test_interpret_ike_v2()" | kind=code-symbol | source=tests/test_new_scanners.py:L147 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ipmi_not_supported": ".test_interpret_ipmi_not_supported()" | kind=code-symbol | source=tests/test_new_scanners.py:L217 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ipmi_supported_flag": ".test_interpret_ipmi_supported_flag()" | kind=code-symbol | source=tests/test_new_scanners.py:L209 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_sip_parses_server": ".test_interpret_sip_parses_server()" | kind=code-symbol | source=tests/test_new_scanners.py:L179 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_iana_enterprise": ".test_ipmi_probe_iana_enterprise()" | kind=code-symbol | source=tests/test_new_scanners.py:L199 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_length_and_version": ".test_ipmi_probe_length_and_version()" | kind=code-symbol | source=tests/test_new_scanners.py:L192 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_presence_ping_type": ".test_ipmi_probe_presence_ping_type()" | kind=code-symbol | source=tests/test_new_scanners.py:L205 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_memcached_unauth_stat": ".test_memcached_unauth_stat()" | kind=code-symbol | source=tests/test_new_scanners.py:L230 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ntp_monlist_mode7_detection": ".test_ntp_monlist_mode7_detection()" | kind=code-symbol | source=tests/test_new_scanners.py:L224 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_sip_probe_starts_with_options": ".test_sip_probe_starts_with_options()" | kind=code-symbol | source=tests/test_new_scanners.py:L166 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_sip_probe_target_in_headers": ".test_sip_probe_target_in_headers()" | kind=code-symbol | source=tests/test_new_scanners.py:L174 | neighbors=[TestUDPProbeConstruction]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-075.json

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
