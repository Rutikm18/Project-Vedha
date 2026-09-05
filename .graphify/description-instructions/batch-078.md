# Node Description Batch 79 of 336

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

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
- "scanner_udp_scanner_interpret_ipmi": "interpret_ipmi()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L219 | neighbors=[udp_scanner.py, Parse RMCP Pong; extract supported enti…, ._probe(), Parse RMCP Pong; extract supported enti…]
- "scanner_udp_scanner_interpret_mdns": "interpret_mdns()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L247 | neighbors=[udp_scanner.py, Return byte count and check QR bit (1 =…, ._probe(), Return byte count and check QR bit (1 =…]
- "scanner_udp_scanner_interpret_sip": "interpret_sip()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L204 | neighbors=[udp_scanner.py, Extract SIP version + server header fro…, ._probe(), Extract SIP version + server header fro…]
- "scanner_udp_scanner_interpret_ssdp": "interpret_ssdp()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L232 | neighbors=[udp_scanner.py, Extract Location and Server from SSDP r…, ._probe(), Extract Location and Server from SSDP r…]
- "scanner_unauth_access": "unauth_access.py" | kind=code-symbol | source=probe/scanner/unauth_access.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _as_text(), classify_unauth_access(), is_rce_capable()]
- "scanner_va_campaign_default_stages": "default_stages()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L390 | neighbors=[va_campaign.py, build_campaign(), Stage, Build the real capability stages from a…]
- "scanner_va_campaign_now": "_now()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L61 | neighbors=[va_campaign.py, .__init__(), .mark(), .snapshot()]
- "scanner_va_campaign_progressreporter_mark": ".mark()" | kind=code-symbol | source=probe/scanner/va_campaign.py:L202 | neighbors=[ProgressReporter, _now(), ._flush(), .run()]
- "scanner_vantage_matrix_reconcile_vantages": "reconcile_vantages()" | kind=code-symbol | source=probe/scanner/vantage_matrix.py:L49 | neighbors=[vantage_matrix.py, Compare per-vantage observations of one…, _extract(), _is_external()]
- "scanner_vnc_scanner_read_security_types": "_read_security_types()" | kind=code-symbol | source=probe/scanner/vnc_scanner.py:L81 | neighbors=[vnc_scanner.py, Read the offered security types, handli…, _recv_exact(), ._probe()]
- "scanner_web_scanner_parse_allow_header": "parse_allow_header()" | kind=code-symbol | source=probe/scanner/web_scanner.py:L45 | neighbors=[web_scanner.py, _fetch(), Read the Allow header from an OPTIONS r…, Read the Allow header from an OPTIONS r…]
- "schemas_asset_assetout": "AssetOut" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L34 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_asset_bulkassetimportresult": "BulkAssetImportResult" | kind=code-symbol | source=manager/backend/app/schemas/asset.py:L54 | neighbors=[asset.py, BaseModel, AssetCriticality, AssetType]
- "schemas_engagement_engagementdetail": "EngagementDetail" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L108 | neighbors=[engagement.py, EngagementOut, EngagementStatus, FindingSeverity]
- "schemas_engagement_engagementfilter": "EngagementFilter" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L71 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L81 | neighbors=[engagement.py, BaseModel, EngagementStatus, FindingSeverity]
- "schemas_engagement_validate_scope_entries": "validate_scope_entries()" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L12 | neighbors=[engagement.py, .validate_scopes(), Validate and de-duplicate exact IP/CIDR…, Validate and de-duplicate exact IP/CIDR…]
- "schemas_finding_rationale_21": "All fields optional — PATCH semantics." | kind=entity | source=manager/backend/app/schemas/finding.py:L21 | neighbors=[FindingPatch, DetectionStatus, FindingSeverity, FindingStatus]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-078.json

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
