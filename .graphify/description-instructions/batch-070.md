# Node Description Batch 71 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "detection_prioritization_load_offline_kev_epss": "_load_offline_kev_epss()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L130 | neighbors=[prioritization.py, prioritize_engagement_findings(), (kev_db, epss_db) from the pinned snaps…, (kev_db, epss_db) from the pinned snaps…]
- "detection_prioritization_strongest_exposure": "_strongest_exposure()" | kind=code-symbol | source=manager/backend/app/detection/prioritization.py:L124 | neighbors=[prioritization.py, prioritize_engagement_findings(), The most-exposed value among an asset's…, The most-exposed value among an asset's…]
- "detection_resolution_apply_manual_reopen": "apply_manual_reopen()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L149 | neighbors=[resolution.py, Operator reopens an auto/'manually'-res…, Operator reopens an auto/'manually'-res…, Operator reopens an auto/'manually'-res…]
- "detection_resolution_build_coverage": "build_coverage()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L36 | neighbors=[resolution.py, host_of(), What this run PROVABLY re-observed. An …, What this run PROVABLY re-observed. An …]
- "detection_resolution_host_of": "host_of()" | kind=code-symbol | source=manager/backend/app/detection/resolution.py:L28 | neighbors=[resolution.py, build_coverage(), IP/host part of a probe target: '10.0.0…, IP/host part of a probe target: '10.0.0…]
- "detection_siem_parse_dt": "_parse_dt()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L35 | neighbors=[siem.py, .parse_response(), .parse_response(), .parse_response()]
- "detection_siem_siemqueryengine_request": "._request()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L68 | neighbors=[.query_alerts(), .query_alerts(), SIEMQueryEngine, .query_alerts()]
- "discovery_device_profile": "device_profile.py" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, asset_type_for(), device_profiles(), device_profile.py — map a probe device_…]
- "discovery_exposure": "exposure.py" | kind=code-symbol | source=manager/backend/app/discovery/exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, escalate_for_exposure(), service_exposure(), exposure.py — reachability-aware risk f…]
- "discovery_finding_translator_create_scan_health_finding": "create_scan_health_finding()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L218 | neighbors=[finding_translator.py, _find_open_duplicate(), Raise ONE engagement-level finding when…, Raise ONE engagement-level finding when…]
- "discovery_finding_translator_finding_port": "_finding_port()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L87 | neighbors=[finding_translator.py, _escalate_by_exposure(), Best-effort port for a probe finding: e…, Best-effort port for a probe finding: e…]
- "discovery_rate_limiter": "rate_limiter.py" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, RateLimiter, RateLimiter — enforces PPS limits per C…, 298a9d4 trim frontend to 7 core pages; …]
- "discovery_xml_parser_nmapxmlparser_parse_host": "._parse_host()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L52 | neighbors=[NmapXMLParser, .parse(), ._parse_port(), ParsedHost]
- "engine_tool_runners_iswindows": "isWindows()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L30 | neighbors=[tool-runners.ts, binName(), hasSystemBinary(), spawnOpts()]
- "engine_types_scansummary": "ScanSummary" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L124 | neighbors=[llm.ts, scanner.ts, types.ts, output.ts]
- "exploit_msf_client_metasploitrpcclient_connect": ".connect()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L38 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, Authenticate with msfrpcd and store the…]
- "exploit_msf_client_metasploitrpcclient_get_job_status": ".get_job_status()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L102 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns {status, output, uuid}.]
- "exploit_msf_client_metasploitrpcclient_kill_job": ".kill_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L118 | neighbors=[MetasploitRPCClient, ._call(), .wait_for_job(), Returns True if job was successfully ki…]
- "exploit_msf_client_metasploitrpcclient_raw_call": "._raw_call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L157 | neighbors=[MetasploitRPCClient, ._call(), .connect(), MetasploitRPCError]
- "exploit_msf_client_metasploitrpcclient_run_module": ".run_module()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L83 | neighbors=[MetasploitRPCClient, ._call(), MetasploitRPCError, Execute a Metasploit module.         Re…]
- "exploit_msf_client_metasploitrpcclient_wait_for_job": ".wait_for_job()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L132 | neighbors=[MetasploitRPCClient, .get_job_status(), .kill_job(), Poll until job completes or max_wait ex…]
- "exploit_nuclei_exploit_nucleiexploitrunner_run_cve_poc": ".run_cve_poc()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L117 | neighbors=[NucleiExploitRunner, ._parse_poc_output(), Run Nuclei CVE PoC template against tar…, Run Nuclei CVE PoC template against tar…]
- "exploit_orchestrator_exploitorchestrator_check_approval_required": "._check_approval_required()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L287 | neighbors=[ExploitOrchestrator, .execute(), Creates and returns an ExploitApprovalR…, Creates and returns an ExploitApprovalR…]
- "exploit_orchestrator_exploitorchestrator_check_blast_radius": "._check_blast_radius()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L265 | neighbors=[ExploitOrchestrator, .execute(), Count running exploit jobs for this eng…, Count running exploit jobs for this eng…]
- "exploit_orchestrator_exploitorchestrator_select_exploit": ".select_exploit()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L67 | neighbors=[ExploitOrchestrator, .execute(), Returns {module, payload, safe_check} f…, Returns {module, payload, safe_check} f…]
- "exploit_orchestrator_exploitorchestrator_validate_safety": ".validate_safety()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L103 | neighbors=[ExploitOrchestrator, .execute(), Raises SafetyViolationError if module o…, Raises SafetyViolationError if module o…]
- "exploit_orchestrator_exploitorchestrator_validate_scope": ".validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L110 | neighbors=[ExploitOrchestrator, .execute(), Raises OutOfScopeError if target_ip not…, Raises OutOfScopeError if target_ip not…]
- "findings_page_findingdetail": "FindingDetail()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L75 | neighbors=[page.tsx, signalChips(), getSlaColor(), riskScoreColor()]
- "findings_page_getslacolor": "getSlaColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L251 | neighbors=[page.tsx, FindingDetail(), isUrgent(), urgencyReasons()]
- "findings_page_riskscorecolor": "riskScoreColor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx, FindingDetail(), FindingsPage(), RiskBadge()]
- "frontend_eslint_config": "eslint.config.mjs" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, eslintConfig, 298a9d4 trim frontend to 7 core pages; …]
- "graph_analyzer_pathanalyzer_score_path": ".score_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L199 | neighbors=[PathAnalyzer, ._materialise_path(), _safe_float(), Risk score 0–100 from: sum of exploit C…]
- "graph_builder_exploit_complexity": "exploit_complexity()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L70 | neighbors=[builder.py, _enum_value(), .add_exploit_edges(), Edge cost for an EXPLOITS edge. Derived…]
- "graph_builder_graphbuilder_add_credential_edges": "._add_credential_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L244 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), CREDENTIAL_REUSE edges between assets s…]
- "graph_builder_graphbuilder_add_network_edges": ".add_network_edges()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L208 | neighbors=[GraphBuilder, asset_node_id(), .build_asset_graph(), Add CONNECTS_TO (directed reachability)…]
- "graph_builder_graphbuilder_build_from_db": ".build_from_db()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L265 | neighbors=[GraphBuilder, .build_asset_graph(), .sync_to_neo4j(), Load assets/services/findings for an en…]
- "graph_neo4j_client": "neo4j_client.py" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Neo4jClient, Neo4jClient — thin, optional wrapper ar…, 298a9d4 trim frontend to 7 core pages; …]
- "graph_neo4j_client_neo4jclient_run": ".run()" | kind=code-symbol | source=manager/backend/app/graph/neo4j_client.py:L87 | neighbors=[Neo4jClient, .ensure_schema(), .run_write(), Run a Cypher statement and return recor…]
- "hooks_usemousegradient": "useMouseGradient.ts" | kind=code-symbol | source=manager/frontend/hooks/useMouseGradient.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, useMouseGradient(), page.tsx, 298a9d4 trim frontend to 7 core pages; …]
- "lib_adapters_toapiengagementcreate": "toApiEngagementCreate()" | kind=code-symbol | source=manager/frontend/lib/adapters.ts:L65 | neighbors=[route.ts, adapters.ts, normalizeList(), engagement-adapters.test.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-070.json

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
