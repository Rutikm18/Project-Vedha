# Node Description Batch 26 of 236

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L256 | neighbors=[port_scanner.py, BaseScanner, ._attempt(), ._build(), .__init__(), ._scan_port()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L836 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…, Run a scanner CLI's body with consisten…]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L365 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…, Simple async rate limiter: at most `rat…]
- "scanner_scanner_base_scanresult": "ScanResult" | kind=code-symbol | source=probe/scanner/scanner_base.py:L200 | neighbors=[scanner_base.py, ._guarded(), One observation about one target. Pure …, .__post_init__(), .to_json(), One observation about one target. Pure …]
- "scanner_snmp_scanner_snmpscanner_walk_subtree": "._walk_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L290 | neighbors=[GETNEXT walk of one OID subtree.  Retur…, SNMPScanner, _build_getnext(), _decode_value(), _encode_oid(), _oid_in_subtree()]
- "scanner_syn_scanner_synscanner_syn_scan_blocking": "._syn_scan_blocking()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L312 | neighbors=[SynScanner, build_syn_packet(), classify(), _local_source_ip(), parse_packet(), syn_cookie()]
- "scanner_tls_fingerprint_build_client_hello": "build_client_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L86 | neighbors=[tls_fingerprint.py, _ext(), _key_share_ext(), _sni_extension(), _supported_versions_ext(), _one_probe()]
- "scanner_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/scanner/windows_collector.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[job_result_service.py, Asset, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L28 | neighbors=[llm.py, ._default_runtime(), ._fallback_candidates(), ._runtime(), Settings, AiGenerateRequest]
- "services_notifications": "notifications.py" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, deliver(), enqueue_notification(), notify_tenant(), _send_email(), _send_jira()]
- "services_portal_metrics": "portal_metrics.py" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _is_closed(), MetricFinding, open_closed_counts(), _period(), severity_breakdown()]
- "states_datastate_datastate": "DataState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L108 | neighbors=[DashboardGrid.tsx, page.tsx, page.tsx, page.tsx, page.tsx, page.tsx]
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "tests_test_active_validation_escalation": "test_active_validation_escalation.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, _ev(), test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…]
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating]
- "tests_test_agent_auth_boundary": "test_agent_auth_boundary.py" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _boundary_test_client(), test_admin_enrollment_approval_is_not_p…, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…, test_legacy_agent_jwt_allows_only_workl…]
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L95 | neighbors=[test_agent_dispatch.py, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_online_heartbeat_clears_finished_…, .test_only_returns_online_agents_in_req…, ScanJobStatus]
- "tests_test_agent_read_tools_result": "_Result" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L19 | neighbors=[test_agent_read_tools.py, Mimics the subset of a SQLAlchemy Resul…, .all(), .__init__(), .scalars(), test_list_assets_batches_services_no_n_…]
- "tests_test_auth_login_make_tenant": "_make_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L61 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_not_expired_when_future(), .test_raises_expired_password(), .test_raises_password_mismatch()]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_customer_reveal": "test_customer_reveal.py" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, _db(), _operator(), test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
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
- "tests_test_remediation_generator_testparsejsonresponse": "TestParseJsonResponse" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L32 | neighbors=[test_remediation_generator.py, .test_empty_returns_empty(), .test_junk_returns_empty(), .test_non_object_json_returns_empty(), .test_plain_object(), .test_recovers_from_preamble()]
- "tests_test_remediation_routes_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L26 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404(), .test_cached_ai_on_hit()]
- "tests_test_result_spool": "test_result_spool.py" | kind=code-symbol | source=probe/tests/test_result_spool.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, result_spool.py, spool(), TestResultSpool]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-025.json

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
