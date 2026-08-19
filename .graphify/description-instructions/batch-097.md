# Node Description Batch 98 of 227

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

- "main_scripts_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L108 | neighbors=[smb_scanner.py, .scan_target()]
- "main_scripts_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L149 | neighbors=[SMBScanner, _netbios_session()]
- "main_scripts_snmp_scanner_oid_in_subtree": "_oid_in_subtree()" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L240 | neighbors=[snmp_scanner.py, ._walk_subtree()]
- "main_scripts_ssh_collector_sshcollector_collect": "._collect()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L95 | neighbors=[SSHCollector, .run()]
- "main_scripts_ssh_collector_sshcollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/ssh_collector.py:L117 | neighbors=[SSHCollector, ._collect()]
- "main_scripts_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L299 | neighbors=[SynScanner, .scan_target()]
- "main_scripts_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L251 | neighbors=[SynScanner, syn_scan_supported()]
- "main_scripts_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L307 | neighbors=[SynScanner, .scan_target()]
- "main_scripts_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L220 | neighbors=[tls_fingerprint.py, fingerprint_host()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L289 | neighbors=[TLSFingerprintScanner, .scan_target()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L315 | neighbors=[TLSFingerprintScanner, ._scan_port()]
- "main_scripts_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L173 | neighbors=[tls_fingerprint.py, jarm_style_digest()]
- "main_scripts_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L185 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "main_scripts_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L262 | neighbors=[TLSScanner, .scan_target()]
- "main_scripts_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L281 | neighbors=[TLSScanner, ._scan_port()]
- "main_scripts_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…]
- "main_scripts_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L173 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L184 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L169 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "main_scripts_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L376 | neighbors=[UDPScanner, ._probe()]
- "main_scripts_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]
- "main_scripts_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "main_scripts_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L78 | neighbors=[web_scanner.py, parse_allow_header()]
- "main_scripts_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L55 | neighbors=[web_scanner.py, .redirect_request()]
- "main_scripts_web_scanner_webscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L143 | neighbors=[WebScanner, .scan_target()]
- "main_scripts_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L160 | neighbors=[WebScanner, ._scan_port()]
- "main_scripts_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "main_scripts_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_transport_order": "._transport_order()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L299 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_winrm_result": "._winrm_result()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L306 | neighbors=[WindowsCollector, ._collect_host()]
- "models_audit_log_rationale_12": "Immutable, append-only audit trail for all exploit actions.     No TimestampMixi" | kind=entity | source=manager/backend/app/models/audit_log.py:L12 | neighbors=[AuditLog, Base]
- "models_probe_site": "probe_site.py" | kind=code-symbol | source=manager/backend/app/models/probe_site.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ProbeSite]
- "models_scan_job_attempt": "scan_job_attempt.py" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, ScanJobAttempt]
- "native_dir_bust_loadwordlist": "loadWordlist()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L97 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dir_bust_probe": "probe()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L71 | neighbors=[dir-bust.ts, nativeDirBust()]
- "native_dns_recon_attemptzonetransfer": "attemptZoneTransfer()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L96 | neighbors=[dns-recon.ts, nativeDnsRecon()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-097.json

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
