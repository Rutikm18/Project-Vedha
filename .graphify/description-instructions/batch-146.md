# Node Description Batch 147 of 380

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

- "exploit_nuclei_exploit_rationale_1": "NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[nuclei_exploit.py, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_121": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L121 | neighbors=[.run_cve_poc(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_161": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L161 | neighbors=[._parse_poc_output(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_49": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L49 | neighbors=[NucleiExploitRunner, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_61": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L61 | neighbors=[.safe_template_check(), SafetyViolationError]
- "exploit_orchestrator_exploitorchestrator_audit": "._audit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L319 | neighbors=[ExploitOrchestrator, .execute()]
- "exploit_safety_requires_approval": "requires_approval()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L239 | neighbors=[safety.py, True if this target requires human mana…]
- "findings_page_decisiondrivers": "decisionDrivers()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1959 | neighbors=[page.tsx, urgencyReasons()]
- "findings_page_decodecvssvector": "decodeCvssVector()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L969 | neighbors=[page.tsx, referenceSources()]
- "findings_page_effortcolor": "effortColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L803 | neighbors=[page.tsx, RemediationPlanView()]
- "findings_page_findingsworkspace": "FindingsWorkspace()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L3100 | neighbors=[page.tsx, useNow()]
- "findings_page_fixfirststrip": "FixFirstStrip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1999 | neighbors=[page.tsx, useCountUp()]
- "findings_page_historytimeline": "HistoryTimeline()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1512 | neighbors=[page.tsx, fmtEventDay()]
- "findings_page_isurgent": "isUrgent()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1942 | neighbors=[page.tsx, getSlaColor()]
- "findings_page_pillstyle": "pillStyle()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L807 | neighbors=[page.tsx, RemediationPlanView()]
- "findings_page_remriskcolor": "remRiskColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L801 | neighbors=[page.tsx, RemediationPlanView()]
- "findings_page_riskbadge": "RiskBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L368 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_signalchips": "signalChips()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L458 | neighbors=[page.tsx, FindingDetail()]
- "findings_page_techniqueurl": "techniqueUrl()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L999 | neighbors=[page.tsx, referenceSources()]
- "findings_page_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1972 | neighbors=[page.tsx, FixFirstStrip()]
- "frontend_proxy_ispublic": "isPublic()" | kind=code-symbol | source=manager/frontend/proxy.ts:L14 | neighbors=[proxy.ts, proxy()]
- "frontend_proxy_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/proxy.ts:L19 | neighbors=[proxy.ts, isPublic()]
- "generate_route_mapstatus": "mapStatus()" | kind=code-symbol | source=manager/frontend/app/api/reports/generate/route.ts:L52 | neighbors=[route.ts, toLiveFinding()]
- "generate_route_tolivefinding": "toLiveFinding()" | kind=code-symbol | source=manager/frontend/app/api/reports/generate/route.ts:L61 | neighbors=[route.ts, mapStatus()]
- "graph_analyzer_priority": "_priority()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L285 | neighbors=[analyzer.py, .identify_chokepoints()]
- "graph_analyzer_safe_float": "_safe_float()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L278 | neighbors=[analyzer.py, .score_path()]
- "graph_builder_service_node_id": "service_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L44 | neighbors=[builder.py, .build_asset_graph()]
- "graph_demo_demoservice": "DemoService" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L37 | neighbors=[demo.py, generate_demo_dataset()]
- "graph_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/graph/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L61 | neighbors=[Neo4jClient, Open the driver and verify connectivity…]
- "hooks_usecountup_usecountup": "useCountUp()" | kind=code-symbol | source=manager/frontend/hooks/useCountUp.ts:L3 | neighbors=[DashboardCharts.tsx, useCountUp.ts]
- "hooks_usemousegradient_usemousegradient": "useMouseGradient()" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L3 | neighbors=[useMouseGradient.ts, page.tsx]
- "id_page_displaydate": "displayDate()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L90 | neighbors=[page.tsx, OverviewTab()]
- "id_page_engagementdetailpage": "EngagementDetailPage()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L546 | neighbors=[page.tsx, statusColor()]
- "id_page_engagementworkspace": "EngagementWorkspace()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L443 | neighbors=[page.tsx, page.tsx]
- "id_page_fmtduration": "fmtDuration()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L45 | neighbors=[page.tsx, CampaignDetailPage()]
- "id_page_fmteta": "fmtEta()" | kind=code-symbol | source=manager/frontend/app/campaign/[id]/page.tsx:L38 | neighbors=[page.tsx, CampaignDetailPage()]
- "id_page_overviewtab": "OverviewTab()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L98 | neighbors=[page.tsx, displayDate()]
- "id_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/[id]/page.tsx:L34 | neighbors=[page.tsx, EngagementDetailPage()]
- "id_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/jobs/[id]/route.ts:L7 | neighbors=[route.ts, fail()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-146.json

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
