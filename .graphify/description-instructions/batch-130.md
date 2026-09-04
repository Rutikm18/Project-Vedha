# Node Description Batch 131 of 332

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

- "id_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L30 | neighbors=[route.ts, fail()]
- "lib_adapters_engstatustoapi": "engStatusToApi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L29 | neighbors=[adapters.ts, toApiEngagementPatch()]
- "lib_adapters_engstatustoui": "engStatusToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L26 | neighbors=[adapters.ts, toUiEngagement()]
- "lib_adapters_evidencetoui": "evidenceToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L104 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_severitytopriority": "severityToPriority()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L100 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_touiagent": "toUiAgent()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L215 | neighbors=[adapters.ts, route.ts]
- "lib_agents_store_genfieldagentid": "genFieldAgentId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L355 | neighbors=[agents-store.ts, registerAgent()]
- "lib_agents_store_getagent": "getAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L398 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_agents_store_getallagents": "getAllAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L394 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_ai_engine_chat": "chat()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L630 | neighbors=[ai-engine.ts, getClient()]
- "lib_ai_engine_hallucinationguard": "hallucinationGuard" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L289 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_llmreportgenerator": "llmReportGenerator" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L206 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_reportsection": "ReportSection" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L9 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_tomodelfindings": "toModelFindings()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L544 | neighbors=[ai-engine.ts, generateReport()]
- "lib_ai_engine_toscorecardinput": "toScorecardInput()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L524 | neighbors=[ai-engine.ts, generateReport()]
- "lib_ai_engine_vulnprioritizer": "vulnPrioritizer" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L97 | neighbors=[ai-engine.ts, route.ts]
- "lib_assistant_access_assistantauthstate": "AssistantAuthState" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L6 | neighbors=[AssistantProvider.tsx, assistant-access.ts]
- "lib_assistant_ageindays": "ageInDays()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L94 | neighbors=[assistant.ts, lifecycleOf()]
- "lib_assistant_lifecyclefacts": "LifecycleFacts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L6 | neighbors=[FactCard.tsx, assistant.ts]
- "lib_assistant_parseadvisor": "parseAdvisor()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L46 | neighbors=[route.ts, assistant.ts]
- "lib_assistant_preferredtext": "preferredText()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L168 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_assistant_publicseverity": "publicSeverity()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L174 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_auth_store_generateotp": "generateOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L24 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifyotp": "verifyOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L38 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifytoken": "verifyToken()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L64 | neighbors=[auth-middleware.ts, auth-store.ts]
- "lib_backend_safejson": "safeJson()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L67 | neighbors=[backend.ts, backend()]
- "lib_campaign_store_campaignsnapshot": "CampaignSnapshot" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L44 | neighbors=[campaign-store.ts, campaign-store.test.ts]
- "lib_campaign_store_setcampaigndir": "setCampaignDir()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L76 | neighbors=[campaign-store.ts, campaign-store.test.ts]
- "lib_cases_store_getcasebyid": "getCaseById()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L231 | neighbors=[cases-store.ts, readCases()]
- "lib_clients_store_client": "Client" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L27 | neighbors=[clients-store.ts, tenant-server.ts]
- "lib_clients_store_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L78 | neighbors=[clients-store.ts, read()]
- "lib_clients_store_listclients": "listClients()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L74 | neighbors=[clients-store.ts, read()]
- "lib_console_source_consolekey": "ConsoleKey" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L38 | neighbors=[DashboardGrid.tsx, console-source.tsx]
- "lib_console_source_operatorconsoleprovider": "OperatorConsoleProvider()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L116 | neighbors=[page.tsx, console-source.tsx]
- "lib_console_source_portalconsoleprovider": "PortalConsoleProvider()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L121 | neighbors=[console-source.tsx, page.tsx]
- "lib_console_source_useconsolecapability": "useConsoleCapability()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L148 | neighbors=[console-source.tsx, useConsoleSource()]
- "lib_detection_store_siemconfig": "SIEMConfig" | kind=code-symbol | source=manager/frontend/lib/detection-store.ts:L399 | neighbors=[detection-store.ts, route.ts]
- "lib_errors_errors": "Errors" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L124 | neighbors=[errors.ts, tool-runners.ts]
- "lib_findings_store_createfinding": "createFinding()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L114 | neighbors=[findings-store.ts, saveFindings()]
- "lib_findings_store_findingseverity": "FindingSeverity" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L7 | neighbors=[findings-store.ts, openvas-client.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-130.json

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
