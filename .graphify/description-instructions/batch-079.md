# Node Description Batch 80 of 119

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

- "discovery_rate_limiter_rationale_1": "RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[rate_limiter.py]
- "discovery_rate_limiter_rationale_44": "True if current time is inside the allowed scan window." | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L44 | neighbors=[.is_within_window()]
- "discovery_rate_limiter_rationale_61": "Blocks until a token is available for the given target IP.         Raises Runtim" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L61 | neighbors=[.acquire()]
- "discovery_service_id_rationale_1": "ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT" | kind=entity | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[service_id.py]
- "discovery_worker_discoveryjobpayload_post_init": ".__post_init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L50 | neighbors=[DiscoveryJobPayload]
- "discovery_worker_discoveryworker_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L61 | neighbors=[DiscoveryWorker]
- "discovery_xml_parser_parsedhost_open_ports": ".open_ports()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L36 | neighbors=[ParsedHost]
- "discovery_xml_parser_rationale_1": "Nmap XML output parser. Converts -oX output into structured ParsedHost / ParsedP" | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[xml_parser.py]
- "discovery_xml_parser_rationale_41": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L41 | neighbors=[NmapXMLParser]
- "discovery_xml_parser_rationale_42": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L42 | neighbors=[NmapXMLParser]
- "draft_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L4 | neighbors=[route.ts]
- "engagements_page_empty_form": "EMPTY_FORM" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L41 | neighbors=[page.tsx]
- "engagements_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L17 | neighbors=[page.tsx]
- "engagements_page_engagementsresponse": "EngagementsResponse" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L25 | neighbors=[page.tsx]
- "engagements_page_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L15 | neighbors=[page.tsx]
- "engagements_page_formstate": "FormState" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L33 | neighbors=[page.tsx]
- "engagements_page_rowskeleton": "RowSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L71 | neighbors=[page.tsx]
- "engagements_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L63 | neighbors=[page.tsx]
- "engagements_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L55 | neighbors=[page.tsx]
- "engagements_page_steps": "STEPS" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L84 | neighbors=[page.tsx]
- "engagements_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L13 | neighbors=[route.ts]
- "engagements_route_post": "POST" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L30 | neighbors=[route.ts]
- "engine_scan_modules_defaultmodules": "defaultModules()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L345 | neighbors=[scan-modules.ts]
- "engine_scan_modules_depthdefaults": "depthDefaults()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L385 | neighbors=[scan-modules.ts]
- "engine_scan_modules_modulebyid": "moduleById()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L329 | neighbors=[scan-modules.ts]
- "engine_scan_modules_modulecategory": "ModuleCategory" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L19 | neighbors=[scan-modules.ts]
- "engine_scan_modules_moduleinput": "ModuleInput" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L27 | neighbors=[scan-modules.ts]
- "engine_scan_modules_moduleoutput": "ModuleOutput" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L28 | neighbors=[scan-modules.ts]
- "engine_scan_modules_scanmodule": "ScanModule" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L30 | neighbors=[scan-modules.ts]
- "engine_tool_runners_httpxline": "HttpxLine" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L661 | neighbors=[tool-runners.ts]
- "engine_tool_runners_naabu_rate": "NAABU_RATE" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L25 | neighbors=[tool-runners.ts]
- "engine_tool_runners_nmap_timing": "NMAP_TIMING" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L26 | neighbors=[tool-runners.ts]
- "engine_tool_runners_nserunspec": "NseRunSpec" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1035 | neighbors=[tool-runners.ts]
- "engine_tool_runners_nsesection": "nseSection()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1070 | neighbors=[tool-runners.ts]
- "engine_tool_runners_processresult": "ProcessResult" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L97 | neighbors=[tool-runners.ts]
- "engine_tool_runners_rundnsrecon": "runDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L590 | neighbors=[tool-runners.ts]
- "engine_types_agentjob": "AgentJob" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L132 | neighbors=[types.ts]
- "engine_types_agentjobresult": "AgentJobResult" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L145 | neighbors=[types.ts]
- "engine_types_discoverydepth": "DiscoveryDepth" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L34 | neighbors=[types.ts]
- "engine_types_scanprofile": "ScanProfile" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L3 | neighbors=[types.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-079.json

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
