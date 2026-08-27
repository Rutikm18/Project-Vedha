# Node Description Batch 105 of 236

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

- "scanner_rdp_scanner_rdpscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L102 | neighbors=[RDPScanner, .scan_target()] | lang=en
- "scanner_rdp_scanner_rdpscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L121 | neighbors=[RDPScanner, ._scan_port()] | lang=en
- "scanner_run_all_open_tcp_ports": "_open_tcp_ports()" | kind=code-symbol | source=probe/scanner/run_all.py:L88 | neighbors=[run_all.py, main()] | lang=en
- "scanner_run_all_ports_arg": "_ports_arg()" | kind=code-symbol | source=probe/scanner/run_all.py:L94 | neighbors=[run_all.py, main()] | lang=en
- "scanner_run_all_read_jsonl": "_read_jsonl()" | kind=code-symbol | source=probe/scanner/run_all.py:L74 | neighbors=[run_all.py, main()] | lang=en
- "scanner_scan_funnel_is_alive": "_is_alive()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L105 | neighbors=[scan_funnel.py, .run_host()] | lang=en
- "scanner_scan_funnel_scanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L94 | neighbors=[.run_host(), _Scanner] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_acquire": ".acquire()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L448 | neighbors=[AdaptiveRateController, .wait()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_on_loss": "._on_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L444 | neighbors=[AdaptiveRateController, .report_loss()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_on_success": "._on_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L437 | neighbors=[AdaptiveRateController, .report_success()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_report_loss": ".report_loss()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L460 | neighbors=[AdaptiveRateController, ._on_loss()] | lang=en
- "scanner_scanner_base_adaptiveratecontroller_report_success": ".report_success()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L454 | neighbors=[AdaptiveRateController, ._on_success()] | lang=en
- "scanner_scanner_base_assess_tarpit": "assess_tarpit()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L88 | neighbors=[scanner_base.py, Heuristic: is this host a tarpit / hone…] | lang=en
- "scanner_scanner_base_basescanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L745 | neighbors=[BaseScanner, RateLimiter] | lang=en
- "scanner_scanner_base_basescanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L753 | neighbors=[BaseScanner, ._guarded()] | lang=en
- "scanner_scanner_base_choose_source_port": "choose_source_port()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L68 | neighbors=[scanner_base.py, The TCP source port for probes. A FIXED…] | lang=en
- "scanner_scanner_base_jittered_delay": "jittered_delay()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L78 | neighbors=[scanner_base.py, A per-probe delay of `base` seconds ± u…] | lang=en
- "scanner_scanner_base_probe_payload": "probe_payload()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L61 | neighbors=[scanner_base.py, Benign, non-attributing payload for ICM…] | lang=en
- "scanner_scanner_base_rationale_170": "Map a connect()/socket-time OSError to (state, reason).      DNS failures (``soc" | kind=entity | source=probe/scanner/scanner_base.py:L170 | neighbors=[classify_os_error(), .networks()] | lang=en
- "scanner_scanner_base_rationale_205": "A self-tuning concurrency window, modelled on TCP congestion control (AIMD)," | kind=entity | source=probe/scanner/scanner_base.py:L205 | neighbors=[AdaptiveRateController, expand_targets()] | lang=pt
- "scanner_scanner_base_rationale_252": "Loads an allowlist of CIDRs / IPs / hostnames and decides whether a target     i" | kind=entity | source=probe/scanner/scanner_base.py:L252 | neighbors=[ScopeGuard, .window()] | lang=en
- "scanner_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L353 | neighbors=[.networks(), bracket_host()] | lang=en
- "scanner_scanner_base_rationale_359": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[_UDPProbeProtocol, BaseScanner] | lang=en
- "scanner_scanner_base_rationale_535": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L535 | neighbors=[BaseScanner, main_entrypoint()] | lang=pt
- "scanner_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=probe/scanner/scanner_base.py:L69 | neighbors=[choose_source_port(), ScopeGuard] | lang=en
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L240 | neighbors=[.write(), ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L344 | neighbors=[ScopeGuard, .in_scope()] | lang=en
- "scanner_scanner_base_user_agent": "user_agent()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L55 | neighbors=[scanner_base.py, HTTP/RTSP User-Agent to send — a generi…] | lang=en
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L85 | neighbors=[service_banner.py, match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L234 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=probe/scanner/service_enum.py:L601 | neighbors=[service_enum.py, local_topology()] | lang=en
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/scanner/service_enum.py:L456 | neighbors=[ServiceEnumScanner, ._probe_port()] | lang=en
- "scanner_service_enum_smb_dialects": "smb_dialects()" | kind=code-symbol | source=probe/scanner/service_enum.py:L293 | neighbors=[service_enum.py, Negotiate against 445; report whether S…] | lang=en
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/scanner/service_enum.py:L388 | neighbors=[service_enum.py, .scan_target()] | lang=en
- "scanner_service_enum_tls_accepts_old": "tls_accepts_old()" | kind=code-symbol | source=probe/scanner/service_enum.py:L258 | neighbors=[service_enum.py, Which deprecated TLS/SSL versions the s…] | lang=en
- "scanner_service_enum_tls_info": "tls_info()" | kind=code-symbol | source=probe/scanner/service_enum.py:L235 | neighbors=[service_enum.py, One permissive TLS handshake: negotiate…] | lang=en
- "scanner_smb_scanner_netbios_session": "_netbios_session()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L31 | neighbors=[smb_scanner.py, ._negotiate()] | lang=en
- "scanner_smb_scanner_smb1_negotiate": "_smb1_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L88 | neighbors=[smb_scanner.py, .scan_target()] | lang=en
- "scanner_smb_scanner_smb2_negotiate": "_smb2_negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L108 | neighbors=[smb_scanner.py, .scan_target()] | lang=en
- "scanner_smb_scanner_smbscanner_negotiate": "._negotiate()" | kind=code-symbol | source=probe/scanner/smb_scanner.py:L149 | neighbors=[SMBScanner, _netbios_session()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-104.json

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
