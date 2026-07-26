# Node Description Batch 10 of 104

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

- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult, Engagement]
- "scanner_safe": "safe.go" | kind=code-symbol | source=probe-go/scanner/safe.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, CircuitBreaker, RetryConfig, backoff(), DialContext(), IsRefused()]
- "scanner_smb_scanner": "smb_scanner.py" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), _netbios_session()]
- "scanner_udp": "udp.go" | kind=code-symbol | source=probe-go/scanner/udp.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, buildSNMPGetRequest(), dnsVersionQuery(), extractSNMPCommunity(), netbiosNameQuery(), ntpRequest()]
- "scanner_udp_scanner": "udp_scanner.py" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, run_scan.py, _dns_probe(), main(), _netbios_probe()]
- "start_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scans/start/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, auth-middleware.ts, AuthContext, withAuth(), job-store.ts, createJob()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L44 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L123 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L300 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port(), .test_no_matching_ports()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L631 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "ad_orchestrator_rationale_1": "ADAssessmentRunner — runs the full Active Directory assessment pipeline and retu" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L1 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_40": "Coordinates all AD checkers for a single engagement." | kind=entity | source=manager/backend/app/ad/orchestrator.py:L40 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "ad_orchestrator_rationale_63": "Returns {findings: [...], stats: {...}, errors: [...]}.         Never raises for" | kind=entity | source=manager/backend/app/ad/orchestrator.py:L63 | neighbors=[ADCSChecker, ASREPRoastChecker, BloodHoundCollector, ADConnectionError, DependencyMissingError, KerberoastChecker]
- "agent_cli_clierror": "CliError" | kind=code-symbol | source=probe/agent/cli.py:L27 | neighbors=[cli.py, Exception, cmd_auth_login(), cmd_engagements_create(), .load(), .request()]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L53 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_result_spool_resultspool": "ResultSpool" | kind=code-symbol | source=probe/agent/result_spool.py:L24 | neighbors=[result_spool.py, Persists scan results locally and retri…, .exists(), .flush_spool(), .__init__(), .load()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), AgentRecommendation, Asset, AttackPath, Finding]
- "ai_llm_report": "llm_report.py" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L1 | neighbors=[_collect_cves_scores(), _enum(), _finding_scores(), LLMReportGenerator, LLMUnavailableError, _uuid()]
- "ai_report_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/route.ts:L1 | neighbors=[POST, ai-engine.ts, generateReport(), auth-middleware.ts, withAuth(), engagements-store.ts]
- "app_layout": "layout.tsx" | kind=code-symbol | source=manager/frontend/app/layout.tsx:L1 | neighbors=[metadata, RootLayout(), QueryProvider.tsx, QueryProvider(), ThemeProvider.tsx, ThemeProvider()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_admin": "admin.ts" | kind=code-symbol | source=manager/frontend/cli/commands/admin.ts:L1 | neighbors=[index.ts, auth.ts, apiFetch(), requireAuth(), buildAdminCommand(), c]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1278 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commands_login": "login.ts" | kind=code-symbol | source=manager/frontend/cli/commands/login.ts:L1 | neighbors=[index.ts, auth.ts, loadSession(), saveSession(), serverUrl(), buildLoginCommand()]
- "commands_report": "report.ts" | kind=code-symbol | source=manager/frontend/cli/commands/report.ts:L1 | neighbors=[index.ts, auth.ts, apiFetch(), requireAuth(), AiReport, buildReportCommand()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "components_toastprovider": "ToastProvider.tsx" | kind=code-symbol | source=manager/frontend/components/ToastProvider.tsx:L1 | neighbors=[layout.tsx, 298a9d4 trim frontend to 7 core pages; …, Toast, TOAST_STYLES, ToastContext, ToastContextValue]
- "config_config": "config.go" | kind=code-symbol | source=probe-go/config/config.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, config.go, env(), envBool(), envDuration(), envInt()]
- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()]
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, GET, POST, adapters.ts, toApiEngagementCreate(), toUiEngagement()]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, MetasploitRPCError, ApprovalRequiredError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_safety": "safety.py" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, requires_approval(), SafetyViolationError]
- "graph_builder": "builder.py" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder]
- "hooks_usetoast": "useToast.ts" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, page.tsx, page.tsx, ToastProvider.tsx, ToastContext, useToast()]
- "ingest_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/ingest/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, types.ts, LiveFinding, POST(), agents-store.ts, getAgent()]
- "lib_nmap_parser": "nmap-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, extractScripts(), NmapHost, NmapScriptResult, NmapService]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-009.json

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
