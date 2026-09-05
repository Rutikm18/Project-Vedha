# Node Description Batch 130 of 336

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

- "detection_logger_rationale_1": "AttackLogger — records every attack action to the ``attack_timeline`` table.  Al" | kind=entity | source=manager/backend/app/detection/logger.py:L1 | neighbors=[logger.py, AttackTimeline]
- "detection_logger_rationale_40": "Persist a single attack action. Returns the AttackTimeline row.          ``times" | kind=entity | source=manager/backend/app/detection/logger.py:L40 | neighbors=[.log_action(), AttackTimeline]
- "detection_prioritization_posture_risk_on_manager_scale": "_posture_risk_on_manager_scale()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L57 | neighbors=[prioritization.py, Score a posture finding with the Manage…]
- "detection_resolution_resolutionoutcome": "ResolutionOutcome" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L75 | neighbors=[resolution.py, decide_resolution()]
- "detection_siem_elasticsiem_build_query": ".build_query()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L191 | neighbors=[ElasticSIEM, .query_alerts()]
- "detection_siem_sentinelsiem_build_kql": ".build_kql()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L141 | neighbors=[SentinelSIEM, .query_alerts()]
- "detection_siem_splunksiem_build_spl": ".build_spl()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L88 | neighbors=[SplunkSIEM, .query_alerts()]
- "detection_sigma_sigmarulegenerator_customise_detection": "._customise_detection()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L153 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_sigmarulegenerator_lookup_template": "._lookup_template()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L144 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_stable_rule_id": "_stable_rule_id()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L166 | neighbors=[sigma.py, .generate_sigma_for_technique()]
- "detection_verification_int_confidence": "_int_confidence()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L37 | neighbors=[verification.py, compute_verdict()]
- "dev_hint_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/dev-hint/route.ts:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, GET()]
- "discovery_exposure_escalate_for_exposure": "escalate_for_exposure()" | kind=code-symbol | source=manager/backend/app/discovery/exposure.py:L66 | neighbors=[exposure.py, Bump a finding one severity rung when i…]
- "discovery_exposure_service_exposure": "service_exposure()" | kind=code-symbol | source=manager/backend/app/discovery/exposure.py:L37 | neighbors=[exposure.py, (ip, proto, port) → exposure verdict, f…]
- "discovery_finding_translator_map_severity": "_map_severity()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L47 | neighbors=[finding_translator.py, create_findings_from_probe_result()]
- "discovery_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/discovery/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "discovery_rate_limiter_ratelimiter_consume_token": "._consume_token()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L85 | neighbors=[RateLimiter, .acquire()]
- "discovery_rate_limiter_ratelimiter_resolve_cidr": "._resolve_cidr()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L75 | neighbors=[RateLimiter, .acquire()]
- "discovery_scan_health_scan_health_summary": "scan_health_summary()" | kind=code-symbol | source=manager/backend/app/discovery/scan_health.py:L17 | neighbors=[scan_health.py, Aggregate result['scan_metrics'] into a…]
- "discovery_service_id_serviceidentifier_identify": ".identify()" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L73 | neighbors=[ServiceIdentifier, ServiceFingerprint]
- "discovery_service_vuln_cleartext_rule": "_cleartext_rule()" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L126 | neighbors=[service_vuln.py, create_service_vuln_findings()]
- "discovery_service_vuln_new_finding": "_new_finding()" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L45 | neighbors=[service_vuln.py, create_service_vuln_findings()]
- "discovery_worker_discoveryworker_grab_one": "._grab_one()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L159 | neighbors=[DiscoveryWorker, ._banner_grab_all()]
- "discovery_worker_discoveryworker_run_nmap": "._run_nmap()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L117 | neighbors=[DiscoveryWorker, .run()]
- "discovery_worker_discoveryworker_save_assets": "._save_assets()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L192 | neighbors=[DiscoveryWorker, .run()]
- "discovery_worker_discoveryworker_set_status": "._set_status()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L268 | neighbors=[DiscoveryWorker, .run()]
- "discovery_xml_parser_nmapxmlparser_parse": ".parse()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L43 | neighbors=[NmapXMLParser, ._parse_host()]
- "engagements_page_hasvaliddaterange": "hasValidDateRange()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L51 | neighbors=[page.tsx, EngagementsPage()]
- "engagements_page_splitentries": "splitEntries()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L48 | neighbors=[page.tsx, EngagementsPage()]
- "engine_scan_modules_modules": "MODULES" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L48 | neighbors=[scan-modules.ts, interactive.ts]
- "engine_scan_modules_modulesbycategory": "modulesByCategory()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L333 | neighbors=[interactive.ts, scan-modules.ts]
- "engine_scan_modules_modulesforports": "modulesForPorts()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L378 | neighbors=[scan-modules.ts, scanner.ts]
- "engine_scan_modules_profilemodules": "profileModules()" | kind=code-symbol | source=manager/frontend/lib/engine/scan-modules.ts:L349 | neighbors=[interactive.ts, scan-modules.ts]
- "engine_scanner_byseveritycount": "bySeverityCount()" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L11 | neighbors=[scanner.ts, runScan()]
- "engine_tool_runners_httpbannergrab": "httpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L311 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_tool_runners_tcpbannergrab": "tcpBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L357 | neighbors=[tool-runners.ts, nativeBannerGrab()]
- "engine_types_evidence": "Evidence" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L77 | neighbors=[types.ts, findings-store.ts]
- "events_route_fail": "fail()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/events/route.ts:L5 | neighbors=[route.ts, GET()]
- "events_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/events/route.ts:L13 | neighbors=[route.ts, fail()]
- "exploit_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/exploit/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-129.json

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
