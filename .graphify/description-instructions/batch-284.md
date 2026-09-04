# Node Description Batch 285 of 330

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

- "tests_test_main_scripts_adaptive_timeout_test_invalid_band_rejected": "test_invalid_band_rejected()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L67 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_narrows_then_widens_after_outlier": "test_narrows_then_widens_after_outlier()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L50 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_no_samples_returns_base": "test_no_samples_returns_base()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L14 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_observe_ignores_bad_samples": "test_observe_ignores_bad_samples()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L38 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_adaptive_timeout_test_timeout_is_clamped_to_max": "test_timeout_is_clamped_to_max()" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L33 | neighbors=[test_main_scripts_adaptive_timeout.py]
- "tests_test_main_scripts_completeness_rationale_1": "test_main_scripts_completeness.py — Epic 4: set-based scan-completeness invarian" | kind=entity | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[test_main_scripts_completeness.py]
- "tests_test_main_scripts_correlation_rationale_1": "test_main_scripts_correlation.py — Epic 2: correlation findings.  Composite, hig" | kind=entity | source=probe/tests/test_main_scripts_correlation.py:L1 | neighbors=[test_main_scripts_correlation.py]
- "tests_test_main_scripts_coverage_closed": "_closed()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L76 | neighbors=[test_main_scripts_coverage.py]
- "tests_test_main_scripts_coverage_rationale_1": "test_main_scripts_coverage.py — P0 coverage + self-health capabilities added to" | kind=entity | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[test_main_scripts_coverage.py]
- "tests_test_main_scripts_coverage_testprofiles_test_custom_dedups_and_requires_ports": ".test_custom_dedups_and_requires_ports()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L64 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_full_is_entire_tcp_space": ".test_full_is_entire_tcp_space()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L42 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_quick_is_small_and_contains_smb": ".test_quick_is_small_and_contains_smb()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L54 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_top100_is_100_unique": ".test_top100_is_100_unique()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L49 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_top1000_covers_windows_ground_truth_extras": ".test_top1000_covers_windows_ground_truth_extras()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L58 | neighbors=[TestProfiles]
- "tests_test_main_scripts_coverage_testprofiles_test_unknown_profile_raises": ".test_unknown_profile_raises()" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L69 | neighbors=[TestProfiles]
- "tests_test_main_scripts_datastore_probe_rationale_1": "test_main_scripts_datastore_probe.py — safe read-only datastore probes make the" | kind=entity | source=probe/tests/test_main_scripts_datastore_probe.py:L1 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_datastore_probe_test_ladder_includes_safe_datastore_probes": "test_ladder_includes_safe_datastore_probes()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L40 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_datastore_probe_test_memcached_probe_response_yields_unauth_finding": "test_memcached_probe_response_yields_unauth_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_datastore_probe.py:L51 | neighbors=[test_main_scripts_datastore_probe.py]
- "tests_test_main_scripts_device_rationale_1": "test_main_scripts_device.py — device-role classification (P0 \"Device classificat" | kind=entity | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[test_main_scripts_device.py]
- "tests_test_main_scripts_device_rationale_94": "FIX 5(b): don't tie an obvious workstation; require role ports/DomainRole     fo" | kind=entity | source=probe/tests/test_main_scripts_device.py:L94 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_testclassifydevice_test_domain_controller": ".test_domain_controller()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L25 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_iot_camera": ".test_iot_camera()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L48 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_network_device_router": ".test_network_device_router()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L37 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_printer": ".test_printer()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L31 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_service_product_reinforces_server": ".test_service_product_reinforces_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L64 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_single_signal_confidence_capped": ".test_single_signal_confidence_capped()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L58 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_unknown_when_no_evidence": ".test_unknown_when_no_evidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L53 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_vmware_hypervisor": ".test_vmware_hypervisor()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L43 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifydevice_test_windows_workstation": ".test_windows_workstation()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L18 | neighbors=[TestClassifyDevice]
- "tests_test_main_scripts_device_testclassifyfromresults_test_extracts_signals_from_scan_results": ".test_extracts_signals_from_scan_results()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L72 | neighbors=[TestClassifyFromResults]
- "tests_test_main_scripts_device_testworkstationvsserver_test_baseline_windows_services_are_not_a_server_signal": ".test_baseline_windows_services_are_not_a_server_signal()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L110 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_testworkstationvsserver_test_real_domain_controller_still_server": ".test_real_domain_controller_still_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L115 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_testworkstationvsserver_test_reference_workstation_unauthenticated": ".test_reference_workstation_unauthenticated()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L99 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_testworkstationvsserver_test_reference_workstation_with_domain_role_0": ".test_reference_workstation_with_domain_role_0()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L105 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_testworkstationvsserver_test_role_service_makes_server": ".test_role_service_makes_server()" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L122 | neighbors=[TestWorkstationVsServer]
- "tests_test_main_scripts_device_ties_rationale_1": "test_main_scripts_device_ties.py — Phase 23: device classification never resolve" | kind=entity | source=probe/tests/test_main_scripts_device_ties.py:L1 | neighbors=[test_main_scripts_device_ties.py]
- "tests_test_main_scripts_device_ties_test_clear_winner_is_not_ambiguous": "test_clear_winner_is_not_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L21 | neighbors=[test_main_scripts_device_ties.py]
- "tests_test_main_scripts_device_ties_test_domain_controller_breaks_the_tie": "test_domain_controller_breaks_the_tie()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L27 | neighbors=[test_main_scripts_device_ties.py]
- "tests_test_main_scripts_device_ties_test_empty_is_unknown_not_ambiguous": "test_empty_is_unknown_not_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L33 | neighbors=[test_main_scripts_device_ties.py]
- "tests_test_main_scripts_device_ties_test_workstation_server_tie_is_ambiguous": "test_workstation_server_tie_is_ambiguous()" | kind=code-symbol | source=probe/tests/test_main_scripts_device_ties.py:L10 | neighbors=[test_main_scripts_device_ties.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-284.json

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
