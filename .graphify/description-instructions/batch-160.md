# Node Description Batch 161 of 336

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

- "tests_test_posture_test_finding_views_handles_null_asset_and_scores": "test_finding_views_handles_null_asset_and_scores()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L128 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_test_finding_views_maps_columns_and_asset_criticality": "test_finding_views_maps_columns_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L114 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_trace_testbehaviourpreserved_test_detect_posture_matches_traced_findings": ".test_detect_posture_matches_traced_findings()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L119 | neighbors=[TestBehaviourPreserved, ._mixed()]
- "tests_test_posture_trace_testruleisolation": "TestRuleIsolation" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L95 | neighbors=[test_posture_trace.py, .test_raising_rule_is_error_and_others_…]
- "tests_test_printer_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L61 | neighbors=[test_printer_scanner.py, .test_main_scripts()]
- "tests_test_printer_scanner_testprinterfindings": "TestPrinterFindings" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L52 | neighbors=[test_printer_scanner.py, .test_exposed_low()]
- "tests_test_printer_scanner_testprinterscanner_test_no_printer_filtered": ".test_no_printer_filtered()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L46 | neighbors=[TestPrinterScanner, ._sc()]
- "tests_test_printer_scanner_testprinterscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L39 | neighbors=[TestPrinterScanner, ._sc()]
- "tests_test_probe_core_testassetmergepassivecollect": "TestAssetMergePassiveCollect" | kind=code-symbol | source=probe/tests/test_probe_core.py:L583 | neighbors=[test_probe_core.py, .test_passive_facts_appended()]
- "tests_test_probe_core_testassetmergeservicebanner": "TestAssetMergeServiceBanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L534 | neighbors=[test_probe_core.py, .test_banner_stored()]
- "tests_test_probe_core_testassetmergesmbscan": "TestAssetMergeSmbScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L559 | neighbors=[test_probe_core.py, .test_smb_state_host_level()]
- "tests_test_probe_core_testassetmergetlsscan": "TestAssetMergeTlsScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L543 | neighbors=[test_probe_core.py, .test_tls_facts_stored()]
- "tests_test_probe_core_testassetmergeunknownscanner": "TestAssetMergeUnknownScanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L592 | neighbors=[test_probe_core.py, .test_unknown_scanner_ignored()]
- "tests_test_probe_core_testassetmergewebscan": "TestAssetMergeWebScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L551 | neighbors=[test_probe_core.py, .test_web_facts_stored()]
- "tests_test_probe_core_testassetneedsrechecklive_test_never_seen": ".test_never_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L476 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_recently_seen": ".test_recently_seen()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L480 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetneedsrechecklive_test_stale": ".test_stale()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L484 | neighbors=[TestAssetNeedsRecheckLive, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_empty": ".test_empty()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L497 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testassetopenportsfordeepscan_test_only_open": ".test_only_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L490 | neighbors=[TestAssetOpenPortsForDeepScan, _asset()]
- "tests_test_probe_core_testcacheentry": "TestCacheEntry" | kind=code-symbol | source=probe/tests/test_probe_core.py:L769 | neighbors=[test_probe_core.py, .test_roundtrip()]
- "tests_test_probe_core_testcacheentry_test_roundtrip": ".test_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L770 | neighbors=[TestCacheEntry, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_error_overrides": ".test_error_overrides()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L760 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_host_discovery_uncertain": ".test_host_discovery_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L756 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_service_banner_deterministic": ".test_service_banner_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L752 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_tcp_port_scan_deterministic": ".test_tcp_port_scan_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L744 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_udp_port_scan_uncertain": ".test_udp_port_scan_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L748 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_unknown_scanner_conservative": ".test_unknown_scanner_conservative()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L764 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testenginesummary_test_run_scoped_summary_does_not_become_a_host": ".test_run_scoped_summary_does_not_become_a_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L672 | neighbors=[ipv6_discovery reports on the RUN (its …, TestEngineSummary]
- "tests_test_probe_core_testgate2_test_never_seen_alive": ".test_never_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L277 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate2_test_ot_always_false": ".test_ot_always_false()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L289 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate2_test_recently_seen_alive": ".test_recently_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L281 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate2_test_stale_seen_alive": ".test_stale_seen_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L285 | neighbors=[TestGate2, _asset()]
- "tests_test_probe_core_testgate3_test_not_alive": ".test_not_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L299 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate3_test_ot_always_false": ".test_ot_always_false()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L303 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate3_test_requires_alive": ".test_requires_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L295 | neighbors=[TestGate3, _asset()]
- "tests_test_probe_core_testgate4_test_all_closed": ".test_all_closed()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L317 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate4_test_no_open_ports": ".test_no_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L313 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate4_test_with_open_ports": ".test_with_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L309 | neighbors=[TestGate4, _asset()]
- "tests_test_probe_core_testgate5_test_dynamically_routed_overrides_port": ".test_dynamically_routed_overrides_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L343 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_explicit_snmp_does_not_require_tcp_liveness": ".test_explicit_snmp_does_not_require_tcp_liveness()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L359 | neighbors=[TestGate5, _asset()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-160.json

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
