# Node Description Batch 60 of 186

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

- "main_scripts_iot_scanner_decode_mdns_name": "_decode_mdns_name()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L129 | neighbors=[iot_scanner.py, _parse_mdns_response(), Decode a DNS wire-format name, followin…]
- "main_scripts_iot_scanner_fetch_upnp_root_desc": "_fetch_upnp_root_desc()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L57 | neighbors=[iot_scanner.py, _probe_ssdp_sync(), HTTP GET the UPnP rootDesc.xml and extr…]
- "main_scripts_iot_scanner_mqtt_connect": "_mqtt_connect()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L257 | neighbors=[iot_scanner.py, _mqtt_remaining_len(), _probe_mqtt()]
- "main_scripts_iot_scanner_parse_coap_response": "_parse_coap_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L359 | neighbors=[iot_scanner.py, _probe_coap_sync(), Extract CoAP response code and content.]
- "main_scripts_iot_scanner_probe_coap_sync": "_probe_coap_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L381 | neighbors=[iot_scanner.py, _coap_get_wellknown_core(), _parse_coap_response()]
- "main_scripts_iot_scanner_probe_cwmp": "_probe_cwmp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L403 | neighbors=[iot_scanner.py, .scan_target(), HTTP GET to CWMP port — detect ACS or C…]
- "main_scripts_iot_scanner_probe_ssdp_sync": "_probe_ssdp_sync()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L89 | neighbors=[iot_scanner.py, _fetch_upnp_root_desc(), _parse_ssdp_headers()]
- "main_scripts_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "main_scripts_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "main_scripts_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "main_scripts_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan()]
- "main_scripts_mass_scan_parse_masscan_json": "_parse_masscan_json()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L147 | neighbors=[mass_scan.py, _parse_masscan_json_detailed(), Parse masscan -oJ output robustly: hand…]
- "main_scripts_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "main_scripts_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan()]
- "main_scripts_mcp_ai_scanner_auth_shaped_json_body": "_auth_shaped_json_body()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L173 | neighbors=[mcp_ai_scanner.py, ._probe_port(), JSON-typed body that actually talks abo…]
- "main_scripts_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L151 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…]
- "main_scripts_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "main_scripts_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "main_scripts_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "main_scripts_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "main_scripts_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "main_scripts_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "main_scripts_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L64 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "main_scripts_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L111 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L204 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Return (socket, is_raw). Prefer datagra…]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L79 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…]
- "main_scripts_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …]
- "main_scripts_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L89 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…]
- "main_scripts_run_all_log": "_log()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L38 | neighbors=[run_all.py, main(), _run_stage()]
- "main_scripts_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L204 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…]
- "main_scripts_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L86 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host()]
- "main_scripts_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L72 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host()]
- "main_scripts_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L54 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host()]
- "main_scripts_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L82 | neighbors=[scan_funnel.py, .scan_target(), Protocol]
- "main_scripts_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L547 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…]
- "main_scripts_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L98 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …]
- "main_scripts_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L114 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…]
- "main_scripts_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L399 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-059.json

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
