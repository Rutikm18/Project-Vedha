# Node Description Batch 160 of 332

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
- "tests_test_probe_core_testgate5_test_iot_profile_no_smb": ".test_iot_profile_no_smb()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L327 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_it_profile_tls_with_tls_port": ".test_it_profile_tls_with_tls_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L323 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_mcp_ai_allowed_on_it_ai_port": ".test_mcp_ai_allowed_on_it_ai_port()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L351 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_no_matching_ports": ".test_no_matching_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L347 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_ot_no_branches": ".test_ot_no_branches()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L331 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_allows": ".test_service_filter_allows()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L339 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_service_filter_blocks": ".test_service_filter_blocks()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L335 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_allowed_on_live_it_host": ".test_snmp_allowed_on_live_it_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L355 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate5_test_snmp_not_allowed_on_iot_profile": ".test_snmp_not_allowed_on_iot_profile()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L363 | neighbors=[TestGate5, _asset()]
- "tests_test_probe_core_testgate6_test_already_collected": ".test_already_collected()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L377 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_no_creds": ".test_no_creds()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L369 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_not_alive": ".test_not_alive()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L381 | neighbors=[TestGate6, _asset()]
- "tests_test_probe_core_testgate6_test_ssh_creds_alive_uncollected": ".test_ssh_creds_alive_uncollected()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L373 | neighbors=[TestGate6, _asset()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-159.json

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
