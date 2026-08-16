# Node Description Batch 52 of 209

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

- "scanner_iot_scanner_probe_mqtt": "_probe_mqtt()" | kind=code-symbol | source=probe/scanner/iot_scanner.py:L289 | neighbors=[iot_scanner.py, .scan_target(), _mqtt_connect(), _mqtt_subscribe_all()]
- "scanner_ja4s_selected_alpn": "_selected_alpn()" | kind=code-symbol | source=probe/scanner/ja4s.py:L69 | neighbors=[ja4s.py, ja4s_from_parsed(), The single ALPN protocol the server cho…, _walk_extensions()]
- "scanner_ja4s_walk_extensions": "_walk_extensions()" | kind=code-symbol | source=probe/scanner/ja4s.py:L56 | neighbors=[ja4s.py, _ext_types(), Yield (type, value) for each extension …, _selected_alpn()]
- "scanner_ja4x_ja4x_from_cert": "ja4x_from_cert()" | kind=code-symbol | source=probe/scanner/ja4x.py:L82 | neighbors=[ja4x.py, ja4x_from_oid_lists(), ja4x_from_der(), JA4X from a `cryptography` x509 Certifi…]
- "scanner_ja4x_ja4x_from_oid_lists": "ja4x_from_oid_lists()" | kind=code-symbol | source=probe/scanner/ja4x.py:L75 | neighbors=[ja4x.py, ja4x_from_cert(), _hash_oids(), Pure JA4X from the three ordered OID li…]
- "scanner_mass_scan_masscan_excludes": "_masscan_excludes()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L307 | neighbors=[mass_scan.py, Excluded networks -> masscan --exclude …, run_mass_scan(), Excluded networks -> masscan --exclude …]
- "scanner_mass_scan_spec_in_scope": "_spec_in_scope()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L312 | neighbors=[mass_scan.py, A CIDR spec is in scope only if it is f…, run_mass_scan(), A CIDR spec is in scope only if it is f…]
- "scanner_mobile_scanner_build_adb_cnxn": "_build_adb_cnxn()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L59 | neighbors=[mobile_scanner.py, _adb_checksum(), _probe_adb(), Build an ADB A_CNXN (CONNECT) message —…]
- "scanner_mobile_scanner_mobilescanner": "MobileScanner" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L278 | neighbors=[mobile_scanner.py, BaseScanner, .scan_target(), Detects mobile device exposure on the n…]
- "scanner_mobile_scanner_probe_mdns_mobile_sync": "_probe_mdns_mobile_sync()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L257 | neighbors=[mobile_scanner.py, _build_mdns_query(), _parse_mdns_ptr_names(), Send one mDNS PTR query to target:5353 …]
- "scanner_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L204 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…]
- "scanner_passive_collector_open_listener": "_open_listener()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L119 | neighbors=[passive_collector.py, .run(), Open one recv-only UDP listener or rais…, Open ONE recv-only UDP listener. Return…]
- "scanner_passive_collector_printable_strings": "_printable_strings()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L73 | neighbors=[passive_collector.py, _device_hint(), Pull short printable ASCII runs from a …, Pull short printable ASCII runs from a …]
- "scanner_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L287 | neighbors=[PortScanner, ._attempt(), ._maybe(), ._scan_port()]
- "scanner_port_scanner_portscanner_maybe": "._maybe()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L197 | neighbors=[PortScanner, ._build(), ._scan_port(), Emit a non-open result only when report…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L83 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), One synchronous RDP handshake. Best-eff…]
- "scanner_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/scanner/run_all.py:L45 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log()]
- "scanner_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L362 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window)., Current integer window (>= min_window).]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L676 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L176 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L269 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L286 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L281 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L170 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "scanner_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/scanner/service_banner.py:L128 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), One probe-ladder rung on its own connec…]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L78 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L117 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L102 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "scanner_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L178 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…]
- "scanner_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L230 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), Outbound-interface IP for reaching dst_…]
- "scanner_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L208 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-051.json

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
