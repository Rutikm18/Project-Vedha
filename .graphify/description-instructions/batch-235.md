# Node Description Batch 236 of 380

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

- "lib_ai_engine_hashprompt": "hashPrompt()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L340 | neighbors=[ai-engine.ts]
- "lib_ai_engine_kev_list": "KEV_LIST" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L92 | neighbors=[ai-engine.ts]
- "lib_ai_engine_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L36 | neighbors=[ai-engine.ts]
- "lib_ai_engine_llmoutputs": "llmOutputs" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L336 | neighbors=[ai-engine.ts]
- "lib_ai_engine_mapfindingforwriteup": "mapFindingForWriteup()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L617 | neighbors=[ai-engine.ts]
- "lib_ai_engine_mapstatus": "mapStatus()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L520 | neighbors=[ai-engine.ts]
- "lib_ai_engine_modelfinding": "ModelFinding" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L592 | neighbors=[ai-engine.ts]
- "lib_ai_engine_numornull": "numOrNull()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L495 | neighbors=[ai-engine.ts]
- "lib_ai_engine_priorityfeatures": "PriorityFeatures" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L24 | neighbors=[ai-engine.ts]
- "lib_ai_engine_rankedfinding": "RankedFinding" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L593 | neighbors=[ai-engine.ts]
- "lib_ai_engine_reportjob": "ReportJob" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L58 | neighbors=[ai-engine.ts]
- "lib_ai_engine_reportjobs": "reportJobs" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L337 | neighbors=[ai-engine.ts]
- "lib_ai_engine_reportresult": "ReportResult" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L414 | neighbors=[ai-engine.ts]
- "lib_ai_engine_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L8 | neighbors=[ai-engine.ts]
- "lib_ai_engine_sev_rank_local": "SEV_RANK_LOCAL" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L590 | neighbors=[ai-engine.ts]
- "lib_ai_engine_shapexplanation": "ShapExplanation" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L30 | neighbors=[ai-engine.ts]
- "lib_ai_engine_simulated": "SIMULATED" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L196 | neighbors=[ai-engine.ts]
- "lib_ai_engine_weights": "WEIGHTS" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L73 | neighbors=[ai-engine.ts]
- "lib_aibrain_workspace_api_brainrequest": "BrainRequest" | kind=code-symbol | source=manager/frontend/lib/aibrain-workspace-api.ts:L7 | neighbors=[aibrain-workspace-api.ts]
- "lib_auth_middleware_authcontext": "AuthContext" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L5 | neighbors=[auth-middleware.ts]
- "lib_auth_middleware_handler": "Handler" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L9 | neighbors=[auth-middleware.ts]
- "lib_auth_middleware_withauth": "withAuth()" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L15 | neighbors=[auth-middleware.ts]
- "lib_auth_store_otpentry": "OtpEntry" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L8 | neighbors=[auth-store.ts]
- "lib_auth_store_otpstore": "otpStore" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L15 | neighbors=[auth-store.ts]
- "lib_auth_store_otpverifyresult": "OtpVerifyResult" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L34 | neighbors=[auth-store.ts]
- "lib_auth_store_sessionpayload": "SessionPayload" | kind=code-symbol | source=manager/frontend/lib/auth-store.ts:L17 | neighbors=[auth-store.ts]
- "lib_backend_backenderror_constructor": ".constructor()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L18 | neighbors=[BackendError]
- "lib_backend_backendopts": "BackendOpts" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L25 | neighbors=[backend.ts]
- "lib_backend_base": "BASE" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L11 | neighbors=[backend.ts]
- "lib_campaign_store_campaignstatus": "CampaignStatus" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L25 | neighbors=[campaign-store.ts]
- "lib_campaign_store_campaignsummary": "CampaignSummary" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L58 | neighbors=[campaign-store.ts]
- "lib_campaign_store_campaigntotals": "CampaignTotals" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L38 | neighbors=[campaign-store.ts]
- "lib_campaign_store_default_dir": "DEFAULT_DIR" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L72 | neighbors=[campaign-store.ts]
- "lib_campaign_store_normalizestage": "normalizeStage()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L122 | neighbors=[campaign-store.ts]
- "lib_campaign_store_stagesnapshot": "StageSnapshot" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L27 | neighbors=[campaign-store.ts]
- "lib_campaign_store_stagestatus": "StageStatus" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L24 | neighbors=[campaign-store.ts]
- "lib_cases_store_case": "Case" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L24 | neighbors=[cases-store.ts]
- "lib_cases_store_caseactivity": "CaseActivity" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L14 | neighbors=[cases-store.ts]
- "lib_cases_store_casecomment": "CaseComment" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L7 | neighbors=[cases-store.ts]
- "lib_cases_store_caseseverity": "CaseSeverity" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L4 | neighbors=[cases-store.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-235.json

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
