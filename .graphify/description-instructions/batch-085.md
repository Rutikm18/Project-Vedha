# Node Description Batch 86 of 186

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

- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L315 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L182 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L109 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L154 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L115 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L74 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L68 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L118 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "scanner_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L255 | neighbors=[OSFingerprintScanner, fingerprint_os()]
- "scanner_os_fingerprint_rationale_205": "Return (socket, is_raw). Prefer datagram-ICMP (unprivileged), then raw." | kind=entity | source=probe/scanner/os_fingerprint.py:L205 | neighbors=[_open_icmp_socket(), OSFingerprintScanner]
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "scanner_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L127 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…]
- "scanner_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L207 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L200 | neighbors=[Requested ports that were never recorde…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L181 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L229 | neighbors=[.scan_target(), ScanMetrics]
- "scanner_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L94 | neighbors=[scan_funnel.py, .run_host()]
- "scanner_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L180 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel]
- "scanner_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L83 | neighbors=[.run_host(), _Scanner]
- "scanner_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L377 | neighbors=[AdaptiveRateController, .wait()]
- "scanner_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L373 | neighbors=[AdaptiveRateController, .report_loss()]
- "scanner_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L366 | neighbors=[AdaptiveRateController, .report_success()]
- "scanner_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L389 | neighbors=[AdaptiveRateController, ._on_loss()]
- "scanner_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L383 | neighbors=[AdaptiveRateController, ._on_success()]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-085.json

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
