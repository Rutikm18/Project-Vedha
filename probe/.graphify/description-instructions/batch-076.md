# Node Description Batch 77 of 92

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
Write every description in Portuguese (pt). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_new_scanners_testudpprobeconstruction_test_tftp_probe_opcode_rrq": ".test_tftp_probe_opcode_rrq()" | kind=code-symbol | source=tests/test_new_scanners.py:L186 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testudpprobeconstruction_test_udp_probes_has_all_playbook_ports": ".test_udp_probes_has_all_playbook_ports()" | kind=code-symbol | source=tests/test_new_scanners.py:L235 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testversionchange_test_different_versions": ".test_different_versions()" | kind=code-symbol | source=tests/test_new_scanners.py:L363 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_empty_old_version": ".test_empty_old_version()" | kind=code-symbol | source=tests/test_new_scanners.py:L371 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_same_version": ".test_same_version()" | kind=code-symbol | source=tests/test_new_scanners.py:L367 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_whitespace_normalised": ".test_whitespace_normalised()" | kind=code-symbol | source=tests/test_new_scanners.py:L375 | neighbors=[TestVersionChange]
- "tests_test_nmap_xml_safety_rationale_1": "test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti" | kind=entity | source=tests/test_nmap_xml_safety.py:L1 | neighbors=[test_nmap_xml_safety.py]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_declaration_is_refused": ".test_entity_declaration_is_refused()" | kind=code-symbol | source=tests/test_nmap_xml_safety.py:L28 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_guard_is_case_insensitive": ".test_entity_guard_is_case_insensitive()" | kind=code-symbol | source=tests/test_nmap_xml_safety.py:L33 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_legitimate_doctype_output_still_parses": ".test_legitimate_doctype_output_still_parses()" | kind=code-symbol | source=tests/test_nmap_xml_safety.py:L38 | neighbors=[TestNmapEntityGuard]
- "tests_test_os_fingerprint_rationale_1": "test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +" | kind=entity | source=tests/test_os_fingerprint.py:L1 | neighbors=[test_os_fingerprint.py]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_none_parsed": ".test_rejects_none_parsed()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L183 | neighbors=[TestAcceptEchoReply]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_jumbo_even_without_os_signal": ".test_mss_flags_jumbo_even_without_os_signal()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L260 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_tunnel_or_vpn": ".test_mss_flags_tunnel_or_vpn()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L256 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_is_path_intel_not_an_os_signal": ".test_mss_is_path_intel_not_an_os_signal()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L263 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_yields_ethernet_mtu": ".test_mss_yields_ethernet_mtu()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L252 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_network_device_from_ttl_255": ".test_network_device_from_ttl_255()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L244 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_no_signals_is_unknown": ".test_no_signals_is_unknown()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L239 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_signals_recorded": ".test_signals_recorded()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L247 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_and_window_agree_boosts_confidence": ".test_ttl_and_window_agree_boosts_confidence()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L233 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_linux": ".test_ttl_only_linux()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L225 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_windows": ".test_ttl_only_windows()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L230 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testicmpbuilders_test_address_mask_request_type": ".test_address_mask_request_type()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L54 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_payload_preserved": ".test_echo_payload_preserved()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L45 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_request_type_and_checksum": ".test_echo_request_type_and_checksum()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L38 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_timestamp_request_type": ".test_timestamp_request_type()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L49 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpcapability_test_available_when_socket_ok": ".test_available_when_socket_ok()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L276 | neighbors=[TestIcmpCapability]
- "tests_test_os_fingerprint_testicmpcapability_test_unavailable_when_socket_raises": ".test_unavailable_when_socket_raises()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L271 | neighbors=[TestIcmpCapability]
- "tests_test_os_fingerprint_testicmpparse_test_parse_raw_icmp_without_ip_header": ".test_parse_raw_icmp_without_ip_header()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L82 | neighbors=[TestIcmpParse]
- "tests_test_os_fingerprint_testicmpparse_test_parse_rejects_short": ".test_parse_rejects_short()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L79 | neighbors=[TestIcmpParse]
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_rejects_short_body": ".test_parse_rejects_short_body()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L118 | neighbors=[TestIcmpTimestamps]
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_handles_odd_length": ".test_checksum_handles_odd_length()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L31 | neighbors=[TestInetChecksum]
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_verifies_to_zero": ".test_checksum_verifies_to_zero()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L25 | neighbors=[TestInetChecksum]
- "tests_test_os_fingerprint_testremoteclock_test_high_bit_marks_nonstandard_clock": ".test_high_bit_marks_nonstandard_clock()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L132 | neighbors=[TestRemoteClock]
- "tests_test_os_fingerprint_testremoteclock_test_standard_value_decodes_to_wall_clock": ".test_standard_value_decodes_to_wall_clock()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L124 | neighbors=[TestRemoteClock]
- "tests_test_os_fingerprint_testttlinference_test_hop_estimate": ".test_hop_estimate()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L205 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_os_family_linux": ".test_os_family_linux()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L209 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_os_family_network": ".test_os_family_network()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L215 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_os_family_unknown_on_none": ".test_os_family_unknown_on_none()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L218 | neighbors=[TestTtlInference]
- "tests_test_os_fingerprint_testttlinference_test_os_family_windows": ".test_os_family_windows()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L212 | neighbors=[TestTtlInference]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-076.json

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
