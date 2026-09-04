# Node Description Batch 78 of 332

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

- "scanner_printer_scanner_build_ipp_get_printer_attributes": "build_ipp_get_printer_attributes()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L54 | neighbors=[printer_scanner.py, _ipp_attr(), ._probe_ipp(), A minimal IPP/1.1 Get-Printer-Attribute…]
- "scanner_printer_scanner_printerscanner_probe_pjl": "._probe_pjl()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L103 | neighbors=[PrinterScanner, ._probe(), parse_pjl_id(), _recv_bounded()]
- "scanner_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L42 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…, TPKT + X.224 Connection Request carryin…]
- "scanner_rsync_scanner_recv_until": "_recv_until()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L57 | neighbors=[rsync_scanner.py, _handshake(), ._list_modules(), ._test_anon()]
- "scanner_rsync_scanner_rsyncscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L130 | neighbors=[Blocking: list modules, then anon-test …, RsyncScanner, ._list_modules(), ._test_anon()]
- "scanner_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L244 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel, Funnel many hosts with bounded concurre…, Funnel many hosts with bounded concurre…]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L977 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_project_now": "project_now()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L85 | neighbors=[scanner_base.py, project_file_stamp(), project_timestamp(), Current time as an AWARE datetime in th…]
- "scanner_scanner_base_raise_fd_limit": "raise_fd_limit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L1044 | neighbors=[scanner_base.py, get_fd_limit(), Raise the soft fd limit toward the hard…, safe_connect_concurrency()]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L311 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L404 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=probe/scanner/service_enum.py:L389 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target(), Descriptive role tags from the open-por…]
- "scanner_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=probe/scanner/service_enum.py:L155 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…, Decode a DNS name (with 0xC0 compressio…]
- "scanner_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=probe/scanner/service_enum.py:L133 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target(), Everything learned about one target bey…]
- "scanner_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=probe/scanner/service_enum.py:L340 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target(), Best-effort OS guess from voluntary evi…]
- "scanner_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=probe/scanner/service_enum.py:L424 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …, Directly-connected subnets and default …]
- "scanner_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=probe/scanner/service_enum.py:L176 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …, Ask the host over multicast DNS (5353) …]
- "scanner_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=probe/scanner/service_enum.py:L203 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…, NetBIOS first-level name encoding (16-b…]
- "scanner_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=probe/scanner/service_enum.py:L213 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…, NBNS node-status (NBSTAT) query to UDP/…]
- "scanner_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=probe/scanner/service_enum.py:L244 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target(), Run the three name sources concurrently…]
- "scanner_smb_enum_scanner_enum_shares": "_enum_shares()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L87 | neighbors=[smb_enum_scanner.py, _decode(), List SMB shares over the null session. …, ._enumerate()]
- "scanner_smb_enum_scanner_enum_users_ridcycle": "_enum_users_ridcycle()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L148 | neighbors=[smb_enum_scanner.py, _decode(), RID-cycling fallback via LSAT: resolve …, ._enumerate()]
- "scanner_smb_enum_scanner_enum_users_samr": "_enum_users_samr()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L102 | neighbors=[smb_enum_scanner.py, _decode(), Enumerate domain/local users via the SA…, ._enumerate()]
- "scanner_smb_scanner_parse_ntlm_challenge": "parse_ntlm_challenge()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L176 | neighbors=[smb_scanner.py, ntlm_os_build(), windows_release_from_build(), Parse an NTLMSSP CHALLENGE (Type-2) out…]
- "scanner_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L38 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target(), Read signing posture from a SUCCESSFUL …]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L403 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_smb_scanner_spnego_init": "_spnego_init()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L133 | neighbors=[smb_scanner.py, ntlm_os_build(), Wrap an NTLMSSP Type-1 in a minimal SPN…, _der()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_ssh_scanner_evaluate_algorithms": "evaluate_algorithms()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L133 | neighbors=[ssh_scanner.py, _dedup(), Grade a server's offered algorithms aga…, ._scan_port()]
- "scanner_ssh_scanner_read_packet": "_read_packet()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L225 | neighbors=[ssh_scanner.py, Read one unencrypted SSH binary packet …, _recv_exact(), ._probe()]
- "scanner_ssh_scanner_sshscanner_probe": "._probe()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L249 | neighbors=[Blocking: connect, exchange identificat…, SSHScanner, _read_ident(), _read_packet()]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L130 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_parse_tcp_options": "parse_tcp_options()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L137 | neighbors=[syn_scanner.py, _parse_mss(), parse_packet(), Walk a TCP options field into a p0f-sty…]
- "scanner_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync(), Flag the security-relevant properties o…]
- "scanner_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync(), Grade overall TLS posture A/B/C/F from …]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-077.json

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
