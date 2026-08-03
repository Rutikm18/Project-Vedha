# Node Description Batch 87 of 131

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

- "detection_engine_vuln_db_rationale_1": "vuln_db.py — offline, pinned vulnerability data store.  NO LIVE API CALLS HAPPEN" | kind=entity | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[vuln_db.py] | lang=en
- "detection_engine_vuln_db_rationale_110": "The CVSS v3 vector string OSV embedded for this CVE, if any.         Uses a pre-" | kind=entity | source=manager/detection_engine/vuln_db.py:L110 | neighbors=[.get_cvss_vector()] | lang=en
- "detection_engine_vuln_db_rationale_44": "Derives the synced product list from cpe_normalizer.py's tables —     the single" | kind=entity | source=manager/detection_engine/vuln_db.py:L44 | neighbors=[_default_products()] | lang=en
- "detection_engine_vuln_db_rationale_60": "Stable hash of the snapshot's actual vulnerability content — recorded     in eve" | kind=entity | source=manager/detection_engine/vuln_db.py:L60 | neighbors=[_content_hash()] | lang=en
- "detection_engine_vuln_db_rationale_79": "In-memory index over a loaded snapshot: product -> OSV vuln records.     Constru" | kind=entity | source=manager/detection_engine/vuln_db.py:L79 | neighbors=[VulnDB] | lang=pt
- "detection_engine_vuln_db_rationale_99": "Raw OSV vulnerability records for this product, or [] if the         snapshot do" | kind=entity | source=manager/detection_engine/vuln_db.py:L99 | neighbors=[.lookup()] | lang=en
- "detection_engine_vuln_db_vulndb_covers": ".covers()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L106 | neighbors=[VulnDB] | lang=en
- "detection_engine_vuln_db_vulndb_known_products": ".known_products()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L115 | neighbors=[VulnDB] | lang=en
- "detection_logger_attacklogger_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L24 | neighbors=[AttackLogger] | lang=en
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
- "discovery_rate_limiter_ratelimiter_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L30 | neighbors=[RateLimiter] | lang=en
- "discovery_rate_limiter_rationale_1": "RateLimiter — enforces PPS limits per CIDR and business-hour windows from the en" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[rate_limiter.py] | lang=en
- "discovery_rate_limiter_rationale_44": "True if current time is inside the allowed scan window." | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L44 | neighbors=[.is_within_window()] | lang=en
- "discovery_rate_limiter_rationale_61": "Blocks until a token is available for the given target IP.         Raises Runtim" | kind=entity | source=manager/backend/app/discovery/rate_limiter.py:L61 | neighbors=[.acquire()] | lang=en
- "discovery_service_id_rationale_1": "ServiceIdentifier — banner + port → structured service fingerprint. Handles: HTT" | kind=entity | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[service_id.py] | lang=en
- "discovery_worker_discoveryjobpayload_post_init": ".__post_init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L50 | neighbors=[DiscoveryJobPayload] | lang=en
- "discovery_worker_discoveryworker_init": ".__init__()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L61 | neighbors=[DiscoveryWorker] | lang=en
- "discovery_xml_parser_parsedhost_open_ports": ".open_ports()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L36 | neighbors=[ParsedHost] | lang=en
- "discovery_xml_parser_rationale_1": "Nmap XML output parser. Converts -oX output into structured ParsedHost / ParsedP" | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[xml_parser.py] | lang=en
- "discovery_xml_parser_rationale_41": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L41 | neighbors=[NmapXMLParser] | lang=en
- "discovery_xml_parser_rationale_42": "Parse nmap -oX XML into a list of ParsedHost objects." | kind=entity | source=manager/backend/app/discovery/xml_parser.py:L42 | neighbors=[NmapXMLParser] | lang=en
- "draft_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L4 | neighbors=[route.ts] | lang=en
- "engagements_page_empty_form": "EMPTY_FORM" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L41 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagement": "Engagement" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L17 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementsresponse": "EngagementsResponse" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "engagements_page_engagementstatus": "EngagementStatus" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "engagements_page_formstate": "FormState" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L33 | neighbors=[page.tsx] | lang=en
- "engagements_page_rowskeleton": "RowSkeleton()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L71 | neighbors=[page.tsx] | lang=en
- "engagements_page_sevcolor": "sevColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L63 | neighbors=[page.tsx] | lang=en
- "engagements_page_statuscolor": "statusColor()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L55 | neighbors=[page.tsx] | lang=en
- "engagements_page_steps": "STEPS" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L84 | neighbors=[page.tsx] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-086.json

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
