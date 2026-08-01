# Node Description Batch 83 of 119

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

- "graph_analyzer_rationale_68": "Best (easiest) exploitable finding on an asset: {cvss, weight, finding}." | kind=entity | source=manager/backend/app/graph/analyzer.py:L68 | neighbors=[._exploit_info()]
- "graph_analyzer_rationale_88": "Build (and cache) the Asset→Asset movement projection. Edge weight is the" | kind=entity | source=manager/backend/app/graph/analyzer.py:L88 | neighbors=[.movement_graph()]
- "graph_builder_graphbuilder_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L91 | neighbors=[GraphBuilder]
- "graph_demo_rationale_1": "Demo dataset generator for the attack-path engine.  Produces a small but realist" | kind=entity | source=manager/backend/app/graph/demo.py:L1 | neighbors=[demo.py]
- "graph_demo_rationale_58": "Returns {engagement_id, assets, services, findings, credentials,     network_top" | kind=entity | source=manager/backend/app/graph/demo.py:L58 | neighbors=[generate_demo_dataset()]
- "graph_neo4j_client_neo4jclient_available": ".available()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L58 | neighbors=[Neo4jClient]
- "graph_neo4j_client_neo4jclient_close": ".close()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L102 | neighbors=[Neo4jClient]
- "graph_neo4j_client_neo4jclient_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L51 | neighbors=[Neo4jClient]
- "graph_neo4j_client_rationale_1": "Neo4jClient — thin, optional wrapper around the neo4j Python driver.  Neo4j is *" | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[neo4j_client.py]
- "graph_neo4j_client_rationale_49": "Connection holder + query helper. No-ops cleanly when the driver is absent." | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L49 | neighbors=[Neo4jClient]
- "graph_neo4j_client_rationale_62": "Open the driver and verify connectivity. Returns False on any failure." | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L62 | neighbors=[.connect()]
- "graph_neo4j_client_rationale_77": "Apply constraints + indexes (idempotent)." | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L77 | neighbors=[.ensure_schema()]
- "graph_neo4j_client_rationale_88": "Run a Cypher statement and return records as dicts. [] if not connected." | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L88 | neighbors=[.run()]
- "graph_neo4j_client_rationale_96": "Run a parametrised write with UNWIND batching for bulk node/edge loads." | kind=entity | source=manager/backend/app/graph/neo4j_client.py:L96 | neighbors=[.run_write()]
- "graph_visualizer_graphvisualizer_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L44 | neighbors=[GraphVisualizer]
- "graph_visualizer_rationale_1": "GraphVisualizer — serialise the attack graph into D3-compatible JSON for the fro" | kind=entity | source=manager/backend/app/graph/visualizer.py:L1 | neighbors=[visualizer.py]
- "graph_visualizer_rationale_19": "Numpy-free seed layout: place nodes on concentric rings by type so the     front" | kind=entity | source=manager/backend/app/graph/visualizer.py:L19 | neighbors=[_deterministic_layout()]
- "graph_visualizer_rationale_53": "Build the D3 payload. ``compromised`` is a set of asset entity_ids to flag" | kind=entity | source=manager/backend/app/graph/visualizer.py:L53 | neighbors=[.to_d3()]
- "id_page_activityitem": "ActivityItem" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L37 | neighbors=[page.tsx]
- "id_page_activitytab": "ActivityTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L285 | neighbors=[page.tsx]
- "id_page_assetrow": "AssetRow" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L45 | neighbors=[page.tsx]
- "id_page_assetstab": "AssetsTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L243 | neighbors=[page.tsx]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
