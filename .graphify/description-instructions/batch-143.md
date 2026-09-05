# Node Description Batch 144 of 336

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

- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L229 | neighbors=[service_banner.py, match_service()]
- "scanner_service_banner_servicebannerscanner_connect": "._connect()" | kind=code-symbol | source=probe/scanner/service_banner.py:L339 | neighbors=[ServiceBannerScanner, ._rung()]
- "scanner_service_banner_servicebannerscanner_ladder_for": "._ladder_for()" | kind=code-symbol | source=probe/scanner/service_banner.py:L416 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L524 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_service_banner_tls_context": "_tls_context()" | kind=code-symbol | source=probe/scanner/service_banner.py:L50 | neighbors=[service_banner.py, A permissive client context for FINGERP…]
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=probe/scanner/service_enum.py:L630 | neighbors=[service_enum.py, local_topology()]
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/scanner/service_enum.py:L485 | neighbors=[ServiceEnumScanner, ._probe_port()]
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/scanner/service_enum.py:L417 | neighbors=[service_enum.py, .scan_target()]
- "scanner_smb_enum_scanner_smbenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L221 | neighbors=[SMBEnumScanner, parse_rid_ranges()]
- "scanner_smb_enum_scanner_smbenumscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L274 | neighbors=[SMBEnumScanner, .scan_target()]
- "scanner_smb_enum_scanner_smbenumscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L295 | neighbors=[SMBEnumScanner, ._scan_port()]
- "scanner_smb_scanner_der_len": "_der_len()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L104 | neighbors=[smb_scanner.py, _der()]
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L229 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smtp_scanner_smtpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L124 | neighbors=[SMTPScanner, .scan_target()]
- "scanner_smtp_scanner_smtpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/smtp_scanner.py:L142 | neighbors=[SMTPScanner, ._scan_port()]
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()]
- "scanner_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()]
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()]
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L329 | neighbors=[SNMPScanner, _extract_sysdescr()]
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "scanner_ssh_kexdb_lookup": "lookup()" | kind=code-symbol | source=probe/scanner/ssh_kexdb.py:L477 | neighbors=[ssh_kexdb.py, Return (failures, warnings, infos) for …]
- "scanner_ssh_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L215 | neighbors=[ssh_scanner.py, _read_packet()]
- "scanner_ssh_scanner_sshscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/ssh_scanner.py:L331 | neighbors=[SSHScanner, ._scan_port()]
- "scanner_syn_scanner_rationale_232": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/scanner/syn_scanner.py:L232 | neighbors=[verify_reply_cookie(), _local_source_ip()]
- "scanner_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L371 | neighbors=[SynScanner, .scan_target()]
- "scanner_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L315 | neighbors=[SynScanner, syn_scan_supported()]
- "scanner_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L379 | neighbors=[SynScanner, .scan_target()]
- "scanner_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L221 | neighbors=[tls_fingerprint.py, fingerprint_host()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L290 | neighbors=[TLSFingerprintScanner, .scan_target()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L320 | neighbors=[TLSFingerprintScanner, ._scan_port()]
- "scanner_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L174 | neighbors=[tls_fingerprint.py, jarm_style_digest()]
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L215 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L320 | neighbors=[TLSScanner, .scan_target()]
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L339 | neighbors=[TLSScanner, ._scan_port()]
- "scanner_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…]
- "scanner_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L173 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L184 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L169 | neighbors=[udp_scanner.py, ._probe()]
- "scanner_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-143.json

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
