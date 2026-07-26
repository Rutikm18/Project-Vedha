# Node Description Batch 21 of 104

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

- "graph_demo_generate_demo_dataset": "generate_demo_dataset()" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L57 | neighbors=[demo.py, DemoAsset, DemoFinding, DemoService, Returns {engagement_id, assets, service…]
- "import_facts_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, BASE, POST(), backend.ts, bearerFrom()]
- "lib_backend_bearerfrom": "bearerFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L64 | neighbors=[route.ts, route.ts, route.ts, backend.ts, with-backend.ts]
- "lib_cases_store_writecases": "writeCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L226 | neighbors=[cases-store.ts, addComment(), createCase(), updateCase(), ensureDataDir()]
- "lib_detection_store_detectionstore": "detectionStore" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L421 | neighbors=[route.ts, detection-store.ts, route.ts, route.ts, route.ts]
- "lib_finding_id_generatefindingid": "generateFindingId()" | kind=code-symbol | source=manager/frontend/lib/finding-id.ts:L13 | neighbors=[scanner.ts, tool-runners.ts, finding-id.ts, findings-store.ts, testssl-parser.ts]
- "lib_findings_store_getfindingbyid": "getFindingById()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L75 | neighbors=[findings.ts, interactive.ts, findings-store.ts, getAllFindings(), findings-store.test.ts]
- "lib_findings_store_updatefinding": "updateFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L132 | neighbors=[tools.ts, interactive.ts, findings-store.ts, ensureDir(), getAllFindings()]
- "lib_findings_store_updatefindingstatus": "updateFindingStatus()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L79 | neighbors=[interactive.ts, findings-store.ts, ensureDir(), getAllFindings(), findings-store.test.ts]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs(), route.ts]
- "lib_job_store_writejobs": "writeJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L32 | neighbors=[job-store.ts, createJob(), markDispatched(), updateJobStatus(), ensureDir()]
- "lib_nmap_parser_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L48 | neighbors=[tool-runners.ts, nmap-parser.ts, extractScripts(), toArray(), parsers.test.ts]
- "lib_nuclei_parser_parsenucleiline": "parseNucleiLine()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L35 | neighbors=[tool-runners.ts, nuclei-parser.ts, route.ts, route.ts, parsers.test.ts]
- "lib_permissions_store_getuser": "getUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L44 | neighbors=[permissions-store.ts, read(), isAdmin(), isScopeAllowed(), route.ts]
- "lib_permissions_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L35 | neighbors=[permissions-store.ts, addUser(), removeUser(), updateScopes(), ensureDir()]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget(), route.ts]
- "lib_testssl_parser_parsetestssljson": "parseTestsslJson()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L38 | neighbors=[tool-runners.ts, testssl-parser.ts, mapSeverity(), parseTestsslOutput(), parsers.test.ts]
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L1 | neighbors=[2885afa Add comprehensive probe testing…, fetcher.ts, storeToken(), LoginForm(), LoginPage()]
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, Enum, Agent, AgentStatus]
- "naabu_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/naabu/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, parseNaabuOutput(), POST(), validateTargets()]
- "pipeline_pipeline_assemble": "assemble()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L396 | neighbors=[pipeline.go, buildHostsMap(), countOpenPorts(), assembleError(), Run()]
- "probe_go_main_main": "main()" | kind=code-symbol | source=probe-go/main.go:L32 | neighbors=[main.go, envFilePath(), localScan(), run(), selfTest()]
- "probe_pipeline_run_active": "_run_active()" | kind=code-symbol | source=probe/pipeline.py:L144 | neighbors=[pipeline.py, _Collector, .write(), _rollup(), _shared()]
- "reject_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, ai-engine.ts, aiReportStore, POST()]
- "routers_activity": "activity.py" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, dependencies.py, ActivityItem, recent_activity(), Recent activity feed.  A tenant-wide, r…]
- "routers_agent_advisor_rationale_1": "agent_advisor.py — API for the agentic AI advisor (recommend-only).  POST /engag" | kind=entity | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[AgentDecisionEngine, AgentUnavailableError, AgentRecommendation, Engagement, agent_advisor.py]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, config.py, database.py, agent_websocket_endpoint(), agent_ws.py — WebSocket endpoint for pr…]
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L245 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), Verify that the JWT token bearer IS the…, submit_job_result()]
- "routers_attack_paths_build_analyzer": "_build_analyzer()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L176 | neighbors=[attack_paths.py, attack_graph(), blast_radius(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_list_chokepoints": "list_chokepoints()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L118 | neighbors=[attack_paths.py, _all_paths_to_critical(), _asset_labels(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_recompute_and_store": "_recompute_and_store()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L200 | neighbors=[attack_paths.py, list_attack_paths(), _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_detection_runs_rationale_1": "detection_runs.py — temporal detection API (\"what changed since last time\").  GE" | kind=entity | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[DetectionRun, Engagement, FindingStatus, Finding, detection_runs.py]
- "routers_findings_rationale_29": "Compute SLA state across the tenant's tracked findings (open/confirmed).     Opt" | kind=entity | source=manager/backend/app/routers/findings.py:L29 | neighbors=[Engagement, FindingStatus, Finding, sla_summary(), PaginatedResponse]
- "scanner_circuitbreaker": "CircuitBreaker" | kind=code-symbol | source=probe-go/scanner/safe.go:L141 | neighbors=[.Allow(), .RecordFailure(), .RecordSuccess(), .Tripped(), safe.go]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L122 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "scanner_port_scanner_portscanner": "PortScanner" | kind=code-symbol | source=probe/scanner/port_scanner.py:L27 | neighbors=[port_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "scanner_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L401 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "scanner_scanner_base_ratelimiter": "RateLimiter" | kind=code-symbol | source=probe/scanner/scanner_base.py:L182 | neighbors=[scanner_base.py, .__init__(), .__init__(), .wait(), Simple async rate limiter: at most `rat…]
- "scanner_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/scanner/service_banner.py:L34 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), .scan_target()]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L84 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-020.json

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
