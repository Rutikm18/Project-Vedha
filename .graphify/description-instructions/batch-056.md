# Node Description Batch 57 of 227

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

- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L184 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics, Tally exactly one terminal per-port obs…, Tally exactly one terminal per-port obs…]
- "scanner_rdp_scanner_probe_rdp": "probe_rdp()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L83 | neighbors=[rdp_scanner.py, build_connection_request(), parse_connection_confirm(), One synchronous RDP handshake. Best-eff…]
- "scanner_run_all_run_stage": "_run_stage()" | kind=code-symbol | source=probe/scanner/run_all.py:L45 | neighbors=[run_all.py, main(), Run one scanner module as a subprocess,…, _log()]
- "scanner_scanner_base_basescanner_guarded": "._guarded()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L756 | neighbors=[BaseScanner, .scan_target(), ScanResult, .assert_in_scope()]
- "scanner_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L169 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …, Map a connect()/socket-time OSError to …]
- "scanner_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L185 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…, Full, debuggable classification for att…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L384 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "scanner_scanner_base_scopeerror": "ScopeError" | kind=code-symbol | source=probe/scanner/scanner_base.py:L247 | neighbors=[scanner_base.py, Exception, .assert_in_scope(), .from_file()]
- "scanner_scanner_base_scopeguard_assert_in_scope": ".assert_in_scope()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L340 | neighbors=[._guarded(), ScopeGuard, ScopeError, .in_scope()]
- "scanner_service_banner_servicebannerscanner_grab": "._grab()" | kind=code-symbol | source=probe/scanner/service_banner.py:L173 | neighbors=[ServiceBannerScanner, match_service(), ._rung(), .scan_target()]
- "scanner_service_enum_serviceenumscanner_probe_port": "._probe_port()" | kind=code-symbol | source=probe/scanner/service_enum.py:L465 | neighbors=[Connect to one port and read whatever i…, ServiceEnumScanner, ._open(), .scan_target()]
- "scanner_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L165 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "scanner_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "scanner_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "scanner_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "scanner_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "scanner_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "scanner_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L118 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "scanner_syn_scanner_parse_mss": "_parse_mss()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L125 | neighbors=[syn_scanner.py, parse_packet(), Walk a TCP options field for the MSS va…, Walk a TCP options field for the MSS va…]
- "scanner_syn_scanner_synscanner_build_results": "._build_results()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L415 | neighbors=[Turn resolved port states + harvested i…, SynScanner, ._syn_scan_blocking(), Turn resolved port states + harvested i…]
- "scanner_tls_fingerprint_cipher_code": "cipher_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L177 | neighbors=[tls_fingerprint.py, jarm_style_digest(), 2-char code from the cipher's position …, 2-char code from the cipher's position …]
- "scanner_tls_fingerprint_parse_server_hello": "parse_server_hello()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L136 | neighbors=[tls_fingerprint.py, _one_probe(), Parse the negotiated version + cipher +…, Parse the negotiated version + cipher +…]
- "scanner_tls_fingerprint_recv_first_record": "_recv_first_record()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L241 | neighbors=[tls_fingerprint.py, _one_probe(), Read exactly the first TLS record (the …, Read exactly the first TLS record (the …]
- "scanner_tls_fingerprint_server_ext_types": "_server_ext_types()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L184 | neighbors=[tls_fingerprint.py, jarm_style_digest(), Concatenate the ServerHello extension T…, Concatenate the ServerHello extension T…]
- "scanner_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync(), Flag the security-relevant properties o…]
- "scanner_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync(), Grade overall TLS posture A/B/C/F from …]
- "scanner_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]
- "scanner_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe(), Parse RMCP Pong; extract supported enti…]
- "scanner_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe(), Return byte count and check QR bit (1 =…]
- "scanner_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe(), Extract SIP version + server header fro…]
- "scanner_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe(), Extract Location and Server from SSDP r…]
- "scanner_udp_scanner_udpscanner_gated_probe": "._gated_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L290 | neighbors=[Acquire the concurrency gate (adaptive …, UDPScanner, ._probe(), Acquire the concurrency gate (adaptive …]
- "scanner_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/scanner/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable()]
- "scanner_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L108 | neighbors=[engagement.py, EngagementOut, EngagementStatus, FindingSeverity]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L71 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L81 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-056.json

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
