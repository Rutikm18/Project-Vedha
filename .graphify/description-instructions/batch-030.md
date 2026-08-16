# Node Description Batch 31 of 209

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

- "lib_ai_engine_aireportstore": "aiReportStore" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L342 | neighbors=[ai-engine.ts, route.ts, route.ts, route.ts, route.ts, route.ts]
- "lib_assistant_factcardvm": "FactCardVM" | kind=code-symbol | source=manager/frontend/lib/assistant.ts:L4 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard.tsx, route.ts, assistant.ts, security-context.ts]
- "lib_cases_store_readcases": "readCases()" | kind=code-symbol | source=manager/frontend/lib/cases-store.ts:L213 | neighbors=[cases-store.ts, addComment(), createCase(), getCaseById(), ensureDataDir(), updateCase()]
- "lib_clients_store_write": "write()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L66 | neighbors=[clients-store.ts, createClient(), read(), updateClient(), updateClientSettings(), ensureDir()]
- "lib_errors_adversaerror": "AdversaError" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L57 | neighbors=[index.ts, errors.ts, .constructor(), .render(), .toJSON(), diagnoseSpawnError()]
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
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/logout/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, c140451 fix(portal): clean 409 on dupli…, POST(), 2885afa Add comprehensive probe testing…]
- "main_scripts_accuracy_score_findings": "score_findings()" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L48 | neighbors=[accuracy.py, evaluate_corpus(), Precision / recall / F1 of produced fin…, _expected_keys(), _finding_key(), _ratio()]
- "main_scripts_db_scanner_dbscanner": "DBScanner" | kind=code-symbol | source=probe/main_scripts/db_scanner.py:L237 | neighbors=[db_scanner.py, BaseScanner, .__init__(), ._probe_one(), ._scan_port(), .scan_target()]
- "main_scripts_delta_scanner_deltaengine": "DeltaEngine" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L157 | neighbors=[delta_scanner.py, .diff(), .load_jsonl(), .summary(), main(), Load JSONL scan snapshots and compute s…]
- "main_scripts_delta_scanner_deltaengine_diff": ".diff()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L204 | neighbors=[DeltaEngine, Delta, _new_service_severity(), _significant_version_change(), main(), Compute security-relevant deltas betwee…]
- "main_scripts_delta_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L317 | neighbors=[delta_scanner.py, .to_dict(), DeltaEngine, .diff(), .load_jsonl(), .summary()]
- "main_scripts_device_classifier": "device_classifier.py" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, classify_device(), classify_from_results(), device_classifier.py — infer a device's…, test_main_scripts_device.py]
- "main_scripts_findings_build_service_index": "build_service_index()" | kind=code-symbol | source=probe/main_scripts/findings.py:L153 | neighbors=[findings.py, _as_dict(), _data(), _scanner(), Map (target, port) -> confirmed-service…, _rule_cleartext_and_exposure()]
- "main_scripts_host_discovery_hostdiscoveryscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L413 | neighbors=[HostDiscoveryScanner, device_hint(), fuse_liveness(), ._probe(), is_locally_administered(), vendor_for_mac()]
- "main_scripts_host_discovery_parse_neighbor_line": "parse_neighbor_line()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L202 | neighbors=[host_discovery.py, Neighbor, normalize_mac(), Parse one `ip neigh` / `arp -n` / `ndp …, read_arp_table(), read_neighbor()]
- "main_scripts_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "main_scripts_nmap_wrapper_nmapexecutionerror": "NmapExecutionError" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L42 | neighbors=[nmap_wrapper.py, .__init__(), OSError, _parse_nmap_xml(), Actionable subprocess failure; never re…, _run_nmap()]
- "main_scripts_os_fingerprint_osfingerprintscanner": "OSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L220 | neighbors=[os_fingerprint.py, BaseScanner, ._icmp_echo_ttl(), .__init__(), .scan_target(), ICMP-echo liveness + TTL harvest -> OS-…]
- "main_scripts_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L311 | neighbors=[PortScanner, _family_of(), ._build(), ._scan_port(), One connect() and its classification. A…, One connect() and its classification. A…]
- "main_scripts_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, build_connection_request(), main(), parse_connection_confirm(), probe_rdp(), RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, main(), BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_run_all_main": "main()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L88 | neighbors=[run_all.py, _log(), _open_tcp_ports(), _ports_arg(), _read_jsonl(), _run_stage()]
- "main_scripts_scan_funnel_scanfunnel": "ScanFunnel" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L98 | neighbors=[scan_funnel.py, build_default_funnel(), Orchestrates discovery → port scan → ro…, .__init__(), .run(), .run_host()]
- "main_scripts_scan_funnel_scanfunnel_run_host": ".run_host()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L131 | neighbors=[ScanFunnel, _candidate_ports(), FunnelResult, _is_alive(), route_ports(), .scan_target()]
- "main_scripts_scanner_base_basescanner": "BaseScanner" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L645 | neighbors=[scanner_base.py, ._guarded(), .__init__(), .run(), .scan_target(), Subclasses implement `scan_target(self,…]
- "main_scripts_scanner_base_resultwriter": "ResultWriter" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L615 | neighbors=[scanner_base.py, Writes ScanResult objects as JSONL to a…, .close(), .__init__(), .write(), run_cli()]
- "main_scripts_service_banner_servicebannerscanner": "ServiceBannerScanner" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L120 | neighbors=[service_banner.py, BaseScanner, ._grab(), .__init__(), ._rung(), .scan_target()]
- "main_scripts_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "main_scripts_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-030.json

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
