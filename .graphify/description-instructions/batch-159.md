# Node Description Batch 160 of 380

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

- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/scanner/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/scanner/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L206 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L316 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/scanner/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "scanner_msrpc_scanner_msrpcscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L144 | neighbors=[MSRPCScanner, .scan_target()]
- "scanner_msrpc_scanner_msrpcscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/msrpc_scanner.py:L167 | neighbors=[MSRPCScanner, ._scan_port()]
- "scanner_nfs_scanner_nfsscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L259 | neighbors=[NFSScanner, .scan_target()]
- "scanner_nfs_scanner_nfsscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L277 | neighbors=[NFSScanner, ._scan_port()]
- "scanner_nfs_scanner_recv_exact": "_recv_exact()" | kind=code-symbol | source=probe/scanner/nfs_scanner.py:L156 | neighbors=[nfs_scanner.py, _recv_record()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L160 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/scanner/nmap_wrapper.py:L121 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/scanner/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "scanner_port_scanner_portscanner_retain_result": "._retain_result()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L642 | neighbors=[PortScanner, Must this result OBJECT outlive the por…]
- "scanner_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L315 | neighbors=[.scan_target(), ScanMetrics]
- "scanner_printer_scanner_ipp_attr": "_ipp_attr()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L49 | neighbors=[printer_scanner.py, build_ipp_get_printer_attributes()]
- "scanner_printer_scanner_printerscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L138 | neighbors=[PrinterScanner, .scan_target()]
- "scanner_printer_scanner_printerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/printer_scanner.py:L155 | neighbors=[PrinterScanner, ._scan_port()]
- "scanner_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L173 | neighbors=[rdp_scanner.py, RDPScanner]
- "scanner_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L142 | neighbors=[RDPScanner, .scan_target()]
- "scanner_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L168 | neighbors=[RDPScanner, ._scan_port()]
- "scanner_rsync_scanner_rsyncscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L144 | neighbors=[RsyncScanner, .scan_target()]
- "scanner_rsync_scanner_rsyncscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/rsync_scanner.py:L162 | neighbors=[RsyncScanner, ._scan_port()]
- "scanner_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/scanner/run_all.py:L92 | neighbors=[run_all.py, main()]
- "scanner_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/scanner/run_all.py:L106 | neighbors=[run_all.py, main()]
- "scanner_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/scanner/run_all.py:L78 | neighbors=[run_all.py, main()]
- "scanner_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L125 | neighbors=[scan_funnel.py, .run_host()]
- "scanner_scan_funnel_rationale_73": "Canonical open-TCP set for a host = deduped, sorted union of every source." | kind=entity | source=probe/scanner/scan_funnel.py:L73 | neighbors=[reconcile_ports(), FunnelResult]
- "scanner_scan_funnel_rationale_87": "Map a host's open ports onto the deep-scanner routes that handle them.     Retur" | kind=entity | source=probe/scanner/scan_funnel.py:L87 | neighbors=[route_ports(), _candidate_ports()]
- "scanner_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L114 | neighbors=[.run_host(), _Scanner]
- "scanner_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L534 | neighbors=[AdaptiveRateController, .wait()]
- "scanner_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L528 | neighbors=[AdaptiveRateController, .report_loss()]
- "scanner_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L521 | neighbors=[AdaptiveRateController, .report_success()]
- "scanner_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L546 | neighbors=[AdaptiveRateController, ._on_loss()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-159.json

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
