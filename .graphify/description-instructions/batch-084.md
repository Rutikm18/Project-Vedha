# Node Description Batch 85 of 332

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

- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port()]
- "tests_test_resolve": "test_resolve.py" | kind=code-symbol | source=probe/tests/test_resolve.py:L1 | neighbors=[dec1e7c fix(scanner): resolve() family …, _infos(), TestResolveFamily, test_resolve.py — resolve() address-fam…]
- "tests_test_result_archive_testarchiveidentity_test_archived_json_equals_the_submitted_payload": ".test_archived_json_equals_the_submitted_payload()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L67 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_failure_envelopes_are_archived_too": ".test_failure_envelopes_are_archived_too()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L98 | neighbors=[A rejected job is exactly the case an o…, TestArchiveIdentity, _job(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_filename_is_result_plus_timestamp": ".test_filename_is_result_plus_timestamp()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L83 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_no_partial_files_are_left_behind": ".test_no_partial_files_are_left_behind()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L120 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveidentity_test_two_jobs_in_the_same_second_do_not_clobber": ".test_two_jobs_in_the_same_second_do_not_clobber()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L112 | neighbors=[TestArchiveIdentity, _job(), _ok_result(), _runner()]
- "tests_test_result_archive_testarchiveisbesteffort": "TestArchiveIsBestEffort" | kind=code-symbol | source=probe/tests/test_result_archive.py:L128 | neighbors=[test_result_archive.py, .test_default_location_is_the_probe_roo…, .test_empty_env_var_disables_archiving(), .test_unwritable_directory_does_not_fai…]
- "tests_test_result_archive_testarchiveisbesteffort_test_empty_env_var_disables_archiving": ".test_empty_env_var_disables_archiving()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L143 | neighbors=[TestArchiveIsBestEffort, _job(), _ok_result(), _runner()]
- "tests_test_risk_port_coverage_risk_ports": "_risk_ports()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L44 | neighbors=[test_risk_port_coverage.py, _port_intel(), test_network_va_scans_every_port_the_ri…, test_va_risk_ports_are_all_actually_in_…]
- "tests_test_risk_port_coverage_test_every_backdoor_port_is_swept": "test_every_backdoor_port_is_swept()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L71 | neighbors=[test_risk_port_coverage.py, Called out separately: these carry the …, _port_intel(), _swept_by_network_va()]
- "tests_test_router_signals_testpositivetls": "TestPositiveTls" | kind=code-symbol | source=probe/tests/test_router_signals.py:L24 | neighbors=[test_router_signals.py, .test_absence_heuristic_still_works(), .test_alert_record_service_routes(), .test_handshake_fact_routes_even_on_cli…]
- "tests_test_router_signals_teststructuredservice": "TestStructuredService" | kind=code-symbol | source=probe/tests/test_router_signals.py:L37 | neighbors=[test_router_signals.py, .test_db_by_service_field(), .test_http_by_service_field(), .test_ssh_by_service_field()]
- "tests_test_rsync_scanner_testparsemodules": "TestParseModules" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L18 | neighbors=[test_rsync_scanner.py, .test_bounded(), .test_protocol_lines_ignored(), .test_tab_and_space_separated()]
- "tests_test_rsync_scanner_testrsyncfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L100 | neighbors=[TestRsyncFindings, .test_anon_modules_high(), .test_auth_only_is_low_disclosure(), .test_no_modules_silent()]
- "tests_test_rsync_scanner_testrsyncscanner": "TestRsyncScanner" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L79 | neighbors=[test_rsync_scanner.py, ._sc(), .test_anon_modules_open(), .test_no_rsync_filtered()]
- "tests_test_runtime_requirements_coverage_declared": "_declared()" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L42 | neighbors=[test_runtime_requirements_coverage.py, Package names declared in a requirement…, test_runtime_image_installs_every_wired…, test_runtime_is_a_subset_of_the_develop…]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L36 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L192 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testrpcreconcile": "TestRpcReconcile" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L266 | neighbors=[test_scan_funnel.py, ._funnel(), .test_advertised_ports_are_scanned_and_…, .test_no_dynamic_ports_no_reconcile_sta…]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scanner_congestion_testconnectcongestionwindow_silent": "._silent()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L145 | neighbors=[TestConnectCongestionWindow, .test_all_silent_host_shrinks_the_windo…, .test_congestion_can_be_disabled(), .test_scan_completes_every_port_under_t…]
- "tests_test_scanner_congestion_testharvesttcpstack_test_never_synthesizes_an_initial_tcp_window": ".test_never_synthesizes_an_initial_tcp_window()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L263 | neighbors=[THE accuracy guarantee for #6b.        …, TestHarvestTcpStack, _FakeSock, _tcp_info_buf()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_disabled_reprobe_leaves_false_filtered_in_place": ".test_disabled_reprobe_leaves_false_filtered_in_place()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L396 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_genuinely_filtered_ports_stay_filtered": ".test_genuinely_filtered_ports_stay_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L368 | neighbors=[TestReprobeCleanupPass, _scanner(), ._silent_attempt(), ._summary()]
- "tests_test_scanner_congestion_testreprobecleanuppass_test_recovers_ports_the_fast_sweep_called_filtered": ".test_recovers_ports_the_fast_sweep_called_filtered()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L355 | neighbors=[TestReprobeCleanupPass, _scanner(), ._rate_limited(), ._summary()]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_service_posture_rules_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L28 | neighbors=[test_service_posture_rules.py, _fire(), test_experimental_scanner_findings_are_…, .test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_test_smb_null_session_is_silent_on_the_live_host": "test_smb_null_session_is_silent_on_the_live_host()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L98 | neighbors=[test_service_posture_rules.py, The live host REFUSED the null bind (ST…, _corpus(), _fire()]
- "tests_test_service_posture_rules_test_ssh_rules_against_live_capture": "test_ssh_rules_against_live_capture()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L72 | neighbors=[test_service_posture_rules.py, The live Windows host offers OpenSSH 9.…, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnonla_test_fires_from_the_second_probe_when_the_first_failed": ".test_fires_from_the_second_probe_when_the_first_failed()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L167 | neighbors=[The live-host case: negotiation returne…, TestRdpNoNla, _corpus(), _fire()]
- "tests_test_service_posture_rules_testrdpnotls": "TestRdpNoTls" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L198 | neighbors=[test_service_posture_rules.py, .test_fires_on_ssl_not_allowed(), .test_ignores_uninterpreted_failure_cod…, .test_silent_when_negotiation_succeeded…]
- "tests_test_sla_policy_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L32 | neighbors=[test_sla_policy.py, .test_get_custom_when_row_present(), .test_get_env_defaults_when_no_row(), .test_put_creates_when_absent()]
- "tests_test_sla_policy_testslapolicyroutes_test_get_custom_when_row_present": ".test_get_custom_when_row_present()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L58 | neighbors=[TestSlaPolicyRoutes, _db(), _operator(), _row()]
- "tests_test_smb_ldap_scanners_testldaptimeouttypes": "TestLDAPTimeoutTypes" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L135 | neighbors=[test_smb_ldap_scanners.py, ldap3 packs receive_timeout into a stru…, .test_receive_timeout_is_an_int(), .test_sub_second_timeout_does_not_floor…]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing": "TestNtlmFingerprintFraming" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L79 | neighbors=[test_smb_ntlm_build.py, Regression: _recv_smb_frame STRIPS the …, .test_end_to_end_framing_extracts_build…, .test_ntlm_os_build_shared_function()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-084.json

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
