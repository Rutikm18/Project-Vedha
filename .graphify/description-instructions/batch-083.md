# Node Description Batch 84 of 119

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

- "intenum": "IntEnum" | kind=code-symbol | neighbors=[EvidenceTier]
- "jobid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L4 | neighbors=[route.ts]
- "launch_route_intensity_presets": "INTENSITY_PRESETS" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L20 | neighbors=[route.ts]
- "launch_route_launchbody": "LaunchBody" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L5 | neighbors=[route.ts]
- "launch_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L28 | neighbors=[route.ts]
- "launch_route_sshcreds": "SshCreds" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L5 | neighbors=[route.ts]
- "launch_route_wincreds": "WinCreds" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L6 | neighbors=[route.ts]
- "lib_adapters_detection_to_ui": "DETECTION_TO_UI" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L86 | neighbors=[adapters.ts]
- "lib_adapters_eng_status_to_api": "ENG_STATUS_TO_API" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L14 | neighbors=[adapters.ts]
- "lib_adapters_eng_status_to_ui": "ENG_STATUS_TO_UI" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L8 | neighbors=[adapters.ts]
- "lib_adapters_find_status_to_api": "FIND_STATUS_TO_API" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L193 | neighbors=[adapters.ts]
- "lib_adapters_find_status_to_ui": "FIND_STATUS_TO_UI" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L89 | neighbors=[adapters.ts]
- "lib_adapters_sev_to_ui": "SEV_TO_UI" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L82 | neighbors=[adapters.ts]
- "lib_agents_store_agent": "Agent" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L15 | neighbors=[agents-store.ts]
- "lib_agents_store_agentcapability": "AgentCapability" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L10 | neighbors=[agents-store.ts]
- "lib_agents_store_agents": "AGENTS" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L69 | neighbors=[agents-store.ts]
- "lib_agents_store_agentsstore": "agentsStore" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L220 | neighbors=[agents-store.ts]
- "lib_agents_store_agentstatus": "AgentStatus" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L5 | neighbors=[agents-store.ts]
- "lib_agents_store_field_agents_file": "FIELD_AGENTS_FILE" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L321 | neighbors=[agents-store.ts]
- "lib_agents_store_fieldagent": "FieldAgent" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L323 | neighbors=[agents-store.ts]
- "lib_agents_store_futureiso": "futureIso()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L62 | neighbors=[agents-store.ts]
- "lib_agents_store_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L60 | neighbors=[agents-store.ts]
- "lib_agents_store_jobs": "JOBS" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L134 | neighbors=[agents-store.ts]
- "lib_agents_store_jobstatus": "JobStatus" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L6 | neighbors=[agents-store.ts]
- "lib_agents_store_jobtype": "JobType" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L7 | neighbors=[agents-store.ts]
- "lib_agents_store_kafka_topics": "KAFKA_TOPICS" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L177 | neighbors=[agents-store.ts]
- "lib_agents_store_kafkatopic": "KafkaTopic" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L8 | neighbors=[agents-store.ts]
- "lib_agents_store_kafkatopicinfo": "KafkaTopicInfo" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L48 | neighbors=[agents-store.ts]
- "lib_agents_store_nowiso": "nowIso()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L61 | neighbors=[agents-store.ts]
- "lib_agents_store_scanjob": "ScanJob" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L31 | neighbors=[agents-store.ts]
- "lib_ai_engine_callanthropicwithretry": "callAnthropicWithRetry()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L163 | neighbors=[ai-engine.ts]
- "lib_ai_engine_criticality_score": "CRITICALITY_SCORE" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L68 | neighbors=[ai-engine.ts]
- "lib_ai_engine_destructive_patterns": "DESTRUCTIVE_PATTERNS" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L283 | neighbors=[ai-engine.ts]
- "lib_ai_engine_epss_mock": "EPSS_MOCK" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L84 | neighbors=[ai-engine.ts]
- "lib_ai_engine_genid": "genId()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L339 | neighbors=[ai-engine.ts]
- "lib_ai_engine_hallucinationresult": "HallucinationResult" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L52 | neighbors=[ai-engine.ts]
- "lib_ai_engine_hashprompt": "hashPrompt()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L340 | neighbors=[ai-engine.ts]
- "lib_ai_engine_kev_list": "KEV_LIST" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L92 | neighbors=[ai-engine.ts]
- "lib_ai_engine_llmoutput": "LLMOutput" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L36 | neighbors=[ai-engine.ts]
- "lib_ai_engine_llmoutputs": "llmOutputs" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L336 | neighbors=[ai-engine.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-083.json

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
