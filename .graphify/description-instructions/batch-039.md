# Node Description Batch 40 of 119

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

- "detection_siem_elasticsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L204 | neighbors=[ElasticSIEM, .build_query(), ._request()]
- "detection_siem_sentinelsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L163 | neighbors=[SentinelSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_sentinelsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L152 | neighbors=[SentinelSIEM, .build_kql(), ._request()]
- "detection_siem_splunksiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L107 | neighbors=[SplunkSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_splunksiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L96 | neighbors=[SplunkSIEM, ._request(), .build_spl()]
- "discovery_finding_translator_find_open_duplicate": "_find_open_duplicate()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L75 | neighbors=[finding_translator.py, create_findings_from_probe_result(), A still-relevant Finding with the same …]
- "discovery_finding_translator_resolve_asset": "_resolve_asset()" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L53 | neighbors=[finding_translator.py, create_findings_from_probe_result(), Find the Asset for a probe-reported tar…]
- "discovery_rate_limiter_ratelimiter_is_within_window": ".is_within_window()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L43 | neighbors=[RateLimiter, .acquire(), True if current time is inside the allo…]
- "discovery_worker_discoveryworker_banner_grab_all": "._banner_grab_all()" | kind=code-symbol | source=manager/backend/app/discovery/worker.py:L149 | neighbors=[DiscoveryWorker, ._grab_one(), .run()]
- "discovery_xml_parser_nmapxmlparser_parse_port": "._parse_port()" | kind=code-symbol | source=manager/backend/app/discovery/xml_parser.py:L114 | neighbors=[NmapXMLParser, ._parse_host(), ParsedPort]
- "engagements_page_engagementspage": "EngagementsPage()" | kind=code-symbol | source=manager/frontend/app/engagements/page.tsx:L87 | neighbors=[page.tsx, hasValidDateRange(), splitEntries()]
- "engine_tool_runners_hassystembinary": "hasSystemBinary()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L35 | neighbors=[tool-runners.ts, isWindows(), resolveBinPath()]
- "engine_tool_runners_nativebannergrab": "nativeBannerGrab()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L303 | neighbors=[tool-runners.ts, httpBannerGrab(), tcpBannerGrab()]
- "engine_tool_runners_resolvebinpath": "resolveBinPath()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L54 | neighbors=[tool-runners.ts, hasBinary(), hasSystemBinary()]
- "engine_tool_runners_runldapenum": "runLdapEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1210 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnetbiosenum": "runNetbiosEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1147 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnfsenum": "runNfsEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1263 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runnmap": "runNmap()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L203 | neighbors=[scanner.ts, tool-runners.ts, tools.ts]
- "engine_tool_runners_runrdpfingerprint": "runRdpFingerprint()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1289 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runrpcenum": "runRpcEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1238 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runsmbenum": "runSmbEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1079 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_runsnmpenum": "runSnmpEnum()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1169 | neighbors=[scanner.ts, tool-runners.ts, runNmapNse()]
- "engine_tool_runners_streamprocess": "streamProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L99 | neighbors=[tool-runners.ts, runNaabu(), runNuclei()]
- "engine_types_scantool": "ScanTool" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L5 | neighbors=[interactive.ts, scan-modules.ts, types.ts]
- "exploit_msf_client_metasploitrpcclient_list_modules": ".list_modules()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L65 | neighbors=[MetasploitRPCClient, ._call(), module_type: exploit | auxiliary | payl…]
- "exploit_nuclei_exploit_nucleiexploitrunner_safe_template_check": ".safe_template_check()" | kind=code-symbol | source=manager/backend/app/exploit/nuclei_exploit.py:L59 | neighbors=[NucleiExploitRunner, Parse template YAML and validate it con…, Parse template YAML and validate it con…]
- "exploit_orchestrator_exploitorchestrator_generate_dns_callback_token": ".generate_dns_callback_token()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L252 | neighbors=[ExploitOrchestrator, Returns a unique FQDN for out-of-band D…, Returns a unique FQDN for out-of-band D…]
- "exploit_safety_validate_module": "validate_module()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L202 | neighbors=[safety.py, Raises SafetyViolationError if module i…, SafetyViolationError]
- "exploit_safety_validate_payload": "validate_payload()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L174 | neighbors=[safety.py, Raises SafetyViolationError if payload …, SafetyViolationError]
- "exploit_safety_validate_scope": "validate_scope()" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L212 | neighbors=[safety.py, Raises OutOfScopeError if target_ip is …, OutOfScopeError]
- "findings_page_findingdetail": "FindingDetail()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L362 | neighbors=[page.tsx, getSlaColor(), riskScoreColor()]
- "frontend_postcss_config": "postcss.config.mjs" | kind=code-symbol | source=manager/frontend/postcss.config.mjs:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, config, 298a9d4 trim frontend to 7 core pages; …]
- "graph_analyzer_pathanalyzer_exploit_info": "._exploit_info()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L67 | neighbors=[PathAnalyzer, .movement_graph(), Best (easiest) exploitable finding on a…]
- "graph_analyzer_pathanalyzer_find_blast_radius": ".find_blast_radius()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L250 | neighbors=[PathAnalyzer, .movement_graph(), Assets reachable (and thus at risk) if …]
- "graph_analyzer_pathanalyzer_identify_chokepoints": ".identify_chokepoints()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L218 | neighbors=[PathAnalyzer, _priority(), Assets that appear in more than ``thres…]
- "graph_analyzer_pathanalyzer_materialise_path": "._materialise_path()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L175 | neighbors=[PathAnalyzer, .find_paths_to_target(), .score_path()]
- "graph_analyzer_pathanalyzer_source_assets": "._source_assets()" | kind=code-symbol | source=manager/backend/app/graph/analyzer.py:L129 | neighbors=[PathAnalyzer, .find_paths_to_target(), .movement_graph()]
- "graph_builder_finding_node_id": "finding_node_id()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L48 | neighbors=[builder.py, .add_exploit_edges(), .build_asset_graph()]
- "graph_builder_graphbuilder_sync_to_neo4j": ".sync_to_neo4j()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L294 | neighbors=[GraphBuilder, .build_from_db(), Mirror the current in-memory graph into…]
- "graph_builder_is_internet_exposed": "is_internet_exposed()" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L83 | neighbors=[builder.py, .build_asset_graph(), _enum_value()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-039.json

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
