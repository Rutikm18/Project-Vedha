# Node Description Batch 81 of 186

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

- "main_scripts_iot_scanner_probe_rtsp": "_probe_rtsp()" | kind=code-symbol | source=probe/main_scripts/iot_scanner.py:L214 | neighbors=[iot_scanner.py, .scan_target()]
- "main_scripts_ja4x_match_suspicious": "match_suspicious()" | kind=code-symbol | source=probe/main_scripts/ja4x.py:L117 | neighbors=[ja4x.py, Return a threat-intel label if this JA4…]
- "main_scripts_mass_scan_connectsweep_probe": "._probe()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L213 | neighbors=[_ConnectSweep, .scan_target()]
- "main_scripts_mass_scan_connectsweep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L229 | neighbors=[_ConnectSweep, ._probe()]
- "main_scripts_mass_scan_have_masscan": "_have_masscan()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L60 | neighbors=[mass_scan.py, run_mass_scan()]
- "main_scripts_mass_scan_masscan_records_to_results": "_masscan_records_to_results()" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L184 | neighbors=[mass_scan.py, run_mass_scan()]
- "main_scripts_mass_scan_masscanrun": "MasscanRun" | kind=code-symbol | source=probe/main_scripts/mass_scan.py:L51 | neighbors=[mass_scan.py, _run_masscan()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_fetch": "._fetch()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L205 | neighbors=[MCPAIScanner, ._probe_port()]
- "main_scripts_mcp_ai_scanner_mcpaiscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L315 | neighbors=[MCPAIScanner, ._probe_port()]
- "main_scripts_mcp_ai_scanner_model_count": "_model_count()" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L182 | neighbors=[mcp_ai_scanner.py, ._result()]
- "main_scripts_mcp_ai_scanner_noredirect": "_NoRedirect" | kind=code-symbol | source=probe/main_scripts/mcp_ai_scanner.py:L109 | neighbors=[mcp_ai_scanner.py, .redirect_request()]
- "main_scripts_mobile_scanner_adb_checksum": "_adb_checksum()" | kind=code-symbol | source=probe/main_scripts/mobile_scanner.py:L55 | neighbors=[mobile_scanner.py, _build_adb_cnxn()]
- "main_scripts_nmap_wrapper_parse_nmap_xml": "_parse_nmap_xml()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L154 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "main_scripts_nmap_wrapper_run_nmap": "_run_nmap()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L115 | neighbors=[nmap_wrapper.py, NmapExecutionError]
- "main_scripts_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=probe/main_scripts/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "main_scripts_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L74 | neighbors=[os_fingerprint.py, _icmp()]
- "main_scripts_os_fingerprint_build_icmp_timestamp": "build_icmp_timestamp()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L68 | neighbors=[os_fingerprint.py, _icmp()]
- "main_scripts_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L187 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…]
- "main_scripts_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L118 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "main_scripts_os_fingerprint_osfingerprintscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L255 | neighbors=[OSFingerprintScanner, fingerprint_os()]
- "main_scripts_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "main_scripts_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "main_scripts_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "main_scripts_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L276 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L346 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L127 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…]
- "main_scripts_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L207 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L200 | neighbors=[Requested ports that were never recorde…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L181 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L229 | neighbors=[.scan_target(), ScanMetrics]
- "main_scripts_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L78 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L84 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L64 | neighbors=[run_all.py, main()]
- "main_scripts_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L94 | neighbors=[scan_funnel.py, .run_host()]
- "main_scripts_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L180 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel]
- "main_scripts_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L83 | neighbors=[.run_host(), _Scanner]
- "main_scripts_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L377 | neighbors=[AdaptiveRateController, .wait()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L373 | neighbors=[AdaptiveRateController, .report_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L366 | neighbors=[AdaptiveRateController, .report_success()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L389 | neighbors=[AdaptiveRateController, ._on_loss()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-080.json

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
