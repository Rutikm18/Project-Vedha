# Node Description Batch 20 of 104

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

- "detection_engine_cvss": "cvss.py" | kind=code-symbol | source=manager/detection_engine/cvss.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, base_score(), parse_vector(), _roundup(), cvss.py — CVSS v3.1 base score from a v…] | lang=en
- "detection_engine_enrichment_rationale_1": "enrichment.py — join CVSS + KEV + EPSS onto a Finding, compute a priority tier." | kind=entity | source=manager/detection_engine/enrichment.py:L1 | neighbors=[enrichment.py, EpssDB, KevDB, Finding, VulnDB] | lang=pt
- "detection_engine_enrichment_rationale_33": "Mutates and returns `finding` with cvss_score/cvss_vector/epss_score/     kev/pr" | kind=entity | source=manager/detection_engine/enrichment.py:L33 | neighbors=[EpssDB, KevDB, enrich_finding(), Finding, VulnDB] | lang=en
- "detection_engine_enrichment_rationale_53": "Returns (tier, human-readable reason). Order of precedence, per spec:     KEV-li" | kind=entity | source=manager/detection_engine/enrichment.py:L53 | neighbors=[_compute_priority(), EpssDB, KevDB, Finding, VulnDB] | lang=en
- "detection_engine_ingest_quarantinedline": "QuarantinedLine" | kind=code-symbol | source=manager/detection_engine/ingest.py:L35 | neighbors=[ingest.py, ingest_file(), Asset, Fact, SourceConfidence] | lang=en
- "detection_engine_matcher": "matcher.py" | kind=code-symbol | source=manager/detection_engine/matcher.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, match_candidate(), _safe_compare(), _version_in_ranges(), matcher.py — does this CPE candidate's …] | lang=en
- "detection_engine_update_snapshot_main": "main()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L184 | neighbors=[update_snapshot.py, _all_known_cve_ids(), sync_epss_snapshot(), sync_kev_snapshot(), sync_snapshot()] | lang=en
- "detection_engine_update_snapshot_ssl_context": "_ssl_context()" | kind=code-symbol | source=manager/detection_engine/update_snapshot.py:L37 | neighbors=[update_snapshot.py, _query_osv(), Some macOS python.org installs ship exp…, sync_epss_snapshot(), sync_kev_snapshot()] | lang=en
- "detection_sigma": "sigma.py" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, SigmaRuleGenerator, _stable_rule_id(), SigmaRuleGenerator — produces a Sigma d…] | lang=en
- "detection_sigma_sigmarulegenerator_generate_sigma_for_technique": ".generate_sigma_for_technique()" | kind=code-symbol | source=manager/backend/app/detection/sigma.py:L109 | neighbors=[Return a Sigma rule (YAML string) for t…, SigmaRuleGenerator, ._customise_detection(), ._lookup_template(), _stable_rule_id()] | lang=en
- "discovery_finding_translator_create_findings_from_probe_result": "create_findings_from_probe_result()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L95 | neighbors=[finding_translator.py, _find_open_duplicate(), _map_severity(), _resolve_asset(), Convert a probe's self-assessed `findin…] | lang=en
- "discovery_rate_limiter_ratelimiter_acquire": ".acquire()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L60 | neighbors=[RateLimiter, ._consume_token(), .is_within_window(), ._resolve_cidr(), Blocks until a token is available for t…] | lang=en
- "discovery_worker": "worker.py" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, database.py, DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …] | lang=en
- "discovery_worker_discoveryworker_run": ".run()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L70 | neighbors=[DiscoveryWorker, ._banner_grab_all(), ._run_nmap(), ._save_assets(), ._set_status()] | lang=en
- "discovery_xml_parser": "xml_parser.py" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, NmapXMLParser, ParsedHost, ParsedPort, Nmap XML output parser. Converts -oX ou…] | lang=en
- "e2e_mock_manager_b64e": "b64e()" | kind=code-symbol | source=manager/frontend/tests/e2e/mock_manager.py:L40 | neighbors=[mock_manager.py, .mgr_box_pub_b64(), .mgr_sig_pub_b64(), ._seal_plan(), spki_pin()] | lang=en
- "e2e_run_main": "main()" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L103 | neighbors=[run.py, make_fake_tools(), probe_env(), run_probe(), scan_plan()] | lang=en
- "engine_scanner_runscan": "runScan()" | kind=code-symbol | source=manager/frontend/lib/engine/scanner.ts:L17 | neighbors=[tools.ts, interactive.ts, scan.ts, scanner.ts, bySeverityCount()] | lang=en
- "engine_tool_runners_rundbenum": "runDbEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1276 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runhttpx": "runHttpx()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L666 | neighbors=[scanner.ts, tool-runners.ts, bin(), hasBinary(), spawnOpts()] | lang=en
- "engine_tool_runners_runnuclei": "runNuclei()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L407 | neighbors=[scanner.ts, tool-runners.ts, bin(), spawnOpts(), streamProcess()] | lang=en
- "engine_tool_runners_runsshaudit": "runSshAudit()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L910 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runsubfinder": "runSubfinder()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L638 | neighbors=[scanner.ts, tool-runners.ts, bin(), collectProcess(), spawnOpts()] | lang=en
- "engine_tool_runners_runtestssl": "runTestssl()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L497 | neighbors=[scanner.ts, tool-runners.ts, binName(), collectProcess(), spawnOpts()] | lang=en
- "engine_types_scanoptions": "ScanOptions" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L36 | neighbors=[tools.ts, interactive.ts, scan.ts, scanner.ts, types.ts] | lang=en
- "eyewitness_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/eyewitness/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, POST(), findings-store.ts, createFinding()] | lang=en
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, __dirname, frontendRoot, nextConfig] | lang=en
- "graph_analyzer": "analyzer.py" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, PathAnalyzer, _priority(), _safe_float(), PathAnalyzer — attack-path discovery, s…] | lang=en
- "graph_analyzer_pathanalyzer_find_paths_to_target": ".find_paths_to_target()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L140 | neighbors=[PathAnalyzer, ._materialise_path(), .movement_graph(), ._source_assets(), Return scored attack paths from every s…] | lang=en
- "graph_builder_asset_node_id": "asset_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L40 | neighbors=[builder.py, ._add_credential_edges(), .add_exploit_edges(), .add_network_edges(), .build_asset_graph()] | lang=en
- "graph_builder_enum_value": "_enum_value()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L52 | neighbors=[builder.py, exploit_complexity(), .build_asset_graph(), is_internet_exposed(), Normalise a value that may be an Enum, …] | lang=en
- "graph_builder_rationale_1": "GraphBuilder — turns engagement assets/services/findings into an attack graph." | kind=entity | source=manager/backend/app/graph/builder.py:L1 | neighbors=[builder.py, Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_108": "Build the full multi-type attack graph. Returns the populated DiGraph         (a" | kind=entity | source=manager/backend/app/graph/builder.py:L108 | neighbors=[.build_asset_graph(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_184": "For each exploitable finding add an EXPLOITS edge Finding→Asset with         ``w" | kind=entity | source=manager/backend/app/graph/builder.py:L184 | neighbors=[.add_exploit_edges(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_209": "Add CONNECTS_TO (directed reachability) and SAME_SEGMENT edges from         segm" | kind=entity | source=manager/backend/app/graph/builder.py:L209 | neighbors=[.add_network_edges(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_245": "CREDENTIAL_REUSE edges between assets sharing a credential.         ``credential" | kind=entity | source=manager/backend/app/graph/builder.py:L245 | neighbors=[._add_credential_edges(), Neo4jClient, Asset, Finding, Service] | lang=pt
- "graph_builder_rationale_266": "Load assets/services/findings for an engagement and build the graph." | kind=entity | source=manager/backend/app/graph/builder.py:L266 | neighbors=[.build_from_db(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_295": "Mirror the current in-memory graph into Neo4j via batched writes." | kind=entity | source=manager/backend/app/graph/builder.py:L295 | neighbors=[.sync_to_neo4j(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_53": "Normalise a value that may be an Enum, str, or None to a lowercase str." | kind=entity | source=manager/backend/app/graph/builder.py:L53 | neighbors=[_enum_value(), Neo4jClient, Asset, Finding, Service] | lang=en
- "graph_builder_rationale_71": "Edge cost for an EXPLOITS edge. Derived from the CVSS Attack Complexity     comp" | kind=entity | source=manager/backend/app/graph/builder.py:L71 | neighbors=[exploit_complexity(), Neo4jClient, Asset, Finding, Service] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-019.json

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
