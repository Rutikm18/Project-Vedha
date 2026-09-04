# Node Description Batch 292 of 332

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

- "tests_test_nmap_wrapper_test_port_scan_profiles_carry_pn": "test_port_scan_profiles_carry_pn()" | kind=code-symbol | source=probe/tests/test_nmap_wrapper.py:L24 | neighbors=[test_nmap_wrapper.py] | lang=en
- "tests_test_nmap_xml_safety_rationale_1": "test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti" | kind=entity | source=probe/tests/test_nmap_xml_safety.py:L1 | neighbors=[test_nmap_xml_safety.py] | lang=en
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_declaration_is_refused": ".test_entity_declaration_is_refused()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L28 | neighbors=[TestNmapEntityGuard] | lang=en
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_guard_is_case_insensitive": ".test_entity_guard_is_case_insensitive()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L33 | neighbors=[TestNmapEntityGuard] | lang=en
- "tests_test_nmap_xml_safety_testnmapentityguard_test_legitimate_doctype_output_still_parses": ".test_legitimate_doctype_output_still_parses()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L38 | neighbors=[TestNmapEntityGuard] | lang=en
- "tests_test_notifications_rationale_1": "test_notifications.py — integration delivery fan-out (item 3 delivery worker)." | kind=entity | source=manager/backend/tests/test_notifications.py:L1 | neighbors=[test_notifications.py] | lang=en
- "tests_test_notifications_testdeliver_test_dispatches_to_the_kind": ".test_dispatches_to_the_kind()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L14 | neighbors=[TestDeliver] | lang=en
- "tests_test_notifications_testdeliver_test_sender_error_is_swallowed": ".test_sender_error_is_swallowed()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L24 | neighbors=[TestDeliver] | lang=en
- "tests_test_notifications_testdeliver_test_unknown_kind_returns_false": ".test_unknown_kind_returns_false()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L21 | neighbors=[TestDeliver] | lang=en
- "tests_test_notifications_testnotifytenant_test_counts_only_successful_channels": ".test_counts_only_successful_channels()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L52 | neighbors=[TestNotifyTenant] | lang=en
- "tests_test_notifications_testnotifytenant_test_fans_to_enabled_and_decrypts_secret": ".test_fans_to_enabled_and_decrypts_secret()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L31 | neighbors=[TestNotifyTenant] | lang=en
- "tests_test_nuclei_background_fakesession_add": ".add()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L46 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L34 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L37 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_commit": ".commit()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L52 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_flush": ".flush()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L49 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L31 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_fakesession_rollback": ".rollback()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L55 | neighbors=[_FakeSession] | lang=en
- "tests_test_nuclei_background_nestedtransaction_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L23 | neighbors=[_NestedTransaction] | lang=en
- "tests_test_nuclei_background_nestedtransaction_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L26 | neighbors=[_NestedTransaction] | lang=en
- "tests_test_nuclei_background_scalarresult_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L15 | neighbors=[_ScalarResult] | lang=en
- "tests_test_nuclei_background_scalarresult_scalar_one_or_none": ".scalar_one_or_none()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L18 | neighbors=[_ScalarResult] | lang=en
- "tests_test_nuclei_background_sessionfactory_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L60 | neighbors=[_SessionFactory] | lang=en
- "tests_test_nuclei_scanner_fakeprocess_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L31 | neighbors=[FakeProcess] | lang=en
- "tests_test_nuclei_scanner_fakeprocess_kill": ".kill()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L61 | neighbors=[FakeProcess] | lang=en
- "tests_test_nuclei_scanner_fakeprocess_terminate": ".terminate()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L57 | neighbors=[FakeProcess] | lang=en
- "tests_test_nuclei_scanner_fakeprocess_wait": ".wait()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L50 | neighbors=[FakeProcess] | lang=en
- "tests_test_nuclei_scanner_test_missing_binary_is_a_reported_failure": "test_missing_binary_is_a_reported_failure()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L95 | neighbors=[test_nuclei_scanner.py] | lang=en
- "tests_test_online_rationale_1": "test_online.py — the OPT-IN live enrichment layer (cve/online.py).  Every test i" | kind=entity | source=probe/tests/test_online.py:L1 | neighbors=[test_online.py] | lang=en
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-291.json

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
