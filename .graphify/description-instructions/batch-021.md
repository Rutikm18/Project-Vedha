# Node Description Batch 22 of 186

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

- "tests_test_tls_posture_testgradetlsposture": "TestGradeTlsPosture" | kind=code-symbol | source=probe/tests/test_tls_posture.py:L72 | neighbors=[test_tls_posture.py, .test_empty_cipher_details_still_grades…, .test_grade_a_modern(), .test_grade_b_no_tls13(), .test_grade_c_no_forward_secrecy(), .test_grade_c_tls11()]
- "tools_issue_license": "issue_license.py" | kind=code-symbol | source=probe/tools/issue_license.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _b64(), issue(), keygen(), main()]
- "vuln_nuclei": "nuclei.py" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NucleiRunReport, NucleiScanError, NucleiScanner]
- "vuln_tasks": "tasks.py" | kind=code-symbol | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, database.py, _dedup_hash(), _fire_critical_webhook(), run_post_scan_enrichment()]
- "websocket_manager_graphwebsocketmanager_handle_client": ".handle_client()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L299 | neighbors=[GraphWebSocketManager, .connect(), .disconnect(), .send_personal(), ._handle_message(), Handle a new WebSocket client connectio…]
- "workers_outbox_run_worker": "run_worker()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L266 | neighbors=[outbox.py, Main loop: claim → process → repeat. Sl…, _claim_batch(), Event, _process(), _reclaim_stale()]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, DependencyMissingError, Base class for Active Directory assessm…, FindingSeverity]
- "ad_ldap_enum_ldapenumerator_get_users": ".get_users()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L213 | neighbors=[LDAPEnumerator, ADUser, _as_list(), ._attr(), ._search(), All user accounts (excludes computer ac…]
- "agent_agent_ws_take_confirmed_job": "_ws_take_confirmed_job()" | kind=code-symbol | source=probe/agent/agent.py:L573 | neighbors=[agent.py, Release a staged job only after the man…, _run_ws_push_loop(), say(), Release a staged job only after the man…, Release a staged job only after the man…]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L495 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_cli_managerclient": "ManagerClient" | kind=code-symbol | source=probe/agent/cli.py:L103 | neighbors=[cli.py, client_from_args(), cmd_auth_login(), cmd_doctor(), cmd_validate(), .__init__()]
- "agent_engine_clamp": "_clamp()" | kind=code-symbol | source=probe/agent/engine.py:L190 | neighbors=[engine.py, _job_runtime_seconds(), Coerce val to float and clamp to [lo, h…, _tuning_from_params(), Coerce val to float and clamp to [lo, h…, Coerce val to float and clamp to [lo, h…]
- "agent_engine_count_open_port_facts": "_count_open_port_facts()" | kind=code-symbol | source=probe/agent/engine.py:L276 | neighbors=[engine.py, _build_run_stats(), Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count unique open network endpoints, no…, Count concrete open services, not gener…]
- "agent_engine_tuning_from_params": "_tuning_from_params()" | kind=code-symbol | source=probe/agent/engine.py:L210 | neighbors=[engine.py, Translate operator-supplied job params …, run_scan(), _clamp(), Return the effective whole-job deadline…, Translate operator-supplied job params …]
- "agent_hw_bind": "hw_bind.py" | kind=code-symbol | source=probe/agent/hw_bind.py:L1 | neighbors=[check_hw_bind(), get_hw_id(), HWBindError, hw_bind.py — hardware fingerprinting fo…, 10dfc80 Add comprehensive probe testing…, test_hw_bind.py]
- "agent_license_check_license": "check_license()" | kind=code-symbol | source=probe/agent/license.py:L84 | neighbors=[license.py, LicenseError, short_id(), verify_license(), gauntlet(), The gate the agent calls at startup. Ho…]
- "agent_result_spool_resultspool_path": "._path()" | kind=code-symbol | source=probe/agent/result_spool.py:L50 | neighbors=[ResultSpool, .exists(), .flush_spool(), .load(), .quarantine(), .remove()]
- "agent_result_spool_resultspool_save": ".save()" | kind=code-symbol | source=probe/agent/result_spool.py:L68 | neighbors=[Atomically write a result payload to th…, ResultSpool, ._path(), ._sync_directory(), .submit_with_retry(), Atomically write a result payload to th…]
- "agent_result_spool_resultspool_submit_with_retry": ".submit_with_retry()" | kind=code-symbol | source=probe/agent/result_spool.py:L129 | neighbors=[Attempt to upload a result with retries…, ResultSpool, .quarantine(), .remove(), .save(), Attempt to upload a result with retries…]
- "agent_task_runner_taskrunner_run_job": ".run_job()" | kind=code-symbol | source=probe/agent/task_runner.py:L88 | neighbors=[Execute a complete scan job lifecycle. …, TaskRunner, JobResult, ._submit_or_spool(), Execute a complete scan job lifecycle. …, Execute a complete scan job lifecycle. …]
- "agent_task_runner_taskrunner_submit_or_spool": "._submit_or_spool()" | kind=code-symbol | source=probe/agent/task_runner.py:L442 | neighbors=[Submit the result, with spool-and-retry…, TaskRunner, .run_job(), Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…, Submit the result, with spool-and-retry…]
- "agent_transport_transport_connect_ws": ".connect_ws()" | kind=code-symbol | source=probe/agent/transport.py:L626 | neighbors=[Establish an authenticated WebSocket co…, Transport, .ensure_device_access(), TransportError, Establish an authenticated WebSocket co…, Establish an authenticated WebSocket co…]
- "agent_transport_transport_load_state": ".load_state()" | kind=code-symbol | source=probe/agent/transport.py:L170 | neighbors=[Transport, .activate_enrollment(), .ensure_device_access(), .__init__(), .refresh_device_access(), .refresh_registration()]
- "agent_transport_transport_poll_jobs": ".poll_jobs()" | kind=code-symbol | source=probe/agent/transport.py:L498 | neighbors=[Poll for pending jobs (HTTP fallback fo…, Transport, .ensure_device_access(), TransportError, Poll for pending jobs (HTTP fallback fo…, Poll for pending jobs (HTTP fallback fo…]
- "agent_transport_transport_refresh_registration": ".refresh_registration()" | kind=code-symbol | source=probe/agent/transport.py:L412 | neighbors=[Refresh routing metadata using the cach…, Transport, .load_state(), .update_state(), TransportError, Refresh routing metadata using the cach…]
- "agent_transport_transport_register": ".register()" | kind=code-symbol | source=probe/agent/transport.py:L214 | neighbors=[Register the probe with the manager.   …, Transport, .save_state(), TransportError, Register the probe with the manager.   …, Register the probe with the manager.   …]
- "agent_use_cases_resolve": "resolve()" | kind=code-symbol | source=probe/agent/use_cases.py:L234 | neighbors=[use_cases.py, Return (scan_type, profile, intensity) …, normalize_intensity(), use_case_for_code(), Return (scan_type, profile, intensity) …, Return (scan_type, profile) for a job. …]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L262 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "assets_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/assets/route.ts:L1 | neighbors=[GET(), backend(), BackendError, bearerFrom(), d1b4dd3 trim frontend to 7 core pages; …, backend.ts]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1754 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1963 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1697 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()]
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1622 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@045c9ae0769ca5697260d9485812cc159ef0734c": "045c9ae fix(posture): normalize run_at in _present_in_run; drop dead scores_pre…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, 9de087a feat(posture): add GET /analyti…, posture.py, test_posture.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@0f0097bd1d03cc4d36e8d8e0f8dbe4bf2d68ae0a": "0f0097b feat(posture): mirror posture scorecard into generated reports" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, fadb4f5 fix(posture): hoist report-sect…, ai_report.py, test_posture.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@0fbec7dfc54f7cd50921f99169270a9330d111d0": "0fbec7d feat(verification): add finding verification verdict columns + migration" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, caf1e5d feat(verification): determinist…, finding.py, test_finding_verification_schema.py, 0021_finding_verification.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@237a8319dd25a9eada7aec7f140dc7dba66b7dcd": "237a831 feat(posture): add run comparison, matrix, and response builder" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, 045c9ae fix(posture): normalize run_at …, posture.py, test_posture.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@2cddd526f80b7999775f6cfdc6726ad8e77325ac": "2cddd52 fix(posture): tenant-scope run helper; test null asset/score paths; tid…" | kind=Commit | source=git | neighbors=[feat/coverage-gated-auto-resolution, integration/all-branches, main, aa560a0 feat(posture): add dashboard Po…, analytics.py, test_posture.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
