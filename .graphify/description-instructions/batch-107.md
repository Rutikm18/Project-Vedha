# Node Description Batch 108 of 209

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

- "tests_test_probe_core_testroutebranches_test_silent_nonstandard_port_routes_tls": ".test_silent_nonstandard_port_routes_tls()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L427 | neighbors=[TestRouteBranches, _asset()]
- "tests_test_probe_core_testscanresult_test_to_json_roundtrip": ".test_to_json_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L228 | neighbors=[TestScanResult, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_all_entries_for_host": ".test_all_entries_for_host()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L782 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_put_get": ".test_put_get()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L746 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_save_and_load_roundtrip": ".test_save_and_load_roundtrip()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L790 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_deterministic_fresh": ".test_should_recheck_deterministic_fresh()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L768 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_force_expired": ".test_should_recheck_force_expired()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L774 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_core_testworkflowcache_test_should_recheck_uncertain_always": ".test_should_recheck_uncertain_always()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L762 | neighbors=[TestWorkflowCache, _scan_result()]
- "tests_test_probe_enrollment_test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses": "test_enroll_token_usable_only_while_live_unrevoked_and_under_max_uses()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L102 | neighbors=[test_probe_enrollment.py, _token()]
- "tests_test_probe_enrollment_token": "_token()" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L85 | neighbors=[test_probe_enrollment.py, test_enroll_token_usable_only_while_liv…]
- "tests_test_probe_manifest_test_manifest_is_clean_parseable_json": "test_manifest_is_clean_parseable_json()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L30 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_is_deterministic": "test_manifest_is_deterministic()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L47 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_manifest_test_manifest_surfaces_the_capability_contract": "test_manifest_surfaces_the_capability_contract()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L37 | neighbors=[test_probe_manifest.py, _manifest()]
- "tests_test_probe_next_features_test_device_inventory_post_stage_classifies_from_open_ports": "test_device_inventory_post_stage_classifies_from_open_ports()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L110 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_device_inventory_skips_hosts_without_evidence": "test_device_inventory_skips_hosts_without_evidence()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L124 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_flags_internet_reachable_ports": "test_exposure_matrix_flags_internet_reachable_ports()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L135 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_exposure_matrix_internal_only_from_lan_vantage": "test_exposure_matrix_internal_only_from_lan_vantage()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L150 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_probe_next_features_test_no_post_stage_for_ordinary_scan_types": "test_no_post_stage_for_ordinary_scan_types()" | kind=code-symbol | source=probe/tests/test_probe_next_features.py:L161 | neighbors=[test_probe_next_features.py, _cache_with()]
- "tests_test_reaper_test_expired_attempt_fails_job_when_retry_budget_is_exhausted": "test_expired_attempt_fails_job_when_retry_budget_is_exhausted()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L39 | neighbors=[test_reaper.py, _objects()]
- "tests_test_reaper_test_expired_attempt_requeues_with_fence_history_preserved": "test_expired_attempt_requeues_with_fence_history_preserved()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L24 | neighbors=[test_reaper.py, _objects()]
- "tests_test_risk_rank_test_bounds": "test_bounds()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L15 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_confirmed_exploitable_outranks_contradicted": "test_confirmed_exploitable_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L23 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_contradicted_sinks_below_inferred": "test_contradicted_sinks_below_inferred()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L29 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_internet_facing_raises_and_auth_lowers": "test_internet_facing_raises_and_auth_lowers()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L37 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_kev_raises_rank": "test_kev_raises_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L33 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_low_confidence_lowers_rank": "test_low_confidence_lowers_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L42 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_constructs_and_wires_real_scanners": ".test_constructs_and_wires_real_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L191 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_port_scanner_is_syn_scanner": ".test_port_scanner_is_syn_scanner()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L201 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_invoked_with_db_port": ".test_db_scanner_invoked_with_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L154 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_not_invoked_without_db_port": ".test_db_scanner_not_invoked_without_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L149 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_forced_runs_full": ".test_dead_host_forced_runs_full()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L130 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_skips_port_scan": ".test_dead_host_skips_port_scan()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L120 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_deep_scanner_receives_only_open_ports": ".test_deep_scanner_receives_only_open_ports()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L142 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_no_open_ports_runs_no_deep_scanners": ".test_no_open_ports_runs_no_deep_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L160 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_open_ports_extracted": ".test_open_ports_extracted()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L137 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_out_of_scope_target": ".test_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L175 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_results_aggregate_all_stages": ".test_results_aggregate_all_stages()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L167 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_stages_run_order": ".test_stages_run_order()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L181 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnelrun": "TestScanFunnelRun" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L217 | neighbors=[test_scan_funnel.py, .test_run_writes_all_results()]
- "tests_test_scan_funnel_testscanfunnelrun_test_run_writes_all_results": ".test_run_writes_all_results()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L218 | neighbors=[TestScanFunnelRun, _make_funnel()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-107.json

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
