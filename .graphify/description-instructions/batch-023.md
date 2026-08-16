# Node Description Batch 24 of 209

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

- "services_portal_metrics": "portal_metrics.py" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _is_closed(), MetricFinding, open_closed_counts(), _period(), severity_breakdown()]
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, config.py, compute(), SlaResult, summarize(), _windows()]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L108 | neighbors=[DashboardGrid.tsx, page.tsx, page.tsx, page.tsx, page.tsx, page.tsx]
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "tests_test_active_validation_escalation": "test_active_validation_escalation.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, _ev(), test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…]
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating]
- "tests_test_agent_auth_boundary": "test_agent_auth_boundary.py" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _boundary_test_client(), test_admin_enrollment_approval_is_not_p…, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…, test_legacy_agent_jwt_allows_only_workl…]
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L95 | neighbors=[test_agent_dispatch.py, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_online_heartbeat_clears_finished_…, .test_only_returns_online_agents_in_req…, ScanJobStatus]
- "tests_test_auth_login_make_tenant": "_make_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L61 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_not_expired_when_future(), .test_raises_expired_password(), .test_raises_password_mismatch()]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_detection_core_mock_kev_db": "_mock_kev_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L86 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_device_profile": "test_device_profile.py" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_ambiguous_keeps_asset_type_none_bu…, test_device_profiles_extracts_role_deta…, test_every_device_type_maps_to_the_righ…, test_malformed_entries_are_skipped(), test_non_device_inventory_result_yields…]
- "tests_test_exploit_engine_testexploitorchestrator_make_orchestrator": "._make_orchestrator()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L246 | neighbors=[TestExploitOrchestrator, .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_installer_contract": "test_installer_contract.py" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, _dry_run(), test_installer_accepts_enroll_token_and…, test_installer_rejects_missing_or_unkno…, test_installer_requires_only_manager_en…]
- "tests_test_main_scripts_vantage_r": "_r()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L12 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_main_scripts_vantage_testreconcilevantages": "TestReconcileVantages" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L16 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_manager_ai_cloud": "_cloud()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L232 | neighbors=[test_manager_ai.py, Settings with provider unset and all cl…, test_default_auto_detect_prefers_openai…, test_default_auto_detects_the_configure…, test_default_runtime_fails_closed_witho…, test_fallback_never_includes_local_olla…]
- "tests_test_nuclei_background_sessionfactory": "_SessionFactory" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L59 | neighbors=[test_nuclei_background.py, .__call__(), .__init__(), test_fatal_nuclei_error_marks_backgroun…, test_partial_nuclei_run_preserves_findi…, ScanJobStatus]
- "tests_test_portal_read_db_for_create": "_db_for_create()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L216 | neighbors=[test_portal_read.py, Mock the create_scan_request db flow: e…, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()]
- "tests_test_portal_scope": "test_portal_scope.py" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _client(), _operator(), TestAssertClient, TestClientScoped, TestPortalTokenClaims]
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=probe/tests/test_probe_core.py:L861 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, result_spool.py, spool(), TestResultSpool]
- "tests_test_scan_health": "test_scan_health.py" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _summary(), test_aggregates_across_hosts(), test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scope_targets": "test_scope_targets.py" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, test_property_every_accepted_target_is_…, TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected": "TestOutOfScopeIsRejected" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L44 | neighbors=[test_scope_targets.py, .test_blank_token_is_rejected(), .test_cidr_broader_than_scope(), .test_explicit_empty_list_is_rejected(), .test_hostname_is_not_routable(), .test_ip_outside_scope()]
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L299 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L266 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reclaim_stale()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L691 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …, Persistent WebSocket push loop.      Re…, Acknowledge an offer without executing …]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L495 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L103 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L190 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…, Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L276 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count concrete open services, not gener…]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L210 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-023.json

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
