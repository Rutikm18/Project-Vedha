# Node Description Batch 208 of 236

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

- "tests_test_new_scanners_testsnmpberutilities_test_encode_sysdescr_oid": ".test_encode_sysdescr_oid()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L30 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_get_pdu_outer_tag": ".test_get_pdu_outer_tag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L92 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getbulk_pdu_tag_and_version": ".test_getbulk_pdu_tag_and_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L103 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_getnext_pdu_tag": ".test_getnext_pdu_tag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L98 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_in_subtree": ".test_oid_in_subtree()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L109 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_testsnmpberutilities_test_oid_roundtrip_sysdescr": ".test_oid_roundtrip_sysdescr()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L35 | neighbors=[TestSNMPBerUtilities]
- "tests_test_new_scanners_teststablehostid_test_hostname_second_priority": ".test_hostname_second_priority()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L343 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_ip_fallback": ".test_ip_fallback()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L348 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_mac_normalises_dashes": ".test_mac_normalises_dashes()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L338 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_mac_takes_priority": ".test_mac_takes_priority()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L333 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_teststablehostid_test_zero_mac_skipped": ".test_zero_mac_skipped()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L353 | neighbors=[TestStableHostId]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_header_fields": ".test_ike_probe_header_fields()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L129 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_init_spi_not_zero": ".test_ike_probe_init_spi_not_zero()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L137 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_length_field_matches_actual": ".test_ike_probe_length_field_matches_actual()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L123 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ike_probe_resp_spi_zero": ".test_ike_probe_resp_spi_zero()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L142 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_short_data": ".test_interpret_ike_short_data()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L162 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_v1": ".test_interpret_ike_v1()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L155 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ike_v2": ".test_interpret_ike_v2()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L147 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ipmi_not_supported": ".test_interpret_ipmi_not_supported()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L217 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_ipmi_supported_flag": ".test_interpret_ipmi_supported_flag()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L209 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_interpret_sip_parses_server": ".test_interpret_sip_parses_server()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L179 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_iana_enterprise": ".test_ipmi_probe_iana_enterprise()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L199 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_length_and_version": ".test_ipmi_probe_length_and_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L192 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ipmi_probe_presence_ping_type": ".test_ipmi_probe_presence_ping_type()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L205 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_memcached_unauth_stat": ".test_memcached_unauth_stat()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L230 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_ntp_monlist_mode7_detection": ".test_ntp_monlist_mode7_detection()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L224 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_sip_probe_starts_with_options": ".test_sip_probe_starts_with_options()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L166 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_sip_probe_target_in_headers": ".test_sip_probe_target_in_headers()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L174 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_tftp_probe_opcode_rrq": ".test_tftp_probe_opcode_rrq()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L186 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_udp_probes_has_all_playbook_ports": ".test_udp_probes_has_all_playbook_ports()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L235 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testversionchange_test_different_versions": ".test_different_versions()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L363 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_empty_old_version": ".test_empty_old_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L371 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_same_version": ".test_same_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L367 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_whitespace_normalised": ".test_whitespace_normalised()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L375 | neighbors=[TestVersionChange]
- "tests_test_nmap_xml_safety_rationale_1": "test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti" | kind=entity | source=probe/tests/test_nmap_xml_safety.py:L1 | neighbors=[test_nmap_xml_safety.py]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_declaration_is_refused": ".test_entity_declaration_is_refused()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L28 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_guard_is_case_insensitive": ".test_entity_guard_is_case_insensitive()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L33 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_legitimate_doctype_output_still_parses": ".test_legitimate_doctype_output_still_parses()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L38 | neighbors=[TestNmapEntityGuard]
- "tests_test_notifications_rationale_1": "test_notifications.py — integration delivery fan-out (item 3 delivery worker)." | kind=entity | source=manager/backend/tests/test_notifications.py:L1 | neighbors=[test_notifications.py]
- "tests_test_notifications_testdeliver_test_dispatches_to_the_kind": ".test_dispatches_to_the_kind()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L14 | neighbors=[TestDeliver]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-207.json

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
