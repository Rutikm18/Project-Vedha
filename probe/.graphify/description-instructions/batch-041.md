# Node Description Batch 42 of 92

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

- "scanner_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=scanner/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "scanner_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "scanner_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=scanner/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=scanner/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "scanner_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=scanner/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "scanner_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L206 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L316 | neighbors=[MCPAIScanner, ._probe_port()]
- "scanner_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L183 | neighbors=[mcp_ai_scanner.py, ._result()]
- "scanner_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=scanner/mcp_ai_scanner.py:L110 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "scanner_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=scanner/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "scanner_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=scanner/nmap_wrapper.py:L154 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=scanner/nmap_wrapper.py:L115 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "scanner_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=scanner/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "scanner_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=scanner/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "scanner_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=scanner/os_fingerprint.py:L253 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…]
- "scanner_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=scanner/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "scanner_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=scanner/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "scanner_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=scanner/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "scanner_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=scanner/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "scanner_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=scanner/port_scanner.py:L300 | neighbors=[PortScanner, ._attempt()]
- "scanner_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/port_scanner.py:L382 | neighbors=[PortScanner, ._attempt()]
- "scanner_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=scanner/port_scanner.py:L130 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…]
- "scanner_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=scanner/port_scanner.py:L210 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=scanner/port_scanner.py:L203 | neighbors=[Requested ports that were never recorde…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=scanner/port_scanner.py:L184 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics]
- "scanner_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=scanner/port_scanner.py:L232 | neighbors=[.scan_target(), ScanMetrics]
- "scanner_rdp_scanner_main": "main()" | kind=code-symbol | source=scanner/rdp_scanner.py:L126 | neighbors=[rdp_scanner.py, RDPScanner]
- "scanner_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=scanner/rdp_scanner.py:L102 | neighbors=[RDPScanner, .scan_target()]
- "scanner_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/rdp_scanner.py:L121 | neighbors=[RDPScanner, ._scan_port()]
- "scanner_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=scanner/run_all.py:L88 | neighbors=[run_all.py, main()]
- "scanner_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=scanner/run_all.py:L94 | neighbors=[run_all.py, main()]
- "scanner_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=scanner/run_all.py:L74 | neighbors=[run_all.py, main()]
- "scanner_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=scanner/scan_funnel.py:L105 | neighbors=[scan_funnel.py, .run_host()]
- "scanner_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=scanner/scan_funnel.py:L94 | neighbors=[.run_host(), _Scanner]
- "scanner_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=scanner/scanner_base.py:L448 | neighbors=[AdaptiveRateController, .wait()]
- "scanner_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=scanner/scanner_base.py:L444 | neighbors=[AdaptiveRateController, .report_loss()]
- "scanner_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=scanner/scanner_base.py:L437 | neighbors=[AdaptiveRateController, .report_success()]
- "scanner_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=scanner/scanner_base.py:L460 | neighbors=[AdaptiveRateController, ._on_loss()]
- "scanner_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=scanner/scanner_base.py:L454 | neighbors=[AdaptiveRateController, ._on_success()]
- "scanner_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=scanner/scanner_base.py:L433 | neighbors=[AdaptiveRateController, Current integer window (>= min_window).]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-041.json

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
