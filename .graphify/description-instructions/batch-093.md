# Node Description Batch 94 of 134

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

- "id_page_cardskeleton": "CardSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L43 | neighbors=[page.tsx]
- "id_page_edit_statuses": "EDIT_STATUSES" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L345 | neighbors=[page.tsx]
- "id_page_editengagementmodal": "EditEngagementModal()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L347 | neighbors=[page.tsx]
- "id_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L19 | neighbors=[page.tsx]
- "id_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L69 | neighbors=[page.tsx]
- "id_page_findingrow": "FindingRow" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L61 | neighbors=[page.tsx]
- "id_page_findingstab": "FindingsTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L192 | neighbors=[page.tsx]
- "id_page_importscanbutton": "ImportScanButton()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L302 | neighbors=[page.tsx]
- "id_page_linkedtab": "LinkedTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L139 | neighbors=[page.tsx]
- "id_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L27 | neighbors=[page.tsx]
- "id_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L17 | neighbors=[page.tsx]
- "id_page_severity_color": "SEVERITY_COLOR" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L77 | neighbors=[page.tsx]
- "id_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L84 | neighbors=[page.tsx]
- "id_page_tabkey": "TabKey" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L16 | neighbors=[page.tsx]
- "id_route_apiactivity": "ApiActivity" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/route.ts:L12 | neighbors=[route.ts]
- "id_route_delete": "DELETE()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/route.ts:L43 | neighbors=[route.ts]
- "import_facts_route_base": "BASE" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L11 | neighbors=[route.ts]
- "import_facts_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L13 | neighbors=[route.ts]
- "intenum": "IntEnum" | kind=code-symbol | neighbors=[EvidenceTier]
- "jobid_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L4 | neighbors=[route.ts]
- "launch_route_intensity_presets": "INTENSITY_PRESETS" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L21 | neighbors=[route.ts]
- "launch_route_launchbody": "LaunchBody" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L5 | neighbors=[route.ts]
- "launch_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/scan/launch/route.ts:L29 | neighbors=[route.ts]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-093.json

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
