# Node Description Batch 35 of 336

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

- "tests_test_scope_targets": "test_scope_targets.py" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, test_property_every_accepted_target_is_…, TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected": "TestOutOfScopeIsRejected" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L44 | neighbors=[test_scope_targets.py, .test_blank_token_is_rejected(), .test_cidr_broader_than_scope(), .test_explicit_empty_list_is_rejected(), .test_hostname_is_not_routable(), .test_ip_outside_scope()]
- "tests_test_sla_policy": "test_sla_policy.py" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, _db(), _finding(), _operator(), _row(), TestPolicyAwareCompute]
- "tests_test_smb_ntlm_build_testparsechallenge": "TestParseChallenge" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L38 | neighbors=[test_smb_ntlm_build.py, .test_legacy_6_1_is_win7(), .test_no_version_field_yields_name_but_…, .test_non_challenge_returns_none(), .test_server_2022_build_20348(), .test_unknown_build_still_classified_wi…]
- "tests_test_syn_scanner_testbuildresultsenrichment": "TestBuildResultsEnrichment" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L349 | neighbors=[test_syn_scanner.py, ._scanner(), .test_closed_and_filtered_suppressed_by…, .test_open_result_carries_signals_and_o…, .test_open_without_signals_has_no_os_gu…, .test_os_guess_is_tagged_tcp_derived_no…]
- "tests_test_tier1_correlations": "test_tier1_correlations.py" | kind=code-symbol | source=probe/tests/test_tier1_correlations.py:L1 | neighbors=[6e2818f Add support for additional serv…, _run(), test_anon_data_exposure_cluster(), test_mgmt_plane_exposed_on_cipher_zero_…, test_mgmt_plane_needs_two_when_no_ciphe…, test_single_anon_finding_does_not_corre…]
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_legacy_versions_legacytlsserver": "_LegacyTLSServer" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L55 | neighbors=[test_tls_legacy_versions.py, .__enter__(), .__exit__(), .__init__(), ._serve(), A loopback server pinned to exactly one…]
- "tests_test_tls_port_coverage": "test_tls_port_coverage.py" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, service_enum.py, test_refused_handshake_is_an_error_not_…, TestDeliberateExclusions, TestSingleSourceOfTruth, TestWidenedCoverage]
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "tests_test_transport_testdeviceenrollment": "TestDeviceEnrollment" | kind=code-symbol | source=probe/tests/test_transport.py:L199 | neighbors=[test_transport.py, .test_activation_persists_recoverable_d…, .test_create_enrollment_request_409_rai…, .test_create_enrollment_request_409_wit…, .test_create_enrollment_request_forward…, .test_device_refresh_signs_unique_nonce…]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L207 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, Push a job to the first online agent in…, Push a job to the first online agent in…]
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L51 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()]
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L367 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…]
- "workflow_gates_gate_0_is_passive_profile": "gate_0_is_passive_profile()" | kind=code-symbol | source=probe/workflow/gates.py:L98 | neighbors=[gates.py, gate_2_host_discovery(), gate_3_port_scan(), gate_4b_os_fingerprint(), True means OT/ICS passive-only mode — a…, True means OT/ICS passive-only mode — a…]
- "workflow_host_health_hosthealthmonitor_state": "._state()" | kind=code-symbol | source=probe/workflow/host_health.py:L129 | neighbors=[HostHealthMonitor, .confirm(), .is_offline(), ._mark_offline(), .note_skipped(), .observe()]
- "workflow_workflow_engine_run_branch": "_run_branch()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L292 | neighbors=[workflow_engine.py, Run ONE deep-scan branch for one host: …, _record(), _record_reused(), _scan_one(), _split_cached()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_dbg": "_dbg()" | kind=code-symbol | source=probe/agent/agent.py:L98 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), _run_ws_push_loop(), _wait_for_manager()]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L497 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L105 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_engine_scan_method_for": "_scan_method_for()" | kind=code-symbol | source=probe/agent/engine.py:L177 | neighbors=[engine.py, _applied_tuning(), syn' for wide sweeps (deep intensity / …, run_scan(), syn' for wide sweeps (deep intensity / …, syn' for wide sweeps (deep intensity / …]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py]
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_local_run_main": "_main()" | kind=code-symbol | source=probe/agent/local_run.py:L158 | neighbors=[local_run.py, _parse_args(), _ports_from_env(), _scope_file(), summarize(), _usage_error()]
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…]
- "agent_transport_transport_heartbeat_ex": ".heartbeat_ex()" | kind=code-symbol | source=probe/agent/transport.py:L674 | neighbors=[Send a heartbeat and report WHY it fail…, Transport, .heartbeat(), .ensure_device_access(), Send a heartbeat and report WHY it fail…, Send a heartbeat and report WHY it fail…]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L286 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L245 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "campaign_progress_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/campaign-progress/route.ts:L1 | neighbors=[fail(), GET(), backend.ts, backend(), BackendError, bearerFrom()]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
