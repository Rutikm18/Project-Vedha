# Node Description Batch 101 of 336

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

- "main_scripts_smtp_scanner_smtpscanner_read_response": "._read_response()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L67 | neighbors=[SMTPScanner, ._cmd(), ._probe()]
- "main_scripts_smtp_scanner_vrfy_leaks": "vrfy_leaks()" | kind=code-symbol | source=probe/main_scripts/smtp_scanner.py:L51 | neighbors=[smtp_scanner.py, VRFY leaks usernames when it gives DIFF…, ._probe()]
- "main_scripts_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "main_scripts_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "main_scripts_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "main_scripts_ssh_kexdb": "ssh_kexdb.py" | kind=code-symbol | source=probe/main_scripts/ssh_kexdb.py:L1 | neighbors=[6e2818f Add support for additional serv…, lookup(), ssh_kexdb.py — vendored SSH algorithm w…]
- "main_scripts_ssh_scanner_cursor_read": ".read()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L77 | neighbors=[_Cursor, .read_name_list(), parse_kexinit()]
- "main_scripts_ssh_scanner_cursor_read_name_list": ".read_name_list()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L84 | neighbors=[_Cursor, .read(), parse_kexinit()]
- "main_scripts_ssh_scanner_dedup": "_dedup()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L124 | neighbors=[ssh_scanner.py, evaluate_algorithms(), ._scan_port()]
- "main_scripts_ssh_scanner_parse_ssh_banner": "parse_ssh_banner()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L46 | neighbors=[ssh_scanner.py, Parse an SSH identification string 'SSH…, ._scan_port()]
- "main_scripts_ssh_scanner_read_ident": "_read_ident()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L194 | neighbors=[ssh_scanner.py, Read the server SSH identification line…, ._probe()]
- "main_scripts_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L356 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "main_scripts_syn_scanner_wait_readable": "_wait_readable()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L243 | neighbors=[syn_scanner.py, Block until `sock` has a packet waiting…, ._syn_scan_blocking()]
- "main_scripts_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L79 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L67 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L74 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "main_scripts_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L203 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "main_scripts_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "main_scripts_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…, RMCP Ping (ASF Presence Ping) to detect…]
- "main_scripts_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…, mDNS PTR query for _services._dns-sd._u…]
- "main_scripts_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "main_scripts_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…, UPnP/SSDP M-SEARCH — unicast to target:…]
- "main_scripts_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "main_scripts_va_campaign_campaigncontext": "CampaignContext" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L138 | neighbors=[va_campaign.py, build_campaign(), Mutable state threaded through the stag…]
- "main_scripts_va_campaign_cliprogressview_call": ".__call__()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L663 | neighbors=[CliProgressView, ._redraw(), ._transitions()]
- "main_scripts_va_campaign_cliprogressview_redraw": "._redraw()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L669 | neighbors=[CliProgressView, .__call__(), ._format()]
- "main_scripts_va_campaign_monotonic": "_monotonic()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L276 | neighbors=[va_campaign.py, ._eta_seconds(), .__init__()]
- "main_scripts_va_campaign_progressreporter_eta_seconds": "._eta_seconds()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L236 | neighbors=[ProgressReporter, _monotonic(), .snapshot()]
- "main_scripts_va_campaign_progressreporter_finish": ".finish()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L217 | neighbors=[ProgressReporter, ._flush(), .run()]
- "main_scripts_va_campaign_progressreporter_set_totals": ".set_totals()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L213 | neighbors=[ProgressReporter, ._flush(), ._refresh_totals()]
- "main_scripts_va_campaign_run_campaign": "run_campaign()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L639 | neighbors=[va_campaign.py, build_campaign(), .run()]
- "main_scripts_va_campaign_stagestate": "StageState" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L151 | neighbors=[va_campaign.py, .__init__(), .to_dict()]
- "main_scripts_va_campaign_vacampaign_refresh_totals": "._refresh_totals()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L322 | neighbors=[VACampaign, .set_totals(), .run()]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "main_scripts_vnc_scanner_classify_security_types": "classify_security_types()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L60 | neighbors=[vnc_scanner.py, Turn a list of offered security-type id…, ._probe()]
- "main_scripts_vnc_scanner_parse_rfb_version": "parse_rfb_version()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L46 | neighbors=[vnc_scanner.py, Parse a 'RFB 003.008' banner into (majo…, ._probe()]
- "main_scripts_vnc_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L71 | neighbors=[vnc_scanner.py, _read_security_types(), ._probe()]
- "main_scripts_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L155 | neighbors=[WebScanner, ._schemes_for(), .scan_target()]
- "main_scripts_web_scanner_webscanner_schemes_for": "._schemes_for()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L148 | neighbors=[Preferred scheme first, the other as a …, WebScanner, ._scan_port()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-100.json

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
