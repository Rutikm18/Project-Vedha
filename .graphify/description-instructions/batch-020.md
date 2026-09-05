# Node Description Batch 21 of 336

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

- "tests_test_job_cancel_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L69 | neighbors=[test_job_cancel.py, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…, test_pending_job_is_cancelled_and_freed…]
- "tests_test_job_cancel_one": "_one()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L60 | neighbors=[test_job_cancel.py, A db.execute() result whose scalar_one_…, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…]
- "tests_test_job_cancel_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L29 | neighbors=[test_job_cancel.py, The REAL CurrentUser, not a SimpleNames…, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…]
- "tests_test_main_scripts_adaptive_timeout": "test_main_scripts_adaptive_timeout.py" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, adaptive_timeout.py, test_estimate_converges_on_stable_rtt(), test_fast_lan_gets_short_timeout_slow_w…, test_first_sample_sets_srtt_and_timeout…]
- "tests_test_main_scripts_completeness": "test_main_scripts_completeness.py" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, port_scanner.py, scanner_base.py, _metrics(), _rec(), test_duplicate_port_is_detected()]
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, ae08d19 feat(scanner): adaptive timeout…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner()]
- "tests_test_main_scripts_hardening": "test_main_scripts_hardening.py" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, make_smb2_error(), make_smb2_success(), _run()]
- "tests_test_new_scanners_testdeltaengine": "TestDeltaEngine" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L380 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner_fakeprocess": "FakeProcess" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L30 | neighbors=[test_nuclei_scanner.py, .__init__(), .kill(), .terminate(), .wait(), test_nonzero_exit_retains_and_marks_par…]
- "tests_test_pipeline_concurrency": "test_pipeline_concurrency.py" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _db_with(), _event(), test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_posture_trace_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L24 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…, ._mixed()]
- "tests_test_posture_trace_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L17 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…, ._mixed()]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_tier1_wiring_gate": "test_tier1_wiring_gate.py" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L1 | neighbors=[64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, scan_funnel.py, scanner_base.py, _funnel(), test_every_it_branch_has_port_table_ent…]
- "tests_test_validation_ingest": "test_validation_ingest.py" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _finding(), test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string(), .test_malformed_xml_returns_empty()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]
- "websocket_manager": "manager.py" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 8f6bf49 Refactor code structure and rem…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, f3bb8db feat(manager): cross-worker WS …]
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L355 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()]
- "ad_ldap_enum": "ldap_enum.py" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L1 | neighbors=[ACE, ADComputer, ADGroup, ADUser, _as_list(), _domain_to_base_dn()]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L887 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …, Acknowledge an offer without executing …, Acknowledge an offer without executing …]
- "agent_cli_client_from_args": "client_from_args()" | kind=code-symbol | source=probe/agent/cli.py:L228 | neighbors=[cli.py, ManagerClient, resolve_profile(), cmd_agents_list(), cmd_auth_status(), cmd_engagements_create()]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L31 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), cmd_validate(), .load()]
- "agent_engine_build_run_stats": "_build_run_stats()" | kind=code-symbol | source=probe/agent/engine.py:L413 | neighbors=[engine.py, _applied_tuning(), _count_open_port_facts(), _hosts_from_facts(), Build one consistent result summary for…, run_scan()]
- "agent_scope_validator": "scope_validator.py" | kind=code-symbol | source=probe/agent/scope_validator.py:L1 | neighbors=[fetch_engagement_scope(), merge_exclusions(), _networks_for_target(), targets_in_excludes(), validate_targets_in_scope(), scope_validator.py — defense-in-depth s…]
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L770 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L854 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L912 | neighbors=[True if the WebSocket connection is act…, Transport, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…]
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L870 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L77 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, Extracts JWT from Authorization header …]
- "commands_interactive_divider": "divider()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L112 | neighbors=[interactive.ts, ln(), mainMenu(), wizardAdmin(), wizardAsk(), wizardEngagement()]
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[apiFetch(), requireAuth(), AiReport, buildReportCommand(), Engagement, errExit()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2de251b6a34cad99831e042cf014ca1bcfa6aed2": "2de251b feat(scanner): ICMP timestamp fallback — echo-filter bypass + clock har…" | kind=Commit | source=git | neighbors=[addcapabilities-fable, feat/complete-pending-work, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, main, ui-ux-backend-updates0109]
- "commit:repo:github.com/Rutikm18/Project-Vedha@daf3de2734a3efdd04df485c8544d56209bd5554": "daf3de2 feat(scanner): add service enumeration and enrichment layer" | kind=Commit | source=git | neighbors=[6be8259 feat(integrations): outbox deli…, addcapabilities-fable, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409]
- "components_engagementstatuscontrol": "EngagementStatusControl.tsx" | kind=code-symbol | source=manager/frontend/components/EngagementStatusControl.tsx:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, ENGAGEMENT_STATES, EngagementStatusControl(), EngagementStatusControlProps, STATUS_COLOR]
- "detection_edr_crowdstrikefalcon": "CrowdStrikeFalcon" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L91 | neighbors=[edr.py, .parse_response(), .query_detections(), EDRQueryEngine, Falcon: query detection IDs then fetch …, Unit tests for the detection validation…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-020.json

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
