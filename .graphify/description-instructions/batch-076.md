# Node Description Batch 77 of 336

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

- "scanner_delta_scanner_extract_version": "_extract_version()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L140 | neighbors=[delta_scanner.py, .load_jsonl(), Best-effort version string., Best-effort version string.]
- "scanner_delta_scanner_new_service_severity": "_new_service_severity()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L298 | neighbors=[delta_scanner.py, .diff(), Heuristic priority for a newly-detected…, Heuristic priority for a newly-detected…]
- "scanner_delta_scanner_scanrecord": "ScanRecord" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L55 | neighbors=[delta_scanner.py, .load_jsonl(), Normalised representation of one ScanRe…, Normalised representation of one ScanRe…]
- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L310 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…, True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L93 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…, Derive a stable host identity from a ra…]
- "scanner_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L110 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…, Fuse OS family + open ports + service p…]
- "scanner_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=probe/scanner/device_classifier.py:L237 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…, Convenience adapter: extract classifier…]
- "scanner_dns_scanner_dnsscanner_ptr_self": "._ptr_self()" | kind=code-symbol | source=probe/scanner/dns_scanner.py:L119 | neighbors=[DNSScanner, ._probe(), _is_ip(), Ask the target (as a resolver) for the …]
- "scanner_findings_as_dict": "_as_dict()" | kind=code-symbol | source=probe/scanner/findings.py:L97 | neighbors=[findings.py, build_service_index(), Accept a raw JSONL dict or a ScanResult…, run_findings()]
- "scanner_findings_rule_smb": "_rule_smb()" | kind=code-symbol | source=probe/scanner/findings.py:L254 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_snmp": "_rule_snmp()" | kind=code-symbol | source=probe/scanner/findings.py:L277 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_ssh": "_rule_ssh()" | kind=code-symbol | source=probe/scanner/findings.py:L582 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_tls": "_rule_tls()" | kind=code-symbol | source=probe/scanner/findings.py:L175 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_udp_amplification": "_rule_udp_amplification()" | kind=code-symbol | source=probe/scanner/findings.py:L308 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_findings_rule_web": "_rule_web()" | kind=code-symbol | source=probe/scanner/findings.py:L419 | neighbors=[findings.py, _data(), Finding, _scanner()]
- "scanner_ftp_scanner_ftpscanner_cmd": "._cmd()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L91 | neighbors=[FTPScanner, ._read_response(), ._list_bounded(), ._probe()]
- "scanner_host_discovery_hostdiscoveryscanner_udp_liveness": "._udp_liveness()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L560 | neighbors=[HostDiscoveryScanner, .scan_target(), ._udp_one(), Run the UDP tier concurrently; return e…]
- "scanner_host_discovery_hostdiscoveryscanner_udp_one": "._udp_one()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L534 | neighbors=[HostDiscoveryScanner, ._udp_liveness(), parse_nbstat(), One UDP liveness probe -> structured si…]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=probe/scanner/host_discovery.py:L294 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…, One OS neighbor-cache observation about…]
- "scanner_host_discovery_parse_nbstat": "parse_nbstat()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L103 | neighbors=[host_discovery.py, ._udp_one(), normalize_mac(), Parse a NetBIOS NBSTAT (node status) re…]
- "scanner_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L331 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line(), Targeted, POST-probe neighbor lookup fo…]
- "scanner_init": "__init__.py" | kind=code-symbol | source=probe/scanner/__init__.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, VA scanner module — pure collection/sca…, 298a9d4 trim frontend to 7 core pages; …]
- "scanner_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L348 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…, CoAP Confirmable GET for /.well-known/c…]
- "scanner_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L130 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…, Decode a DNS wire-format name, followin…]
- "scanner_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L58 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…, HTTP GET the UPnP rootDesc.xml and extr…]
- "scanner_iot_scanner_iotscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L452 | neighbors=[IoTScanner, _probe_cwmp(), _probe_mqtt(), _probe_rtsp()]
- "scanner_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L361 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content., Extract CoAP response code and content.]
- "scanner_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L405 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…, HTTP GET to CWMP port — detect ACS or C…]
- "scanner_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L291 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "scanner_ipmi_scanner_ipmiscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L72 | neighbors=[IPMIScanner, build_open_session_request(), parse_open_session_response(), Blocking: one RMCP+ Open Session Reques…]
- "scanner_ipv6_discovery_parse_ip_neigh6": "parse_ip_neigh6()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L42 | neighbors=[ipv6_discovery.py, _is_ipv6(), Parse Linux `ip -6 neigh show` into [(a…, _read_neighbor_cache()]
- "scanner_ipv6_discovery_parse_ndp": "parse_ndp()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L59 | neighbors=[ipv6_discovery.py, _is_ipv6(), Parse macOS/BSD `ndp -an` into [(addres…, _read_neighbor_cache()]
- "scanner_ipv6_discovery_ping_all_nodes": "_ping_all_nodes()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L102 | neighbors=[ipv6_discovery.py, discover_ipv6_hosts(), _run(), Fire an ICMPv6 echo at ff02::1 (scoped …]
- "scanner_ja4s_selected_alpn": "_selected_alpn()" | kind=code-symbol | source=probe/scanner/ja4s.py:L69 | neighbors=[ja4s.py, ja4s_from_parsed(), The single ALPN protocol the server cho…, _walk_extensions()]
- "scanner_ja4s_walk_extensions": "_walk_extensions()" | kind=code-symbol | source=probe/scanner/ja4s.py:L56 | neighbors=[ja4s.py, _ext_types(), Yield (type, value) for each extension …, _selected_alpn()]
- "scanner_ja4x_ja4x_from_cert": "ja4x_from_cert()" | kind=code-symbol | source=probe/scanner/ja4x.py:L82 | neighbors=[ja4x.py, ja4x_from_oid_lists(), ja4x_from_der(), JA4X from a `cryptography` x509 Certifi…]
- "scanner_ja4x_ja4x_from_oid_lists": "ja4x_from_oid_lists()" | kind=code-symbol | source=probe/scanner/ja4x.py:L75 | neighbors=[ja4x.py, ja4x_from_cert(), _hash_oids(), Pure JA4X from the three ordered OID li…]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan(), Excluded networks -> masscan --exclude …]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan(), A CIDR spec is in scope only if it is f…]
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L174 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…, JSON-typed body that actually talks abo…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-076.json

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
