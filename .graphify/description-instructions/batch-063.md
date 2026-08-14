# Node Description Batch 64 of 186

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

- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L160 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…]
- "scanner_mcp_ai_scanner_mcpaiscanner_result": "._result()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L211 | neighbors=[MCPAIScanner, ._probe_port(), _model_count()]
- "scanner_mobile_scanner_build_mdns_query": "_build_mdns_query()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L187 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Build a DNS PTR query in mDNS wire form…]
- "scanner_mobile_scanner_mobilescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L285 | neighbors=[MobileScanner, _probe_adb(), _probe_lockdownd()]
- "scanner_mobile_scanner_parse_adb_header": "_parse_adb_header()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L70 | neighbors=[mobile_scanner.py, _probe_adb(), Parse a 24-byte ADB message header.  Re…]
- "scanner_mobile_scanner_parse_mdns_ptr_names": "_parse_mdns_ptr_names()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L198 | neighbors=[mobile_scanner.py, _probe_mdns_mobile_sync(), Extract PTR target names (service insta…]
- "scanner_mobile_scanner_probe_lockdownd": "_probe_lockdownd()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L150 | neighbors=[mobile_scanner.py, .scan_target(), Attempt TCP connect to lockdownd port 6…]
- "scanner_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L64 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "scanner_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L111 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "scanner_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L187 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…]
- "scanner_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L79 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Parse an ICMP reply. Handles both raw-s…]
- "scanner_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L204 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…]
- "scanner_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L86 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host()]
- "scanner_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L72 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host()]
- "scanner_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L54 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host()]
- "scanner_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L82 | neighbors=[scan_funnel.py, Protocol, .scan_target()]
- "scanner_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L98 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L114 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L313 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L302 | neighbors=[.acquire(), .run(), RateLimiter]
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L637 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L628 | neighbors=[.run(), ResultWriter, .to_json()]
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L205 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L253 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "scanner_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "scanner_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "scanner_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "scanner_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L60 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…]
- "scanner_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L84 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …]
- "scanner_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L122 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking()]
- "scanner_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L174 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking()]
- "scanner_syn_scanner_parse_packet": "parse_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L106 | neighbors=[syn_scanner.py, Parse a raw IPv4+TCP packet (as receive…, ._syn_scan_blocking()]
- "scanner_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L152 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__()]
- "scanner_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L210 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "scanner_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L187 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-063.json

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
