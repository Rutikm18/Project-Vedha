# Node Description Batch 73 of 227

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

- "main_scripts_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L433 | neighbors=[AdaptiveRateController, Current integer window (>= min_window)., Current integer window (>= min_window).]
- "main_scripts_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L647 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…, Wrap an IPv6 literal in [] for a URL au…]
- "main_scripts_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L384 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…, Standard 16-bit one's-complement Intern…]
- "main_scripts_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L659 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…, Parse '22,80,443,8000-8100' into a sort…]
- "main_scripts_scanner_base_ratelimiter_wait": ".wait()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L373 | neighbors=[.acquire(), .run(), RateLimiter]
- "main_scripts_scanner_base_resolve": "resolve()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L531 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…, Resolve `target` to a concrete (family,…]
- "main_scripts_scanner_base_resultwriter_close": ".close()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L717 | neighbors=[async_udp_probe(), ResultWriter, run_cli()]
- "main_scripts_scanner_base_resultwriter_write": ".write()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L708 | neighbors=[.run(), ResultWriter, .to_json()]
- "main_scripts_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L357 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard, Read-only view of excluded networks (to…]
- "main_scripts_scanner_base_scopeguard_from_file": ".from_file()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L276 | neighbors=[run_cli(), ScopeGuard, ScopeError]
- "main_scripts_scanner_base_scopeguard_in_scope": ".in_scope()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L324 | neighbors=[ScopeGuard, .assert_in_scope(), .filter()]
- "main_scripts_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L352 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard, Read-only view of allowed networks (for…]
- "main_scripts_service_enum_classify_roles": "classify_roles()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L360 | neighbors=[service_enum.py, Descriptive role tags from the open-por…, .scan_target()]
- "main_scripts_service_enum_dns_read_name": "_dns_read_name()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L126 | neighbors=[service_enum.py, mdns_hostname(), Decode a DNS name (with 0xC0 compressio…]
- "main_scripts_service_enum_enrichment": "Enrichment" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L104 | neighbors=[service_enum.py, Everything learned about one target bey…, .scan_target()]
- "main_scripts_service_enum_guess_os": "guess_os()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L311 | neighbors=[service_enum.py, Best-effort OS guess from voluntary evi…, .scan_target()]
- "main_scripts_service_enum_local_topology": "local_topology()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L395 | neighbors=[service_enum.py, main(), Directly-connected subnets and default …]
- "main_scripts_service_enum_mdns_hostname": "mdns_hostname()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L147 | neighbors=[service_enum.py, _dns_read_name(), Ask the host over multicast DNS (5353) …]
- "main_scripts_service_enum_nb_encode": "_nb_encode()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L174 | neighbors=[service_enum.py, netbios_name(), NetBIOS first-level name encoding (16-b…]
- "main_scripts_service_enum_netbios_name": "netbios_name()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L184 | neighbors=[service_enum.py, _nb_encode(), NBNS node-status (NBSTAT) query to UDP/…]
- "main_scripts_service_enum_resolve_hostnames": "resolve_hostnames()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L215 | neighbors=[service_enum.py, Run the three name sources concurrently…, .scan_target()]
- "main_scripts_smb_scanner_parse_smb2_security_mode": "parse_smb2_security_mode()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L36 | neighbors=[smb_scanner.py, Read signing posture from a SUCCESSFUL …, .scan_target()]
- "main_scripts_snmp_scanner_ber_parse": "_ber_parse()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L104 | neighbors=[snmp_scanner.py, _parse_varbinds(), Shallow parse of BER TLVs starting at o…]
- "main_scripts_snmp_scanner_oid_tlv": "_oid_tlv()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L155 | neighbors=[snmp_scanner.py, _ber_len(), _varbind()]
- "main_scripts_snmp_scanner_snmpscanner_snmpv3_present": "._snmpv3_present()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L324 | neighbors=[Send a SNMPv3 Discover. Any reply = v3 …, SNMPScanner, ._udp()]
- "main_scripts_syn_scanner_synscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L284 | neighbors=[SynScanner, ._fallback_scan(), ._syn_scan_target()]
- "main_scripts_tls_fingerprint_key_share_ext": "_key_share_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L78 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_sni_extension": "_sni_extension()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L66 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_fingerprint_supported_versions_ext": "_supported_versions_ext()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L73 | neighbors=[tls_fingerprint.py, build_client_hello(), _ext()]
- "main_scripts_tls_scanner_classify_cipher": "classify_cipher()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L60 | neighbors=[tls_scanner.py, Flag the security-relevant properties o…, _scan_tls_sync()]
- "main_scripts_tls_scanner_get_cert_der": "_get_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L173 | neighbors=[tls_scanner.py, _sni(), _scan_tls_sync()]
- "main_scripts_tls_scanner_grade_tls_posture": "grade_tls_posture()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L104 | neighbors=[tls_scanner.py, Grade overall TLS posture A/B/C/F from …, _scan_tls_sync()]
- "main_scripts_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L139 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…, RMCP Ping (ASF Presence Ping) to detect…]
- "main_scripts_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L158 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…, mDNS PTR query for _services._dns-sd._u…]
- "main_scripts_udp_scanner_sip_probe": "_sip_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L113 | neighbors=[udp_scanner.py, SIP OPTIONS request — safe fingerprint …, ._probe()]
- "main_scripts_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L146 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…, UPnP/SSDP M-SEARCH — unicast to target:…]
- "main_scripts_unauth_access_classify_unauth_access": "classify_unauth_access()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L48 | neighbors=[unauth_access.py, _as_text(), Decide whether `banner` proves unauthen…]
- "main_scripts_vantage_matrix_extract": "_extract()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L41 | neighbors=[vantage_matrix.py, (proto, port, status) from a ScanResult…, reconcile_vantages()]
- "models_agent_recommendation_rationale_1": "agent_recommendation.py — decisions/actions proposed by the agentic AI advisor." | kind=entity | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[agent_recommendation.py, Base, TimestampMixin]
- "models_attack_path": "attack_path.py" | kind=code-symbol | source=manager/backend/app/models/attack_path.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackPath, 298a9d4 trim frontend to 7 core pages; …]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-072.json

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
