# Node Description Batch 59 of 236

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

- "scanner_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L253 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…, True if we can open an ICMP socket (dat…]
- "scanner_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "scanner_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L300 | neighbors=[PortScanner, ._attempt(), ._maybe(), ._scan_port()]
- "scanner_port_scanner_portscanner_maybe": "._maybe()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L197 | neighbors=[PortScanner, ._build(), ._scan_port(), Emit a non-open result only when report…]
- "scanner_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L130 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…, Resolve a named scan profile to a concr…]
- "scanner_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L210 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics, Ports recorded more than once (a port m…, Ports recorded more than once (a port m…]
- "scanner_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L203 | neighbors=[Requested ports that were never recorde…, ScanMetrics, Requested ports that were never recorde…, Requested ports that were never recorde…]
- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L184 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L83 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), One synchronous RDP handshake. Best-eff…]
- "scanner_scan_funnel_build_default_funnel": "build_default_funnel()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L215 | neighbors=[scan_funnel.py, ScanFunnel, Wire the funnel with the package's real…, Wire the funnel with the package's real…]
- "scanner_scan_funnel_candidate_ports": "_candidate_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L97 | neighbors=[scan_funnel.py, The port set worth scanning = union of …, .run_host(), The port set worth scanning = union of …]
- "scanner_scan_funnel_funnelresult": "FunnelResult" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L83 | neighbors=[scan_funnel.py, The full outcome of funnelling one host., .run_host(), The full outcome of funnelling one host.]
- "scanner_scan_funnel_route_ports": "route_ports()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L65 | neighbors=[scan_funnel.py, Map a host's open ports onto the deep-s…, .run_host(), Map a host's open ports onto the deep-s…]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L756 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L169 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L185 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L384 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L247 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L340 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L173 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/service_enum.py:L465 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target()]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L118 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L125 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "scanner_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L415 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking(), Turn resolved port states + harvested i…]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "scanner_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync(), Flag the security-relevant properties o…]
- "scanner_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync(), Grade overall TLS posture A/B/C/F from …]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-058.json

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
