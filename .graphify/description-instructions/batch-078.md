# Node Description Batch 79 of 236

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

- "scanner_ja4s_ext_types": "_ext_types()" | kind=code-symbol | source=probe/scanner/ja4s.py:L65 | neighbors=[ja4s.py, _walk_extensions(), ja4s_from_parsed()]
- "scanner_ja4s_ja4s_from_serverhello": "ja4s_from_serverhello()" | kind=code-symbol | source=probe/scanner/ja4s.py:L109 | neighbors=[ja4s.py, ja4s_from_parsed(), JA4S from raw ServerHello record bytes …]
- "scanner_ja4x_hash_oids": "_hash_oids()" | kind=code-symbol | source=probe/scanner/ja4x.py:L68 | neighbors=[ja4x.py, oid_to_hex(), ja4x_from_oid_lists()]
- "scanner_ja4x_ja4x_from_der": "ja4x_from_der()" | kind=code-symbol | source=probe/scanner/ja4x.py:L93 | neighbors=[ja4x.py, ja4x_from_cert(), JA4X from raw DER bytes. `cryptography`…]
- "scanner_ja4x_oid_to_hex": "oid_to_hex()" | kind=code-symbol | source=probe/scanner/ja4x.py:L39 | neighbors=[ja4x.py, _hash_oids(), DER-encode an OID's content octets and …]
- "scanner_mass_scan_parse_masscan_json_detailed": "_parse_masscan_json_detailed()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L154 | neighbors=[mass_scan.py, _parse_masscan_json(), _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L212 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "scanner_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "scanner_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "scanner_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "scanner_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "scanner_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "scanner_os_fingerprint_accept_echo_reply": "accept_echo_reply()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L137 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), True only for an ICMP ECHO reply that a…]
- "scanner_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "scanner_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L70 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_timestamp()]
- "scanner_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L162 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "scanner_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L361 | neighbors=[OSFingerprintScanner, fingerprint_os(), remote_clock()]
- "scanner_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, .scan_target(), Interpret a timestamp reply's transmit …]
- "scanner_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L41 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…]
- "scanner_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L55 | neighbors=[rdp_scanner.py, probe_rdp(), Parse a Connection Confirm. Returns Non…]
- "scanner_run_all_log": "_log()" | kind=code-symbol | source=probe/scanner/run_all.py:L48 | neighbors=[run_all.py, main(), _run_stage()]
- "scanner_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L191 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…]
- "scanner_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L93 | neighbors=[scan_funnel.py, Protocol, .scan_target()]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L373 | neighbors=[.acquire(), .run(), RateLimiter]
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L717 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L708 | neighbors=[.run(), ResultWriter, .to_json()]
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L276 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L324 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "scanner_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=probe/scanner/service_enum.py:L360 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target()]
- "scanner_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=probe/scanner/service_enum.py:L126 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…]
- "scanner_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=probe/scanner/service_enum.py:L104 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target()]
- "scanner_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=probe/scanner/service_enum.py:L311 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target()]
- "scanner_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=probe/scanner/service_enum.py:L395 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …]
- "scanner_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=probe/scanner/service_enum.py:L147 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …]
- "scanner_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=probe/scanner/service_enum.py:L174 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…]
- "scanner_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=probe/scanner/service_enum.py:L184 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…]
- "scanner_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=probe/scanner/service_enum.py:L215 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target()]
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "scanner_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "scanner_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-078.json

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
