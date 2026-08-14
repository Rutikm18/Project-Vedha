# Node Description Batch 29 of 186

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

- "lib_errors_vedhaerror": "VedhaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, diagnoseSpawnError(), .constructor(), .render(), .toJSON()]
- "lib_findings_store_ensuredir": "ensureDir()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L22 | neighbors=[findings-store.ts, deleteFinding(), getAllFindings(), saveFindings(), updateFinding(), updateFindingStatus()]
- "lib_graph_store_graphstore": "graphStore" | kind=code-symbol | source=manager/frontend/lib/graph-store.ts:L329 | neighbors=[route.ts, route.ts, route.ts, route.ts, graph-store.ts, route.ts]
- "lib_httpx_parser_parsehttpxjsonline": "parseHttpxJsonLine()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L41 | neighbors=[httpx-parser.ts, .decode(), isOptionalNumber(), isOptionalString(), normalizePort(), parsers.test.ts]
- "lib_netexec_parser": "netexec-parser.ts" | kind=code-symbol | source=manager/frontend/lib/netexec-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, NetExecHost, NetExecParseResult, parseBoolean(), parseNetExecLog(), scanner-adapters.test.ts]
- "lib_scan_events": "scan-events.ts" | kind=code-symbol | source=manager/frontend/lib/scan-events.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, broadcastToScan(), Callback, scanListeners, subscribeScan(), 298a9d4 trim frontend to 7 core pages; …]
- "lib_scanner_request_validation_validateopenvasscanrequest": "validateOpenVASScanRequest()" | kind=code-symbol | source=manager/frontend/lib/scanner-request-validation.ts:L112 | neighbors=[scanner-request-validation.ts, isRecord(), validateHost(), validateSafeString(), validateScannerTargets(), scanner-adapters.test.ts]
- "lib_security_context_resolvesecurityreference": "resolveSecurityReference()" | kind=code-symbol | source=manager/frontend/lib/security-context.ts:L37 | neighbors=[route.ts, route.ts, route.ts, security-context.ts, publicCveRecord(), SecurityContextError]
- "lib_testssl_parser_parsetestssljson": "parseTestsslJson()" | kind=code-symbol | source=manager/frontend/lib/testssl-parser.ts:L44 | neighbors=[testssl-parser.ts, parseTestsslJsonChecked(), parseTestsslOutput(), parsers.test.ts, tool-runners.ts, mapSeverity()]
- "lib_whatweb_parser": "whatweb-parser.ts" | kind=code-symbol | source=manager/frontend/lib/whatweb-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, parseWhatWebOutput(), WhatWebParseResult, WhatWebResult, scanner-adapters.test.ts]
- "main_scripts_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "main_scripts_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "main_scripts_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "main_scripts_delta_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "main_scripts_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/main_scripts/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L413 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, .__init__(), OSError, _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L220 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), .__init__(), .scan_target(), ICMP-echo liveness + TTL harvest -> OS-…]
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L88 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L98 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L131 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "main_scripts_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L645 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "main_scripts_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L615 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "main_scripts_service_banner": "service_banner.py" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _dec(), main(), match_service(), ServiceBannerScanner, service_banner.py — grab service banner…]
- "main_scripts_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L120 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "main_scripts_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "main_scripts_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "main_scripts_tls_fingerprint_fingerprint_host": "fingerprint_host()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L274 | neighbors=[tls_fingerprint.py, jarm_style_digest(), _one_probe(), _probe_specs(), Run all probes and return (62-char dige…, Run all probes and return (62-char dige…]
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L227 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L276 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanJob, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L114 | neighbors=[agent_ws.py, _agent_token_from_websocket(), _claim_pushed_job(), Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…, Persistent WebSocket for probe → manage…]
- "routers_agents_job_reachability_scope": "_job_reachability_scope()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L137 | neighbors=[agents.py, _agent_can_execute_job(), enqueue_agent_job(), Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…, Return the narrow IP scope needed to ro…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-028.json

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
