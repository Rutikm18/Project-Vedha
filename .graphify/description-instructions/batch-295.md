# Node Description Batch 296 of 336

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

- "tests_test_new_scanners_testudpprobeconstruction_test_udp_probes_has_all_playbook_ports": ".test_udp_probes_has_all_playbook_ports()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L235 | neighbors=[TestUDPProbeConstruction]
- "tests_test_new_scanners_testversionchange_test_different_versions": ".test_different_versions()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L363 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_empty_old_version": ".test_empty_old_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L371 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_same_version": ".test_same_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L367 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_whitespace_normalised": ".test_whitespace_normalised()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L375 | neighbors=[TestVersionChange]
- "tests_test_nfs_scanner_rationale_1": "test_nfs_scanner.py — NFS export enumeration over ONC RPC.  The live RPC path ne" | kind=entity | source=probe/tests/test_nfs_scanner.py:L1 | neighbors=[test_nfs_scanner.py]
- "tests_test_nfs_scanner_testxdrparsers_test_parser_is_bounded": ".test_parser_is_bounded()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L84 | neighbors=[TestXdrParsers]
- "tests_test_nfs_scanner_testxdrparsers_test_world_readable_logic": ".test_world_readable_logic()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L77 | neighbors=[TestXdrParsers]
- "tests_test_nmap_wrapper_rationale_1": "test_nmap_wrapper.py — the \"nmap returned 0 while native scanners saw ports\" bug" | kind=entity | source=probe/tests/test_nmap_wrapper.py:L1 | neighbors=[test_nmap_wrapper.py]
- "tests_test_nmap_wrapper_test_filtered_ports_not_emitted_as_open": "test_filtered_ports_not_emitted_as_open()" | kind=code-symbol | source=probe/tests/test_nmap_wrapper.py:L36 | neighbors=[test_nmap_wrapper.py]
- "tests_test_nmap_wrapper_test_open_ports_are_emitted": "test_open_ports_are_emitted()" | kind=code-symbol | source=probe/tests/test_nmap_wrapper.py:L31 | neighbors=[test_nmap_wrapper.py]
- "tests_test_nmap_wrapper_test_port_scan_profiles_carry_pn": "test_port_scan_profiles_carry_pn()" | kind=code-symbol | source=probe/tests/test_nmap_wrapper.py:L24 | neighbors=[test_nmap_wrapper.py]
- "tests_test_nmap_xml_safety_rationale_1": "test_nmap_xml_safety.py — nmap XML parsing must resist XML-bomb / entity injecti" | kind=entity | source=probe/tests/test_nmap_xml_safety.py:L1 | neighbors=[test_nmap_xml_safety.py]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_declaration_is_refused": ".test_entity_declaration_is_refused()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L28 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_entity_guard_is_case_insensitive": ".test_entity_guard_is_case_insensitive()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L33 | neighbors=[TestNmapEntityGuard]
- "tests_test_nmap_xml_safety_testnmapentityguard_test_legitimate_doctype_output_still_parses": ".test_legitimate_doctype_output_still_parses()" | kind=code-symbol | source=probe/tests/test_nmap_xml_safety.py:L38 | neighbors=[TestNmapEntityGuard]
- "tests_test_notifications_rationale_1": "test_notifications.py — integration delivery fan-out (item 3 delivery worker)." | kind=entity | source=manager/backend/tests/test_notifications.py:L1 | neighbors=[test_notifications.py]
- "tests_test_notifications_testdeliver_test_dispatches_to_the_kind": ".test_dispatches_to_the_kind()" | kind=code-symbol | source=manager/backend/tests/test_notifications.py:L14 | neighbors=[TestDeliver]
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
- "tests_test_online_rationale_1": "test_online.py — the OPT-IN live enrichment layer (cve/online.py).  Every test i" | kind=entity | source=probe/tests/test_online.py:L1 | neighbors=[test_online.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-295.json

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
