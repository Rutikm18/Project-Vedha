# Node Description Batch 49 of 104

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

- "lib_adapters_touiagent": "toUiAgent()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L154 | neighbors=[adapters.ts, route.ts]
- "lib_agents_store_genfieldagentid": "genFieldAgentId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L355 | neighbors=[agents-store.ts, registerAgent()]
- "lib_agents_store_getallagents": "getAllAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L394 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_ai_engine_chat": "chat()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L488 | neighbors=[ai-engine.ts, getClient()]
- "lib_ai_engine_hallucinationguard": "hallucinationGuard" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L290 | neighbors=[route.ts, ai-engine.ts]
- "lib_ai_engine_llmreportgenerator": "llmReportGenerator" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L206 | neighbors=[route.ts, ai-engine.ts]
- "lib_ai_engine_reportsection": "ReportSection" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L9 | neighbors=[route.ts, ai-engine.ts]
- "lib_ai_engine_vulnprioritizer": "vulnPrioritizer" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L97 | neighbors=[ai-engine.ts, route.ts]
- "lib_auth_middleware_authcontext": "AuthContext" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L5 | neighbors=[auth-middleware.ts, route.ts]
- "lib_auth_store_generateotp": "generateOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L24 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifyotp": "verifyOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L38 | neighbors=[auth-store.ts, route.ts]
- "lib_backend_safejson": "safeJson()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L55 | neighbors=[backend.ts, backend()]
- "lib_cases_store_getcasebyid": "getCaseById()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L231 | neighbors=[cases-store.ts, readCases()]
- "lib_clients_store_client": "Client" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L27 | neighbors=[clients-store.ts, tenant-server.ts]
- "lib_clients_store_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L78 | neighbors=[clients-store.ts, read()]
- "lib_clients_store_listclients": "listClients()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L74 | neighbors=[clients-store.ts, read()]
- "lib_detection_store_siemconfig": "SIEMConfig" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L399 | neighbors=[detection-store.ts, route.ts]
- "lib_engagements_store_engagementsstore": "engagementsStore" | kind=code-symbol | source=manager/frontend/lib/engagements-store.ts:L122 | neighbors=[route.ts, engagements-store.ts]
- "lib_errors_errors": "Errors" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L124 | neighbors=[tool-runners.ts, errors.ts]
- "lib_findings_store_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L7 | neighbors=[findings-store.ts, openvas-client.ts]
- "lib_findings_store_setdatapath": "setDataPath()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L13 | neighbors=[findings-store.ts, findings-store.test.ts]
- "lib_findings_store_sladeadline": "slaDeadline()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L27 | neighbors=[findings-store.ts, saveFindings()]
- "lib_graph_store_edgesforpath": "edgesForPath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L241 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_graph_store_scorepath": "scorePath()" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L225 | neighbors=[graph-store.ts, buildAttackPaths()]
- "lib_job_store_genjobid": "genJobId()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L37 | neighbors=[job-store.ts, createJob()]
- "lib_job_store_getnextjobforagent": "getNextJobForAgent()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L62 | neighbors=[job-store.ts, readJobs()]
- "lib_nuclei_parser_nucleimatch": "NucleiMatch" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L3 | neighbors=[nuclei-parser.ts, scan-pipeline.ts]
- "lib_openvas_client_gettask": "getTask()" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L28 | neighbors=[openvas-client.ts, route.ts]
- "lib_openvas_client_openvasfinding": "OpenVASFinding" | kind=code-symbol | source=manager/frontend/lib/openvas-client.ts:L3 | neighbors=[openvas-client.ts, scan-pipeline.ts]
- "lib_permissions_store_getallusers": "getAllUsers()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L40 | neighbors=[permissions-store.ts, read()]
- "lib_permissions_store_iptoint": "ipToInt()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L120 | neighbors=[permissions-store.ts, targetMatchesScope()]
- "lib_permissions_store_permitteduser": "PermittedUser" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L8 | neighbors=[admin.ts, permissions-store.ts]
- "lib_permissions_store_targetmatchesscope": "targetMatchesScope()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L124 | neighbors=[permissions-store.ts, ipToInt()]
- "lib_scan_events_broadcasttoscan": "broadcastToScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L20 | neighbors=[route.ts, scan-events.ts]
- "lib_scan_events_subscribescan": "subscribeScan()" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L7 | neighbors=[scan-events.ts, route.ts]
- "lib_scan_pipeline_computeoverallprogress": "computeOverallProgress()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L117 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_createinitialpipelinestate": "createInitialPipelineState()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L89 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_drainscanevents": "drainScanEvents()" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L83 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_pipelinestate": "PipelineState" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L33 | neighbors=[scan-pipeline.ts, route.ts]
- "lib_scan_pipeline_profile_tools": "PROFILE_TOOLS" | kind=code-symbol | source=manager/frontend/lib/scan-pipeline.ts:L58 | neighbors=[scan-pipeline.ts, route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-048.json

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
