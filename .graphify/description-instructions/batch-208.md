# Node Description Batch 209 of 336

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

- "lib_agents_store_jobtype": "JobType" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L7 | neighbors=[agents-store.ts]
- "lib_agents_store_kafka_topics": "KAFKA_TOPICS" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L177 | neighbors=[agents-store.ts]
- "lib_agents_store_kafkatopic": "KafkaTopic" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L8 | neighbors=[agents-store.ts]
- "lib_agents_store_kafkatopicinfo": "KafkaTopicInfo" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L48 | neighbors=[agents-store.ts]
- "lib_agents_store_nowiso": "nowIso()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L61 | neighbors=[agents-store.ts]
- "lib_agents_store_scanjob": "ScanJob" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L31 | neighbors=[agents-store.ts]
- "lib_ai_engine_assemblefinding": "assembleFinding()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L646 | neighbors=[ai-engine.ts]
- "lib_ai_engine_callanthropicwithretry": "callAnthropicWithRetry()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L163 | neighbors=[ai-engine.ts]
- "lib_ai_engine_classifydomain": "classifyDomain()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L501 | neighbors=[ai-engine.ts]
- "lib_ai_engine_compactfinding": "compactFinding()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L662 | neighbors=[ai-engine.ts]
- "lib_ai_engine_criticality_score": "CRITICALITY_SCORE" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L68 | neighbors=[ai-engine.ts]
- "lib_ai_engine_deriveconfidence": "deriveConfidence()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L526 | neighbors=[ai-engine.ts]
- "lib_ai_engine_destructive_patterns": "DESTRUCTIVE_PATTERNS" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L283 | neighbors=[ai-engine.ts]
- "lib_ai_engine_epss_mock": "EPSS_MOCK" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L84 | neighbors=[ai-engine.ts]
- "lib_ai_engine_fallbackwriteup": "fallbackWriteup()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L629 | neighbors=[ai-engine.ts]
- "lib_ai_engine_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L339 | neighbors=[ai-engine.ts]
- "lib_ai_engine_groupinginput": "groupingInput()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L675 | neighbors=[ai-engine.ts]
- "lib_ai_engine_hallucinationresult": "HallucinationResult" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L52 | neighbors=[ai-engine.ts]
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
- "lib_ai_engine_reportsession": "ReportSession" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L424 | neighbors=[ai-engine.ts]
- "lib_ai_engine_reviewstatus": "ReviewStatus" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L8 | neighbors=[ai-engine.ts]
- "lib_ai_engine_sev_rank_local": "SEV_RANK_LOCAL" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L590 | neighbors=[ai-engine.ts]
- "lib_ai_engine_shapexplanation": "ShapExplanation" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L30 | neighbors=[ai-engine.ts]
- "lib_ai_engine_simulated": "SIMULATED" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L196 | neighbors=[ai-engine.ts]
- "lib_ai_engine_weights": "WEIGHTS" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L73 | neighbors=[ai-engine.ts]
- "lib_auth_middleware_authcontext": "AuthContext" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L5 | neighbors=[auth-middleware.ts]
- "lib_auth_middleware_handler": "Handler" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L9 | neighbors=[auth-middleware.ts]
- "lib_auth_middleware_withauth": "withAuth()" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L15 | neighbors=[auth-middleware.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-208.json

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
