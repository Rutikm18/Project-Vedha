# Node Description Batch 20 of 119

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

- "detection_engine_matcher": "matcher.py" | kind=code-symbol | source=manager/detection_engine/matcher.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, match_candidate(), _safe_compare(), _version_in_ranges(), matcher.py — does this CPE candidate's …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "detection_engine_matcher_rationale_1": "matcher.py — does this CPE candidate's version fall inside a vulnerable range, p" | kind=entity | source=manager/detection_engine/matcher.py:L1 | neighbors=[CPECandidate, matcher.py, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_34": "dpkg_compare, but None instead of a misleading answer when one side     has an e" | kind=entity | source=manager/detection_engine/matcher.py:L34 | neighbors=[CPECandidate, _safe_compare(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_45": "Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A" | kind=entity | source=manager/detection_engine/matcher.py:L45 | neighbors=[CPECandidate, _version_in_ranges(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_81": "All Findings this single CPE candidate produces against the snapshot.     Empty" | kind=entity | source=manager/detection_engine/matcher.py:L81 | neighbors=[CPECandidate, match_candidate(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L85 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "discovery_finding_translator_rationale_1": "Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[finding_translator.py, Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_finding_translator_rationale_54": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[_resolve_asset(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_78": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L78 | neighbors=[_find_open_duplicate(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_98": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_worker": "worker.py" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, database.py, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "discovery_xml_parser": "xml_parser.py" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, NmapXMLParser, ParsedHost, ParsedPort, Nmap XML output parser. Converts -oX ou…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "discovery_xml_parser_parsedport": "ParsedPort" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L13 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, xml_parser.py, ._parse_port()] | lang=en
- "engine_tool_runners_hasbinary": "hasBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L63 | neighbors=[tool-runners.ts, resolveBinPath(), runFfuf(), runHttpx(), runNaabu(), runWhatweb()] | lang=en
- "engine_tool_runners_runffuf": "runFfuf()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L881 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runhostdiscovery": "runHostDiscovery()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L564 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts(), tools.ts] | lang=en
- "engine_tool_runners_runwhatweb": "runWhatweb()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L798 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "exploit_orchestrator": "orchestrator.py" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, ExploitOrchestrator, ExploitOrchestrator — safe, scoped, aud…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "graph_analyzer": "analyzer.py" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, PathAnalyzer, _priority(), _safe_float(), PathAnalyzer — attack-path discovery, s…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "graph_analyzer_pathanalyzer_movement_graph": ".movement_graph()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L87 | neighbors=[PathAnalyzer, .find_blast_radius(), .find_paths_to_target(), ._exploit_info(), ._source_assets(), Build (and cache) the Asset→Asset movem…] | lang=en
- "import_facts_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, BASE, POST(), bearerFrom(), 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "lib_agents_store_readfieldagents": "readFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L343 | neighbors=[agents-store.ts, getAgent(), getAllAgents(), ensureDataDir(), registerAgent(), updateAgentLastSeen()] | lang=en
- "lib_ai_engine_aireportstore": "aiReportStore" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L342 | neighbors=[ai-engine.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "lib_cases_store_readcases": "readCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L213 | neighbors=[cases-store.ts, addComment(), createCase(), getCaseById(), ensureDataDir(), updateCase()] | lang=en
- "lib_clients_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L66 | neighbors=[clients-store.ts, createClient(), read(), updateClient(), updateClientSettings(), ensureDir()] | lang=en
- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()] | lang=en
- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()] | lang=en
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()] | lang=en
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L329 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts] | lang=en
- "lib_httpx_parser_parsehttpxjsonline": "parseHttpxJsonLine()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L41 | neighbors=[httpx-parser.ts, .decode(), isOptionalNumber(), isOptionalString(), normalizePort(), parsers.test.ts] | lang=en
- "lib_netexec_parser": "netexec-parser.ts" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), scanner-adapters.test.ts] | lang=en
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, broadcastToScan(), Callback, scanListeners, subscribeScan(), 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "lib_scanner_request_validation_validateopenvasscanrequest": "validateOpenVASScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L112 | neighbors=[scanner-request-validation.ts, isRecord(), validateHost(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts] | lang=en
- "lib_testssl_parser_parsetestssljson": "parseTestsslJson()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L44 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslOutput(), parsers.test.ts, tool-runners.ts, mapSeverity()] | lang=en
- "lib_whatweb_parser": "whatweb-parser.ts" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, parseWhatWebOutput(), WhatWebParseResult, WhatWebResult, scanner-adapters.test.ts] | lang=en
- "login_page": "page.tsx" | kind=code-symbol | source=manager/frontend/app/login/page.tsx:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, LoginForm(), LoginPage(), 2885afa Add comprehensive probe testing…, fetcher.ts, storeToken()] | lang=en
- "pipeline_pipeline_test": "pipeline_test.go" | kind=code-symbol | source=probe-go/pipeline/pipeline_test.go:L1 | neighbors=[b4b12a9 Rename project and update files, TestOTPlansNeverReachActiveGates(), TestResolveRequestedCIDRAppliesExclusio…, TestResolveRequestedHostsDoesNotExpandA…, TestResolveRequestedHostsFailsClosed(), TestWebTLSPlanEnablesOnlyWebAndTLSBranc…] | lang=en
- "routers_activity": "activity.py" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, ActivityItem, recent_activity(), Recent activity feed.  A tenant-wide, r…, 2885afa Add comprehensive probe testing…] | lang=en
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, Engagement, Finding, ScanJob, recent_activity()] | lang=en
- "routers_agents_enqueue_agent_job": "enqueue_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L753 | neighbors=[agents.py, _agent_can_execute_job(), _encrypt_scope_for_agent(), _job_params_contain_secret(), _job_reachability_scope(), _resolve_scan_type()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
