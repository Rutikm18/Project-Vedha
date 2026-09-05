# Node Description Batch 43 of 336

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

- "workflow_intensity": "intensity.py" | kind=code-symbol | source=probe/workflow/intensity.py:L1 | neighbors=[engine.py, 22701ea Add tests for scanner parity an…, test_probe_next_features.py, port_scanner.py, intensity_port_override(), resolve_intensity()]
- "ad_ldap_enum_ldapenumerator_get_aces": ".get_aces()" | kind=code-symbol | source=manager/backend/app/ad/ldap_enum.py:L310 | neighbors=[LDAPEnumerator, ._attr(), ._parse_security_descriptor(), ._require_conn(), Parse the nTSecurityDescriptor of an ob…, Parse the nTSecurityDescriptor of an ob…]
- "agent_agent_is_local_manager_url": "_is_local_manager_url()" | kind=code-symbol | source=probe/agent/agent.py:L67 | neighbors=[agent.py, main(), Recognize only explicit single-host dev…, Recognize only explicit single-host dev…, Recognize only explicit single-host dev…, Recognize only explicit single-host dev…]
- "agent_agent_manager_reachable": "_manager_reachable()" | kind=code-symbol | source=probe/agent/agent.py:L178 | neighbors=[agent.py, _classify_connection_error(), GET /health. Returns (ok, human-detail)…, _wait_for_manager(), GET /health. Returns (ok, human-detail)…, GET /health. Returns (ok, human-detail)…]
- "agent_agent_result_summary": "_result_summary()" | kind=code-symbol | source=probe/agent/agent.py:L117 | neighbors=[agent.py, main(), One-line, transparent summary of what a…, _ws_run_job(), One-line, transparent summary of what a…, One-line, transparent summary of what a…]
- "agent_agent_ws_flush_spool": "_ws_flush_spool()" | kind=code-symbol | source=probe/agent/agent.py:L489 | neighbors=[agent.py, Re-submit previously spooled results ov…, _run_ws_push_loop(), say(), _ws_http_poll_fallback(), Re-submit previously spooled results ov…]
- "agent_cli_cmd_doctor": "cmd_doctor()" | kind=code-symbol | source=probe/agent/cli.py:L313 | neighbors=[cli.py, _doctor_check(), ManagerClient, .request(), output(), resolve_profile()]
- "agent_cli_cmd_engagements_create": "cmd_engagements_create()" | kind=code-symbol | source=probe/agent/cli.py:L446 | neighbors=[cli.py, client_from_args(), CliError, .request(), output(), split_values()]
- "agent_engine_derive_devices": "_derive_devices()" | kind=code-symbol | source=probe/agent/engine.py:L505 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Classify each target's device role from…, Classify each target's device role from…, Classify each target's device role from…]
- "agent_engine_derive_exposure": "_derive_exposure()" | kind=code-symbol | source=probe/agent/engine.py:L525 | neighbors=[engine.py, _results_by_target(), _derive_post_stage(), Reconcile each target's per-vantage rea…, Reconcile each target's per-vantage rea…, Reconcile each target's per-vantage rea…]
- "agent_init": "__init__.py" | kind=code-symbol | source=probe/agent/__init__.py:L1 | neighbors=[agent — the probe transport layer (seal…, 10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "agent_result_spool_resultspool_load": ".load()" | kind=code-symbol | source=probe/agent/result_spool.py:L99 | neighbors=[Load a previously spooled result, retur…, ResultSpool, .exists(), ._path(), Load a previously spooled result, retur…, Load a previously spooled result, retur…]
- "agent_result_spool_resultspool_quarantine": ".quarantine()" | kind=code-symbol | source=probe/agent/result_spool.py:L115 | neighbors=[Move a terminally rejected result out o…, ResultSpool, .flush_spool(), ._path(), ._sync_directory(), .submit_with_retry()]
- "agent_transport_enrollment_conflict_detail": "_enrollment_conflict_detail()" | kind=code-symbol | source=probe/agent/transport.py:L122 | neighbors=[transport.py, Best-effort extraction of the manager's…, .create_enrollment_request(), Best-effort extraction of the manager's…, A poll/activate targeted an enrollment …, Best-effort extraction of the manager's…]
- "agent_transport_manager_fingerprint": "manager_fingerprint()" | kind=code-symbol | source=probe/agent/transport.py:L104 | neighbors=[transport.py, Stable identity for the manager a crede…, .activate_enrollment(), .refresh_device_access_ex(), .save_state(), Stable identity for the manager a crede…]
- "agent_transport_transport_save_state": ".save_state()" | kind=code-symbol | source=probe/agent/transport.py:L305 | neighbors=[Persist the agent identity AND the mana…, Transport, .bootstrap(), .register(), manager_fingerprint(), .update_state()]
- "agent_use_cases_as_int": "_as_int()" | kind=code-symbol | source=probe/agent/use_cases.py:L254 | neighbors=[use_cases.py, normalize_intensity(), Coerce an int-or-numeric-string to int,…, use_case_for_code(), Coerce an int-or-numeric-string to int,…, Coerce an int-or-numeric-string to int,…]
- "agent_use_cases_normalize_intensity": "normalize_intensity()" | kind=code-symbol | source=probe/agent/use_cases.py:L276 | neighbors=[use_cases.py, _as_int(), Accept an intensity as a number (1/2/3)…, resolve(), Accept an intensity as a number (1/2/3)…, Accept an intensity as a number (1/2/3)…]
- "agent_use_cases_use_case_for_code": "use_case_for_code()" | kind=code-symbol | source=probe/agent/use_cases.py:L265 | neighbors=[use_cases.py, Map a numeric use-case code → use_case_…, resolve(), _as_int(), Map a numeric use-case code → use_case_…, Map a numeric use-case code → use_case_…]
- "ai_agent_agentdecisionengine_exec_read_tool": "._exec_read_tool()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L249 | neighbors=[AgentDecisionEngine, ._list_assets(), ._list_attack_paths(), ._list_findings(), ._overview(), .run()]
- "ai_agent_agentdecisionengine_run": ".run()" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L183 | neighbors=[AgentDecisionEngine, ._create(), ._exec_read_tool(), ._persist(), AgentUnavailableError, _tool_result()]
- "ai_agent_rationale_1": "agent.py — AgentDecisionEngine: the agentic AI advisor.  WHAT IT IS: a Claude to" | kind=entity | source=manager/backend/app/ai/agent.py:L1 | neighbors=[agent.py, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_agent_rationale_59": "Raised when the Anthropic SDK or API key is not configured." | kind=entity | source=manager/backend/app/ai/agent.py:L59 | neighbors=[AgentUnavailableError, AgentRecommendation, Asset, AttackPath, Finding, Service]
- "ai_prioritizer_vulnprioritizer_explain_prediction": ".explain_prediction()" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L158 | neighbors=[Per-feature contribution to this predic…, VulnPrioritizer, extract_features(), .fallback_score(), ._formula_contributions(), .predict_priority()]
- "alembic_env": "env.py" | kind=code-symbol | source=manager/backend/alembic/env.py:L1 | neighbors=[do_run_migrations(), run_migrations_offline(), run_migrations_online(), config.py, d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "auth_portal_scope_assert_client": "assert_client()" | kind=code-symbol | source=manager/backend/app/auth/portal_scope.py:L31 | neighbors=[portal_scope.py, client_scoped(), Return the client's bound engagement id…, require_client(), resolve_scope(), Return the client's bound engagement id…]
- "campaigns_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/campaigns/route.ts:L1 | neighbors=[GET(), POST(), campaign-store.ts, listCampaigns(), saveCampaign(), d98f654 feat(manager): network-VA campa…]
- "cancel_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/fleet/jobs/[jobId]/cancel/route.ts:L1 | neighbors=[POST, backend.ts, backend(), with-backend.ts, withBackend(), 8f6bf49 Refactor code structure and rem…]
- "cli_auth_loadsession": "loadSession()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L15 | neighbors=[auth.ts, requireAuth(), doctor.ts, interactive.ts, login.ts, logout.ts]
- "commands_interactive_ensureauthenticated": "ensureAuthenticated()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L117 | neighbors=[interactive.ts, ask(), askSecret(), ln(), mainMenu(), runInteractive()]
- "commands_interactive_runhostdiscoveryonly": "runHostDiscoveryOnly()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L595 | neighbors=[interactive.ts, choose(), confirm(), ln(), runIterativeEngagement(), wizardScan()]
- "commands_interactive_runphasewithtools": "runPhaseWithTools()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L963 | neighbors=[interactive.ts, runPhaseEnumeration(), runPhaseHostDiscovery(), runPhasePortScan(), runPhaseServiceDetect(), runPhaseVulnAssess()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bf61dbc3d12b9690e3e603f4adbf0e341f656c0c": "bf61dbc docs: probe run/test guide; gitignore nohup.out" | kind=Commit | source=git | neighbors=[bd85323 feat(probe): self-heal re-enrol…, addcapabilities-fable, feat/nvd-vuln-detection-and-ingest-hard…, main, ui-ux-backend-updates0109, 21ebc46 feat(detection): unified priori…]
- "console_freshness": "Freshness.tsx" | kind=code-symbol | source=manager/frontend/components/console/Freshness.tsx:L1 | neighbors=[07ba102 feat: enhance UI UX and detecti…, 3c9062a refactor: Update dashboard comp…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, Freshness(), DashboardGrid.tsx]
- "customers_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/route.ts:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "cve_ingest_get": "_get()" | kind=code-symbol | source=probe/cve/ingest.py:L55 | neighbors=[ingest.py, _ssl_context(), ingest_epss(), ingest_kev(), ingest_nvd(), GET with backoff on the transient failu…]
- "cve_ingest_ingest_nvd": "ingest_nvd()" | kind=code-symbol | source=probe/cve/ingest.py:L150 | neighbors=[ingest.py, ingest_all(), _get(), ingest_one_cve(), _ssl_context(), Pull the NVD CVE corpus into the mirror…]
- "cve_ingest_ingest_one_cve": "ingest_one_cve()" | kind=code-symbol | source=probe/cve/ingest.py:L117 | neighbors=[ingest.py, ingest_nvd(), _cvss(), _iter_cpe_matches(), _parse_criteria(), Upsert one NVD `cve` object + its CPE-a…]
- "cve_vulndb": "vulndb.py" | kind=code-symbol | source=probe/cve/vulndb.py:L1 | neighbors=[6e2818f Add support for additional serv…, _norm(), VulnDB, vulndb.py — the offline vulnerability m…, test_cve_correlation.py, test_weakness_map.py]
- "detection_active_validation": "active_validation.py" | kind=code-symbol | source=manager/backend/app/detection/active_validation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, 7bd104a feat(active-validation): pure r…, interpret_validation(), should_escalate(), ValidationOutcome, active_validation.py — manager-side dec…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-042.json

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
