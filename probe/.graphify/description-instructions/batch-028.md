# Node Description Batch 29 of 92

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

- "main_scripts_port_scanner_family_of": "_family_of()" | kind=code-symbol | source=main_scripts/port_scanner.py:L92 | neighbors=[port_scanner.py, ._attempt(), Return 'ipv4'/'ipv6' for an IP literal,…]
- "main_scripts_rdp_scanner_build_connection_request": "build_connection_request()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L41 | neighbors=[rdp_scanner.py, probe_rdp(), TPKT + X.224 Connection Request carryin…]
- "main_scripts_rdp_scanner_parse_connection_confirm": "parse_connection_confirm()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L55 | neighbors=[rdp_scanner.py, probe_rdp(), Parse a Connection Confirm. Returns Non…]
- "main_scripts_run_all_log": "_log()" | kind=code-symbol | source=main_scripts/run_all.py:L48 | neighbors=[run_all.py, main(), _run_stage()]
- "main_scripts_scanner_base_async_udp_probe_retry": "async_udp_probe_retry()" | kind=code-symbol | source=main_scripts/scanner_base.py:L627 | neighbors=[scanner_base.py, async_udp_probe(), `async_udp_probe` with bounded per-port…]
- "main_scripts_scanner_base_classify_os_error": "classify_os_error()" | kind=code-symbol | source=main_scripts/scanner_base.py:L169 | neighbors=[scanner_base.py, describe_os_error(), Map a connect()/socket-time OSError to …]
- "main_scripts_scanner_base_describe_os_error": "describe_os_error()" | kind=code-symbol | source=main_scripts/scanner_base.py:L185 | neighbors=[scanner_base.py, classify_os_error(), Full, debuggable classification for att…]
- "main_scripts_scanner_base_expand_targets": "expand_targets()" | kind=code-symbol | source=main_scripts/scanner_base.py:L470 | neighbors=[scanner_base.py, Accepts CIDRs ('10.0.0.0/24'), single I…, run_cli()]
- "main_scripts_scanner_base_main_entrypoint": "main_entrypoint()" | kind=code-symbol | source=main_scripts/scanner_base.py:L836 | neighbors=[scanner_base.py, .run(), Run a scanner CLI's body with consisten…]
- "main_scripts_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=main_scripts/scanner_base.py:L373 | neighbors=[.acquire(), .run(), RateLimiter]
- "main_scripts_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=main_scripts/scanner_base.py:L717 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "main_scripts_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=main_scripts/scanner_base.py:L708 | neighbors=[.run(), ResultWriter, .to_json()]
- "main_scripts_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=main_scripts/scanner_base.py:L276 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "main_scripts_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=main_scripts/scanner_base.py:L324 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "main_scripts_service_banner_servicebannerscanner_rung": "._rung()" | kind=code-symbol | source=main_scripts/service_banner.py:L131 | neighbors=[One probe-ladder rung on its own connec…, ServiceBannerScanner, ._grab()]
- "main_scripts_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=main_scripts/service_enum.py:L360 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target()]
- "main_scripts_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=main_scripts/service_enum.py:L126 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…]
- "main_scripts_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=main_scripts/service_enum.py:L311 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target()]
- "main_scripts_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=main_scripts/service_enum.py:L395 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …]
- "main_scripts_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=main_scripts/service_enum.py:L147 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …]
- "main_scripts_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=main_scripts/service_enum.py:L174 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…]
- "main_scripts_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=main_scripts/service_enum.py:L184 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…]
- "main_scripts_service_enum_rationale_1": "service_enum.py — enrichment / enumeration layer that runs AFTER host_discovery." | kind=entity | source=main_scripts/service_enum.py:L1 | neighbors=[BaseScanner, ScanResult, service_enum.py]
- "main_scripts_service_enum_rationale_105": "Everything learned about one target beyond 'it is alive'." | kind=entity | source=main_scripts/service_enum.py:L105 | neighbors=[BaseScanner, ScanResult, Enrichment]
- "main_scripts_service_enum_rationale_127": "Decode a DNS name (with 0xC0 compression) -> (name, next_offset)." | kind=entity | source=main_scripts/service_enum.py:L127 | neighbors=[BaseScanner, ScanResult, _dns_read_name()]
- "main_scripts_service_enum_rationale_148": "Ask the host over multicast DNS (5353) for the PTR of its own address." | kind=entity | source=main_scripts/service_enum.py:L148 | neighbors=[BaseScanner, ScanResult, mdns_hostname()]
- "main_scripts_service_enum_rationale_175": "NetBIOS first-level name encoding (16-byte name -> 32 nibble bytes)." | kind=entity | source=main_scripts/service_enum.py:L175 | neighbors=[BaseScanner, ScanResult, _nb_encode()]
- "main_scripts_service_enum_rationale_185": "NBNS node-status (NBSTAT) query to UDP/137; return the workstation name." | kind=entity | source=main_scripts/service_enum.py:L185 | neighbors=[BaseScanner, ScanResult, netbios_name()]
- "main_scripts_service_enum_rationale_216": "Run the three name sources concurrently off the event loop." | kind=entity | source=main_scripts/service_enum.py:L216 | neighbors=[BaseScanner, ScanResult, resolve_hostnames()]
- "main_scripts_service_enum_rationale_236": "One permissive TLS handshake: negotiated version + cert subject/issuer." | kind=entity | source=main_scripts/service_enum.py:L236 | neighbors=[BaseScanner, ScanResult, tls_info()]
- "main_scripts_service_enum_rationale_259": "Which deprecated TLS/SSL versions the server still accepts (weak-config)." | kind=entity | source=main_scripts/service_enum.py:L259 | neighbors=[BaseScanner, ScanResult, tls_accepts_old()]
- "main_scripts_service_enum_rationale_294": "Negotiate against 445; report whether SMBv1 is offered (defensive flag)." | kind=entity | source=main_scripts/service_enum.py:L294 | neighbors=[BaseScanner, ScanResult, smb_dialects()]
- "main_scripts_service_enum_rationale_313": "Best-effort OS guess from voluntary evidence. Returns (label, confidence)." | kind=entity | source=main_scripts/service_enum.py:L313 | neighbors=[BaseScanner, ScanResult, guess_os()]
- "main_scripts_service_enum_rationale_361": "Descriptive role tags from the open-port signature." | kind=entity | source=main_scripts/service_enum.py:L361 | neighbors=[BaseScanner, ScanResult, classify_roles()]
- "main_scripts_service_enum_rationale_396": "Directly-connected subnets and default gateway(s) from the OS route table." | kind=entity | source=main_scripts/service_enum.py:L396 | neighbors=[BaseScanner, ScanResult, local_topology()]
- "main_scripts_service_enum_rationale_466": "Connect to one port and read whatever it voluntarily advertises." | kind=entity | source=main_scripts/service_enum.py:L466 | neighbors=[BaseScanner, ScanResult, ._probe_port()]
- "main_scripts_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=main_scripts/service_enum.py:L215 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target()]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=main_scripts/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "main_scripts_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "main_scripts_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=main_scripts/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-028.json

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
