# Node Description Batch 27 of 236

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

- "tests_test_scan_health": "test_scan_health.py" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _summary(), test_aggregates_across_hosts(), test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scope_targets": "test_scope_targets.py" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, test_property_every_accepted_target_is_…, TestExclusions, TestIpVersionSafety, TestNoScopeAuthorizesNothing, TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected": "TestOutOfScopeIsRejected" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L44 | neighbors=[test_scope_targets.py, .test_blank_token_is_rejected(), .test_cidr_broader_than_scope(), .test_explicit_empty_list_is_rejected(), .test_hostname_is_not_routable(), .test_ip_outside_scope()]
- "tests_test_sla_policy": "test_sla_policy.py" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, _db(), _finding(), _operator(), _row(), TestPolicyAwareCompute]
- "tests_test_tls_integration": "test_tls_integration.py" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, tls_scanner.py, _self_signed(), test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade()]
- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_agentconnectionmanager_push_job": ".push_job()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L177 | neighbors=[AgentConnectionManager, .deliver_job(), .unregister(), .push_job_to_first_online(), .run_backplane(), Push a job to a specific agent over Web…]
- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L380 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages., Handle incoming WebSocket messages.]
- "workers_outbox_claim_batch": "_claim_batch()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L157 | neighbors=[outbox.py, Event, Atomically claim up to `batch_size` due…, run_worker(), Atomically claim up to `batch_size` due…, Atomically claim up to `batch_size` due…]
- "workflow_router_route_branches": "route_branches()" | kind=code-symbol | source=probe/workflow/router.py:L83 | neighbors=[router.py, For every open port with a banner fact,…, looks_like_db(), looks_like_http(), looks_like_ssh(), looks_like_tls()]
- "workflow_workflow_engine_gather_per_host": "_gather_per_host()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L84 | neighbors=[workflow_engine.py, _scan_one(), Run per-host probes with bounded fan-ou…, run_engagement(), Run per-host probes with bounded fan-ou…, Run per-host probes with bounded fan-ou…]
- "workflow_workflow_engine_port_candidates": "_port_candidates()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L122 | neighbors=[workflow_engine.py, Return TCP ports worth scanning for thi…, run_engagement(), Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…, Return TCP ports worth scanning for thi…]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_ws_stage_job_offer": "_ws_stage_job_offer()" | kind=code-symbol | source=probe/agent/agent.py:L691 | neighbors=[agent.py, Acknowledge an offer without executing …, _run_ws_push_loop(), Acknowledge an offer without executing …, Persistent WebSocket push loop.      Re…, Acknowledge an offer without executing …]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L495 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L103 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L351 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…, Serialize effective limits without ever…]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L206 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Return the effective whole-job deadline…, Coerce val to float and clamp to [lo, h…]
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=probe/agent/engine.py:L514 | neighbors=[engine.py, RuntimeError, Raised when Manager fencing revokes the…, _run_with_cancellation(), Raised when Manager fencing revokes the…, Raised when Manager fencing revokes the…]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py]
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_local_run_main": "_main()" | kind=code-symbol | source=probe/agent/local_run.py:L158 | neighbors=[local_run.py, _parse_args(), _ports_from_env(), _scope_file(), summarize(), _usage_error()]
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…]
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L88 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool(), Execute a complete scan job lifecycle. …, Execute a complete scan job lifecycle. …]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L442 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_transport_fetch_scope": ".fetch_scope()" | kind=code-symbol | source=probe/agent/transport.py:L562 | neighbors=[Fetch the engagement's authoritative sc…, Transport, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…, Fetch the engagement's authoritative sc…]
- "agent_transport_transport_http_get": ".http_get()" | kind=code-symbol | source=probe/agent/transport.py:L646 | neighbors=[Generic authenticated GET, returns pars…, Transport, Generic authenticated GET, returns pars…, Generic authenticated GET, returns pars…, Refresh a device token before expiry; l…, Generic authenticated GET, returns pars…]
- "agent_transport_transport_is_authenticated": ".is_authenticated()" | kind=code-symbol | source=probe/agent/transport.py:L202 | neighbors=[True if we have both an agent_id and a …, Transport, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …, True if we have both an agent_id and a …]
- "agent_transport_transport_is_ws_connected": ".is_ws_connected()" | kind=code-symbol | source=probe/agent/transport.py:L704 | neighbors=[True if the WebSocket connection is act…, Transport, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…, True if the WebSocket connection is act…]
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L208 | neighbors=[Transport, .activate_enrollment(), .ensure_device_access(), .__init__(), .refresh_device_access(), .refresh_registration()]
- "agent_transport_transport_ws_url": ".ws_url()" | kind=code-symbol | source=probe/agent/transport.py:L662 | neighbors=[Return the WebSocket endpoint without e…, Transport, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…, Return the WebSocket endpoint without e…]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L286 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L245 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-026.json

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
