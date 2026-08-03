# Node Description Batch 90 of 131

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

- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx]
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L177 | neighbors=[page.tsx]
- "findings_page_subscribetolocationchange": "subscribeToLocationChange()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L27 | neighbors=[page.tsx]
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L26 | neighbors=[route.ts]
- "findings_route_positiveint": "positiveInt()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L21 | neighbors=[route.ts]
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L97 | neighbors=[route.ts]
- "findings_route_status_to_api": "STATUS_TO_API" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L12 | neighbors=[route.ts]
- "findings_route_valid_severities": "VALID_SEVERITIES" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L11 | neighbors=[route.ts]
- "findings_route_valid_sorts": "VALID_SORTS" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L19 | neighbors=[route.ts]
- "fleet_page_enrollmentrequest": "EnrollmentRequest" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L11 | neighbors=[page.tsx]
- "fleet_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L34 | neighbors=[page.tsx]
- "fleet_page_fleetpage": "FleetPage()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L45 | neighbors=[page.tsx]
- "fleet_page_fleetresponse": "FleetResponse" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L23 | neighbors=[page.tsx]
- "fleet_page_inputstyle": "inputStyle" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L28 | neighbors=[page.tsx]
- "frontend_eslint_config_eslintconfig": "eslintConfig" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L5 | neighbors=[eslint.config.mjs]
- "frontend_next_config_dirname": "__dirname" | kind=code-symbol | source=manager/frontend/next.config.mjs:L4 | neighbors=[next.config.mjs]
- "frontend_next_config_frontendroot": "frontendRoot" | kind=code-symbol | source=manager/frontend/next.config.mjs:L5 | neighbors=[next.config.mjs]
- "frontend_next_config_nextconfig": "nextConfig" | kind=code-symbol | source=manager/frontend/next.config.mjs:L18 | neighbors=[next.config.mjs]
- "frontend_next_config_securityheaders": "securityHeaders" | kind=code-symbol | source=manager/frontend/next.config.mjs:L6 | neighbors=[next.config.mjs]
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
- "graph_analyzer_rationale_221": "Assets that appear in more than ``threshold`` (default 50%) of all paths —" | kind=entity | source=manager/backend/app/graph/analyzer.py:L221 | neighbors=[.identify_chokepoints()]
- "graph_analyzer_rationale_251": "Assets reachable (and thus at risk) if ``compromised_asset_id`` is owned." | kind=entity | source=manager/backend/app/graph/analyzer.py:L251 | neighbors=[.find_blast_radius()]
- "graph_analyzer_rationale_68": "Best (easiest) exploitable finding on an asset: {cvss, weight, finding}." | kind=entity | source=manager/backend/app/graph/analyzer.py:L68 | neighbors=[._exploit_info()]
- "graph_analyzer_rationale_88": "Build (and cache) the Asset→Asset movement projection. Edge weight is the" | kind=entity | source=manager/backend/app/graph/analyzer.py:L88 | neighbors=[.movement_graph()]
- "graph_builder_graphbuilder_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L91 | neighbors=[GraphBuilder]
- "graph_demo_rationale_1": "Demo dataset generator for the attack-path engine.  Produces a small but realist" | kind=entity | source=manager/backend/app/graph/demo.py:L1 | neighbors=[demo.py]
- "graph_demo_rationale_58": "Returns {engagement_id, assets, services, findings, credentials,     network_top" | kind=entity | source=manager/backend/app/graph/demo.py:L58 | neighbors=[generate_demo_dataset()]
- "graph_neo4j_client_neo4jclient_available": ".available()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L58 | neighbors=[Neo4jClient]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-089.json

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
