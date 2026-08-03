# Node Description Batch 13 of 131

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

- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L118 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, scanner_base.py, CacheEntry]
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[orchestrator.py, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADAssessmentRunner, ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[.run(), ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError]
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L91 | neighbors=[agent.py, _bounded_env_int(), _is_local_manager_url(), _load_env(), _obtain_identity(), _poll_jobs_or_empty()]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, AgentRecommendation, Asset]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "auth_middleware": "middleware.py" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L1 | neighbors=[database.py, agent_jwt_path_allows(), _is_public_enrollment_request(), TenantIsolationMiddleware, 10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L58 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, GzipRequestMiddleware]
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, backup-before-secret-removal, main, spike/probe-go, e8262a3 feat(probe): explicit unauthent…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, main, spike/probe-go, 01f4398 feat(probe): IoT survey reaches…, web_scanner.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, backup-before-secret-removal, main, spike/probe-go, bce780a feat(probe): enumerate HTTP met…]
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx]
- "dashboard_slarow": "SlaRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, getSla(), SEV_BG, SEV_COLOR, SlaRow(), Severity]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), run_detection_job()]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_engine_update_snapshot": "update_snapshot.py" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _all_known_cve_ids(), main(), _query_osv(), _ssl_context(), sync_epss_snapshot()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, _content_hash(), _default_products(), load_snapshot(), SnapshotMeta]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "explain_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/explain/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, ManagerAiResponse, POST(), backend.ts, backend(), BackendError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[.validate_safety(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[.validate_scope(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-012.json

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
