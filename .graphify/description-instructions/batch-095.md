# Node Description Batch 96 of 380

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

- "tests_test_run_delta_new_testendpointshape": "TestEndpointShape" | kind=code-symbol | source=manager/backend/tests/test_run_delta_new.py:L79 | neighbors=[test_run_delta_new.py, ._db(), .test_delta_reports_both_halves(), .test_no_runs_short_circuits_before_que…]
- "tests_test_run_delta_new_testendpointshape_test_delta_reports_both_halves": ".test_delta_reports_both_halves()" | kind=code-symbol | source=manager/backend/tests/test_run_delta_new.py:L91 | neighbors=[TestEndpointShape, _finding(), _run(), ._db()]
- "tests_test_run_delta_new_testnewfindingsaresurfaced_test_finding_first_seen_exactly_at_run_start_counts_as_new": ".test_finding_first_seen_exactly_at_run_start_counts_as_new()" | kind=code-symbol | source=manager/backend/tests/test_run_delta_new.py:L62 | neighbors=[The run's own findings share its start …, TestNewFindingsAreSurfaced, _finding(), _run()]
- "tests_test_run_delta_new_testnewfindingsaresurfaced_test_helper_selects_only_findings_first_seen_in_this_run": ".test_helper_selects_only_findings_first_seen_in_this_run()" | kind=code-symbol | source=manager/backend/tests/test_run_delta_new.py:L52 | neighbors=[A finding carried over from an earlier …, TestNewFindingsAreSurfaced, _finding(), _run()]
- "tests_test_runtime_requirements_coverage_declared": "_declared()" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L42 | neighbors=[test_runtime_requirements_coverage.py, Package names declared in a requirement…, test_runtime_image_installs_every_wired…, test_runtime_is_a_subset_of_the_develop…]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L36 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L192 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testrpcreconcile": "TestRpcReconcile" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L266 | neighbors=[test_scan_funnel.py, ._funnel(), .test_advertised_ports_are_scanned_and_…, .test_no_dynamic_ports_no_reconcile_sta…]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scan_schedule_api_testcreate_test_creator_is_recorded": ".test_creator_is_recorded()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L111 | neighbors=[TestCreate, _body(), _db(), _user()]
- "tests_test_scan_schedule_api_testcreate_test_unknown_engagement_is_404": ".test_unknown_engagement_is_404()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L92 | neighbors=[TestCreate, _body(), _db(), _user()]
- "tests_test_scan_schedule_api_testpause_test_schedule_can_be_disabled_without_deletion": ".test_schedule_can_be_disabled_without_deletion()" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_api.py:L137 | neighbors=[Pausing during a change freeze is routi…, TestPause, _db(), _user()]
- "tests_test_scan_schedule_model": "test_scan_schedule_model.py" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L1 | neighbors=[e80b25f feat(scheduling): ScanSchedule …, TestColumns, TestRelationshipSafety, ScanSchedule: the table behind recurrin…]
- "tests_test_scan_schedule_model_testrelationshipsafety": "TestRelationshipSafety" | kind=code-symbol | source=manager/backend/tests/test_scan_schedule_model.py:L51 | neighbors=[test_scan_schedule_model.py, .test_created_by_survives_user_deletion…, .test_engagement_deletion_removes_the_s…, .test_is_registered_in_the_model_aggreg…]
- "tests_test_scanner_congestion_testconnectcongestionwindow_silent": "._silent()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L146 | neighbors=[TestConnectCongestionWindow, .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_scan_completes_every_port_under_t…]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_collapsed_delivery_still_backs_off": ".test_collapsed_delivery_still_backs_off()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L454 | neighbors=[A genuinely lossy path (verified separa…, TestDeliveryAwareBackoff, ._sc(), A genuinely lossy path (verified separa…]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_mostly_answering_host_is_not_treated_as_congested": ".test_mostly_answering_host_is_not_treated_as_congested()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L445 | neighbors=[~97% definitive (the measured RST-suppr…, TestDeliveryAwareBackoff, ._sc(), ~97% definitive (the measured RST-suppr…]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_no_opinion_before_the_sample_floor": ".test_no_opinion_before_the_sample_floor()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L463 | neighbors=[Never throttle on a handful of early pr…, TestDeliveryAwareBackoff, ._sc(), Never throttle on a handful of early pr…]
- "tests_test_scanner_congestion_testdeliveryawarebackoff_test_recovery_after_a_bad_patch": ".test_recovery_after_a_bad_patch()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L477 | neighbors=[Delivery returning must clear the loss …, TestDeliveryAwareBackoff, ._sc(), Delivery returning must clear the loss …]
- "tests_test_scanner_congestion_testharvesttcpstack_test_maxseg_is_reported_but_never_as_advertised_mss": ".test_maxseg_is_reported_but_never_as_advertised_mss()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L232 | neighbors=[TCP_MAXSEG on an ESTABLISHED socket is …, TestHarvestTcpStack, _FakeSock, TCP_MAXSEG on an ESTABLISHED socket is …]
- "tests_test_scanner_congestion_testharvesttcpstack_test_timestamped_ethernet_host_is_not_mislabelled_a_tunnel": ".test_timestamped_ethernet_host_is_not_mislabelled_a_tunnel()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L242 | neighbors=[End-to-end form of the same guarantee, …, TestHarvestTcpStack, _FakeSock, End-to-end form of the same guarantee, …]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_cleanup_raises_the_timeout_floor": ".test_cleanup_raises_the_timeout_floor()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L415 | neighbors=[A converged estimator can be tuned to a…, TestReprobeCleanupPass, _scanner(), A converged estimator can be tuned to a…]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_disabled_reprobe_leaves_false_filtered_in_place": ".test_disabled_reprobe_leaves_false_filtered_in_place()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L397 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_genuinely_filtered_ports_stay_filtered": ".test_genuinely_filtered_ports_stay_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L369 | neighbors=[TestReprobeCleanupPass, _scanner(), ._silent_attempt(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_recovers_ports_the_fast_sweep_called_filtered": ".test_recovers_ports_the_fast_sweep_called_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L356 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scanner_congestion_testresolvecandidates_test_v4_is_reachable_even_when_aaaa_sorts_first": ".test_v4_is_reachable_even_when_aaaa_sorts_first()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L306 | neighbors=[The false negative #9 exists to kill: a…, TestResolveCandidates, _fake_gai(), The false negative #9 exists to kill: a…]
- "tests_test_scheduler_testadvance": "TestAdvance" | kind=code-symbol | source=manager/backend/tests/test_scheduler.py:L64 | neighbors=[test_scheduler.py, .test_advances_from_now_not_from_the_mi…, .test_is_never_left_in_the_past(), .test_sets_last_run_and_next_by_interva…]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_self_scan_fakequeue": "FakeQueue" | kind=code-symbol | source=probe/tests/test_self_scan.py:L35 | neighbors=[test_self_scan.py, .enqueue(), .__init__(), test_execute_writes_scope_runs_engine_a…]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_service_posture_rules_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L28 | neighbors=[test_service_posture_rules.py, _fire(), test_experimental_scanner_findings_are_…, .test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_test_smb_null_session_is_silent_on_the_live_host": "test_smb_null_session_is_silent_on_the_live_host()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L98 | neighbors=[test_service_posture_rules.py, The live host REFUSED the null bind (ST…, _corpus(), _fire()]
- "tests_test_service_posture_rules_test_ssh_rules_against_live_capture": "test_ssh_rules_against_live_capture()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L72 | neighbors=[test_service_posture_rules.py, The live Windows host offers OpenSSH 9.…, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnonla_test_fires_from_the_second_probe_when_the_first_failed": ".test_fires_from_the_second_probe_when_the_first_failed()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L167 | neighbors=[The live-host case: negotiation returne…, TestRdpNoNla, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnotls": "TestRdpNoTls" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L198 | neighbors=[test_service_posture_rules.py, .test_fires_on_ssl_not_allowed(), .test_ignores_uninterpreted_failure_cod…, .test_silent_when_negotiation_succeeded…]
- "tests_test_servicenow_integration_testregistration": "TestRegistration" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L25 | neighbors=[test_servicenow_integration.py, .test_existing_kinds_are_untouched(), .test_sender_is_registered_for_dispatch…, .test_servicenow_is_an_accepted_kind()]
- "tests_test_sla_policy_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L32 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_custom_when_row_present": ".test_get_custom_when_row_present()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L58 | neighbors=[TestSlaPolicyRoutes, _db(), _operator(), _row()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
