# Node Description Batch 163 of 332

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

- "tests_test_rsync_scanner_testhandshake_test_greeting_is_echoed_verbatim_including_digest_list": ".test_greeting_is_echoed_verbatim_including_digest_list()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L57 | neighbors=[TestHandshake, _FakeSock]
- "tests_test_rsync_scanner_testhandshake_test_legacy_greeting_without_digest_list_still_works": ".test_legacy_greeting_without_digest_list_still_works()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L63 | neighbors=[TestHandshake, _FakeSock]
- "tests_test_rsync_scanner_testhandshake_test_non_rsync_greeting_returns_none_and_sends_nothing": ".test_non_rsync_greeting_returns_none_and_sends_nothing()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L73 | neighbors=[TestHandshake, _FakeSock]
- "tests_test_rsync_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L120 | neighbors=[test_rsync_scanner.py, .test_main_scripts()]
- "tests_test_rsync_scanner_testrsyncfindings_test_anon_modules_high": ".test_anon_modules_high()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L104 | neighbors=[TestRsyncFindings, ._fact()]
- "tests_test_rsync_scanner_testrsyncfindings_test_auth_only_is_low_disclosure": ".test_auth_only_is_low_disclosure()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L109 | neighbors=[TestRsyncFindings, ._fact()]
- "tests_test_rsync_scanner_testrsyncfindings_test_no_modules_silent": ".test_no_modules_silent()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L115 | neighbors=[TestRsyncFindings, ._fact()]
- "tests_test_rsync_scanner_testrsyncscanner_test_anon_modules_open": ".test_anon_modules_open()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L84 | neighbors=[TestRsyncScanner, ._sc()]
- "tests_test_rsync_scanner_testrsyncscanner_test_no_rsync_filtered": ".test_no_rsync_filtered()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L93 | neighbors=[TestRsyncScanner, ._sc()]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt_test_run_scoped_fact_is_not_collected_as_an_identity": ".test_run_scoped_fact_is_not_collected_as_an_identity()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L54 | neighbors=[TestRunScopedFactsAreExempt, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_excluded_cidr_still_wins": ".test_excluded_cidr_still_wins()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L107 | neighbors=[TestTheScopeGateStillWorks, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_out_of_scope_host_fact_is_still_rejected": ".test_out_of_scope_host_fact_is_still_rejected()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L75 | neighbors=[TestTheScopeGateStillWorks, _fact()]
- "tests_test_runtime_requirements_coverage_test_runtime_image_installs_every_wired_branch_dependency": "test_runtime_image_installs_every_wired_branch_dependency()" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L56 | neighbors=[test_runtime_requirements_coverage.py, _declared()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_constructs_and_wires_real_scanners": ".test_constructs_and_wires_real_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L193 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_port_scanner_is_syn_scanner": ".test_port_scanner_is_syn_scanner()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L203 | neighbors=[TestBuildDefaultFunnel, _scope()]
- "tests_test_scan_funnel_testrpcreconcile_test_advertised_ports_are_scanned_and_only_reachable_confirmed": ".test_advertised_ports_are_scanned_and_only_reachable_confirmed()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L278 | neighbors=[TestRpcReconcile, ._funnel()]
- "tests_test_scan_funnel_testrpcreconcile_test_no_dynamic_ports_no_reconcile_stage": ".test_no_dynamic_ports_no_reconcile_stage()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L297 | neighbors=[TestRpcReconcile, ._funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_invoked_with_db_port": ".test_db_scanner_invoked_with_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L156 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_db_scanner_not_invoked_without_db_port": ".test_db_scanner_not_invoked_without_db_port()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L151 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_forced_runs_full": ".test_dead_host_forced_runs_full()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L132 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_dead_host_skips_port_scan": ".test_dead_host_skips_port_scan()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L122 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_deep_scanner_receives_only_open_ports": ".test_deep_scanner_receives_only_open_ports()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L144 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_no_open_ports_runs_no_deep_scanners": ".test_no_open_ports_runs_no_deep_scanners()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L162 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_open_ports_extracted": ".test_open_ports_extracted()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L139 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_out_of_scope_target": ".test_out_of_scope_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L177 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_results_aggregate_all_stages": ".test_results_aggregate_all_stages()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L169 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnel_test_stages_run_order": ".test_stages_run_order()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L183 | neighbors=[TestScanFunnel, _make_funnel()]
- "tests_test_scan_funnel_testscanfunnelrun": "TestScanFunnelRun" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L304 | neighbors=[test_scan_funnel.py, .test_run_writes_all_results()]
- "tests_test_scan_funnel_testscanfunnelrun_test_run_writes_all_results": ".test_run_writes_all_results()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L305 | neighbors=[TestScanFunnelRun, _make_funnel()]
- "tests_test_scan_health_test_clean_scan_is_healthy_and_does_not_warn": "test_clean_scan_is_healthy_and_does_not_warn()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L17 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scan_health_test_local_resource_errors_flag_degraded": "test_local_resource_errors_flag_degraded()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L24 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scan_health_test_missing_ports_flag_incomplete": "test_missing_ports_flag_incomplete()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L32 | neighbors=[test_scan_health.py, _summary()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_responsive_host_is_not_throttled": ".test_responsive_host_is_not_throttled()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L162 | neighbors=[TestConnectCongestionWindow, _scanner()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_short_tcp_info_buffer_is_ignored": ".test_short_tcp_info_buffer_is_ignored()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L258 | neighbors=[TestHarvestTcpStack, _FakeSock]
- "tests_test_scanner_congestion_testreprobecleanuppass_silent_attempt": "._silent_attempt()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L378 | neighbors=[TestReprobeCleanupPass, .test_genuinely_filtered_ports_stay_fil…]
- "tests_test_scanner_congestion_testresolvecandidates_test_deduplicates_repeated_addresses": ".test_deduplicates_repeated_addresses()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L301 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_congestion_testresolvecandidates_test_family_filter_restricts_results": ".test_family_filter_restricts_results()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L312 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_congestion_testresolvecandidates_test_returns_every_family_in_order": ".test_returns_every_family_in_order()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L296 | neighbors=[TestResolveCandidates, _fake_gai()]
- "tests_test_scanner_parity_test_scanner_module_matches_main_scripts": "test_scanner_module_matches_main_scripts()" | kind=code-symbol | source=probe/tests/test_scanner_parity.py:L48 | neighbors=[test_scanner_parity.py, Each scanner/<mod>.py is byte-identical…]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_multiple_encrypts_different": ".test_multiple_encrypts_different()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L78 | neighbors=[Each encryption uses a fresh ephemeral …, TestEncryptDecryptRoundtrip]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-162.json

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
