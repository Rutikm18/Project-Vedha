# Node Description Batch 137 of 336

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

- "main_scripts_syn_scanner_rationale_232": "A genuine reply to our SYN acknowledges ISN+1. The reply's own source     (ip_sr" | kind=entity | source=probe/main_scripts/syn_scanner.py:L232 | neighbors=[verify_reply_cookie(), _local_source_ip()]
- "main_scripts_syn_scanner_synscanner_fallback_scan": "._fallback_scan()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L371 | neighbors=[SynScanner, .scan_target()]
- "main_scripts_syn_scanner_synscanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L315 | neighbors=[SynScanner, syn_scan_supported()]
- "main_scripts_syn_scanner_synscanner_syn_scan_target": "._syn_scan_target()" | kind=code-symbol | source=probe/main_scripts/syn_scanner.py:L379 | neighbors=[SynScanner, .scan_target()]
- "main_scripts_tls_fingerprint_probe_specs": "_probe_specs()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L221 | neighbors=[tls_fingerprint.py, fingerprint_host()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L290 | neighbors=[TLSFingerprintScanner, .scan_target()]
- "main_scripts_tls_fingerprint_tlsfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L320 | neighbors=[TLSFingerprintScanner, ._scan_port()]
- "main_scripts_tls_fingerprint_version_code": "version_code()" | kind=code-symbol | source=probe/main_scripts/tls_fingerprint.py:L174 | neighbors=[tls_fingerprint.py, jarm_style_digest()]
- "main_scripts_tls_scanner_parse_cert_der": "_parse_cert_der()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L215 | neighbors=[tls_scanner.py, _scan_tls_sync()]
- "main_scripts_tls_scanner_tlsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L320 | neighbors=[TLSScanner, .scan_target()]
- "main_scripts_tls_scanner_tlsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/tls_scanner.py:L339 | neighbors=[TLSScanner, ._scan_port()]
- "main_scripts_udp_scanner_ike_probe": "_ike_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L77 | neighbors=[udp_scanner.py, Minimal IKEv2 IKE_SA_INIT probe.  Sends…]
- "main_scripts_udp_scanner_interpret_dns_recursion": "interpret_dns_recursion()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L173 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_interpret_memcached_stats": "interpret_memcached_stats()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L184 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_interpret_ntp_monlist": "interpret_ntp_monlist()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L169 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_ntp_monlist_probe": "_ntp_monlist_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L50 | neighbors=[udp_scanner.py, ._probe()]
- "main_scripts_udp_scanner_tftp_probe": "_tftp_probe()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L132 | neighbors=[udp_scanner.py, TFTP RRQ for a non-existent file.  Erro…]
- "main_scripts_udp_scanner_udpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/udp_scanner.py:L386 | neighbors=[UDPScanner, ._probe()]
- "main_scripts_unauth_access_as_text": "_as_text()" | kind=code-symbol | source=probe/main_scripts/unauth_access.py:L40 | neighbors=[unauth_access.py, classify_unauth_access()]
- "main_scripts_va_campaign_atomic_write_json": "_atomic_write_json()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L282 | neighbors=[va_campaign.py, ._flush()]
- "main_scripts_va_campaign_bounded_gather": "_bounded_gather()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L374 | neighbors=[va_campaign.py, Run coro_factory(item) over items with …]
- "main_scripts_va_campaign_campaignoptions": "CampaignOptions" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L97 | neighbors=[va_campaign.py, Everything that changes WHAT the campai…]
- "main_scripts_va_campaign_cliprogressview_format": "._format()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L690 | neighbors=[CliProgressView, ._redraw()]
- "main_scripts_va_campaign_cliprogressview_transitions": "._transitions()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L678 | neighbors=[CliProgressView, .__call__()]
- "main_scripts_va_campaign_discover_ipv6": "_discover_ipv6()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L343 | neighbors=[va_campaign.py, Best-effort IPv6 neighbor discovery (ND…]
- "main_scripts_va_campaign_progressreporter_current": "._current()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L230 | neighbors=[ProgressReporter, .snapshot()]
- "main_scripts_va_campaign_progressreporter_percent": "._percent()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L222 | neighbors=[ProgressReporter, .snapshot()]
- "main_scripts_va_campaign_stage": "Stage" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L126 | neighbors=[va_campaign.py, default_stages()]
- "main_scripts_va_campaign_stageoutcome": "StageOutcome" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L113 | neighbors=[va_campaign.py, What a stage produced. `count` is stage…]
- "main_scripts_va_campaign_stagestate_to_dict": ".to_dict()" | kind=code-symbol | source=probe/main_scripts/va_campaign.py:L161 | neighbors=[.snapshot(), StageState]
- "main_scripts_vantage_matrix_is_external": "_is_external()" | kind=code-symbol | source=probe/main_scripts/vantage_matrix.py:L34 | neighbors=[vantage_matrix.py, reconcile_vantages()]
- "main_scripts_vnc_scanner_vncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L127 | neighbors=[VNCScanner, .scan_target()]
- "main_scripts_vnc_scanner_vncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/vnc_scanner.py:L145 | neighbors=[VNCScanner, ._scan_port()]
- "main_scripts_web_scanner_fetch": "_fetch()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L78 | neighbors=[web_scanner.py, parse_allow_header()]
- "main_scripts_web_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L55 | neighbors=[web_scanner.py, .redirect_request()]
- "main_scripts_web_scanner_webscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/web_scanner.py:L176 | neighbors=[WebScanner, ._scan_port()]
- "main_scripts_windows_collector_smb_registry_collect": "_smb_registry_collect()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L158 | neighbors=[windows_collector.py, Connect to RemoteRegistry over SMB and …]
- "main_scripts_windows_collector_windowscollector_full_user": "._full_user()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L294 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_run": ".run()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L326 | neighbors=[WindowsCollector, ._collect_host()]
- "main_scripts_windows_collector_windowscollector_smb_result": "._smb_result()" | kind=code-symbol | source=probe/main_scripts/windows_collector.py:L318 | neighbors=[WindowsCollector, ._collect_host()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-136.json

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
