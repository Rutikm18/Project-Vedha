# Node Description Batch 148 of 236

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

- "findings_page_verification_meta": "VERIFICATION_META" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L187 | neighbors=[page.tsx]
- "findings_page_verificationbadge": "VerificationBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L193 | neighbors=[page.tsx]
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L27 | neighbors=[route.ts]
- "findings_route_positiveint": "positiveInt()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L22 | neighbors=[route.ts]
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L103 | neighbors=[route.ts]
- "findings_route_status_to_api": "STATUS_TO_API" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L12 | neighbors=[route.ts]
- "findings_route_valid_severities": "VALID_SEVERITIES" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L11 | neighbors=[route.ts]
- "findings_route_valid_sorts": "VALID_SORTS" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L19 | neighbors=[route.ts]
- "findings_route_valid_verification": "VALID_VERIFICATION" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L20 | neighbors=[route.ts]
- "fleet_page_agentstatus": "agentStatus()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L79 | neighbors=[page.tsx]
- "fleet_page_ago": "ago()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L86 | neighbors=[page.tsx]
- "fleet_page_enrollmentrequest": "EnrollmentRequest" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L11 | neighbors=[page.tsx]
- "fleet_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L95 | neighbors=[page.tsx]
- "fleet_page_fleetpage": "FleetPage()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L106 | neighbors=[page.tsx]
- "fleet_page_fleetresponse": "FleetResponse" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L23 | neighbors=[page.tsx]
- "fleet_page_inputstyle": "inputStyle" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L28 | neighbors=[page.tsx]
- "fleet_page_jobbadge": "jobBadge()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L67 | neighbors=[page.tsx]
- "fleet_page_probe": "Probe" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L42 | neighbors=[page.tsx]
- "fleet_page_probejob": "ProbeJob" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L55 | neighbors=[page.tsx]
- "fleet_page_statebadge": "stateBadge()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L30 | neighbors=[page.tsx]
- "frontend_eslint_config_eslintconfig": "eslintConfig" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L5 | neighbors=[eslint.config.mjs]
- "frontend_next_config_app_version": "APP_VERSION" | kind=code-symbol | source=manager/frontend/next.config.mjs:L22 | neighbors=[next.config.mjs]
- "frontend_next_config_dirname": "__dirname" | kind=code-symbol | source=manager/frontend/next.config.mjs:L5 | neighbors=[next.config.mjs]
- "frontend_next_config_frontendroot": "frontendRoot" | kind=code-symbol | source=manager/frontend/next.config.mjs:L6 | neighbors=[next.config.mjs]
- "frontend_next_config_nextconfig": "nextConfig" | kind=code-symbol | source=manager/frontend/next.config.mjs:L36 | neighbors=[next.config.mjs]
- "frontend_next_config_resolveappversion": "resolveAppVersion()" | kind=code-symbol | source=manager/frontend/next.config.mjs:L12 | neighbors=[next.config.mjs]
- "frontend_next_config_securityheaders": "securityHeaders" | kind=code-symbol | source=manager/frontend/next.config.mjs:L24 | neighbors=[next.config.mjs]
- "frontend_postcss_config_config": "config" | kind=code-symbol | source=manager/frontend/postcss.config.mjs:L1 | neighbors=[postcss.config.mjs]
- "frontend_proxy_config": "config" | kind=code-symbol | source=manager/frontend/proxy.ts:L57 | neighbors=[proxy.ts]
- "frontend_proxy_public_paths": "PUBLIC_PATHS" | kind=code-symbol | source=manager/frontend/proxy.ts:L5 | neighbors=[proxy.ts]
- "frontend_proxy_public_prefixes": "PUBLIC_PREFIXES" | kind=code-symbol | source=manager/frontend/proxy.ts:L8 | neighbors=[proxy.ts]
- "gaps_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/gaps/route.ts:L5 | neighbors=[route.ts]
- "generate_route_demo_asset": "DEMO_ASSET" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L28 | neighbors=[route.ts]
- "generate_route_demo_engagement": "DEMO_ENGAGEMENT" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L7 | neighbors=[route.ts]
- "generate_route_demo_finding": "DEMO_FINDING" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L19 | neighbors=[route.ts]
- "generate_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/generate/route.ts:L5 | neighbors=[route.ts]
- "graph_analyzer_pathanalyzer_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L61 | neighbors=[PathAnalyzer]
- "graph_analyzer_rationale_1": "PathAnalyzer — attack-path discovery, scoring, chokepoint and blast-radius analy" | kind=entity | source=manager/backend/app/graph/analyzer.py:L1 | neighbors=[analyzer.py]
- "graph_analyzer_rationale_147": "Return scored attack paths from every source asset to the target.         Each p" | kind=entity | source=manager/backend/app/graph/analyzer.py:L147 | neighbors=[.find_paths_to_target()]
- "graph_analyzer_rationale_200": "Risk score 0–100 from: sum of exploit CVSS along the path, a penalty for" | kind=entity | source=manager/backend/app/graph/analyzer.py:L200 | neighbors=[.score_path()]

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
