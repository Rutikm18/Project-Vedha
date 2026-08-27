# Node Description Batch 39 of 92

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

- "main_scripts_nmap_wrapper_validated_extra_args": "_validated_extra_args()" | kind=code-symbol | source=main_scripts/nmap_wrapper.py:L69 | neighbors=[nmap_wrapper.py, Allow tuning only; target, script, and …]
- "main_scripts_os_fingerprint_build_icmp_addrmask": "build_icmp_addrmask()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L76 | neighbors=[os_fingerprint.py, _icmp()]
- "main_scripts_os_fingerprint_icmp_supported": "icmp_supported()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L253 | neighbors=[os_fingerprint.py, True if we can open an ICMP socket (dat…]
- "main_scripts_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=main_scripts/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "main_scripts_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=main_scripts/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "main_scripts_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=main_scripts/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "main_scripts_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=main_scripts/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "main_scripts_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=main_scripts/port_scanner.py:L300 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=main_scripts/port_scanner.py:L382 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_resolve_profile": "resolve_profile()" | kind=code-symbol | source=main_scripts/port_scanner.py:L130 | neighbors=[port_scanner.py, Resolve a named scan profile to a concr…]
- "main_scripts_port_scanner_scanmetrics_duplicate_ports": ".duplicate_ports()" | kind=code-symbol | source=main_scripts/port_scanner.py:L210 | neighbors=[Ports recorded more than once (a port m…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_missing_ports": ".missing_ports()" | kind=code-symbol | source=main_scripts/port_scanner.py:L203 | neighbors=[Requested ports that were never recorde…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_record": ".record()" | kind=code-symbol | source=main_scripts/port_scanner.py:L184 | neighbors=[Tally exactly one terminal per-port obs…, ScanMetrics]
- "main_scripts_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=main_scripts/port_scanner.py:L232 | neighbors=[.scan_target(), ScanMetrics]
- "main_scripts_rdp_scanner_main": "main()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L126 | neighbors=[rdp_scanner.py, RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L102 | neighbors=[RDPScanner, .scan_target()]
- "main_scripts_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/rdp_scanner.py:L121 | neighbors=[RDPScanner, ._scan_port()]
- "main_scripts_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=main_scripts/run_all.py:L88 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=main_scripts/run_all.py:L94 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_rationale_47": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L47 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_48": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L48 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_49": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L49 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_52": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L52 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_53": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L53 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_55": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L55 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_rationale_56": "Run one scanner module as a subprocess, tee its JSONL to <name>.jsonl." | kind=entity | source=main_scripts/run_all.py:L56 | neighbors=[_run_stage(), ScanResult]
- "main_scripts_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=main_scripts/run_all.py:L74 | neighbors=[run_all.py, main()]
- "main_scripts_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L105 | neighbors=[scan_funnel.py, .run_host()]
- "main_scripts_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/scan_funnel.py:L94 | neighbors=[.run_host(), _Scanner]
- "main_scripts_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=main_scripts/scanner_base.py:L448 | neighbors=[AdaptiveRateController, .wait()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=main_scripts/scanner_base.py:L444 | neighbors=[AdaptiveRateController, .report_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=main_scripts/scanner_base.py:L437 | neighbors=[AdaptiveRateController, .report_success()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=main_scripts/scanner_base.py:L460 | neighbors=[AdaptiveRateController, ._on_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=main_scripts/scanner_base.py:L454 | neighbors=[AdaptiveRateController, ._on_success()]
- "main_scripts_scanner_base_adaptiveratecontroller_window": ".window()" | kind=code-symbol | source=main_scripts/scanner_base.py:L433 | neighbors=[AdaptiveRateController, Current integer window (>= min_window).]
- "main_scripts_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=main_scripts/scanner_base.py:L88 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…]
- "main_scripts_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=main_scripts/scanner_base.py:L745 | neighbors=[BaseScanner, RateLimiter]
- "main_scripts_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=main_scripts/scanner_base.py:L753 | neighbors=[BaseScanner, ._guarded()]
- "main_scripts_scanner_base_bracket_host": "bracket_host()" | kind=code-symbol | source=main_scripts/scanner_base.py:L647 | neighbors=[scanner_base.py, Wrap an IPv6 literal in [] for a URL au…]
- "main_scripts_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=main_scripts/scanner_base.py:L68 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-038.json

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
