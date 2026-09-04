# Node Description Batch 141 of 330

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

- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()] | lang=en
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()] | lang=en
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()] | lang=en
- "scanner_msrpc_scanner_msrpcscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L144 | neighbors=[MSRPCScanner, .scan_target()] | lang=en
- "scanner_msrpc_scanner_msrpcscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L167 | neighbors=[MSRPCScanner, ._scan_port()] | lang=en
- "scanner_nfs_scanner_nfsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L259 | neighbors=[NFSScanner, .scan_target()] | lang=en
- "scanner_nfs_scanner_nfsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L277 | neighbors=[NFSScanner, ._scan_port()] | lang=en
- "scanner_nfs_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L156 | neighbors=[nfs_scanner.py, _recv_record()] | lang=en
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L160 | neighbors=[nmap_wrapper.py, NmapExecutionError] | lang=en
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L121 | neighbors=[nmap_wrapper.py, NmapExecutionError] | lang=en
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()] | lang=en
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()] | lang=en
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()] | lang=en
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()] | lang=en
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()] | lang=en
- "scanner_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L315 | neighbors=[.scan_target(), ScanMetrics] | lang=en
- "scanner_printer_scanner_ipp_attr": "_ipp_attr()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L49 | neighbors=[printer_scanner.py, build_ipp_get_printer_attributes()] | lang=en
- "scanner_printer_scanner_printerscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L138 | neighbors=[PrinterScanner, .scan_target()] | lang=en
- "scanner_printer_scanner_printerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L155 | neighbors=[PrinterScanner, ._scan_port()] | lang=en
- "scanner_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L173 | neighbors=[rdp_scanner.py, RDPScanner] | lang=en
- "scanner_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L142 | neighbors=[RDPScanner, .scan_target()] | lang=en
- "scanner_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L168 | neighbors=[RDPScanner, ._scan_port()] | lang=en
- "scanner_rsync_scanner_rsyncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L144 | neighbors=[RsyncScanner, .scan_target()] | lang=en
- "scanner_rsync_scanner_rsyncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L162 | neighbors=[RsyncScanner, ._scan_port()] | lang=en
- "scanner_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/scanner/run_all.py:L92 | neighbors=[run_all.py, main()] | lang=en
- "scanner_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/scanner/run_all.py:L106 | neighbors=[run_all.py, main()] | lang=en
- "scanner_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/scanner/run_all.py:L78 | neighbors=[run_all.py, main()] | lang=en
- "scanner_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L125 | neighbors=[scan_funnel.py, .run_host()] | lang=en
- "scanner_scan_funnel_rationale_73": "Canonical open-TCP set for a host = deduped, sorted union of every source." | kind=entity | source=probe/scanner/scan_funnel.py:L73 | neighbors=[reconcile_ports(), FunnelResult] | lang=en
- "scanner_scan_funnel_rationale_87": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/scanner/scan_funnel.py:L87 | neighbors=[route_ports(), _candidate_ports()] | lang=en
- "scanner_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L114 | neighbors=[.run_host(), _Scanner] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L512 | neighbors=[AdaptiveRateController, .wait()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L508 | neighbors=[AdaptiveRateController, .report_loss()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L501 | neighbors=[AdaptiveRateController, .report_success()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L524 | neighbors=[AdaptiveRateController, ._on_loss()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L518 | neighbors=[AdaptiveRateController, ._on_success()] | lang=en
- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L966 | neighbors=[BaseScanner, RateLimiter] | lang=en
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L974 | neighbors=[BaseScanner, ._guarded()] | lang=en
- "scanner_scanner_base_rationale_170": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/scanner/scanner_base.py:L170 | neighbors=[classify_os_error(), .networks()] | lang=en
- "scanner_scanner_base_rationale_205": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L205 | neighbors=[AdaptiveRateController, expand_targets()] | lang=pt

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-140.json

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
