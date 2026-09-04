# Node Description Batch 74 of 330

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

- "main_scripts_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L133 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target(), Everything learned about one target bey…]
- "main_scripts_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L340 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target(), Best-effort OS guess from voluntary evi…]
- "main_scripts_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L424 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …, Directly-connected subnets and default …]
- "main_scripts_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L176 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …, Ask the host over multicast DNS (5353) …]
- "main_scripts_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L203 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…, NetBIOS first-level name encoding (16-b…]
- "main_scripts_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L213 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…, NBNS node-status (NBSTAT) query to UDP/…]
- "main_scripts_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L244 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target(), Run the three name sources concurrently…]
- "main_scripts_smb_enum_scanner_enum_shares": "_enum_shares()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L87 | neighbors=[smb_enum_scanner.py, _decode(), List SMB shares over the null session. …, ._enumerate()]
- "main_scripts_smb_enum_scanner_enum_users_ridcycle": "_enum_users_ridcycle()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L148 | neighbors=[smb_enum_scanner.py, _decode(), RID-cycling fallback via LSAT: resolve …, ._enumerate()]
- "main_scripts_smb_enum_scanner_enum_users_samr": "_enum_users_samr()" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L102 | neighbors=[smb_enum_scanner.py, _decode(), Enumerate domain/local users via the SA…, ._enumerate()]
- "main_scripts_smb_scanner_parse_ntlm_challenge": "parse_ntlm_challenge()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L176 | neighbors=[smb_scanner.py, ntlm_os_build(), windows_release_from_build(), Parse an NTLMSSP CHALLENGE (Type-2) out…]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L38 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target(), Read signing posture from a SUCCESSFUL …]
- "main_scripts_smb_scanner_smbscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L403 | neighbors=[SMBScanner, parse_smb2_security_mode(), _smb1_negotiate(), _smb2_negotiate()]
- "main_scripts_smb_scanner_spnego_init": "_spnego_init()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L133 | neighbors=[smb_scanner.py, ntlm_os_build(), Wrap an NTLMSSP Type-1 in a minimal SPN…, _der()]
- "main_scripts_snmp_scanner_decode_oid": "_decode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L63 | neighbors=[snmp_scanner.py, _decode_value(), _parse_varbinds(), BER-encoded OID bytes → dotted-notation…]
- "main_scripts_snmp_scanner_encode_oid": "_encode_oid()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L45 | neighbors=[snmp_scanner.py, Dotted-notation OID string → BER-encode…, ._amplification_factor(), ._walk_subtree()]
- "main_scripts_snmp_scanner_req_id_tlv": "_req_id_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L178 | neighbors=[snmp_scanner.py, _build_get(), _build_getbulk_v2c(), _build_getnext()]
- "main_scripts_snmp_scanner_varbind": "_varbind()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L159 | neighbors=[snmp_scanner.py, _ber_len(), _oid_tlv(), _varbind_list()]
- "main_scripts_ssh_collector_sshcollector": "SSHCollector" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L80 | neighbors=[ssh_collector.py, ._collect(), .__init__(), .run()]
- "main_scripts_ssh_scanner_evaluate_algorithms": "evaluate_algorithms()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L133 | neighbors=[ssh_scanner.py, _dedup(), Grade a server's offered algorithms aga…, ._scan_port()]
- "main_scripts_ssh_scanner_read_packet": "_read_packet()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L225 | neighbors=[ssh_scanner.py, Read one unencrypted SSH binary packet …, _recv_exact(), ._probe()]
- "main_scripts_ssh_scanner_sshscanner_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/ssh_scanner.py:L249 | neighbors=[Blocking: connect, exchange identificat…, SSHScanner, _read_ident(), _read_packet()]
- "main_scripts_syn_scanner_build_syn_packet": "build_syn_packet()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L130 | neighbors=[syn_scanner.py, build_ip_header(), build_tcp_syn(), ._syn_scan_blocking()]
- "main_scripts_syn_scanner_parse_tcp_options": "parse_tcp_options()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L137 | neighbors=[syn_scanner.py, _parse_mss(), parse_packet(), Walk a TCP options field into a p0f-sty…]
- "main_scripts_tls_scanner_sni": "_sni()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L146 | neighbors=[tls_scanner.py, _get_cert_der(), Never send an IP literal as SNI — non-c…, _try_version()]
- "main_scripts_udp_scanner_interpret_ike": "interpret_ike()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L188 | neighbors=[udp_scanner.py, Parse IKEv1 or IKEv2 response header., ._probe(), Parse IKEv1 or IKEv2 response header.]
- "main_scripts_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe(), Parse RMCP Pong; extract supported enti…]
- "main_scripts_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe(), Return byte count and check QR bit (1 =…]
- "main_scripts_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe(), Extract SIP version + server header fro…]
- "main_scripts_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe(), Extract Location and Server from SSDP r…]
- "main_scripts_va_campaign_default_stages": "default_stages()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L390 | neighbors=[va_campaign.py, build_campaign(), Stage, Build the real capability stages from a…]
- "main_scripts_va_campaign_now": "_now()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L61 | neighbors=[va_campaign.py, .__init__(), .mark(), .snapshot()]
- "main_scripts_va_campaign_progressreporter_mark": ".mark()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L202 | neighbors=[ProgressReporter, _now(), ._flush(), .run()]
- "main_scripts_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "main_scripts_vnc_scanner_read_security_types": "_read_security_types()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L81 | neighbors=[vnc_scanner.py, Read the offered security types, handli…, _recv_exact(), ._probe()]
- "main_scripts_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/models/engagement.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, Engagement, 298a9d4 trim frontend to 7 core pages; …]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-073.json

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
