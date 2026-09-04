# Node Description Batch 44 of 330

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

- "detection_engine_matcher_rationale_45": "Returns (matched, matched_interval_desc) — the latter for evidence_reason.     A" | kind=entity | source=manager/detection_engine/matcher.py:L45 | neighbors=[_version_in_ranges(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_matcher_rationale_81": "All Findings this single CPE candidate produces against the snapshot.     Empty" | kind=entity | source=manager/detection_engine/matcher.py:L81 | neighbors=[match_candidate(), CPECandidate, Finding, FindingState, SourceConfidence, VulnDB] | lang=en
- "detection_engine_posture_rules_evaluate_rule": "evaluate_rule()" | kind=code-symbol | source=manager/detection_engine/posture_rules.py:L780 | neighbors=[posture_rules.py, detect_posture_traced(), _fact_indicates_no_service(), get_path(), TraceRow, Evaluate ONE rule against ONE fact and …] | lang=en
- "detection_engine_update_snapshot_main": "main()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L233 | neighbors=[update_snapshot.py, sync_epss_full(), sync_kev_snapshot(), sync_snapshot(), _all_known_cve_ids(), sync_epss_snapshot()] | lang=en
- "detection_engine_update_snapshot_ssl_context": "_ssl_context()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L37 | neighbors=[update_snapshot.py, _query_osv(), Some macOS python.org installs ship exp…, sync_epss_full(), sync_epss_snapshot(), sync_kev_snapshot()] | lang=en
- "detection_engine_version_compare_verify_pure_python_matches_dpkg": "verify_pure_python_matches_dpkg()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L243 | neighbors=[version_compare.py, Confirm pure-Python agrees with the rea…, _dpkg_compare_pure_python(), _dpkg_compare_via_binary(), _load_validation_markers(), _save_validation_marker()] | lang=en
- "detection_engine_vuln_db_content_hash": "_content_hash()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L66 | neighbors=[vuln_db.py, Stable hash of the snapshot's actual vu…, _read_snapshot(), Stable hash of the snapshot's actual vu…, load_snapshot(), Stable hash of the snapshot's actual vu…] | lang=en
- "detection_engine_vuln_db_load_snapshot": "load_snapshot()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L208 | neighbors=[vuln_db.py, _merge_companion(), _read_snapshot(), _content_hash(), SnapshotMeta, VulnDB] | lang=en
- "detection_engine_vuln_db_merge_companion": "_merge_companion()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L184 | neighbors=[vuln_db.py, load_snapshot(), _read_snapshot(), SnapshotMeta, VulnDB, Merge an NVD/CPE companion snapshot int…] | lang=en
- "detection_prioritization_prioritize_engagement_findings": "prioritize_engagement_findings()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L145 | neighbors=[prioritization.py, composite_risk_score(), _load_offline_kev_epss(), _strongest_exposure(), (Re)compute risk_score for every still-…, (Re)compute risk_score for every still-…] | lang=en
- "detection_resolution_decide_resolution": "decide_resolution()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L72 | neighbors=[resolution.py, resolution_threshold(), ResolutionOutcome, evaluate_resolutions(), Pure heart of auto-resolution. Given wh…, Pure heart of auto-resolution. Given wh…] | lang=en
- "detection_vantage_fusion_fuse_exposure_results": "fuse_exposure_results()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L80 | neighbors=[vantage_fusion.py, _collect(), _is_external(), _verdict(), fused_service_exposure(), Fuse several probes' exposure_matrix re…] | lang=en
- "discovery_finding_translator_find_open_duplicate": "_find_open_duplicate()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L132 | neighbors=[finding_translator.py, create_findings_from_probe_result(), create_scan_health_finding(), A still-relevant Finding with the same …, A still-relevant Finding with the same …, A still-relevant Finding with the same …] | lang=en
- "discovery_finding_translator_rationale_1": "Convert a probe's self-assessed `findings` into persisted Finding rows.  WHY THI" | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[finding_translator.py, Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=pt
- "discovery_finding_translator_rationale_54": "Find the Asset for a probe-reported target IP, creating a minimal one if needed." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L54 | neighbors=[_resolve_asset(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_finding_translator_rationale_78": "A still-relevant Finding with the same (engagement, asset, title), if any." | kind=entity | source=manager/backend/app/discovery/finding_translator.py:L78 | neighbors=[_find_open_duplicate(), Asset, AssetType, FindingSeverity, FindingStatus, Finding] | lang=en
- "discovery_service_id": "service_id.py" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ServiceFingerprint, ServiceIdentifier, ServiceIdentifier — banner + port → str…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "discovery_service_vuln_create_service_vuln_findings": "create_service_vuln_findings()" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L140 | neighbors=[service_vuln.py, _cleartext_rule(), _http_rules(), _new_finding(), _ssh_rules(), Scan the result's `facts` for weak/outd…] | lang=en
- "engine_tool_runners_hasbinary": "hasBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L63 | neighbors=[tool-runners.ts, resolveBinPath(), runFfuf(), runHttpx(), runNaabu(), runWhatweb()] | lang=en
- "engine_tool_runners_runffuf": "runFfuf()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L881 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runhostdiscovery": "runHostDiscovery()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L564 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts(), tools.ts] | lang=en
- "engine_tool_runners_runwhatweb": "runWhatweb()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L798 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), hasBinary(), spawnOpts()] | lang=en
- "graph_analyzer": "analyzer.py" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, PathAnalyzer, _priority(), _safe_float(), PathAnalyzer — attack-path discovery, s…, 298a9d4 trim frontend to 7 core pages; …] | lang=en
- "graph_analyzer_pathanalyzer_movement_graph": ".movement_graph()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L87 | neighbors=[PathAnalyzer, .find_blast_radius(), .find_paths_to_target(), ._exploit_info(), ._source_assets(), Build (and cache) the Asset→Asset movem…] | lang=en
- "import_facts_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/import-facts/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, BASE, POST(), bearerFrom(), 298a9d4 trim frontend to 7 core pages; …, backend.ts] | lang=en
- "integrations_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/route.ts:L1 | neighbors=[00c6648 feat(settings): editable email/…, GET, backend.ts, backend(), with-backend.ts, withBackend()] | lang=en
- "lib_agents_store_readfieldagents": "readFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L343 | neighbors=[agents-store.ts, getAgent(), getAllAgents(), ensureDataDir(), registerAgent(), updateAgentLastSeen()] | lang=en
- "lib_ai_engine_aireportstore": "aiReportStore" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L342 | neighbors=[ai-engine.ts, route.ts, route.ts, route.ts, route.ts, route.ts] | lang=en
- "lib_assistant_factcardvm": "FactCardVM" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L17 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, assistant.ts, security-context.ts] | lang=en
- "lib_assistant_tofactcard": "toFactCard()" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L127 | neighbors=[assistant.ts, isExploited(), lifecycleOf(), plainWhyItMatters(), security-context.ts, assistant.test.ts] | lang=en
- "lib_campaign_store_savecampaign": "saveCampaign()" | kind=code-symbol | source=manager/frontend/lib/campaign-store.ts:L140 | neighbors=[route.ts, campaign-store.ts, ensureDir(), fileFor(), validateSnapshot(), campaign-store.test.ts] | lang=en
- "lib_cases_store_readcases": "readCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L213 | neighbors=[cases-store.ts, addComment(), createCase(), getCaseById(), ensureDataDir(), updateCase()] | lang=en
- "lib_clients_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L66 | neighbors=[clients-store.ts, createClient(), read(), updateClient(), updateClientSettings(), ensureDir()] | lang=en
- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()] | lang=en
- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()] | lang=en
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()] | lang=en
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L329 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts] | lang=en
- "lib_httpx_parser_parsehttpxjsonline": "parseHttpxJsonLine()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L41 | neighbors=[httpx-parser.ts, .decode(), isOptionalNumber(), isOptionalString(), normalizePort(), parsers.test.ts] | lang=en
- "lib_netexec_parser": "netexec-parser.ts" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), scanner-adapters.test.ts] | lang=en
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, broadcastToScan(), Callback, scanListeners, subscribeScan(), 298a9d4 trim frontend to 7 core pages; …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-043.json

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
