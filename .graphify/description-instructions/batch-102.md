# Node Description Batch 103 of 227

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "scanner_scanner_base_rationale_252": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L252 | neighbors=[ScopeGuard, .window()] | lang=en
- "scanner_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L353 | neighbors=[.networks(), bracket_host()] | lang=en
- "scanner_scanner_base_rationale_359": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[_UDPProbeProtocol, BaseScanner] | lang=en
- "scanner_scanner_base_rationale_535": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L535 | neighbors=[BaseScanner, main_entrypoint()] | lang=pt
- "scanner_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=probe/scanner/scanner_base.py:L69 | neighbors=[choose_source_port(), ScopeGuard] | lang=en
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L240 | neighbors=[.write(), ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L344 | neighbors=[ScopeGuard, .in_scope()] | lang=en
- "scanner_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L55 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…] | lang=en
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L85 | neighbors=[service_banner.py, match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L216 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=probe/scanner/service_enum.py:L601 | neighbors=[service_enum.py, local_topology()] | lang=en
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/scanner/service_enum.py:L456 | neighbors=[ServiceEnumScanner, ._probe_port()] | lang=en
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/scanner/service_enum.py:L293 | neighbors=[service_enum.py, Negotiate against 445; report whether S…] | lang=en
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/scanner/service_enum.py:L388 | neighbors=[service_enum.py, .scan_target()] | lang=en
- "scanner_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=probe/scanner/service_enum.py:L258 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…] | lang=en
- "scanner_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=probe/scanner/service_enum.py:L235 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…] | lang=en
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()] | lang=en
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L88 | neighbors=[smb_scanner.py, .scan_target()] | lang=en
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L108 | neighbors=[smb_scanner.py, .scan_target()] | lang=en
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L149 | neighbors=[SMBScanner, _netbios_session()] | lang=en
- "scanner_snmp_scanner_extract_sysdescr": "_extract_sysdescr()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L44 | neighbors=[snmp_scanner.py, .scan_target()] | lang=en
- "scanner_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()] | lang=en
- "scanner_snmp_scanner_snmpscanner_query": "._query()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L84 | neighbors=[SNMPScanner, _build_get()] | lang=en
- "scanner_snmp_scanner_snmpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L329 | neighbors=[SNMPScanner, _extract_sysdescr()] | lang=en
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()] | lang=en
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()] | lang=en
- "scanner_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L299 | neighbors=[SynScanner, .scan_target()] | lang=en
- "scanner_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L251 | neighbors=[SynScanner, syn_scan_supported()] | lang=en
- "scanner_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/scanner/syn_scanner.py:L307 | neighbors=[SynScanner, .scan_target()] | lang=en
- "scanner_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L220 | neighbors=[tls_fingerprint.py, fingerprint_host()] | lang=en
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L289 | neighbors=[TLSFingerprintScanner, .scan_target()] | lang=en
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L315 | neighbors=[TLSFingerprintScanner, ._scan_port()] | lang=en
- "scanner_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=probe/scanner/tls_fingerprint.py:L173 | neighbors=[tls_fingerprint.py, jarm_style_digest()] | lang=en
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L185 | neighbors=[tls_scanner.py, _scan_tls_sync()] | lang=en
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L262 | neighbors=[TLSScanner, .scan_target()] | lang=en
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/tls_scanner.py:L281 | neighbors=[TLSScanner, ._scan_port()] | lang=en
- "scanner_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…] | lang=en
- "scanner_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L173 | neighbors=[udp_scanner.py, ._probe()] | lang=en
- "scanner_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L184 | neighbors=[udp_scanner.py, ._probe()] | lang=en
- "scanner_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/scanner/udp_scanner.py:L169 | neighbors=[udp_scanner.py, ._probe()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-102.json

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
