# Node Description Batch 46 of 330

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
- "main_scripts_ssh_scanner_parse_kexinit": "parse_kexinit()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L106 | neighbors=[ssh_scanner.py, _Cursor, .read(), .read_name_list(), Parse a SSH_MSG_KEXINIT body into its n…, ._scan_port()]
- "main_scripts_ssh_scanner_sshscanner": "SSHScanner" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L242 | neighbors=[ssh_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_ssh_scanner_sshscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L279 | neighbors=[SSHScanner, _dedup(), evaluate_algorithms(), parse_kexinit(), parse_ssh_banner(), .scan_target()]
- "main_scripts_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L91 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "main_scripts_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L115 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "main_scripts_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L213 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…]
- "main_scripts_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L295 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), A genuine reply to our SYN acknowledges…, Outbound-interface IP for reaching dst_…, Outbound-interface IP for reaching dst_…]
- "main_scripts_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L176 | neighbors=[syn_scanner.py, parse_tcp_options(), Back-compat shim: MSS only. New code us…, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "main_scripts_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L273 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…, True only when a real SYN scan can work…, True only when a real SYN scan can work…]
- "main_scripts_tls_scanner_scan_tls_sync": "_scan_tls_sync()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L274 | neighbors=[tls_scanner.py, classify_cipher(), _get_cert_der(), grade_tls_posture(), _parse_cert_der(), _try_version()]
- "main_scripts_udp_scanner_udpscanner": "UDPScanner" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L282 | neighbors=[udp_scanner.py, BaseScanner, ._gated_probe(), .__init__(), ._probe(), .scan_target()]
- "main_scripts_va_campaign_vacampaign": "VACampaign" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L290 | neighbors=[va_campaign.py, build_campaign(), Runs the ordered stages sequentially, e…, .__init__(), ._refresh_totals(), .run()]
- "main_scripts_va_campaign_vacampaign_run": ".run()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L301 | neighbors=[run_campaign(), VACampaign, .finish(), .mark(), .snapshot(), ._refresh_totals()]
- "main_scripts_vantage_matrix": "vantage_matrix.py" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _extract(), _is_external(), reconcile_vantages(), vantage_matrix.py — reconcile the SAME …, test_main_scripts_vantage.py]
- "main_scripts_vnc_scanner_vncscanner": "VNCScanner" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L101 | neighbors=[vnc_scanner.py, BaseScanner, .__init__(), ._probe(), ._scan_port(), .scan_target()]
- "main_scripts_vnc_scanner_vncscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L108 | neighbors=[Blocking: RFB version handshake + read …, VNCScanner, classify_security_types(), parse_rfb_version(), _read_security_types(), _recv_exact()]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target(), ._schemes_for()]
- "main_scripts_windows_collector": "windows_collector.py" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, main(), _smb_registry_collect(), WindowsCollector, _winrm_collect(), windows_collector.py — credentialed (au…]
- "main_scripts_windows_collector_windowscollector_collect_host": "._collect_host()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L255 | neighbors=[WindowsCollector, ._full_user(), ._smb_result(), ._transport_order(), ._winrm_result(), .run()]
- "reveal_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "routers_activity_activityitem": "ActivityItem" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L31 | neighbors=[activity.py, BaseModel, recent_activity(), Engagement, Finding, ScanJob]

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
