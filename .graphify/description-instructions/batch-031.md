# Node Description Batch 32 of 92

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

- "scanner_os_fingerprint_build_icmp_echo": "build_icmp_echo()" | kind=code-symbol | source=scanner/os_fingerprint.py:L66 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_echo_ttl()]
- "scanner_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=scanner/os_fingerprint.py:L70 | neighbors=[os_fingerprint.py, _icmp(), ._icmp_timestamp()]
- "scanner_os_fingerprint_hop_estimate": "hop_estimate()" | kind=code-symbol | source=scanner/os_fingerprint.py:L162 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl()]
- "scanner_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/os_fingerprint.py:L361 | neighbors=[OSFingerprintScanner, fingerprint_os(), remote_clock()]
- "scanner_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=scanner/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, .scan_target(), Interpret a timestamp reply's transmit …]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …]
- "scanner_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=scanner/port_scanner.py:L92 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…]
- "scanner_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=scanner/rdp_scanner.py:L41 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…]
- "scanner_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=scanner/rdp_scanner.py:L55 | neighbors=[rdp_scanner.py, probe_rdp(), Parse a Connection Confirm. Returns Non…]
- "scanner_run_all_log": "_log()" | kind=code-symbol | source=scanner/run_all.py:L48 | neighbors=[run_all.py, main(), _run_stage()]
- "scanner_scan_funnel_scanner": "_Scanner" | kind=code-symbol | source=scanner/scan_funnel.py:L93 | neighbors=[scan_funnel.py, Protocol, .scan_target()]
- "scanner_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=scanner/scanner_base.py:L627 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…]
- "scanner_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=scanner/scanner_base.py:L169 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=scanner/scanner_base.py:L185 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…]
- "scanner_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=scanner/scanner_base.py:L470 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()]
- "scanner_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=scanner/scanner_base.py:L836 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…]
- "scanner_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=scanner/scanner_base.py:L373 | neighbors=[.acquire(), .run(), RateLimiter]
- "scanner_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=scanner/scanner_base.py:L717 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "scanner_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=scanner/scanner_base.py:L708 | neighbors=[.run(), ResultWriter, .to_json()]
- "scanner_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=scanner/scanner_base.py:L276 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "scanner_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=scanner/scanner_base.py:L324 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "scanner_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=scanner/service_banner.py:L131 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab()]
- "scanner_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=scanner/service_enum.py:L360 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target()]
- "scanner_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=scanner/service_enum.py:L126 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…]
- "scanner_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=scanner/service_enum.py:L104 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target()]
- "scanner_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=scanner/service_enum.py:L311 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target()]
- "scanner_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=scanner/service_enum.py:L395 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …]
- "scanner_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=scanner/service_enum.py:L147 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …]
- "scanner_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=scanner/service_enum.py:L174 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…]
- "scanner_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=scanner/service_enum.py:L184 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…]
- "scanner_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=scanner/service_enum.py:L215 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target()]
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=scanner/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "scanner_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=scanner/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "scanner_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=scanner/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "scanner_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=scanner/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "scanner_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=scanner/syn_scanner.py:L79 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…]
- "scanner_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=scanner/syn_scanner.py:L103 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …]
- "scanner_syn_scanner_classify": "classify()" | kind=code-symbol | source=scanner/syn_scanner.py:L179 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking()]
- "scanner_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=scanner/syn_scanner.py:L231 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-031.json

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
