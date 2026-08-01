# Node Description Batch 12 of 119

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

- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult, Engagement]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult, Engagement]
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _build_get(), _extract_sysdescr(), main()]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, FindingFilter, FindingOut, FindingPatch]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L44 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config.py, test_ai_request_rejects_unsafe_model_an…, test_manager_ollama_generation_owns_sec…, test_manager_openai_generation_is_serve…, test_manager_openai_rejects_unconfigure…]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L745 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L118 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()]
- "workflow_cache": "cache.py" | kind=code-symbol | source=probe/workflow/cache.py:L1 | neighbors=[engine.py, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, scanner_base.py, CacheEntry]
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L547 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), _flush_spool_over_http(), say(), _ws_run_job()]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, _maybe_decimal(), _maybe_uuid(), _tool_result(), _val()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), AgentRecommendation, Asset, AttackPath, Finding]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, backup-before-secret-removal, main, spike/probe-go, e8262a3 feat(probe): explicit unauthent…]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, main, spike/probe-go, 01f4398 feat(probe): IoT survey reaches…, web_scanner.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, backup-before-secret-removal, main, spike/probe-go, bce780a feat(probe): enumerate HTTP met…]
- "dashboard_slarow": "SlaRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/SlaRow.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, getSla(), SEV_BG, SEV_COLOR, SlaRow(), Severity]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
