# Node Description Batch 48 of 380

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
- "websocket_manager_agentconnectionmanager_is_connected": ".is_connected()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L293 | neighbors=[AgentConnectionManager, .run_backplane(), Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected., Check if a specific agent is connected.]
- "websocket_manager_graphwebsocketmanager_broadcast_graph_update": ".broadcast_graph_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L405 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…, Broadcast graph data update to all subs…]
- "websocket_manager_graphwebsocketmanager_broadcast_layout_update": ".broadcast_layout_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L424 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…, Broadcast layout change to all subscrib…]
- "websocket_manager_graphwebsocketmanager_broadcast_node_update": ".broadcast_node_update()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L414 | neighbors=[GraphWebSocketManager, .broadcast(), Broadcast a single node update., Broadcast a single node update., Broadcast a single node update., Broadcast a single node update.]
- "workflow_asset_asset_needs_recheck_live": ".needs_recheck_live()" | kind=code-symbol | source=probe/workflow/asset.py:L89 | neighbors=[Asset, _utcnow(), Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…, Is liveness unknown, or stale past `thr…]
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L310 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…, Parse the nTSecurityDescriptor of an ob…]
- "agent_agent_configure_logging": "configure_logging()" | kind=code-symbol | source=probe/agent/agent.py:L281 | neighbors=[agent.py, main(), Install a root log handler for the daem…, Install a root log handler for the daem…, Install a root log handler for the daem…, Install a root log handler for the daem…]
- "agent_agent_job_intent": "_job_intent()" | kind=code-symbol | source=probe/agent/agent.py:L107 | neighbors=[agent.py, Human label for what a job will actuall…, _ws_run_job(), Human label for what a job will actuall…, Human label for what a job will actuall…, Human label for what a job will actuall…]
- "agent_agent_preflight_scope_check": "_preflight_scope_check()" | kind=code-symbol | source=probe/agent/agent.py:L213 | neighbors=[agent.py, main(), _detect_primary_ipv4(), say(), Auto-troubleshoot the single silent kil…, Auto-troubleshoot the single silent kil…]
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…]
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L313 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()]
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L446 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()]
- "agent_config_model": "config_model.py" | kind=code-symbol | source=probe/agent/config_model.py:L1 | neighbors=[parse_env_file(), render_effective(), resolve(), _to_bool(), config_model.py — single config precede…, 08d8fe1 Phase 2: config precedence load…]
- "agent_engine_env_number": "_env_number()" | kind=code-symbol | source=probe/agent/engine.py:L53 | neighbors=[engine.py, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…, Read a bounded numeric safety setting w…]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_job_admission": "job_admission.py" | kind=code-symbol | source=probe/agent/job_admission.py:L1 | neighbors=[drop_denied(), manager_ip_from_env(), verify_signed_job(), job_admission.py — the agent's independ…, 5bf1aab Wire independent admission gate…, 79ea84a Finish pending gaps: real clock…]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…, Load a previously spooled result, retur…]
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=probe/agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_setup_resolved": "_resolved()" | kind=code-symbol | source=probe/agent/setup.py:L55 | neighbors=[setup.py, cmd_collect_diagnostics(), cmd_config(), cmd_connect(), cmd_doctor(), _probe_env()]
- "agent_setup_state_dir": "_state_dir()" | kind=code-symbol | source=probe/agent/setup.py:L39 | neighbors=[setup.py, cmd_collect_diagnostics(), cmd_connect(), cmd_doctor(), cmd_self_scan(), cmd_uninstall()]
- "agent_task_runner_jobresult": "JobResult" | kind=code-symbol | source=probe/agent/task_runner.py:L94 | neighbors=[task_runner.py, Structured result from running one scan…, .run_job(), Structured result from running one scan…, Structured result from running one scan…, Structured result from running one scan…]
- "agent_task_runner_taskrunner_archive_result": "._archive_result()" | kind=code-symbol | source=probe/agent/task_runner.py:L593 | neighbors=[Write the outbound payload to the local…, TaskRunner, _result_dir(), ._submit_or_spool(), Write the outbound payload to the local…, Write the outbound payload to the local…]
- "agent_task_runner_taskrunner_init": ".__init__()" | kind=code-symbol | source=probe/agent/task_runner.py:L113 | neighbors=[Args:             http_get:       Callb…, TaskRunner, Args:             http_get:       Callb…, Args:             http_get:       Callb…, Create the result archive directory at …, Create the result archive directory at …]
- "agent_transport_enrollment_conflict_detail": "_enrollment_conflict_detail()" | kind=code-symbol | source=probe/agent/transport.py:L122 | neighbors=[transport.py, Best-effort extraction of the manager's…, .create_enrollment_request(), Best-effort extraction of the manager's…, A poll/activate targeted an enrollment …, Best-effort extraction of the manager's…]
- "agent_transport_manager_fingerprint": "manager_fingerprint()" | kind=code-symbol | source=probe/agent/transport.py:L104 | neighbors=[transport.py, Stable identity for the manager a crede…, .activate_enrollment(), .refresh_device_access_ex(), .save_state(), Stable identity for the manager a crede…]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L305 | neighbors=[Persist the agent identity AND the mana…, Transport, .bootstrap(), .register(), manager_fingerprint(), .update_state()]
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L254 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code(), Coerce an int-or-numeric-string to int,…, Coerce an int-or-numeric-string to int,…]
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L276 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…]
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L265 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int(), Map a numeric use-case code → use_case_…, Map a numeric use-case code → use_case_…]
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L254 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()]
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L184 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()]
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_llm_report_normalize_ai_plan": "_normalize_ai_plan()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L430 | neighbors=[llm_report.py, .generate_remediation_plan(), _safe_commands(), Coerce a parsed AI response into the sa…, Coerce a parsed AI response into the sa…, Coerce a parsed AI response into the sa…]
- "ai_llm_report_remediation_plan_prompt": "_remediation_plan_prompt()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L360 | neighbors=[llm_report.py, .generate_remediation_plan(), Build the structured-remediation prompt…, _enum(), Build the structured-remediation prompt…, Build the structured-remediation prompt…]
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()]
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
