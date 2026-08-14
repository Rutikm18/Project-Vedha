# Node Description Batch 165 of 186

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

- "tests_test_new_scanners_teststablehostid_test_zero_mac_skipped": ".test_zero_mac_skipped()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L350 | neighbors=[TestStableHostId]
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
- "tests_test_new_scanners_testversionchange_test_different_versions": ".test_different_versions()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L360 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_empty_old_version": ".test_empty_old_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L368 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_same_version": ".test_same_version()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L364 | neighbors=[TestVersionChange]
- "tests_test_new_scanners_testversionchange_test_whitespace_normalised": ".test_whitespace_normalised()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L372 | neighbors=[TestVersionChange]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-164.json

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
