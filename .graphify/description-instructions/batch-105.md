# Node Description Batch 106 of 332

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

- "scanner_service_banner_servicebannerscanner_read_some": "._read_some()" | kind=code-symbol | source=probe/scanner/service_banner.py:L348 | neighbors=[Read up to read_bytes: wait `first_wait…, ServiceBannerScanner, ._rung()]
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/scanner/service_enum.py:L322 | neighbors=[service_enum.py, Negotiate against 445; report whether S…, Negotiate against 445; report whether S…]
- "scanner_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=probe/scanner/service_enum.py:L287 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…, Which deprecated TLS/SSL versions the s…]
- "scanner_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=probe/scanner/service_enum.py:L264 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…, One permissive TLS handshake: negotiate…]
- "scanner_smb_enum_scanner_merge_users": "_merge_users()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L200 | neighbors=[smb_enum_scanner.py, Merge user lists, de-duplicated by (nam…, ._enumerate()]
- "scanner_smb_enum_scanner_parse_rid_ranges": "parse_rid_ranges()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L52 | neighbors=[smb_enum_scanner.py, Parse 'a-b,c-d,e' into a sorted, de-dup…, .__init__()]
- "scanner_smb_enum_scanner_safe": "_safe()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L300 | neighbors=[smb_enum_scanner.py, _decode(), ._enumerate()]
- "scanner_smb_scanner_align8": "_align8()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L249 | neighbors=[smb_scanner.py, Pad to the 8-byte boundary MS-SMB2 requ…, _smb2_negotiate()]
- "scanner_smb_scanner_build_ntlmssp_negotiate": "build_ntlmssp_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L115 | neighbors=[smb_scanner.py, ntlm_os_build(), NTLMSSP NEGOTIATE (Type-1). Sets NEGOTI…]
- "scanner_smb_scanner_der": "_der()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L111 | neighbors=[smb_scanner.py, _der_len(), _spnego_init()]
- "scanner_smb_scanner_encryption_context": "_encryption_context()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L265 | neighbors=[smb_scanner.py, SMB2_ENCRYPTION_CAPABILITIES (MS-SMB2 2…, _smb2_negotiate()]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L33 | neighbors=[smb_scanner.py, ntlm_os_build(), ._negotiate()]
- "scanner_smb_scanner_preauth_integrity_context": "_preauth_integrity_context()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L254 | neighbors=[smb_scanner.py, SMB2_PREAUTH_INTEGRITY_CAPABILITIES (MS…, _smb2_negotiate()]
- "scanner_smb_scanner_recv_smb_frame": "_recv_smb_frame()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L316 | neighbors=[smb_scanner.py, ntlm_os_build(), Read one length-prefixed (Direct-TCP/NB…]
- "scanner_smb_scanner_smb2_session_setup": "_smb2_session_setup()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L203 | neighbors=[smb_scanner.py, ntlm_os_build(), SMB2 SESSION_SETUP request (MessageId 1…]
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L369 | neighbors=[SMB negotiate against the first address…, SMBScanner, _netbios_session()]
- "scanner_smb_scanner_smbscanner_ntlm_fingerprint": "._ntlm_fingerprint()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L393 | neighbors=[Best-effort: SMB2 NEGOTIATE then a pre-…, SMBScanner, ntlm_os_build()]
- "scanner_smb_scanner_windows_release_from_build": "windows_release_from_build()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L141 | neighbors=[smb_scanner.py, parse_ntlm_challenge(), Map an NT major.minor.build to a friend…]
- "scanner_smtp_scanner_parse_ehlo_capabilities": "parse_ehlo_capabilities()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L39 | neighbors=[smtp_scanner.py, Extract EHLO capability tokens from a m…, ._probe()]
- "scanner_smtp_scanner_smtpscanner_cmd": "._cmd()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L83 | neighbors=[SMTPScanner, ._read_response(), ._probe()]
- "scanner_smtp_scanner_smtpscanner_read_response": "._read_response()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L67 | neighbors=[SMTPScanner, ._cmd(), ._probe()]
- "scanner_smtp_scanner_vrfy_leaks": "vrfy_leaks()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L51 | neighbors=[smtp_scanner.py, VRFY leaks usernames when it gives DIFF…, ._probe()]
- "scanner_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "scanner_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "scanner_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "scanner_ssh_kexdb": "ssh_kexdb.py" | kind=code-symbol | source=probe/scanner/ssh_kexdb.py:L1 | neighbors=[6e2818f Add support for additional serv…, lookup(), ssh_kexdb.py — vendored SSH algorithm w…]
- "scanner_ssh_scanner_cursor_read": ".read()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L77 | neighbors=[_Cursor, .read_name_list(), parse_kexinit()]
- "scanner_ssh_scanner_cursor_read_name_list": ".read_name_list()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L84 | neighbors=[_Cursor, .read(), parse_kexinit()]
- "scanner_ssh_scanner_dedup": "_dedup()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L124 | neighbors=[ssh_scanner.py, evaluate_algorithms(), ._scan_port()]
- "scanner_ssh_scanner_parse_ssh_banner": "parse_ssh_banner()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L46 | neighbors=[ssh_scanner.py, Parse an SSH identification string 'SSH…, ._scan_port()]
- "scanner_ssh_scanner_read_ident": "_read_ident()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L194 | neighbors=[ssh_scanner.py, Read the server SSH identification line…, ._probe()]
- "scanner_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L356 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "scanner_syn_scanner_wait_readable": "_wait_readable()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L243 | neighbors=[syn_scanner.py, Block until `sock` has a packet waiting…, ._syn_scan_blocking()]
- "scanner_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L79 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L67 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L74 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "scanner_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L203 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "scanner_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…, RMCP Ping (ASF Presence Ping) to detect…]
- "scanner_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…, mDNS PTR query for _services._dns-sd._u…]
- "scanner_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-105.json

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
