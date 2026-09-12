# Node Description Batch 132 of 380

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

- "tests_test_risk_port_coverage_port_intel": "_port_intel()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L35 | neighbors=[test_risk_port_coverage.py, _risk_ports(), test_every_backdoor_port_is_swept()]
- "tests_test_risk_port_coverage_test_branch_tables_still_contribute": "test_branch_tables_still_contribute()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L109 | neighbors=[test_risk_port_coverage.py, The sweep is profile catalog UNION the …, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_datagram_branch_ports_are_not_in_the_tcp_sweep": "test_datagram_branch_ports_are_not_in_the_tcp_sweep()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L127 | neighbors=[test_risk_port_coverage.py, The complement of the rule above, pinne…, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_network_va_scans_every_port_the_risk_catalog_knows": "test_network_va_scans_every_port_the_risk_catalog_knows()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L60 | neighbors=[test_risk_port_coverage.py, _risk_ports(), _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_sweep_stays_within_a_sane_budget": "test_sweep_stays_within_a_sane_budget()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L100 | neighbors=[test_risk_port_coverage.py, A connect scan is one socket per port p…, _swept_by_network_va()]
- "tests_test_risk_port_coverage_test_va_risk_ports_are_all_actually_in_the_risk_catalog": "test_va_risk_ports_are_all_actually_in_the_risk_catalog()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L80 | neighbors=[test_risk_port_coverage.py, Reverse direction: VA_RISK_PORTS must n…, _risk_ports()]
- "tests_test_router_signals_open": "_open()" | kind=code-symbol | source=probe/tests/test_router_signals.py:L20 | neighbors=[test_router_signals.py, test_https_on_odd_port_routes_tls_and_w…, .test_binary_protocol_ports_route_nowhe…]
- "tests_test_router_signals_testwebschemes": "TestWebSchemes" | kind=code-symbol | source=probe/tests/test_router_signals.py:L59 | neighbors=[test_router_signals.py, .test_observed_tls_prefers_https(), .test_static_table_still_applies()]
- "tests_test_rsync_scanner_testrsyncscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L80 | neighbors=[TestRsyncScanner, .test_anon_modules_open(), .test_no_rsync_filtered()]
- "tests_test_run_delta_new_testnewfindingsaresurfaced_test_missing_first_seen_is_not_claimed_as_new": ".test_missing_first_seen_is_not_claimed_as_new()" | kind=code-symbol | source=manager/backend/tests/test_run_delta_new.py:L69 | neighbors=[Legacy rows predate the time series; ca…, TestNewFindingsAreSurfaced, _finding()]
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
- "tests_test_scan_schedule_api_testinputvalidation_test_interval_below_one_hour_is_refused": ".test_interval_below_one_hour_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L57 | neighbors=[A 1-minute deep-scan schedule queues fa…, TestInputValidation, _body()]
- "tests_test_scan_schedule_api_testlistanddelete": "TestListAndDelete" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L118 | neighbors=[test_scan_schedule_api.py, .test_delete_missing_schedule_is_404(), .test_list_returns_schedules()]
- "tests_test_scan_schedule_api_testlistanddelete_test_delete_missing_schedule_is_404": ".test_delete_missing_schedule_is_404()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L129 | neighbors=[TestListAndDelete, _db(), _user()]
- "tests_test_scan_schedule_api_testlistanddelete_test_list_returns_schedules": ".test_list_returns_schedules()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L120 | neighbors=[TestListAndDelete, _db(), _user()]
- "tests_test_scan_schedule_api_testpause": "TestPause" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L135 | neighbors=[test_scan_schedule_api.py, .test_interval_can_be_changed(), .test_schedule_can_be_disabled_without_…]
- "tests_test_scan_schedule_api_testpause_test_interval_can_be_changed": ".test_interval_can_be_changed()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L150 | neighbors=[TestPause, _db(), _user()]
- "tests_test_scanner_congestion_testcollapserecovery_test_backoff_is_still_meaningful": ".test_backoff_is_still_meaningful()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L585 | neighbors=[The floor must not neuter congestion co…, TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testcollapserecovery_test_floor_scales_with_concurrency": ".test_floor_scales_with_concurrency()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L590 | neighbors=[port_scanner derives the floor from con…, TestCollapseRecovery, _scanner()]
- "tests_test_scanner_congestion_testcollapserecovery_test_old_behaviour_was_slow": ".test_old_behaviour_was_slow()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L570 | neighbors=[Documents the regression: without the f…, TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testcollapserecovery_test_recovery_to_usable_throughput_is_faster": ".test_recovery_to_usable_throughput_is_faster()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L560 | neighbors=[Measured: 80 successes with the floors …, TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testcollapserecovery_test_ssthresh_keeps_a_slow_start_runway": ".test_ssthresh_keeps_a_slow_start_runway()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L543 | neighbors=[The floor is tied to min_window (2x), N…, TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testcollapserecovery_test_window_never_fully_serialises": ".test_window_never_fully_serialises()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L555 | neighbors=[A window of 1 turns a 65,535-port sweep…, TestCollapseRecovery, ._collapsed()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_all_silent_host_shrinks_the_window": ".test_all_silent_host_shrinks_the_window()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L151 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_congestion_can_be_disabled": ".test_congestion_can_be_disabled()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L186 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_test_scan_completes_every_port_under_throttling": ".test_scan_completes_every_port_under_throttling()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L175 | neighbors=[TestConnectCongestionWindow, _scanner(), ._silent()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_each_scan_owns_its_delivery_window": ".test_each_scan_owns_its_delivery_window()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L496 | neighbors=[One quiet host must not throttle the ne…, TestDeliveryAwareBackoff, _scanner()]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_window_resets_between_hosts": ".test_window_resets_between_hosts()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L489 | neighbors=[One quiet host must not throttle the ne…, TestDeliveryAwareBackoff, _scanner()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_absurd_values_are_rejected": ".test_absurd_values_are_rejected()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L276 | neighbors=[TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testharvesttcpstack_test_tcp_info_yields_wscale_rtt_and_advmss": ".test_tcp_info_yields_wscale_rtt_and_advmss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L250 | neighbors=[TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_no_ambiguous_ports_means_no_cleanup_pass": ".test_no_ambiguous_ports_means_no_cleanup_pass()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L406 | neighbors=[TestReprobeCleanupPass, _scanner(), ._summary()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-131.json

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
