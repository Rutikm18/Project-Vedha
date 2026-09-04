# Node Description Batch 287 of 332

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

- "tests_test_main_scripts_datastore_probe_rationale_1": "test_main_scripts_datastore_probe.py — safe read-only datastore probes make the" | kind=entity | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[test_main_scripts_datastore_probe.py] | lang=en
- "tests_test_main_scripts_datastore_probe_test_ladder_includes_safe_datastore_probes": "test_ladder_includes_safe_datastore_probes()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L40 | neighbors=[test_main_scripts_datastore_probe.py] | lang=en
- "tests_test_main_scripts_datastore_probe_test_memcached_probe_response_yields_unauth_finding": "test_memcached_probe_response_yields_unauth_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L51 | neighbors=[test_main_scripts_datastore_probe.py] | lang=en
- "tests_test_main_scripts_device_rationale_1": "test_main_scripts_device.py — device-role classification (P0 \"Device classificat" | kind=entity | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[test_main_scripts_device.py] | lang=en
- "tests_test_main_scripts_device_rationale_94": "FIX 5(b): don't tie an obvious workstation; require role ports/DomainRole     fo" | kind=entity | source=probe/tests/test_main_scripts_device.py:L94 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_domain_controller": ".test_domain_controller()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L25 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_iot_camera": ".test_iot_camera()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L48 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_network_device_router": ".test_network_device_router()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L37 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_printer": ".test_printer()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L31 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_service_product_reinforces_server": ".test_service_product_reinforces_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L64 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_single_signal_confidence_capped": ".test_single_signal_confidence_capped()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L58 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_unknown_when_no_evidence": ".test_unknown_when_no_evidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L53 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_vmware_hypervisor": ".test_vmware_hypervisor()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L43 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifydevice_test_windows_workstation": ".test_windows_workstation()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L18 | neighbors=[TestClassifyDevice] | lang=en
- "tests_test_main_scripts_device_testclassifyfromresults_test_extracts_signals_from_scan_results": ".test_extracts_signals_from_scan_results()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L72 | neighbors=[TestClassifyFromResults] | lang=en
- "tests_test_main_scripts_device_testworkstationvsserver_test_baseline_windows_services_are_not_a_server_signal": ".test_baseline_windows_services_are_not_a_server_signal()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L110 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_testworkstationvsserver_test_real_domain_controller_still_server": ".test_real_domain_controller_still_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L115 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_testworkstationvsserver_test_reference_workstation_unauthenticated": ".test_reference_workstation_unauthenticated()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L99 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_testworkstationvsserver_test_reference_workstation_with_domain_role_0": ".test_reference_workstation_with_domain_role_0()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L105 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_testworkstationvsserver_test_role_service_makes_server": ".test_role_service_makes_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L122 | neighbors=[TestWorkstationVsServer] | lang=en
- "tests_test_main_scripts_device_ties_rationale_1": "test_main_scripts_device_ties.py — Phase 23: device classification never resolve" | kind=entity | source=probe/tests/test_main_scripts_device_ties.py:L1 | neighbors=[test_main_scripts_device_ties.py] | lang=en
- "tests_test_main_scripts_device_ties_test_clear_winner_is_not_ambiguous": "test_clear_winner_is_not_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L21 | neighbors=[test_main_scripts_device_ties.py] | lang=en
- "tests_test_main_scripts_device_ties_test_domain_controller_breaks_the_tie": "test_domain_controller_breaks_the_tie()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L27 | neighbors=[test_main_scripts_device_ties.py] | lang=en
- "tests_test_main_scripts_device_ties_test_empty_is_unknown_not_ambiguous": "test_empty_is_unknown_not_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L33 | neighbors=[test_main_scripts_device_ties.py] | lang=en
- "tests_test_main_scripts_device_ties_test_workstation_server_tie_is_ambiguous": "test_workstation_server_tie_is_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L10 | neighbors=[test_main_scripts_device_ties.py] | lang=en
- "tests_test_main_scripts_errno_rationale_1": "test_main_scripts_errno.py — Phase 2: shared TCP/UDP errno classification.  Veri" | kind=entity | source=probe/tests/test_main_scripts_errno.py:L1 | neighbors=[test_main_scripts_errno.py] | lang=en
- "tests_test_main_scripts_errno_test_dns_failure_is_error_not_filtered": "test_dns_failure_is_error_not_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L45 | neighbors=[test_main_scripts_errno.py] | lang=en
- "tests_test_main_scripts_errno_test_errno_none_falls_back_to_os_error": "test_errno_none_falls_back_to_os_error()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L41 | neighbors=[test_main_scripts_errno.py] | lang=en
- "tests_test_main_scripts_errno_test_port_scanner_uses_the_same_shared_classifier": "test_port_scanner_uses_the_same_shared_classifier()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L58 | neighbors=[test_main_scripts_errno.py] | lang=en
- "tests_test_main_scripts_findings_rationale_1": "test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic," | kind=entity | source=probe/tests/test_main_scripts_findings.py:L1 | neighbors=[test_main_scripts_findings.py] | lang=en
- "tests_test_main_scripts_findings_test_build_service_index_extracts_confirmed_services": "test_build_service_index_extracts_confirmed_services()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L198 | neighbors=[test_main_scripts_findings.py] | lang=en
- "tests_test_main_scripts_hardening_rationale_1": "test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied" | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[test_main_scripts_hardening.py] | lang=en
- "tests_test_main_scripts_hardening_rationale_101": "A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro" | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L101 | neighbors=[_smb2_header()] | lang=pt
- "tests_test_main_scripts_hardening_rationale_123": "STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9," | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L123 | neighbors=[make_smb2_error()] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_linux_ttl_only_capped": ".test_linux_ttl_only_capped()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L92 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_no_signal_is_unknown": ".test_no_signal_is_unknown()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L87 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_ttl_only_is_not_absolute": ".test_ttl_only_is_not_absolute()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L74 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_two_signals_beat_one": ".test_two_signals_beat_one()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L81 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testsmbparsing_test_negotiate_request_excludes_smb311": ".test_negotiate_request_excludes_smb311()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L152 | neighbors=[TestSmbParsing] | lang=en
- "tests_test_main_scripts_hardening_testsmbparsing_test_negotiate_request_offers_smb311_with_preauth_context": ".test_negotiate_request_offers_smb311_with_preauth_context()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L152 | neighbors=[TestSmbParsing] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-286.json

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
