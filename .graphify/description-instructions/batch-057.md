# Node Description Batch 58 of 131

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

- "detection_siem_splunksiem_build_spl": ".build_spl()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L88 | neighbors=[SplunkSIEM, .query_alerts()]
- "detection_sigma_sigmarulegenerator_customise_detection": "._customise_detection()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L153 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_sigmarulegenerator_lookup_template": "._lookup_template()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L144 | neighbors=[SigmaRuleGenerator, .generate_sigma_for_technique()]
- "detection_sigma_stable_rule_id": "_stable_rule_id()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L166 | neighbors=[sigma.py, .generate_sigma_for_technique()]
- "discovery_finding_translator_map_severity": "_map_severity()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L46 | neighbors=[finding_translator.py, create_findings_from_probe_result()]
- "discovery_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/discovery/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "discovery_rate_limiter_ratelimiter_consume_token": "._consume_token()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L85 | neighbors=[RateLimiter, .acquire()]
- "discovery_rate_limiter_ratelimiter_resolve_cidr": "._resolve_cidr()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L75 | neighbors=[RateLimiter, .acquire()]
- "discovery_service_id_serviceidentifier_identify": ".identify()" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L73 | neighbors=[ServiceIdentifier, ServiceFingerprint]
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
- "exploit_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/exploit/__init__.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "exploit_msf_client_metasploitrpcclient_disconnect": ".disconnect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L53 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_msf_client_metasploitrpcclient_module_info": ".module_info()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L126 | neighbors=[MetasploitRPCClient, ._call()]
- "exploit_nuclei_exploit_nucleiexploitrunner_extract_evidence": "._extract_evidence()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L183 | neighbors=[NucleiExploitRunner, ._parse_poc_output()]
- "exploit_nuclei_exploit_rationale_1": "NucleiExploitRunner — CVE PoC validation using Nuclei templates.  Enforces templ" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L1 | neighbors=[nuclei_exploit.py, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_121": "Run Nuclei CVE PoC template against target.         Returns {vulnerable, evidenc" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L121 | neighbors=[.run_cve_poc(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_161": "Parse nuclei JSONL output for a single CVE PoC result." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L161 | neighbors=[._parse_poc_output(), SafetyViolationError]
- "exploit_nuclei_exploit_rationale_49": "Run Nuclei CVE PoC templates against a single target.     Every template is safe" | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L49 | neighbors=[NucleiExploitRunner, SafetyViolationError]
- "exploit_nuclei_exploit_rationale_61": "Parse template YAML and validate it contains no write/delete/DoS actions." | kind=entity | source=manager/backend/app/exploit/nuclei_exploit.py:L61 | neighbors=[.safe_template_check(), SafetyViolationError]
- "exploit_orchestrator_exploitorchestrator_audit": "._audit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L319 | neighbors=[ExploitOrchestrator, .execute()]
- "exploit_safety_requires_approval": "requires_approval()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L239 | neighbors=[safety.py, True if this target requires human mana…]
- "findings_page_findingspage": "FindingsPage()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L920 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_fixfirststrip": "FixFirstStrip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L810 | neighbors=[page.tsx, useCountUp()]
- "findings_page_isurgent": "isUrgent()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L765 | neighbors=[page.tsx, getSlaColor()]
- "findings_page_riskbadge": "RiskBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L151 | neighbors=[page.tsx, riskScoreColor()]
- "findings_page_urgencyreasons": "urgencyReasons()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L771 | neighbors=[page.tsx, getSlaColor()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-057.json

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
