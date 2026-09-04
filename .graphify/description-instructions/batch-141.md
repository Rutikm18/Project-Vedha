# Node Description Batch 142 of 332

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
- "scanner_scanner_base_rationale_353": "Read-only view of allowed networks (for CIDR-level engines)." | kind=entity | source=probe/scanner/scanner_base.py:L353 | neighbors=[.networks(), bracket_host()] | lang=en
- "scanner_scanner_base_rationale_359": "One-shot datagram protocol backing `async_udp_probe`. Resolves its future     wi" | kind=entity | source=probe/scanner/scanner_base.py:L359 | neighbors=[_UDPProbeProtocol, BaseScanner] | lang=en
- "scanner_scanner_base_rationale_535": "Subclasses implement `scan_target(self, target)` (async), returning a list     o" | kind=entity | source=probe/scanner/scanner_base.py:L535 | neighbors=[BaseScanner, main_entrypoint()] | lang=pt
- "scanner_scanner_base_rationale_69": "The TCP source port for probes. A FIXED port (e.g. 53/88) lets a scan slip     p" | kind=entity | source=probe/scanner/scanner_base.py:L69 | neighbors=[choose_source_port(), ScopeGuard] | lang=en
- "scanner_scanner_base_resolve_project_tz": "_resolve_project_tz()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L66 | neighbors=[scanner_base.py, The project timezone, degrading safely …] | lang=en
- "scanner_scanner_base_scanresult_to_json": ".to_json()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L304 | neighbors=[.write(), ScanResult] | lang=en
- "scanner_scanner_base_scopeguard_filter": ".filter()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L408 | neighbors=[ScopeGuard, .in_scope()] | lang=en
- "scanner_scanner_base_sendpacer_observe_round": ".observe_round()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L590 | neighbors=[Fold one send/collect round's reply rat…, SendPacer] | lang=en
- "scanner_scanner_base_sendpacer_pace": ".pace()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L577 | neighbors=[Block just long enough to hold `rate` p…, SendPacer] | lang=en
- "scanner_scanner_base_sendpacer_stats": ".stats()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L606 | neighbors=[Pacing telemetry for the scan summary (…, SendPacer] | lang=en
- "scanner_scanner_registry_is_verified": "is_verified()" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L97 | neighbors=[scanner_registry.py, True only for a scanner explicitly on t…] | lang=en
- "scanner_scanner_registry_verification_report": "verification_report()" | kind=code-symbol | source=probe/scanner/scanner_registry.py:L107 | neighbors=[scanner_registry.py, The scanner-module trust view: which sc…] | lang=en
- "scanner_service_banner_dec": "_dec()" | kind=code-symbol | source=probe/scanner/service_banner.py:L229 | neighbors=[service_banner.py, match_service()] | lang=en
- "scanner_service_banner_servicebannerscanner_connect": "._connect()" | kind=code-symbol | source=probe/scanner/service_banner.py:L339 | neighbors=[ServiceBannerScanner, ._rung()] | lang=en
- "scanner_service_banner_servicebannerscanner_ladder_for": "._ladder_for()" | kind=code-symbol | source=probe/scanner/service_banner.py:L416 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_banner_servicebannerscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/service_banner.py:L524 | neighbors=[ServiceBannerScanner, ._grab()] | lang=en
- "scanner_service_banner_tls_context": "_tls_context()" | kind=code-symbol | source=probe/scanner/service_banner.py:L50 | neighbors=[service_banner.py, A permissive client context for FINGERP…] | lang=en
- "scanner_service_enum_main": "main()" | kind=code-symbol | source=probe/scanner/service_enum.py:L630 | neighbors=[service_enum.py, local_topology()] | lang=en
- "scanner_service_enum_serviceenumscanner_open": "._open()" | kind=code-symbol | source=probe/scanner/service_enum.py:L485 | neighbors=[ServiceEnumScanner, ._probe_port()] | lang=en
- "scanner_service_enum_tags_for": "tags_for()" | kind=code-symbol | source=probe/scanner/service_enum.py:L417 | neighbors=[service_enum.py, .scan_target()] | lang=en
- "scanner_smb_enum_scanner_smbenumscanner_init": ".__init__()" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L221 | neighbors=[SMBEnumScanner, parse_rid_ranges()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-141.json

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
