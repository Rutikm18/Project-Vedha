# Node Description Batch 297 of 336

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

- "tests_test_online_rationale_52": "A fake transport that ignores its args and returns fixed bytes." | kind=entity | source=probe/tests/test_online.py:L52 | neighbors=[_get_returning()] | lang=en
- "tests_test_online_rationale_65": "A CVEFinding as the offline pass would emit it — CVSS None models a mirror gap." | kind=entity | source=probe/tests/test_online.py:L65 | neighbors=[_finding()] | lang=en
- "tests_test_os_fingerprint_rationale_1": "test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +" | kind=entity | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[test_os_fingerprint.py] | lang=pt
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_none_parsed": ".test_rejects_none_parsed()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L183 | neighbors=[TestAcceptEchoReply] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_jumbo_even_without_os_signal": ".test_mss_flags_jumbo_even_without_os_signal()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L260 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_tunnel_or_vpn": ".test_mss_flags_tunnel_or_vpn()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L256 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_mss_is_path_intel_not_an_os_signal": ".test_mss_is_path_intel_not_an_os_signal()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L263 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_mss_yields_ethernet_mtu": ".test_mss_yields_ethernet_mtu()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L252 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_network_device_from_ttl_255": ".test_network_device_from_ttl_255()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L244 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_no_signals_is_unknown": ".test_no_signals_is_unknown()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L239 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_no_ttl_means_no_ttl_source": ".test_no_ttl_means_no_ttl_source()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L276 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_signals_recorded": ".test_signals_recorded()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L247 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_and_window_agree_boosts_confidence": ".test_ttl_and_window_agree_boosts_confidence()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L233 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_linux": ".test_ttl_only_linux()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L225 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_windows": ".test_ttl_only_windows()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L230 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_source_defaults_to_unspecified": ".test_ttl_source_defaults_to_unspecified()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L273 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_source_recorded_when_provided": ".test_ttl_source_recorded_when_provided()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L267 | neighbors=[TestFingerprintOs] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_address_mask_request_type": ".test_address_mask_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L54 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_payload_preserved": ".test_echo_payload_preserved()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L45 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_request_type_and_checksum": ".test_echo_request_type_and_checksum()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L38 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpbuilders_test_timestamp_request_type": ".test_timestamp_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L49 | neighbors=[TestIcmpBuilders] | lang=en
- "tests_test_os_fingerprint_testicmpcapability_test_available_when_socket_ok": ".test_available_when_socket_ok()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L442 | neighbors=[TestIcmpCapability] | lang=en
- "tests_test_os_fingerprint_testicmpcapability_test_unavailable_when_socket_raises": ".test_unavailable_when_socket_raises()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L437 | neighbors=[TestIcmpCapability] | lang=en
- "tests_test_os_fingerprint_testicmpparse_test_parse_raw_icmp_without_ip_header": ".test_parse_raw_icmp_without_ip_header()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L82 | neighbors=[TestIcmpParse] | lang=en
- "tests_test_os_fingerprint_testicmpparse_test_parse_rejects_short": ".test_parse_rejects_short()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L79 | neighbors=[TestIcmpParse] | lang=en
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_rejects_short_body": ".test_parse_rejects_short_body()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L118 | neighbors=[TestIcmpTimestamps] | lang=en
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_handles_odd_length": ".test_checksum_handles_odd_length()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L31 | neighbors=[TestInetChecksum] | lang=en
- "tests_test_os_fingerprint_testinetchecksum_test_checksum_verifies_to_zero": ".test_checksum_verifies_to_zero()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L25 | neighbors=[TestInetChecksum] | lang=en
- "tests_test_os_fingerprint_testprovenance_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L370 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_datagram_echo_without_ttl_does_not_fake_a_ttl": ".test_datagram_echo_without_ttl_does_not_fake_a_ttl()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L383 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_icmp_unavailable_tcp_hints_is_method_tcp_hints_not_icmp": ".test_icmp_unavailable_tcp_hints_is_method_tcp_hints_not_icmp()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L393 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_icmp_unavailable_with_tcp_ttl_is_tcp_ttl_not_icmp": ".test_icmp_unavailable_with_tcp_ttl_is_tcp_ttl_not_icmp()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L425 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_no_icmp_but_tcp_ttl_hint_is_method_tcp_ttl": ".test_no_icmp_but_tcp_ttl_hint_is_method_tcp_ttl()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L411 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_real_echo_reply_is_method_icmp_echo": ".test_real_echo_reply_is_method_icmp_echo()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L374 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testprovenance_test_timestamp_reply_tags_ttl_source": ".test_timestamp_reply_tags_ttl_source()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L403 | neighbors=[TestProvenance] | lang=en
- "tests_test_os_fingerprint_testremoteclock_test_high_bit_marks_nonstandard_clock": ".test_high_bit_marks_nonstandard_clock()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L132 | neighbors=[TestRemoteClock] | lang=en
- "tests_test_os_fingerprint_testremoteclock_test_standard_value_decodes_to_wall_clock": ".test_standard_value_decodes_to_wall_clock()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L124 | neighbors=[TestRemoteClock] | lang=en
- "tests_test_os_fingerprint_testsmbbuildenrichment_scanner": "._scanner()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L329 | neighbors=[TestSmbBuildEnrichment] | lang=en
- "tests_test_os_fingerprint_testsmbbuildenrichment_test_build_lifts_ttl_only_guess_to_authoritative": ".test_build_lifts_ttl_only_guess_to_authoritative()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L334 | neighbors=[TestSmbBuildEnrichment] | lang=en
- "tests_test_os_fingerprint_testsmbbuildenrichment_test_no_smb_leaves_ttl_only_result_untouched": ".test_no_smb_leaves_ttl_only_result_untouched()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L350 | neighbors=[TestSmbBuildEnrichment] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-296.json

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
