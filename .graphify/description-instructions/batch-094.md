# Node Description Batch 95 of 336

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

- "detection_engine_version_compare_save_validation_marker": "_save_validation_marker()" | kind=code-symbol | source=manager/detection_engine/version_compare.py:L232 | neighbors=[version_compare.py, _load_validation_markers(), verify_pure_python_matches_dpkg()]
- "detection_engine_vuln_db_clear_caches": "_clear_caches()" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L137 | neighbors=[vuln_db.py, Test hook: drop the memoized snapshot c…, Test hook: drop the memoized snapshot c…]
- "detection_exposure_fusion_service_recompute_fused_exposure": "recompute_fused_exposure()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L50 | neighbors=[exposure_fusion_service.py, Fuse all probes' exposure_matrix observ…, _results_from_scan_rows()]
- "detection_exposure_fusion_service_results_from_scan_rows": "_results_from_scan_rows()" | kind=code-symbol | source=manager/backend/app/detection/exposure_fusion_service.py:L30 | neighbors=[exposure_fusion_service.py, Reconstruct one {"exposure": [...]} dic…, recompute_fused_exposure()]
- "detection_logger_attacklogger_log_action": ".log_action()" | kind=code-symbol | source=manager/backend/app/detection/logger.py:L27 | neighbors=[AttackLogger, _as_uuid(), Persist a single attack action. Returns…]
- "detection_siem_elasticsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L219 | neighbors=[ElasticSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_elasticsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L204 | neighbors=[ElasticSIEM, .build_query(), ._request()]
- "detection_siem_sentinelsiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L163 | neighbors=[SentinelSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_sentinelsiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L152 | neighbors=[SentinelSIEM, .build_kql(), ._request()]
- "detection_siem_splunksiem_parse_response": ".parse_response()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L107 | neighbors=[SplunkSIEM, _parse_dt(), SIEMAlert]
- "detection_siem_splunksiem_query_alerts": ".query_alerts()" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L96 | neighbors=[SplunkSIEM, ._request(), .build_spl()]
- "detection_vantage_fusion_collect": "_collect()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L37 | neighbors=[vantage_fusion.py, fuse_exposure_results(), (ip → {(proto,port): {vantage: status}}…]
- "detection_vantage_fusion_fused_service_exposure": "fused_service_exposure()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L118 | neighbors=[vantage_fusion.py, fuse_exposure_results(), (ip, proto, port) → fused exposure verd…]
- "detection_vantage_fusion_is_external": "_is_external()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L30 | neighbors=[vantage_fusion.py, fuse_exposure_results(), _verdict()]
- "detection_vantage_fusion_verdict": "_verdict()" | kind=code-symbol | source=manager/backend/app/detection/vantage_fusion.py:L67 | neighbors=[vantage_fusion.py, fuse_exposure_results(), _is_external()]
- "detection_verification_qualifies_for_llm": "_qualifies_for_llm()" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L75 | neighbors=[verification.py, Only spend an LLM call where a rational…, verify_finding()]
- "detection_verification_verificationverdict": "VerificationVerdict" | kind=code-symbol | source=manager/backend/app/detection/verification.py:L29 | neighbors=[verification.py, compute_verdict(), verify_finding()]
- "discovery_device_profile_asset_type_for": "asset_type_for()" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L29 | neighbors=[device_profile.py, device_profiles(), The AssetType for a classifier device_t…]
- "discovery_device_profile_device_profiles": "device_profiles()" | kind=code-symbol | source=manager/backend/app/discovery/device_profile.py:L36 | neighbors=[device_profile.py, asset_type_for(), ip → {asset_type, device_role, role_det…]
- "discovery_rate_limiter_ratelimiter_is_within_window": ".is_within_window()" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L43 | neighbors=[RateLimiter, .acquire(), True if current time is inside the allo…]
- "discovery_scan_health": "scan_health.py" | kind=code-symbol | source=manager/backend/app/discovery/scan_health.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, scan_health_summary(), scan_health.py — turn the probe's per-h…]
- "discovery_service_vuln_http_rules": "_http_rules()" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L95 | neighbors=[service_vuln.py, create_service_vuln_findings(), Findings for an HTTP service, from its …]
- "discovery_service_vuln_ssh_rules": "_ssh_rules()" | kind=code-symbol | source=manager/backend/app/discovery/service_vuln.py:L64 | neighbors=[service_vuln.py, create_service_vuln_findings(), SSH hygiene findings the CVE engine doe…]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-094.json

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
