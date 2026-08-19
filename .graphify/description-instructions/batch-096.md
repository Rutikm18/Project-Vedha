# Node Description Batch 97 of 227

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

- "main_scripts_os_fingerprint_os_family_from_ttl": "os_family_from_ttl()" | kind=code-symbol | source=probe/main_scripts/os_fingerprint.py:L169 | neighbors=[os_fingerprint.py, infer_initial_ttl()]
- "main_scripts_passive_collector_coverage": "_coverage()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L158 | neighbors=[passive_collector.py, .run()]
- "main_scripts_passive_collector_is_readable": "_is_readable()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L351 | neighbors=[passive_collector.py, ._select()]
- "main_scripts_passive_collector_listener_error_code": "_listener_error_code()" | kind=code-symbol | source=probe/main_scripts/passive_collector.py:L150 | neighbors=[passive_collector.py, .run()]
- "main_scripts_port_scanner_portscanner_build": "._build()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L300 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_portscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L382 | neighbors=[PortScanner, ._attempt()]
- "main_scripts_port_scanner_scanmetrics_summary": ".summary()" | kind=code-symbol | source=probe/main_scripts/port_scanner.py:L232 | neighbors=[.scan_target(), ScanMetrics]
- "main_scripts_rdp_scanner_main": "main()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L126 | neighbors=[rdp_scanner.py, RDPScanner]
- "main_scripts_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L102 | neighbors=[RDPScanner, .scan_target()]
- "main_scripts_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/rdp_scanner.py:L121 | neighbors=[RDPScanner, ._scan_port()]
- "main_scripts_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L78 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L84 | neighbors=[run_all.py, main()]
- "main_scripts_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/main_scripts/run_all.py:L64 | neighbors=[run_all.py, main()]
- "main_scripts_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L94 | neighbors=[scan_funnel.py, .run_host()]
- "main_scripts_scan_funnel_scanfunnel_run": ".run()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L180 | neighbors=[Funnel many hosts with bounded concurre…, ScanFunnel]
- "main_scripts_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L83 | neighbors=[.run_host(), _Scanner]
- "main_scripts_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L448 | neighbors=[AdaptiveRateController, .wait()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L444 | neighbors=[AdaptiveRateController, .report_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L437 | neighbors=[AdaptiveRateController, .report_success()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L460 | neighbors=[AdaptiveRateController, ._on_loss()]
- "main_scripts_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L454 | neighbors=[AdaptiveRateController, ._on_success()]
- "main_scripts_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L88 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…]
- "main_scripts_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L745 | neighbors=[BaseScanner, RateLimiter]
- "main_scripts_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L753 | neighbors=[BaseScanner, ._guarded()]
- "main_scripts_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L68 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…]
- "main_scripts_scanner_base_jittered_delay": "jittered_delay()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L78 | neighbors=[scanner_base.py, A per-probe delay of `base` seconds ± u…]
- "main_scripts_scanner_base_probe_payload": "probe_payload()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L61 | neighbors=[scanner_base.py, Benign, non-attributing payload for ICM…]
- "main_scripts_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L240 | neighbors=[.write(), ScanResult]
- "main_scripts_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L344 | neighbors=[ScopeGuard, .in_scope()]
- "main_scripts_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L55 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…]
- "main_scripts_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L85 | neighbors=[service_banner.py, match_service()]
- "main_scripts_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/main_scripts/service_banner.py:L216 | neighbors=[ServiceBannerScanner, ._grab()]
- "main_scripts_service_enum_main": "main()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L601 | neighbors=[service_enum.py, local_topology()]
- "main_scripts_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L456 | neighbors=[ServiceEnumScanner, ._probe_port()]
- "main_scripts_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L293 | neighbors=[service_enum.py, Negotiate against 445; report whether S…]
- "main_scripts_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L388 | neighbors=[service_enum.py, .scan_target()]
- "main_scripts_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L258 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…]
- "main_scripts_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=probe/main_scripts/service_enum.py:L235 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…]
- "main_scripts_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()]
- "main_scripts_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/main_scripts/smb_scanner.py:L88 | neighbors=[smb_scanner.py, .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-096.json

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
