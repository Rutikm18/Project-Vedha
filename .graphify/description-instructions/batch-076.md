# Node Description Batch 77 of 330

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
- "scanner_mcp_ai_scanner_known_false_positive": "_known_false_positive()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L152 | neighbors=[mcp_ai_scanner.py, ._probe_port(), Server/body fingerprint match against k…, Server/body fingerprint match against k…]
- "scanner_mcp_ai_scanner_mcp_oauth_signal": "_mcp_oauth_signal()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L161 | neighbors=[mcp_ai_scanner.py, ._probe_port(), The strongest possible evidence for a r…, The strongest possible evidence for a r…]
- "scanner_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "scanner_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "scanner_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "scanner_msrpc_scanner_summarize": "_summarize()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L69 | neighbors=[msrpc_scanner.py, ._enumerate(), Reduce the raw endpoint list to distinc…, _extract_tcp_ports()]
- "scanner_nfs_scanner_nfsscanner_mount_export": "._mount_export()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L221 | neighbors=[NFSScanner, ._rpc(), parse_mount_export(), ._probe()]
- "scanner_nfs_scanner_nfsscanner_portmap_dump": "._portmap_dump()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L203 | neighbors=[NFSScanner, ._rpc(), parse_portmap_dump(), ._probe()]
- "scanner_nfs_scanner_recv_record": "_recv_record()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L136 | neighbors=[nfs_scanner.py, Read RPC record-marking fragments (RFC …, _recv_exact(), _rpc_call()]
- "scanner_nfs_scanner_xdr_u32": ".u32()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L63 | neighbors=[parse_mount_export(), parse_portmap_dump(), _XDR, .opaque()]
- "scanner_os_fingerprint_match_stack_signature": "match_stack_signature()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L202 | neighbors=[os_fingerprint.py, fingerprint_os(), infer_initial_ttl(), p0f-style match on (initial TTL, option…]
- "scanner_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L482 | neighbors=[OSFingerprintScanner, ._icmp_scan_target(), fingerprint_os(), remote_clock()]
- "scanner_os_fingerprint_osfingerprintscanner_tcp_ttl_result": "._tcp_ttl_result()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L468 | neighbors=[OSFingerprintScanner, ._icmp_scan_target(), fingerprint_os(), FIX 3b: aliveness/TTL came from a TCP S…]
- "scanner_os_fingerprint_parse_icmp_timestamps": "parse_icmp_timestamps()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L108 | neighbors=[os_fingerprint.py, ._icmp_timestamp(), _strip_ip_header(), Parse an ICMP timestamp reply (type 14)…]
- "scanner_os_fingerprint_remote_clock": "remote_clock()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L121 | neighbors=[os_fingerprint.py, ._icmp_scan_target(), Interpret a timestamp reply's transmit …, .scan_target()]
- "scanner_os_fingerprint_strip_ip_header": "_strip_ip_header()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L81 | neighbors=[os_fingerprint.py, parse_icmp_reply(), parse_icmp_timestamps(), Return (ttl, icmp_bytes). Raw-socket de…]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L416 | neighbors=[PortScanner, ._attempt(), ._maybe(), ._scan_port()]
- "scanner_port_scanner_portscanner_maybe": "._maybe()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L197 | neighbors=[PortScanner, ._build(), ._scan_port(), Emit a non-open result only when report…]
- "scanner_printer_scanner_build_ipp_get_printer_attributes": "build_ipp_get_printer_attributes()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L54 | neighbors=[printer_scanner.py, _ipp_attr(), ._probe_ipp(), A minimal IPP/1.1 Get-Printer-Attribute…]
- "scanner_printer_scanner_printerscanner_probe_pjl": "._probe_pjl()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L103 | neighbors=[PrinterScanner, ._probe(), parse_pjl_id(), _recv_bounded()]
- "scanner_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L42 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…, TPKT + X.224 Connection Request carryin…]
- "scanner_rsync_scanner_recv_until": "_recv_until()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L57 | neighbors=[rsync_scanner.py, _handshake(), ._list_modules(), ._test_anon()]
- "scanner_rsync_scanner_rsyncscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L130 | neighbors=[Blocking: list modules, then anon-test …, RsyncScanner, ._list_modules(), ._test_anon()]
- "scanner_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L244 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…]

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
