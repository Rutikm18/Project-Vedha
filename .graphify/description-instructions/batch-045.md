# Node Description Batch 46 of 336

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

- "main_scripts_findings_rule_nfs": "_rule_nfs()" | kind=code-symbol | source=probe/main_scripts/findings.py:L757 | neighbors=[findings.py, NFS anonymous export exposure. A world-…, _data(), Finding, _scanner(), NFS anonymous export exposure. A world-…]
- "main_scripts_findings_rule_printer": "_rule_printer()" | kind=code-symbol | source=probe/main_scripts/findings.py:L985 | neighbors=[findings.py, Exposed network printer — an informatio…, _data(), Finding, _scanner(), Exposed network printer — an informatio…]
- "main_scripts_findings_rule_rdp": "_rule_rdp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L535 | neighbors=[findings.py, Confirmed RDP (X.224 handshake) + NLA d…, _data(), Finding, _scanner(), Confirmed RDP (X.224 handshake) + NLA d…]
- "main_scripts_findings_rule_rsync": "_rule_rsync()" | kind=code-symbol | source=probe/main_scripts/findings.py:L823 | neighbors=[findings.py, rsync daemon exposure. Anonymously-sele…, _data(), Finding, _scanner(), rsync daemon exposure. Anonymously-sele…]
- "main_scripts_findings_rule_smb_enum": "_rule_smb_enum()" | kind=code-symbol | source=probe/main_scripts/findings.py:L618 | neighbors=[findings.py, Anonymous SMB (null-session) informatio…, _data(), Finding, _scanner(), Anonymous SMB (null-session) informatio…]
- "main_scripts_findings_rule_smtp": "_rule_smtp()" | kind=code-symbol | source=probe/main_scripts/findings.py:L924 | neighbors=[findings.py, SMTP hygiene: VRFY/EXPN user enumeratio…, _data(), Finding, _scanner(), SMTP hygiene: VRFY/EXPN user enumeratio…]
- "main_scripts_findings_rule_tls_fingerprint": "_rule_tls_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L467 | neighbors=[findings.py, JA4X-based threat-intel match. Fires on…, _data(), Finding, _scanner(), JA4X-based threat-intel match. Fires on…]
- "main_scripts_findings_rule_tls_server_fingerprint": "_rule_tls_server_fingerprint()" | kind=code-symbol | source=probe/main_scripts/findings.py:L515 | neighbors=[findings.py, JA4S-based threat-intel match on the TL…, _data(), Finding, _scanner(), JA4S-based threat-intel match on the TL…]
- "main_scripts_findings_rule_unauth_access": "_rule_unauth_access()" | kind=code-symbol | source=probe/main_scripts/findings.py:L489 | neighbors=[findings.py, Proven UNAUTHENTICATED access to a data…, _data(), Finding, _scanner(), Proven UNAUTHENTICATED access to a data…]
- "main_scripts_findings_rule_vnc": "_rule_vnc()" | kind=code-symbol | source=probe/main_scripts/findings.py:L861 | neighbors=[findings.py, VNC/RFB authentication exposure. 'None'…, _data(), Finding, _scanner(), VNC/RFB authentication exposure. 'None'…]
- "main_scripts_ftp_scanner": "ftp_scanner.py" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, banner_software(), FTPScanner, main(), parse_pasv(), ftp_scanner.py — FTP anonymous-access c…]
- "main_scripts_ftp_scanner_ftpscanner_list_bounded": "._list_bounded()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L128 | neighbors=[FTPScanner, ._cmd(), ._read_response(), parse_pasv(), ._probe(), Confirm anonymous READ via PASV + LIST,…]
- "main_scripts_ftp_scanner_ftpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ftp_scanner.py:L95 | neighbors=[FTPScanner, banner_software(), ._cmd(), ._list_bounded(), ._read_response(), Blocking: greeting → anonymous login → …]
- "main_scripts_ipmi_scanner": "ipmi_scanner.py" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, build_open_session_request(), IPMIScanner, main(), parse_open_session_response(), ipmi_scanner.py — IPMI 2.0 cipher-zero …]
- "main_scripts_ipmi_scanner_ipmiscanner": "IPMIScanner" | kind=code-symbol | source=probe/main_scripts/ipmi_scanner.py:L65 | neighbors=[ipmi_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_ipv6_discovery_discover_ipv6_hosts": "discover_ipv6_hosts()" | kind=code-symbol | source=probe/main_scripts/ipv6_discovery.py:L118 | neighbors=[ipv6_discovery.py, _own_ipv6_addresses(), _ping_all_nodes(), _read_neighbor_cache(), main(), Discover live IPv6 neighbors on the seg…]
- "main_scripts_ldap_scanner": "ldap_scanner.py" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _first(), LDAPScanner, main(), ldap_scanner.py — LDAP anonymous-bind e…]
- "main_scripts_ldap_scanner_ldapscanner": "LDAPScanner" | kind=code-symbol | source=probe/main_scripts/ldap_scanner.py:L47 | neighbors=[ldap_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_mass_scan_connectsweep": "_ConnectSweep" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L206 | neighbors=[mass_scan.py, BaseScanner, .__init__(), ._probe(), .scan_target(), run_mass_scan()]
- "main_scripts_msrpc_scanner_msrpcscanner": "MSRPCScanner" | kind=code-symbol | source=probe/main_scripts/msrpc_scanner.py:L82 | neighbors=[msrpc_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_os_fingerprint_icmp": "_icmp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L59 | neighbors=[os_fingerprint.py, build_icmp_addrmask(), build_icmp_echo(), build_icmp_timestamp(), Build an ICMP message (header + rest) w…, Build an ICMP message (header + rest) w…]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L337 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…, p0f-style match on (initial TTL, option…]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L436 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…, Send an ICMP timestamp request (type 13…]
- "main_scripts_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L175 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "main_scripts_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L267 | neighbors=[.scan_target(), Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…]
- "main_scripts_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L95 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), probe_rdp_posture(), One synchronous RDP handshake offering …, One synchronous RDP handshake. Best-eff…]
- "main_scripts_rdp_scanner_rdpscanner": "RDPScanner" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L135 | neighbors=[rdp_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), main()]
- "main_scripts_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L59 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log(), Run one scanner module as a subprocess,…, Run one scanner module as a subprocess,…]
- "main_scripts_scanner_base_sendpacer": "SendPacer" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L535 | neighbors=[scanner_base.py, Blocking packets-per-second pacer with …, .__init__(), .observe_round(), .pace(), .stats()]
- "main_scripts_scanner_registry": "scanner_registry.py" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, info(), is_verified(), ScannerInfo, verification_report(), scanner_registry.py — the single source…]
- "main_scripts_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L426 | neighbors=[ServiceBannerScanner, match_service(), parse_http_head(), ._ladder_for(), ._rung(), .scan_target()]
- "main_scripts_service_enum_serviceenumscanner": "ServiceEnumScanner" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L478 | neighbors=[service_enum.py, BaseScanner, .__init__(), ._open(), ._probe_port(), .scan_target()]
- "main_scripts_smb_enum_scanner_smbenumscanner": "SMBEnumScanner" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L218 | neighbors=[smb_enum_scanner.py, BaseScanner, ._enumerate(), .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L273 | neighbors=[smb_scanner.py, ntlm_os_build(), _align8(), _encryption_context(), _preauth_integrity_context(), .scan_target()]
- "main_scripts_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L362 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), ._ntlm_fingerprint(), .scan_target()]
- "main_scripts_smtp_scanner": "smtp_scanner.py" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, main(), parse_ehlo_capabilities(), SMTPScanner, vrfy_leaks(), smtp_scanner.py — SMTP hygiene: user en…]
- "main_scripts_smtp_scanner_smtpscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L87 | neighbors=[Blocking: greeting → EHLO → STARTTLS/VR…, SMTPScanner, parse_ehlo_capabilities(), ._cmd(), ._read_response(), vrfy_leaks()]
- "main_scripts_snmp_scanner_parse_varbinds": "_parse_varbinds()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L126 | neighbors=[snmp_scanner.py, _ber_parse(), _decode_oid(), Extract (oid_dotted, value_tag, value_b…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmpscanner_discover_community": "._discover_community()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L277 | neighbors=[Return (community, sysdescr) for the fi…, SNMPScanner, _build_get(), _decode_value(), _parse_varbinds(), ._udp()]
- "main_scripts_snmp_scanner_varbind_list": "_varbind_list()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L164 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len(), _varbind()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-045.json

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
