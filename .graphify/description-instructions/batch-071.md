# Node Description Batch 72 of 332

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

- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_portal_client_severity_var": "SEVERITY_VAR" | kind=code-symbol | source=manager/frontend/lib/portal-client.ts:L117 | neighbors=[page.tsx, portal-client.ts, page.tsx, page.tsx]
- "lib_severity_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L24 | neighbors=[FactCard.tsx, page.tsx, severity.ts, page.tsx]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "login_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L54 | neighbors=[route.ts, isClientToken(), setPortalCookies(), setSessionCookies()]
- "login_route_put": "PUT()" | kind=code-symbol | source=manager/frontend/app/api/portal/login/route.ts:L104 | neighbors=[route.ts, isClientToken(), setPortalCookies(), setSessionCookies()]
- "main_scripts_accuracy_gate_load_corpus": "load_corpus()" | kind=code-symbol | source=probe/main_scripts/accuracy_gate.py:L65 | neighbors=[accuracy_gate.py, load_corpora(), CorpusError, Load and structurally validate one corp…]
- "main_scripts_adaptive_timeout": "adaptive_timeout.py" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, AdaptiveTimeout, from_rtts(), test_main_scripts_adaptive_timeout.py]
- "main_scripts_adaptive_timeout_from_rtts": "from_rtts()" | kind=code-symbol | source=probe/main_scripts/adaptive_timeout.py:L53 | neighbors=[adaptive_timeout.py, AdaptiveTimeout, .observe(), Convenience: build an estimator and fol…]
- "main_scripts_delta_scanner_extract_service": "_extract_service()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L123 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort service name from data dict…, Best-effort service name from data dict…]
- "main_scripts_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L140 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string., Best-effort version string.]
- "main_scripts_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L298 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…, Heuristic priority for a newly-detected…]
- "main_scripts_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L55 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…, Normalised representation of one ScanRe…]
- "main_scripts_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L310 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…, True if version changed in a security-r…]
- "main_scripts_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/main_scripts/delta_scanner.py:L93 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…, Derive a stable host identity from a ra…]
- "main_scripts_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/main_scripts/device_classifier.py:L110 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…, Fuse OS family + open ports + service p…]
- "main_scripts_dns_scanner_dnsscanner_ptr_self": "._ptr_self()" | kind=code-symbol | source=probe/main_scripts/dns_scanner.py:L119 | neighbors=[DNSScanner, ._probe(), _is_ip(), Ask the target (as a resolver) for the …]
- "main_scripts_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/main_scripts/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "main_scripts_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/main_scripts/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=probe/main_scripts/findings.py:L582 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=probe/main_scripts/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=probe/main_scripts/findings.py:L308 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_findings_rule_web": "_rule_web()" | kind=code-symbol | source=probe/main_scripts/findings.py:L419 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "main_scripts_ftp_scanner_ftpscanner_cmd": "._cmd()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L91 | neighbors=[FTPScanner, ._read_response(), ._list_bounded(), ._probe()]
- "main_scripts_host_discovery_hostdiscoveryscanner_udp_liveness": "._udp_liveness()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L560 | neighbors=[HostDiscoveryScanner, .scan_target(), ._udp_one(), Run the UDP tier concurrently; return e…]
- "main_scripts_host_discovery_hostdiscoveryscanner_udp_one": "._udp_one()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L534 | neighbors=[HostDiscoveryScanner, ._udp_liveness(), parse_nbstat(), One UDP liveness probe -> structured si…]
- "main_scripts_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L294 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…, One OS neighbor-cache observation about…]
- "main_scripts_host_discovery_parse_nbstat": "parse_nbstat()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L103 | neighbors=[host_discovery.py, ._udp_one(), normalize_mac(), Parse a NetBIOS NBSTAT (node status) re…]
- "main_scripts_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/main_scripts/host_discovery.py:L331 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line(), Targeted, POST-probe neighbor lookup fo…]
- "main_scripts_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L348 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…, CoAP Confirmable GET for /.well-known/c…]
- "main_scripts_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L130 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…, Decode a DNS wire-format name, followin…]
- "main_scripts_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L58 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…, HTTP GET the UPnP rootDesc.xml and extr…]
- "main_scripts_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L452 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "main_scripts_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L361 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content., Extract CoAP response code and content.]
- "main_scripts_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L405 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…, HTTP GET to CWMP port — detect ACS or C…]
- "main_scripts_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L291 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "main_scripts_ipmi_scanner_ipmiscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L72 | neighbors=[IPMIScanner, build_open_session_request(), parse_open_session_response(), Blocking: one RMCP+ Open Session Reques…]
- "main_scripts_ipv6_discovery_parse_ip_neigh6": "parse_ip_neigh6()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L42 | neighbors=[ipv6_discovery.py, _is_ipv6(), Parse Linux `ip -6 neigh show` into [(a…, _read_neighbor_cache()]
- "main_scripts_ipv6_discovery_parse_ndp": "parse_ndp()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L59 | neighbors=[ipv6_discovery.py, _is_ipv6(), Parse macOS/BSD `ndp -an` into [(addres…, _read_neighbor_cache()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-071.json

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
