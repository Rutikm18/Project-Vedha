# Node Description Batch 29 of 209

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

- "vuln_tasks_rationale_171": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L171 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService]
- "vuln_tasks_rationale_35": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L35 | neighbors=[run_post_scan_enrichment(), Asset, Engagement, FindingSeverity, FindingStatus, Finding]
- "vuln_tasks_rationale_38": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L38 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService]
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L205 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, Push a job to the first online agent in…, .unregister()]
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L49 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()]
- "websocket_manager_graphwebsocketmanager_handle_message": "._handle_message()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L319 | neighbors=[GraphWebSocketManager, .handle_client(), .broadcast(), .send_personal(), Handle incoming WebSocket messages., Handle incoming WebSocket messages.]
- "workers_outbox_reclaim_stale": "_reclaim_stale()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L203 | neighbors=[outbox.py, Requeue events a dead worker left in PR…, _dead_letter_stale_stmt(), _requeue_stale_stmt(), _stale_cutoff(), run_worker()]
- "workflow_intensity": "intensity.py" | kind=code-symbol | source=probe/workflow/intensity.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, test_probe_next_features.py, port_scanner.py, intensity_port_override(), resolve_intensity()]
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L310 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…, Parse the nTSecurityDescriptor of an ob…]
- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=probe/agent/agent.py:L130 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…]
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L64 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…]
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L171 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()]
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…]
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L311 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()]
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L444 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()]
- "agent_engine_applied_tuning": "_applied_tuning()" | kind=code-symbol | source=probe/agent/engine.py:L345 | neighbors=[engine.py, _scan_method_for(), _build_run_stats(), Serialize effective limits without ever…, Serialize effective limits without ever…, Serialize effective limits without ever…]
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L72 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…, Single factory for error result dicts —…]
- "agent_engine_job_runtime_seconds": "_job_runtime_seconds()" | kind=code-symbol | source=probe/agent/engine.py:L200 | neighbors=[engine.py, _clamp(), Return the effective whole-job deadline…, run_scan(), Coerce val to float and clamp to [lo, h…, Return the effective whole-job deadline…]
- "agent_engine_leaselosterror": "LeaseLostError" | kind=code-symbol | source=probe/agent/engine.py:L485 | neighbors=[engine.py, RuntimeError, Raised when Manager fencing revokes the…, _run_with_cancellation(), Raised when Manager fencing revokes the…, Raised when Manager fencing revokes the…]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…, Load a previously spooled result, retur…]
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=probe/agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=probe/agent/task_runner.py:L39 | neighbors=[task_runner.py, Orchestrates one scan job's lifecycle. …, .__init__(), .run_job(), ._submit_or_spool(), Orchestrates one scan job's lifecycle. …]
- "agent_transport_atomic_write_private_state": "_atomic_write_private_state()" | kind=code-symbol | source=probe/agent/transport.py:L45 | neighbors=[transport.py, _sync_directory(), Durably replace one private JSON state …, .update_state(), Durably replace one private JSON state …, Durably replace one private JSON state …]
- "agent_transport_transport_heartbeat": ".heartbeat()" | kind=code-symbol | source=probe/agent/transport.py:L463 | neighbors=[Send a heartbeat to the manager.       …, Transport, .ensure_device_access(), Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …, Send a heartbeat to the manager.       …]
- "agent_transport_transport_submit_result": ".submit_result()" | kind=code-symbol | source=probe/agent/transport.py:L537 | neighbors=[Submit a scan result to the manager.   …, Transport, .ensure_device_access(), Submit a scan result to the manager.   …, Submit a scan result to the manager.   …, Submit a scan result to the manager.   …]
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()]
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()]
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_llm_report_llmreportgenerator_generate_remediation_plan": ".generate_remediation_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L244 | neighbors=[LLMReportGenerator, ._complete(), _normalize_ai_plan(), _parse_json_response(), _remediation_plan_prompt(), Generate a STRUCTURED, OS-specific reme…]
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()]
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_portal_scope_assert_client": "assert_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L31 | neighbors=[portal_scope.py, client_scoped(), Return the client's bound engagement id…, require_client(), resolve_scope(), Return the client's bound engagement id…]
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts]
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()]
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()]
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@1d5ae943f799b5d9bba43f41c366d70ed4c00b1a": "1d5ae94 feat(fleet): live \"Connected probes\" status section" | kind=Commit | source=git | neighbors=[feat/syn-scanner-osfp-adaptive, main, 88c9278 feat(ai): pin manager LLM pipel…, page.tsx, c4386e4 feat(customers): operator Custo…, feat/user-portal-reskin-scan-request]
- "commit:repo:github.com/Rutikm18/Project-Vedha@65e568441bfb43e313c743db52bd2f65fb7e86fe": "65e5684 feat(probe): transparent job logging (real use-case + result summary)" | kind=Commit | source=git | neighbors=[1af3404 feat(deploy): probe-free manage…, agent.py, feat/syn-scanner-osfp-adaptive, main, ae08d19 feat(scanner): adaptive timeout…, feat/user-portal-reskin-scan-request]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
