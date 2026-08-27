# Node Description Batch 31 of 92

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

- "scanner_delta_scanner_significant_version_change": "_significant_version_change()" | kind=code-symbol | source=scanner/delta_scanner.py:L308 | neighbors=[delta_scanner.py, .diff(), True if version changed in a security-r…]
- "scanner_delta_scanner_stable_host_id": "_stable_host_id()" | kind=code-symbol | source=scanner/delta_scanner.py:L91 | neighbors=[delta_scanner.py, .load_jsonl(), Derive a stable host identity from a ra…]
- "scanner_device_classifier_classify_device": "classify_device()" | kind=code-symbol | source=scanner/device_classifier.py:L98 | neighbors=[device_classifier.py, classify_from_results(), Fuse OS family + open ports + service p…]
- "scanner_device_classifier_classify_from_results": "classify_from_results()" | kind=code-symbol | source=scanner/device_classifier.py:L201 | neighbors=[device_classifier.py, classify_device(), Convenience adapter: extract classifier…]
- "scanner_findings_is_open": "_is_open()" | kind=code-symbol | source=scanner/findings.py:L119 | neighbors=[findings.py, A definitively open TCP port. `open|fil…, _rule_cleartext_and_exposure()]
- "scanner_findings_summarize": "summarize()" | kind=code-symbol | source=scanner/findings.py:L1175 | neighbors=[findings.py, _main(), _tally()]
- "scanner_host_discovery_hostdiscoveryscanner_probe": "._probe()" | kind=code-symbol | source=scanner/host_discovery.py:L398 | neighbors=[HostDiscoveryScanner, .scan_target(), Return 'open', 'refused', or None (no r…]
- "scanner_host_discovery_neighbor": "Neighbor" | kind=code-symbol | source=scanner/host_discovery.py:L195 | neighbors=[host_discovery.py, parse_neighbor_line(), One OS neighbor-cache observation about…]
- "scanner_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=scanner/host_discovery.py:L111 | neighbors=[host_discovery.py, parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "scanner_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=scanner/host_discovery.py:L263 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line()]
- "scanner_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=scanner/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()]
- "scanner_init": "__init__.py" | kind=code-symbol | source=scanner/__init__.py:L1 | neighbors=[a548359 feat(auto-enrollment): implemen…, ae7a30b feat: add Posture & Patch-Compa…, VA scanner module — pure collection/sca…]
- "scanner_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=scanner/iot_scanner.py:L348 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…]
- "scanner_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=scanner/iot_scanner.py:L130 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…]
- "scanner_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=scanner/iot_scanner.py:L58 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…]
- "scanner_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=scanner/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "scanner_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=scanner/iot_scanner.py:L361 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content.]
- "scanner_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=scanner/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "scanner_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=scanner/iot_scanner.py:L405 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…]
- "scanner_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=scanner/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "scanner_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=scanner/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…]
- "scanner_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=scanner/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "scanner_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=scanner/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]
- "scanner_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=scanner/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "scanner_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=scanner/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "scanner_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=scanner/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()]
- "scanner_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=scanner/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…]
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()]
- "scanner_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L174 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…]
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L152 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…]
- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L161 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…]
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "scanner_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=scanner/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "scanner_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "scanner_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=scanner/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "scanner_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=scanner/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "scanner_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=scanner/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "scanner_os_fingerprint_accept_echo_reply": "accept_echo_reply()" | kind=code-symbol | source=scanner/os_fingerprint.py:L137 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), True only for an ICMP ECHO reply that a…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-030.json

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
