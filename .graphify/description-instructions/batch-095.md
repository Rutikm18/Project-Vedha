# Node Description Batch 96 of 209

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
Write every description in Portuguese (pt). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L665 | neighbors=[BaseScanner, RateLimiter]
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L673 | neighbors=[BaseScanner, ._guarded()]
- "scanner_scanner_base_rationale_205": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L205 | neighbors=[AdaptiveRateController, expand_targets()]
- "scanner_scanner_base_rationale_359": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[_UDPProbeProtocol, BaseScanner]
- "scanner_scanner_base_rationale_535": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L535 | neighbors=[BaseScanner, main_entrypoint()]
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L169 | neighbors=[.write(), ScanResult]
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L273 | neighbors=[ScopeGuard, .in_scope()]
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L82 | neighbors=[service_banner.py, match_service()]
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L213 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()]
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L88 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L108 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L149 | neighbors=[SMBScanner, _netbios_session()]
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()]
- "scanner_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()]
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L329 | neighbors=[SNMPScanner, _extract_sysdescr()]
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "scanner_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L295 | neighbors=[SynScanner, .scan_target()]
- "scanner_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L250 | neighbors=[SynScanner, syn_scan_supported()]
- "scanner_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L303 | neighbors=[SynScanner, .scan_target()]
- "scanner_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L220 | neighbors=[tls_fingerprint.py, fingerprint_host()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L289 | neighbors=[TLSFingerprintScanner, .scan_target()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L315 | neighbors=[TLSFingerprintScanner, ._scan_port()]
- "scanner_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L173 | neighbors=[tls_fingerprint.py, jarm_style_digest()]
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L185 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L262 | neighbors=[TLSScanner, .scan_target()]
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L281 | neighbors=[TLSScanner, ._scan_port()]
- "scanner_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…]
- "scanner_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L172 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L183 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L168 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ipmi_probe": "_ipmi_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L138 | neighbors=[udp_scanner.py, RMCP Ping (ASF Presence Ping) to detect…]
- "scanner_udp_scanner_mdns_probe": "_mdns_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L157 | neighbors=[udp_scanner.py, mDNS PTR query for _services._dns-sd._u…]
- "scanner_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ssdp_probe": "_ssdp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L145 | neighbors=[udp_scanner.py, UPnP/SSDP M-SEARCH — unicast to target:…]
- "scanner_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "scanner_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L375 | neighbors=[UDPScanner, ._probe()]
- "scanner_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=probe/scanner/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-095.json

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
