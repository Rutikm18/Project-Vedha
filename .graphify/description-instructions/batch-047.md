# Node Description Batch 48 of 330

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

- "scanner_ftp_scanner_ftpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/ftp_scanner.py:L95 | neighbors=[FTPScanner, banner_software(), ._cmd(), ._list_bounded(), ._read_response(), Blocking: greeting → anonymous login → …]
- "scanner_host_discovery_device_hint": "device_hint()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L239 | neighbors=[host_discovery.py, is_locally_administered(), .scan_target(), Best-effort device classification from …, Best-effort device classification from …, Best-effort device classification from …]
- "scanner_host_discovery_is_locally_administered": "is_locally_administered()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L222 | neighbors=[host_discovery.py, device_hint(), .scan_target(), True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…, True if the 2nd-least-significant bit o…]
- "scanner_host_discovery_normalize_mac": "normalize_mac()" | kind=code-symbol | source=probe/scanner/host_discovery.py:L208 | neighbors=[host_discovery.py, parse_nbstat(), parse_neighbor_line(), Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…, Zero-pad each octet ('d2:58:2b:ff:cb:4'…]
- "scanner_ipmi_scanner_ipmiscanner": "IPMIScanner" | kind=code-symbol | source=probe/scanner/ipmi_scanner.py:L65 | neighbors=[ipmi_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_ipv6_discovery_discover_ipv6_hosts": "discover_ipv6_hosts()" | kind=code-symbol | source=probe/scanner/ipv6_discovery.py:L118 | neighbors=[ipv6_discovery.py, _own_ipv6_addresses(), _ping_all_nodes(), _read_neighbor_cache(), main(), Discover live IPv6 neighbors on the seg…]
- "scanner_ldap_scanner_ldapscanner": "LDAPScanner" | kind=code-symbol | source=probe/scanner/ldap_scanner.py:L47 | neighbors=[ldap_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/scanner/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "scanner_mass_scan_run_masscan": "_run_masscan()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L64 | neighbors=[mass_scan.py, Run masscan over the given target specs…, MasscanRun, _parse_masscan_json_detailed(), Run masscan over the given target specs…, _parse_masscan_json()]
- "scanner_msrpc_scanner_msrpcscanner": "MSRPCScanner" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L82 | neighbors=[msrpc_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "scanner_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…, Build an ICMP message (header + rest) w…]
- "scanner_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L436 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…, Send an ICMP timestamp request (type 13…]
- "scanner_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/scanner/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…, Listen-only discovery. No active probin…]
- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L267 | neighbors=[.scan_target(), Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), probe_rdp_posture(), One synchronous RDP handshake offering …, One synchronous RDP handshake. Best-eff…]
- "scanner_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L135 | neighbors=[rdp_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), main()]
- "scanner_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/scanner/run_all.py:L59 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…, Run one scanner module as a subprocess,…]
- "scanner_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L497 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window)., Current integer window (>= min_window)., Full, debuggable classification for att…, Current integer window (>= min_window).]
- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L421 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…, Read-only view of excluded networks (to…]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L416 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…, Read-only view of allowed networks (for…, Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_sendpacer": "SendPacer" | kind=code-symbol | source=probe/scanner/scanner_base.py:L535 | neighbors=[scanner_base.py, Blocking packets-per-second pacer with …, .__init__(), .observe_round(), .pace(), .stats()]
- "scanner_scanner_registry": "scanner_registry.py" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, info(), is_verified(), ScannerInfo, verification_report(), scanner_registry.py — the single source…]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L426 | neighbors=[ServiceBannerScanner, match_service(), parse_http_head(), ._ladder_for(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=probe/scanner/service_enum.py:L478 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "scanner_smb_enum_scanner_smbenumscanner": "SMBEnumScanner" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L218 | neighbors=[smb_enum_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L273 | neighbors=[smb_scanner.py, ntlm_os_build(), _align8(), _encryption_context(), _preauth_integrity_context(), .scan_target()]
- "scanner_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L362 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), ._ntlm_fingerprint(), .scan_target()]
- "scanner_smtp_scanner_smtpscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L87 | neighbors=[Blocking: greeting → EHLO → STARTTLS/VR…, SMTPScanner, parse_ehlo_capabilities(), ._cmd(), ._read_response(), vrfy_leaks()]
- "scanner_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community(), ._query()]
- "scanner_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "scanner_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]
- "scanner_ssh_scanner_parse_kexinit": "parse_kexinit()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L106 | neighbors=[ssh_scanner.py, _Cursor, .read(), .read_name_list(), Parse a SSH_MSG_KEXINIT body into its n…, ._scan_port()]
- "scanner_ssh_scanner_sshscanner": "SSHScanner" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L242 | neighbors=[ssh_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "scanner_ssh_scanner_sshscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L279 | neighbors=[SSHScanner, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), .scan_target()]
- "scanner_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L91 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "scanner_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L115 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "scanner_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L213 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…]
- "scanner_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L295 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), A genuine reply to our SYN acknowledges…, Outbound-interface IP for reaching dst_…, Outbound-interface IP for reaching dst_…]
- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L176 | neighbors=[syn_scanner.py, parse_tcp_options(), Back-compat shim: MSS only. New code us…, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-047.json

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
