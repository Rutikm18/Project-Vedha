# Node Description Batch 17 of 104

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

- "detection_engine_correlate_rationale_1": "correlate.py — dedup, authoritative-suppression, and cross-fact composite correl" | kind=entity | source=manager/detection_engine/correlate.py:L1 | neighbors=[correlate.py, CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_115": "The CPE 'product' field — used as the join key on BOTH sides (a     Finding's cp" | kind=entity | source=manager/detection_engine/correlate.py:L115 | neighbors=[_product_from_cpe(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_135": "SMBv1 enabled + (credentialed hotfix list present AND missing every     known MS" | kind=entity | source=manager/detection_engine/correlate.py:L135 | neighbors=[correlate_smb_patch(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_36": "Collapse by finding_id (deterministic: same asset+cve+cpe always     hashes the" | kind=entity | source=manager/detection_engine/correlate.py:L36 | neighbors=[dedup_findings(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_correlate_rationale_63": "Suppress a suspected/potential (inferred-source) finding when the     SAME host" | kind=entity | source=manager/detection_engine/correlate.py:L63 | neighbors=[suppress_negated(), CPECandidate, Asset, Finding, FindingState, SourceConfidence] | lang=en
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, EpssDB, KevDB, load_epss(), load_kev(), enrichment_db.py — load the pinned KEV/…] | lang=en
- "detection_engine_matcher_rationale_1": "matcher.py — does this CPE candidate's version fall inside a vulnerable range, p" | kind=entity | source=manager/detection_engine/matcher.py:L1 | neighbors=[CPECandidate, matcher.py, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_34": "dpkg_compare, but None instead of a misleading answer when one side     has an e" | kind=entity | source=manager/detection_engine/matcher.py:L34 | neighbors=[CPECandidate, _safe_compare(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_45": "Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A" | kind=entity | source=manager/detection_engine/matcher.py:L45 | neighbors=[CPECandidate, _version_in_ranges(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_81": "All Findings this single CPE candidate produces against the snapshot.     Empty" | kind=entity | source=manager/detection_engine/matcher.py:L81 | neighbors=[CPECandidate, match_candidate(), Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_version_compare_compare_part": "_compare_part()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L85 | neighbors=[version_compare.py, _compare_non_digit(), _split_segments(), _dpkg_compare_pure_python(), upstream_version or debian_revision com…, semver_compare()] | lang=en
- "discovery_finding_translator_rationale_1": "Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[finding_translator.py, Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_finding_translator_rationale_54": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[_resolve_asset(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_78": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L78 | neighbors=[_find_open_duplicate(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_98": "Convert a probe's self-assessed `findings` list into persisted Finding rows." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L98 | neighbors=[create_findings_from_probe_result(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_xml_parser_parsedport": "ParsedPort" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L13 | neighbors=[DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…, xml_parser.py, ._parse_port()] | lang=en
- "e2e_mock_manager_start": "start()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L234 | neighbors=[mock_manager.py, Start the HTTPS server in a thread. Ret…, _make_handler(), _QuietServer, _self_signed(), spki_pin()] | lang=en
- "engine_tool_runners_hasbinary": "hasBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L61 | neighbors=[tool-runners.ts, resolveBinPath(), runFfuf(), runHttpx(), runNaabu(), runWhatweb()] | lang=en
- "engine_tool_runners_runffuf": "runFfuf()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L829 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runhostdiscovery": "runHostDiscovery()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L536 | neighbors=[tools.ts, scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runwhatweb": "runWhatweb()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L757 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "graph_analyzer_pathanalyzer_movement_graph": ".movement_graph()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L87 | neighbors=[PathAnalyzer, .find_blast_radius(), .find_paths_to_target(), ._exploit_info(), ._source_assets(), Build (and cache) the Asset→Asset movem…] | lang=en
- "graph_demo": "demo.py" | kind=code-symbol | source=manager/backend/app/graph/demo.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, DemoAsset, DemoFinding, DemoService, generate_demo_dataset(), Demo dataset generator for the attack-p…] | lang=en
- "install_install": "install.go" | kind=code-symbol | source=probe-go/install/install.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, copyFile(), Install(), installLaunchd(), installSystemd(), Uninstall()] | lang=en
- "lib_agents_store_readfieldagents": "readFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L343 | neighbors=[agents-store.ts, getAgent(), getAllAgents(), ensureDataDir(), registerAgent(), updateAgentLastSeen()] | lang=en
- "lib_ai_engine_aireportstore": "aiReportStore" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L343 | neighbors=[route.ts, route.ts, route.ts, route.ts, ai-engine.ts, route.ts] | lang=en
- "lib_cases_store_readcases": "readCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L213 | neighbors=[cases-store.ts, addComment(), createCase(), getCaseById(), ensureDataDir(), updateCase()] | lang=en
- "lib_clients_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L66 | neighbors=[clients-store.ts, createClient(), read(), updateClient(), updateClientSettings(), ensureDir()] | lang=en
- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()] | lang=en
- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()] | lang=en
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()] | lang=en
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L349 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts] | lang=en
- "me_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/me/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, backend.ts, backend(), with-backend.ts, withBackend(), GET] | lang=en
- "native_tls_info": "tls-info.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/tls-info.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, tool-runners.ts, nativeTlsInfo(), TlsInfoResult, WEAK_PROTOCOLS, WEAK_SIGNATURES] | lang=en
- "openvas_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/openvas/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), openvas-client.ts, startOpenVASScan(), POST()] | lang=en
- "probes_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L1 | neighbors=[0557559 scanner: real use-case library,…, backend.ts, backend(), with-backend.ts, withBackend(), GET] | lang=en
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, Engagement, Finding, ScanJob, recent_activity()] | lang=en
- "routers_agent_advisor": "agent_advisor.py" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, dependencies.py, list_recommendations(), _rec_dict(), run_advisor(), agent_advisor.py — API for the agentic …] | lang=en
- "routers_analytics_rationale_1": "Dashboard exposure analytics endpoint.  Serves protocol-risk + zone-health aggre" | kind=entity | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[Asset, Engagement, FindingStatus, Finding, Service, analytics.py] | lang=en
- "routers_detection_runs": "detection_runs.py" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, dependencies.py, latest_run_delta(), list_detection_runs(), _run_dict(), detection_runs.py — temporal detection …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-016.json

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
