# Node Description Batch 72 of 104

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_siem_build_siem_engine": "build_siem_engine()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L249 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_1": "SIEM query engines — abstract interface + Splunk / Microsoft Sentinel / Elastic" | kind=entity | source=manager/backend/app/detection/siem.py:L1 | neighbors=[siem.py] | lang=en
- "detection_siem_rationale_135": "Microsoft Sentinel via the Azure Monitor Logs query REST API with KQL.     confi" | kind=entity | source=manager/backend/app/detection/siem.py:L135 | neighbors=[SentinelSIEM] | lang=en
- "detection_siem_rationale_185": "Elasticsearch via the _search API (KQL/EQL-style bool query).     config: {base_" | kind=entity | source=manager/backend/app/detection/siem.py:L185 | neighbors=[ElasticSIEM] | lang=en
- "detection_siem_rationale_51": "Abstract SIEM connector." | kind=entity | source=manager/backend/app/detection/siem.py:L51 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_rationale_82": "Splunk via the REST search endpoint (``/services/search/jobs/export``) with an" | kind=entity | source=manager/backend/app/detection/siem.py:L82 | neighbors=[SplunkSIEM] | lang=en
- "detection_siem_siemqueryengine_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L55 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_siem_siemqueryengine_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L60 | neighbors=[SIEMQueryEngine] | lang=en
- "detection_sigma_rationale_1": "SigmaRuleGenerator — produces a Sigma detection rule (YAML) for a MITRE techniqu" | kind=entity | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[sigma.py] | lang=pt
- "detection_sigma_rationale_114": "Return a Sigma rule (YAML string) for the technique, customised with the" | kind=entity | source=manager/backend/app/detection/sigma.py:L114 | neighbors=[.generate_sigma_for_technique()] | lang=en
- "discovery_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/discovery/__init__.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …] | lang=en
- "discovery_rate_limiter_ratelimiter_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L30 | neighbors=[RateLimiter] | lang=en
- "discovery_rate_limiter_rationale_1": "RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[rate_limiter.py] | lang=en
- "discovery_rate_limiter_rationale_44": "True if current time is inside the allowed scan window." | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L44 | neighbors=[.is_within_window()] | lang=en
- "discovery_rate_limiter_rationale_61": "Blocks until a token is available for the given target IP.         Raises Runtim" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L61 | neighbors=[.acquire()] | lang=en
- "discovery_service_id_rationale_1": "ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT" | kind=entity | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[service_id.py] | lang=en
- "discovery_worker_discoveryjobpayload_post_init": ".__post_init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L52 | neighbors=[DiscoveryJobPayload] | lang=en
- "discovery_worker_discoveryworker_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L63 | neighbors=[DiscoveryWorker] | lang=en
- "discovery_xml_parser_parsedhost_open_ports": ".open_ports()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L37 | neighbors=[ParsedHost] | lang=en
- "discovery_xml_parser_rationale_1": "Nmap XML output parser. Converts -oX output into structured ParsedHost / ParsedP" | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[xml_parser.py] | lang=en
- "discovery_xml_parser_rationale_42": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L42 | neighbors=[NmapXMLParser] | lang=en
- "draft_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L5 | neighbors=[route.ts] | lang=en
- "e2e_interop_verify_rationale_1": "Verify the Python probe can open what the TypeScript manager sealed (T14 interop" | kind=entity | source=manager/frontend/tests/e2e/interop_verify.py:L1 | neighbors=[interop_verify.py] | lang=en
- "e2e_mock_manager_managerstate_ingest": ".ingest()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L110 | neighbors=[ManagerState] | lang=en
- "e2e_mock_manager_managerstate_init": ".__init__()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L45 | neighbors=[ManagerState] | lang=en
- "e2e_mock_manager_managerstate_queue_scan": ".queue_scan()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L71 | neighbors=[ManagerState] | lang=en
- "e2e_mock_manager_quietserver_handle_error": ".handle_error()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L224 | neighbors=[_QuietServer] | lang=en
- "e2e_mock_manager_rationale_1": "Reference mock manager for end-to-end probe testing.  Implements the PROBE_PROTO" | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L1 | neighbors=[mock_manager.py] | lang=en
- "e2e_mock_manager_rationale_235": "Start the HTTPS server in a thread. Returns (httpd, base_url, pin_b64)." | kind=entity | source=manager/frontend/tests/e2e/mock_manager.py:L235 | neighbors=[start()] | lang=en
- "e2e_run_rationale_1": "End-to-end probe test: real probe process ↔ reference mock manager over HTTPS." | kind=entity | source=manager/frontend/tests/e2e/run.py:L1 | neighbors=[run.py] | lang=en
- "e2e_run_rationale_30": "Deterministic stand-ins emitting realistic output for 127.0.0.1." | kind=entity | source=manager/frontend/tests/e2e/run.py:L30 | neighbors=[make_fake_tools()] | lang=en
- "engagements_page_empty_form": "EMPTY_FORM" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L40 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L17 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementspage": "EngagementsPage()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L80 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementsresponse": "EngagementsResponse" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "engagements_page_formstate": "FormState" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L33 | neighbors=[page.tsx] | lang=en
- "engagements_page_rowskeleton": "RowSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L64 | neighbors=[page.tsx] | lang=en
- "engagements_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L56 | neighbors=[page.tsx] | lang=en
- "engagements_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L48 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-071.json

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
