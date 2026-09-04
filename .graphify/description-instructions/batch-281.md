# Node Description Batch 282 of 332

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

- "tests_test_ftp_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L76 | neighbors=[TestParity] | lang=en
- "tests_test_ftp_scanner_testpurelogic_test_banner_software": ".test_banner_software()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L23 | neighbors=[TestPureLogic] | lang=en
- "tests_test_ftp_scanner_testpurelogic_test_parse_pasv": ".test_parse_pasv()" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L19 | neighbors=[TestPureLogic] | lang=en
- "tests_test_host_discovery_mobile_rationale_1": "Pure-logic tests for the ARP/MAC/mobile-detection helpers in host_discovery. No" | kind=entity | source=probe/tests/test_host_discovery_mobile.py:L1 | neighbors=[test_host_discovery_mobile.py] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_iphone_lockdownd_port": ".test_iphone_lockdownd_port()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L53 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_mobile_vendor": ".test_mobile_vendor()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L59 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_no_signal": ".test_no_signal()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L65 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_plain_vendor_passthrough": ".test_plain_vendor_passthrough()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L62 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testdevicehint_test_randomized_mac_is_mobile": ".test_randomized_mac_is_mobile()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L56 | neighbors=[TestDeviceHint] | lang=en
- "tests_test_host_discovery_mobile_testlocallyadministered_test_globally_unique_macs": ".test_globally_unique_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L39 | neighbors=[TestLocallyAdministered] | lang=en
- "tests_test_host_discovery_mobile_testlocallyadministered_test_randomized_phone_macs": ".test_randomized_phone_macs()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L33 | neighbors=[TestLocallyAdministered] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_extracts_from_arp_line": ".test_extracts_from_arp_line()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L17 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_lowercases": ".test_lowercases()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L14 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_broadcast": ".test_rejects_broadcast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L21 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_garbage": ".test_rejects_garbage()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L27 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_rejects_multicast": ".test_rejects_multicast()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L24 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac_test_zero_pads_octets": ".test_zero_pads_octets()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L10 | neighbors=[TestNormalizeMac] | lang=en
- "tests_test_host_discovery_mobile_testvendorlookup_test_known_oui": ".test_known_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L45 | neighbors=[TestVendorLookup] | lang=en
- "tests_test_host_discovery_mobile_testvendorlookup_test_unknown_oui": ".test_unknown_oui()" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L48 | neighbors=[TestVendorLookup] | lang=en
- "tests_test_host_discovery_udp_closed_udp_port": "_closed_udp_port()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L110 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_no_neighbor": "no_neighbor()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L120 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_rationale_1": "test_host_discovery_udp.py — the unprivileged UDP liveness tier + name facts.  C" | kind=entity | source=probe/tests/test_host_discovery_udp.py:L1 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_rationale_233": "A RST mid-handshake (ConnectionResetError) is the target's stack talking." | kind=entity | source=probe/tests/test_host_discovery_udp.py:L233 | neighbors=[test_tcp_reset_counts_as_proof_of_life()] | lang=en
- "tests_test_host_discovery_udp_rationale_25": "Build a NetBIOS node-status response (RFC 1002 §4.2.18)." | kind=entity | source=probe/tests/test_host_discovery_udp.py:L25 | neighbors=[_nbstat_reply()] | lang=pt
- "tests_test_host_discovery_udp_rationale_252": "On-LAN INCOMPLETE/FAILED = nobody owns the address right now; spending     datag" | kind=entity | source=probe/tests/test_host_discovery_udp.py:L252 | neighbors=[test_udp_tier_skipped_when_arp_definiti…] | lang=en
- "tests_test_host_discovery_udp_responder_connection_made": ".connection_made()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L95 | neighbors=[_Responder] | lang=en
- "tests_test_host_discovery_udp_responder_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L98 | neighbors=[_Responder] | lang=en
- "tests_test_host_discovery_udp_responder_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L91 | neighbors=[_Responder] | lang=en
- "tests_test_host_discovery_udp_scanner": "_scanner()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L124 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_test_icmp_unreachable_from_closed_port_proves_stack_is_up": "test_icmp_unreachable_from_closed_port_proves_stack_is_up()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L155 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_test_reverse_dns_name_recorded_and_becomes_alias": "test_reverse_dns_name_recorded_and_becomes_alias()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L206 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_test_udp_tier_skipped_when_neighbor_vouches": "test_udp_tier_skipped_when_neighbor_vouches()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L187 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_test_udp_tier_skipped_when_tcp_proves_life": "test_udp_tier_skipped_when_tcp_proves_life()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L166 | neighbors=[test_host_discovery_udp.py] | lang=en
- "tests_test_host_discovery_udp_testfusewithudp_test_icmp_unreachable_alone": ".test_icmp_unreachable_alone()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L68 | neighbors=[TestFuseWithUdp] | lang=en
- "tests_test_host_discovery_udp_testfusewithudp_test_no_signals_unchanged": ".test_no_signals_unchanged()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L82 | neighbors=[TestFuseWithUdp] | lang=en
- "tests_test_host_discovery_udp_testfusewithudp_test_tcp_plus_udp_corroborate": ".test_tcp_plus_udp_corroborate()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L74 | neighbors=[TestFuseWithUdp] | lang=en
- "tests_test_host_discovery_udp_testfusewithudp_test_udp_reply_alone_is_confirmed_alive": ".test_udp_reply_alone_is_confirmed_alive()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L60 | neighbors=[TestFuseWithUdp] | lang=en
- "tests_test_host_discovery_udp_testparsenbstat_test_not_a_response": ".test_not_a_response()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L48 | neighbors=[TestParseNbstat] | lang=en
- "tests_test_host_health_rationale_1": "test_host_health.py — mid-scan target-offline detection.  The interesting cases" | kind=entity | source=probe/tests/test_host_health.py:L1 | neighbors=[test_host_health.py] | lang=en
- "tests_test_host_health_rationale_122": "One false alarm must not disable the check for the rest of the scan." | kind=entity | source=probe/tests/test_host_health.py:L122 | neighbors=[.test_flaky_host_can_be_suspected_again…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-281.json

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
