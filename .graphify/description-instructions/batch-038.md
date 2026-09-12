# Node Description Batch 39 of 380

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

- "tests_test_result_archive_job": "_job()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L42 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_failure_envelopes_are_archived_to…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…]
- "tests_test_result_archive_runner": "_runner()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L33 | neighbors=[test_result_archive.py, .test_archived_json_equals_the_submitte…, .test_failure_envelopes_are_archived_to…, .test_filename_is_result_plus_timestamp…, .test_no_partial_files_are_left_behind(), .test_two_jobs_in_the_same_second_do_no…]
- "tests_test_result_archive_testprepareatstartup": "TestPrepareAtStartup" | kind=code-symbol | source=probe/tests/test_result_archive.py:L162 | neighbors=[test_result_archive.py, The agent creates the archive directory…, .test_creates_the_directory_including_p…, .test_disabled_when_env_is_empty(), .test_existing_but_unwritable_directory…, .test_is_idempotent_across_restarts()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, result_spool.py, spool(), TestResultSpool]
- "tests_test_risk_port_coverage_swept_by_network_va": "_swept_by_network_va()" | kind=code-symbol | source=probe/tests/test_risk_port_coverage.py:L53 | neighbors=[test_risk_port_coverage.py, Exactly what a default network_va puts …, test_branch_tables_still_contribute(), test_datagram_branch_ports_are_not_in_t…, test_every_backdoor_port_is_swept(), test_named_high_value_ports_are_scanned…]
- "tests_test_risk_rank_rank": "_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L6 | neighbors=[test_risk_rank.py, test_bounds(), test_confirmed_exploitable_outranks_con…, test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lo…, test_kev_raises_rank()]
- "tests_test_risk_score_contract": "test_risk_score_contract.py" | kind=code-symbol | source=manager/backend/tests/test_risk_score_contract.py:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, test_only_detection_engine_posture_evid…, test_posture_severity_and_evidence_driv…]
- "tests_test_scan_health": "test_scan_health.py" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _summary(), test_aggregates_across_hosts(), test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scanner_congestion_testresolvecandidates": "TestResolveCandidates" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L296 | neighbors=[test_scanner_congestion.py, .test_absent_requested_family_falls_bac…, .test_deduplicates_repeated_addresses(), .test_family_filter_restricts_results(), .test_literal_ip_resolves_to_itself(), .test_returns_every_family_in_order()]
- "tests_test_scope_targets": "test_scope_targets.py" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, test_property_every_accepted_target_is_…, TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected": "TestOutOfScopeIsRejected" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L44 | neighbors=[test_scope_targets.py, .test_blank_token_is_rejected(), .test_cidr_broader_than_scope(), .test_explicit_empty_list_is_rejected(), .test_hostname_is_not_routable(), .test_ip_outside_scope()]
- "tests_test_service": "test_service.py" | kind=code-symbol | source=probe/tests/test_service.py:L1 | neighbors=[de0005e Phase 9: per-OS service install…, test_activation_commands_per_os(), test_install_writes_unit_then_uninstall…, test_launchd_plist_restart_on_failure_o…, test_systemd_unit_has_limits_env_and_st…, test_uninstall_commands_per_os()]
- "tests_test_servicenow_integration_testincidentcreation": "TestIncidentCreation" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L52 | neighbors=[test_servicenow_integration.py, ._config(), .test_authenticates_with_the_stored_sec…, .test_deliver_routes_servicenow_and_rep…, .test_http_failure_propagates_to_delive…, .test_posts_an_incident_to_the_table_ap…]
- "tests_test_sla_policy": "test_sla_policy.py" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, _db(), _finding(), _operator(), _row(), TestPolicyAwareCompute]
- "tests_test_smb_ntlm_build_testparsechallenge": "TestParseChallenge" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L38 | neighbors=[test_smb_ntlm_build.py, .test_legacy_6_1_is_win7(), .test_no_version_field_yields_name_but_…, .test_non_challenge_returns_none(), .test_server_2022_build_20348(), .test_unknown_build_still_classified_wi…]
- "tests_test_syn_budget_wiring": "test_syn_budget_wiring.py" | kind=code-symbol | source=probe/tests/test_syn_budget_wiring.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, scanner_base.py, _scope(), TestEngineWiresTheBudgetIntoTheSynScann…, TestFallbackCarriesTheBudget, TestRawPathStopsAtTheDeadline]
- "tests_test_syn_scanner_testbuildresultsenrichment": "TestBuildResultsEnrichment" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L349 | neighbors=[test_syn_scanner.py, ._scanner(), .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_os_guess_is_tagged_tcp_derived_no…]
- "tests_test_tier1_correlations": "test_tier1_correlations.py" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L1 | neighbors=[6e2818f Add support for additional serv…, _run(), test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_…, test_mgmt_plane_needs_two_when_no_ciphe…, test_single_anon_finding_does_not_corre…]
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_legacy_versions_legacytlsserver": "_LegacyTLSServer" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L55 | neighbors=[test_tls_legacy_versions.py, .__enter__(), .__exit__(), .__init__(), ._serve(), A loopback server pinned to exactly one…]
- "tests_test_tls_port_coverage": "test_tls_port_coverage.py" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, service_enum.py, test_refused_handshake_is_an_error_not_…, TestDeliberateExclusions, TestSingleSourceOfTruth, TestWidenedCoverage]
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "tests_test_transport_testdeviceenrollment": "TestDeviceEnrollment" | kind=code-symbol | source=probe/tests/test_transport.py:L199 | neighbors=[test_transport.py, .test_activation_persists_recoverable_d…, .test_create_enrollment_request_409_rai…, .test_create_enrollment_request_409_wit…, .test_create_enrollment_request_forward…, .test_device_refresh_signs_unique_nonce…]
- "tests_test_verification_kb": "test_verification_kb.py" | kind=code-symbol | source=manager/backend/tests/test_verification_kb.py:L1 | neighbors=[c6420a6 Add deterministic verification …, F(), test_anon_ftp_retest_attempts_the_login…, test_detection_coverage_is_not_consulte…, test_detection_method_from_validation_s…, test_generic_fallback_always_has_a_pass…]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L207 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, Push a job to the first online agent in…, Push a job to the first online agent in…]
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L51 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()]
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L367 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L98 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), gate_4b_os_fingerprint(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…]
- "workflow_host_health_hosthealthmonitor_state": "._state()" | kind=code-symbol | source=probe/workflow/host_health.py:L129 | neighbors=[HostHealthMonitor, .confirm(), .is_offline(), ._mark_offline(), .note_skipped(), .observe()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_dbg": "_dbg()" | kind=code-symbol | source=probe/agent/agent.py:L102 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), _run_ws_push_loop(), _wait_for_manager()]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L71 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…, Recognize only explicit single-host dev…, Recognize only explicit single-host dev…, Recognize only explicit single-host dev…]
- "agent_agent_manager_reachable": "_manager_reachable()" | kind=code-symbol | source=probe/agent/agent.py:L182 | neighbors=[agent.py, _classify_connection_error(), GET /health. Returns (ok, human-detail)…, _wait_for_manager(), GET /health. Returns (ok, human-detail)…, GET /health. Returns (ok, human-detail)…]
- "agent_agent_result_summary": "_result_summary()" | kind=code-symbol | source=probe/agent/agent.py:L121 | neighbors=[agent.py, main(), One-line, transparent summary of what a…, _ws_run_job(), One-line, transparent summary of what a…, One-line, transparent summary of what a…]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L497 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L105 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_doctor_check": "Check" | kind=code-symbol | source=probe/agent/doctor.py:L23 | neighbors=[doctor.py, check_clock(), check_disk(), check_privilege(), check_python(), classify_connectivity()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-038.json

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
