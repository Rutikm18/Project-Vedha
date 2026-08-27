# Node Description Batch 32 of 236

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "vuln_nessus": "nessus.py" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NessusScanner, NessusScanner — wraps the Tenable Nessu…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_nessus_nessusscanner_get_client": "._get_client()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L49 | neighbors=[NessusScanner, .create_scan(), .export_nessus_file(), ._auth_headers(), .get_results(), .launch_scan()] | lang=en
- "vuln_tasks_rationale_1": "Background tasks triggered after a vuln scan completes.  Pipeline:   1. Load all" | kind=entity | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[tasks.py, Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=pt
- "vuln_tasks_rationale_168": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L168 | neighbors=[_dedup_hash(), Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=en
- "vuln_tasks_rationale_171": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L171 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "vuln_tasks_rationale_35": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L35 | neighbors=[run_post_scan_enrichment(), Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=en
- "vuln_tasks_rationale_38": "Triggered by the vuln scan API after a scan completes.     Safe to run as a Fast" | kind=entity | source=manager/backend/app/vuln/tasks.py:L38 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, Finding, VulnEnrichmentService] | lang=en
- "websocket_manager_agentconnectionmanager_push_job_to_first_online": ".push_job_to_first_online()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L205 | neighbors=[AgentConnectionManager, .online_agents_for_tenant(), .push_job(), Push a job to the first online agent in…, Push a job to the first online agent in…, .unregister()] | lang=en
- "websocket_manager_connectionmanager_broadcast": ".broadcast()" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L49 | neighbors=[ConnectionManager, .disconnect(), .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), ._handle_message()] | lang=en
- "workers_outbox_mark_retry_or_dead": "_mark_retry_or_dead()" | kind=code-symbol | source=manager/backend/app/workers/outbox.py:L259 | neighbors=[outbox.py, _process(), Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…, Reschedule with exponential backoff, or…] | lang=en
- "workflow_intensity": "intensity.py" | kind=code-symbol | source=probe/workflow/intensity.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, test_probe_next_features.py, port_scanner.py, intensity_port_override(), resolve_intensity()] | lang=en
- "workflow_workflow_engine_scan_one": "_scan_one()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L71 | neighbors=[workflow_engine.py, _gather_per_host(), Run one component without allowing a ta…, run_engagement(), Run one component without allowing a ta…, Run one component without allowing a ta…] | lang=en
- "workflow_workflow_engine_split_cached": "_split_cached()" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L104 | neighbors=[workflow_engine.py, Splits candidate_ports into (ports that…, run_engagement(), Splits candidate_ports into (ports that…, Splits candidate_ports into (ports that…, Splits candidate_ports into (ports that…] | lang=en
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L310 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…, Parse the nTSecurityDescriptor of an ob…] | lang=en
- "agent_agent_classify_connection_error": "_classify_connection_error()" | kind=code-symbol | source=probe/agent/agent.py:L130 | neighbors=[agent.py, _enroll_device(), main(), _manager_reachable(), _obtain_identity(), Map a low-level connection exception to…] | lang=en
- "agent_agent_dbg": "_dbg()" | kind=code-symbol | source=probe/agent/agent.py:L87 | neighbors=[agent.py, _enroll_device(), main(), _obtain_identity(), _wait_for_manager(), _ws_run_job()] | lang=en
- "agent_agent_load_env": "_load_env()" | kind=code-symbol | source=probe/agent/agent.py:L64 | neighbors=[agent.py, main(), Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…, Load key=value lines from probe.env for…] | lang=en
- "agent_agent_load_or_create_signing_identity": "_load_or_create_signing_identity()" | kind=code-symbol | source=probe/agent/agent.py:L1024 | neighbors=[agent.py, _obtain_identity(), Load or atomically create the probe's E…, Load or atomically create the probe's E…, Load or atomically create the probe's E…, Run all startup security checks before …] | lang=en
- "agent_agent_wait_for_manager": "_wait_for_manager()" | kind=code-symbol | source=probe/agent/agent.py:L171 | neighbors=[agent.py, main(), Bounded reachability preflight. Proceed…, _dbg(), _manager_reachable(), say()] | lang=en
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…] | lang=en
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L311 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()] | lang=en
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L444 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()] | lang=en
- "agent_engine_error_result": "_error_result()" | kind=code-symbol | source=probe/agent/engine.py:L72 | neighbors=[engine.py, _runtime_manifest(), Single factory for error result dicts —…, run_scan(), Single factory for error result dicts —…, Single factory for error result dicts —…] | lang=en
- "agent_engine_hosts_from_facts": "_hosts_from_facts()" | kind=code-symbol | source=probe/agent/engine.py:L303 | neighbors=[engine.py, _build_run_stats(), Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…, Build promotion-ready hosts without dup…] | lang=en
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…, Load a previously spooled result, retur…] | lang=en
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=probe/agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()] | lang=en
- "agent_task_runner_taskrunner": "TaskRunner" | kind=code-symbol | source=probe/agent/task_runner.py:L39 | neighbors=[task_runner.py, Orchestrates one scan job's lifecycle. …, .__init__(), .run_job(), ._submit_or_spool(), Orchestrates one scan job's lifecycle. …] | lang=en
- "agent_transport_transport_bootstrap": ".bootstrap()" | kind=code-symbol | source=probe/agent/transport.py:L307 | neighbors=[Register using a manager-side shared bo…, Transport, .save_state(), TransportError, Register using a manager-side shared bo…, Register using a manager-side shared bo…] | lang=en
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L254 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code(), Coerce an int-or-numeric-string to int,…, Coerce an int-or-numeric-string to int,…] | lang=en
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L276 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…] | lang=en
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L265 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int(), Map a numeric use-case code → use_case_…, Map a numeric use-case code → use_case_…] | lang=en
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()] | lang=en
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()] | lang=en
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service] | lang=en
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service] | lang=en
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()] | lang=en
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "auth_portal_scope_assert_client": "assert_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L31 | neighbors=[portal_scope.py, client_scoped(), Return the client's bound engagement id…, require_client(), resolve_scope(), Return the client's bound engagement id…] | lang=en
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
