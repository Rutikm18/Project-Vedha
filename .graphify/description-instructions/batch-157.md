# Node Description Batch 158 of 227

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

- "main_scripts_scanner_base_scanresult_post_init": ".__post_init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L231 | neighbors=[ScanResult]
- "main_scripts_scanner_base_scopeguard_from_list": ".from_list()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L299 | neighbors=[ScopeGuard]
- "main_scripts_scanner_base_scopeguard_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L263 | neighbors=[ScopeGuard]
- "main_scripts_scanner_base_setup_logging": "setup_logging()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L828 | neighbors=[scanner_base.py]
- "main_scripts_scanner_base_udpprobeprotocol_connection_lost": ".connection_lost()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L591 | neighbors=[_UDPProbeProtocol]
- "main_scripts_scanner_base_udpprobeprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L577 | neighbors=[_UDPProbeProtocol]
- "main_scripts_scanner_base_udpprobeprotocol_error_received": ".error_received()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L581 | neighbors=[_UDPProbeProtocol]
- "main_scripts_scanner_base_udpprobeprotocol_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L574 | neighbors=[_UDPProbeProtocol]
- "main_scripts_service_banner_main": "main()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L222 | neighbors=[service_banner.py]
- "main_scripts_service_banner_rationale_1": "service_banner.py — grab service banners and light version strings.  METHOD (col" | kind=entity | source=probe/main_scripts/service_banner.py:L1 | neighbors=[service_banner.py]
- "main_scripts_service_banner_rationale_116": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L116 | neighbors=[._rung()]
- "main_scripts_service_banner_rationale_130": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L130 | neighbors=[._rung()]
- "main_scripts_service_banner_rationale_133": "One probe-ladder rung on its own connection. Returns banner bytes, b\"\"         (" | kind=entity | source=probe/main_scripts/service_banner.py:L133 | neighbors=[._rung()]
- "main_scripts_service_banner_rationale_82": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L82 | neighbors=[match_service()]
- "main_scripts_service_banner_rationale_89": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L89 | neighbors=[match_service()]
- "main_scripts_service_banner_rationale_92": "Soft-match collected bytes to {service, product, version}; None if unknown." | kind=entity | source=probe/main_scripts/service_banner.py:L92 | neighbors=[match_service()]
- "main_scripts_service_banner_servicebannerscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L126 | neighbors=[ServiceBannerScanner]
- "main_scripts_service_enum_rationale_1": "service_enum.py — enrichment / enumeration layer that runs AFTER host_discovery." | kind=entity | source=probe/main_scripts/service_enum.py:L1 | neighbors=[service_enum.py]
- "main_scripts_service_enum_rationale_105": "Everything learned about one target beyond 'it is alive'." | kind=entity | source=probe/main_scripts/service_enum.py:L105 | neighbors=[Enrichment]
- "main_scripts_service_enum_rationale_127": "Decode a DNS name (with 0xC0 compression) -> (name, next_offset)." | kind=entity | source=probe/main_scripts/service_enum.py:L127 | neighbors=[_dns_read_name()]
- "main_scripts_service_enum_rationale_148": "Ask the host over multicast DNS (5353) for the PTR of its own address." | kind=entity | source=probe/main_scripts/service_enum.py:L148 | neighbors=[mdns_hostname()]
- "main_scripts_service_enum_rationale_175": "NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)." | kind=entity | source=probe/main_scripts/service_enum.py:L175 | neighbors=[_nb_encode()]
- "main_scripts_service_enum_rationale_185": "NBNS node-status (NBSTAT) query to UDP/137; return the workstation name." | kind=entity | source=probe/main_scripts/service_enum.py:L185 | neighbors=[netbios_name()]
- "main_scripts_service_enum_rationale_216": "Run the three name sources concurrently off the event loop." | kind=entity | source=probe/main_scripts/service_enum.py:L216 | neighbors=[resolve_hostnames()]
- "main_scripts_service_enum_rationale_236": "One permissive TLS handshake: negotiated version + cert subject/issuer." | kind=entity | source=probe/main_scripts/service_enum.py:L236 | neighbors=[tls_info()]
- "main_scripts_service_enum_rationale_259": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=probe/main_scripts/service_enum.py:L259 | neighbors=[tls_accepts_old()]
- "main_scripts_service_enum_rationale_294": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=probe/main_scripts/service_enum.py:L294 | neighbors=[smb_dialects()]
- "main_scripts_service_enum_rationale_313": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=probe/main_scripts/service_enum.py:L313 | neighbors=[guess_os()]
- "main_scripts_service_enum_rationale_361": "Descriptive role tags from the open-port signature." | kind=entity | source=probe/main_scripts/service_enum.py:L361 | neighbors=[classify_roles()]
- "main_scripts_service_enum_rationale_396": "Directly-connected subnets and default gateway(s) from the OS route table." | kind=entity | source=probe/main_scripts/service_enum.py:L396 | neighbors=[local_topology()]
- "main_scripts_service_enum_rationale_466": "Connect to one port and read whatever it voluntarily advertises." | kind=entity | source=probe/main_scripts/service_enum.py:L466 | neighbors=[._probe_port()]
- "main_scripts_service_enum_reverse_dns": "reverse_dns()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L119 | neighbors=[service_enum.py]
- "main_scripts_service_enum_serviceenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L452 | neighbors=[ServiceEnumScanner]
- "main_scripts_smb_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L197 | neighbors=[smb_scanner.py]
- "main_scripts_smb_scanner_rationale_1": "smb_scanner.py — detect which SMB dialects a host supports.  METHOD (collection" | kind=entity | source=probe/main_scripts/smb_scanner.py:L1 | neighbors=[smb_scanner.py]
- "main_scripts_smb_scanner_rationale_37": "Read signing posture from a SUCCESSFUL SMB2 NEGOTIATE response.      Wire layout" | kind=entity | source=probe/main_scripts/smb_scanner.py:L37 | neighbors=[parse_smb2_security_mode()]
- "main_scripts_smb_scanner_smbscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L145 | neighbors=[SMBScanner]
- "main_scripts_snmp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L401 | neighbors=[snmp_scanner.py]
- "main_scripts_snmp_scanner_rationale_1": "snmp_scanner.py — full SNMP enumeration: community discovery, targeted MIB walk," | kind=entity | source=probe/main_scripts/snmp_scanner.py:L1 | neighbors=[snmp_scanner.py]
- "main_scripts_snmp_scanner_rationale_105": "Shallow parse of BER TLVs starting at offset. Returns [(tag, value), ...]." | kind=entity | source=probe/main_scripts/snmp_scanner.py:L105 | neighbors=[_ber_parse()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-157.json

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
