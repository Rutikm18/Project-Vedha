# Node Description Batch 43 of 92

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

- "scanner_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=scanner/scanner_base.py:L88 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…]
- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=scanner/scanner_base.py:L745 | neighbors=[BaseScanner, RateLimiter]
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/scanner_base.py:L753 | neighbors=[BaseScanner, ._guarded()]
- "scanner_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=scanner/scanner_base.py:L647 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…]
- "scanner_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…]
- "scanner_scanner_base_inet_checksum": "inet_checksum()" | kind=code-symbol | source=scanner/scanner_base.py:L384 | neighbors=[scanner_base.py, Standard 16-bit one's-complement Intern…]
- "scanner_scanner_base_jittered_delay": "jittered_delay()" | kind=code-symbol | source=scanner/scanner_base.py:L78 | neighbors=[scanner_base.py, A per-probe delay of `base` seconds ± u…]
- "scanner_scanner_base_parse_ports": "parse_ports()" | kind=code-symbol | source=scanner/scanner_base.py:L659 | neighbors=[scanner_base.py, Parse '22,80,443,8000-8100' into a sort…]
- "scanner_scanner_base_probe_payload": "probe_payload()" | kind=code-symbol | source=scanner/scanner_base.py:L61 | neighbors=[scanner_base.py, Benign, non-attributing payload for ICM…]
- "scanner_scanner_base_resolve": "resolve()" | kind=code-symbol | source=scanner/scanner_base.py:L531 | neighbors=[scanner_base.py, Resolve `target` to a concrete (family,…]
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=scanner/scanner_base.py:L240 | neighbors=[.write(), ScanResult]
- "scanner_scanner_base_scopeguard_excludes": ".excludes()" | kind=code-symbol | source=scanner/scanner_base.py:L357 | neighbors=[Read-only view of excluded networks (to…, ScopeGuard]
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=scanner/scanner_base.py:L344 | neighbors=[ScopeGuard, .in_scope()]
- "scanner_scanner_base_scopeguard_networks": ".networks()" | kind=code-symbol | source=scanner/scanner_base.py:L352 | neighbors=[Read-only view of allowed networks (for…, ScopeGuard]
- "scanner_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=scanner/scanner_base.py:L55 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…]
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=scanner/service_banner.py:L85 | neighbors=[service_banner.py, match_service()]
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/service_banner.py:L234 | neighbors=[ServiceBannerScanner, ._grab()]
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=scanner/service_enum.py:L601 | neighbors=[service_enum.py, local_topology()]
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=scanner/service_enum.py:L456 | neighbors=[ServiceEnumScanner, ._probe_port()]
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=scanner/service_enum.py:L293 | neighbors=[service_enum.py, Negotiate against 445; report whether S…]
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=scanner/service_enum.py:L388 | neighbors=[service_enum.py, .scan_target()]
- "scanner_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=scanner/service_enum.py:L258 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…]
- "scanner_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=scanner/service_enum.py:L235 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…]
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()]
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=scanner/smb_scanner.py:L88 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=scanner/smb_scanner.py:L108 | neighbors=[smb_scanner.py, .scan_target()]
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=scanner/smb_scanner.py:L149 | neighbors=[SMBScanner, _netbios_session()]
- "scanner_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=scanner/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()]
- "scanner_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=scanner/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "scanner_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=scanner/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "scanner_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=scanner/syn_scanner.py:L299 | neighbors=[SynScanner, .scan_target()]
- "scanner_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=scanner/syn_scanner.py:L251 | neighbors=[SynScanner, syn_scan_supported()]
- "scanner_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=scanner/syn_scanner.py:L307 | neighbors=[SynScanner, .scan_target()]
- "scanner_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L220 | neighbors=[tls_fingerprint.py, fingerprint_host()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L289 | neighbors=[TLSFingerprintScanner, .scan_target()]
- "scanner_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L315 | neighbors=[TLSFingerprintScanner, ._scan_port()]
- "scanner_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=scanner/tls_fingerprint.py:L173 | neighbors=[tls_fingerprint.py, jarm_style_digest()]
- "scanner_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=scanner/tls_scanner.py:L185 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "scanner_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/tls_scanner.py:L279 | neighbors=[TLSScanner, .scan_target()]
- "scanner_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/tls_scanner.py:L298 | neighbors=[TLSScanner, ._scan_port()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-042.json

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
