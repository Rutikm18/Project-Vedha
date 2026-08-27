# Node Description Batch 28 of 92

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

- "main_scripts_host_discovery_rationale_264": "Bulk {ip: normalized_mac} snapshot of the neighbor cache (fallback path).      R" | kind=entity | source=main_scripts/host_discovery.py:L264 | neighbors=[read_arp_table(), BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_rationale_311": "Combine TCP + neighbor signals into a confidence-scored verdict.      Returns a" | kind=entity | source=main_scripts/host_discovery.py:L311 | neighbors=[fuse_liveness(), BaseScanner, ScanResult] | lang=pt
- "main_scripts_host_discovery_rationale_399": "Return 'open', 'refused', or None (no response)." | kind=entity | source=main_scripts/host_discovery.py:L399 | neighbors=[._probe(), BaseScanner, ScanResult] | lang=en
- "main_scripts_host_discovery_read_arp_table": "read_arp_table()" | kind=code-symbol | source=main_scripts/host_discovery.py:L263 | neighbors=[host_discovery.py, Bulk {ip: normalized_mac} snapshot of t…, parse_neighbor_line()] | lang=en
- "main_scripts_host_discovery_read_neighbor": "read_neighbor()" | kind=code-symbol | source=main_scripts/host_discovery.py:L232 | neighbors=[host_discovery.py, Targeted, POST-probe neighbor lookup fo…, parse_neighbor_line()] | lang=en
- "main_scripts_iot_scanner_coap_get_wellknown_core": "_coap_get_wellknown_core()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L348 | neighbors=[iot_scanner.py, _probe_coap_sync(), CoAP Confirmable GET for /.well-known/c…] | lang=en
- "main_scripts_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L130 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…] | lang=en
- "main_scripts_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L58 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…] | lang=en
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L259 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()] | lang=en
- "main_scripts_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L361 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content.] | lang=en
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L383 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()] | lang=en
- "main_scripts_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L405 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…] | lang=en
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=main_scripts/iot_scanner.py:L90 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()] | lang=en
- "main_scripts_ja4s_compute_ja4s": "compute_ja4s()" | kind=code-symbol | source=main_scripts/ja4s.py:L115 | neighbors=[ja4s.py, ja4s_from_parsed(), Do one standard TLS handshake and compu…] | lang=en
- "main_scripts_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=main_scripts/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()] | lang=en
- "main_scripts_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=main_scripts/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …] | lang=en
- "main_scripts_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=main_scripts/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()] | lang=en
- "main_scripts_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=main_scripts/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…] | lang=en
- "main_scripts_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=main_scripts/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …] | lang=en
- "main_scripts_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=main_scripts/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()] | lang=en
- "main_scripts_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=main_scripts/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…] | lang=en
- "main_scripts_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=main_scripts/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()] | lang=en
- "main_scripts_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=main_scripts/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()] | lang=en
- "main_scripts_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L174 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…] | lang=en
- "main_scripts_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L152 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…] | lang=en
- "main_scripts_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L161 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…] | lang=en
- "main_scripts_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=main_scripts/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()] | lang=en
- "main_scripts_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…] | lang=en
- "main_scripts_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()] | lang=en
- "main_scripts_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…] | lang=en
- "main_scripts_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…] | lang=en
- "main_scripts_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=main_scripts/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…] | lang=en
- "main_scripts_os_fingerprint_accept_echo_reply": "accept_echo_reply()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L137 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), True only for an ICMP ECHO reply that a…] | lang=en
- "main_scripts_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()] | lang=en
- "main_scripts_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L70 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_timestamp()] | lang=en
- "main_scripts_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L162 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()] | lang=en
- "main_scripts_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L361 | neighbors=[OSFingerprintScanner, fingerprint_os(), remote_clock()] | lang=en
- "main_scripts_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, .scan_target(), Interpret a timestamp reply's transmit …] | lang=en
- "main_scripts_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=main_scripts/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…] | lang=en
- "main_scripts_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=main_scripts/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-027.json

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
