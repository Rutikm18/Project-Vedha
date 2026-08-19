# Node Description Batch 42 of 227

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

- "main_scripts_iot_scanner_parse_mdns_response": "_parse_mdns_response()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L156 | neighbors=[iot_scanner.py, _decode_mdns_name(), _probe_mdns_sync(), Extract PTR target names from mDNS resp…, Extract PTR target names from mDNS resp…]
- "main_scripts_ja4s_ja4s_from_fields": "ja4s_from_fields()" | kind=code-symbol | source=probe/main_scripts/ja4s.py:L85 | neighbors=[ja4s.py, _alpn_code(), _version_str(), ja4s_from_parsed(), Pure JA4S from already-extracted Server…]
- "main_scripts_mobile_scanner_probe_adb": "_probe_adb()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L94 | neighbors=[mobile_scanner.py, .scan_target(), _build_adb_cnxn(), _parse_adb_header(), Send ADB CNXN and read the device's CNX…]
- "main_scripts_os_fingerprint_open_icmp_socket": "_open_icmp_socket()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L270 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), ._icmp_timestamp(), Return (socket, is_raw). Prefer datagra…, Return (socket, is_raw). Prefer datagra…]
- "main_scripts_os_fingerprint_osfingerprintscanner_icmp_timestamp": "._icmp_timestamp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L329 | neighbors=[OSFingerprintScanner, build_icmp_timestamp(), _open_icmp_socket(), parse_icmp_timestamps(), Send an ICMP timestamp request (type 13…]
- "main_scripts_os_fingerprint_parse_icmp_reply": "parse_icmp_reply()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L94 | neighbors=[os_fingerprint.py, ._icmp_echo_ttl(), _strip_ip_header(), Parse an ICMP reply. Handles both raw-s…, Parse an ICMP reply. Handles both raw-s…]
- "main_scripts_passive_collector_passivecollector": "PassiveCollector" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L210 | neighbors=[passive_collector.py, .__init__(), .run(), ._select(), Listen-only discovery. No active probin…]
- "main_scripts_passive_collector_passivelistenererror": "PassiveListenerError" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L106 | neighbors=[passive_collector.py, .run(), .__init__(), RuntimeError, All passive sources failed before the l…]
- "main_scripts_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L92 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…, Return 'ipv4'/'ipv6' for an IP literal,…]
- "main_scripts_scanner_base_basescanner_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L768 | neighbors=[BaseScanner, .wait(), .write(), main_entrypoint(), run_cli()]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L131 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab(), One probe-ladder rung on its own connec…, One probe-ladder rung on its own connec…]
- "main_scripts_smb_scanner_smbscanner": "SMBScanner" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L142 | neighbors=[smb_scanner.py, BaseScanner, .__init__(), ._negotiate(), .scan_target()]
- "main_scripts_snmp_scanner_ber_len": "_ber_len()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L37 | neighbors=[snmp_scanner.py, _oid_tlv(), _snmp_msg(), _varbind(), _varbind_list()]
- "main_scripts_snmp_scanner_build_get": "_build_get()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L183 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._discover_community()]
- "main_scripts_snmp_scanner_build_getbulk_v2c": "_build_getbulk_v2c()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L195 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._amplification_factor()]
- "main_scripts_snmp_scanner_build_getnext": "_build_getnext()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L189 | neighbors=[snmp_scanner.py, _req_id_tlv(), _snmp_msg(), _varbind_list(), ._walk_subtree()]
- "main_scripts_snmp_scanner_decode_value": "_decode_value()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L78 | neighbors=[snmp_scanner.py, _decode_oid(), Human-readable SNMP value for common AS…, ._discover_community(), ._walk_subtree()]
- "main_scripts_snmp_scanner_snmp_msg": "_snmp_msg()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L169 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext(), _ber_len()]
- "main_scripts_snmp_scanner_snmpscanner_amplification_factor": "._amplification_factor()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L314 | neighbors=[One GETBULK request — measure response/…, SNMPScanner, _build_getbulk_v2c(), _encode_oid(), ._udp()]
- "main_scripts_snmp_scanner_snmpscanner_udp": "._udp()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L260 | neighbors=[SNMPScanner, ._amplification_factor(), ._discover_community(), ._snmpv3_present(), ._walk_subtree()]
- "main_scripts_ssh_collector": "ssh_collector.py" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _collect_over_ssh(), main(), SSHCollector, ssh_collector.py — credentialed (authen…]
- "main_scripts_syn_scanner_build_ip_header": "build_ip_header()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L79 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…, Build a 20-byte IPv4 header with a vali…]
- "main_scripts_syn_scanner_build_tcp_syn": "build_tcp_syn()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L103 | neighbors=[syn_scanner.py, build_syn_packet(), Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …, Build a 20-byte TCP SYN segment with a …]
- "main_scripts_syn_scanner_classify": "classify()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L179 | neighbors=[syn_scanner.py, SYN/ACK -> open, RST -> closed, anythin…, ._syn_scan_blocking(), SYN/ACK -> open, RST -> closed, anythin…, SYN/ACK -> open, RST -> closed, anythin…]
- "main_scripts_syn_scanner_local_source_ip": "_local_source_ip()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L231 | neighbors=[syn_scanner.py, Outbound-interface IP for reaching dst_…, ._syn_scan_blocking(), Outbound-interface IP for reaching dst_…, Outbound-interface IP for reaching dst_…]
- "main_scripts_syn_scanner_syn_scan_supported": "syn_scan_supported()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L209 | neighbors=[syn_scanner.py, True only when a real SYN scan can work…, .__init__(), True only when a real SYN scan can work…, True only when a real SYN scan can work…]
- "main_scripts_tls_fingerprint_ext": "_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L62 | neighbors=[tls_fingerprint.py, build_client_hello(), _key_share_ext(), _sni_extension(), _supported_versions_ext()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner": "TLSFingerprintScanner" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L282 | neighbors=[tls_fingerprint.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_tls_scanner_tlsscanner": "TLSScanner" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L255 | neighbors=[tls_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "main_scripts_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable(), test_main_scripts_unauth.py]
- "main_scripts_web_scanner_webscanner": "WebScanner" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L136 | neighbors=[web_scanner.py, BaseScanner, .__init__(), ._scan_port(), .scan_target()]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_base": "base.py" | kind=code-symbol | source=manager/backend/app/models/base.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Base, TimestampMixin, UUIDMixin, 298a9d4 trim frontend to 7 core pages; …]
- "models_exploit_approval": "exploit_approval.py" | kind=code-symbol | source=manager/backend/app/models/exploit_approval.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Enum, ApprovalStatus, ExploitApprovalRequest, 298a9d4 trim frontend to 7 core pages; …]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 6be8259 feat(integrations): outbox deli…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_probe_enrollment": "probe_enrollment.py" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, AgentCredential, ProbeEnrollmentRequest, ProbeEnrollmentToken]
- "models_scan_request": "scan_request.py" | kind=code-symbol | source=manager/backend/app/models/scan_request.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 35f02a9 feat(portal): rich scan request…, c7f226f chore: bundle pending working-t…, ScanRequest, scan_request.py — a customer-initiated,…]
- "path_route_proxy": "proxy()" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L17 | neighbors=[route.ts, GET(), PATCH(), POST(), portalToken()]
- "pathid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/attack-paths/[pathId]/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, graphStore, GET(), 298a9d4 trim frontend to 7 core pages; …, graph-store.ts]
- "portscan_portscanner_attempt": "._attempt()" | kind=code-symbol | source=portscan.py:L145 | neighbors=[PortScanner, classify_os_error(), family_of(), ._record(), .scan_port()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-041.json

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
