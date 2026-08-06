# Node Description Batch 71 of 134

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

- "tests_test_outbox_reclaim_test_reclaim_handles_none_rowcount_from_driver": "test_reclaim_handles_none_rowcount_from_driver()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L136 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_reclaim_is_noop_when_nothing_is_stranded": "test_reclaim_is_noop_when_nothing_is_stranded()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L127 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_reclaim_runs_both_sweeps_commits_and_sums_rowcounts": "test_reclaim_runs_both_sweeps_commits_and_sums_rowcounts()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L115 | neighbors=[test_outbox_reclaim.py, _mock_session()]
- "tests_test_outbox_reclaim_test_stale_cutoff_is_now_minus_lease": "test_stale_cutoff_is_now_minus_lease()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L60 | neighbors=[test_outbox_reclaim.py, _now()]
- "tests_test_passive_collector_socket_close": ".close()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L31 | neighbors=[_Socket, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_passive_collector_test_collector_raises_when_no_listener_binds": "test_collector_raises_when_no_listener_binds()" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L165 | neighbors=[test_passive_collector.py, _Writer]
- "tests_test_posture_test_build_posture_buckets_resolved_new_persisting": "test_build_posture_buckets_resolved_new_persisting()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L89 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_build_posture_single_run_has_no_prev": "test_build_posture_single_run_has_no_prev()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L76 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_compute_scores_uses_risk_epss_exploit_and_asset_criticality": "test_compute_scores_uses_risk_epss_exploit_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L53 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_finding_views_handles_null_asset_and_scores": "test_finding_views_handles_null_asset_and_scores()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L128 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_test_finding_views_maps_columns_and_asset_criticality": "test_finding_views_maps_columns_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L114 | neighbors=[test_posture.py, _Row]
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
- "tests_test_probe_core_testcacheentry": "TestCacheEntry" | kind=code-symbol | source=probe/tests/test_probe_core.py:L732 | neighbors=[test_probe_core.py, .test_roundtrip()]
- "tests_test_probe_core_testcacheentry_test_roundtrip": ".test_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L733 | neighbors=[TestCacheEntry, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_error_overrides": ".test_error_overrides()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L723 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_host_discovery_uncertain": ".test_host_discovery_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L719 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_service_banner_deterministic": ".test_service_banner_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L715 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_tcp_port_scan_deterministic": ".test_tcp_port_scan_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L707 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_udp_port_scan_uncertain": ".test_udp_port_scan_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L711 | neighbors=[TestClassifyCertainty, _scan_result()]
- "tests_test_probe_core_testclassifycertainty_test_unknown_scanner_conservative": ".test_unknown_scanner_conservative()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L727 | neighbors=[TestClassifyCertainty, _scan_result()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-070.json

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
