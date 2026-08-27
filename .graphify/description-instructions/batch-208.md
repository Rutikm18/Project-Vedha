# Node Description Batch 209 of 236

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

- "tests_test_notifications_testdeliver_test_sender_error_is_swallowed": ".test_sender_error_is_swallowed()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L24 | neighbors=[TestDeliver]
- "tests_test_notifications_testdeliver_test_unknown_kind_returns_false": ".test_unknown_kind_returns_false()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L21 | neighbors=[TestDeliver]
- "tests_test_notifications_testnotifytenant_test_counts_only_successful_channels": ".test_counts_only_successful_channels()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L52 | neighbors=[TestNotifyTenant]
- "tests_test_notifications_testnotifytenant_test_fans_to_enabled_and_decrypts_secret": ".test_fans_to_enabled_and_decrypts_secret()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L31 | neighbors=[TestNotifyTenant]
- "tests_test_nuclei_background_fakesession_add": ".add()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L46 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L34 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L37 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_commit": ".commit()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L52 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_flush": ".flush()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L49 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L31 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_fakesession_rollback": ".rollback()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L55 | neighbors=[_FakeSession]
- "tests_test_nuclei_background_nestedtransaction_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L23 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_nestedtransaction_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L26 | neighbors=[_NestedTransaction]
- "tests_test_nuclei_background_scalarresult_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L15 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_scalarresult_scalar_one_or_none": ".scalar_one_or_none()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L18 | neighbors=[_ScalarResult]
- "tests_test_nuclei_background_sessionfactory_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L60 | neighbors=[_SessionFactory]
- "tests_test_nuclei_scanner_fakeprocess_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L31 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_kill": ".kill()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L61 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_terminate": ".terminate()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L57 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_fakeprocess_wait": ".wait()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L50 | neighbors=[FakeProcess]
- "tests_test_nuclei_scanner_test_missing_binary_is_a_reported_failure": "test_missing_binary_is_a_reported_failure()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L95 | neighbors=[test_nuclei_scanner.py]
- "tests_test_os_fingerprint_rationale_1": "test_os_fingerprint.py — Tier 2.1 (OS fingerprinting) + 2.2 (ICMP multi-probe +" | kind=entity | source=probe/tests/test_os_fingerprint.py:L1 | neighbors=[test_os_fingerprint.py]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_none_parsed": ".test_rejects_none_parsed()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L183 | neighbors=[TestAcceptEchoReply]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_jumbo_even_without_os_signal": ".test_mss_flags_jumbo_even_without_os_signal()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L260 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_flags_tunnel_or_vpn": ".test_mss_flags_tunnel_or_vpn()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L256 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_is_path_intel_not_an_os_signal": ".test_mss_is_path_intel_not_an_os_signal()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L263 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_mss_yields_ethernet_mtu": ".test_mss_yields_ethernet_mtu()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L252 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_network_device_from_ttl_255": ".test_network_device_from_ttl_255()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L244 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_no_signals_is_unknown": ".test_no_signals_is_unknown()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L239 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_signals_recorded": ".test_signals_recorded()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L247 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_and_window_agree_boosts_confidence": ".test_ttl_and_window_agree_boosts_confidence()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L233 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_linux": ".test_ttl_only_linux()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L225 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testfingerprintos_test_ttl_only_windows": ".test_ttl_only_windows()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L230 | neighbors=[TestFingerprintOs]
- "tests_test_os_fingerprint_testicmpbuilders_test_address_mask_request_type": ".test_address_mask_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L54 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_payload_preserved": ".test_echo_payload_preserved()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L45 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_echo_request_type_and_checksum": ".test_echo_request_type_and_checksum()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L38 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpbuilders_test_timestamp_request_type": ".test_timestamp_request_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L49 | neighbors=[TestIcmpBuilders]
- "tests_test_os_fingerprint_testicmpcapability_test_available_when_socket_ok": ".test_available_when_socket_ok()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L276 | neighbors=[TestIcmpCapability]
- "tests_test_os_fingerprint_testicmpcapability_test_unavailable_when_socket_raises": ".test_unavailable_when_socket_raises()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L271 | neighbors=[TestIcmpCapability]
- "tests_test_os_fingerprint_testicmpparse_test_parse_raw_icmp_without_ip_header": ".test_parse_raw_icmp_without_ip_header()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L82 | neighbors=[TestIcmpParse]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-208.json

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
