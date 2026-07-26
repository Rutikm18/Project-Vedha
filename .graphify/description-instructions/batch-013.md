# Node Description Batch 14 of 104

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

- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode(), build_parser(), _main()]
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "ad_findings_aderror": "ADError" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L22 | neighbors=[findings.py, ADConnectionError, Exception, FindingSeverity, FindingStatus, DependencyMissingError]
- "agent_agent_ws_http_poll_fallback": "_ws_http_poll_fallback()" | kind=code-symbol | source=probe/agent/agent.py:L432 | neighbors=[agent.py, Poll pending jobs even while WS is conn…, _run_ws_push_loop(), say(), _ws_flush_spool(), _ws_run_job()]
- "agent_cli_cmd_scan_run": "cmd_scan_run()" | kind=code-symbol | source=probe/agent/cli.py:L493 | neighbors=[cli.py, client_from_args(), .request(), output(), parse_param_pairs(), _poll_job()]
- "agent_license_verify_license": "verify_license()" | kind=code-symbol | source=probe/agent/license.py:L52 | neighbors=[license.py, check_license(), Returns the license payload dict if val…, _b64d(), host_fingerprint(), LicenseError]
- "agent_spool": "spool.go" | kind=code-symbol | source=probe-go/agent/spool.go:L1 | neighbors=[spool.go, .Count(), .Flush(), NewSpool(), .Save(), 2885afa Add comprehensive probe testing…]
- "agent_task_runner": "task_runner.py" | kind=code-symbol | source=probe/agent/task_runner.py:L1 | neighbors=[JobResult, TaskRunner, use_cases.py, task_runner.py — orchestrates the full …, 2885afa Add comprehensive probe testing…, test_integration.py]
- "agent_use_cases": "use_cases.py" | kind=code-symbol | source=probe/agent/use_cases.py:L1 | neighbors=[task_runner.py, resolve(), use_cases.py — the finite, pre-defined …, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "ai_llm_report_llmreportgenerator_generate_and_store": "._generate_and_store()" | kind=code-symbol | source=manager/backend/app/ai/llm_report.py:L262 | neighbors=[LLMReportGenerator, ._complete(), _uuid(), .generate_detection_rule_explanation(), .generate_executive_summary(), .generate_remediation_steps()]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L20 | neighbors=[GzipRequestMiddleware, middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware]
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()]
- "commands_interactive_pickengagementid": "pickEngagementId()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1757 | neighbors=[interactive.ts, choose(), fetchEngagements(), ln(), wizardEngagement(), wizardReport()]
- "commands_interactive_pickhostsubset": "pickHostSubset()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1138 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runPhasePortScan()]
- "commands_interactive_runautonomousmode": "runAutonomousMode()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L697 | neighbors=[interactive.ts, ask(), choose(), confirm(), ln(), runValidationFlow()]
- "commands_interactive_wizardadmin": "wizardAdmin()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1966 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardask": "wizardAsk()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1700 | neighbors=[interactive.ts, mainMenu(), ask(), confirm(), divider(), ln()]
- "commands_interactive_wizardfindings": "wizardFindings()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1625 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[index.ts, auth.ts, clearSession(), loadSession(), buildLogoutCommand(), 2885afa Add comprehensive probe testing…]
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[index.ts, auth.ts, apiFetch(), requireAuth(), buildWhoamiCommand(), 2885afa Add comprehensive probe testing…]
- "components_pageshell_pageshell": "PageShell()" | kind=code-symbol | source=manager/frontend/components/PageShell.tsx:L18 | neighbors=[page.tsx, PageShell.tsx, page.tsx, page.tsx, page.tsx, page.tsx]
- "config_config_load": "Load()" | kind=code-symbol | source=probe-go/config/config.go:L32 | neighbors=[config.go, env(), envBool(), envDuration(), envInt(), hostname()]
- "dashboard_protocolrow": "ProtocolRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, Exposure.tsx, ProtocolRow(), riskColor(), mock-dashboard.ts, ProtocolRisk]
- "detection_edr_edrqueryengine": "EDRQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L62 | neighbors=[edr.py, CrowdStrikeFalcon, .__init__(), .query_detections(), ._request(), MicrosoftDefender]
- "detection_engine_ai_normalizer_ainormalizercache_get": ".get()" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L152 | neighbors=[AINormalizerCache, ._key(), .propose_cpe(), extract_raw_text(), .propose_cpe(), propose_candidates()]
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()]
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()]
- "discovery_xml_parser_parsedhost": "ParsedHost" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L25 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, xml_parser.py, ._parse_host()]
- "engine_tool_runners_binname": "binName()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L75 | neighbors=[tool-runners.ts, bin(), isWindows(), runHostDiscovery(), runSshAudit(), runTestssl()]
- "engine_tool_runners_runnaabu": "runNaabu()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L145 | neighbors=[tools.ts, scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts()]
- "engine_types_scancallbacks": "ScanCallbacks" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L109 | neighbors=[agent.py, tools.ts, interactive.ts, scan.ts, scanner.ts, tool-runners.ts]
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, Exposure, GET, backend.ts, backend(), with-backend.ts]
- "graph_builder_graphbuilder_add_exploit_edges": ".add_exploit_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L183 | neighbors=[GraphBuilder, asset_node_id(), exploit_complexity(), finding_node_id(), _to_float(), .build_asset_graph()]
- "graph_demo_demoasset": "DemoAsset" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L27 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "graph_demo_demofinding": "DemoFinding" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L45 | neighbors=[demo.py, generate_demo_dataset(), Unit tests for the attack-path analysis…, TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "hooks_usetoast_usetoast": "useToast()" | kind=code-symbol | source=manager/frontend/hooks/useToast.ts:L6 | neighbors=[page.tsx, page.tsx, useToast.ts, page.tsx, page.tsx, page.tsx]
- "lib_backend_backenderror": "BackendError" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L13 | neighbors=[route.ts, route.ts, backend.ts, backend(), .constructor(), with-backend.ts]
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, route.ts, broadcastToScan(), Callback, scanListeners, subscribeScan()]
- "lib_tenant": "tenant.ts" | kind=code-symbol | source=manager/frontend/lib/tenant.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, middleware.ts, RESERVED, resolveTenantSubdomain(), rootDomain(), subdomainFromHost()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-013.json

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
