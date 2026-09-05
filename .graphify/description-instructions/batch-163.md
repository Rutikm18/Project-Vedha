# Node Description Batch 164 of 336

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

- "tests_test_result_archive_testprepareatstartup_test_existing_but_unwritable_directory_is_caught_at_startup": ".test_existing_but_unwritable_directory_is_caught_at_startup()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L184 | neighbors=[The Linux bind-mount case: Docker creat…, TestPrepareAtStartup]
- "tests_test_risk_port_coverage_test_named_high_value_ports_are_scanned": "test_named_high_value_ports_are_scanned()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L151 | neighbors=[test_risk_port_coverage.py, _swept_by_network_va()]
- "tests_test_risk_rank_test_bounds": "test_bounds()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L15 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_confirmed_exploitable_outranks_contradicted": "test_confirmed_exploitable_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L23 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_contradicted_sinks_below_inferred": "test_contradicted_sinks_below_inferred()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L29 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_internet_facing_raises_and_auth_lowers": "test_internet_facing_raises_and_auth_lowers()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L37 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_kev_raises_rank": "test_kev_raises_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L33 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_low_confidence_lowers_rank": "test_low_confidence_lowers_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L42 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_risk_rank_test_severity_remains_an_impact_signal_without_cvss": "test_severity_remains_an_impact_signal_without_cvss()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L72 | neighbors=[test_risk_rank.py, _rank()]
- "tests_test_router_signals_test_https_on_odd_port_routes_tls_and_web": "test_https_on_odd_port_routes_tls_and_web()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L52 | neighbors=[test_router_signals.py, _open()]
- "tests_test_router_signals_test_no_tls_flag_omits_the_marker": "test_no_tls_flag_omits_the_marker()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L161 | neighbors=[test_router_signals.py, --no-tls means no handshake was tried, …]
- "tests_test_router_signals_test_service_banner_records_tls_probed": "test_service_banner_records_tls_probed()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L137 | neighbors=[test_router_signals.py, The flag must actually be emitted, or t…]
- "tests_test_router_signals_test_workflow_hands_observed_tls_ports_to_web_scanner": "test_workflow_hands_observed_tls_ports_to_web_scanner()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L70 | neighbors=[test_router_signals.py, 9000 is in the static WEB table but NOT…]
- "tests_test_router_signals_testtlsprobednegative_test_binary_protocol_ports_route_nowhere": ".test_binary_protocol_ports_route_nowhere()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L129 | neighbors=[TestTlsProbedNegative, _open()]
- "tests_test_rsync_scanner_testhandshake_test_echo_stops_at_the_first_line": ".test_echo_stops_at_the_first_line()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L68 | neighbors=[TestHandshake, _FakeSock]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-163.json

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
