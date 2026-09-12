# Node Description Batch 148 of 380

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
- "lib_adapters_engstatustoapi": "engStatusToApi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L31 | neighbors=[adapters.ts, toApiEngagementPatch()]
- "lib_adapters_engstatustoui": "engStatusToUi()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L28 | neighbors=[adapters.ts, toUiEngagement()]
- "lib_adapters_evidencestring": "evidenceString()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L106 | neighbors=[adapters.ts, evidenceToUi()]
- "lib_adapters_optionalevidencestring": "optionalEvidenceString()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L116 | neighbors=[adapters.ts, evidenceToUi()]
- "lib_adapters_severitytopriority": "severityToPriority()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L102 | neighbors=[adapters.ts, toUiFinding()]
- "lib_adapters_touiagent": "toUiAgent()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L282 | neighbors=[adapters.ts, route.ts]
- "lib_agents_store_genfieldagentid": "genFieldAgentId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L355 | neighbors=[agents-store.ts, registerAgent()]
- "lib_agents_store_getagent": "getAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L398 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_agents_store_getallagents": "getAllAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L394 | neighbors=[agents-store.ts, readFieldAgents()]
- "lib_ai_engine_chat": "chat()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L822 | neighbors=[ai-engine.ts, getClient()]
- "lib_ai_engine_countseverities": "countSeverities()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L683 | neighbors=[ai-engine.ts, generateReportSectioned()]
- "lib_ai_engine_hallucinationguard": "hallucinationGuard" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L289 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_llmreportgenerator": "llmReportGenerator" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L206 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_reportsection": "ReportSection" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L9 | neighbors=[ai-engine.ts, route.ts]
- "lib_ai_engine_reportsession": "ReportSession" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L424 | neighbors=[route.ts, ai-engine.ts]
- "lib_ai_engine_vulnprioritizer": "vulnPrioritizer" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L97 | neighbors=[ai-engine.ts, route.ts]
- "lib_aibrain_workspace_api_aibrainworkspacesurface": "AIBrainWorkspaceSurface" | kind=code-symbol | source=manager/frontend/lib/aibrain-workspace-api.ts:L5 | neighbors=[page.tsx, aibrain-workspace-api.ts]
- "lib_aibrain_workspace_api_createaibrainworkspaceapi": "createAIBrainWorkspaceApi()" | kind=code-symbol | source=manager/frontend/lib/aibrain-workspace-api.ts:L14 | neighbors=[page.tsx, aibrain-workspace-api.ts]
- "lib_assistant_access_assistantauthstate": "AssistantAuthState" | kind=code-symbol | source=manager/frontend/lib/assistant-access.ts:L6 | neighbors=[AssistantProvider.tsx, assistant-access.ts]
- "lib_assistant_ageindays": "ageInDays()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L94 | neighbors=[assistant.ts, lifecycleOf()]
- "lib_assistant_lifecyclefacts": "LifecycleFacts" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L6 | neighbors=[FactCard.tsx, assistant.ts]
- "lib_assistant_parseadvisor": "parseAdvisor()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L46 | neighbors=[route.ts, assistant.ts]
- "lib_assistant_preferredtext": "preferredText()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L168 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_assistant_publicseverity": "publicSeverity()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L174 | neighbors=[assistant.ts, cveRecordToFactCard()]
- "lib_auth_store_generateotp": "generateOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L24 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifyotp": "verifyOtp()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L38 | neighbors=[auth-store.ts, route.ts]
- "lib_auth_store_verifytoken": "verifyToken()" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L64 | neighbors=[auth-middleware.ts, auth-store.ts]
- "lib_backend_safejson": "safeJson()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L84 | neighbors=[backend.ts, backend()]
- "lib_campaign_store_campaignsnapshot": "CampaignSnapshot" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L44 | neighbors=[campaign-store.ts, campaign-store.test.ts]
- "lib_campaign_store_setcampaigndir": "setCampaignDir()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L76 | neighbors=[campaign-store.ts, campaign-store.test.ts]
- "lib_campaign_workspace_api_campaignworkspacesurface": "CampaignWorkspaceSurface" | kind=code-symbol | source=manager/frontend/lib/campaign-workspace-api.ts:L5 | neighbors=[page.tsx, campaign-workspace-api.ts]
- "lib_campaign_workspace_api_createcampaignworkspaceapi": "createCampaignWorkspaceApi()" | kind=code-symbol | source=manager/frontend/lib/campaign-workspace-api.ts:L7 | neighbors=[page.tsx, campaign-workspace-api.ts]
- "lib_cases_store_getcasebyid": "getCaseById()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L231 | neighbors=[cases-store.ts, readCases()]
- "lib_clients_store_client": "Client" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L27 | neighbors=[clients-store.ts, tenant-server.ts]
- "lib_clients_store_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L78 | neighbors=[clients-store.ts, read()]
- "lib_clients_store_listclients": "listClients()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L74 | neighbors=[clients-store.ts, read()]
- "lib_console_source_consolekey": "ConsoleKey" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L39 | neighbors=[DashboardGrid.tsx, console-source.tsx]
- "lib_console_source_normalizeportaldataset": "normalizePortalDataset()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L190 | neighbors=[console-source.tsx, console-source.test.ts]
- "lib_console_source_operatorconsoleprovider": "OperatorConsoleProvider()" | kind=code-symbol | source=manager/frontend/lib/console-source.tsx:L134 | neighbors=[page.tsx, console-source.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-147.json

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
