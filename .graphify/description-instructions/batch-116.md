# Node Description Batch 117 of 332

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

- "tests_test_remediation_generator_testgenerateremediationplan_gen": "._gen()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L117 | neighbors=[TestGenerateRemediationPlan, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_test_unparseable_output_raises_value_error": ".test_unparseable_output_raises_value_error()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L122 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testgenerateremediationplan_test_valid_output_returns_ai_plan_with_model": ".test_valid_output_returns_ai_plan_with_model()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L127 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testsafecommands": "TestSafeCommands" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L55 | neighbors=[test_remediation_generator.py, .test_drops_destructive_keeps_safe(), .test_null_command_yields_nothing()]
- "tests_test_remediation_kb_testrecipeshape": "TestRecipeShape" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L43 | neighbors=[test_remediation_kb.py, .test_every_recipe_has_required_fields(), .test_every_recipe_step_has_all_os_keys…]
- "tests_test_remediation_routes_genai": "_GenAI" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L85 | neighbors=[test_remediation_routes.py, .generate_remediation_plan(), .__init__()]
- "tests_test_remediation_routes_returning_row": "_returning_row()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L60 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…]
- "tests_test_remediation_routes_testgetremediation_test_cross_tenant_is_404": ".test_cross_tenant_is_404()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L136 | neighbors=[TestGetRemediation, _db_scalar(), _operator()]
- "tests_test_remediation_upsert_integration_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L55 | neighbors=[test_remediation_upsert_integration.py, _stmt(), test_upsert_resets_gate_and_is_race_saf…]
- "tests_test_resolution_apply_test_covered_clean_medium_finding_is_auto_resolved": "test_covered_clean_medium_finding_is_auto_resolved()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L35 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_db_version_change_blocks_resolution": "test_db_version_change_blocks_resolution()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L64 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_resolution_apply_test_uncovered_finding_is_left_open": "test_uncovered_finding_is_left_open()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L51 | neighbors=[test_resolution_apply.py, _db_returning(), _finding()]
- "tests_test_result_spool_spool": "spool()" | kind=code-symbol | source=probe/tests/test_result_spool.py:L13 | neighbors=[test_result_spool.py, ResultSpool with tiny retry delay for f…, ResultSpool with tiny retry delay for f…]
- "tests_test_risk_port_coverage_port_intel": "_port_intel()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L35 | neighbors=[test_risk_port_coverage.py, _risk_ports(), test_every_backdoor_port_is_swept()]
- "tests_test_risk_port_coverage_test_branch_tables_still_contribute": "test_branch_tables_still_contribute()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L109 | neighbors=[test_risk_port_coverage.py, The sweep is profile catalog UNION the …, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_datagram_branch_ports_are_not_in_the_tcp_sweep": "test_datagram_branch_ports_are_not_in_the_tcp_sweep()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L127 | neighbors=[test_risk_port_coverage.py, The complement of the rule above, pinne…, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_network_va_scans_every_port_the_risk_catalog_knows": "test_network_va_scans_every_port_the_risk_catalog_knows()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L60 | neighbors=[test_risk_port_coverage.py, _risk_ports(), _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_sweep_stays_within_a_sane_budget": "test_sweep_stays_within_a_sane_budget()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L100 | neighbors=[test_risk_port_coverage.py, A connect scan is one socket per port p…, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_va_risk_ports_are_all_actually_in_the_risk_catalog": "test_va_risk_ports_are_all_actually_in_the_risk_catalog()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L80 | neighbors=[test_risk_port_coverage.py, Reverse direction: VA_RISK_PORTS must n…, _risk_ports()]
- "tests_test_router_signals_open": "_open()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L20 | neighbors=[test_router_signals.py, test_https_on_odd_port_routes_tls_and_w…, .test_binary_protocol_ports_route_nowhe…]
- "tests_test_router_signals_testwebschemes": "TestWebSchemes" | kind=code-symbol | source=probe/tests/test_router_signals.py:L59 | neighbors=[test_router_signals.py, .test_observed_tls_prefers_https(), .test_static_table_still_applies()]
- "tests_test_rsync_scanner_testrsyncscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L80 | neighbors=[TestRsyncScanner, .test_anon_modules_open(), .test_no_rsync_filtered()]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt_test_a_real_result_with_one_run_scoped_fact_is_accepted_whole": ".test_a_real_result_with_one_run_scoped_fact_is_accepted_whole()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L58 | neighbors=[The damage was collateral: one non-host…, TestRunScopedFactsAreExempt, _fact()]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt_test_ipv6_discovery_auto_target_is_not_rejected": ".test_ipv6_discovery_auto_target_is_not_rejected()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L44 | neighbors=[The exact payload that caused the 422., TestRunScopedFactsAreExempt, _fact()]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt_test_ipv6_discovery_interface_name_is_not_rejected": ".test_ipv6_discovery_interface_name_is_not_rejected()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L49 | neighbors=[Same record, but an interface actually …, TestRunScopedFactsAreExempt, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_an_unknown_scanner_gets_no_exemption": ".test_an_unknown_scanner_gets_no_exemption()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L88 | neighbors=[Only the documented run-scoped scanners…, TestTheScopeGateStillWorks, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_hostname_target_is_still_refused": ".test_hostname_target_is_still_refused()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L102 | neighbors=[Authorization is IP/CIDR-only; a hostna…, TestTheScopeGateStillWorks, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_run_scoped_name_does_not_launder_an_out_of_scope_host": ".test_run_scoped_name_does_not_launder_an_out_of_scope_host()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L94 | neighbors=[The exemption skips the record entirely…, TestTheScopeGateStillWorks, _fact()]
- "tests_test_run_scoped_fact_scope_testthescopegatestillworks_test_scanner_control_record_exemption_is_unchanged": ".test_scanner_control_record_exemption_is_unchanged()" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L111 | neighbors=[The pre-existing <nmap-run> exemption t…, TestTheScopeGateStillWorks, _fact()]
- "tests_test_runtime_requirements_coverage_test_runtime_is_a_subset_of_the_development_set": "test_runtime_is_a_subset_of_the_development_set()" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L66 | neighbors=[test_runtime_requirements_coverage.py, A package shipped in the image but abse…, _declared()]
- "tests_test_scan_funnel_recordingdeep": "RecordingDeep" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L49 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target()]
- "tests_test_scan_funnel_testreconcileports": "TestReconcilePorts" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L221 | neighbors=[test_scan_funnel.py, .test_ignores_non_ints_and_empty(), .test_union_dedup_sorted()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_all_silent_host_shrinks_the_window": ".test_all_silent_host_shrinks_the_window()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L150 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_congestion_can_be_disabled": ".test_congestion_can_be_disabled()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L185 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_scan_completes_every_port_under_throttling": ".test_scan_completes_every_port_under_throttling()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L174 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_absurd_values_are_rejected": ".test_absurd_values_are_rejected()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L275 | neighbors=[TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_maxseg_is_reported_but_never_as_advertised_mss": ".test_maxseg_is_reported_but_never_as_advertised_mss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L231 | neighbors=[TCP_MAXSEG on an ESTABLISHED socket is …, TestHarvestTcpStack, _FakeSock]
- "tests_test_scanner_congestion_testharvesttcpstack_test_tcp_info_yields_wscale_rtt_and_advmss": ".test_tcp_info_yields_wscale_rtt_and_advmss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L249 | neighbors=[TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_timestamped_ethernet_host_is_not_mislabelled_a_tunnel": ".test_timestamped_ethernet_host_is_not_mislabelled_a_tunnel()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L241 | neighbors=[End-to-end form of the same guarantee, …, TestHarvestTcpStack, _FakeSock]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_cleanup_raises_the_timeout_floor": ".test_cleanup_raises_the_timeout_floor()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L414 | neighbors=[A converged estimator can be tuned to a…, TestReprobeCleanupPass, _scanner()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-116.json

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
