# Node Description Batch 152 of 380

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

- "main_scripts_nfs_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/main_scripts/nfs_scanner.py:L156 | neighbors=[nfs_scanner.py, _recv_record()] | lang=en
- "main_scripts_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L160 | neighbors=[nmap_wrapper.py, NmapExecutionError] | lang=en
- "main_scripts_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L121 | neighbors=[nmap_wrapper.py, NmapExecutionError] | lang=en
- "main_scripts_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()] | lang=en
- "main_scripts_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()] | lang=en
- "main_scripts_os_fingerprint_rationale_205": "p0f-style match on (initial TTL, option layout, window scale) → a specific     s" | kind=entity | source=probe/main_scripts/os_fingerprint.py:L205 | neighbors=[match_stack_signature(), _open_icmp_socket()] | lang=pt
- "main_scripts_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()] | lang=en
- "main_scripts_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()] | lang=en
- "main_scripts_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()] | lang=en
- "main_scripts_port_scanner_portscanner_retain_result": "._retain_result()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L642 | neighbors=[PortScanner, Must this result OBJECT outlive the por…] | lang=en
- "main_scripts_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L315 | neighbors=[.scan_target(), ScanMetrics] | lang=en
- "main_scripts_printer_scanner_ipp_attr": "_ipp_attr()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L49 | neighbors=[printer_scanner.py, build_ipp_get_printer_attributes()] | lang=en
- "main_scripts_printer_scanner_printerscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L138 | neighbors=[PrinterScanner, .scan_target()] | lang=en
- "main_scripts_printer_scanner_printerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/printer_scanner.py:L155 | neighbors=[PrinterScanner, ._scan_port()] | lang=en
- "main_scripts_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L173 | neighbors=[rdp_scanner.py, RDPScanner] | lang=en
- "main_scripts_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L142 | neighbors=[RDPScanner, .scan_target()] | lang=en
- "main_scripts_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L168 | neighbors=[RDPScanner, ._scan_port()] | lang=en
- "main_scripts_rsync_scanner_rsyncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L144 | neighbors=[RsyncScanner, .scan_target()] | lang=en
- "main_scripts_rsync_scanner_rsyncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/rsync_scanner.py:L162 | neighbors=[RsyncScanner, ._scan_port()] | lang=en
- "main_scripts_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L92 | neighbors=[run_all.py, main()] | lang=en
- "main_scripts_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L106 | neighbors=[run_all.py, main()] | lang=en
- "main_scripts_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L78 | neighbors=[run_all.py, main()] | lang=en
- "main_scripts_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L125 | neighbors=[scan_funnel.py, .run_host()] | lang=en
- "main_scripts_scan_funnel_rationale_73": "Canonical open-TCP set for a host = deduped, sorted union of every source." | kind=entity | source=probe/main_scripts/scan_funnel.py:L73 | neighbors=[reconcile_ports(), FunnelResult] | lang=en
- "main_scripts_scan_funnel_rationale_87": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/main_scripts/scan_funnel.py:L87 | neighbors=[route_ports(), _candidate_ports()] | lang=en
- "main_scripts_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L114 | neighbors=[.run_host(), _Scanner] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L534 | neighbors=[AdaptiveRateController, .wait()] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L528 | neighbors=[AdaptiveRateController, .report_loss()] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L521 | neighbors=[AdaptiveRateController, .report_success()] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L546 | neighbors=[AdaptiveRateController, ._on_loss()] | lang=en
- "main_scripts_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L540 | neighbors=[AdaptiveRateController, ._on_success()] | lang=en
- "main_scripts_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L988 | neighbors=[BaseScanner, RateLimiter] | lang=en
- "main_scripts_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L996 | neighbors=[BaseScanner, ._guarded()] | lang=en
- "main_scripts_scanner_base_rationale_252": "Full, debuggable classification for attaching to a ScanResult: state,     reason" | kind=entity | source=probe/main_scripts/scanner_base.py:L252 | neighbors=[describe_os_error(), ScopeGuard] | lang=en
- "main_scripts_scanner_base_rationale_518": "Current integer window (>= min_window)." | kind=entity | source=probe/main_scripts/scanner_base.py:L518 | neighbors=[.window(), async_udp_probe()] | lang=en
- "main_scripts_scanner_base_rationale_629": "Pacing telemetry for the scan summary (so a throttled scan is visible)." | kind=entity | source=probe/main_scripts/scanner_base.py:L629 | neighbors=[.stats(), async_udp_probe_retry()] | lang=en
- "main_scripts_scanner_base_resolve_project_tz": "_resolve_project_tz()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L66 | neighbors=[scanner_base.py, The project timezone, degrading safely …] | lang=en
- "main_scripts_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L304 | neighbors=[.write(), ScanResult] | lang=en
- "main_scripts_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L408 | neighbors=[ScopeGuard, .in_scope()] | lang=en
- "main_scripts_scanner_registry_is_verified": "is_verified()" | kind=code-symbol | source=probe/main_scripts/scanner_registry.py:L97 | neighbors=[scanner_registry.py, True only for a scanner explicitly on t…] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-151.json

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
